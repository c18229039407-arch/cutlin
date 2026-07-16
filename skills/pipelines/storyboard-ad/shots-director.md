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

## Output
`shot_library` (accepted clip + keyframe + QA verdict per shot) and a decision_log of routing choices and reserve draws.
