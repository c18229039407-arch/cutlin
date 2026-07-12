<p align="center">
  <img src="assets/logo.png" alt="Cutlin" width="200">
</p>

<h1 align="center">Cutlin</h1>

<p align="center"><a href="README.md">简体中文</a> · English</p>

---

Cutlin upgrades the AI coding assistant you already use into a full video production crew. You describe what you want; the agent takes it from there — topic research, scriptwriting and voiceover, asset creation, editing, and the final render.

**One distinction worth stating up front:** a lot of "AI video" boils down to slapping a zoom on a few still images. Cutlin can animate stills too, but it also supports a **real-footage route**: the agent pulls genuinely filmed motion clips from royalty-free libraries and open archives, ranks them semantically, cuts them with intent, and renders a proper timeline. That's editing, not sleight of hand.

## Technical Showcase

Cutlin isn't a thin wrapper over somebody's video API — it's a production system with mandatory quality checks wired into every stage.

**Pipeline architecture.** Every production moves through a staged pipeline with checkpoints and approval gates:

```
 idea ──▶ research ──▶ script ──▶ scene plan ──▶ assets ──▶ compose ──▶ QA ──▶ render
   │          │           │            │            │           │        │
   └──────────┴───────────┴────────────┴────────────┴───────────┴────────┘
              checkpoints · decision logs · cost snapshots · approval gates
```

**Multi-provider orchestration.** Image, video, voice, and music providers are each scored on 7 dimensions (quality, cost, latency, style fit, availability, license, consistency), and the scoring lands in an auditable decision log. Selection happens per shot — not one vendor bolted onto the whole project.

**Three composition engine paths, chosen per production:**

| Engine | Best for | Cost profile |
|---|---|---|
| Remotion composition | data-driven scenes, captions, motion graphics | free (local render) |
| Still-image animation (Ken Burns / parallax / particles) | stills-to-motion, anime & editorial styles | ~$0.02–$0.15 per video |
| Generated motion clips (Veo / Kling / MiniMax / local Wan) | true motion, cinematic shots | ~$0.70–$3 per video |

**Pre-delivery self-review.** ffprobe validation, frame sampling, audio-level analysis, delivery-promise verification, and subtitle checks run automatically on every render — a failing cut never reaches you.

**Zero-key baseline.** With no API keys configured at all, the free path still works: footage-corpus retrieval, timeline editing, local Remotion rendering.

---

## Start From A Video You Already Love

Instead of agonizing over a blank prompt, hand it a video you admire.

Cutlin accepts a **YouTube video, Short, Reel, TikTok, or local file** as a reference and breaks it down into an actionable production plan:

1. **Paste the reference**
2. **The agent dissects its copy structure, pacing, scene cuts, key frames, and visual style**
3. **Before real work begins you get 2–3 distinct concepts, honest tool paths, cost estimates, and samples**

```text
"I'm sending you a Short that really lands for me. Match its feel, but make the topic quantum computing."
```

What you get back is not a guessed-at prompt stew — it's a plan that explains itself:

- What was **kept** from the reference: pacing skeleton, hook style, narrative structure, tone
- What was **swapped**: subject, visual treatment, angle, narration approach
- What it will **roughly cost** at your target length, before asset generation starts
- What the render will **actually look like** with the tools you currently have

Any coding agent that can read files and execute code will do the driving — **Claude Code, Cursor, Copilot, Windsurf, and Codex** all work out of the box.

---

## Watch It Happen — Cutlin Studio

Chat tells you what the agent *said*. **Cutlin Studio shows you what the production is actually doing**: a local board that fills itself in as the pipeline runs — stages light up, the script lands on the page, asset cards shimmer while generating, and every decision and dollar is on the wall.

The agent opens it for you automatically when a production starts. To open it manually:

```bash
python -m backlot open                  # the library — every project on disk
python -m backlot open <project-id>     # one production's live board
python scripts/backlot_simulate_run.py  # no production yet? watch a simulated one
```

> **Prefer double-click?** The repo root ships launchers: `打开观测端.bat` (Windows) and `打开观测端.command` (macOS; right-click → Open on first run if Gatekeeper blocks it).

The board is read-only: it watches `projects/` and pushes updates over SSE without touching the production. Approvals happen back in your AI assistant's chat. After a run finishes, hit **▶ Replay Run** to scrub the whole production by its timestamps. See [`backlot/README.md`](backlot/README.md).

---

## Quick Start

### Prerequisites

- **Python, version 3.10 at minimum** — download at [python.org](https://www.python.org/downloads/)
- **FFmpeg** — `brew install ffmpeg` on macOS, `sudo apt install ffmpeg` on Ubuntu, otherwise [ffmpeg.org](https://ffmpeg.org/download.html)
- **Node.js 18 or newer** — [nodejs.org](https://nodejs.org/)
- **An AI coding assistant** — Claude Code, Cursor, Copilot, Windsurf, or Codex

### Install & Run

```bash
git clone https://github.com/c18229039407-arch/cutlin.git
cd cutlin
make setup
```

Open the directory in your AI coding assistant and just ask:

```
"I need one minute of animation that teaches how neural networks learn"
```

Or, for the real-footage route:

```text
"Cut a 75-second documentary montage: the city on a rainy night. Real footage only, skip the narration, keep the mood elegiac and score it to match."
```

From there it's out of your hands in the best way: the agent researches the topic with live web search, generates visuals, writes and voices the script with voice direction, auto-sources royalty-free music, burns word-level subtitles, and renders the cut. Before anything reaches your eyes, the system runs a multi-point self-check — ffprobe validation, frame sampling, audio-level analysis, delivery-promise verification, subtitle checks. Every provider pick is scored on 7 dimensions and archived. Every creative fork waits for your sign-off.

> **`make` missing on your system?** Run the equivalent by hand — macOS/Linux: `python3 -m venv .venv && source .venv/bin/activate && python -m pip install -r requirements.txt && cd remotion-composer && npm install && cd .. && python -m pip install piper-tts && cp .env.example .env`
>
> Windows PowerShell: `py -3 -m venv .venv; .\.venv\Scripts\Activate.ps1; python -m pip install -r requirements.txt; cd remotion-composer; npm install; cd ..; python -m pip install piper-tts; Copy-Item .env.example .env`
>
> **Windows:** if `npm install` fails with `ERR_INVALID_ARG_TYPE`, use `npx --yes npm install` instead.

### If You're An Agent Reading This: Welcome Aboard

This repository was built to be operated by agents. Fastest way to get productive, in order:

1. **Rules before work**
   Read [`AGENT_GUIDE.md`](AGENT_GUIDE.md) end to end, then build your mental map from [`PROJECT_CONTEXT.md`](PROJECT_CONTEXT.md).
2. **Don't invent your own workflow**
   Cutlin is pipeline-driven: orchestration lives in `pipeline_defs/`, stage director skills in `skills/pipelines/`, and tools are discovered via the registry.
3. **Check what cards you're holding**
   Run:
   ```bash
   python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.support_envelope(), indent=2))"
   python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.provider_menu(), indent=2))"
   ```
4. **Treat every video request as a pipeline-selection problem**
   Pick the right pipeline, read the manifest, read the stage skill — only then touch tools.

### Add API Keys (optional — more keys = more tools)

```bash
# .env — every key is optional; add the ones you have

# Image + video gateway:
FAL_KEY=your-key               # FLUX images + Google Veo, Kling, MiniMax video + Recraft images

# Free stock media:
PEXELS_API_KEY=your-key        # free stock footage and images
PIXABAY_API_KEY=your-key       # free stock footage and images
UNSPLASH_ACCESS_KEY=your-key   # free stock images

# Music:
SUNO_API_KEY=your-key          # full songs and instrumentals, any genre

# Voice & images:
ELEVENLABS_API_KEY=your-key    # top-tier TTS, AI music, sound effects
OPENAI_API_KEY=your-key        # OpenAI TTS, GPT Image 2
XAI_API_KEY=your-key           # xAI Grok image edit/generation + Grok video
GOOGLE_API_KEY=your-key        # Google Imagen images, Google TTS (700+ voices)

# More video providers:
HEYGEN_API_KEY=your-key        # HeyGen — unified gateway to VEO, Sora, Runway, Kling
RUNWAY_API_KEY=your-key        # Runway Gen-4 direct
```

<details>
<summary><strong>Have a GPU? Unlock free local video generation</strong></summary>

```bash
make install-gpu

# Then add to .env:
VIDEO_GEN_LOCAL_ENABLED=true
VIDEO_GEN_LOCAL_MODEL=wan2.1-1.3b  # or wan2.1-14b, hunyuan-1.5, ltx2-local, cogvideo-5b
```

</details>

---

## What You Get With Zero API Keys

No spend, no keys — still real videos. Right after `make setup` you have:

| Capability | Free tool | What it does |
|-----------|-----------|-------------|
| **Narration** | Piper TTS | local, offline speech synthesis with near-human narration |
| **Open footage** | Archive.org + NASA + Wikimedia Commons | public-domain archival footage, educational media, documentary material |
| **Extra stock** | Pexels + Unsplash + Pixabay | free stock video and images (developer keys are free to obtain) |
| **Composition (React)** | Remotion | React rendering: spring-animated image scenes, text cards, data cards, charts, TikTok-style word captions, TalkingHead avatars |
| **Composition (HTML/GSAP)** | HyperFrames | HTML/CSS/GSAP rendering: kinetic typography, product spots, launch teasers, website-to-video, rigged SVG character animation |
| **Post-production** | FFmpeg | encoding, subtitle burn-in, audio mixing, color grading |
| **Captions** | built-in | auto-generated subtitles with word-level timing |

Remotion vs. HyperFrames is decided at the proposal stage and locked into `render_runtime`: data-driven explainers and anything reusing the existing React scene stack default to Remotion; heavy motion-graphics work that's more natural in HTML + GSAP (including the `character-animation` pipeline's rigged SVG output) defaults to HyperFrames. Full decision matrix in `skills/core/hyperframes.md`.

**A few nearly-free paths:**

- **Image-based video:** Piper reads the script, images supply the visuals, Remotion choreographs them into a polished cut.
- **Local character animation:** SVG rigs + pose libraries + GSAP timelines; HyperFrames renders the cartoon performance to `projects/<project-name>/renders/final.mp4`.
- **Real-footage video:** the documentary-montage pipeline builds a CLIP-searchable corpus from Archive.org, NASA, Wikimedia Commons (optionally Pexels and Unsplash) and cuts genuine motion footage into a complete film.

To lock in that third route, name the format explicitly — **documentary montage**, **tone poem**, or **stock-footage collage** — and add the phrase **use real footage only**; the pipeline will commit to the retrieve-and-edit path.

---

## Try These Prompts

Once set up, drop any of these into your AI coding assistant — each one triggers a full pipeline run.

### Start from a reference video

> "This short nails the vibe I want. Recreate that feel, but teach high-schoolers how mRNA vaccines work."

> "Break down what makes this Reel work, then pitch me three fresh takes I could shoot for my app launch."

> "Steal the rhythm and the cold-open from this clip, and rebuild it as a 40-second piece on how GPS satellites keep time."

### Zero keys needed

> "Give me a 45-second animated piece on why cats always land on their feet"

> "A 60-second narrated video with captions: how container shipping changed the world"

> "Build a chart-heavy explainer on global renewable energy adoption"

### Free real-footage documentary path

> "A 90-second real-footage montage: the last hour before a harbor wakes up. No voiceover, quiet and wistful."

> "One minute of archival collage on the Space Race's public euphoria, essay-film flavor, sourced from open archives."

> "Real stock footage only: a drifting montage about night trains and the people asleep on them. Score it, skip the narration."

### With an image/video provider configured (~$0.15–$1.50)

> "30 seconds of Ghibli-flavored animation: a lighthouse keeper who tends a garden of glowing jellyfish at dusk"

> "An anime-style half-minute: an abandoned observatory on a snowfield, aurora overhead, one warm window lit"

> "Use AI-generated visuals to explain how neural networks learn, aimed at total beginners"

> "Cut a launch teaser for Lumo, a made-up desk lamp that reads your focus and shifts its light"

### Full setup (~$1–$3)

> "A cinematic 30-second teaser: the day every mirror on Earth started showing a five-second delay"

> "90 animated seconds on how the immune system fights a virus, for middle schoolers — playful narrator, original score"

Hunting for more ideas? The **[Prompt Gallery](PROMPT_GALLERY.md)** collects field-tested prompts with expected costs and sample outputs — or run `make demo` to render a zero-key demo right now.

---

## Pipelines

A pipeline is the full journey a production takes — from the first idea to the rendered file.

| Pipeline | What it produces | Best for |
|----------|-----------------|----------|
| **Animated Explainer** | AI-generated explainer with research, narration, visuals, music | education, tutorials, topic breakdowns |
| **Animation** | motion graphics, kinetic typography, animated sequences | social media, product demos, abstract concepts |
| **Avatar Spokesperson** | digital-human presenter videos | corporate comms, training, announcements |
| **Cinematic** | trailers, teasers, mood-driven cuts | brand films, teasers, promos |
| **Clip Factory** | ranked short clips mass-produced from one long source | repurposing long content into social shorts |
| **Documentary Montage** | thematic montages cut from CLIP-indexed free libraries and open archives (Pexels, Archive.org, NASA, Wikimedia, Unsplash) | video essays, mood pieces, retrieval-first B-roll cuts, real-footage video without paid video APIs |
| **Hybrid** | user footage + AI-generated supporting visuals | reinforcing existing footage with graphics |
| **Localization & Dub** | subtitles, translation, and dubbing for existing video | multilingual distribution |
| **Podcast Repurpose** | podcast highlights turned into video | podcast marketing, audiograms |
| **Screen Demo** | polished software screen recordings and walkthroughs | product demos, tutorials, docs |
| **Talking Head** | presenter-led videos built around real people on camera | presentations, vlogs, interviews |

Every pipeline shares one skeleton:

```
research → proposal → script → scene plan → assets → edit → compose
```

Each stage carries a **director skill** — a Markdown instruction file that tells the agent exactly how to run that step. The agent reads the skill, uses the tools, reviews its own work, checkpoints state, and stops for your approval at creative decision points.

> **Web research is a formal stage, not garnish.** Before a single line of script gets written, the agent searches YouTube, Reddit, Hacker News, news outlets, and academic sources — collecting data points, audience questions, trending angles, and visual references into a structured research brief. Your video stands on real, current information, not hallucinated "facts."

---

## Why Cutlin?

The typical AI video product is a vending machine: one prompt in, one clip out. Cutlin gives you an **end-to-end production pipeline** — the same structured process a real production team follows, executed by your AI agent.

Most "free AI video" stacks quietly mean "animate some stills." Cutlin can do that trick too, but it can also finish films from **real footage** sourced through free and open channels: semantically ranked, deliberately cut, rendered as a proper timeline.

Edit your own on-camera footage. Generate a fully animated explainer from nothing. Split a two-hour podcast into a dozen social clips. Translate and dub your content into ten languages. Assemble a cinematic brand trailer from stock and AI scenes. **If a production team can make it, Cutlin can orchestrate it.**

- **12 production pipelines** — explainers, talking head, screen demos, cinematic trailers, animation, podcasts, localization, documentary montage
- **52 production tools** — video generation, image creation, TTS, music, mixing, subtitles, enhancement, analysis
- **400+ agent skills** — production skills, pipeline directors, creative methods, QA checklists, and deep technical knowledge packs that teach the agent to use every tool like a professional
- **Reference-driven creation** — paste a video you like; the agent translates it into a grounded, differentiated production plan so you never have to craft the perfect prompt
- **Real documentaries without paid video models** — properly cut films from free/open motion footage and archives, not zooms on still images
- **Built-in live web research** — 15–25 searches across YouTube, Reddit, news, and academic sites before scripting, so content stands on fresh, real data
- **Free/local and cloud providers, side by side** — every capability has an open-source local option or a premium API; use whichever you have
- **No vendor lock-in** — swap providers freely; the system scores them on 7 dimensions (task fit, output quality, control, reliability, cost efficiency, latency, continuity) and auto-picks the best match
- **Production-grade quality gates** — delivery-promise enforcement blocks slideshow-grade renders; pre-compose validation stops broken plans before they burn GPU; mandatory post-render self-review (ffprobe + frame sampling + audio analysis) means junk never ships. Every provider pick, style call, and fallback lands in an auditable decision log
- **Built-in budget controls** — pre-run estimates, spend caps, per-action approval thresholds. No billing surprises

---

## How It Works

Cutlin is built **agent-first**: there is no hidden code orchestrator hiding backstage — your AI coding assistant is the orchestrator.

```
You: "Make me an explainer on how black holes form"
 │
 ▼
Read the pipeline manifest (YAML): stages, tooling, review bars, success gates
 │
 ▼
Read the stage director skills (Markdown): the HOW for each step
 │
 ▼
Call Python tools: a scoring selector ranks every candidate across 7 axes
 │
 ▼
Self-review against reviewer skills: schema checks, script fidelity, quality bars
 │
 ▼
Persist a checkpoint (JSON): resumable, with decision log and cost snapshot
 │
 ▼
Pause for your sign-off: every creative fork waits for a human yes
 │
 ▼
Pre-compose gate: delivery promise, slideshow-risk scan, renderer governance
 │
 ▼
Render (Remotion or FFmpeg): the engine that fits the visual grammar
 │
 ▼
Post-render audit: ffprobe, frame pulls, audio analysis, promise verification
 │
 ▼
The video ships — only after every check above clears
```

**Python supplies tools and persistence — not judgment.** All creative decisions, orchestration logic, review criteria, and quality bars live in human-readable instruction files (YAML manifests + Markdown skills) you can inspect and rewrite. Every decision is archived with its alternatives, confidence scores, and reasoning.

---

## Architecture

```
Cutlin/
├── tools/              # 48 Python tools — the hands the agent works with
│   ├── video/          # 13 video generation tools + compose, stitch, trim
│   ├── audio/          # 4 TTS providers + Suno/ElevenLabs music, mixing, enhancement
│   ├── graphics/       # 9 image/graphics tools + charts, code snippets, math animation
│   ├── enhancement/    # upscaling, background removal, face enhancement, color grading
│   ├── analysis/       # transcription, scene detection, frame sampling
│   ├── avatar/         # digital humans, lip sync
│   └── subtitle/       # SRT/VTT generation
│
├── pipeline_defs/      # YAML pipeline manifests (the agent's "scripts")
├── skills/             # Markdown skill files (the agent's "knowledge")
│   ├── pipelines/      # per-pipeline stage director skills
│   ├── creative/       # creative technique skills
│   ├── core/           # core tool skills
│   └── meta/           # reviewers, checkpoint protocol
│
├── schemas/            # 15 JSON Schemas (contract validation)
├── styles/             # visual style guidance (YAML)
├── remotion-composer/  # React/Remotion composition engine
├── lib/                # core infrastructure (config, checkpoints, pipeline loader)
└── tests/              # contract tests, QA integration tests, eval toolkit
```

### Three-tier knowledge architecture

```
Tier 1  tools/ + pipeline_defs/    the inventory: what capabilities exist and how they chain
Tier 2  skills/                    the house rules: Cutlin's conventions and quality bars
Tier 3  .agents/skills/            the deep cuts: external technical know-how, on demand
```

Tools declare which Tier-3 skills they depend on. The agent reads Tier 1 to inventory its tools, Tier 2 to learn the house rules, and reaches for Tier 3 when it needs to go deep.

---

## Supported Providers

> **Full setup guide with pricing and free tiers:** [`docs/PROVIDERS.md`](docs/PROVIDERS.md)

<details>
<summary><strong>Video generation — 14 providers</strong></summary>

| Provider | Type | Notes |
|----------|------|-------|
| **Kling** | cloud API | quality and speed in one |
| **Runway Gen-4** | cloud API | cinematic; Gen-3 Alpha Turbo / Gen-4 Turbo / Gen-4 Aleph |
| **Google Veo 3** | cloud API | long-form, cinematic; via fal.ai or HeyGen |
| **Grok Imagine Video** | cloud API | strong reference-driven video and native xAI short-form generation |
| **Higgsfield** | cloud API | multi-model orchestrator with Soul ID character consistency |
| **MiniMax** | cloud API | standout cost efficiency |
| **HeyGen** | cloud API | unified multi-model gateway |
| **WAN 2.1** | local GPU | free; 1.3B and 14B variants |
| **Hunyuan** | local GPU | free, excellent quality |
| **CogVideo** | local GPU | free; 2B and 5B variants |
| **LTX-Video** | local GPU / Modal | free locally, or self-hosted in the cloud |
| **Pexels** | stock | free stock footage |
| **Pixabay** | stock | free stock footage |
| **Wikimedia Commons** | stock | free/open footage and archival material |

</details>

<details>
<summary><strong>Image generation — 10 tools/providers</strong></summary>

| Provider | Type | Notes |
|----------|------|-------|
| **FLUX** | cloud API | image quality at the front of the pack |
| **Google Imagen** | cloud API | Imagen 4: crisp output, generous aspect-ratio menu |
| **Grok Imagine Image** | cloud API | shines at edits, restyling, and blending several inputs |
| **GPT Image 2** | cloud API | OpenAI's image model |
| **Recraft** | cloud API | leans toward design-grade output |
| **Local Diffusion** | local GPU | Stable Diffusion on your own card, no bill |
| **Pexels** | stock | free stock images |
| **Pixabay** | stock | free stock images |
| **Unsplash** | stock | free stock images |
| **ManimCE** | local | purpose-built for math and science animation |

</details>

<details>
<summary><strong>Text-to-speech — 4 providers</strong></summary>

| Provider | Type | Notes |
|----------|------|-------|
| **ElevenLabs** | cloud API | the voice-quality ceiling |
| **Google TTS** | cloud API | 700+ voices, 50+ languages — best for localization |
| **OpenAI TTS** | cloud API | fast and inexpensive |
| **Piper** | local | completely free, works offline |

</details>

<details>
<summary><strong>Music, SFX & post-production</strong></summary>

**Music & sound effects:**

| Provider | Type | Notes |
|----------|------|-------|
| **Suno AI** | cloud API | full songs with vocals and lyrics, any genre, up to 8 minutes |
| **ElevenLabs Music** | cloud API | AI music generation |
| **ElevenLabs SFX** | cloud API | sound-effect generation |

**Post-production (always on, always free):**

| Tool | What it does |
|------|-------------|
| **FFmpeg** | video assembly, encoding, subtitle burn-in, audio mixing |
| **Video Stitch** | multi-clip assembly, crossfades, picture-in-picture, spatial layouts |
| **Video Trimmer** | precise cuts and extraction |
| **Audio Mixer** | multi-track mixing, ducking, fades |
| **Audio Enhance** | noise reduction, loudness normalization |
| **Color Grade** | LUT-based color grading |
| **Subtitle Gen** | SRT/VTT from timestamps |

**Enhancement:**

| Tool | What it does |
|------|-------------|
| **Upscale** | Real-ESRGAN super-resolution for both stills and footage |
| **Background Remove** | rembg / U2Net background removal |
| **Face Enhance** | facial quality enhancement |
| **Face Restore** | CodeFormer / GFPGAN face restoration |

**Analysis:**

| Tool | What it does |
|------|-------------|
| **Transcriber** | WhisperX transcription, timestamped to the individual word |
| **Scene Detect** | spots the cut points without help |
| **Frame Sampler** | pulls representative frames, not random ones |
| **Video Understand** | reads what is on screen via CLIP/BLIP-2 |

**Avatar & lip sync:**

| Tool | What it does |
|------|-------------|
| **Talking Head** | animates a still portrait into a speaking presenter (SadTalker / MuseTalk) |
| **Lip Sync** | matches mouth movement to any audio track (Wav2Lip) |

**Composition & rendering:**

| Engine | Type | What it does |
|--------|------|-------------|
| **Remotion** | local (Node.js) | programmatic React video: spring-animated image scenes, data reveals, chapter titles, showcase cards, TikTok-style word captions, scene transitions (fade/slide/wipe/flip), Google Fonts, audio with fade curves, TalkingHead compositing. **With no video-gen provider configured, the agent generates stills and Remotion turns them into fully animated video.** |
| **HyperFrames** | local (Node.js ≥ 22) | programmatic HTML/CSS/GSAP video: kinetic typography, product spots, launch teasers, custom motion graphics, registered blocks (data charts, noise overlays, shader transitions), website-to-video workflows, rigged SVG character animation. Invoked via `npx hyperframes`; no monorepo checkout required. |
| **FFmpeg** | local | core assembly, encoding, subtitle burn-in, mixing, grading |

Which render runtime gets used is settled once, at the proposal stage (`render_runtime`), and then locked via `edit_decisions`. Silently switching runtimes mid-run is a governance violation — see `skills/core/hyperframes.md`.

</details>

---

## Style System

Style playbooks are the visual constitution of a production:

| Playbook | Best for |
|----------|----------|
| **Clean Professional** | corporate, education, SaaS |
| **Flat Motion Graphics** | social media, TikTok, startups |
| **Minimalist Diagram** | technical deep dives, architecture |

A playbook pins down typography, palette, motion language, audio profile, and quality rules; the agent reads it once and applies it to every generated asset.

---

## Platform Output Presets

Render presets for the major platforms, ready out of the box:

| Preset | Resolution | Aspect ratio |
|---------|-----------|--------------|
| YouTube Landscape | 1920x1080 | 16:9 |
| YouTube 4K | 3840x2160 | 16:9 |
| YouTube Shorts | 1080x1920 | 9:16 |
| Instagram Reels | 1080x1920 | 9:16 |
| Instagram Feed | 1080x1080 | 1:1 |
| TikTok | 1080x1920 | 9:16 |
| LinkedIn | 1920x1080 | 16:9 |
| Cinematic | 2560x1080 | 21:9 |

---

## Production Governance

Cutlin treats video production with the rigor of software engineering: quality gates at every stage, an audit trail behind every decision, a leash on every dollar.

### Quality gates

- **Pre-compose validation** — a broken delivery promise (say, a "motion-forward" video that's 80% stills), a critical slideshow-risk score, or a missing renderer family each blocks the render. Bad plans get stopped before they burn GPU time.
- **Post-render self-review** — after every render the runtime runs ffprobe validation, samples frames at 4 positions to catch black screens and broken overlays, analyzes audio for silence or clipping, verifies the delivery promise, and checks subtitles. Fail the review, and the video is never shown.
- **Slideshow-risk scoring** — a 6-dimension analysis (repetitiveness, decorative visuals, weak motion, shot intent, typography over-reliance, unsupported cinematic claims) blocks "animated PowerPoint" output.
- **Source-file inspection** — when users supply their own footage, the system probes every file (resolution, codec, audio channels, duration) and builds a planning baseline before any creative decision. No more inventing content from filenames.

### Score-based provider selection

Every tool pick (video gen, image gen, TTS, music) goes through a 7-dimension scoring engine: task fit (30%), output quality (20%), control features (15%), reliability (15%), cost efficiency (10%), latency (5%), continuity (5%). The winner — and every alternative's score — lands in the decision record.

The selector normalizes loose brief context before scoring: even if all the agent has is "Pixar-style short with consistent characters," it expands that into scoreable intent and style signals without demanding a perfectly pre-shaped `task_context`.

Selector output also surfaces the winning provider's `agent_skills`, so the agent can jump straight to the relevant Tier-3 skill before writing a single prompt.

### Decision audit trail

Every significant creative and technical choice — provider, style playbook, music track, voice, renderer family, plus any fallback or downgrade — is recorded with its alternatives, confidence scores, and reasoning. The accumulated decision log persists across all stages, so you can trace exactly why the output looks the way it does.

### Budget controls

- **Estimate** before running — see the projected cost
- **Lock** the budget — reserve funds before the call
- **Settle** afterward — record actual spend
- **Configurable modes** — `observe` (track only), `warn` (overspend alerts), `cap` (hard ceiling)
- **Per-action approval** — spends above a threshold (default: $0.50) pause for confirmation
- **Total budget cap** — $10 by default, fully configurable

No billing surprises. The agent shows you the number before it spends it.

---

## Agent Compatibility

Any AI coding assistant that reads files and executes Python can drive Cutlin. Platform-specific instruction files are already in place:

| Platform | Config file |
|----------|------------|
| **Claude Code** | `CLAUDE.md` |
| **Cursor** | `CURSOR.md` + `.cursor/rules/` |
| **GitHub Copilot** | `COPILOT.md` + `.github/copilot-instructions.md` |
| **Codex** | `CODEX.md` |
| **Windsurf** | `.windsurfrules` |

All the per-platform entry files converge on the same two source documents: `AGENT_GUIDE.md` (operating manual and agent contract) and `PROJECT_CONTEXT.md` (architecture reference).

> **Planned:** local LLM support via **Ollama** and **LM Studio** — running the entire production pipeline without any cloud model.

---

## Contributing

Extension points are baked into the architecture. The two most common contributions:

### Adding a new tool

1. Create a Python file in the matching `tools/` subdirectory
2. Inherit from `BaseTool` and implement the tool contract
3. The registry discovers it automatically — no manual registration
4. If the tool needs usage guidance, add a matching skill file

### Adding a new pipeline

1. Sketch the whole pipeline as a YAML manifest inside `pipeline_defs/`
2. Give each stage a director skills in `skills/pipelines/<your-pipeline>/`
3. Reuse existing tools — add new ones only when needed

Full technical reference in `docs/ARCHITECTURE.md`, provider guide (setup, pricing, free tiers) in `docs/PROVIDERS.md`, agent contract in `AGENT_GUIDE.md`.

---

## Contact

For bugs, feature requests, and workflow discussions, use [GitHub Issues](https://github.com/c18229039407-arch/cutlin/issues) so everything stays trackable.

---

## Testing

```bash
# Run contract tests (no API keys needed)
make test-contracts

# Run all tests
make test
```

---

## License

[GNU AGPLv3](LICENSE)

## Acknowledgements

Cutlin is a modified fork of [OpenMontage](https://github.com/calesthio/OpenMontage) by calesthio. Thanks to the original authors for their excellent work.

---

**Cutlin** — video production with software-grade rigor: real quality gates, directed by your AI assistant.
