# Character Director - Storyboard Ad Pipeline

## When To Use
Conditional stage: runs when the storyboard declares recurring characters or hero products. Skip for pure scenery/montage pieces.

## Process
1. **Card first.** For each recurring entity write a card: appearance, wardrobe, materials, distinguishing marks, forbidden variations. JSON-structured so shot prompts can splice it verbatim.
2. **Multi-view sheet.** Generate front / side / three-quarter views minimum (six views for hero characters) with **one lighting setup and a neutral background**. The sheet exists to feed reference-image inputs (Kling multi-reference, Veo reference-to-video, Higgsfield Soul ID) — variety in pose, not in identity.
3. **Freeze before spend.** The human approves the sheets before any image-to-video generation. Changing a character after shots exist means reshooting every shot they appear in.

## QA Anchors
Record wardrobe colors and light direction into the card — the shots stage checks generated clips against these anchors, frame-sampled, before accepting a shot.

## Output
`character_kit`: cards + approved reference sheets + continuity anchors.
