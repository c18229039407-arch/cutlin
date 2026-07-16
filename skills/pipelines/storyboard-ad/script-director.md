# Script Director - Storyboard Ad Pipeline

## When To Use
After the human approves a proposal. You write what is heard and list what is read — separately.

## Process
1. Write narration in segments that map **one-to-one** onto planned shot windows. Note expected seconds per line; TTS will give exact durations later.
2. Maintain a separate `on_screen_text` list (titles, captions, price, CTA, legal). These are overlay layers in assembly — never baked into generated imagery.
3. Keep claims within what research sourced. If a line needs a new claim, send back to research rather than improvising.

## Output
Schema-valid `script` with narration segments and the on_screen_text register.
