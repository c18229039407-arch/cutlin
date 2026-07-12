<p align="center">
  <img src="assets/logo.png" alt="Cutlin" width="200">
</p>

<h1 align="center">Cutlin</h1>

<p align="center">简体中文 · <a href="README_en.md">English</a></p>

---

Cutlin 把你手边的 AI 编程助手升级成一支视频制作班底。你只负责说清楚想要什么，剩下的选题调研、写稿配音、素材制作、剪辑合成，交给智能体按流程推进。

**一个值得先讲明白的区别：** 市面上大量"AI 做视频"，本质是给几张静态图加个推拉镜头。Cutlin 当然也支持图生动画，但它同样能走**真素材路线**——智能体从免版税素材站和开放档案库里检索真实拍摄的动态画面，按语义排序、有目的地取舍，再剪进时间线输出成片。这是剪辑，不是障眼法。

## 技术展示

Cutlin 不是把某家视频 API 包了一层壳，而是一套每个环节都设有强制质检的生产系统。

**流水线架构。** 每次生产都经过带检查点与审批门禁的分阶段流水线：

```
 创意 ──▶ 调研 ──▶ 脚本 ──▶ 场景规划 ──▶ 素材生成 ──▶ 合成 ──▶ QA ──▶ 渲染
   │        │        │          │            │          │       │
   └────────┴────────┴──────────┴────────────┴──────────┴───────┘
          检查点 · 决策日志 · 成本快照 · 审批门禁
```

**多供应商编排。** 图像、视频、语音、音乐供应商逐一经过 7 个维度的评分（质量、成本、延迟、风格匹配、可用性、许可、一致性），评分过程写入可审计的决策日志。粒度是"这一个镜头用哪个工具"，而不是整个项目绑死一家。

**三条合成引擎路径，按生产需求选择：**

| 引擎 | 适用场景 | 成本区间 |
|---|---|---|
| Remotion 合成 | 数据驱动场景、字幕、动态图形 | 免费（本地渲染） |
| 静帧动画（Ken Burns / 视差 / 粒子） | 静图转动态、动漫与编辑风格 | 每条约 $0.02–$0.15 |
| 生成式动态片段（Veo / Kling / MiniMax / 本地 Wan） | 真实运动镜头、电影感画面 | 每条约 $0.70–$3 |

**渲染前自审。** 每次出片前自动执行 ffprobe 校验、抽帧检查、音频电平分析、交付承诺核验和字幕检查——不合格的片子不会送到你面前。

**零 Key 基线。** 一个 API Key 都不配也能干活：素材库检索、时间线剪辑、本地 Remotion 渲染，这条免费路径始终可用。

---

## 从您已经喜欢的视频开始

与其对着空白提示词冥思苦想，不如直接丢给它一条你欣赏的片子。

给 Cutlin 一条 **YouTube 长片、Short、Reel、TikTok 链接，或者本地视频文件**，它会把这条片子逆向拆解，还原成一份能直接开工的制作蓝图：

1. **丢一条参考片进来**
2. **智能体逆向还原它的叙事骨架、剪辑节奏、分镜方式、关键画面与视觉气质**
3. **正式动工前，先交给你几版走向不同的概念方案，附带工具选型、花费估算和预览小样**

```text
"我把一条很打动我的 YouTube Short 发给你。照着它的感觉，帮我做一条讲量子计算的。"
```

你得到的不是一锅乱炖的猜测式提示词，而是一份说得清楚的方案：

- 参考片里**哪些被继承**：节奏骨架、开场钩子、叙事结构、整体基调
- **哪些被替换**：主题内容、视觉处理、切入角度、旁白方式
- 在你的目标时长下，素材生成动工前**大概要花多少钱**
- 用你当前可用的工具，**实际渲染出来会长什么样**

驱动端不挑平台：**Claude Code、Cursor、Copilot、Windsurf、Codex** 谁来都一样——只要这个 AI 助手读得了文件、跑得动代码，就能开工。

---

## 实时观测看板 — Cutlin Studio

聊天窗口告诉你智能体*说了什么*，**Cutlin Studio 让你看见生产*实际在做什么***：本地看板随流水线运行自动填充——阶段亮灯、脚本落页、素材卡片闪烁生成中、每一笔决策和花费都在墙上。

生产启动时智能体会自动为你打开它。手动打开：

```bash
python -m backlot open                  # 项目库 — 磁盘上的所有项目
python -m backlot open <project-id>     # 某次生产的实时看板
python scripts/backlot_simulate_run.py  # 还没跑过项目？看一次模拟生产
```

> **不想敲命令？** 仓库根目录提供双击启动脚本：Windows 双击 `打开观测端.bat`，macOS 双击 `打开观测端.command`（首次运行若被系统拦截，右键 → 打开）。

看板是只读的：它监视 `projects/` 目录并通过 SSE 实时推送，不干预生产。审批动作在 AI 助手的对话里完成。运行结束后可点「▶ 回放运行」按时间戳完整回放。详见 [`backlot/README.md`](backlot/README.md)。

---

## 快速开始

### 必备条件

- **Python 3.10 及以上** — 官网下载：[python.org](https://www.python.org/downloads/)
- **FFmpeg** — macOS 用 `brew install ffmpeg`，Ubuntu 用 `sudo apt install ffmpeg`，其余平台见 [ffmpeg.org](https://ffmpeg.org/download.html)
- **Node.js 18 及以上** — [nodejs.org](https://nodejs.org/)
- **任意一款 AI 编程助手** — Claude Code / Cursor / Copilot / Windsurf / Codex 皆可

### 安装与运行

```bash
# 取源码，进目录，一键装齐依赖
git clone https://github.com/c18229039407-arch/cutlin.git
cd cutlin
make setup   # = Python 依赖 + Remotion + piper-tts + 生成 .env
```

用你的 AI 编程助手打开这个目录，然后直接下需求：

```
"制作一个 60 秒的动画解说视频，讲解神经网络是如何学习的"
```

想走真素材路线的话：

```text
"来一条 75 秒的纪录片蒙太奇，主题是雨夜的城市。全程真实素材，不要旁白，基调偏挽歌，配乐要贴这个情绪。"
```

之后的事不用你操心：智能体联网调研选题、生成画面、写稿并按语音指导配音、自动找免版税配乐、烧录词级字幕、渲染成片。片子送到你眼前之前，系统会先跑一遍多点自检——ffprobe 校验、抽帧、音频电平分析、交付承诺核对、字幕检查；每一次供应商选择都经 7 维评分并留档；每一个创意节点都停下来等你点头。

> **机器上没有 `make`？** 手动跑一遍它做的事即可（macOS/Linux）：
> ```bash
> python3 -m venv .venv && source .venv/bin/activate   # 建好并激活虚拟环境
> python -m pip install -r requirements.txt            # Python 依赖
> ( cd remotion-composer && npm install )              # 渲染引擎依赖
> python -m pip install piper-tts                      # 免费本地 TTS
> cp .env.example .env                                 # 密钥配置模板
> ```
> Windows PowerShell 对应为：`py -3 -m venv .venv; .\.venv\Scripts\Activate.ps1; python -m pip install -r requirements.txt; cd remotion-composer; npm install; cd ..; python -m pip install piper-tts; Copy-Item .env.example .env`；若 `npm install` 抛 `ERR_INVALID_ARG_TYPE`，换 `npx --yes npm install` 再试。

### 如果你是正在阅读本文的智能体：欢迎上岗

这座仓库本来就是为智能体施工准备的。想最快进入状态，按这个顺序来：

1. **规则先行**
   开工前把 [`AGENT_GUIDE.md`](AGENT_GUIDE.md) 通读一遍，接着看 [`PROJECT_CONTEXT.md`](PROJECT_CONTEXT.md) 建立全局认知。
2. **工作流不许现编**
   一切生产走既定流水线：编排看 `pipeline_defs/`，各阶段怎么演看 `skills/pipelines/` 的导演技能，可用工具由 registry 扫描给出。
3. **开工前先清点装备**
   跑这两条命令看看当前环境解锁了什么：
   ```bash
   python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.support_envelope(), indent=2))"
   python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.provider_menu(), indent=2))"
   ```
4. **每条视频需求，第一问都是"该走哪条流水线"**
   顺序铁律：先定流水线，再读它的清单，再读阶段技能，最后才轮到调工具。

### 添加 API 密钥（可选 — 密钥越多 = 工具越多）

```bash
# .env 里没有必填项：拿到哪把钥匙就填哪把，空着的行删掉也无妨

# ── 一把顶多把的聚合网关 ──────────────────────────
FAL_KEY=<填你的密钥>            # 打通 FLUX/Recraft 出图与 Veo/Kling/MiniMax 出片

# ── 免费素材站（注册即领）─────────────────────────
PEXELS_API_KEY=<填你的密钥>     # 视频 + 图片素材库
PIXABAY_API_KEY=<填你的密钥>    # 视频 + 图片素材库
UNSPLASH_ACCESS_KEY=<填你的密钥> # 图片素材库

# ── 配乐 ─────────────────────────────────────
SUNO_API_KEY=<填你的密钥>       # AI 作整曲：带人声、带伴奏、流派随选

# ── 语音与图像各家直连 ─────────────────────────
ELEVENLABS_API_KEY=<填你的密钥> # 第一梯队 TTS，附带音乐与音效能力
OPENAI_API_KEY=<填你的密钥>     # 解锁 OpenAI 的 TTS 与 GPT Image 2
XAI_API_KEY=<填你的密钥>        # Grok 的图像编辑/生成与视频生成
GOOGLE_API_KEY=<填你的密钥>     # Imagen 出图 + 700 余种音色的 Google TTS

# ── 再多几家视频供应商 ─────────────────────────
HEYGEN_API_KEY=<填你的密钥>     # 一个入口转接 VEO/Sora/Runway/Kling
RUNWAY_API_KEY=<填你的密钥>     # 直连 Runway Gen-4
```

<details>
<summary><strong>机器带 GPU？本地视频生成一分钱不花</strong></summary>

```bash
make install-gpu

# 装完在 .env 里打开本地生成开关：
VIDEO_GEN_LOCAL_ENABLED=true
VIDEO_GEN_LOCAL_MODEL=wan2.1-1.3b  # 可换：wan2.1-14b / hunyuan-1.5 / ltx2-local / cogvideo-5b
```

</details>

---

## 零 API 密钥的体验

一分钱不花、一个 Key 不配，同样能出真片子。`make setup` 装完即拥有：

| 想做什么 | 靠什么免费做到 | 做到什么程度 |
|-----------|-----------|-------------|
| **旁白配音** | Piper TTS | 离线跑在本机，旁白听感自然 |
| **开源影像素材** | Archive.org + NASA + Wikimedia Commons | 公版档案片段、科教影像与纪录片级素材 |
| **额外素材库** | Pexels + Unsplash + Pixabay | 免费图库与视频库，开发者 Key 注册即得 |
| **合成 (React)** | Remotion | React 驱动的渲染：弹簧动画图片场景、文字卡、数据卡、图表、TikTok 式词级字幕、TalkingHead 数字人 |
| **合成 (HTML/GSAP)** | HyperFrames | HTML/CSS/GSAP 驱动的渲染：动态排版、产品短片、发布预告、网站转视频、绑定 SVG 角色动画 |
| **后期制作** | FFmpeg | 转码压制、字幕硬烧、多轨混音、色彩处理 |
| **字幕生成** | 内置 | 词级时间轴字幕，自动产出 |

Remotion 还是 HyperFrames，由 Cutlin 在提案阶段裁定并锁进 `render_runtime`：数据驱动解说和复用现有 React 场景库的需求默认走 Remotion；重度动态图形、更适合用 HTML + GSAP 表达的需求（包括 `character-animation` 流水线的 SVG/GSAP 绑定输出）默认走 HyperFrames。完整决策矩阵见 `skills/core/hyperframes.md`。

**几条几乎不花钱的路径：**

- **静图动起来：** 旁白交给 Piper，画面交给图像工具，Remotion 负责让静态素材带上动感与节奏。
- **卡通角色本地演出：** SVG 骨骼绑定配姿势库，GSAP 排时间线，HyperFrames 渲出角色表演，成片自动落在 `projects/<项目名>/renders/final.mp4`。
- **全真素材剪片：** 纪录片蒙太奇流水线先从 Archive.org、NASA、Wikimedia Commons（还可加挂 Pexels 与 Unsplash）建一座可 CLIP 语义检索的素材语料库，再把真实影像剪成完整作品。

如果目标是第三条路线（真实素材成片），下需求时把关键词说死：点名**纪录片蒙太奇 (documentary montage)**、**音画诗 (tone poem)** 或**素材拼贴 (stock-footage collage)** 之一，并且明确加一句**只用真实素材 (use real footage only)**，流水线就会锁定检索-剪辑路径。

---

## 尝试这些提示词

装好之后，任选一条丢进你的 AI 编程助手，每一条都会触发一次完整的流水线生产。

### 从参考视频开始

> "This short nails the vibe I want. Recreate that feel, but teach high-schoolers how mRNA vaccines work."（这条短片的气质正是我要的。复刻这种感觉，内容换成给高中生讲 mRNA 疫苗原理。）

> "Break down what makes this Reel work, then pitch me three fresh takes I could shoot for my app launch."（拆一拆这条 Reel 好在哪，再给我三个能用于 App 发布的全新方案。）

> "Steal the rhythm and the cold-open from this clip, and rebuild it as a 40-second piece on how GPS satellites keep time."（把这条片的节奏和冷开场"偷"过来，重做成一条 40 秒的 GPS 卫星授时解说。）

### 零密钥需求

> "Give me a 45-second animated piece on why cats always land on their feet"（做一条 45 秒动画：猫为什么总能四脚着地）

> "A 60-second narrated video with captions: how container shipping changed the world"（60 秒带旁白和字幕：集装箱如何改变世界）

> "Build a chart-heavy explainer on global renewable energy adoption"（做一条以图表为主的全球可再生能源普及解说）

### 免费的真实素材纪录片路径

> "A 90-second real-footage montage: the last hour before a harbor wakes up. No voiceover, quiet and wistful."（90 秒真实素材蒙太奇：港口苏醒前的最后一小时。不要旁白，安静而怅然。）

> "One minute of archival collage on the Space Race's public euphoria, essay-film flavor, sourced from open archives."（一分钟档案拼贴：太空竞赛年代的大众狂热，视频随笔味道，取材开放档案库。）

> "Real stock footage only: a drifting montage about night trains and the people asleep on them. Score it, skip the narration."（只用真实库存素材：夜行列车与车上睡着的人，一条漂浮感的蒙太奇。配乐要，旁白不要。）

### 配置了图像/视频提供商 (~0.15 美元–1.50 美元)

> "30 seconds of Ghibli-flavored animation: a lighthouse keeper who tends a garden of glowing jellyfish at dusk"（30 秒吉卜力味动画：黄昏时分打理发光水母花园的灯塔看守人）

> "An anime-style half-minute: an abandoned observatory on a snowfield, aurora overhead, one warm window lit"（动漫风 30 秒：雪原上被遗弃的天文台，极光当空，只有一扇窗透着暖光）

> "Use AI-generated visuals to explain how neural networks learn, aimed at total beginners"（用 AI 生成画面，给纯小白讲清楚神经网络怎么学习）

> "Cut a launch teaser for Lumo, a made-up desk lamp that reads your focus and shifts its light"（为虚构的感知专注度自动调光台灯 Lumo 剪一条发布预告）

### 完整设置 (~1 美元–3 美元)

> "A cinematic 30-second teaser: the day every mirror on Earth started showing a five-second delay"（30 秒电影感预告：某一天，地球上所有镜子都开始延迟五秒）

> "90 animated seconds on how the immune system fights a virus, for middle schoolers — playful narrator, original score"（面向中学生的 90 秒免疫系统抗病毒动画——旁白要俏皮，配乐要原创）

还想找灵感？翻翻 **[提示词画廊](PROMPT_GALLERY.md)**——里面的每条提示词都实际跑通过，标注了预期花费和产出效果。等不及的话，`make demo` 一条命令马上渲一段零密钥样片。

---

## 流水线

一条流水线就是一套从想法到成片的完整工序。

| 流水线 | 交付什么 | 什么时候用它 |
|----------|-----------------|----------|
| **动画解说 (Animated Explainer)** | 调研、旁白、画面、配乐一站配齐的解说成片 | 科普、教程、把一个主题讲透 |
| **动画 (Animation)** | 动态图形、字体动效与序列动画 | 社媒内容、产品展示、抽象概念可视化 |
| **化身代言 (Avatar Spokesperson)** | 由数字人担纲主讲的视频 | 内部培训、企业口径发布 |
| **电影级 (Cinematic)** | 预告、先导与情绪流剪辑 | 品牌形象、造势与推广 |
| **片段工厂 (Clip Factory)** | 一条长片进，一批排好优先级的短片出 | 长视频拆条、社媒分发 |
| **纪录片蒙太奇 (Documentary Montage)** | 基于 CLIP 索引的免费影像库与开放档案（Pexels、Archive.org、NASA、Wikimedia、Unsplash）剪出的主题蒙太奇 | 视频随笔、情绪短片、检索优先的空镜剪辑、无付费视频 API 的真素材成片 |
| **混合 (Hybrid)** | 你的实拍 + AI 补充画面 | 在既有素材上叠加视觉增强 |
| **本地化与配音 (Localization & Dub)** | 现成视频的翻译、字幕与重新配音 | 出海与多语种发行 |
| **播客重制 (Podcast Repurpose)** | 把播客的高光段落做成视频 | 节目引流、音频内容可视化 |
| **屏幕演示 (Screen Demo)** | 打磨过的软件操作录屏 | 功能演示、上手教程、配套文档 |
| **口播 (Talking Head)** | 以真人出镜讲述为主体的成片 | 演讲实录、vlog、对谈 |

所有流水线共享同一套骨架：

```
研究 -> 提案 -> 脚本 -> 场景规划 -> 资产生成 -> 剪辑 -> 合成
```

每个阶段背后站着一位**导演技能 (director skill)**：一份 Markdown 写成的岗位说明书，规定这一步的目标、手法和验收线。智能体照着它调工具、自我检查、落盘检查点；碰到需要拍板的创意节点，就先停手来问你。

> **联网调研是正式工序，不是点缀。** 动笔写稿之前，智能体会检索 YouTube、Reddit、Hacker News、新闻站和学术资源，收集数据点、受众关心的问题、热门切入角度和视觉参考，全部沉淀进结构化的调研简报。你的视频建立在当下的真实信息上，而不是模型幻觉出来的"事实"。

---

## 为什么选择 Cutlin？

多数 AI 视频工具的交付物是"一条提示词换一段片段"。Cutlin 给你的是**端到端的制作流水线**——真实制作团队的那套工序，由你的 AI 智能体代劳。

多数"免费 AI 视频"方案的潜台词是"给静态图加动效"。Cutlin 也会这一手，但它还能用免费/开源渠道的**真实素材**成片：语义排序、有意图地剪辑、按正规时间线渲染输出。

自己拍的口播交给它精剪；一条全动画解说从零起稿；两小时的播客拆出一打社交短片；同一条内容配成十国语言；库存空镜混搭 AI 场景，拼出电影质感的品牌预告。**凡是一支制作团队排得出的活儿，Cutlin 都排得动。**

- **十二条成建制的流水线**：从解说、口播、录屏、预告，到动画、播客拆条、多语配音、真素材蒙太奇，一条不缺
- **五十二件专业工具**：视频与图像生成、配音、作曲、混音、字幕、画质增强、内容理解，全部注册在案
- **四百余份智能体技能**：制作规范、阶段导演、创意方法论、质检清单加深度技术手册，把"会用工具"升级成"用得地道"
- **拿参考片当需求书**：丢一条你欣赏的视频进来，系统把它翻译成一份既扎实又不雷同的制作方案，省去憋提示词的痛苦
- **不买视频模型照样出真片**：靠免费与开源渠道的真实影像和档案素材剪成片，而不是给静图加个缩放糊弄
- **调研是硬性工序**：动笔前对 YouTube、Reddit、新闻与学术源做 15-25 轮联网检索，内容锚定在当下的真实信息上
- **免费本地与付费云端双轨并行**：每项能力都备着开源方案和高级 API 两手，手里有什么就用什么
- **谁家都锁不住你**：供应商随插随换，7 个维度（任务契合、质量、控制、可靠性、性价比、延迟、连续性）打分自动择优
- **出厂标准向生产级看齐**：交付承诺拦"会动的 PPT"，合成前校验省 GPU，渲染后强制自审（ffprobe + 抽帧 + 音频分析），每个决策进可审计的日志
- **钱袋子有闸门**：事前估价、支出上限、单笔审批阈值三重保险，月底账单不会吓到你

---

## 工作原理

Cutlin 的架构信条是**智能体优先 (agent-first)**：系统里不存在一个躲在后台调度一切的编排程序——坐在编排席上的，就是你的 AI 编程助手自己。

```
你说："帮我做一条讲黑洞如何形成的解说片"
 │
 ▼
读流水线清单 (YAML)：这次生产有哪些阶段、用哪些工具、验收线在哪
 │
 ▼
读阶段导演技能 (Markdown)：每一步具体该怎么干
 │
 ▼
调 Python 工具干活：选型器先按 7 个维度给候选工具排座次
 │
 ▼
按审阅者技能自查：Schema 校验、是否忠于剧本、质量达标与否
 │
 ▼
落盘检查点 (JSON)：断点可续，决策日志与成本快照随行
 │
 ▼
到创意节点就停：方案摆到你面前，等你点头再走
 │
 ▼
合成前闸门：核交付承诺、测幻灯片风险、查渲染器合规
 │
 ▼
开渲染（Remotion 或 FFmpeg）：按视觉语法匹配合成引擎
 │
 ▼
渲染后复检：ffprobe、抽帧、音频分析、承诺兑现核对
 │
 ▼
成片出厂——前提是通过了上面每一道检查
```

**Python 负责工具与持久化，不负责决策。** 全部创意判断、编排逻辑、审查标准和质量门槛都写在人类可读的指令文件里（YAML 清单 + Markdown 技能），随你审阅和改写。每一项决定连同备选方案、置信度评分和推理过程一并留档。

---

## 架构

```
Cutlin/
├── tools/              # 48 件 Python 工具——智能体伸得出去的"手"
│   ├── video/          # 视频生成 ×13，外加合成、拼接与裁切
│   ├── audio/          # TTS ×4，Suno/ElevenLabs 配乐，混音与音频增强
│   ├── graphics/       # 图像/图形生成 ×9，含图表、代码卡片、数学动画
│   ├── enhancement/    # 超分放大、抠背景、面部修复、调色
│   ├── analysis/       # 语音转写、场景切分、抽帧
│   ├── avatar/         # 数字人与唇形同步
│   └── subtitle/       # 产出 SRT/VTT 字幕
│
├── pipeline_defs/      # YAML 流水线清单——智能体照着演的"分场剧本"
├── skills/             # Markdown 技能库——智能体的"业务知识"
│   ├── pipelines/      # 每条流水线各阶段的导演技能
│   ├── creative/       # 创意手法类技能
│   ├── core/           # 核心工具用法
│   └── meta/           # 审阅规范与检查点协议
│
├── schemas/            # 15 份 JSON Schema，产物契约在此验明正身
├── styles/             # 视觉风格剧本（YAML）
├── remotion-composer/  # React/Remotion 合成引擎
├── lib/                # 地基设施：配置、检查点、流水线装载
└── tests/              # 契约测试、QA 集成与评估套件
```

### 三层知识架构

```
第 1 层  tools/ + pipeline_defs/    盘点家底：有哪些能力可调，怎么编排
第 2 层  skills/                    立好规矩：Cutlin 的用法约定与验收标准
第 3 层  .agents/skills/            补足专业：具体技术领域的深度知识包
```

每个工具都会自报家门：声明自己关联哪些第 3 层知识包。智能体的阅读顺序也随之清晰——第 1 层点清家底，第 2 层学会规矩，真要钻进某项技术的细节时，再翻第 3 层。

---

## 支持的提供商

> 每家怎么注册、收费几何、白嫖额度有多少——[`docs/PROVIDERS.md`](docs/PROVIDERS.md) 一篇讲全。

<details>
<summary><strong>视频生成：十四家供应商坐镇</strong></summary>

| 供应商 | 接入方式 | 一句话点评 |
|----------|------|-------|
| **Kling** | 云端 API | 画质在线，出片也快 |
| **Runway Gen-4** | 云端 API | 电影质感路线；覆盖 Gen-3 Alpha Turbo 至 Gen-4 Aleph |
| **Google Veo 3** | 云端 API | 擅长长镜头与电影感；走 fal.ai 或 HeyGen 通道 |
| **Grok Imagine Video** | 云端 API | 支持参考图出片，xAI 原生短视频 |
| **Higgsfield** | 云端 API | 聚合多模型；Soul ID 锁定角色形象不走样 |
| **MiniMax** | 云端 API | 花小钱办大事的选项 |
| **HeyGen** | 云端 API | 一个 Key 通多家模型的网关 |
| **WAN 2.1** | 本地 GPU | 零成本；1.3B / 14B 双规格 |
| **Hunyuan (混元)** | 本地 GPU | 零成本，画面表现拿得出手 |
| **CogVideo** | 本地 GPU | 零成本；2B / 5B 双规格 |
| **LTX-Video** | 本地 GPU / Modal | 本地白嫖，也能自托管到云上 |
| **Pexels** | 素材库 | 免费库存视频 |
| **Pixabay** | 素材库 | 免费库存视频 |
| **Wikimedia Commons** | 素材库 | 免费/开放的库存视频与档案影像 |

</details>

<details>
<summary><strong>图像生成：十种来源任你调</strong></summary>

| 供应商 | 接入方式 | 一句话点评 |
|----------|------|-------|
| **FLUX** | 云端 API | 画质稳居第一梯队 |
| **Google Imagen** | 云端 API | Imagen 4：画质高，宽高比选择多 |
| **Grok Imagine Image** | 云端 API | 强在改图、迁移风格与多图融合 |
| **GPT Image 2** | 云端 API | OpenAI 的图像模型 |
| **Recraft** | 云端 API | 偏设计感的生成路线 |
| **Local Diffusion** | 本地 GPU | 本机跑 Stable Diffusion，不花钱 |
| **Pexels** | 素材库 | 免费库存图片 |
| **Pixabay** | 素材库 | 免费库存图片 |
| **Unsplash** | 素材库 | 免费库存图片 |
| **ManimCE** | 本地 | 数理科普动画的专用引擎 |

</details>

<details>
<summary><strong>语音合成 TTS：四条路可选</strong></summary>

| 供应商 | 接入方式 | 一句话点评 |
|----------|------|-------|
| **ElevenLabs** | 云端 API | 音质对标行业上限 |
| **Google TTS** | 云端 API | 音色 700+、语言 50+，做本地化绕不开 |
| **OpenAI TTS** | 云端 API | 速度快，价格低 |
| **Piper** | 本地 | 免费且离线可用 |

</details>

<details>
<summary><strong>配乐、音效与全套后期</strong></summary>

**音乐与音效：**

| 供应商 | 接入方式 | 一句话点评 |
|----------|------|-------|
| **Suno AI** | 云端 API | 整首歌连人声带歌词一起生成，流派不限，单曲最长 8 分钟 |
| **ElevenLabs Music** | 云端 API | 配乐类 AI 生成 |
| **ElevenLabs SFX** | 云端 API | 按描述产出音效 |

**后期制作（始终可用，完全免费）：**

| 组件 | 拿来干什么 |
|------|-------------|
| **FFmpeg** | 组装成片、转码、硬字幕、混音 |
| **Video Stitch** | 片段串接、交叉溶解、画中画与多画面排布 |
| **Video Trimmer** | 帧级精度的截取与抽段 |
| **Audio Mixer** | 多轨合成、人声闪避、淡入淡出曲线 |
| **Audio Enhance** | 去噪与响度归一 |
| **Color Grade** | 套 LUT 做整体调色 |
| **Subtitle Gen** | 按时间戳生成 SRT/VTT |

**画面增强：**

| 组件 | 拿来干什么 |
|------|-------------|
| **Upscale** | Real-ESRGAN 图像与视频超分辨率 |
| **Background Remove** | rembg / U2Net 一键抠背景 |
| **Face Enhance** | 人脸区域画质提升 |
| **Face Restore** | CodeFormer / GFPGAN 修复受损人脸 |

**分析：**

| 组件 | 拿来干什么 |
|------|-------------|
| **Transcriber** | WhisperX 转写，精确到每个词的时间戳 |
| **Scene Detect** | 自动找出镜头切换点 |
| **Frame Sampler** | 有策略地抽取关键帧 |
| **Video Understand** | CLIP/BLIP-2 看懂画面内容 |

**化身与唇形同步：**

| 组件 | 拿来干什么 |
|------|-------------|
| **Talking Head** | SadTalker / MuseTalk 驱动数字人开口 |
| **Lip Sync** | Wav2Lip 按音频对口型 |

**合成与渲染：**

| 引擎 | 运行形态 | 能力清单 |
|--------|------|-------------|
| **Remotion** | 本地 (Node.js) | 用 React 写视频：图片场景配弹簧动效、数据揭示动画、章节题卡、展示卡片、TikTok 风格逐词字幕、四类转场（淡化/滑动/擦除/翻转）、Google Fonts 排版、可淡化的音频轨，还能合成 TalkingHead 数字人。**没配任何视频生成商时会自动降级：智能体只出静态图，由 Remotion 负责让它们动起来。** |
| **HyperFrames** | 本地 (Node.js ≥ 22) | 用 HTML/CSS/GSAP 写视频：字体动效、产品宣传短片、发布倒计时、自定义动态图形，外加注册制区块（数据图表、噪点层、着色器转场）、把网页直接变成视频、SVG 绑定角色表演。一句 `npx hyperframes` 即可调用，整个 monorepo 不用下载。 |
| **FFmpeg** | 本地 | 一切的地基：装配、压制、烧字幕、合音轨、调颜色 |

用哪套渲染运行时，在提案阶段就一锤定音（写入 `render_runtime`），并经 `edit_decisions` 固化。开工后擅自改换运行时属于治理红线，具体裁量规则见 `skills/core/hyperframes.md`。

</details>

---

## 风格系统

风格剧本 (Style playbooks) 是一次生产的视觉宪法：

| 风格剧本 | 适配的内容类型 |
|----------|----------|
| **干净专业 (Clean Professional)** | 企业宣传、教育课程、SaaS 产品 |
| **扁平动态图形 (Flat Motion Graphics)** | 社媒短内容、TikTok、创业团队 |
| **极简图解 (Minimalist Diagram)** | 硬核技术拆解、系统架构讲解 |

剧本统一约束排版、配色、运动语言、音频配置和质量规则；智能体读取后贯彻到每一件生成的素材上。

---

## 平台输出配置

主流平台的渲染档位开箱即备：

| 输出档位 | 像素规格 | 画幅 |
|---------|-----------|--------------|
| YouTube 宽屏 (Landscape) | 1920x1080 | 16:9 |
| YouTube 4K | 3840x2160 | 16:9 |
| YouTube 短片 (Shorts) | 1080x1920 | 9:16 |
| Instagram Reels | 1080x1920 | 9:16 |
| Instagram 动态 (Feed) | 1080x1080 | 1:1 |
| TikTok | 1080x1920 | 9:16 |
| LinkedIn | 1920x1080 | 16:9 |
| 电影级 (Cinematic) | 2560x1080 | 21:9 |

---

## 制作治理

Cutlin 用对待软件工程的严格程度对待视频生产：每个阶段有质检关卡，每个决定有审计痕迹，每笔支出有约束。

### 质量检验门

- **合成前校验** — 交付承诺被违反（比如承诺"以运动为主"结果 80% 是静图）、幻灯片风险评分达到危急、渲染器族缺失，任何一条都会拦下渲染。烂方案在烧 GPU 之前就被截停。
- **渲染后自审** — 每次出片后，运行时自动跑 ffprobe 校验、在 4 个位置抽帧排查黑屏与破损叠层、分析音频是否静音或削波、核对交付承诺、检查字幕。自审不过，片子不见人。
- **PPT 风险评分** — 从 6 个维度（重复度、装饰性画面、运动幅度不足、镜头意图、过度依赖排版、名不副实的电影级宣称）打分，堵住"会动的 PPT"式产出。
- **源文件体检** — 用户提交自有素材时，系统逐个探查文件（分辨率、编码、声道、时长），先建立规划底数再做任何创意决定。不再靠文件名脑补内容。

### 基于评分的提供商选择

视频、图像、语音、音乐——任何一次供应商选型都要走完 7 维打分：任务契合度权重 30%，输出质量 20%，控制能力 15%，可靠性 15%，成本效益 10%，延迟与连续性各 5%。最终不只记录谁赢了，落选者的分数同样进档案，方便日后复盘。

选择器打分前会先归一化松散的简报语境——就算智能体手里只有一句"皮克斯风格、角色要一致的动画短片"，选择器也能把它展开成可评分的意图与风格信号，不要求预先构造完美的 `task_context`。

评分结果里还夹带一份"导航"：胜出供应商对应的 `agent_skills` 索引。智能体动笔写生成提示词之前，可以顺着索引先补完该供应商的第 3 层专业知识。

### 决策审计跟踪

每一个重要的创意与技术选择——供应商、风格剧本、配乐曲目、音色、渲染器族，以及任何备选与降级——都会连同备选项、置信度和推理一起记录。决策日志跨阶段累积持久保存，最终成片长成什么样，每一步都可回溯。

### 预算控制

- 花之前**先报价**：这一步预计多少钱，提前亮出来
- 调用时**先圈钱**：额度锁定后才允许发起请求
- 结束后**再对账**：以实际消耗入账，预估与实付都留痕
- **三档管控模式**任选：`observe` 只记录、`warn` 超了就喊、`cap` 到顶即停
- **单笔超阈值要人批**：默认 0.50 美元以上的动作先挂起等你确认
- **全局封顶**默认 10 美元，数字随你改

账单没有惊喜。花钱之前，智能体先把数字摆给你看。

---

## 智能体兼容性

只要能读文件、能执行 Python 的 AI 编程助手都能驱动 Cutlin。各平台的专属指令文件已经备好：

| AI 助手 | 专属入口文件 |
|----------|------------|
| **Claude Code** | `CLAUDE.md` |
| **Cursor** | `CURSOR.md` + `.cursor/rules/` |
| **GitHub Copilot** | `COPILOT.md` + `.github/copilot-instructions.md` |
| **Codex** | `CODEX.md` |
| **Windsurf** | `.windsurfrules` |

各平台的入口文件殊途同归，最终都指向同两份母文档：`AGENT_GUIDE.md`（智能体的操作契约）与 `PROJECT_CONTEXT.md`（架构地图）。

> 路线图上的一项：对接 **Ollama** 和 **LM Studio**，让整条流水线可以由本地大模型驱动，彻底摆脱云端依赖。

---

## 参与贡献

Cutlin 的架构天然为扩展而生。两种最常见的贡献方式：

### 添加新工具

1. 挑好归属的 `tools/` 子目录，落一个新的 Python 文件
2. 继承 `BaseTool`，把工具契约的方法补齐
3. 什么都不用注册——registry 扫描时自动收编
4. 用法不自明的工具，请附一份配套技能文档

### 添加新流水线

1. 先在 `pipeline_defs/` 用 YAML declare 出整条流水线的清单
2. 到 `skills/pipelines/<流水线名>/` 给每个阶段配上导演技能
3. 工具能复用就复用，缺口再按上面的方法补

完整技术参考见 `docs/ARCHITECTURE.md`，提供商指南（安装、定价、免费额度）见 `docs/PROVIDERS.md`，智能体契约见 `AGENT_GUIDE.md`。

---

## 联系方式

Bug 反馈、功能建议和工作流讨论，请统一走 [GitHub Issues](https://github.com/c18229039407-arch/cutlin/issues)，方便追踪和落实。

---

## 测试

```bash
# 契约测试套件——一个 API Key 都不配也能全绿
make test-contracts

# 全量测试
make test
```

---

## 许可证

[GNU AGPLv3](LICENSE)

## 致谢

Cutlin 基于 [OpenMontage](https://github.com/calesthio/OpenMontage)（作者 calesthio）修改而来，感谢原作者的出色工作。

---

**Cutlin** — 由你的 AI 助手执导、带真实质检关卡的生产级视频系统。
