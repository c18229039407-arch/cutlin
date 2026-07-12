#!/usr/bin/env bash
# Cutlin Studio 观测端 — macOS 双击启动（Linux 亦可直接运行）
cd "$(dirname "$0")"

# 优先使用项目虚拟环境
if [ -x ".venv/bin/python" ]; then
  PY=".venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then
  PY="python3"
else
  echo "未找到 Python，请先安装 Python 3.10+：https://www.python.org/downloads/"
  read -r -p "按回车键退出..." _
  exit 1
fi

echo "正在启动 Cutlin Studio 观测端..."
"$PY" -m backlot open || {
  echo ""
  echo "启动失败。请确认已在本目录执行过 make setup（或 pip install -r requirements.txt）。"
  read -r -p "按回车键退出..." _
  exit 1
}
