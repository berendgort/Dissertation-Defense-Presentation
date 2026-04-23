# Speaker Notes · Backup Slides B1–B15

These are the 15 backup slides. Each slide maps to one of the most likely committee
attacks against the dissertation. This file is the private script: it does NOT show
on the projected slides.

Every answer follows the `BRACE / PANEL` protocol from
`question_answering/question_answering.md` and
`question_answering/committee/ANSWER_FORMAT.md`:

- `B`reathe / `P`ause — 1–3 s, do not start talking in a rush.
- `R`estate the question in one clean sentence.
- `A`nswer first — one-sentence position, no backstory.
- `C`ite one anchor — one number, one comparison, one design reason.
- `E`dge and `E`nd — scope / limitation, then land the contribution.

Default structure: **Claim → Proof → Boundary → Meaning**.
Target length: 30 s. Stretch to 60 s only for important technical questions.

> One number per answer. Never bluff. Stop after the main point.

---

## Top 15 Weak Points — Why These 15 Slides Exist

These are the fifteen places where the dissertation is most likely to be pressed.
They are the reason B1–B15 exist in exactly this order.

1. **B1 — Statistical rigor.** Are the gaps real or split noise?
2. **B2 — Baseline fairness.** Did baselines get a fair chance?
3. **B3 — Trace and dataset selection.** Why this pod, these cells, this subsample?
4. **B4 — Simulator and twin fidelity.** Are we leaning on a friendly simulator?
5. **B5 — LLM reproducibility.** How does anyone reproduce `78.3%` next year?
6. **B6 — PARES / what counts as an agent.** Is `AgentEdge` really agentic?
7. **B7 — Why `78.3%` and not `100%`.** If the twin is a filter, why does anything fail?
8. **B8 — Scaling and context window.** Why do savings peak at `20` nodes?
9. **B9 — Success metric.** Is exact end-state matching too strict or too convenient?
10. **B10 — State staleness.** What happens between plan and execute?
11. **B11 — AERO vs Pathformer CPU/RAM chart.** Was Pathformer judged on fair bars?
12. **B12 — Informer / Pathformer / AERO roles.** Why didn't you also benchmark Informer?
13. **B13 — AERO beyond workload traces.** Does `AERO` generalize outside CPU/RAM?
14. **B14 — OmniFORE deployment and leakage.** Is the zero-shot protocol fair and deployable?
15. **B15 — 6G scope.** Is this really a 6G thesis or only cloud orchestration?

Each slide follows the same shape: `question → 3 anchored answer points → pivot`.
Every pivot point in the notes below ends on the thesis contribution, not on a technicality.

---

## B1 · Statistical Rigor

> _"How do I know these gaps aren't just split noise?"_

### 30-second answer — `BRACE`

- **(B)** Pause. Don't defend at volume.
- **(R)** "The question is whether the reported improvements could be explained by random variation instead of real architectural effects."
- **(A)** "The short answer is no. The effect sizes are an order of magnitude larger than the noise floor in every chapter."
- **(C)** One anchor: `AgentEdge` runs `630` trials across `6` scenarios (`60` per arm) with Wilson-score intervals. The `2.76x` uplift over `ReAct` and the `10x` drop in API-call variance are far outside any plausible split-draw.
- **(E/End)** "What I do not claim is formal paired hypothesis tests across models. That boundary is disclosed, not hidden. Within that boundary, the effects dominate the noise."

### Anchor number

`630` `AgentEdge` runs; `2.76x` success uplift; `10x` API-call-variance reduction.

### Follow-up traps

- _"Why no paired `t`-tests?"_ → The comparators differ in stochastic sources (LLM sampling vs. deterministic solvers). A paired test assumes matched draws that don't exist. Wilson intervals on a bounded binary outcome are the more honest statistic. I would add McNemar's or bootstrap tests as a reviewer-friendly extension, but they would not move the direction of the result.
- _"Only one seed per forecaster?"_ → `AERO` uses a shared `50`-trial Bayesian-optimization budget, so the comparison is budget-matched, not seed-matched. For `OmniFORE`, training repeats use `5` seeds and report mean. Live validation collapses the debate because the live pod is the same physical process for all predictors.

### Pivot out

"So effect sizes dominate plausible split noise. That lets the thesis keep its contribution claim intact: deployable prediction, transferable forecasting, and validated orchestration."

---

## B2 · Baseline Fairness

> _"Did the baselines really get a fair chance?"_

### 30-second answer — `BRACE`

- **(R)** "The concern is whether we handicapped the comparators to make our own numbers look better."
- **(A)** "The short answer is no. Same budget, same tools, same base model. Only the architecture differs."
- **(C)** Anchor: all forecasters (Pathformer, SparseTSF, ModernTCN, AGCRN, LSTNet, `AERO`, `OmniFORE`) share the same `50`-trial Bayesian-optimization budget, the authors' published hyperparameter ranges, and the same preprocessing. `ReAct` and `LATS` run on the same `12` Flask APIs, the same `Qwen 2.5-Coder-32B`, the same `6` scenarios, and the same metric harness as `AgentEdge`.
- **(E)** "What I cannot claim is perfect tuning of every baseline — no one can, in a monograph. What I can claim is that the procedure is symmetric."

### Anchor number

`50`-trial shared BO budget across forecasters; `12` shared Flask APIs across agent arms.

### Follow-up traps

- _"Why didn't you tune `ReAct` more aggressively?"_ → The single-agent arm in `AgentEdge` uses the same prompt effort and the same tool surface as `ReAct`. If the architecture of `ReAct` were the better choice, that arm would have won. It did not, even with our prompt effort on its side. That isolates architecture from raw LLM capability.
- _"Why not a DRL slice controller as baseline?"_ → DRL slice control is a strong candidate backend, but it solves a narrower optimization problem after intent is already formalized. A fair DRL comparison would require re-scoping the agentic problem. I flag that as future work in the synthesis slide.

### Pivot out

"The architecture is what differs — not budget, tools, or base model. That keeps the comparison honest."

---

## B3 · Trace and Dataset Selection

> _"Why this one pod, why a `20%` subsample, why Google cells `A`–`F`?"_

### 30-second answer — `BRACE`

- **(R)** "The question is whether the chosen traces bias the result."
- **(A)** "Each contribution answers its own question on its own protocol. No single trace is asked to carry three claims."
- **(C)** Anchors:
  - `AERO` — Alibaba `MS_11349` pod. Chosen because the comparator papers (Pathformer, SparseTSF) use it. Not our pick, their pick.
  - `OmniFORE` — train on Google cells `A`–`F`, zero-shot to held-out cells `G`–`H`, then cross-dataset to an Alibaba pod. Cell boundaries prevent leakage by construction.
  - `AgentEdge` — `6` public scenarios with multiple valid end-states per scenario, `630` runs.
- **(E)** "The Alibaba `20%` subsample is a disclosed compute limit. The generalization claim scales with target exposure, not with our wall-clock budget."

### Anchor number

`100` Google traces for `OmniFORE`, `6`-scenario `x` `60`-run matrix for `AgentEdge`.

### Follow-up traps

- _"`20%` means the result is cherry-picked."_ → The `20%` is `5`-minute aligned to the Google cadence. The purpose is transfer under limited target exposure, which is strictly harder than exhaustive in-distribution fit. More data would help our model more than it would help the comparators.
- _"Why not true 6G radio traces?"_ → No public 6G workload trace of this granularity exists yet. Borg/Alibaba are the best production-scale proxies for service-level orchestration. Wireless-native validation is explicitly flagged as future work, including through the collaboration with `Nearby Computing S.L.`.

### Pivot out

"Each contribution answers one question under its own protocol. No trace is doing three jobs."

---

## B4 · Simulator and Digital-Twin Fidelity

> _"Are the results leaning on a friendly simulator?"_

### 30-second answer — `BRACE`

- **(R)** "The concern is whether the simulator is validating itself."
- **(A)** "The twin is a gate, not an oracle. Predictor and simulator are loosely coupled by design."
- **(C)** Anchors:
  - The digital twin runs as a separate process, with separate state and `15–25%` injected timing and power jitter, so it is not a mirror of the executor.
  - `COSCO` is peer-reviewed (IEEE TPDS `2022`), and `AERO` trains on different traces from the `COSCO` workload distributions. So the predictor is not co-tuned with the simulator.
  - `AERO` closes Chapter `3` on a physical testbed under real drift — the live-drift anchor is independent of any simulator.
- **(E)** "Bare-metal validation of `AgentEdge` is explicit future work. The thesis does not claim full production-grade twin fidelity."

### Anchor number

`15–25%` jitter between twin and executor; live testbed confirms `AERO` under real drift.

### Follow-up traps

- _"If the twin is imperfect, the `78.3%` is overstated."_ → The twin's imperfection is why success is `78.3%`, not `100%`. A perfect twin would mean the critic could never miss. See B7.
- _"How much of the energy saving survives a different simulator?"_ → The cross-scale shape (floor at `8` nodes, peak at `20`, drop at `35`) is a context-window story, not a simulator story. See B8.

### Pivot out

"The twin is a risk-reduction layer, not a proof device. The contribution is validated autonomy, not blind autonomy."

---

## B5 · LLM Reproducibility

> _"How does anyone reproduce `78.3%` next year when the model changes?"_

### 30-second answer — `BRACE`

- **(R)** "The question is how durable the absolute number is when hosted LLMs drift."
- **(A)** "The comparison reproduces. The absolute number is instrument-dependent, and that boundary is disclosed."
- **(C)** Anchors:
  - Pinned model: `Qwen 2.5-Coder-32B` snapshot, named provider, prompt SHA-`256`, seeded randomness.
  - All arms — `ReAct`, `LATS`, single-agent, `AgentEdge` — share the same LLM, so the architectural delta survives provider drift.
  - Scale handles non-determinism: `60` runs per arm, never a single draw.
- **(E)** "I am not claiming bit-for-bit replay of a hosted snapshot. I am claiming the architectural ordering reproduces."

### Anchor number

`60` runs per arm; single shared LLM across agentic comparators.

### Follow-up traps

- _"Why `Qwen` and not the top-ranked benchmark model?"_ → The selection was empirical: `Qwen 2.5-Coder-32B` hit the best balance of success, reasoning quality, and acceptable runtime across `qwen3`, `qwen2.5`, `deepseek-*`, `gpt-oss`. I was selecting an instrument, not a benchmark trophy.
- _"Couldn't model updates invert your ranking?"_ → They could change the absolute success rate. They cannot invert the ordering that matters here, because the ablation (twin-off: `53.3%` vs `AgentEdge`: `78.3%`) uses the same model on both sides of the line. Architectural contribution is isolated from model identity.

### Pivot out

"The architectural claim reproduces. The absolute number is scoped to the instrument, which is the correct scoping for a defense."

---

## B6 · `PARES` — What Counts as an Agent

> _"What exactly counts as an agent in this thesis?"_

### 30-second answer — `BRACE`

- **(R)** "The question is whether the label 'agent' means anything concrete here."
- **(A)** "In this thesis an agent is anything that satisfies all five `PARES` capabilities: `Perceive`, `Act`, `Reason`, `Evaluate`, `Sustain`. A system missing any one of them is not agent-complete for orchestration."
- **(C)** Anchor: in the Chapter `5` state-of-the-art table, `AgentEdge` is the only system that passes all five letters. `ReAct` passes `Act` and `Reason` but has no separate `Evaluate` stage; that is exactly why the digital-twin ablation hurts it.
- **(E)** "`PARES` is synthesized from six representative agentic-AI frameworks, not copied from a single one. I am not proposing it as a standard; I am using it as a disciplined minimal vocabulary so the architectural claim is testable."

### Anchor number

`5` capabilities; only `AgentEdge` passes all `5` in the Ch. `5` comparison table.

### Follow-up traps

- _"Why five? Why not four, or seven?"_ → Four would drop `Sustain`, which is what separates a stateless chat system from a closed-loop orchestrator. Seven starts to mix capabilities with implementation choices. Five is the minimal set that keeps the mapping to `Intent → Observe → Plan → Act` clean.
- _"Is `Sustain` not just memory?"_ → `Sustain` is memory plus persistent identity across the control loop. Rejected plans, accepted plans, and deadlock evidence all survive across iterations. Without that, `ActSimCrit` would keep discovering the same failure.

### Pivot out

"`PARES` is what gives the contribution a testable contract. It is what lets me say `validated autonomy` without it being a vibe."

---

## B7 · Why `78.3%` and not `100%`

> _"If the critic validates on a twin, why does anything fail?"_

### 30-second answer — `BRACE`

- **(R)** "The question is how a validated system can still miss `21.7%` of the time."
- **(A)** "Three sources of residual failure, and all three are disclosed rather than tuned away."
- **(C)** Anchors:
  1. Critic recall — any LLM-based critic admits a small fraction of plans that the solver then rejects at execution.
  2. Twin-live mismatch — `15–25%` timing and power jitter between validation and execution can turn a marginal plan into a failing one.
  3. Refinement cap — unsolvable intents end as observable deadlock, which is counted as failure rather than as "skipped scenario."
- **(E)** "The key contrast is `AgentEdge` `78.3%` vs twin-off `53.3%`: the twin moves the delta by `1.47x` over direct planning. Unsafe-action containment stays at `100%` — the remaining failure is observable and explicit, never silent."

### Anchor number

`78.3%` with twin vs `53.3%` without twin — `1.47x` uplift from `ActSimCrit` alone.

### Follow-up traps

- _"So the twin is not strictly better."_ → It is strictly better on success, variance, and containment. It is not perfect, and the thesis does not claim that. What it claims is validated autonomy, not infallible autonomy.
- _"How many of the failures are silent vs observable?"_ → All observed failures are observable by design, because the critic logs the rejection reason and the solver logs the deadlock. Zero silent infrastructure-damaging actions were observed across `630` runs.

### Pivot out

"The remaining `21.7%` is disclosed residual — not hidden failure. That is what makes the safety claim defensible."

---

## B8 · Scaling Behavior and the Context Window

> _"Why does energy saving peak at `20` nodes and drop at `35`?"_

### 30-second answer — `BRACE`

- **(R)** "The question is whether the scaling curve is a flaw in the architecture."
- **(A)** "No, the shape is a context-budget effect, not an architecture effect. And it is predictable."
- **(C)** Anchors:
  - `8` nodes: saving `~89 W`. Floor-limited — there isn't much to consolidate.
  - `20` nodes: saving `300.8 W`. The full state fits the planner context — the sweet spot.
  - `35` nodes: saving `185.2 W`. State overflows the context window — the planner starts losing information.
- **(E)** "The `150 ms` `AgentEdge` decision budget is a future-work target aligned with O-RAN / MEC literature, not a today claim. The limit that matters today is context engineering, which is exactly the future-work direction on slide `49`."

### Anchor number

`300.8 W` peak saving at `20` nodes; `50 ms` scheduler inference + `150 ms` decision target.

### Follow-up traps

- _"So `AgentEdge` doesn't scale."_ → It scales within its context budget, which is an LLM capability constraint, not an architecture constraint. Semantic tool discovery, state summarization, and smaller specialized models (future work directions) all shift the cliff further out without redesigning `AgentEdge`.
- _"Why not just throw in a larger-context model?"_ → Context grows quadratically in attention cost and linearly in latency, and performance degrades past `32k–128k` tokens even in frontier models. Compressing the context is the right answer, not enlarging it.

### Pivot out

"The shape is a context-window cliff, not a design failure. It tells us exactly where the next mile of engineering goes."

---

## B9 · Success Metric Validity

> _"Isn't exact end-state matching biased toward plans you anticipated?"_

### 30-second answer — `BRACE`

- **(R)** "The concern is whether the metric secretly rewards plans we authored."
- **(A)** "Exact matching is strictly harder than soft matching, and it is applied identically to every arm."
- **(C)** Anchors:
  1. Exact match against a set of valid end-states. Symmetric placements — e.g. two nodes with identical resource profiles — both count as success.
  2. Identical metric across arms — any anticipation bias would apply to `ReAct` and `LATS` just as much as to `AgentEdge`.
  3. Paired with continuous metrics — energy, API-call variance, response time — so the success rate is never the only signal.
- **(E)** "Open orchestration benchmarks from live production traces would strengthen this further. That is future work, not a concession."

### Anchor number

`6` scenarios × `60` runs; multiple valid end-states per scenario.

### Follow-up traps

- _"Why not use cost-to-goal as the metric?"_ → It was considered, but cost-to-goal collapses different trade-offs (QoS vs energy vs latency) into a scalar that requires a weighting the operator should own, not the researcher. Exact match is a strict floor; the continuous metrics handle the trade-offs.
- _"What if the agent hits the end-state accidentally?"_ → Runs are scenario-specific with distractor actions available. Random walks collapse to near-zero success — visible in `ReAct`'s `28.3%` compared to `AgentEdge`'s `78.3%`.

### Pivot out

"Exact match is strictly harder than soft match. The continuous metrics catch what the binary metric misses."

---

## B10 · State Staleness Between Plan and Execute

> _"What if infrastructure state changes while the agent is still planning?"_

### 30-second answer — `BRACE`

- **(R)** "The question is how the system handles the gap between observation and action."
- **(A)** "Staleness is handled at three layers: execution gate, three-tier state isolation, and `ActSimCrit` re-planning."
- **(C)** Anchors:
  1. Execution gate — the Infra Action agent re-queries live state before each committed call. Nothing goes out on stale observations.
  2. Three-tier state isolation — baseline, accepted, and simulated states are kept distinct, so the twin can never overwrite the live view.
  3. Failure routes to `Planning`, not local retry — when a call fails, `ActSimCrit` re-plans on a fresh observation, not on the old reasoning chain.
- **(E)** "Planner latency still matters. An ILP planner drops from `107 s` to `48 s` under the thesis setup, but `150 ms` is the production target. That gap is explicitly future work, not a solved claim."

### Anchor number

Three-tier state isolation; ILP planning `107 s → 48 s` in this setup; `~100x` cheaper retry in the twin vs physical.

### Follow-up traps

- _"What if the live state is wrong?"_ → Then the action fails at the execution gate and routes back to planning, not to production damage. The separation between planning and execution is explicitly a safety mechanism.
- _"You still can't prevent a race condition."_ → Correct. Distributed multi-agent coordination is one of the open directions on slide `50`. This thesis demonstrates the single-instance pattern; distributed conflict resolution is the next research step.

### Pivot out

"Staleness is contained, not eliminated. The next mile is faster planners and focused context."

---

## B11 · `AERO` vs Pathformer — The CPU/RAM Chart

> _"Why does `Pathformer` look lighter in the CPU/RAM chart?"_

### 30-second answer — `BRACE`

- **(R)** "The question is about a visual on the live-deployment slide where the `Pathformer` bars look smaller."
- **(A)** "Those bars are the node's total CPU/RAM utilization, not the predictor's own footprint. It's an artifact."
- **(C)** Anchors:
  1. `Pathformer` (`2.4 M` parameters) does not fit the far-edge envelope — the node was running without it. That produces a misleadingly low bar.
  2. `AERO` (`599` parameters, `0.38 ms` inference) actually executed on-node during the measurement window.
  3. The thesis fit criterion is parameter budget, not observed runtime stack CPU/RAM.
- **(E)** "Slide `16` (`V2`) removed those bars so the chart can't be misread this way."

### Anchor number

`2.4 M` Pathformer vs `599`-parameter AERO — `~4000x` fewer parameters, matched accuracy.

### Follow-up traps

- _"So the chart was misleading in V1."_ → Yes, and it was fixed. The underlying claim — parameter-budget dominance — was never in doubt, because parameter count is not measured on the node but counted from the architecture itself.
- _"Are you hiding a slower predictor behind the parameter count?"_ → No. Live inference for `AERO` is `0.38 ms`, which is inside the orchestration loop budget by more than two orders of magnitude.

### Pivot out

"The fit is judged on parameters, not on observed runtime bars. That is what makes `AERO` actually edge-deployable."

---

## B12 · Informer vs Pathformer vs `AERO`

> _"Why didn't you benchmark `AERO` directly against `Informer`?"_

### 30-second answer — `BRACE`

- **(R)** "The question is whether an obvious baseline was skipped."
- **(A)** "Three models, three roles. `Informer` is in the survey, not in the `AERO` benchmark — and that is by design."
- **(C)** Anchors:
  - `Informer` — attention-family survey anchor (`J4` Communications Magazine paper). Same footprint class as `Pathformer`, so comparing `AERO` to `Informer` would not add a distinct claim.
  - `Pathformer` — the heavy accuracy frontier at `2.4 M` parameters. Strongest baseline to beat on accuracy.
  - `AERO` — small-and-accurate quadrant. Matches `Pathformer` at `~4000x` fewer parameters.
- **(E)** "Matching the stronger heavy baseline is the harder claim. Beating `Informer` does not strengthen it further."

### Anchor number

`~4000x` parameter reduction vs `Pathformer` at matched accuracy.

### Follow-up traps

- _"Wouldn't `Informer` be smaller than Pathformer?"_ → Roughly same footprint class. If `AERO` matches `Pathformer`, the `AERO`-vs-`Informer` gap is dominated by the same `~10^3`-parameter gap.
- _"You could still have added `Informer` for completeness."_ → Fair. The rationale is scope: the chapter carries `Pathformer` / `SparseTSF` / `AERO` forward into orchestration simulation because they span the trade-off corners. Adding a fourth inside that loop would not have changed the orchestration result.

### Pivot out

"Three models, three roles. The stronger baseline was the right one to pin."

---

## B13 · `AERO` Beyond Workload Traces

> _"Can `AERO` be used for signals other than CPU/memory?"_

### 30-second answer — `BRACE`

- **(R)** "The question is whether `AERO`'s design is specific to container telemetry."
- **(A)** "`AERO` is signal-agnostic — any low-dimensional time-series with learnable periodicity is a candidate."
- **(C)** Anchors:
  1. Signal-agnostic by design: adaptive period detection operates on the autocorrelation of the input, independent of semantics.
  2. Plausible 6G candidates: PRB utilization, UPF throughput, handover rate, latency percentiles — all inherit daily/weekly cycles.
  3. Not a fit for event-driven or highly non-stationary regimes — that is where `OmniFORE`'s attention mechanism is the correct tool.
- **(E)** "I am not claiming that `AERO` has been validated on wireless-native traces. That is the natural extension through the `Nearby Computing` collaboration."

### Anchor number

`599` parameters, `0.38 ms` inference — budget independent of signal family.

### Follow-up traps

- _"What about non-periodic bursty traffic?"_ → That is the weak regime. After a regime shift, `AERO` needs roughly two new periods to re-stabilize. For bursty or abrupt-shift signals, `OmniFORE`'s attention generalizes better.
- _"Would you use it for radio KPIs in production today?"_ → As a candidate, yes, but with a wireless-native validation step before deploying. The thesis establishes the edge-feasibility property; per-signal validation is a deployment engineering step.

### Pivot out

"Where a 6G signal is recurrent, `AERO` is a candidate. Where it is not, `OmniFORE` takes over."

---

## B14 · `OmniFORE` Deployment Tier and Leakage

> _"Where does `OmniFORE` actually run, and is the zero-shot protocol clean?"_

### 30-second answer — `BRACE`

- **(R)** "Two questions fused: placement tier and leakage discipline."
- **(A)** "`OmniFORE` is tier-agnostic — placement is an operator decision. The research claim is generalization, not placement. The zero-shot protocol is clean by construction."
- **(C)** Anchors:
  1. Tier-agnostic: runs on far-edge (memory permitting), regional (where evaluated), or cloud.
  2. Identical protocol: train on Borg cells `A`–`F`, freeze weights, evaluate on held-out Alibaba pod. Cell boundaries prevent train/test leakage.
  3. Effect sizes: `ModernTCN` -`44%`, `AGCRN` -`295%`, `LSTNet` -`554%` MAE relative to `OmniFORE` under the same protocol.
- **(E)** "The gap is architectural. Attention learns portable pattern features. Graph-adaptive methods overfit the training super-cell structure."

### Anchor number

`-295%` AGCRN MAE vs `OmniFORE` on Borg → Alibaba zero-shot transfer.

### Follow-up traps

- _"The numbers are suspiciously large."_ → They are large because graph-adaptive models overfit training graph structure and cannot transfer that structure. That is exactly the kind of failure mode the generalization claim is designed to expose.
- _"Does `OmniFORE` replace `AERO`?"_ → No. `AERO` solves deployability within one service family; `OmniFORE` solves scalability across service families. They sit on different axes of the orchestration stack.

### Pivot out

"The gap is architectural, not a protocol favor. Attention transfers; graph-adaptive methods do not."

---

## B15 · 6G Scope

> _"Which 6G services does this really cover, and is this a 6G thesis or just a cloud thesis?"_

### 30-second answer — `BRACE`

- **(R)** "The question is whether the thesis earns the 6G label."
- **(A)** "Yes, at the orchestration layer — the layer above radio scheduling. The contribution is payload-agnostic service control for the edge-cloud continuum."
- **(C)** Anchors:
  1. Payload-agnostic: the orchestration contract does not depend on which 6G service is running.
  2. Network and app plane: relevant to O-RAN, UPF/SMF, slice, MEC on the network side; and XR, V2X, federated inference on the app side.
  3. `Nearby Computing S.L.` — production orchestration platform, anonymized live traces, scheduler interface. The industrial grounding is concrete.
- **(E)** "I do not claim a full wireless-native validation. What I claim is a validated orchestration layer that is 6G-compatible and sits above the radio-resource-management layer, not replacing it."

### Anchor number

`J4` Communications Magazine paper maps to `OmniFORE` on slide `46`; industrial collaboration with `Nearby Computing S.L.`.

### Follow-up traps

- _"You should have had real 6G radio traces."_ → Agreed that it would strengthen the wireless claim. It would not change the orchestration contribution, because the contribution is one abstraction level above radio scheduling. Wireless-native validation is the natural next milestone.
- _"This looks like a cloud-orchestration thesis dressed up for 6G."_ → The dissertation is explicit about operating above the radio layer. The reason it is framed for 6G is that the trends that make the problem acute — service density, edge placement, autonomous control — are 6G trends, not classic cloud trends. The machinery is reusable in 5G/B5G today, which is a strength, not a weakness.

### Pivot out

"Real-traffic grounding, not vendor lock-in. The thesis contributes the control layer that 6G orchestration needs — validated autonomy, deployable prediction, transferable forecasting."

---

## Global Landing Lines (Reuse Anywhere)

End any answer with one of these if you need a safe exit:

- `AERO` — "So the key contribution is not only forecasting accuracy, but edge-feasible forecasting."
- `OmniFORE` — "So the main value is reducing retraining burden across heterogeneous services."
- `AgentEdge` — "So the contribution is validated autonomy, not blind autonomy."
- Whole thesis — "The integrated contribution is deployable prediction, transferable forecasting, and validated orchestration."

## Fast Anchor Sheet (Memorize)

- `AERO` — `599` params · `99.98%` reduction vs `Pathformer` · `0.38 ms` · `13%` energy · `99%` fewer SLA violations.
- `OmniFORE` — `~30%` cross-dataset MAE improvement · `19.35%` zero-shot gain · `15x` faster than `AGCRN`.
- `AgentEdge` — `78.3%` success · `2.76x` over `ReAct` · `10x` API-call consistency · `300.8 W` peak saving · `1.47x` uplift from `ActSimCrit`.
- Scale — `6` scenarios · `60` runs/arm · `630` total runs.

One number per answer. Never two.
