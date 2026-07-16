# Publish Director - Storyboard Ad Pipeline

## When To Use
Final gate. Render, audit, ship — in that order, never reordered.

## Audit Checklist (all mandatory)
1. ffprobe container check: codec, resolution, duration within ±2s of plan.
2. Frame pulls at every cut boundary: no background flashes, no identity drift across chained shots.
3. Audio: loudness target for the platform, no clipping, narration placement spot-checks.
4. Overlay text legibility at target playback size; claims cross-checked against research_brief sources.
5. Write the `qa_report`; a red item blocks delivery — reshoot or reassemble, do not hand-wave.

## Output
`final_video` + `qa_report`.
