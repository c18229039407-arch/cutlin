# Storyboard Director - Storyboard Ad Pipeline

## When To Use
The heart of this pipeline. You translate the script into a shot table that generation and assembly can execute mechanically.

## Shot Table Fields (every shot)
| Field | Meaning |
|-------|---------|
| id | s01, s02... |
| duration | seconds; must respect the 5-15s single-generation ceiling |
| framing | wide / medium / close / macro |
| camera | push / orbit / static / handheld drift... one move per shot |
| content_brief | what is in frame, written for an image model |
| continuity | `hard_cut` or `chain_from:<shot_id>` (consume that shot's tail frame as the next keyframe reference) |
| light | time-of-day + key direction, kept consistent within a scene block |
| overlay | which on_screen_text items ride on this shot |

## Rules
1. Durations sum to the approved runtime.
2. Every chained pair names the carried frame explicitly. First/last-frame chaining is the cheapest continuity tool available — design for it rather than hoping the model stays consistent.
3. Data, charts, prices, captions are overlay work: mark them, do not brief them into the model.
4. Keep one lighting recipe per scene block; a light jump reads as a location jump.

## Output
`storyboard` artifact + decision_log. Human approval is mandatory — this is the cheapest moment to change the film.
