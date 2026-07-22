# Shots Director - Storyboard Ad Pipeline

## When To Use
The spend stage. You turn the storyboard into an accepted clip per shot, one shot at a time, gate by gate.

## Per-Shot Loop (strict order)
1. **Keyframe.** Generate the still first (flux_image or selected image tool), splicing the character card + shot content_brief + scene light recipe into the prompt. Get it accepted (human or auto per checkpoint policy).
2. **Chain check.** If `continuity: chain_from`, pull the upstream shot's tail frame and pass it as the reference/first-frame input.
3. **Animate.** Route through the scoring engine: premium tier (kling/veo) for hero shots, budget tier (wan_video_fal / ltx2_video_fal / pixverse_video — see core/budget-video-providers) for volume shots. Pass the keyframe via image_to_video.
4. **Per-shot QA before the next shot starts:**
   - identity: sample 3 frames, compare against character_kit anchors (wardrobe color, marks, light direction);
   - motion: frame-difference check to catch static "boiled stills";
   - text: confirm NO legible model-generated text drifted into frame.
5. **Reshoot or accept.** Failures draw from the reserve with a logged reason. Two identity failures on one shot escalate to the EP.

## QA metric design — two traps verified on a real run

**Do not use first-vs-last frame difference as a degradation signal.** A shot
with an intentional push-in or orbit legitimately ends up looking very
different from where it started. On a real 5-clip run this metric flagged 4
of 5 clips as "drifting" when inspection showed all five intact — acting on
it would have burned the reshoot reserve on healthy footage.

Use instead:
- **Motion steadiness**: coefficient of variation of frame-to-frame diffs
  across the whole clip. Intentional camera movement is steady (CV well under
  0.6); degradation is erratic. Measured 0.13-0.40 on accepted clips.
- **Edge-density ratio**: mean gradient magnitude of the last frame over the
  first. Structure that melts loses edges. Accept roughly 0.6-1.7x; measured
  0.77-1.35x on accepted clips.

**Validate source_in_seconds against the clip's real duration before
rendering.** When one source clip is cut into several shots it is easy to
write an in-point that runs past the end — the render then freezes or goes
black at that cut instead of failing loudly. Probe each clip with ffprobe and
assert `source_in + shot_length <= duration`. On a real run this caught a
shot reaching 5.20s into a 5.04s clip.

## Output
`shot_library` (accepted clip + keyframe + QA verdict per shot) and a decision_log of routing choices and reserve draws.
