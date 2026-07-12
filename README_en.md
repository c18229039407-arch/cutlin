<p align="center">
  <img src="assets/logo.png" alt="Cutlin" width="200">
</p>

<h1 align="center">Cutlin</h1>

<p align="center"><a href="README.md">简体中文</a> · English</p>

---

Cutlin turns the coding agent you already use into an on-call video production crew. Describe the film you want in one sentence; the agent handles everything downstream — research, planning, scripting, voiceover, visuals, editing, rendering — and comes back to you at every decision that matters.

One thing worth saying up front: a large share of "AI video" is a camera move layered over still images. Cutlin can do that trick, but its more interesting mode is the **real-footage route** — retrieving genuinely filmed motion from open archives and royalty-free libraries, ranking it semantically, and cutting it into a timeline with intent. What comes out is an edit, not an animated slideshow.

---

## Up and running in three minutes

Four prerequisites: **Python 3.10+** ([python.org](https://www.python.org/downloads/)), **FFmpeg** (`brew install ffmpeg` on macOS, `sudo apt install ffmpeg` on Ubuntu), **Node.js 18+** ([nodejs.org](https://nodejs.org/)), and any **AI coding assistant** — Claude Code, Cursor, Copilot, Windsurf, or Codex.

```bash
# grab the source, step inside, install everything in one go
git clone https://github.com/c18229039407-arch/cutlin.git
cd cutlin
make setup   # = Python deps + Remotion + piper-tts + a fresh .env
```

> **No `make` on this machine?** Do what it would have done, step by step (macOS/Linux):
> ```bash
> python3 -m venv .venv && source .venv/bin/activate   # create + enter the venv
> python -m pip install -r requirements.txt            # Python deps
> ( cd remotion-composer && npm install )              # render-engine deps
> python -m pip install piper-tts                      # free local TTS
> cp .env.example .env                                 # key template
> ```
> On Windows PowerShell: `py -3 -m venv .venv; .\.venv\Scripts\Activate.ps1; python -m pip install -r requirements.txt; cd remotion-composer; npm install; cd ..; python -m pip install piper-tts; Copy-Item .env.example .env`. If `npm install` throws `ERR_INVALID_ARG_TYPE`, retry with `npx --yes npm install`.

Open the folder with your coding assistant and brief it like a producer:

```
"I need one minute of animation that teaches how neural networks learn"
```

From there the agent researches the topic live on the web, produces the visuals, writes and voices the script to spec, finds royalty-free music, burns word-timed captions, and renders. Before anything reaches you it passes a machine audit — ffprobe checks, frame pulls, audio-level analysis, delivery-promise verification. Too impatient to configure anything? `make demo` renders a zero-key sample immediately.

---

## One production, on the record

Not marketing copy — an actual zero-key run performed by this repo's maintainer, at zero cost:

- **The brief**: a 60-second animated explainer, "How neural networks learn," narrated in Chinese
- **Voice**: piper local TTS, synthesized in 7 segments and aligned to a measured timeline
- **Visuals**: 7 Remotion motion-graphics scenes — title card, weights callout, prediction-vs-truth comparison, a loss-descent line chart (the centerpiece), an iteration progress bar, results KPIs, closing card
- **Music**: an ambient pad synthesized locally with ffmpeg, normalized to −16 LUFS, mixed under at 0.13
- **QA caught a genuine bug**: post-render frame sampling revealed an empty line chart (a data field didn't match the component contract); after the fix, pixel-level checks confirmed the curve — exactly the failure mode the self-review stage exists for
- **Bill**: $0.00; final file 1080p / 30fps / 61 seconds

---

## The production board: Cutlin Studio

The chat window tells you what the agent *said*; **Studio shows you what the production is actually doing**. It is a local web board where stages light up, script pages land, asset cards pulse while generating, and every decision and dollar goes up on the wall. The agent opens it for you when a run starts; manual routes:

```bash
python -m backlot open                  # library view: every project found on disk
python -m backlot open <project-id>     # zoom into one production's live board
python scripts/backlot_simulate_run.py  # no runs yet? watch a simulated production
```

> **Prefer double-click?** The repo root ships launchers: `打开观测端.bat` (Windows) and `打开观测端.command` (macOS; right-click → Open on first run if Gatekeeper blocks it).

The board is read-only: it watches `projects/` and streams over SSE, never steering the run. Approvals happen back in your assistant's chat. Finished runs replay end-to-end from their timestamps via **▶ 回放运行 (Replay Run)**. Details in [`backlot/README.md`](backlot/README.md).

---

## A clip you admire is a valid brief

Skip the blank-prompt anxiety. Hand Cutlin a **YouTube video, Short, Reel, TikTok link, or a local file** and it reverse-engineers the piece into a buildable blueprint:

1. **Drop in the reference**
2. **The agent recovers its narrative skeleton, cutting rhythm, shot logic, key frames, and visual temperament**
3. **Before real work begins, you get several divergent concept passes with tool routing, cost estimates, and preview samples**

```text
"I'm sending you a Short that really lands for me. Match its feel, but make the topic quantum computing."
```

What you get back is an articulate plan, not prompt voodoo: what the reference **contributes** (pacing skeleton, cold open, narrative shape, tone), what gets **swapped out** (subject, visual treatment, angle, narration style), roughly **what it will cost** at your target length, and **what it will actually look like** rendered with the tools you have.

### More prompt fuel

Each of these kicks off a full pipeline run. Free with zero keys:

> "Give me a 45-second animated piece on why cats always land on their feet"

> "A 60-second narrated video with captions: how container shipping changed the world"

> "Build a chart-heavy explainer on global renewable energy adoption"

The real-footage documentary route (also free):

> "A 90-second real-footage montage: the last hour before a harbor wakes up. No voiceover, quiet and wistful."

> "One minute of archival collage on the Space Race's public euphoria, essay-film flavor, sourced from open archives."

> "Real stock footage only: a drifting montage about night trains and the people asleep on them. Score it, skip the narration."

To lock that route in, name the format — **documentary montage**, **tone poem**, or **stock-footage collage** — and add **use real footage only**; the pipeline commits to retrieve-and-edit.

With generation providers configured (roughly $0.15–$3 per video):

> "30 seconds of Ghibli-flavored animation: a lighthouse keeper who tends a garden of glowing jellyfish at dusk"

> "Use AI-generated visuals to explain how neural networks learn, aimed at total beginners"

> "A cinematic 30-second teaser: the day every mirror on Earth started showing a five-second delay"

The **[Prompt Gallery](PROMPT_GALLERY.md)** holds field-tested prompts with cost expectations and sample outputs.

---

## The capability map

### Twelve pipelines

| Reach for it when | Pipeline | What lands in your folder |
|----------|----------|-----------------|
| teaching, tutorials, one topic done thoroughly | **Animated Explainer** | a finished explainer with research, narration, visuals, and score |
| social content, product showcases, abstract ideas | **Animation** | motion graphics, kinetic type, animated sequences |
| internal training, official announcements | **Avatar Spokesperson** | a digital presenter fronting your message |
| brand image, hype, promotion | **Cinematic** | trailers, teasers, mood-driven cuts |
| slicing long content for social | **Clip Factory** | one long source in, a prioritized batch of shorts out |
| video essays, mood pieces, real footage with no paid API | **Documentary Montage** | themed montages cut from a CLIP-searchable open-footage corpus |
| augmenting footage you already shot | **Hybrid** | your material + AI-generated supporting visuals |
| shipping in other languages | **Localization & Dub** | translation, subtitles, and re-voicing of existing video |
| promoting a show, visualizing audio | **Podcast Repurpose** | highlight moments turned into video |
| feature demos, walkthroughs, docs | **Screen Demo** | polished software screen recordings |
| talks, vlogs, interviews | **Talking Head** | presenter-led videos built around real people on camera |

All of them ride one skeleton: `idea → research → script → scene plan → assets → edit → compose`. A Markdown **director skill** governs each stage — goals, method, acceptance bar; the agent follows it, self-checks, writes checkpoints, and halts at creative forks for your sign-off. Research is non-negotiable: 15–25 live searches across YouTube, Reddit, news, and academic sources before a word of script exists.

### The vendor bench (all optional; the free path always works)

**Video generation, 14 strong** — cloud: Kling (strong output without the wait), Runway Gen-4 (the cinematic lane, Gen-3 Alpha Turbo through Gen-4 Aleph), Google Veo 3 (long takes, via fal.ai or HeyGen), Grok Imagine Video (reference-image driven), Higgsfield (multi-model with Soul ID character lock), MiniMax (the budget pick), HeyGen (one key, many models); local GPU, all free: WAN 2.1 (1.3B/14B), Hunyuan, CogVideo (2B/5B), LTX-Video (self-hostable on Modal); stock as backstop: Pexels, Pixabay, Wikimedia Commons.

**Image generation, 10 routes** — FLUX (front-of-pack quality), Google Imagen 4, Grok Imagine (edits, restyles, multi-image blends), GPT Image 2, Recraft (design-leaning), local Stable Diffusion (free), ManimCE (purpose-built math/science animation), plus the Pexels / Pixabay / Unsplash libraries.

**Text-to-speech, 4 voices** — ElevenLabs (the quality ceiling), Google TTS (700+ voices, 50+ languages — the localization workhorse), OpenAI TTS (quick and cheap), Piper (free and offline).

**Score & sound** — Suno (whole tracks with vocals, up to 8 minutes), ElevenLabs Music and SFX.

**The post suite (always free)** — FFmpeg for assembly and encoding, Video Stitch for joins and transitions, Video Trimmer for frame-accurate cuts, Audio Mixer with ducking, Audio Enhance for denoise and loudness, Color Grade via LUTs, Subtitle Gen for SRT/VTT; enhancement via Real-ESRGAN upscaling, rembg background removal, CodeFormer/GFPGAN face restoration; analysis via WhisperX word-level transcription, scene-boundary detection, smart frame sampling, and CLIP/BLIP-2 visual understanding; avatars via SadTalker/MuseTalk animation and Wav2Lip mouth sync.

> Sign-up steps, price tags, and free-tier limits for every vendor live in one place: [`docs/PROVIDERS.md`](docs/PROVIDERS.md).

### Three composition engines

| Engine | Runs as | What it brings |
|--------|------|-------------|
| **Remotion** | local (Node.js) | video written in React: spring-animated image scenes, data reveals, chapter cards, showcase cards, TikTok-style word captions, four transition families, Google Fonts, fade-curved audio, TalkingHead compositing. **With no video vendor configured it degrades gracefully: the agent produces stills and Remotion supplies all the motion.** |
| **HyperFrames** | local (Node.js ≥ 22) | video written in HTML/CSS/GSAP: kinetic type, product spots, launch teasers, registered blocks (data charts, noise layers, shader transitions), website-to-video, rigged SVG character performance. One `npx hyperframes` call, no monorepo download. |
| **FFmpeg** | local | the bedrock: assembly, encoding, subtitle burn-in, audio mux, color work |

Remotion versus HyperFrames is settled once, at the proposal stage, written to `render_runtime`, and frozen via `edit_decisions`; switching mid-run is a governance violation. The full decision matrix lives in `skills/core/hyperframes.md`.

---

## How far does zero keys go?

Everything `make setup` leaves you with, free:

| What you want | The free way to get it | How far it goes |
|-----------|-----------|-------------|
| **Narration** | Piper TTS | runs offline on your machine, natural-sounding delivery |
| **Open footage** | Archive.org + NASA + Wikimedia Commons | public-domain archive clips, educational media, documentary-grade material |
| **More stock** | Pexels + Unsplash + Pixabay | free photo and footage libraries; developer keys are free to register |
| **Compositing (React)** | Remotion | the full Remotion column above |
| **Compositing (HTML/GSAP)** | HyperFrames | the full HyperFrames column above |
| **Post** | FFmpeg | encode, burn subtitles, mix audio, grade color |
| **Captions** | built in | word-timed subtitles, generated automatically |

Three near-zero-cost routes to a finished film:

- **Stills, set in motion**: Piper reads the script, image tools supply frames, Remotion gives the cut its rhythm and movement.
- **Cartoon characters, performed locally**: SVG rigs with pose libraries on GSAP timelines, rendered by HyperFrames straight to `projects/<name>/renders/final.mp4`.
- **A film from real footage**: the documentary-montage pipeline builds a CLIP-searchable corpus from open sources, then cuts genuine motion into a complete piece.

## Want more? Drop keys into .env

```bash
# Nothing here is mandatory — fill in the keys you actually hold, delete the rest

# ── one key, several doors ─────────────────────────
FAL_KEY=<paste-yours>            # unlocks FLUX/Recraft imagery plus Veo, Kling, MiniMax video

# ── free stock libraries (sign up, get a key) ──────
PEXELS_API_KEY=<paste-yours>     # footage + photo library
PIXABAY_API_KEY=<paste-yours>    # footage + photo library
UNSPLASH_ACCESS_KEY=<paste-yours> # photo library

# ── soundtrack ─────────────────────────────────────
SUNO_API_KEY=<paste-yours>       # whole tracks with vocals or instrumentals, genre of your choosing

# ── direct lines to voice & image vendors ──────────
ELEVENLABS_API_KEY=<paste-yours> # flagship-grade TTS, with music and SFX on the side
OPENAI_API_KEY=<paste-yours>     # brings in OpenAI TTS and GPT Image 2
XAI_API_KEY=<paste-yours>        # Grok's image editing/creation and video generation
GOOGLE_API_KEY=<paste-yours>     # Imagen for stills, Google TTS with 700-odd voices

# ── extra video vendors ────────────────────────────
HEYGEN_API_KEY=<paste-yours>     # single door into VEO, Sora, Runway, and Kling
RUNWAY_API_KEY=<paste-yours>     # straight to Runway Gen-4
```

<details>
<summary><strong>Got a GPU in the box? Local video generation costs nothing</strong></summary>

```bash
make install-gpu

# then flip the local-generation switch in .env:
VIDEO_GEN_LOCAL_ENABLED=true
VIDEO_GEN_LOCAL_MODEL=wan2.1-1.3b  # swap in wan2.1-14b / hunyuan-1.5 / ltx2-local / cogvideo-5b
```

</details>

---

## Why it earns the pick

- **Twelve pipelines, fully staffed** — explainer, talking head, screen capture, trailer, animation, podcast repurposing, dubbing, and real-footage montage all ship ready to run
- **Fifty-two registered tools** — generation for video and stills, voice, scoring, mixing, captions, enhancement, and content understanding
- **Four hundred-plus skill files** — production standards, per-stage directors, creative playbooks, QA checklists, and deep-dive manuals that turn "can call the tool" into "uses it well"
- **A reference clip is a valid brief** — hand over a video you admire, get back a plan that is grounded yet distinct
- **Genuine films without buying a video model** — cut from real footage in free and open archives
- **Nobody locks you in** — vendors hot-swap freely, auto-ranked across seven axes
- **Shipping standards borrowed from software** — delivery promises catch "animated slideshows," pre-compose checks spare your GPU, a forced post-render audit keeps junk in-house, and every call lands in an auditable log
- **A gate on the wallet** — quotes before spending, hard caps, per-action approval thresholds

Hand it your own talking-head footage to fine-cut. Start an animated explainer from nothing. Split a two-hour podcast into a dozen social clips. Dub one piece into ten languages. **If a production crew could schedule it, Cutlin can orchestrate it.**

---

## How the machine runs

The architectural creed is **agent-first**: no orchestration program lurks backstage — the entity in the director's chair is your coding assistant itself.

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

**Python does the labor and the bookkeeping; it never makes the call.** Creative judgment, orchestration logic, review criteria, and quality bars all live in human-readable YAML manifests and Markdown skills you can read and rewrite. Every decision is archived with its alternatives, confidence score, and reasoning.

### The lay of the repo

```
Cutlin/
├── tools/              # 48 Python tools — the hands the agent works with
│   ├── video/          # 13 video generators plus compose, stitch, trim
│   ├── audio/          # 4 TTS vendors, Suno/ElevenLabs music, mixing, enhancement
│   ├── graphics/       # 9 image/graphics generators incl. charts, code cards, math animation
│   ├── enhancement/    # upscaling, background removal, face restoration, grading
│   ├── analysis/       # transcription, scene detection, frame sampling
│   ├── avatar/         # digital humans and lip sync
│   └── subtitle/       # SRT/VTT output
│
├── pipeline_defs/      # YAML manifests — the stage plays the agent performs
├── skills/             # Markdown skill library — the agent's working knowledge
│   ├── pipelines/      # per-stage directors for every pipeline
│   ├── creative/       # craft and technique skills
│   ├── core/           # core tool usage
│   └── meta/           # review standards and the checkpoint protocol
│
├── schemas/            # 15 JSON Schemas where artifacts prove their shape
├── styles/             # visual style playbooks (YAML)
├── remotion-composer/  # the React/Remotion composition engine
├── lib/                # foundations: config, checkpoints, pipeline loading
└── tests/              # contract tests, QA integration, evaluation kit
```

Knowledge sits in three tiers:

```
Tier 1  tools/ + pipeline_defs/    the inventory: what capabilities exist and how they chain
Tier 2  skills/                    the house rules: Cutlin's conventions and quality bars
Tier 3  .agents/skills/            the deep cuts: external technical know-how, on demand
```

Every tool declares which Tier-3 packs it leans on. The agent reads Tier 1 to count its cards, Tier 2 to learn the house rules, and opens Tier 3 only when a technique needs real depth.

---

## Production governance

Video production held to software-engineering rigor: a quality gate at every stage, an audit trail behind every decision, a constraint on every dollar.

**Quality gates.** The pre-compose check stops plans that break their delivery promise (pledging "motion-first" while 80% is stills), score critical on slideshow risk, or miss their renderer family — doomed plans die before they burn GPU. The post-render audit runs ffprobe, samples frames at four positions for black screens and broken overlays, analyzes audio for silence and clipping, verifies promises, and checks captions; a failing cut never reaches you. Slideshow risk is scored across six dimensions to block "PowerPoint that moves." When you submit your own media, each file is probed for real parameters — no guessing content from filenames.

**Scored selection.** Every vendor pick — video, image, voice, music — runs the 7-axis engine: task fit 30%, output quality 20%, control 15%, reliability 15%, cost efficiency 10%, latency and continuity 5% each. Losers' scores are archived beside the winner's. The selector also normalizes loose briefs into scoreable intent — even a single line like "Pixar-style short with consistent characters" — and its output carries the winner's `agent_skills` index so the agent can read the matching Tier-3 pack before writing a single generation prompt.

**Decision audit.** Vendor, style playbook, soundtrack, voice, renderer family, every fallback — recorded with alternatives, confidence, and reasoning, accumulated across stages and persisted. However the final film turned out, every step is traceable.

**Budget gates.** A quote before spending, funds reserved at call time, books balanced afterward; `observe` / `warn` / `cap` enforcement levels; per-action holds past the threshold (default $0.50); a global ceiling at $10, movable at will.

---

## Style and output specs

Three **style playbooks** act as a production's visual constitution — typography, palette, motion language, audio profile, and quality rules in one binding document: Clean Professional (corporate, education, SaaS), Flat Motion Graphics (social content, TikTok, startups), Minimalist Diagram (deep technical teardowns, architecture walkthroughs).

**Output presets** come ready for the major platforms: 16:9 landscape for YouTube 1080p/4K and LinkedIn; 9:16 vertical covering Shorts, Reels, and TikTok at 1080×1920; 1:1 square for Instagram feed at 1080×1080; and a 21:9 cinematic 2560×1080.

---

## If you are an agent reading this: welcome aboard

This repository was laid out for agents to work in. The fastest route to competence:

1. **Rules before work**
   Read [`AGENT_GUIDE.md`](AGENT_GUIDE.md) end to end, then build your map from [`PROJECT_CONTEXT.md`](PROJECT_CONTEXT.md).
2. **No improvised workflows**
   Everything runs on pipelines: orchestration lives in `pipeline_defs/`, per-stage direction in `skills/pipelines/`, and the registry discovers the tools.
3. **Count your cards before playing**
   ```bash
   python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.support_envelope(), indent=2))"
   python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.provider_menu(), indent=2))"
   ```
4. **Every video request starts with "which pipeline?"**
   The iron order: pick the pipeline, read its manifest, read the stage skills, and only then touch tools.

Per-platform entry files are ready: Claude Code reads `CLAUDE.md`; Cursor, `CURSOR.md` plus `.cursor/rules/`; GitHub Copilot, `COPILOT.md` plus `.github/copilot-instructions.md`; Codex, `CODEX.md`; Windsurf, `.windsurfrules`. All of them converge on the same two source documents: `AGENT_GUIDE.md` (the operating contract) and `PROJECT_CONTEXT.md` (the architecture map).

> On the roadmap: **Ollama** and **LM Studio** integration, so a local LLM can steer the whole pipeline with no cloud model in the loop.

---

## Extending and contributing

Extension points are baked in. A new tool: pick its home under `tools/`, drop a Python file, subclass `BaseTool` and fill in the contract; the registry recruits it automatically on scan — add a skill doc if usage isn't self-evident. A new pipeline: sketch the manifest in YAML under `pipeline_defs/`, give each stage a director skill under `skills/pipelines/<name>/`, and reuse tools where you can.

Going deeper: the technical panorama is in `docs/ARCHITECTURE.md`, vendor sign-up/pricing/quotas in `docs/PROVIDERS.md`, the agent contract in `AGENT_GUIDE.md`.

**Tests**:

```bash
# contract suite — runs clean with zero API keys configured
make test-contracts

# the whole battery
make test
```

**Feedback**: bugs, feature requests, and workflow discussion all go through [GitHub Issues](https://github.com/c18229039407-arch/cutlin/issues).

---

## License

[GNU AGPLv3](LICENSE)

## Acknowledgements

Cutlin is a modified fork of [OpenMontage](https://github.com/calesthio/OpenMontage) by calesthio. Thanks to the original authors for their excellent work.

---

**Cutlin** — video production with software-grade rigor: real quality gates, directed by your AI assistant.
