# Assembly Director - Storyboard Ad Pipeline

## When To Use
All shots accepted. You make twelve clips feel like one film. Remotion is the instrument; this skill is the score.

## Process
1. **Timeline.** Lay shots per the storyboard; honor the continuity plan (hard cuts by default — set `transition_in/out: "none"` on video cuts; dissolves only where the storyboard asked).
2. **Unify color.** One grade/LUT pass across every shot (color_grade). Cross-shot color temperature drift is the #1 tell of stitched AI footage.
3. **Audio as full-timeline tracks.** Narration segments placed at measured offsets, mixed and loudness-normalized once; music bed spans the whole piece with a single fade shape. Never score shots individually.
4. **Overlays.** All on_screen_text items ride Remotion layers: word-timed captions from narration timestamps, titles, price, CTA end card. Typography from the active playbook.

## Output
Schema-valid `edit_decisions` + `render_manifest`. Must clear the pre-compose gate (delivery promise, slideshow risk, renderer governance) before rendering.
