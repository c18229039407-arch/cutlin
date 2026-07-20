# Cutting Room — Declarative Timeline Panel

## What It Is
`remotion-composer/public/cutting-room.html` is a single-file, NLE-style
panel for last-mile adjustments on a finished composition. It edits the
**props declaration**, not pixels: three tracks (cuts / overlays / audio),
edge-trim with ripple so video cuts stay contiguous, an inspector for
timing, text, accent color, and `transition_in/out` (default | none), an
approximate in-browser preview, and a big tape-style timecode.

Rendering still goes through the pipeline. The panel's only outputs are a
downloaded `props-edited.json` and a copy-ready render command — the
declaration file remains the single source of truth, and nothing bypasses
the pre-compose gate or the post-render audit.

## When To Point The Human Here
- "把第三镜掐短半秒 / 字幕换两个字 / 角标晚一点出来" — parameter-level
  tweaks where a conversation round-trip feels heavier than a drag.
- Reviewing cut timing against narration by scrubbing, before deciding on
  a re-render.

Do NOT use it for: adding/removing scenes, changing scene types, caption
word-timing, or anything schema-level — those go through the normal
edit/compose stages so review gates still apply.

## How To Open
- Standalone: open the file directly in a browser. It must stay in
  `remotion-composer/public/` so relative asset paths (e.g.
  `ad-assets/*.mp4`) resolve for preview.
- Via Studio: with backlot running, `/composer/cutting-room.html`
  (linked as "✂ 剪辑室" from the library header). The mount is read-only
  GET — the Studio never writes.

## Round-Trip Flow
1. Panel: 载入 props → adjust → 导出 props JSON (`props-edited.json`).
2. Pipeline: re-render with the edited declaration, e.g.
   `npx remotion render src/index.tsx Explainer out.mp4 --props props-edited.json --codec h264`
3. Post-render audit runs as usual; log the revision in the decision log
   if this is a governed production.

## Sharp Edges (verified)
- Preview is an approximation: per-cut `<video>` elements plus CSS
  overlay stand-ins — spring physics, chart draws, and caption burns
  render only in the real pipeline output.
- Headless/CI Chromium builds often ship without H.264, so the preview
  shows placeholder tiles there; desktop Chrome/Edge/Safari play fine.
- The cuts track enforces contiguity by ripple; if a trim makes a cut
  shorter than its source clip you get a freeze-free result, but a cut
  LONGER than its source will exhaust the clip in the final render —
  check source durations before extending.
