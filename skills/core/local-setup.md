# Local Setup & Diagnosis

`scripts/doctor.py` diagnoses a local install and configures provider keys.
Wired into the Makefile:

```bash
make doctor          # diagnose everything, fix nothing (exits 1 on problems)
make doctor-offline  # local checks only, no network probes
make configure       # interactive key setup wizard
```

## Why this exists

Almost every failure mode on a fresh local install is **silent**:

- a key that authenticates but is attached to the wrong project, so every
  call returns `resource not granted` from deep inside a tool;
- a TTS key with no voice id set, which fails only at synthesis time;
- a font CDN that is unreachable from your network, so the render does not
  fail — it quietly falls back and you find out when you watch the output;
- a tool that "disappeared" because its key is missing, which looks
  identical to a tool that is broken.

None of these raise an error until you are minutes into a render. The doctor
surfaces them in seconds, before anything is spent.

## What it checks

**Runtime** — Python ≥3.10, ffmpeg, ffprobe, node ≥18, npx, and whether
`remotion-composer/node_modules` is installed.

**Fonts** — system CJK font count (missing fonts turn Chinese captions into
tofu boxes), and reachability of `fonts.gstatic.com`. The render layer loads
its display face through `@remotion/google-fonts`, which resolves to that
host **at render time**; on a network where it is blocked the render silently
falls back to a default face. This is a real localization risk for users in
mainland China, and it is why the check exists.

**Keys** — live probes, all free:

| Key | Probe | Cost |
|-----|-------|------|
| `FAL_KEY` | empty payload to the fal queue | free — the gateway accepts it, then completes with a validation error, and bills nothing |
| `DOUBAO_SPEECH_API_KEY` | two-character synthesis | negligible; the only way to catch service-not-activated and project-mismatch |
| `PEXELS_API_KEY` | search, `per_page=1` | free |
| `PIXABAY_API_KEY` | search, `per_page=3` | free |

The fal probe deserves a note: fal's queue gateway does not validate payloads
at submit time, so a malformed request is accepted and later completes
carrying a `detail` validation error without generating anything. That makes
it a reliable, zero-cost auth probe — and, separately, a way to read an
endpoint's required fields without paying to discover them.

**Tools** — registered count vs currently-available count, with a note that
unavailable tools are keyless-and-parked, not broken.

## The configure wizard

`make configure` walks the capability bundles (video+image generation,
Chinese TTS, stock footage+music), and for each one shows what it unlocks and
what it costs before asking for anything. Every key entered is probed live
before it is written; a failed probe prints the *specific* reason rather than
"invalid key", and you can still save it deliberately.

Keys are written to `.env` with mode `600`, merged into the existing file so
comments and unrelated entries survive. Secrets are never echoed back in
full — output is masked to first four and last four characters. `.env` is in
`.gitignore`; nothing here changes that.

The wizard refuses to run without a TTY and says so, rather than hanging on
an unreadable stdin.

## Failure-mode reference

Diagnoses the doctor prints, and what they actually mean:

- **`密钥无效或已撤销`** — 401/403 from the provider. The key string is wrong,
  or it was rotated.
- **`账号未开通「大模型语音合成」，或密钥所属项目与开通服务的项目不一致`** —
  Volcengine returns error `55000000 resource not granted`. The key is valid;
  the *account* has not enabled the Seed-TTS resource, or the key belongs to a
  different project than the one where it was enabled. Fixing this is a
  console action, not a code change.
- **`缺少 DOUBAO_SPEECH_VOICE_TYPE`** — the TTS tool requires a voice id and
  cannot verify the key without one.
- **`服务瞬时不可用（503）`** — transient; the provider's CDN occasionally
  drops the download leg of an otherwise successful job. Retry.
- **`fonts.gstatic.com 不可达`** — see Fonts above. Not fatal, but check the
  title typography in the output before shipping.

## Exit codes

`0` clean, `1` problems found — so `make doctor` can gate CI or a deploy
script. `--offline` skips every network probe for air-gapped checks.
