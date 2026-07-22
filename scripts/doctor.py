#!/usr/bin/env python3
"""Cutlin doctor — diagnose a local install, and configure provider keys.

Two modes:

    python scripts/doctor.py              # diagnose everything, fix nothing
    python scripts/doctor.py --configure  # interactive key setup wizard

The doctor exists because the failure modes on a fresh local install are
almost all *silent*: a key that authenticates but is attached to the wrong
project, a voice id that was never set, a font that quietly falls back
because a CDN is unreachable from your network. None of these raise an
error until you are ten minutes into a render.

Every key probe here is free: search endpoints, queue submissions that get
rejected at validation, or (for TTS) a two-character synthesis. Running the
doctor does not spend money.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = REPO_ROOT / ".env"

# ANSI, matching the Studio's two-accent terminal theme:
# amber = needs your attention, phosphor green = done.
AMBER = "\033[38;5;214m"
GREEN = "\033[38;5;120m"
RED = "\033[38;5;203m"
DIM = "\033[2m"
BOLD = "\033[1m"
OFF = "\033[0m"

OK = f"{GREEN}✓{OFF}"
WARN = f"{AMBER}!{OFF}"
BAD = f"{RED}✗{OFF}"


def _supports_color() -> bool:
    return sys.stdout.isatty() and os.environ.get("NO_COLOR") is None


if not _supports_color():
    AMBER = GREEN = RED = DIM = BOLD = OFF = ""
    OK, WARN, BAD = "[ok]", "[!]", "[x]"


def header(text: str) -> None:
    print(f"\n{BOLD}{text}{OFF}")
    print(f"{DIM}{'─' * 66}{OFF}")


# ---------------------------------------------------------------------------
# Capability bundles — what a key actually buys you, in plain language.
# ---------------------------------------------------------------------------

BUNDLES: list[dict] = [
    {
        "id": "fal",
        "title": "视频与图像生成 / Video + image generation",
        "keys": ["FAL_KEY"],
        "unlocks": "FLUX 出图、Kling/Veo/Wan/LTX-2/PixVerse 出视频",
        "cost": "按量付费，出一张图约 $0.025，出 5 秒视频 $0.1-0.5",
        "signup": "https://fal.ai/dashboard/keys",
        "optional": True,
    },
    {
        "id": "doubao",
        "title": "中文语音合成 / Chinese TTS",
        "keys": ["DOUBAO_SPEECH_API_KEY", "DOUBAO_SPEECH_VOICE_TYPE"],
        "unlocks": "豆包 Seed-TTS 2.0 中文旁白（带词级时间戳）",
        "cost": "有免费额度，超出后按字符计费",
        "signup": "火山引擎控制台 → 语音技术 → 大模型语音合成",
        "optional": True,
    },
    {
        "id": "stock",
        "title": "素材库与配乐 / Stock footage + music",
        "keys": ["PEXELS_API_KEY", "PIXABAY_API_KEY"],
        "unlocks": "真实素材检索、免版税配乐",
        "cost": "完全免费",
        "signup": "https://www.pexels.com/api/ · https://pixabay.com/api/docs/",
        "optional": True,
    },
]


# ---------------------------------------------------------------------------
# Runtime checks
# ---------------------------------------------------------------------------


def check_runtime() -> list[str]:
    """Check the binaries a render actually shells out to."""
    header("运行时依赖 / Runtime")
    problems: list[str] = []

    py = sys.version_info
    if py >= (3, 10):
        print(f"  {OK} Python {py.major}.{py.minor}.{py.micro}")
    else:
        print(f"  {BAD} Python {py.major}.{py.minor} — 需要 3.10 以上")
        problems.append("升级 Python 到 3.10+")

    for binary, why, fix in [
        ("ffmpeg", "音频装配与最终编码", "https://ffmpeg.org/download.html"),
        ("ffprobe", "渲染后质检探针", "随 ffmpeg 一同安装"),
        ("node", "Remotion 渲染引擎", "https://nodejs.org (需要 18+)"),
        ("npx", "调用 Remotion CLI", "随 Node.js 一同安装"),
    ]:
        path = shutil.which(binary)
        if path:
            print(f"  {OK} {binary:8} {DIM}{path}{OFF}")
        else:
            print(f"  {BAD} {binary:8} 缺失 — {why}。安装：{fix}")
            problems.append(f"安装 {binary}")

    node = shutil.which("node")
    if node:
        try:
            out = subprocess.run(
                [node, "--version"], capture_output=True, text=True, timeout=10
            ).stdout.strip()
            major = int(out.lstrip("v").split(".")[0])
            if major < 18:
                print(f"  {BAD} Node {out} 过低 — Remotion 需要 18+")
                problems.append("升级 Node.js 到 18+")
        except Exception:  # noqa: BLE001
            pass

    deps = REPO_ROOT / "remotion-composer" / "node_modules"
    if deps.is_dir():
        print(f"  {OK} 渲染引擎依赖已安装")
    else:
        print(f"  {BAD} remotion-composer/node_modules 缺失 — 跑 `make setup`")
        problems.append("执行 make setup 安装渲染引擎依赖")

    return problems


def check_fonts() -> list[str]:
    """Check CJK font availability and Google Fonts reachability.

    Remotion loads its display face through @remotion/google-fonts, which
    resolves to fonts.gstatic.com at render time. On a network where that
    host is unreachable the render does not fail loudly — it silently falls
    back, and you find out when you watch the output.
    """
    header("字体 / Fonts")
    problems: list[str] = []

    cjk_count = 0
    if shutil.which("fc-list"):
        try:
            out = subprocess.run(
                ["fc-list", ":lang=zh"], capture_output=True, text=True, timeout=15
            ).stdout
            cjk_count = len([line for line in out.splitlines() if line.strip()])
        except Exception:  # noqa: BLE001
            pass
        if cjk_count:
            print(f"  {OK} 系统中文字体 {cjk_count} 款")
        else:
            print(f"  {BAD} 未找到中文字体 — 中文字幕会变成方框")
            problems.append("安装中文字体（如 Noto Sans CJK SC）")
    else:
        print(f"  {WARN} 无 fc-list，跳过系统字体检查（macOS/Windows 通常自带中文字体）")

    reachable = _probe_url("https://fonts.gstatic.com/", timeout=6)
    if reachable:
        print(f"  {OK} fonts.gstatic.com 可达")
    else:
        print(f"  {WARN} fonts.gstatic.com 不可达")
        print(
            f"      {DIM}渲染层通过 @remotion/google-fonts 在渲染时拉取字体文件。"
            f"该地址不通时不会报错，只会静默回退成默认字体，"
            f"成片的标题字形会和预期不一致。{OFF}"
        )
        problems.append(
            "网络无法访问 Google Fonts：渲染前请确认标题字体是否被静默回退"
        )

    return problems


def _probe_url(url: str, timeout: int = 8) -> bool:
    try:
        import requests

        requests.head(url, timeout=timeout)
        return True
    except Exception:  # noqa: BLE001
        return False


# ---------------------------------------------------------------------------
# Live key probes — all free
# ---------------------------------------------------------------------------


def probe_fal(key: str) -> tuple[bool, str]:
    """Submit an empty payload to the fal queue.

    The gateway does not validate payloads at submit time: a malformed
    request is accepted, then completes carrying a validation error, and
    nothing is billed. That makes it a free, reliable auth probe.
    """
    try:
        import requests

        r = requests.post(
            "https://queue.fal.run/fal-ai/flux/dev",
            headers={"Authorization": f"Key {key}", "Content-Type": "application/json"},
            json={},
            timeout=20,
        )
        if r.status_code in (401, 403):
            return False, "密钥无效或已撤销"
        if r.status_code in (200, 422):
            return True, "认证通过"
        return False, f"意外响应 HTTP {r.status_code}"
    except Exception as exc:  # noqa: BLE001
        return False, f"网络错误: {str(exc)[:60]}"


def probe_doubao(key: str, voice: str) -> tuple[bool, str]:
    """Synthesize two characters. Catches the failure modes a format check
    cannot see: service not activated, key attached to the wrong project,
    missing voice id."""
    if not voice:
        return False, "缺少 DOUBAO_SPEECH_VOICE_TYPE（音色 ID），密钥本身无法单独验证"
    try:
        sys.path.insert(0, str(REPO_ROOT))
        os.environ["DOUBAO_SPEECH_API_KEY"] = key
        os.environ["DOUBAO_SPEECH_VOICE_TYPE"] = voice
        from tools.tool_registry import registry

        registry.discover()
        tool = registry.get("doubao_tts")
        if tool is None:
            return False, "找不到 doubao_tts 工具"
        result = tool.execute({"text": "测试"})
        if result.success:
            out = (result.data or {}).get("output")
            if out and Path(out).exists():
                Path(out).unlink(missing_ok=True)
                Path(str(out) + ".json").unlink(missing_ok=True)
            return True, "合成成功"
        err = str(getattr(result, "error", ""))
        if "not granted" in err or "55000000" in err:
            return False, (
                "密钥有效，但账号未开通「大模型语音合成」，"
                "或密钥所属项目与开通服务的项目不一致"
            )
        if "503" in err:
            return False, "服务瞬时不可用（503），稍后重试即可"
        return False, err[:90]
    except Exception as exc:  # noqa: BLE001
        return False, f"{str(exc)[:80]}"


def probe_pexels(key: str) -> tuple[bool, str]:
    try:
        import requests

        r = requests.get(
            "https://api.pexels.com/v1/search",
            headers={"Authorization": key},
            params={"query": "test", "per_page": 1},
            timeout=15,
        )
        if r.status_code == 200:
            return True, "认证通过"
        if r.status_code in (401, 403):
            return False, "密钥无效"
        return False, f"HTTP {r.status_code}"
    except Exception as exc:  # noqa: BLE001
        return False, f"网络错误: {str(exc)[:60]}"


def probe_pixabay(key: str) -> tuple[bool, str]:
    try:
        import requests

        r = requests.get(
            "https://pixabay.com/api/",
            params={"key": key, "q": "test", "per_page": 3},
            timeout=15,
        )
        if r.status_code == 200:
            return True, "认证通过"
        if r.status_code in (400, 401, 403):
            return False, "密钥无效"
        return False, f"HTTP {r.status_code}"
    except Exception as exc:  # noqa: BLE001
        return False, f"网络错误: {str(exc)[:60]}"


PROBES = {
    "FAL_KEY": lambda env: probe_fal(env.get("FAL_KEY", "")),
    "DOUBAO_SPEECH_API_KEY": lambda env: probe_doubao(
        env.get("DOUBAO_SPEECH_API_KEY", ""), env.get("DOUBAO_SPEECH_VOICE_TYPE", "")
    ),
    "PEXELS_API_KEY": lambda env: probe_pexels(env.get("PEXELS_API_KEY", "")),
    "PIXABAY_API_KEY": lambda env: probe_pixabay(env.get("PIXABAY_API_KEY", "")),
}


# ---------------------------------------------------------------------------
# .env handling — never prints a secret back
# ---------------------------------------------------------------------------


def read_env() -> dict[str, str]:
    env: dict[str, str] = {}
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            env[k.strip()] = v.strip()
    # Process environment wins, matching how the tools resolve keys.
    for k in list(PROBES) + ["DOUBAO_SPEECH_VOICE_TYPE"]:
        if os.environ.get(k):
            env[k] = os.environ[k]
    return env


def write_env(updates: dict[str, str]) -> None:
    """Merge updates into .env, preserving comments and unrelated lines."""
    lines = (
        ENV_PATH.read_text(encoding="utf-8").splitlines()
        if ENV_PATH.exists()
        else ["# Cutlin local configuration — never commit this file", ""]
    )
    remaining = dict(updates)
    out: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and "=" in stripped:
            key = stripped.partition("=")[0].strip()
            if key in remaining:
                out.append(f"{key}={remaining.pop(key)}")
                continue
        out.append(line)
    for key, value in remaining.items():
        out.append(f"{key}={value}")
    ENV_PATH.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")
    ENV_PATH.chmod(0o600)


def mask(value: str) -> str:
    if not value:
        return ""
    if len(value) <= 8:
        return "*" * len(value)
    return f"{value[:4]}{'*' * 8}{value[-4:]}"


# ---------------------------------------------------------------------------
# Diagnose
# ---------------------------------------------------------------------------


def check_keys(env: dict[str, str], live: bool = True) -> list[str]:
    header("供应商密钥 / Provider keys")
    problems: list[str] = []

    if live:
        try:
            import requests  # noqa: F401
        except ImportError:
            # Report the missing dependency once, rather than letting every
            # probe fail separately and look like N unrelated key problems.
            print(f"  {BAD} 缺少 requests 依赖，无法联网验证密钥")
            print(f"      {DIM}跑 `make setup` 装齐依赖，或用 `make doctor-offline` 跳过验证{OFF}")
            live = False
            problems.append("安装 Python 依赖（make setup）后才能联网验证密钥")

    for bundle in BUNDLES:
        primary = bundle["keys"][0]
        value = env.get(primary, "")
        if not value:
            print(f"  {DIM}○ {bundle['title']}{OFF}")
            print(f"      {DIM}未配置 — 解锁：{bundle['unlocks']}{OFF}")
            continue

        print(f"  {BOLD}{bundle['title']}{OFF}")
        for key in bundle["keys"]:
            v = env.get(key, "")
            if not v:
                print(f"      {WARN} {key} 未设置")
                continue
            if not live or key not in PROBES:
                print(f"      {OK} {key} = {mask(v)} {DIM}(未联网验证){OFF}")
                continue
            ok, detail = PROBES[key](env)
            if ok:
                print(f"      {OK} {key} = {mask(v)} — {detail}")
            else:
                print(f"      {BAD} {key} = {mask(v)} — {detail}")
                problems.append(f"{key}: {detail}")
    return problems


def check_tools() -> list[str]:
    header("工具池 / Tool registry")
    try:
        sys.path.insert(0, str(REPO_ROOT))
        from tools.tool_registry import registry

        registry.discover()
        env = registry.support_envelope()
        available = sum(1 for v in env.values() if v.get("status") == "available")
        print(f"  {OK} 已注册 {len(env)} 件工具，其中 {GREEN}{available}{OFF} 件当前可用")
        print(f"      {DIM}未可用的工具是缺对应密钥而静默下架的，不是故障{OFF}")
        if available == 0:
            return ["工具池为空，检查 Python 依赖是否装全"]
    except Exception as exc:  # noqa: BLE001
        print(f"  {BAD} 工具池加载失败: {str(exc)[:90]}")
        return ["工具池无法加载，跑 `make setup` 重装依赖"]
    return []


def diagnose(live: bool = True) -> int:
    print(f"\n{BOLD}Cutlin 环境体检{OFF}  {DIM}{REPO_ROOT}{OFF}")
    problems: list[str] = []
    problems += check_runtime()
    problems += check_fonts()
    problems += check_keys(read_env(), live=live)
    problems += check_tools()

    header("结论 / Verdict")
    if not problems:
        print(f"  {OK} 一切正常，可以开工。")
        print(f"      {DIM}零成本档随时可跑；配了密钥的档位也已验证可用。{OFF}")
        return 0
    print(f"  {WARN} 发现 {len(problems)} 项待处理：\n")
    for i, p in enumerate(problems, 1):
        print(f"    {i}. {p}")
    print(f"\n  {DIM}密钥类问题可以跑 `python scripts/doctor.py --configure` 逐项修。{OFF}")
    return 1


# ---------------------------------------------------------------------------
# Configure wizard
# ---------------------------------------------------------------------------


def configure() -> int:
    print(f"\n{BOLD}Cutlin 密钥配置向导{OFF}")
    print(
        f"{DIM}每输入一把密钥都会立刻联网验证，验证全部免费。"
        f"密钥只写入本地 .env（权限 600，已在 .gitignore 中）。"
        f"直接回车 = 跳过该项。{OFF}"
    )

    if not sys.stdin.isatty():
        print(f"\n  {BAD} 当前不是交互式终端，无法运行向导。")
        print(f"      在本机终端里执行：python scripts/doctor.py --configure")
        return 1

    env = read_env()
    updates: dict[str, str] = {}

    for bundle in BUNDLES:
        header(bundle["title"])
        print(f"  解锁：{bundle['unlocks']}")
        print(f"  成本：{bundle['cost']}")
        print(f"  申请：{DIM}{bundle['signup']}{OFF}")

        primary = bundle["keys"][0]
        if env.get(primary):
            answer = input(f"\n  已配置 {mask(env[primary])}，重新设置？[y/N] ").strip().lower()
            if answer != "y":
                continue

        pending: dict[str, str] = {}
        for key in bundle["keys"]:
            hint = ""
            if key == "DOUBAO_SPEECH_VOICE_TYPE":
                hint = f" {DIM}(音色 ID，如 zh_female_vv_uranus_bigtts){OFF}"
            value = input(f"  {key}{hint}: ").strip()
            if value:
                pending[key] = value

        if not pending:
            print(f"  {DIM}已跳过{OFF}")
            continue

        merged = {**env, **updates, **pending}
        probe_key = next((k for k in bundle["keys"] if k in PROBES), None)
        if probe_key and merged.get(probe_key):
            print(f"  {DIM}验证中…{OFF}", end="\r")
            ok, detail = PROBES[probe_key](merged)
            print(" " * 30, end="\r")
            if ok:
                print(f"  {OK} 验证通过 — {detail}")
                updates.update(pending)
            else:
                print(f"  {BAD} 验证失败 — {detail}")
                keep = input("  仍然保存？[y/N] ").strip().lower()
                if keep == "y":
                    updates.update(pending)
        else:
            updates.update(pending)

    if not updates:
        print(f"\n  {DIM}没有改动。{OFF}")
        return 0

    write_env(updates)
    print(f"\n  {OK} 已写入 {ENV_PATH}（权限 600）")
    print(f"      {DIM}更新了 {len(updates)} 项：{', '.join(updates)}{OFF}")

    for key in updates:
        os.environ[key] = updates[key]
    check_tools()
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Diagnose a Cutlin install, or configure provider keys."
    )
    parser.add_argument(
        "--configure", action="store_true", help="交互式配置供应商密钥"
    )
    parser.add_argument(
        "--offline", action="store_true", help="跳过所有联网验证，只做本地检查"
    )
    args = parser.parse_args()
    if args.configure:
        return configure()
    return diagnose(live=not args.offline)


if __name__ == "__main__":
    raise SystemExit(main())
