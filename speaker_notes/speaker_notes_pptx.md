<!--
PPTX notes format:
- Start each block with `### Slide 01 · Title` or `### Backup B1 · Short label`.
- The exporter matches on the slide token only: `01`, `02`, ..., `B1`, `B2`, ...
- Put plain presenter text below the heading. Literal `- ` list markers are kept in the exported notes.
- Leave the body empty if a slide should have no speaker notes in the exported `.pptx`.

Timing plan (target: ~55 min, v1 rehearsal ran ~55 min):
  Framing   (01-08) =  5:40   |  AERO      (09-18) = 10:10
  OmniFORE  (19-30) =  9:50   |  AgentEdge (31-46) = 19:00
  Synthesis (47-52) =  6:00   |  Total           = 50:40 (≈ 4 min buffer)

Format of timing line per slide:
  `Time ~Xs · T+MM:SS` where T+ is the cumulative running time after this slide.
  Backup slides have no timing (used only on demand during Q&A).
-->

### Slide 01 · Title

Time ~30s · T+0:30

Good morning.

- Berend Jelmer Dirk Gort.
- Doctoral Program in Signal Theory and Telecommunications, UPC.
- Supervisor: Dr. Angelos Antonopoulos (Nearby Computing). Co-supervisor: Dra. Anna Umbert (UPC).
- Industrial partner: Nearby Computing: evaluated against real infrastructure.

### Slide 02 · Defense outline

Time ~20s · T+0:50

Fix the map before the evidence starts.

- Five parts: Framing → AERO → OmniFORE → AgentEdge → Synthesis.
- Color code: blue = AERO, orange = OmniFORE, pink = AgentEdge.

### Slide 03 · Manual reality today

Time ~60s · T+1:50

Four layers, four open problems, one stack that does not close the loop.

- L1 Operator: intent in, exceptions only (Problem 4).
- L2 Decision: no intelligent path from NL intent to action (Problem 3).
- L3 Prediction · far edge: no accurate per-node forecasts (Problem 1).
- L3 Prediction · regional cluster: new model per service (Problem 2).
- L4 Infra: heterogeneous far-edge nodes, regional clusters, cloud.

### Slide 04 · Zero-touch: operator sets intent, not actions

Time ~50s · T+2:40

Predict, decide, act, observe: with humans on exceptions only.

- Left: the control loop.
- Right: reactive control lags both up (SLA violations) and down (wasted energy).
- Predictive control closes both gaps: two of three contributions land here.

### Slide 05 · Forecasting must run where the service runs

Time ~40s · T+3:20

The deployability gap.

- Microcontroller-class budget: ~256 KB SRAM; fp32 ⇒ ~65K params upper bound, much less in practice (activations, gradients, buffers) [Lin et al., NeurIPS '22].
- SOTA baseline: 2.4M params ≈ 10 MB fp32 → ~40× over budget: accurate, undeployable.
- Lightweight alts ~50K params ≈ 200 KB fp32 → fills the budget: deployable, but accuracy collapses under drift.
- RQ1: can workload prediction be practical and accurate at edge scale?
- Target: <1,000 params ≈ 4 KB fp32 — fits with headroom; the point is not minimum size, but fitting the device with room left for the rest of the system.

### Slide 06 · One model for many services

Time ~40s · T+4:00

The generalization barrier.

- Default today: one model per service → O(N) cost.
- 6G scale: 300+ services per operator.
- Real barrier = retraining burden, not inference cost.
- RQ2: one framework across heterogeneous services, no per-service retraining?

### Slide 07 · From natural-language intent to intelligent orchestration action

Time ~40s · T+4:40

The decision layer is still manual.

- Operator: *"reduce energy while keeping SLA"*: does not map to a heuristic or fixed objective.
- A human still reads dashboards, picks services, and runs drain/scale/migrate/power-off.
- Zero-touch here needs two abilities: understand intent, and act safely on it.

### Slide 08 · One orchestration stack that predicts, generalizes, and acts on intent

Time ~60s · T+5:40: end of Framing (target 5:40) ✓

Four problems → 3 RQs → 3 objectives → 3 contributions.

- RQ1 → O1 → AERO: deployable edge prediction.
- RQ2 → O2 → OmniFORE: cross-service generalization.
- RQ3 → O3+O4 → AgentEdge: intelligent action from intent.
- Each contribution removes one blocker; together they close the zero-touch loop.

### Slide 09 · AERO

Time ~20s · T+6:00

Contribution 1 · edge-deployable workload prediction.

- Claim: adaptive periodicity lets a tiny model produce operationally useful forecasts at the edge.
- Quantified goal: <1,000 parameters.

### Slide 10 · System Model & Motivation

Time ~60s · T+7:00

Timing, not mechanism.

- Each edge node is microcontroller-class; whole control loop stays on-node.
- Loop: observability → predictor → local scheduler → infrastructure → observability.
- Deployment can be a single node, a node with an MCU nearby, or several micronodes.
- Toy: WS-A queue spike, WS-B still free; dispatch due in ~50 ms.
- Local forecast: reroute in time. Off-node round-trip: reply arrives after deadline.
- Prediction is only useful if it arrives before the slot closes.

### Slide 11 · State-of-the-art: accurate or deployable, not both

Time ~50s · T+7:50

Three regimes, one empty quadrant.

- Red · heavy: Pathformer 2.4M, WGAN 2.9M, ModernTCN 247K, FourierGNN 228K.
- Amber · lightweight: SparseTSF: fits, accuracy gives way.
- Green target (top-left): small *and* accurate.
- AERO: 599 parameters, sitting in the empty quadrant.

### Slide 12 · Design: how AERO works in three steps

Time ~70s · T+9:00

Make the signal easier before a tiny model forecasts it.

- Step 1: find the rhythm: re-detect periodicity each window.
- Step 2: align first: line up repeated cycles.
- Step 3: reuse cached layers: same pattern, same block.

### Slide 13 · Scenario 1: Workload Prediction

Time ~50s · T+9:50

Efficiency benchmark setup.

- Data: Alibaba 2022 microservices trace, pod MS_11349 · 18,720 samples · 13 days · CPU + memory.
- Models: 5 baselines + AERO.
- Rig: A100 40 GB · 30 CPU · 200 GiB RAM · Python/PyTorch.
- Tuning: Bayesian optimization · 20 random + 30 refinement trials per model.
- Outputs: MAE, RMSE, latency, convergence, parameters, memory.

### Slide 14 · Result 1: small enough and accurate enough

Time ~80s · T+11:10

Three columns, one conclusion.

- Params: AERO 599 · heavy baselines 228K–2.9M · SparseTSF 35 (too weak).
- Latency: AERO 0.38 ms · Pathformer 0.52 ms · both inside 50 ms budget.
- MAE: AERO 2.9e-4: on par with ModernTCN, close to Pathformer.
- Only AERO is simultaneously deployable and accurate.

### Slide 15 · Scenario 2: Orchestration outcomes

Time ~50s · T+12:00

From forecast quality to control impact.

- Simulator: COSCO on AzureFog · 50 hosts (60% edge, 40% cloud) · 3 ms edge / 76 ms cloud · 5 Gb.
- Run: 2,000 cycles at 300 ms · 50 containers · 4 arrivals/step.
- Input: BitBrains Random · 500 VMs · 8,631 samples · 7 signals.
- Arms: AERO, Pathformer, SparseTSF, reactive.
- Same scheduler, same stream, same objective: only forecast changes.

### Slide 16 · Result 2: controlled simulation results

Time ~90s · T+13:30

Four operational metrics.

- Energy (J): reactive 1293 · SparseTSF 1140 · AERO/Pathformer 1123.
- Response time (s): reactive 10.02 · SparseTSF 6.5 · AERO 3.29 · Pathformer 2.45.
- SLA violations (%): reactive 22.21 · SparseTSF 4.60 · AERO 0.21 · Pathformer 0.10.
- Migrations: 2,026 / 5,309 / 7,747 / 8,480: predictive acts before overloads.
- Honest read: only AERO fits edge hardware while staying close to Pathformer (~4,000× larger).

### Slide 17 · Scenario 3: Live deployment

Time ~50s · T+14:20

Field test.

- Train: Google Cluster trace · T = 8,930 · 4 features · 5-min resolution.
- Deploy: AERO + SparseTSF as microservices on i9-9900K · 46 GB · RTX 2060 · Docker Compose.
- Held-out split: looks similar. Live unseen workload: drift exposes the difference.
- Metrics: normalized MAE, RMSE, mean inference time · 50 ms real-time threshold.

### Slide 18 · Result 3: live deployment results under drift

Time ~90s · T+15:50: end of AERO (target 15:50) ✓

Latency is not the differentiator; drift robustness is.

- MAE: AERO 0.051 · SparseTSF 0.411 (~8× worse).
- RMSE: AERO 0.079 · SparseTSF 0.430.
- Inference: AERO 2.65 ms · SparseTSF 1.12 ms · both well inside 50 ms.
- Operator impact: ~15% lower response time · ~12% lower energy.

### Slide 19 · OmniFORE

Time ~20s · T+16:10

Contribution 2 · one forecasting framework, all services.

- Claim (weaker): models can predict any trace.
- Goal (operational): one model to process all workload traces.
- Next: zero-shot on unseen services, up to frozen-weight cross-dataset transfer.

### Slide 20 · Problem: one model, many services

Time ~45s · T+16:55

Operator-terms statement.

- One model, trained once, forecasts any service in the catalogue: including unseen.
- Visual: bursty vs steady families must both be covered.
- Formal: one shared weight set · no per-service tuning · minimize average error across seen + unseen.

### Slide 21 · System Model & Motivation

Time ~40s · T+17:35

One prediction layer serves many services at a site.

- Returns per-service forecasts to the same downstream stack.
- Today: each site carries its own model copy: retraining, memory, monitoring repeat everywhere.
- Target: one shared model, many sites, many services: no duplicated ML workload.

### Slide 22 · State-of-the-art: no prior method lives in the top-right

Time ~50s · T+18:25

Two red regimes, one empty target.

- Red 1 · per-service retraining: ModernTCN, AGCRN, LSTNet.
- Red 2 · generic but heavy: foundation models: too heavy, too generic.
- Top-right (one model + unseen-service accuracy): empty.
- OmniFORE is designed to occupy it.

### Slide 23 · Design: how OmniFORE works in three phases

Time ~50s · T+19:15

Generalization from the whole pipeline.

- Phase 1 (S1-S4): design the training set: encode, cluster, sample balanced.
- Phase 2 (S5-S6): rescale + shared attention across heterogeneous services.
- Phase 3 (S7): tune hyperparameters on held-out services: reward transfer, not memorization.

### Slide 24 · Building the training set

Time ~50s · T+20:05

Representativeness engineered before training.

- S1: fingerprint each trace into a shape descriptor.
- S2: cluster fingerprints into bursty / steady / periodic.
- S3: tag each trace with its group label.
- S4: sample proportionally: balanced mix.

### Slide 25 · Training the model

Time ~70s · T+21:15

Shared model, portable patterns.

- S5 equal scale: rescale each trace so large services do not dominate.
- S6 efficient attention: full window, strongest matches, sparse links: long windows stay cheap.
- The model matches patterns, not service identity → transfers to unseen services.

### Slide 26 · Tuning for transfer

Time ~50s · T+22:05

Reward new-service performance, not train-set fit.

- Bayesian optimisation over the objective curve; star marks the winner.
- Training set is used to fit; held-out traces T1/T2/T3 score transfer.
- Winner is the setting that works on *new* services.

### Slide 27 · Scenario 1: Clustering Impact

Time ~40s · T+22:45

Isolate the clustering step.

- Left: clustered sample: balanced mix.
- Right: random baseline: 5 draws averaged.
- Everything else held fixed: same model, tuning, test services.
- If clustered wins, the gain is from data selection itself.

### Slide 28 · Result 1: clustering-based training helps

Time ~60s · T+23:45

Clean experimental control; gain comes from data selection.

- MAE −20.66% · RMSE −24.63% · SMAPE −32.71%.
- Clustering covers bursty/steady/periodic; random over-samples common shapes.
- Next: does this representativeness survive full cross-dataset transfer?

### Slide 29 · Scenario 2: Cross-dataset transfer

Time ~45s · T+24:30

The hardest test a forecaster can run.

- Train on Google Borg (cells A–F) · freeze weights · evaluate on Alibaba Cloud 2022 (pod MS_11349).
- Different provider, different workload mix, no fine-tuning.
- On-slide line: *this is where benchmark wins usually fall apart*.

### Slide 30 · Result 2: generalises without retraining

Time ~70s · T+25:40: end of OmniFORE (target 25:40) ✓

Transfer result on Alibaba.

- MAE: OmniFORE 0.00727 · ModernTCN 0.01045 · AGCRN 0.02870 · LSTNet 0.04751.
- Baselines vs OmniFORE: ModernTCN +44% · AGCRN +295% · LSTNet +554%.
- Portable workload patterns → new service forecasts with existing model.
- RQ2 answered. Last missing block = AgentEdge.

### Slide 31 · AgentEdge

Time ~20s · T+26:00

Contribution 3 · intent → validated autonomous action.

- Claim: multi-agent LLM + validation beats single-agent and tree-search baselines · success >75%.
- Anchors: multi-agent · tool-use · multi-step reasoning · digital-twin validation.

### Slide 32 · Problem & Motivation

Time ~60s · T+27:00

The decision layer is the missing step.

- *"reduce energy while keeping SLA"*: Kubernetes cannot act on that sentence.
- Someone chooses: which services, which moves, where spare capacity, what is safe, what to monitor.
- Existing optimizers start only after the formalization.
- Without this layer, the loop still depends on a human in the middle.

### Slide 33 · System Model

Time ~60s · T+28:00

Pin the interfaces before showing AgentEdge.

- Four layers: operator · decision · service-orchestration · infra.
- Prediction sits inside service-orchestration, not as its own layer.
- Decision does not query prediction directly: service-orchestration stores predictions, decision reads them + live state.
- Decision logic reasons over sets of actions, not single raw actions.

### Slide 34 · Design: what is an agent?

Time ~60s · T+29:00

Precise definition before comparisons.

- PARES: all five required:
  - Perceive live bounded state.
  - Act through typed tools.
  - Reason over goals and constraints.
  - Evaluate plans before production.
  - Sustain across multi-step interactions.
- PARES synthesised in Chapter 2 from six agentic-framework papers.

### Slide 35 · State-of-the-art · 6G still lacks a full agent

Time ~70s · T+30:10

Zero 6G rows are full agents.

- Matrix: deployment · P · A · R · E · S · multi-agent coordination.
- Top-right card: why Chapter 5 baselines come from ML, not 6G.
- 6G papers: valuable related work, but miss PARES and the Intent-Observe-Plan-Act model.
- ReAct + LATS are PARES-complete but task-misaligned: legitimate baselines when retargeted.
- Only AgentEdge is full-row green.

### Slide 36 · Graph of graphs + microservice deployment

Time ~90s · T+31:40

Graph-of-graphs architecture, thin pods, shared backends.

- Top-level orchestrator routes 4 subgraphs: Intent → Observability → Planning → Infra Action.
- Each specialist is itself a subgraph.
- Deployment: thin pods share one LLM backend (prompt/reply) and one MCP server (typed tools).
- MCP → container orchestrator → far/near/cloud tiers → updated state back to observe.
- Every specialist satisfies PARES.
- Benefits: lightweight · flexible (swap LLM) · typed (shared tool schema).

### Slide 37 · AgentEdge splits orchestration across four specialists

Time ~90s · T+33:10

Each specialist is the minimal fix for one failure mode.

- 01 Intent: ambiguous NL → typed goal (`{"goal":"save_power","sla":"preserve"}`).
- 02 Observability: raw telemetry → structured alerts (*node_3 hot*, *node_5 headroom*).
- 03 Planning · ActSimCrit: Plan → Sim → Crit; reject-retry until accepted.
- 04 Infra Action: validated plan → `POST /migrate` / `PATCH /power`, with retries on failure.
- Drop one → predictable failure: ambiguous intent · state blindness · unvalidated plans · unreliable execution.

### Slide 38 · Planning Agent · ActSimCrit loop

Time ~120s · T+35:10  (core slide: spend the time)

5 LLM calls + 1 simulation per iteration.

- P1 Plan: end-goal + constraints.
- P2 State: bottlenecks/violations between current and goal.
- P3 Actions: next batch of tool calls, skipping rejected batches.
- P4 Sim + Critic: twin simulation + independent critic LLM (no memory of prior attempts).
- P5 Intent met? yes → emit validated plan · no → reject/retry to P3.
- DEADLOCK chip on cap hit → propose alternative intent.
- Mechanisms: action batching · three-tier state (baseline/accepted/simulated) · rejection-feedback · deadlock detection.
- Output is a validated plan; the infra agent executes, not diagnoses.

### Slide 39 · Simulator testbed + six scenarios

Time ~90s · T+36:40

Evaluation harness + the scenarios.

- Tier 3 cloud: 0-1 node · 64 CPU · 256 GB · 180-450 W.
- Tier 2 near edge: 0-10 nodes · 16 CPU · 32 GB · 40-120 W · 25-60 ms link.
- Tier 1 far edge: 6-12 nodes · 4 CPU · 8 GB · 10-35 W · 10-25 ms link.
- Simulator parameters table (shared across tiers):
  - Services: web 0.25c · db 0.5c · api 0.25c.
  - Timing: deploy 15-45 s · migrate 8-30 s · scale 5-54 s.
  - Stochastic: timing ±15-25% · failure 0.1-2% · latency ±1-2 ms.
  - Power: **low-power -60%** (pink) · sampled 5 s · util 60/30/10.
- Same simulator = digital twin inside ActSimCrit.
- Group A · constraint resolution (two nodes, italic prompt under each card):
  - S1 Full Node — *"deploy a new service on edge-0"* → free space first.
  - S2 Sleep Conflict — *"sleep edge-1 + scale APIService to 1.4c"* → move, then sleep.
  - S3 Won't Fit — *"sleep edge-1 + scale APIService to 2.4c"* → redistribute load (oversized svc, red ✗ blocks consolidation arrow).
- Group B · energy scalability (same prompt on all three: *"reduce energy whilst keeping SLA"*):
  - S4 small (8 nodes, 6 svc, 2 idle).
  - S5 medium (18, 15, 3).
  - S6 large (35, 30, 6).
- Success = exact match to pre-defined valid end-states. No partial credit.
- Fairness: same catalogue, same LLM: only architecture varies.

### Slide 40 · Scenario 1: multi-agent vs single-agent

Time ~70s · T+37:50

Architecture-vs-architecture, same LLM, same tools, same tasks.

- AgentEdge: graph of graphs · 4 specialists sequentially.
- ReAct: one-LLM think-act loop · no validation.
- LATS: one-LLM + MCTS · strongest single-agent baseline.
- Protocol: pre-defined valid end-states · exact-match success.
- Toy: edge-0/edge-1 at 50/50 · task = shut one server off · valid ends = 100/0 or 0/100 · 50/50 or 75/25 = fail.
- 60 runs per arm: any gap is architectural.

### Slide 41 · Result 1: multi-agent beats every baseline

Time ~60s · T+38:50

Architectural lift, not model capability.

- AgentEdge 78.3% · LATS 65.0% · ReAct 28.3%.
- 1.20× LATS · 2.76× ReAct.
- Same LLM, tasks, simulator: gap comes from architecture itself.
- Next: twin-on vs twin-off.

### Slide 42 · Scenario 2: twin ablation

Time ~90s · T+40:20

Isolate the twin as *pre-execution validation*.

- Twin ON: Plan → Sim (twin) → Crit (independent LLM) → Exec on real infra. Retries are virtual, capped.
- Twin OFF: Plan → ∅ → Crit → Exec straight on production. Retries are physical, unbounded.
- PLAN/CRIT identical on both sides; only SIM is removed.
- Report both success rate and API-call count: failure-shifting cannot hide.

### Slide 43 · Result 2: sandbox validation reduces costly trial-and-error

Time ~60s · T+41:20

Twin lifts success and collapses variance.

- Success: 78.3% (on) vs 53.3% (off) · 1.47×.
- API-call stability: σ 1.1 (on) vs σ 109.4 (off) · ~10× variance.
- Without simulation: unproductive retry loops that are operationally unsafe: every retry touches prod.
- Twin is structural, not cosmetic.

### Slide 44 · Scenario 3: energy scalability

Time ~70s · T+42:30

Does AgentEdge keep saving energy as infra grows? Slide is visual on purpose.

- Start pattern at every scale: 1 service per node (~25% load) + a few nodes fully idle. All still draw power.
- Light box + red band = node at ~25% · dashed empty box = fully idle.
- Scale A · Small: 8 nodes · 6 svc · 2 idle.
- Scale B · Medium: 18 · 15 · 3.
- Scale C · Large: 35 · 30 · 5.
- Obvious fix: consolidate onto fewer nodes · power the rest down.
- Question: does the agent still do this cleanly at every scale?

### Slide 45 · Result 3: power drops across every scale

Time ~90s · T+44:00

Three panels, one story. Y = rack watts · X = API calls.

- 8 nodes: ~460 → ~370 W · ΔW = 89 W.
- 18 nodes: ~710 → ~410 W · ΔW = 300.8 W (the peak).
- 35 nodes: ~1,250 → ~1,060 W · ΔW = 185.2 W.
- Why 18 > 35? Context-window artefact at 35: full state overflows the prompt.
- Summarisation / sharded context would keep the curve descending.
- All 30 runs succeeded at every scale.
- Validated autonomy remains energy-relevant at production scale; saturation explained, not hidden.

### Slide 46 · Slide 03 reprise + publication mapping

Time ~40s · T+44:40: end of AgentEdge (target 44:40) ✓

Callback to the framing stack, now labelled by contribution.

- L1+L2 → AgentEdge · L3 → AERO + OmniFORE · L4 → related book chapter.
- AgentEdge → [J1], [C1].
- AERO → [J4], [C3].
- OmniFORE → [J3], [J5], [C2].
- [B1] = infrastructure-level related output.
- Full bibliographic list on backup B7.

### Slide 47 · Future Work · Agentic Frontier

Time ~40s · T+45:20

Prediction is solved; the agentic layer is the frontier.

- FW1 · Reliability & Trust: no shared score · rejected paths invisible.
- FW2 · Real-time Infra: tens of seconds per plan · accuracy cliff beyond ~30 tools.
- FW3 · Distributed Ecosystems: parallel agents collide · tool-calls change shape per provider.
- 3 slides, 6 blockers, each paired with a direction.

### Slide 48 · FW1 · Reliability & Trust

Time ~70s · T+46:30

Two blockers, two cards.

- Evaluation: multi-solution tasks + LLM non-determinism → no shared score.
  - Direction: orchestration-trace datasets · equivalence-class scoring · confidence intervals.
- Trust at decision time: only the chosen branch is shown; nothing formally checks output.
  - Direction: reasoning-trace standards · constraint-clamping with NL feedback · critic-of-critics on ActSimCrit.
- Trust is won by showing rejected paths.

### Slide 49 · FW2 · Real-time Infrastructure

Time ~70s · T+47:40

Two empirically grounded blockers.

- Inference efficiency: observe → plan → revise → critique → actuate: seconds per call.
  - SLA line crosses the critic step; token cost compounds at scale.
  - Direction: call reduction via multi-step prompting · distilled orchestration-specific models (AERO lesson applied to the planner).
- Tool discovery: accuracy holds up to ~30 tools, cliffs beyond. AgentEdge (3 MCPs, ~40 tools) sits on the cliff.
  - Dissertation finding: removing an MCP sometimes *improved* success.
  - Direction: semantic tool retrieval · hierarchical catalogs · autonomous read-only discovery.

### Slide 50 · FW3 · Distributed Ecosystems

Time ~70s · T+48:50

From one instance to fleets.

- Multi-agent coordination: parallel agents → contradicting actions on shared infra (A consolidates node-07 · B powers it down).
  - Direction: intent-level consensus · lock-lease on intended actions · share plans, not raw state.
- Model-agnostic design: swap LLM → tool-calls change shape (camelCase JSON vs XML-ish): "glue code" tax.
  - Direction: canonical intent schema for tool-calls (OpenAPI-equivalent for agents) · model-agnostic evaluation.
- Pick an LLM for cost, latency, privacy: not compatibility.

### Slide 51 · Three contributions, one systems thesis

Time ~90s · T+50:20

3 claims · 9 anchor numbers.

- AERO: 599 params · 8× lower live MAE vs SOTA small model · 0.21% SLA vs 22% reactive.
- OmniFORE: −30.4% MAE vs ModernTCN · +20.7% gain from clustering · zero-shot Google → Alibaba.
- AgentEdge: 1.47× twin-on vs twin-off · 10× lower API variance · 300.8 W reclaimed @ 18 nodes.
- Edge-cloud orchestration moves from reactive supervision to a proactive, validated control stack.

### Slide 52 · Questions

Time ~20s · T+50:40: end of deck · ~4 min buffer to 55 min target

Thank you.

- *"The system is zero-touch. The Q&A should definitely not be."*
- Deck guide on the right · supervisors and tribunal on the left.

### Backup B1 · AgentEdge S35 result

(Q&A only · not timed into the 55-min plan)

Context bloat, not architectural contradiction.

- 9.5% at S35 vs 55.5% at S18 · same architecture · same base model.
- Defence 1: larger-context + better-reasoning models will relax this bottleneck.
- Defence 2: current state loading is naive: compressed / semantic / retrieval-augmented state reduces tokens, PARES unchanged.

### Backup B2 · AgentEdge state staleness

(Q&A only)

ActSimCrit re-checks live state at the execution gate.

- Execution agent queries infrastructure state immediately before commit: stale plans caught at the last safe boundary.
- Faster planning shortens drift window (e.g. classical optimizer swap: 107 s → 48 s).
- Smaller, more relevant context also reduces staleness risk.

### Backup B3 · Adapted baselines

(Q&A only)

ReAct and LATS were adapted to orchestration, not taken off the shelf.

- Same orchestration harness · same tool schemas · same base LLM · same metric collection as AgentEdge.
- Heuristics / RL / MILP need a formal objective: NL intent is the input here.
- Fair baseline = another LLM-based decision mechanism on the same tool surface.

### Backup B4 · Nearby Computing data scope

(Q&A only)

What Nearby Computing contributed + reproducibility.

- Production orchestration platform · live workload traces · scheduler integration.
- Anonymized service identities · resource/load traces only exposed.
- Protocol reproducible on any compatible orchestration stack.
- Value: realistic traffic, not synthetic replay alone.

### Backup B5 · Utilization citations

(Q&A only)

Headroom claims from the framing section.

- <40% utilization anchored in Google Borg, Azure, EC2 production studies.
- Edge-specific twist: 1-2 orders of magnitude less compute than cloud: reactive scheduling has much less room once bursts arrive.

### Backup B6 · PARES full definition

(Q&A only)

Formal capability contract.

- Perception: bounds context; prompt cannot grow without limit.
- Action: typed tool surface at the orchestration boundary.
- Reasoning: scoped decision process inside each specialist.
- Evaluation: explicit pre-execution judgment (critique + validation in AgentEdge).
- Sustained: stability over noisy, long-running production conditions.
- This is why some prior systems are not considered true agents.

### Backup B7 · Full publications

(Q&A only)

Full bibliographic record, grouped by contribution color.

- AERO · OmniFORE · AgentEdge · book chapter (kept separate).
- State totals · point to the color grouping · go venue-by-venue only if asked.

### Backup B8 · Execution agent

(Q&A only)

Typed executor, not reasoning-heavy.

- Input: approved action sequence + current infra state.
- Action surface: Kubernetes calls · orchestrator hooks · rollback primitives.
- Evaluation: post-execution state diff: did infra reach the intended state?
- Feedback loop: on failure, rollback where possible, record trace, return to Planning: closes ActSimCrit without re-running intent parsing.

### Backup B9 · OmniFORE deployment granularity

(Q&A only)

OmniFORE is layer-agnostic by design.

- Research problem = generalization, not a specific tier.
- Placement = operator decision, not thesis constraint.
- Far-edge: possible at stronger aggregation nodes.
- Regional: most natural: evaluation uses this.
- Cloud: works for longer horizons.

### Backup B10 · Why 78.3%, not 100%?

(Q&A only)

The twin is a gate, not an oracle.

- Three residual failure modes:
  - F1 Twin-live mismatch: approximations miss extreme contention.
  - F2 Critic recall: critic occasionally rubber-stamps infeasible plans: biggest contributor to the residual 21.7%.
  - F3 Budget cut-off: refinement budget exhausted before feasible plan found · safe fail over silent accept.
- Framing: 78.3% is the first *validated* success metric here: prior baselines can't be measured consistently because they actuate invalid plans.

### Backup B11 · 6G service mix

(Q&A only)

Orchestration contract is payload-agnostic.

- Network plane: O-RAN control · UPF/SMF control · slice management · MEC sidecars.
- Application plane: XR streaming · V2X loops · federated inference · industrial control · health telemetry.
- Claim: forecast, generalize, act safely regardless of service family.

### Backup B12 · Informer vs Pathformer vs AERO

(Q&A only)

Roles, not rankings.

- Informer-family: magazine-survey context · not the core AERO baseline.
- Pathformer: main AERO comparison baseline: current small-ish accurate frontier, still overshoots far-edge budgets.
- AERO's claim: match operational forecasting quality while staying tiny enough to deploy at the far edge.

### Backup B13 · AERO beyond workload traces

(Q&A only)

Reusable for any univariate time series with learnable periodicity.

- Contract: observe · detect periodic structure · forecast: independent of signal being workload.
- 6G examples: PRB utilization · MCS distributions · active connections · UPF throughput · session setup rates · service request rates · latency percentiles · byte rates · handover rates.
- Caveat: if the signal isn't periodic enough, OmniFORE is the more natural candidate.
