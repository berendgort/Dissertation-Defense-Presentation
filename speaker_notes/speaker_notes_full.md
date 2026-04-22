### Slide 01 · Title

Good morning. I am Berend Jelmer Dirk Gort, and today I defend my doctoral thesis, *AI-Driven Zero-Touch Orchestration of Edge-Cloud Services*, within the Doctoral Program in Signal Theory and Telecommunications at Universitat Politècnica de Catalunya. The work was supervised by Dr. Angelos Antonopoulos at Nearby Computing and co-supervised by Associate Professor Dra. Anna Umbert at UPC.

It was developed with Nearby Computing as the industrial partner, which matters because the contributions you will see today were exercised against real infrastructure rather than only offline benchmarks.

### Slide 02 · From framing to validated autonomy

The defense follows a five-part path. I start with framing, then move through the three contributions in order: AERO, OmniFORE, and AgentEdge, and I close with a synthesis. The color code is consistent throughout the deck: blue for AERO, orange for OmniFORE, and pink for AgentEdge.

The point of this slide is simply to fix the map before the evidence starts: framing first, then the three contributions, then synthesis.

### Slide 03 · Manual reality today

This slide defines the operator contract we want at the top of the stack: the operator should set intent, and the loop should do the rest with human review only on exceptions. The reason that contract is still a problem, marked here as Problem 4, is that the layers underneath do not yet support it.

At layer two there is no intelligent path from natural-language intent to orchestration action, so the operator still ends up bridging the gap manually. At layer three the prediction layer fails in two different ways: at the far edge there are no accurate per-node forecasts, and in larger compute sites a new model must be refit for every service. The far-edge box makes the motivation explicit: prediction matters because actions must be chosen before SLA and energy drift become irreversible. Layer four is the given environment: heterogeneous far-edge nodes, regional clusters, and the cloud. Four layers, four open problems, one stack that still does not close the loop.

### Slide 04 · Zero-touch: operator sets intent, not actions

The goal is zero-touch: operator sets intent, not actions. Goals, SLAs, and constraints go in; orchestration decisions come out. The left-hand loop is the control cycle: predict, decide, act, observe. Forecasts drive decisions, decisions are executed, the new state is observed, and fresh traces feed the next round. Human review should happen only on exceptions.

The right-hand figure explains why prediction is load-bearing. The black line is demand, and the red staircase is reactive capacity. When demand rises, reactive control scales up late, so the system spends time under-provisioned and accumulates SLA violations. When demand falls, reactive control scales down late, so the system keeps idle capacity online and wastes energy. The dashed blue curve is predictive control: capacity is in place when the spike arrives and released when it leaves. Prediction closes both gaps, which is why two of the three thesis contributions land in the predict stage.

### Slide 05 · Forecasting must run where the service runs

The first sub-problem is a deployability problem at the far edge. Today's SOTA baseline is a 2.4-million-parameter transformer: accurate, but too large for small edge hardware. Lightweight alternatives around fifty-thousand parameters fit the device budget, but their accuracy collapses under drift.

That leaves the deployability gap — small and accurate at the same time — unfilled. Research question one follows directly: can workload prediction remain practical and accurate at edge scale? I fix the quantitative target up-front: below one thousand parameters with competitive accuracy.

### Slide 06 · One model for many services

The second sub-problem is generalization. Even if edge prediction works, the default practice is still one model per service, and that cost scales linearly with the catalogue. Each new service or drift event means retraining, monitoring, and maintenance all over again.

At 6G scale that quickly becomes a three-hundred-plus-service problem, so the real barrier is not inference cost but retraining burden. Research question two therefore becomes: can one forecasting framework cover heterogeneous service workloads without per-service retraining?

### Slide 07 · From natural-language intent to intelligent orchestration action

The third and fourth problems belong to the decision layer. The operator can already state intent in natural language, for example, *"reduce energy while keeping SLA"*, but that input does not map cleanly onto classical heuristics or fixed objective functions. Today the bridge is still a human who reads dashboards, chooses services, chooses targets, and executes commands like drain, scale, migrate, or power-off.

That means the control loop still scales with human attention rather than workload. Zero-touch at this layer means two abilities together: understand intent and turn it into safe orchestration action without a person translating each step by hand.

### Slide 08 · One orchestration stack that predicts, generalizes, and acts on intent

These four problems collapse into three research questions, three objectives, and three contributions. Research question one becomes objective one and contribution one, AERO: deployable edge prediction. Research question two becomes objective two and contribution two, OmniFORE: cross-service generalization. Research question three becomes objectives three and four and contribution three, AgentEdge: intelligent action from intent.

The claim at the bottom of the slide is the whole thesis in one line: each contribution removes one blocker, and together they close the zero-touch loop.

### Slide 09 · AERO

Contribution one is AERO: edge-deployable workload prediction. The banner states the claim very directly: adaptive periodicity lets a tiny model produce operationally useful forecasts at the edge.

The quantified goal is fewer than one thousand parameters. That is the constraint that the rest of the AERO section has to defend.

### Slide 10 · System Model & Motivation

This slide is deliberately generic: it is the system model for the predictor box, not AERO itself yet. On the left, the local loop is observe, predict, and schedule inside one control cycle. The predictor could sit per node or as a sidecar; the system constraint is only that the forecast reaches the scheduler before the slot closes.

On the right, the toy example explains why timing is the load-bearing issue. Workstation A backs up while B is still free, and the dispatch decision is due in three seconds. If the forecast is local, the scheduler reroutes in time. If the loop first goes off-node, the reply returns after the useful moment. So the claim here is not about AERO's mechanism; it is about placement and timing: prediction is only operationally useful if it arrives before the slot closes.

### Slide 11 · State-of-the-art - Accurate or deployable, not both

The literature now falls into three color-coded regimes. In red are the heavy, undeployable baselines: Pathformer at 2.4 million parameters, WGAN at 2.9 million, ModernTCN at 247 thousand, and FourierGNN at 228 thousand. In amber is SparseTSF, the adapted lightweight baseline: it fits the budget, but accuracy gives way.

The green target zone at the top-left is the point of the slide: small and accurate. AERO sits there at 599 parameters, and the experiments from here on are about showing it truly belongs in that empty quadrant.

### Slide 12 · Design - How AERO works in three steps

AERO's mechanism is intentionally simple on this slide. Step one is to find the rhythm: the repeating pattern in the trace can change over time, so AERO re-checks it every window. Step two is to align first: once the rhythm is known, the repeated cycles are lined up so a small predictor can work on organized structure rather than raw disorder. Step three is to reuse cached layers: when the same pattern returns, the same block can be reused instead of recomputed from scratch.

The big idea is that AERO makes the signal easier before it asks a tiny model to forecast it.

### Slide 13 · Scenario 1 - Workload Prediction

This is the scenario slide for the efficiency benchmark. The dataset is the Alibaba 2022 microservices trace, specifically pod MS_11349, with 18,720 one-minute samples across thirteen days and two normalized features: CPU and memory. The benchmark set is five baselines plus AERO.

All models are trained on the same server: NVIDIA A100 40 GB, 30 CPU cores, 200 GiB RAM, 512 GiB SSD, Ubuntu 20.04.2, using Python and PyTorch. Hyperparameters are tuned with Bayesian optimization using twenty random trials and thirty refinement trials per model. The reported outputs are MAE, RMSE, latency, convergence, parameter count, and memory. The slide fixes the exact setup before I show the efficiency result.

### Slide 14 · Result 1 - Small enough and accurate enough

Three columns, one conclusion. In parameter count, AERO has 599 parameters, while the heavy baselines range from 228 thousand up to 2.9 million. SparseTSF is smaller at 35 parameters, but size alone is not the goal. In inference latency, AERO is at 0.38 milliseconds, well inside the 50-millisecond budget; even Pathformer stays at 0.52 milliseconds, but it does so with a far larger model. In MAE, AERO reaches 2.9 times ten to the minus four, essentially on par with ModernTCN and close to Pathformer.

So the title is the takeaway: only AERO is simultaneously small enough to deploy and accurate enough to matter.

### Slide 15 · Scenario 2 - Orchestration outcomes

Now I move from forecasting quality to control impact. The simulator is COSCO on AzureFog: 50 heterogeneous hosts, sixty percent edge and forty percent cloud, with 3-millisecond edge latency, 76-millisecond cloud latency, and 5-gigabit links. The run lasts 2,000 cycles at 300 milliseconds, with 50 containers and 4 arrivals per step.

Forecast inputs come from the BitBrains Random trace: 500 VM traces, 8,631 samples, and seven workload signals. The compared arms are AERO, Pathformer, SparseTSF, and a reactive controller that bypasses prediction. Same scheduler, same workload stream, same objective of minimizing energy plus response time; only the forecast quality changes.

### Slide 16 · Result 2 - Controlled simulation results

The result slide uses four operational metrics. Energy is 1293 joules for the reactive baseline, 1140 for SparseTSF, and 1123 for both AERO and Pathformer. Response time falls from 10.02 seconds for reactive to 6.5 for SparseTSF, 3.29 for AERO, and 2.45 for Pathformer. SLA violations collapse from 22.21 percent reactive to 4.60 percent with SparseTSF, 0.21 percent with AERO, and 0.10 percent with Pathformer.

Task migrations increase because predictive schedulers act before overloads appear: 2,026 for reactive, 5,309 for SparseTSF, 7,747 for AERO, and 8,480 for Pathformer. The honest interpretation is that only AERO fits edge hardware while staying close to Pathformer, a model roughly 4,000x larger.

### Slide 17 · Scenario 3 - Live deployment

The final AERO test is live deployment. The training source is a Google Cluster trace with T equal to 8,930 samples, four features, and five-minute resolution. Both AERO and SparseTSF are trained with the same setup and hyperparameter search, then deployed as microservices on a physical testbed: i9-9900K, 46 GB RAM, RTX 2060, Ubuntu 24.04.1, using Docker Compose.

On the held-out test split the two models look almost indistinguishable; the live unseen workload is where drift exposes the difference. The live evaluation reports normalized MAE, RMSE, and mean inference time under the 50-millisecond real-time threshold.

### Slide 18 · Result 3 - Live deployment results under real-world drift

The live deployment numbers are clean. On the unseen workload, AERO reaches a mean absolute error of 0.051, while SparseTSF reaches 0.411, about eight times higher. RMSE tells the same story: 0.079 for AERO and 0.430 for SparseTSF. Inference is 2.65 milliseconds for AERO and 1.12 milliseconds for SparseTSF, so both remain comfortably within the 50-millisecond scheduler budget.

The point is that latency is not the differentiator; drift robustness is. That is why the operator-impact footer matters: roughly fifteen percent lower response time and twelve percent lower energy once the model stays accurate in the live environment.

### Slide 19 · OmniFORE

Contribution two is OmniFORE: one forecasting framework, all services. The banner separates the claim from the goal. The claim is that models exist that can predict any trace. The goal is stronger and more operational: one model that can process all workload traces.

The concrete promise I test next is zero-shot prediction on services the model never saw during training, up to cross-dataset transfer with frozen weights.

### Slide 20 · Problem - one model, many services

This slide states the OmniFORE problem in operator terms. I want one model trained once on a service catalogue and then able to forecast any service in that catalogue, including services it has never seen. The visual contrast is between bursty and steady families, because the model has to cover both without separate retraining.

Formally, the goal is one shared set of weights, no per-service fine-tuning, and average prediction error minimized across all services, seen and unseen. That is the only path by which the prediction layer actually scales operationally.

### Slide 21 · System Model & Motivation

Again this is the generic setting, not the method. On the left, one prediction layer observes many service traces at a compute site, which could be any tier, and returns per-service forecasts into the same downstream decision stack. On the right, the motivation is operational cost.

Today each site tends to carry its own forecasting model copy. As the number of sites grows, retraining, memory, and monitoring repeat everywhere. The target is one shared model that can serve many sites and many services, instead of duplicating the machine-learning workload at every location.

### Slide 22 · State-of-the-art - no prior method lives in the top-right

The prior work again falls into two red regimes around one green target. The first red regime is per-service retraining: ModernTCN, AGCRN, and LSTNet can work well on the service they saw, but every new service needs a new model. The second red regime is generic but heavy: foundation models promise reuse, but are too heavy and too generic to be the deployable workload layer.

The top-right quadrant, one model with unseen-service accuracy, is still empty. OmniFORE is designed to occupy that gap.

### Slide 23 · Design - How OmniFORE works in three phases

This slide packages the OmniFORE pipeline. Phase one, stages S1 through S4, designs the training set by encoding traces, clustering shapes, and sampling a balanced catalogue. Phase two, stages S5 and S6, rescales each service and then uses attention over a shared window so one model can learn across heterogeneous services. Phase three, stage S7, tunes hyperparameters on held-out services so the selected setting is rewarded for transfer rather than memorization.

The message is that generalization comes from the whole pipeline: representative data, shared training, and transfer-focused tuning.

### Slide 24 · Building the training set

This slide zooms into phase one. S1 fingerprints each trace by compressing it into a shape descriptor. S2 clusters those fingerprints into bursty, steady, and periodic families. S3 tags every trace with its group label. S4 samples proportionally from those groups to build a balanced mix.

The point is that representativeness is engineered before training begins, so the model later sees the catalogue in balanced form instead of allowing one family to dominate the dataset.

### Slide 25 · Training the model

Phase two has two steps. S5 is equal scale: raw services arrive at very different magnitudes, so each trace is rescaled so that large services do not drown out small ones. Every workload gets an equal say in training.

S6 is efficient attention. The top figure shows the head scanning the full recent window and pulling forward the strongest matching moments. The bottom figure contrasts all links with a sparse view, showing why long windows stay cheap instead of paying equal attention to everything.

That is also why the model generalizes: it matches patterns rather than service identity, so after rescaling those patterns can transfer to services it has never seen.

### Slide 26 · Tuning for transfer

Phase three is the single S₇ stage: tune so it transfers. On the left, Bayesian optimisation keeps moving toward the best region, and the star marks the winning setting on the objective-function curve. On the right, the training set is shown separately because it is used to fit the model, not to score the hyperparameters. Only the held-out traces T1, T2, and T3 feed the combined transfer score, so the selected setting is the one that works across new services, not the one that merely fits the training set. The bottom result strip makes the payoff explicit: the winner is chosen for new services.

### Slide 27 · Scenario 1 - Clustering Impact

Scenario 1 isolates the impact of clustering in the training-set design. On the left is the clustered sample: a balanced mix of workload patterns. On the right is the random baseline: draw the traces at random, repeat that five times, then average the result. Everything else is held fixed: same model, same tuning, same test services. Only the training traces differ. So if the clustered version wins, the gain comes from the data selection step itself.

### Slide 28 · Result 1 - Clustering-based training helps

The percentages matter here because the experimental control is so clean. When the training traces are chosen through clustering instead of random sampling, MAE drops by 20.66 percent, RMSE by 24.63 percent, and SMAPE by 32.71 percent. The model, tuning, and zero-shot test are all unchanged, so the gain comes from the training-set selection step itself.

That is the takeaway: clustering forces the sample to cover bursty, steady, and periodic workload families, whereas random selection over-samples the common shapes and misses rare ones. The next experiment asks whether that representativeness survives a full cross-dataset transfer.

### Slide 29 · Scenario 2 - Cross-dataset transfer

The second experiment is the hardest test a forecaster can run: train on Google Borg cells A through F, freeze the weights, and evaluate on Alibaba Cloud 2022 — specifically pod MS_11349. No retraining, no fine-tuning, different cloud provider, different workload mix. The three strips on-slide call out exactly what is different between the two environments, and the italic line on the slide is honest about what usually happens here: *this is where benchmark wins usually fall apart*. If the model generalises, it has to generalise without our help.

### Slide 30 · Result 2 - Generalises without retraining

This is the transfer result on Alibaba. OmniFORE reaches an MAE of 0.00727, while ModernTCN reaches 0.01045, AGCRN 0.02870, and LSTNet 0.04751 on the same task. Read the bars as "how much worse the baseline is than OmniFORE": ModernTCN is 44 percent higher, AGCRN 295 percent higher, and LSTNet 554 percent higher, all with OmniFORE still running as the same frozen model.

That is why this result matters operationally. The model is learning portable workload patterns rather than provider-specific identities, so a new service can be forecast with the existing model immediately instead of triggering a new training cycle. That answers research question two: one framework generalises across heterogeneous services, and the last missing block in the zero-touch loop is AgentEdge.

### Slide 31 · AgentEdge

Contribution three is AgentEdge: natural-language intent becomes validated autonomous action. The banner states the claim in one sentence: a multi-agent large-language-model system with validation before execution beats single-agent and tree-search baselines, with success above seventy-five percent. The keywords I want on the record from this slide forward are multi-agent, tool-use, multi-step reasoning, and digital-twin validation. Those are the technical anchors for everything in the rest of this section.

### Slide 32 · Problem & Motivation

This slide must make one point absolutely explicit: the decision layer is not a convenience, it is the missing step that turns a human goal into something the platform can actually execute. If an operator says *"reduce energy while keeping SLA"*, Kubernetes cannot do anything with that sentence. Someone still has to decide which service may move, which node must stay pinned, where spare capacity exists, what action is safe, and what has to be monitored afterward. In the example on the slide, that human translation becomes something like: keep the latency-critical service pinned, shift batch load to a freer node, then allow low-power mode where it is safe. Existing optimizers usually start only after those choices have already been made and written down as formal inputs. That is why this layer is necessary: without it, the control loop still depends on a human in the middle. The figure then visualizes that exact translation step before the next slide formalizes it as the system model.

### Slide 33 · System Model

This slide is the generic stack, not the AgentEdge architecture yet. The left column compresses the loop into four layers: operator intent, a decision layer, a service-orchestration layer, and the infrastructure itself. In that framing, the prediction step belongs inside the service-orchestration layer rather than standing alone as its own layer. The key point in the right-hand diagram is that the decision layer does not query the prediction layer directly. Instead, service orchestration queries the prediction model, stores the returned predictions in data objects, and the decision layer reads those stored objects together with the live state. Inside that decision layer, the intelligent logic reasons over sets of actions rather than a single raw action. The purpose of this slide is simply to pin down those interfaces before the following slides introduce the concrete AgentEdge design.

### Slide 34 · Design - What is an agent?

Before the state of the art, I first need a precise definition of what I mean by *agent* in this thesis. It is not just one LLM call. Read the slide left to right as five compact cards. To count as an agent here, the system must satisfy PARES: Perceive live bounded state, Act through typed tools, Reason over goals and constraints, Evaluate candidate plans before production, and Sustain behaviour across multi-step interactions. Every card is load-bearing, and if one is missing the system may still be useful automation, but it is not agent-complete.

The reference band below the cards makes an important methodological point: PARES was not copied from one single framework. It was synthesised in Chapter 2 from six representative agentic-framework papers, and that is what justifies using it as the comparison contract on the next slide.

### Slide 35 · State-of-the-art: 6G literature still lacks a full agent

This table makes one point directly: the 6G literature does not yet give us a full agent. The left side is the capability matrix with deployment, the five PARES letters — Perceive, Act, Reason, Evaluate, Sustain — and multi-agent coordination. The numbered Ref. column maps to the compact citations on the lower right, and the top-right card explains why the Chapter 5 baselines had to come from ML rather than from the 6G rows.

The reason is methodological, not cosmetic. The six 6G papers are valuable related work, but they do not satisfy full PARES and they do not fit the validated Intent-Observe-Plan-Act system model that AgentEdge evaluates for edge-cloud orchestration. ReAct and LATS are therefore the legitimate baselines: they are genuine agentic frameworks that interpret natural-language intent and coordinate multi-step actions, and we retarget them to the same tools, base LLM, and scenarios for fairness. The conclusion the slide is meant to land is simple: zero 6G rows are full agents, ReAct and LATS are PARES-complete but task-misaligned, and only AgentEdge is full-row green.

### Slide 36 · Graph of graphs and microservice deployment

The architecture is a graph of graphs — a top-level orchestrator routes, from *start* to *end*, through four subgraphs in sequence: Intent, Observability, Planning, and Infra Action. Each of those four agents is itself a small subgraph with its own internal reasoning steps; the legend on the left makes that explicit, one box per specialist, one dashed rectangle per inner subgraph. On the right is the deployment story, stripped to the essentials. Specialist pods — intent, observe, plan, infra_action — are thin, and they share two backend services: a single LLM backend that answers prompt-and-reply traffic, and a single MCP server that exposes typed tool calls. The MCP server then talks to the container orchestrator, which actually executes actions across the three physical tiers — far edge, near edge, cloud — and sends updated state back to observe. Everything agents do is either *prompt/reply* against the LLM or *tool call/result* against MCP: nothing else. On top of that, every specialist still satisfies PARES — Perceive, Act, Reason, Evaluate, Sustain — so these are agents, not prompt chains. The three benefit pills at the bottom are the architectural takeaway: *lightweight*, because thin pods call a shared LLM instead of carrying the heavy model; *flexible*, because the LLM backend can be swapped at deploy time without rewriting the agents; and *typed*, because MCP returns one shared typed interface and result shape no matter which agent called it.

### Slide 37 · AgentEdge splits orchestration across four specialists

This slide walks the committee left-to-right through the four specialists as a numbered pipeline, because each one is the minimal response to one specific failure mode in the intent-to-action path. *01 Intent Agent* takes the operator's ambiguous natural-language request — on the slide, *"cut power, keep SLA"* — and parses it into a typed goal, shown as the JSON block with `"goal": "save_power"` and `"sla": "preserve"`. Without this step, every downstream agent would have to re-interpret the operator sentence and they would disagree. *02 Observability Agent* watches the live system and filters raw telemetry — the rising power trace on the slide — into a small set of structured alerts such as *node_3 hot* and *node_5 has headroom*. Without this step, planning drowns in raw metrics. *03 Planning Agent · ActSimCrit* is the heart of the system, and the loop figure shows why: Plan proposes, Sim runs it in the digital twin, Crit critiques the simulated outcome, and the red dashed *reject* arc sends control back to Plan until the critic accepts; only then does a validated plan leave the box. That inner loop is the whole reason plans do not reach production without validation, and it is expanded on the next slide. *04 Infra Action Agent* takes the validated plan and executes it as concrete API calls — on the slide, *migrate svc → node_5* and *low_power node_3* become `POST /migrate` and `PATCH /power` requests, with retries on failure. The committee takeaway: drop any one of these four and the system fails in a predictable, locatable way — ambiguous intent, state blindness, unvalidated plans, or unreliable execution.

### Slide 38 · Planning Agent · the ActSimCrit loop

This is the core of AgentEdge, and I talk it through as a five-phase loop that runs five LLM calls plus one simulation per iteration. *P1 Plan* sets the end-goal state and the constraints the loop has to respect. *P2 State* reads the current system and identifies the bottlenecks and violations that stand between current and goal. *P3 Actions* picks the next batch of tool calls, skipping any batches the critic has already rejected. *P4 Sim + Critic* is the validation step — the action batch is simulated inside a digital twin (a sandbox, no LLM) and then judged by an independent critic LLM that has no memory of prior attempts. *P5 Intent met?* asks whether the simulated end-state actually satisfies P1; if yes, the loop emits a validated plan to the Infrastructure Action Agent, and if no, control goes back along the red dashed *reject · retry* arc to P3. If the iteration or rejection caps are hit, the loop terminates cleanly into a DEADLOCK chip and the agent proposes an alternative intent instead of spinning forever. On the right, four mechanisms make this loop actually work in practice. *Action batching* groups logically connected steps — e.g. `migrate + migrate + low-power` — into one LLM call instead of replanning each action. *Three-tier state* separates baseline, accepted, and simulated state, so only validated batches ever promote accepted state and failed batches leave it untouched. *Rejection-feedback* records the structured reason each batch was rejected — on-slide example: *node_5 over capacity (+0.4 core)*, next try *node_7 instead* — and the schema excludes rejected options from the next selection. *Deadlock detection* uses iteration and reject caps to convert infeasible intents into an achievable alternative rather than retrying forever. The output is a validated plan, not a guess; the infra agent executes it, it does not diagnose.

### Slide 39 · Simulator testbed and six evaluation scenarios

This slide does two jobs at once: it introduces the three-tier edge-cloud testbed that I use as the evaluation harness, and it lays out the six scenarios I run on it. On the left, the tiered architecture is stacked from cloud down to far edge. Tier 3, cloud, is zero-to-one node with 64 CPU, 256 GB, power envelope 180-450 W. Tier 2, near edge, is zero-to-ten nodes with 16 CPU, 32 GB, 40-120 W, connected to cloud by a 25-60 ms link. Tier 1, far edge, is typically six-to-twelve nodes with 4 CPU, 8 GB, 10-35 W, connected to near edge by 10-25 ms. Three footer chips fix the rest of the contract: *low-power* saves roughly sixty percent of wattage, timing across the stack is stochastic at fifteen-to-twenty-five percent, and the simulator exposes twelve Flask API endpoints. Same simulator also serves as the digital twin inside ActSimCrit at runtime. On the right, the six scenarios split into two groups. *Group A · constraint resolution* (S1-S3) uses two nodes to force reasoning under conflict. S1 *Full Node* — one node full, one idle — tests *free space first*. S2 *Sleep Conflict* — one active, one asleep — tests *move, then sleep*. S3 *Won't Fit* — consolidation blocked by a "NO" — tests *redistribute load*. *Group B · energy scalability* (S4-S6) uses consolidation plus power-down under three infrastructure sizes: S4 small, 8 nodes and 6 services with 2 idle; S5 medium, 18 nodes and 15 services with 3 idle; S6 large, 35 nodes and 30 services with 6 idle. Success is defined by pre-defined valid end-states and an exact match — no partial credit. The fairness guarantee in the footer of the right panel is critical: *same catalogue, same LLM, only architecture varies* — that is what makes the Experiment 1 comparison honest.

### Slide 40 · Scenario 1 — Multi-agent vs single-agent

The first AgentEdge experiment is an architecture-versus-architecture comparison, and the left side of the slide shows all three arms side by side as diagrams so we can see *why* they differ, not just that they differ. AgentEdge is the graph of graphs — four specialist agents (intent, observe, plan, infra_action) routed sequentially, one graph end-to-end. ReAct is the one-LLM think-act loop — a single model interleaves reasoning, tool calls, and observation, and only stops on a finish action; no specialization, no plan validation. LATS is the same single LLM but wrapped in Monte-Carlo tree search — the model expands, scores, and rolls out over a tree of reasoning steps, keeping the best trajectory; it is the strongest single-agent baseline in the literature. The right side of the slide is the measurement protocol, shown as a picture. Each scenario pre-defines *all valid infrastructure end-states* up front, and a run counts as successful only if the final placement lands in that set — exactly matching one of the predefined configurations. The cartoon on the right makes this concrete with a simple example: the initial state is edge-0 at fifty-percent utilisation and edge-1 at fifty-percent utilisation, and the task is *shut one server off*. The valid end-states panel shows two symmetric configurations — all load consolidated on edge-0 with edge-1 off, or all load consolidated on edge-1 with edge-0 off — both tick. The *anything else · fail* panel shows two ways a run goes wrong: still 50/50 because the task was never completed, or an uneven split such as 75/25 where consolidation stopped halfway. No partial credit. And that is the whole point of this design: same LLM, same tools, same tasks, sixty runs per arm — if the success rates differ, the gap cannot be model capability, it has to come from the architecture itself.

### Slide 41 · Result 1 - Multi-agent beats every baseline

The numbers are clean. AgentEdge succeeds on 78.3 percent of trials. LATS succeeds on 65.0 percent. ReAct succeeds on 28.3 percent. As multipliers, which are stickier than raw percentages, that is 1.20 times LATS and 2.76 times ReAct. The finding banner is direct: multi-agent architecture beats every SOTA single-agent baseline, on the same LLM, on the same tasks, in the same simulator. The next experiment takes the next obvious question — is this gain really coming from the digital twin, or from the four-agent structure alone?

### Slide 42 · Scenario 2 - Twin ablation

The ablation turns the digital twin on and off and holds everything else constant. The two panels are labelled *TWIN ON* on the left and *TWIN OFF* on the right, and they show four boxes each — PLAN, SIM, CRIT, EXEC — with the same red dashed *reject · retry* arc looping from CRIT back to PLAN. On the *TWIN ON* side, PLAN sets the actions, SIM runs them on the digital twin, CRIT (an independent critic LLM) judges the simulated outcome, and only a validated plan reaches EXEC on real infra — this is the full AgentEdge pipeline. On the *TWIN OFF* side, the PLAN and CRIT boxes are identical, but the SIM box is replaced with a red dashed *REMOVED · Sim + Critic · no pre-execution validation* ghost. What that means precisely: planning still happens, the reject-retry loop still exists, but there is no sandbox simulation before actions hit production. Plans are pushed straight to EXEC. The bullets under each panel make the consequence concrete: *TWIN ON* → plans validated on the twin before touching infra, and retries are *virtual*, bounded by iteration and reject caps; *TWIN OFF* → plans pushed to real infra without validation, and retries are *physical*, local to Exec, and unbounded. The point of this design is to isolate the twin's contribution as *pre-execution validation*, not as the existence of retries. The twin does not change whether a plan can succeed; it changes how many physical retries it takes and how much damage those retries can do on the way. That is why we report both success rate and API-call count — failure-shifting cannot hide behind either metric alone.

### Slide 43 · Result 2 - Sandbox validation reduces costly trial-and-error

The ablation tells a very direct story. With the twin, success is 78.3 percent; without it, success drops to 53.3 percent — a 1.47 times improvement. The more operational number is API behaviour. With the twin, API-call counts stay tight at 10.9 with a standard deviation of 1.1. Without the twin, they range from eight to five-hundred-and-seventeen with a standard deviation of 109.4 — about ten times higher variability. Without simulation, the agent enters unproductive retry loops that are not just slower; they are operationally unsafe, because every retry touches production. The twin is therefore structural: it lifts success *and* collapses variance. The last experiment asks how this behaviour changes as the infrastructure grows.

### Slide 44 · Scenario 3 - Energy scalability

The scalability experiment asks a practical question: does AgentEdge keep saving energy as the infrastructure grows? Same task, three infrastructure sizes. The start state at every scale is services spread across nodes with some nodes left idle, and those idle nodes still draw baseline power — that is the target the agent has to reclaim. The goal is consistent across all three scales: *consolidate services, power down idle nodes*. The three panels are *Scale A · Small* — 8 nodes, 6 services, 2 idle; *Scale B · Medium* — 18 nodes, 15 services, 3 idle, consolidation spans two racks; and *Scale C · Large* — 35 nodes, 30 services, 6 idle, cross-rack coordination stress. The legend is explicit: red blocks are service-bearing nodes, dashed white blocks are idle nodes that are candidates for power-down. The success metric is on the footer strip — energy reduction greater than zero watts at every scale. The honest test underneath the number is whether multi-agent coordination remains effective as the infrastructure grows without the planning overhead starting to dominate at 35 nodes. That is the question the next slide answers.

### Slide 45 · Result 3 - Power drops across every scale

Three panels, one story. The y-axis on each panel is total rack power in watts, and the x-axis is the number of API calls the agent has made. Every green square marks the starting power, every red triangle marks the settled power, and the green arrow in the middle of each panel is the delta-watts — how much power the agent reclaimed. At eight nodes, power drops from about four-hundred-and-sixty watts to roughly three-hundred-and-seventy watts; delta-W equals eighty-nine watts. At eighteen nodes, power drops from about seven-hundred-and-ten watts to four-hundred-and-ten watts; delta-W equals three-hundred-point-eight watts — the peak, and the one I want the committee to remember. At thirty-five nodes, power drops from roughly twelve-hundred-and-fifty watts to just over one-thousand watts; delta-W equals one-hundred-and-eighty-five-point-two watts. A reasonable follow-up is *why does eighteen beat thirty-five?* The thirty-five-node curve flattens early because the full node state overflows the LLM prompt; it is a context-window artefact, not a fundamental limit. With summarisation or sharded context, the curve would keep descending. All thirty runs succeeded across every scale. The key claim on this slide is that validated autonomy remains energy-relevant at production scale, and that the saturation at the largest scale is explained rather than hidden.

### Slide 46 · Slide 03 reprise + publication mapping

This slide is a callback to slide three. The left side is a headline-only version of the same four-layer stack, but now labelled by contribution instead of problem: AgentEdge sits at layers one and two, AERO and OmniFORE split layer three, and the related book chapter sits with layer four. The right side maps the stack onto the thesis publication list: AgentEdge maps to [J1] and [C1], AERO maps to [J4] and [C3], OmniFORE maps to [J3], [J5], and [C2], and [B1] is the related book-chapter output at infrastructure level.

I keep this one very short in delivery. The point is simply that the publication record lines up with the stack itself. The full bibliographic list remains on backup slide B7.

### Slide 47 · Future Work · The Agentic Intelligence Layer

Same stack as the previous slide. The left column is unchanged on purpose: L1 and L2 are the agentic layers, L3 is the prediction layer finished by AERO and OmniFORE, L4 is the hardware we run on. What changed is the right-hand side. The publications are gone, and in their place is a single clear indicator: future work lives on L1 and L2. That is the agentic intelligence layer, and that is where this chapter of research continues.

Three short cards explain why. The first, *prediction is heavily researched*: lightweight nets and attention mechanisms rest on decades of time-series work. It is a mature field with established methodology. The second, *orchestration is a younger field*: which predictor to invoke for each situation, when a forecast warrants action, how to balance objectives that no single model optimizes — those are all still open questions. The third, *predictors become tools the agent selects*: AERO and OmniFORE are tools an agent picks, the same way a human operator picks between monitoring dashboards. Once you frame them as tools, the research question moves one level up, to the entity that chooses between them.

That is the transition. From here, the next three slides open up the specific blockers on L1 and L2.

### Slide 48 · Future Work 1 · Reliability & Trust

The first future-work slide picks the two blockers that, together, decide whether operators will ever let an agent run unattended. I keep only two per slide, each shown as its own card with a visual.

On the **left card**, the blocker is that *there are no public benchmarks for orchestration*. Every team builds its own bench, runs it on their own workload, and reports numbers that nobody else can reproduce. The visual puts three dashed boxes on the left — team A, team B, team C, each with their *own bench* — and then an arrow into a single shared frame on the right: an open orchestration benchmark fed by real operator traces, a leaderboard, and public competitions. The direction is a concrete programme that can start tomorrow. First, publish open benchmarks built from real, historical operator action traces — not synthetic workloads, the actual actions that humans and schedulers took on production clusters. Second, run public competitions on those benchmarks so the field accumulates a shared research history instead of re-inventing the wheel paper by paper. Third, the same trace datasets are exactly what is needed to train orchestration *world models* — V-JEPA 2 style — so an agent can simulate the consequences of a planned action before it commits.

On the **right card**, the blocker is *security*, and I want to be precise about the threat model. The concern is not external prompt injection — orchestration agents sit inside a protected perimeter where only authorized operators have access. The concern is what happens when the agent itself makes a mistake. An agent with Kubernetes API access can delete pods, misconfigure services, or cause cascading failures without any adversary involved. So the research question is simple: *put brakes between the agent and production*. The visual is deliberately minimal — the agent on the left, the cluster on the right, and one safety layer in the middle with three rows inside it: *keep data local*, *cap the damage*, *second check*. Each row is the operational claim; underneath, I list the research direction that makes it real. For *keep data local* — benchmark on-prem orchestration models against cloud LLMs on identical traces, so we can measure the cost of on-prem containment instead of just asserting it. For *cap the damage* — formalize blast-radius bounds and test containment primitives (rate limits, kill-switches, scope restrictions) in simulation, so "rate limit" becomes a guarantee instead of a heuristic. For *second check* — measure how multi-agent consensus trades off success rate against latency, because adding reviewers costs seconds per decision and we need the curve, not a claim. This is defense-in-depth applied to agentic orchestration, and AgentEdge already starts from it by separating planning from execution.

### Slide 49 · Future Work 2 · Real-time Infrastructure

The second slide narrows to the two most empirically grounded real-time blockers we hit inside AgentEdge.

On the **left card**, *inference efficiency*. Each orchestration is a chain of LLM calls: observe, plan, revise, critique, actuate, and every call is seconds, not milliseconds. The timeline visual stacks those boxes along the real axis, drops a red dashed real-time-SLA line right through the critic step, and the over-budget bracket sits on the bottom axis past the SLA so you can read the blown budget directly off the timeline. I lead with the strongest direction: *train specialised small models for orchestration*, right-sized world models per decision, the same lesson AERO already proved at the forecasting layer. The second direction is *bring algorithmic planners like ILP into the loop*. Integer linear programming turns planning back into a problem we can solve with decades of operations-research tooling instead of leaving it to free-form reasoning, and our own early experiments look very favorable.

On the **right card**, *tool discovery*. This one is an empirical finding from the thesis itself. Tool-pick accuracy stays flat up to roughly twenty tools and then cliffs. The chart shows exactly that shape, with a highlighted cliff at thirty and an annotated AgentEdge point (three MCP servers, about forty tools) sitting right on the cliff. I also keep the counterintuitive remark the dissertation reports: removing an MCP server sometimes *improved* success. Two directions. First, *filter the tool surface and deliver only task-relevant context* to the agent: semantic retrieval and hierarchical catalogs so the planner sees a focused relevant set rather than the full shelf every turn. Second, *learn tool selection from past traces*, routed by what actually worked in production, not by tool names and descriptions alone. Latency and tool surface are both context-engineering problems, not hardware ones.

### Slide 50 · Future Work 3 · Distributed Ecosystems

The last future-work slide is the one about what happens when we stop talking about a single AgentEdge instance and start talking about fleets of them.

On the **left card**, *multi-agent coordination*. Once we parallelise across regions — the only honest way to scale, because stacking agents in series just stacks latency — independent instances on shared infrastructure will propose contradicting actions. The visual is deliberate: Agent A in region N says consolidate onto node-07, Agent B in region S says power-down node-07, both arrows converge on the same shared node, and the conflict is the red X at the far right — detected only after the fact. The direction is intent-level consensus: lock-lease schemes on *intended* actions before commit, share plans rather than raw state, classic distributed-systems techniques applied to probabilistic planners.

On the **right card**, *model-agnostic design*. This blocker comes straight from the AgentEdge development experience. Swap the LLM provider and the tool calls change shape: provider X returns camelCase JSON, provider Y returns an XML-ish schema, and the same intent suddenly routes through model-specific adapters, prompt re-tuning, and retry regressions — a "glue code" tax that undermines portability. The direction is a canonical intent schema for agent tool-calls, an OpenAPI-equivalent for agentic systems, combined with model-agnostic evaluation. Once that exists, practitioners pick an LLM for cost, latency, and privacy — not compatibility.

Two cards per slide, one visual each, the blocker on top and the direction on the bottom. That is the whole future-work section.

### Slide 51 · Three contributions, one systems thesis

Three claims, each defended with three anchor numbers that were already shown on the result slides, nine anchors in total. Claim one, AERO — eight-times-lower live MAE versus the SOTA small model, roughly a hundred-times fewer SLA misses than a reactive baseline, and all of it in 599 parameters: real-time forecasting fits on the edge, SOTA accuracy, robust under drift, and small enough to deploy anywhere. Claim two, OmniFORE — 30.4 percent lower MAE versus ModernTCN, a 20.7 percent gain from clustering-based training, and zero-shot transfer from Google to Alibaba: one attention model generalises across services, no retraining for each new workload. Claim three, AgentEdge — 1.47 times success twin-on versus twin-off, ten-times-lower API-call variance, and 300.8 watts of rack power reclaimed at eighteen nodes: agentic orchestration with a digital-twin critic is reliable on live infrastructure and saves energy at scale. The closing line captures the thesis: edge-cloud orchestration moves from reactive supervision to a proactive, validated control stack — three layers, nine anchor numbers. That is what I defend.

### Slide 52 · Questions

Thank you. I welcome your questions. The final slide keeps the compact deck guide on the right — sections 1 through 3 by slide range, so the committee can jump directly to framing, a specific contribution, or synthesis — and on the left, the italic line *"the system is zero-touch · the Q and A should definitely not be"* plus my supervisors and the thesis tribunal.

### Backup B1 · AgentEdge S35 result

Use this slide if the committee asks why the 35-node scenario drops to 9.5 percent while the 18-node case reaches 55.5 percent. The answer is context bloat, not an architectural contradiction. The same AgentEdge architecture and the same base model are used at both scales; what changes is the amount of cluster state the LLM must ingest and reason over at once.

The two defenses on the slide are the ones to emphasize. First, larger-context and better-reasoning models will relax this bottleneck without changing the architecture. Second, the current implementation loads the full state naively; compressed state representations, semantic filtering, and retrieval over state can reduce token load sharply while preserving the same PARES design.

### Backup B2 · AgentEdge state staleness

This slide answers the question of what happens if the system state changes between planning and execution. The short answer is that ActSimCrit re-checks live state at the execution gate. The Execution agent queries current infrastructure state immediately before committing actions, so stale plans are caught at the last safe boundary rather than after actuation.

The second half of the slide explains how the residual gap can be reduced further. Faster planning shortens the window in which the system can drift, and the example on the slide is that swapping the planner for a classical optimizer reduced response time from 107 seconds to 48 seconds without changing the architecture. Smaller, more relevant context also reduces state-staleness risk.

### Backup B3 · Adapted baselines

This backup makes the baseline story explicit. ReAct and LATS were adapted to orchestration; they were not taken off the shelf. Both were wrapped in the same orchestration harness as AgentEdge, exposed to the same tool schemas and Kubernetes-facing actions, and run on the same base LLM with the same metric collection.

The second point is why traditional optimization or learning baselines are not direct competitors here. Heuristics, reinforcement learning, and MILP require a formal objective function. Natural-language intent is the input in this thesis, so the fair baseline is another LLM-based decision mechanism operating on the same tool surface.

### Backup B4 · Nearby Computing data scope

Use this slide if the committee asks what Nearby Computing actually contributed and how reproducible the data-dependent parts are. Nearby Computing provided access to the production orchestration platform, live workload traces from real deployments, and the scheduler integration interface used for predictive-versus-reactive comparisons.

The reproducibility line is equally important: service identities were anonymized, only resource and load traces were exposed, and the experimental protocol can be reproduced on any compatible orchestration stack. The value of the contribution is that the evaluation is grounded in realistic traffic, not synthetic replay alone.

### Backup B5 · Utilization citations

This backup supports the utilization and headroom claims from the framing section. The under-40-percent utilization statement is anchored in production studies such as Google Borg, Azure capacity reports, and EC2 usage analyses, which consistently show that clusters keep large reserves to tolerate bursts.

The edge-specific point is that the same headroom logic breaks down on small nodes. Edge hardware operates with one or two orders of magnitude less compute than cloud clusters, so reactive scheduling has much less room to maneuver once bursts arrive.

### Backup B6 · PARES full definition

This is the full form of the PARES capability contract. Perception defines what the agent can observe and is important because it bounds context instead of allowing the prompt to grow without limit. Action defines the typed tool surface at the orchestration boundary. Reasoning is the scoped decision process used inside each specialized agent.

Evaluation is the explicit judgment step, implemented in AgentEdge through critique and validation before execution. Sustained operation covers stability over noisy, long-running production conditions. If asked why some prior systems are not considered true agents in this thesis, this is the formal answer.

### Backup B7 · Full publications

This backup is only the full bibliographic record, grouped by contribution color. It is the slide to open if the committee asks for venues, publication titles, or DOI-level detail. The publications are split across AERO, OmniFORE, and AgentEdge, with the book chapter kept separate because it is not one of the three core thesis contributions.

The speaking strategy here should stay short: state the totals shown on the slide, point to the color grouping, and only go into a specific venue or paper title if the committee asks for it.

### Backup B8 · Execution agent

This slide expands the Execution agent because the main talk treats it as a typed executor rather than a reasoning-heavy component. Its input is an approved action sequence plus current infrastructure state. Its action surface is Kubernetes calls, orchestrator hooks, and rollback primitives. Its evaluation step is a post-execution state difference: did the infrastructure reach the intended state?

The main conceptual point is the feedback loop. On failure, the Execution agent rolls back where possible, records success or failure traces, and returns that context to Planning. That is what closes ActSimCrit across multiple turns without re-triggering the full pipeline from intent parsing onward.

### Backup B9 · OmniFORE deployment granularity

This backup gives the clean answer to the question of where OmniFORE can run. OmniFORE is layer-agnostic by design. The research problem is generalization across services, not committing to a specific infrastructure tier. Placement is therefore an operator decision rather than a thesis constraint.

The slide lays out the three natural options. Far-edge deployment is possible where there is enough memory, such as stronger aggregation nodes. Regional deployment is the most natural setting and is what the evaluation uses. Cloud deployment also works for longer forecast horizons. The one-line answer is that the research question is solved before placement is chosen.

### Backup B10 · Why 78.3%, not 100%?

This slide is for the inevitable question about why AgentEdge does not reach perfect success even with a digital twin. The short answer is that the twin is a gate, not an oracle. It removes a large class of unsafe plans, but three residual failure modes remain: mismatch between the twin and the live system, imperfect critic recall, and refinement-budget cut-off after too many rejections.

The framing sentence at the bottom is the key one to keep ready: 78.3 percent is still the first validated success metric in this setting. Earlier baselines either cannot be measured consistently or succeed only by committing invalid plans. The important point is that the remaining failure modes are known and scoped, not hidden.

### Backup B11 · 6G service mix

This backup answers the bait question about what kinds of services 6G will actually carry. The thesis takes a deliberately non-committal stance on service mix because the orchestration contract is the same regardless of payload. The important split is between network-plane workloads and application-plane workloads, and both appear on the slide.

Examples on the network side include O-RAN control functions, UPF or SMF control, slice management, and MEC sidecars. Examples on the application side include XR streaming, V2X loops, federated inference, industrial control, and health telemetry. The architectural claim is payload-agnostic: forecast, generalize, and act safely no matter which service family is being orchestrated.

### Backup B12 · Informer vs Pathformer vs AERO

Use this slide to separate three concepts that are easy to conflate in Q&A. Informer-family models belong to the broader attention-mechanism discussion and appear in the magazine survey context; they are not the core AERO baseline. Pathformer is the main AERO comparison baseline because it represents the current small-ish accurate forecasting frontier, but it still overshoots far-edge deployment budgets.

AERO's claim is therefore not raw MAE dominance over every transformer. The claim is matching operational forecasting quality while staying tiny enough to deploy at the far edge. That is why this slide says roles, not rankings.

### Backup B13 · AERO beyond workload traces

This backup answers whether AERO can be reused beyond CPU or memory forecasting. The answer is yes for any univariate time series with learnable periodicity. The architectural contract is observe, detect periodic structure, and forecast; that does not depend on the signal being a workload trace specifically.

The slide gives examples across the 6G stack: physical resource-block utilization, MCS distributions, active connections, UPF throughput, session setup rates, service request rates, latency percentiles, byte rates, and handover rates. The caveat is also important: if the signal is not periodic enough, then OmniFORE is the more natural candidate.
