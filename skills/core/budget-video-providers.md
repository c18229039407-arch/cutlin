# Budget-Tier Cloud Video Providers (fal channel)

Field guide for the three budget/mid-tier video generators added alongside the
premium fal tools (kling_video / veo_video / minimax_video). All three share
FAL_KEY, the queue API, and `run_fal_queue_job` in `tools/video/_shared.py`.
Every spec below was verified by real generation on 2026-07-16.

## When to reach for this tier

Use the ladder, not a single rung:

1. **Draft loop** — iterate prompts and motion ideas on `ltx2_video_fal`
   (cheapest, fastest, 1080p output verified at ~6s clips).
2. **Volume shots** — B-roll and secondary cuts on `wan_video_fal`
   (open-weights Wan family, 720p/5s verified, ~$0.10/s) or
   `pixverse_video` for stylized/social flavor (720p/5s verified).
3. **Hero shots only** — promote the surviving prompts to Kling / Veo.

Pair with the keyframe-first workflow: generate stills (FLUX) → get the
frame approved → animate via image_to_video. Scrapping a still costs cents;
scrapping a motion clip costs 10-50x more.

## Tool cheat sheet

| Tool | Endpoint family | Verified output | Niche |
|------|-----------------|-----------------|-------|
| `ltx2_video_fal` | fal-ai/ltx-2 | 1920×1080, ~6s | ultra-cheap concepting, Apache-2.0 family |
| `wan_video_fal` | fal-ai/wan/v2.2-a14b | 1280×720, ~5s | budget volume, consistent with local wan_video |
| `pixverse_video` | fal-ai/pixverse/v4.5 | 1280×720, ~5.4s | stylized / anime-flavored social clips |

All three support `text_to_video` and `image_to_video` (`image_url` accepts
data URIs). Extra endpoint fields go through `extra_params` untouched.

## Known sharp edges (verified, not folklore)

- **PixVerse v5 endpoint intermittently returns HTTP 500 at submit** (observed
  2026-07). The tool defaults to v4.5, which is stable. Retry v5 only if the
  premium look matters and the run is not time-critical.
- **fal's queue gateway does not validate payloads at submit time.** A malformed
  request is accepted (HTTP 200) and "completes" with a `detail` validation
  error in the response body — no generation happens and nothing is billed.
  `run_fal_queue_job` surfaces this as a failure; do not treat COMPLETED as
  success without checking for `detail`.
- **No native audio in this tier.** Score/dialogue must come from the audio
  pipeline (doubao_tts / piper + music tools).
- Wan and PixVerse return ~720p: plan an upscale pass (Real-ESRGAN) if the
  delivery preset is 1080p+ and the shot survives to the final cut.

## Selection notes for the scoring engine

These tools deliberately under-promise on `cinematic_quality` so the 7-axis
selector keeps routing hero shots to the premium tier. If a brief says
"draft", "iteration", "cheap", or "volume", this tier should win on
cost-efficiency without manual overrides.
