# Video Provider Scores — 8-Axis Baseline & Provenance

Provenance for `VIDEO_PROVIDER_BASELINE` in `lib/scoring.py`. Reviewed
2026-07. Every cell traces to public user-review sentiment (Trustpilot,
Reddit, Product Hunt, hands-on tested reviews) cross-checked against public
benchmarks (VBench / VBench-2.0, Artificial Analysis Elo).

## Why video gets its own axes

The generic 7-axis `ProviderScore` still drives image and TTS selection.
Video generation runs on 8 different axes because three of them — motion
stability, physical accuracy, audio capability — are meaningless for stills
and speech, and because provider quality on video is now documented publicly
in a way it is not for the other modalities.

| # | Axis | 中文 | What it measures |
|---|------|------|------------------|
| 1 | `prompt_following` | 提示词跟随 | Instruction adherence |
| 2 | `motion_stability` | 运动稳定 | Smoothness, absence of flicker/warping |
| 3 | `visual_quality` | 视觉质量 | Aesthetic + imaging quality |
| 4 | `physical_accuracy` | 物理准确性 | Weight, momentum, collision plausibility |
| 5 | `subject_consistency` | 主体一致性 | Identity stability across frames and shots |
| 6 | `controllability` | 可控性 | Camera control, reference images, frame control |
| 7 | `audio_capability` | 音频能力 | Native synchronized audio / dialogue / lip-sync |
| 8 | `engineering` | 工程维度 | Cost, reliability, billing trust, availability, latency |

Axis 4 is deliberately separate from axis 2: a model can move smoothly while
violating physics. VBench-2.0 exists precisely because the two diverge.

## Scene weight tables

Weights live in `VIDEO_SCENE_WEIGHTS`. Each sums to 1.0.

| 维度 | 电商广告 | 品牌TVC | 纪实 | 社媒短片 | general* |
|---|---|---|---|---|---|
| 主体一致性 | 25% | 20% | 15% | 10% | 17.5% |
| 工程维度 | 25% | 10% | 15% | 20% | 17.5% |
| 提示词跟随 | 15% | 15% | 10% | 15% | 13.75% |
| 可控性 | 15% | 20% | 10% | 10% | 13.75% |
| 视觉质量 | 10% | 20% | 15% | 15% | 15% |
| 运动稳定 | 6% | 10% | 10% | 15% | 10.25% |
| 物理准确性 | 2% | 3% | 20% | 5% | 7.5% |
| 音频能力 | 2% | 2% | 5% | 10% | 4.75% |

\* `general` is the arithmetic mean of the four authored tables, used when a
brief matches no scene vocabulary. It is derived, not authored.

Rationale for the authored tables:
- **电商广告** — the product must not deform (consistency 25%) and these ship
  in volume, so unit cost and reliability dominate (engineering 25%). Physics
  and audio barely matter; music is added in post.
- **品牌TVC** — art direction is the job: controllability and visual quality
  at 20% each. Engineering drops to 10% because a brand film is a low-volume,
  high-value shoot.
- **纪实** — physics jumps to 20%, the highest single physics weight anywhere:
  realistic content dies on implausible motion, and viewers spot it instantly.
- **社媒短片** — volume plus platform audio culture: engineering 20%, motion
  15%, audio 10%.

## Baseline scores

See `VIDEO_PROVIDER_BASELINE` for the numbers. Confidence and status flags:

- `confidence`: `high` (multiple independent user sources agree) / `medium`
  (thin or mixed) / `low` (benchmark or vendor sourced, little independent
  user corroboration).
- `status`: `available` / `restricted` / `deprecated` — procurement reality,
  not quality.

Both are applied as multipliers on the weighted score, so the ranker cannot
hand a production shot to something we cannot actually buy:

```
_CONFIDENCE_MULTIPLIER = {high: 1.0, medium: 0.97, low: 0.90, derived: 0.92}
_STATUS_MULTIPLIER     = {available: 1.0, restricted: 0.75, deprecated: 0.40}
```

**Verified effect (brand_tvc scene, 2026-07):** Seedance 2.0 scores 0.817 raw
— higher than Kling's 0.796 — but its overseas API was suspended in March
2026, so `restricted` drops it to 0.595 and it does not win. Sora 2 falls from
0.771 to 0.299 on `deprecated`. This is the intended behavior: **benchmark
leadership does not equal procurability.**

## Vendor-claim vs user-report conflicts

Where a vendor's marketing and independent user testing disagree, the score
follows the user reports and the conflict is recorded here.

1. **Kling subject consistency.** Vendor markets a character staying
   "identical across all six shots". Hands-on testers report facial likeness
   drift and lip-sync desync starting around shot 4-5 with 3+ speaking
   characters, and drift on clips beyond ~5s. Scored 0.72, not the ~0.9 the
   marketing implies.
2. **Hailuo (minimax) "zero flicker / physics mastery".** Independent testing
   shows temporal consistency collapsing in fast floor-work, with anatomy
   dissolving around the 3s mark. The truth is bimodal — excellent on calm
   motion, breaks on complex motion. Scored 0.86 motion / 0.74 physics rather
   than the near-ceiling the vendor implies.
3. **Seedance benchmark supremacy vs procurability.** Genuinely tops the Elo
   boards; overseas API suspended over copyright cease-and-desists. Quality
   scores kept high, `status: restricted` applied.
4. **HappyHorse "#1 model" vs availability.** Leads Artificial Analysis on
   both T2V and I2V, but public API access is not broadly available and there
   is essentially no independent user review data. `confidence: low` +
   `status: restricted`.
5. **Vidu "#2 globally" vs Trustpilot under 2.5/5.** Vendor cites the ranking;
   users report downtime, credits burned on failed renders, and bans.
   Reflected in `engineering: 0.38`.

## The engineering axis is blended, not static

`score_video_provider` blends the reviewed vendor-level baseline with this
call's live budget fit:

```
engineering = baseline_engineering * 0.6 + live_cost_efficiency * 0.4
```

So a provider that is generally fine but too expensive for the remaining
budget right now still gets marked down, while the reviewed signal (billing
trust, support quality, API maturity) stays dominant.

## Unreviewed providers

A provider with no baseline entry gets scores derived from what its tool
actually declares (`supports`, `best_for`) via `_derive_video_scores`, is
marked `data_source="derived"`, and is discounted 8%. Declared capability is
not measured quality — the discount says so.

Physics defaults to 0.45 for derived providers. Given VBench-2.0 reports most
models scoring under 60% on physics tasks, that prior is generous, not harsh.

## Maintenance

This market moves fast enough that the table is a snapshot, not a constant.
Re-review quarterly, and immediately when:
- a provider changes availability (API shutdown, regional suspension, GA);
- a major version ships (Kling 3.5, Seedance 2.5, Wan 2.7, LTX-2.3 were all
  in flight at review time);
- pricing moves materially (Veo cut ~47-62% during 2026).

Update the numbers here and in `VIDEO_PROVIDER_BASELINE` together, and note
what changed. Never raise a score on vendor marketing alone.
