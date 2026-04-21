Defense PowerPoint Speaker Notes

PowerPoint-ready notes.
Each Notes block uses short speakable cue bullets.

Format per slide:
- Slide title and timing
- Say: opener
- Notes: short glance-readable beats
- Next: transition cue

Total runtime target: ~49:30 + Q&A.

------------------------------------------------------------------------

Slide 01 - Title
Time: 00:00 (0:30)

Say:
Today I defend AI-Driven Zero-Touch Orchestration of Edge-Cloud Services.

Notes:
- UPC doctoral program in Signal Theory and Telecommunications.
- Thesis defense on AI-Driven Zero-Touch Orchestration of Edge-Cloud Services.
- Supervised by Angelos Antonopoulos and Anna Umbert.
- Developed with Nearby Computing on real infrastructure.

Next:
Let me outline the defense.

------------------------------------------------------------------------

Slide 02 - Outline
Time: 00:30 (0:30)

Say:
The defense follows the same logic as the thesis - five parts.

Notes:
- Five-part flow: framing, AERO, OmniFORE, AgentEdge, synthesis.
- Same logic as the thesis.
- Colors track the three contributions throughout.
- Formal research-question map comes on slide 8.

Next:
Before the chapters, the operational setting.

------------------------------------------------------------------------

Slide 03 - Manual reality today
Time: 01:00 (0:45)

Say:
Orchestration today is a layered control problem - and the operator holds it together by hand.

Notes:
- Four-layer operator stack across far edge, regional clusters, and cloud.
- L1: operator sets intent, then translates it manually.
- L2: no intelligent bridge from intent to action.
- L3: no far-edge forecast; regional layer needs per-service retraining.
- L4: heterogeneous infrastructure is the given reality.
- Four layers, four open problems, one operator holding it together.

Next:
What the loop should actually look like.

------------------------------------------------------------------------

Slide 04 - Zero-touch: operator sets intent, not actions
Time: 01:45 (0:55)

Say:
Zero-touch means the operator sets intent; the loop does the rest - and prediction is the load-bearing stage.

Notes:
- Loop stages: predict, decide, act, observe.
- Operator sets goals, SLAs, constraints; reviews exceptions only.
- Chart: black = demand, red stair = reactive capacity, dashed cyan = predictive.
- Red region = SLA violations; reactive is late to scale up.
- Amber region = wasted energy; reactive is late to scale down.
- Predictive capacity tracks demand; closes BOTH gaps.
- Prediction is why this loop works; two contributions land here.

Next:
Three sub-problems - toy examples only, no solution names yet.

------------------------------------------------------------------------

Slide 05 - Forecasting must run where the service runs
Time: 02:30 (0:40)

Say:
Today's forecasters are either accurate or deployable - never both.

Notes:
- Heavy models are accurate but not deployable.
- Lightweight models fit, but collapse under drift.
- Small-and-adaptive quadrant is empty.
- RQ1: practical and accurate prediction at edge scale.
- Target: under 1,000 parameters with competitive accuracy.

Next:
Even if RQ1 is solved, a second problem remains.

------------------------------------------------------------------------

Slide 06 - One model for many services
Time: 03:10 (0:40)

Say:
One predictor per service does not scale; the bottleneck is operator time.

Notes:
- Per-service forecasting does not scale.
- O(N) retraining, monitoring, and tuning.
- 300+ microservices at 6G scale.
- New service or new drift means a new model.
- RQ2: one framework across heterogeneous services.
- Bottleneck is maintenance burden, not inference cost.

Next:
Even with prediction solved, the act step is still open.

------------------------------------------------------------------------

Slide 07 - From NL intent to intelligent orchestration action
Time: 03:50 (0:45)

Say:
The bridge from intent to action is a human today. That's the problem.

Notes:
- Operator says: "reduce energy while keeping SLA."
- Today a human translates that into drain, scale, migrate, power-off.
- Dashboards, guesswork, and command-level intervention.
- Natural language is a formal input, not a convenience.
- Rules out heuristics, RL, and MILP.
- RQ3 + Problem 4: intent into validated orchestration action.

Next:
Three RQs, three objectives, three contributions.

------------------------------------------------------------------------

Slide 08 - Dissertation objective
Time: 04:35 (0:45)

Say:
One stack that predicts, generalizes, and acts on intent.

Notes:
- RQ1 -> O1 -> AERO.
- RQ2 -> O2 -> OmniFORE.
- RQ3 -> O3 + O4 -> AgentEdge.
- Each contribution removes one blocker.
- Together they close the zero-touch loop.
- C1 -> C2 -> C3 -> loop.

Next:
I start with AERO.

------------------------------------------------------------------------

Slide 09 - AERO banner
Time: 05:20 (0:30)

Say:
Contribution 1 - AERO - Edge-Deployable Workload Prediction.

Notes:
- AERO: edge-deployable workload prediction.
- Adaptive periodicity keeps the model tiny.
- Target: under 1,000 parameters.
- Roughly four orders smaller than today's forecasters.

Next:
Generic system model first.

------------------------------------------------------------------------

Slide 10 - The edge decision loop - generic system model
Time: 05:50 (0:55)

Say:
Any forecaster has to fit this loop; AERO just fits it best.

Notes:
- Generic loop: Observability, ML model, Scheduler, back to Observability.
- ML box is a dashed placeholder - method-agnostic.
- Contract: lookback kappa in, horizon lambda out.
- Hard budget: fit edge RAM, return before next decision cycle.
- On slide 11 the dashed box is slotted with AERO.

Next:
Capability, not constraint.

------------------------------------------------------------------------

Slide 11 - Where AERO runs - capability, not constraint
Time: 06:45 (0:55)

Say:
AERO has the capability to run at every tier; where it lives is an operational choice.

Notes:
- Same loop, AERO slotted as the ML model.
- Capability: far-edge node, regional scheduler, or container runtime sidecar.
- 599 parameters, under 50 ms inference, kappa 96, lambda 96.
- Traffic-light motivator: far-edge cannot pay a cloud round-trip per cycle.
- Big transformers, even TinyTST, overflow the 50 ms budget.

Next:
State of the art.

------------------------------------------------------------------------

Slide 12 - Accurate or deployable, not both
Time: 07:40 (0:50)

Say:
The scatter makes the gap obvious - target quadrant is empty.

Notes:
- Two camps: accurate and heavy, or light and weak.
- Pathformer, WGAN, ModernTCN, FourierGNN: accurate but too large.
- SparseTSF: deployable but fragile under drift.
- Small-and-accurate quadrant is empty.
- AERO enters at 599 parameters.

Next:
Why adaptive periodicity is the right key.

------------------------------------------------------------------------

Slide 13 - Edge efficiency from signal structure
Time: 08:30 (0:50)

Say:
Edge efficiency comes from signal structure, not from compression.

Notes:
- Edge efficiency from signal structure, not compression.
- Small head on period-aligned features.
- Online periodicity re-estimation under drift.
- No attention, no KV cache.
- 0.38 ms on mobile CPU.

Next:
Three-step mechanism.

------------------------------------------------------------------------

Slide 14 - Adaptive periodicity in 3 steps
Time: 09:20 (0:55)

Say:
Detection -> adaptive forecasting -> layer caching.

Notes:
- Three steps: detect, forecast, cache.
- Online autocorrelation finds tau.
- Forecast reshaped around tau with a lightweight head.
- Cache reuses layers for recurring periods.
- 24h, 12h, 6h examples.
- No attention, no per-service fine-tuning.

Next:
Two questions: efficient? control-useful?

------------------------------------------------------------------------

Slide 15 - Efficiency benchmark scenario
Time: 10:15 (0:45)

Say:
Deployability first, accuracy second.

Notes:
- First experiment: deployability before raw accuracy.
- Alibaba cluster trace, five baselines, matched hardware.
- Parameter count vs sub-1,000 target.
- Latency vs sub-millisecond target.
- MAE, RMSE, and multi-periodicity still matter.

Next:
Result.

------------------------------------------------------------------------

Slide 16 - Efficiency result
Time: 11:00 (1:00)

Say:
Smallest deployable model, still adapts, still accurate.

Notes:
- AERO: 599 parameters.
- Heavy baselines: 228K up to 2.9M.
- 0.38 ms latency on mobile CPU.
- MAE 2.85e-4, close to ModernTCN.
- Tracks phase shifts; SparseTSF drifts out of phase.
- Smallest deployable model that still adapts.

Next:
Does better forecasting change scheduling?

------------------------------------------------------------------------

Slide 17 - Simulation scenario
Time: 12:00 (0:50)

Say:
Control question, not a regression question.

Notes:
- Second experiment: control quality, not just regression error.
- COSCO fog simulator with BitBrains traces.
- 500 VMs, 50 heterogeneous nodes.
- 60% edge, 40% cloud.
- AERO, Pathformer, SparseTSF, and reactive baseline.
- Objective: energy plus response time.

Next:
Result.

------------------------------------------------------------------------

Slide 18 - Simulation result
Time: 12:50 (0:55)

Say:
AERO matches a model 4,000x larger.

Notes:
- Energy: 1293 J to 1123 J, 13% down from reactive.
- Response: 10.02 s to 3.29 s, 67% down.
- SLA violations: 22.21% to 0.21%, 99% down.
- Essentially tied with Pathformer.
- AERO matches a model 4,000x larger.

Next:
Honest test - live infrastructure.

------------------------------------------------------------------------

Slide 19 - Live deployment scenario
Time: 13:45 (0:45)

Say:
Does AERO hold when real production traffic shifts?

Notes:
- Third experiment moves to live infrastructure.
- Train on Google Cluster Traces.
- Test on unseen live Nearby Computing workload.
- Held-out split looks similar for both models.
- Live phase exposes real drift.
- Same hyperparameters for a clean comparison.

Next:
Result.

------------------------------------------------------------------------

Slide 20 - Live result
Time: 14:30 (1:10)

Say:
8x lower error under real drift.

Notes:
- Live MAE: 0.051 vs 0.411, about 8x lower.
- RMSE: 0.079 vs 0.430.
- Held-out data: both 0.020.
- Gap appears only under real drift.
- Inference stays within the 50 ms budget.
- About 15% lower response time and 12% lower energy.
- RQ1 answered.

Next:
RQ2 - one framework across services.

------------------------------------------------------------------------

Slide 21 - OmniFORE banner
Time: 15:40 (0:30)

Say:
Contribution 2 - OmniFORE - One Forecasting Framework, All Services.

Notes:
- OmniFORE: one forecasting framework, all services.
- Generalization from training-set design, not model size.
- Zero-shot prediction on unseen services.
- Google to Alibaba with frozen weights.

Next:
Problem.

------------------------------------------------------------------------

Slide 22 - Train a catalogue, forecast any service
Time: 16:10 (0:50)

Say:
One shared model across bursty and steady families.

Notes:
- One shared model across bursty and steady services.
- Bursty web front-ends and steady batch workers.
- Many traces, one shared theta.
- Objective: average error across all services.
- No per-service retraining.

Next:
System model.

------------------------------------------------------------------------

Slide 23 - Where OmniFORE runs
Time: 17:00 (0:40)

Say:
Same stack as AERO, one layer up - regional cluster.

Notes:
- Same prediction layer as AERO, one layer up.
- Regional cluster, one shared model.
- Serves web, batch, event-driven, and API workloads.
- GPU-capable hardware.
- Heterogeneous data by design.

Next:
State of the art.

------------------------------------------------------------------------

Slide 24 - No prior method lives in the top-right
Time: 17:40 (0:50)

Say:
The top-right - one model, high accuracy on unseen services - is empty.

Notes:
- Existing methods miss the top-right quadrant.
- ModernTCN: strong in-distribution, one model per service.
- AGCRN, LSTNet, foundation models: generic, not heterogeneity-aware.
- OmniFORE targets one model plus OOD accuracy.
- Recipe: better examples, shared patterns, transfer-oriented tuning.

Next:
Rationale.

------------------------------------------------------------------------

Slide 25 - Generalization from the training set
Time: 18:30 (0:50)

Say:
Three pain-points -> three decisions on the training set, not the model.

Notes:
- Three pain points, three data decisions.
- Heterogeneity -> group similar traces.
- Scale -> rescale each service individually.
- Overfit -> tune on held-out services.
- Gain comes from the training set, not the head.

Next:
The pipeline.

------------------------------------------------------------------------

Slide 26 - 3 phases, 7 stages
Time: 19:20 (0:50)

Say:
Three phases - Curate, Train, Tune.

Notes:
- Three phases, seven stages.
- Curate designs the training set (S1-S4).
- Train fits the model (S5-S6).
- Tune picks settings that transfer (S7).
- Next three slides unpack those phases.

Next:
Phase 1.

------------------------------------------------------------------------

Slide 27 - Phase 1 S1-S4 - designing the training set
Time: 20:10 (0:55)

Say:
Representativeness is engineered, not wished for.

Notes:
- Representativeness is engineered.
- Fingerprint each trace by shape.
- Group into bursty, steady, periodic.
- Tag every trace by family.
- Build a balanced mix across the catalogue.
- Attention keeps the whole window in view; past points do not die with the roll.

Next:
Phase 2.

------------------------------------------------------------------------

Slide 28 - Phase 2 S5-S6 - same scale, then focus
Time: 21:05 (0:50)

Say:
Head is conventional; the gain is what it's trained on.

Notes:
- Phase 2 puts every service on the same scale.
- Individual rescaling gives each service equal weight.
- Conventional attention head.
- Learns patterns that rhyme across families.
- Gain still comes from the curated training set.

Next:
Phase 3.

------------------------------------------------------------------------

Slide 29 - Phase 3 S7 - tune so it transfers
Time: 21:55 (0:45)

Say:
Score each config against held-out services, not the training distribution.

Notes:
- Phase 3 defines what good means.
- Bayesian optimization with GP surrogate.
- Score configurations on held-out services.
- Reward transfer, not memorization.
- Generalization enforced at tuning time.

Next:
Two experiments.

------------------------------------------------------------------------

Slide 30 - E1 - clustering scenario
Time: 22:40 (0:45)

Say:
Does picking smart training data really help?

Notes:
- First OmniFORE experiment is an ablation.
- Version A: one representative trace per cluster.
- Version B: 100 random traces.
- Same model, same tuning, same test.
- Only the training set changes.

Next:
Result.

------------------------------------------------------------------------

Slide 31 - E1 - clustering result
Time: 23:25 (0:55)

Say:
Smart picking wins by about 20% on every metric.

Notes:
- Clustering improves every metric.
- MAE down 20.66%.
- RMSE down 24.63%.
- SMAPE down 32.71%.
- Silhouette up 131.8%.
- Real structure, not memorization.

Next:
Cross-dataset transfer.

------------------------------------------------------------------------

Slide 32 - E2 - cross-dataset scenario
Time: 24:20 (0:45)

Say:
Test it on a dataset it has never seen.

Notes:
- Hardest test: unseen dataset.
- Train on Google Borg A through F.
- Freeze weights, test on Alibaba Cloud 2022.
- Pod MS_11349.
- No retraining, no fine-tuning.
- Different provider, different workload mix.

Next:
Result.

------------------------------------------------------------------------

Slide 33 - E2 - cross-dataset result
Time: 25:05 (1:00)

Say:
Predicts any new service effectively; no retraining needed.

Notes:
- Unseen Alibaba pod: MAE 7.27e-3.
- 30.41% better than ModernTCN.
- 74.67% better than AGCRN.
- 84.70% better than LSTNet.
- RQ2 answered: new services without retraining.

Next:
Last piece - AgentEdge.

------------------------------------------------------------------------

Slide 34 - AgentEdge banner
Time: 26:05 (0:30)

Say:
Contribution 3 - AgentEdge - NL intent -> validated autonomous action.

Notes:
- AgentEdge: natural-language intent to validated action.
- Multi-agent LLM plus validation before execution.
- Beats single-agent and tree-search baselines.
- Target: above 75% strict success.
- Four anchors: multi-agent, tool use, reasoning, digital-twin validation.

Next:
Problem.

------------------------------------------------------------------------

Slide 35 - No system turns intent into actions
Time: 26:35 (0:50)

Say:
The middle of the diagram is a question mark today.

Notes:
- Operator says: "reduce energy while keeping SLA."
- The middle is the missing piece.
- Intent is ambiguous.
- Actions are irreversible.
- State is distributed.
- One system has to solve all three.

Next:
Where AgentEdge sits in the stack.

------------------------------------------------------------------------

Slide 36 - Where AgentEdge runs
Time: 27:25 (0:50)

Say:
AgentEdge is the agentic decision layer - L1 + L2.

Notes:
- AgentEdge sits in layers 1 and 2.
- Four agents: Intent, Observability, Planning, Infra Action.
- Planning uses ActSimCrit with twin validation.
- Twelve orchestrator or Kubernetes endpoints.
- AERO and OmniFORE become prediction tools inside the loop.

Next:
PARES - the capability contract.

------------------------------------------------------------------------

Slide 37 - PARES - capability framework
Time: 28:15 (0:55)

Say:
PARES is the capability contract - how I compare prior work on the next slide.

Notes:
- PARES: Perceive, Act, Reason, Evaluate, Sustain.
- Prior work in prose is impossible to compare.
- Each capability maps to one clear question.
- Separate agents specialize per role.
- Framework built on a general orchestration library, not a script.

Next:
State of the art.

------------------------------------------------------------------------

Slide 38 - Prior systems miss load-bearing capabilities
Time: 29:10 (1:10)

Say:
Only AgentEdge is full-row green.

Notes:
- Capability matrix, not a single score.
- Nine required capabilities.
- Every prior system misses at least one load-bearing column.
- Three unique columns: edge-plus-cloud span, validation before action, PARES.
- Q&A prep: ReAct + LATS retargeted onto our tool surface.
- Same tools, same base LLM, same scenarios for fair comparison.
- Only AgentEdge is full-row green.

Next:
Rationale.

------------------------------------------------------------------------

Slide 39 - One pain -> one design decision
Time: 30:20 (0:55)

Say:
Drop any one of these four and the system fails predictably.

Notes:
- Each pain point forces one design choice.
- Ambiguous intent -> Intent agent.
- Distributed state -> Observability agent.
- Plans fail -> ActSimCrit.
- Irreversible action -> digital twin.
- Remove one piece and the system breaks.

Next:
Architecture.

------------------------------------------------------------------------

Slide 40 - Graph-of-graphs, 4 agents, PARES
Time: 31:15 (0:55)

Say:
Outer sequential flow; each agent is its own subgraph.

Notes:
- Graph of graphs.
- Outer flow: start, Intent, Observability, Planning, Infra Action, end.
- Each agent is its own subgraph.
- Every agent satisfies PARES.
- Specialized enough to debug, flexible enough to stay agentic.

Next:
Perception agents first.

------------------------------------------------------------------------

Slide 41 - Intent + Observability
Time: 32:10 (1:00)

Say:
Perception is a bounded world model plus a typed intent parse.

Notes:
- Perception = typed intent + bounded state.
- Intent agent outputs structured JSON goals.
- Example: rebalance node_3 to node_5, keep SLA, save at least 15% energy.
- Observability agent outputs a typed cluster snapshot.
- Example: p99_ms 118, budget_used 0.70.
- Structured I/O all the way through.

Next:
Planning and ActSimCrit.

------------------------------------------------------------------------

Slide 42 - Planning + ActSimCrit
Time: 33:10 (1:15)

Say:
Validation before execution is structural, not post-hoc.

Notes:
- Five-phase planning loop.
- Strategic plan, state analysis, action selection.
- Simulate and critique.
- Check intent satisfaction.
- Critic rejection goes back to action selection, not the live cluster.
- Batching, three-tier state, rejection feedback, deadlock detection.
- Nothing executes until the validated JSON object exists.

Next:
The simulator.

------------------------------------------------------------------------

Slide 43 - Simulator - master scenario
Time: 34:25 (0:55)

Say:
Runtime guarantee AND experimental harness.

Notes:
- Simulator has two roles.
- Runtime digital twin inside ActSimCrit.
- Experimental harness for all AgentEdge evaluations.
- Far edge, near edge, and cloud tiers.
- Twelve API endpoints.
- Same infra, same LLM, same tools; only architecture changes.

Next:
Experiment 1.

------------------------------------------------------------------------

Slide 44 - E1 - single vs multi-agent scenario
Time: 35:20 (0:50)

Say:
Architecture vs architecture - not LLM vs LLM.

Notes:
- First AgentEdge experiment compares architectures.
- Three scenarios: full node, low-power conflict, compound deficit.
- Three systems: AgentEdge, ReAct, LATS.
- Same base model: qwen3-235B-A22B, temperature 0.2.
- Thirty runs per scenario.
- Metric: strict valid end-state success.

Next:
Result.

------------------------------------------------------------------------

Slide 45 - E1 - result vs baselines
Time: 36:10 (0:55)

Say:
Architecture gain, not model gain.

Notes:
- AgentEdge: 78.3%.
- LATS: 65.0%.
- ReAct: 28.3%.
- 1.20x over LATS.
- 2.76x over ReAct.
- Gain comes from architecture, not model choice.

Next:
Is the twin structural?

------------------------------------------------------------------------

Slide 46 - E2 - twin ablation scenario
Time: 37:05 (1:00)

Say:
Turn the digital twin on and off; hold everything else constant.

Notes:
- Twin ablation: everything constant except simulation.
- With twin: Plan, Simulate, Critique, Execute.
- Without twin: same agents, Crit failure refines plan in place.
- No round-trip back to Planning when twin is off.
- Twin isolates pre-execution validation, not "retry at all."
- Q&A prep: report both success and API-call count; failures cannot hide.

Next:
Result.

------------------------------------------------------------------------

Slide 47 - E2 - twin ablation result
Time: 38:05 (1:00)

Say:
Sandbox validation reduces costly trial-and-error.

Notes:
- With twin: 78.3% success.
- Without twin: 53.3%.
- 1.47x lift from the twin.
- With twin: 10.9 +/- 1.1 API calls.
- Without twin: 8 to 517 calls, SD 109.4.
- About 10x lower API-call variance.
- Twin is structural: lifts success AND collapses variance.

Next:
Scalability with cluster size.

------------------------------------------------------------------------

Slide 48 - E3 - energy scalability scenario
Time: 39:05 (0:50)

Say:
Does the agent keep saving energy as infrastructure grows?

Notes:
- Final AgentEdge question: do energy savings survive scale?
- Three sizes: 8, 20, 35 nodes.
- Same task: energy consolidation under SLA.
- Main metric: watts saved, plus percent of baseline rack power.
- Response time reported alongside.

Next:
Result.

------------------------------------------------------------------------

Slide 49 - E3 - energy at scale
Time: 39:55 (1:10)

Say:
Savings hold at every scale; 20 nodes is the peak.

Notes:
- 8 nodes: 89 W saved, 20.6% gain.
- 20 nodes: 300.8 W saved, 55.5% gain - the peak.
- 35 nodes: 185.2 W saved, 9.5% gain.
- Shared y-axis, 10 runs per scale.
- 100% success at every scale.
- Q&A prep: dip at 35 nodes is a context-window artefact, not a ceiling.
- Summarization or sharding would continue the scaling.

Next:
Synthesis.

------------------------------------------------------------------------

Slide 50 - Operator stack + publications
Time: 41:05 (1:10)

Say:
Three contributions, one stack, problems answered layer by layer.

Notes:
- Same four-layer stack, now populated with anchors.
- L1 operator: intent plus exception review.
- L2 decision: AgentEdge - 78.3% success; 55.5% energy saved at 18 nodes.
- L3 prediction: AERO - 599 params, 0.38 ms inference.
- L3 prediction: OmniFORE - 30.41% lower MAE, zero-shot to new services.
- L4/L5: Kubernetes API, 12 endpoints.
- 8 publications; full list on backup slide B7.

Next:
Open problems are all on L1 + L2 - the agentic frontier.

------------------------------------------------------------------------

Slide 51 - Future Work - Agentic Era
Time: 42:15 (0:30)

Say:
L3 + L4 solved; open problems live at L1 + L2.

Notes:
- Predictor layers solved; frontier moves up.
- L3 and L4 dimmed.
- L1 and L2 remain open.
- Three next challenges: reliability and trust.
- Real-time agent infrastructure.
- Distributed orchestration ecosystems.

Next:
Direction 1.

------------------------------------------------------------------------

Slide 52 - Benchmarks do not exist yet
Time: 42:45 (0:55)

Say:
Benchmarks do not exist yet - and without them, we cannot know whether a change helps.

Notes:
- First trust problem: benchmarking.
- No shared benchmark suites today.
- Multiple plans can be valid; no single ground truth.
- LLM non-determinism: one fix can break another scenario.
- Good benchmarks would enable small fine-tuned orchestration models.
- Research needs equivalence classes of correct plans.

Next:
Direction 2.

------------------------------------------------------------------------

Slide 53 - Latencies accumulate to tens of seconds
Time: 43:40 (1:00)

Say:
This is a context-engineering problem, not a hardware one.

Notes:
- Second barrier: latency.
- Planning loops and tool calls add up to tens of seconds.
- Observed state can change before execution.
- Accuracy drops when the tool surface gets too large.
- Roughly beyond 30 tools in our experiments.
- Path: bounded context, fewer tools, smaller tuned models.
- Further out: fuse agent loops with RAN/core timing budgets.

Next:
Direction 3.

------------------------------------------------------------------------

Slide 54 - Parallel instances conflict on shared infra
Time: 44:40 (0:50)

Say:
Parallel instances conflict on shared infrastructure.

Notes:
- Third direction: coordination at scale.
- Many agent instances across regions and domains.
- Need OpenAPI-equivalent for agent tool-calls - model-agnostic.
- Consensus or lock-lease for intended actions.
- Conflict detection before actuation, not after.
- One agent consolidates onto a node while another powers it down.

Next:
Conclusions.

------------------------------------------------------------------------

Slide 55 - Conclusions
Time: 45:30 (1:00)

Say:
Three layers; one systems thesis; nine anchor numbers.

Notes:
- Claim 1 AERO: 599 params; 8x lower error under drift; -50% migrations vs SOTA.
- Claim 2 OmniFORE: -30.41% MAE vs ModernTCN; +20.66% from clustering; zero-shot on unseen cloud.
- Claim 3 AgentEdge: 1.47x twin on vs off; 10x lower API variance; 300.8 W peak @ 18N.
- Orchestration moves from reactive supervision to a proactive, validated control stack.

Next:
Questions.

------------------------------------------------------------------------

Slide 56 - Q&A
Time: 46:30 (open floor)

Say:
Thank the committee; I welcome your questions.

Notes:
- Questions on deployability, generalization, validated autonomy.
- Also baselines, evaluation methodology, and future work.
- Backup slides B1-B13 available for deep-dives.
- Open floor to the committee.
