### Slide 01 · Title

Good morning. I am Berend Jelmer Dirk Gort, and today I defend my doctoral thesis, *AI-Driven Zero-Touch Orchestration of Edge-Cloud Services*, within the Doctoral Program in Signal Theory and Telecommunications at Universitat Politècnica de Catalunya. The work was supervised by Dr. Angelos Antonopoulos at Nearby Computing and co-supervised by Associate Professor Dra. Anna Umbert at UPC.

It was developed with Nearby Computing as the industrial partner, which matters because the contributions you will see today were exercised against real infrastructure rather than only offline benchmarks.

### Slide 02 · From framing to validated autonomy

The defense follows a five-part path. I start with framing, then move through the three contributions in order: AERO, OmniFORE, and AgentEdge, and I close with a synthesis. The color code is consistent throughout the deck: blue for AERO, orange for OmniFORE, and pink for AgentEdge.

The purpose of this slide is simply to give the committee the map before I start spending numbers.

### Slide 03 · Manual reality today

This is the operator stack as it exists today. At layer one the operator can express intent, but still has to inspect the system manually. At layer two there is no intelligent path from natural-language intent to orchestration action. At layer three the prediction layer fails in two different ways: at the far edge there are no accurate per-node forecasts, and in larger compute sites a new model must be refit for every service.

The far-edge box now makes the motivation explicit: prediction matters because actions must be chosen before SLA and energy drift become irreversible. Layer four is the given environment: heterogeneous far-edge nodes, regional clusters, and the cloud. Four layers, four open problems, one operator holding the loop together.

### Slide 04 · Zero-touch: operator sets intent, not actions

The goal is zero-touch: operator sets intent, not actions. Goals, SLAs, and constraints go in; orchestration decisions come out. The left-hand loop is the control cycle: predict, decide, act, observe. Forecasts drive decisions, decisions are executed, the new state is observed, and fresh traces feed the next round. Human review should happen only on exceptions.

The right-hand figure explains why prediction is load-bearing. The black line is demand, and the red staircase is reactive capacity. When demand rises, reactive control scales up late, so the system spends time under-provisioned and accumulates SLA violations. When demand falls, reactive control scales down late, so the system keeps idle capacity online and wastes energy. The dashed blue curve is predictive control: capacity is in place when the spike arrives and released when it leaves. Prediction closes both gaps, which is why two of the three thesis contributions land in the predict stage.

### Slide 05 · Forecasting must run where the service runs

As the first sub-problem, prediction at the far edge is a deployability problem. Today's SOTA baseline is a 2.4-million-parameter transformer: accurate, but too large for small edge hardware. Lightweight alternatives around fifty thousand parameters fit the device budget, but their accuracy collapses under drift.

That leaves an unfilled deployability gap: small and accurate at the same time. This becomes research question one: can workload prediction remain practical and accurate at edge scale? The target I set up-front is below one thousand parameters with competitive accuracy.

### Slide 06 · One model for many services

The second sub-problem is generalization. Even if edge prediction works, the default practice is still one model per service, and that cost scales linearly with the catalogue. Each new service or drift event means retraining, monitoring, and maintenance all over again.

At 6G scale a typical operator can easily manage hundreds of microservices, so the real barrier is not inference cost but retraining burden. Research question two therefore becomes: can one forecasting framework cover heterogeneous service workloads without per-service retraining?

### Slide 07 · From natural-language intent to intelligent orchestration action

The third and fourth problems belong to the decision layer. The operator can already state intent in natural language, for example, *"reduce energy while keeping SLA"*, but the bridge from that sentence to concrete orchestration commands is still a human. The operator reads dashboards, chooses services, chooses targets, and executes commands like drain, scale, migrate, or power-off.

That means the control loop scales with human attention rather than workload. The decision layer therefore has to do two things at once: understand intent and act on it safely. That is the combined research question behind AgentEdge and the real meaning of zero-touch.

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

### Slide 12 · How AERO works in three steps

AERO's mechanism is intentionally simple on this slide. Step one is to find the rhythm: the repeating pattern in the trace can change over time, so AERO re-checks it every window. Step two is to align first: once the rhythm is known, the repeated cycles are lined up so a small predictor can work on organized structure rather than raw disorder. Step three is to reuse cached layers: when the same pattern returns, the same block can be reused instead of recomputed from scratch.

The big idea is that AERO makes the signal easier before it asks a tiny model to forecast it.

### Slide 13 · Scenario 1 - Workload Prediction

This is now the proper scenario slide for the efficiency benchmark. The dataset is the Alibaba 2022 microservices trace, specifically pod MS_11349, with 18,720 one-minute samples across thirteen days and two normalized features: CPU and memory. The benchmark set is five baselines plus AERO.

All models are trained on the same server: NVIDIA A100 40 GB, 30 CPU cores, 200 GiB RAM, 512 GiB SSD, Ubuntu 20.04.2, using Python and PyTorch. Hyperparameters are tuned with Bayesian optimization using twenty random trials and thirty refinement trials per model. The reported outputs are MAE, RMSE, latency, convergence, parameter count, and memory. In other words, this slide fixes the exact setup before I show the efficiency result.

### Slide 14 · Only AERO is both small enough and accurate enough

Three columns, one conclusion. In parameter count, AERO has 599 parameters, while the heavy baselines range from 228 thousand up to 2.9 million. SparseTSF is smaller at 35 parameters, but size alone is not the goal. In inference latency, AERO is at 0.38 milliseconds, well inside the 50-millisecond budget; even Pathformer stays at 0.52 milliseconds, but it does so with a far larger model. In MAE, AERO reaches 2.9 times ten to the minus four, essentially on par with ModernTCN and close to Pathformer.

So the title is the takeaway: only AERO is simultaneously small enough to deploy and accurate enough to matter.

### Slide 15 · Scenario 2 - Orchestration outcomes

Now I move from forecasting quality to control impact. The simulator is COSCO on AzureFog: 50 heterogeneous hosts, sixty percent edge and forty percent cloud, with 3-millisecond edge latency, 76-millisecond cloud latency, and 5-gigabit links. The run lasts 2,000 cycles at 300 milliseconds, with 50 containers and 4 arrivals per step.

Forecast inputs come from the BitBrains Random trace: 500 VM traces, 8,631 samples, and seven workload signals. The compared arms are AERO, Pathformer, SparseTSF, and a reactive controller that bypasses prediction. Same scheduler, same workload stream, same objective of minimizing energy plus response time; only the forecast quality changes.

### Slide 16 · Simulation results under controlled edge-cloud environment

The result slide uses four operational metrics. Energy is 1293 joules for the reactive baseline, 1140 for SparseTSF, and 1123 for both AERO and Pathformer. Response time falls from 10.02 seconds for reactive to 6.5 for SparseTSF, 3.29 for AERO, and 2.45 for Pathformer. SLA violations collapse from 22.21 percent reactive to 4.60 percent with SparseTSF, 0.21 percent with AERO, and 0.10 percent with Pathformer.

Task migrations increase because predictive schedulers act before overloads appear: 2,026 for reactive, 5,309 for SparseTSF, 7,747 for AERO, and 8,480 for Pathformer. The honest interpretation is that AERO stays close to Pathformer while clearly outperforming SparseTSF and reactive orchestration.

### Slide 17 · Scenario 3 - Live deployment

The final AERO test is live deployment. The training source is a Google Cluster trace with T equal to 8,930 samples, four features, and five-minute resolution. Both AERO and SparseTSF are trained with the same setup and hyperparameter search, then deployed as microservices on a physical testbed: i9-9900K, 46 GB RAM, RTX 2060, Ubuntu 24.04.1, using Docker Compose.

On the held-out test split the two models look almost indistinguishable; the live unseen workload is where drift exposes the difference. The live evaluation reports normalized MAE, RMSE, and mean inference time under the 50-millisecond real-time threshold.

### Slide 18 · Live deployment results under real-world drift

This slide now stays on the live deployment numbers only. On the unseen live workload, AERO reaches a mean absolute error of 0.051, while SparseTSF reaches 0.411, about eight times higher. RMSE tells the same story: 0.079 for AERO and 0.430 for SparseTSF. Inference is 2.65 milliseconds for AERO and 1.12 milliseconds for SparseTSF, so both remain comfortably within the 50-millisecond scheduler budget.

The point is that latency is not the differentiator; drift robustness is. That is why the operator-impact footer still matters: roughly fifteen percent lower response time and twelve percent lower energy once the model stays accurate in the live environment.

### Slide 19 · OmniFORE

Contribution two is OmniFORE: one forecasting framework, all services. The banner separates the claim from the goal. The claim is that models exist that can predict any trace. The goal is stronger and more operational: one model that can process all workload traces.

The concrete promise I test next is zero-shot prediction on services the model never saw during training, up to cross-dataset transfer with frozen weights.

### Slide 20 · Train on a service catalogue, forecast any service in it

This slide states the OmniFORE problem in operator terms. I want one model trained once on a service catalogue and then able to forecast any service in that catalogue, including services it has never seen. The visual contrast is between bursty and steady families, because the model has to cover both without separate retraining.

Formally, the goal is one shared set of weights, no per-service fine-tuning, and average prediction error minimized across all services, seen and unseen. That is the only path by which the prediction layer actually scales operationally.

### Slide 21 · System Model - one model, many services

Again this is the generic setting, not the method. On the left, one prediction layer observes many service traces at a compute site, which could be any tier, and returns per-service forecasts into the same downstream decision stack. On the right, the motivation is operational cost.

Today each site tends to carry its own forecasting model copy. As the number of sites grows, retraining, memory, and monitoring repeat everywhere. The target is one shared model that can serve many sites and many services, instead of duplicating the machine-learning workload at every location.

### Slide 22 · State-of-the-Art - no prior method lives in the top-right

The prior work again falls into two red regimes around one green target. The first red regime is per-service retraining: ModernTCN, AGCRN, and LSTNet can work well on the service they saw, but every new service needs a new model. The second red regime is generic but heavy: foundation models promise reuse, but are too heavy and too generic to be the deployable workload layer.

The top-right quadrant, one model with unseen-service accuracy, is still empty. OmniFORE is designed to occupy that gap.

### Slide 23 · How OmniFORE generalizes in three phases

This slide packages the OmniFORE pipeline. Phase one, stages S1 through S4, designs the training set by encoding traces, clustering shapes, and sampling a balanced catalogue. Phase two, stages S5 and S6, rescales each service and then uses attention over a shared window so one model can learn across heterogeneous services. Phase three, stage S7, tunes hyperparameters on held-out services so the selected setting is rewarded for transfer rather than memorization.

The message is that generalization comes from the whole pipeline: representative data, shared training, and transfer-focused tuning.

### Slide 24 · Designing the training set

This slide zooms into phase one. S1 fingerprints each trace by compressing it into a shape descriptor. S2 clusters those fingerprints into bursty, steady, and periodic families. S3 tags every trace with its group label. S4 samples proportionally from those groups to build a balanced mix.

The point is that representativeness is engineered before training begins, so the model later sees the catalogue in balanced form instead of allowing one family to dominate the dataset.

### Slide 25 · Training the model

Phase two has two steps. S5 is equal scale: raw services arrive at very different magnitudes, so each trace is rescaled so that large services do not drown out small ones. Every workload gets an equal say in training. S6 is efficient attention: for each forecast step the model scans the full recent window and keeps the strongest matches.

That matters because the model generalizes by matching patterns rather than service identity. After rescaling, those patterns can transfer to services it has never seen.

### Slide 26 · Tuning so it transfers

Phase three is the single S₇ stage: tune so it transfers. Bayesian optimisation scans the hyperparameter space with a Gaussian-process surrogate and an acquisition function that picks the next configuration to try. The critical design decision is what we *score* each configuration against. The usual practice is to score against the training distribution, which rewards memorising the training set. OmniFORE scores against a held-out batch of services that was kept out of training entirely, so the optimiser is rewarded for choosing hyperparameters that work on services the model has never seen. Generalisation is enforced at the optimiser level, not only at the dataset level.

### Slide 27 · Does picking smart training data really help?

The first experiment is an ablation on the pipeline itself. Version A is the OmniFORE way — one representative trace per cluster, selected from bursty, steady, and periodic families. Version B is a random baseline — one hundred traces drawn at random from the catalogue. Everything else is held fixed: same model, same tuning, same test services. Only the training traces differ. The reason this experiment is worth running is that it isolates the training-set design from the model, so any difference in the results is attributable to the pipeline, not to the head.

### Slide 28 · Smart picking wins by about twenty percent, on every metric

The numbers are consistent across error metrics. Mean absolute error improves by 20.66 percent, root-mean-square error by 24.63 percent, and symmetric mean absolute percentage error by 32.71 percent. And the silhouette score, which measures whether the clusters are structurally meaningful rather than arbitrary, is 131.8 percent higher with the OmniFORE grouping, which tells us the clusters have real structure to exploit and the model is not simply memorising. The finding is that clustering-based training yields real, attributable gains on every metric we care about. The next experiment pushes this further by asking whether the gain survives a dataset the model has literally never seen.

### Slide 29 · Test it on a dataset it has never seen

The second experiment is the hardest test a forecaster can run: train on Google Borg cells A through F, freeze the weights, and evaluate on Alibaba Cloud 2022 — specifically pod MS_11349. No retraining, no fine-tuning, different cloud provider, different workload mix. The three strips on-slide call out exactly what is different between the two environments, and the italic line on the slide is honest about what usually happens here: *this is where benchmark wins usually fall apart*. If the model generalises, it has to generalise without our help.

### Slide 30 · Predicts any new service effectively, no retraining needed

The hero number on the slide is a mean absolute error of 7.27 times ten to the minus three on the unseen Alibaba pod. Against the same task, ModernTCN reports 10.45 — OmniFORE is 30.41 percent better. AGCRN reports 28.70 — we are 74.67 percent better. LSTNet reports 47.51 — we are 84.70 percent better. The finding banner is that OmniFORE predicts any new service effectively, with no retraining, with frozen weights, on a dataset it has never seen. The patterns it learned are not tied to Google; they generalise. That is research question two answered: one framework generalises across heterogeneous services, and the cost of adding a new service is zero. With prediction now both deployable at the edge and generalisable across services, the last piece of the zero-touch loop is validated action, which is AgentEdge.

### Slide 31 · AgentEdge

Contribution three is AgentEdge: natural-language intent becomes validated autonomous action. The one-line claim on the banner is that a multi-agent LLM design, with validation before execution, beats single-agent and tree-search baselines — quantified on-slide at more than seventy-five percent success. The keywords I want on the record from this slide forward are multi-agent, tool-use, multi-step reasoning, and digital-twin validation. Those are the technical anchors for everything in the rest of this section.

### Slide 32 · No system can turn operator intent into orchestration actions

The problem AgentEdge solves is visible on the diagram. The operator types *"reduce energy while keeping SLA"*, and on the far right of the diagram sit the concrete cluster actions — scale, migrate, switch to low-power. The middle of the diagram, today, is a question mark. There is no system that can take that sentence and produce a correct action sequence. The slide gives three reasons why: intent is ambiguous, because natural language underspecifies what to do; actions are irreversible, because draining a node or migrating a service cannot be undone cleanly; and state is distributed, because the information needed to decide well is spread across the cluster. An agent that wants to close this gap must handle all three at once.

### Slide 33 · System model — operator to orchestration stack

This slide is the generic stack, not the AgentEdge architecture yet. The left column shows the layers: operator intent at the top, a decision layer beneath it, then supporting signals, the service-orchestration interface, and finally the infrastructure itself. The large diagram on the right turns that stack into a loop. Intent comes down from the operator, the decision layer must combine meaning and cluster state, supporting forecasts and checks can be queried underneath, and only then does a validated action flow through Kubernetes into the infrastructure. So the point of this slide is to pin down the interfaces and the missing capability: something has to sit between natural-language intent and typed orchestration actions. The following slides introduce the actual design that fills that gap.

### Slide 34 · PARES — the capability contract

Before the state of the art, a short aside on what I mean by *agent* in this thesis. Prior systems are described in prose; impossible to compare. PARES is the capability contract I use throughout: Perceive the cluster state, Act through typed tools, Reason explicitly over the goal, Evaluate candidate plans before committing, Sustain across multi-step interactions. Separate agents specialise; no single LLM carries every role. The framework is built on a general orchestration library, not a monolithic script. This is the grid I use to compare prior work on the next slide.

### Slide 35 · Every prior system is missing load-bearing capabilities

The state of the art is a capability matrix. Nine capabilities run across the top — things like natural-language intent translation, wireless-agent awareness, fault handling, chain-of-agent reasoning, multi-agent coordination, service orchestration, cross-layer span, pre-execution validation, and PARES. Every prior system I benchmarked is missing at least one load-bearing column. The three differentiators I want the committee to focus on are the three where no prior system delivers at all: spanning edge-plus-cloud, validating before acting, and filling the PARES capability contract. That PARES column has zero prior entries. One honest question that comes up here is *why ReAct and LATS as baselines, if none of them satisfies PARES?* No prior system does, across the full orchestration cycle. We therefore adapted ReAct, the reason-act loop, and LATS, tree-search over LLM rollouts, by retargeting them onto our tool surface: same tools, same base LLM, same scenarios, so comparison is fair. The bottom line on-slide is simple: only AgentEdge is full-row green.

### Slide 36 · Each pain-point forces exactly one design decision

The rationale table has four rows, and each row is the minimal response to one specific pain-point. Ambiguous natural-language intent forces a dedicated Intent agent whose only job is to parse operator sentences into structured goals. A large, distributed state forces an Observability agent with tool-use and a bounded world model, so the system does not drown in raw telemetry. The fact that plans break in complex environments forces ActSimCrit — Plan, Simulate, Critique — which validates candidate plans before execution. The fact that actions are irreversible on live infrastructure forces a digital-twin sandbox where the simulation happens. The line the slide leaves with the committee is that each of these four is load-bearing: drop any one of them and the system fails predictably in a way that can be traced to the missing piece.

### Slide 37 · Graph-of-graphs, four specialised agents

The architecture is a graph of graphs. Outer structure is sequential — start, Intent, Observability, Planning, Infra Action, end — and each of those four agents is itself a small subgraph with its own internal reasoning steps. On top of that, every agent satisfies the PARES capability contract: Perceive, Act, Reason, Evaluate, Sustain — the five capabilities that define what it means to be an agent in this framework rather than a prompt chain. The agentic-spectrum note on the slide places this design deliberately: it is specialised enough to be debuggable, but not so rigid that it reduces to a pipeline.

### Slide 38 · How the agent reads intent and observes the cluster

This slide shows the two perception agents with concrete examples. The Intent agent takes an operator sentence and returns structured JSON. On-slide it reads as a rebalance goal from node three to node five, subject to an SLA constraint and an energy-savings floor of fifteen percent. The Observability agent takes the bounded infrastructure context and returns a typed snapshot: per-node metrics plus an SLA object with p99 latency of 118 milliseconds and an error budget used at 0.70. Perception is a bounded world model plus a typed intent parse, not free-form chatter. That is what makes the rest of the pipeline debuggable.

### Slide 39 · How the agent plans, simulates, and executes safely

This is the core of AgentEdge. The Planning agent runs a five-phase loop: strategic planning, state analysis, action selection, digital-twin simulation with a critic, and a check on whether the intent is satisfied. If the critic rejects the simulated outcome, control returns to action selection rather than being committed to the cluster. Four technical mechanisms sit underneath that loop: tool-call batching, a three-tier state representation, rejection-feedback on failed plans, and deadlock detection. The example JSON at the bottom of the slide shows the output of a successful cycle — a plan object with `validated: true`, an energy delta of minus eighteen percent, and SLA preserved. Nothing reaches the cluster until that object exists. Validation before execution is structural, not a post-hoc check.

### Slide 40 · Infrastructure simulator, testbed for safe agent evaluation

The simulator does two jobs at once. At runtime, it is the digital twin that the Planning agent uses inside ActSimCrit to validate a proposed tool-call batch before anything is committed. As an evaluation harness, it is the controlled environment where all three AgentEdge experiments run. The tier table on-slide names the three levels — far edge, near edge, cloud — with per-tier node counts, CPU and memory, power envelopes, latency, and the sixty-percent low-power saving applied in each tier. The twelve API endpoints — deploy, migrate, scale, low-power, status, and seven others — are listed as chips, and the simulator is explicit about its stochastic timing, its 0.1-to-2-percent failure probability, and its real-time validation. The bottom line on-slide — *same infrastructure, same LLM, same tools, only architecture varies* — is the fairness guarantee that makes the next three experiments comparable.

### Slide 41 · Does the multi-agent design outperform single-agent baselines?

The first AgentEdge experiment is an architecture-versus-architecture comparison. Three scenarios are specified on-slide: S1 is a full-node reallocation task; S2 is a low-power conflict where multiple constraints compete; S3 is a compound-constraint task with a measured 0.52-core deficit that forces the agent to reason across services. Success is defined by predefined valid end-states, and we run thirty trials per scenario per system, reporting the percent success rate. The three arms are AgentEdge with four agents and the twin, ReAct — the reason-act loop — and LATS, which is tree-search over LLM rollouts. Critically, all three arms run on the same base LLM, `qwen3-235B-A22B` at temperature 0.2, so any difference between them is attributable to architecture, not to model capability.

### Slide 42 · Multi-agent architecture beats every SOTA single-agent baseline

The numbers are clean. AgentEdge succeeds on 78.3 percent of trials. LATS succeeds on 65.0 percent. ReAct succeeds on 28.3 percent. As multipliers, which are stickier than raw percentages, that is 1.20 times LATS and 2.76 times ReAct. The finding banner is direct: multi-agent architecture beats every SOTA single-agent baseline, on the same LLM, on the same tasks, in the same simulator. The next experiment takes the next obvious question — is this gain really coming from the digital twin, or from the four-agent structure alone?

### Slide 43 · Is the twin structural or decorative?

The ablation turns the digital twin on and off and holds everything else constant. The *WITH* arm is the full AgentEdge — Plan, Simulate, Critique, Execute. The *WITHOUT* arm runs the same four agents, with planning and critique, but strips out the simulation step so the critic has no simulated trajectory to evaluate. Let me be precise about what "WITHOUT" means here, because this is a question that often comes up: on a Crit failure the plan is refined *in place* by the Exec agent; no round-trip back to Planning. In other words, the twin's contribution is isolated as *pre-execution validation*, not as the existence of a retry mechanism at all. The Q&A anticipation on-slide is the related point: the twin does not change *whether* a plan can succeed, it changes *how many physical retries* it takes. We report both success rate and API-call count, so failure-shifting cannot hide behind either metric alone.

### Slide 44 · Sandbox validation reduces costly trial-and-error

The ablation tells a very direct story. With the twin, success is 78.3 percent; without it, success drops to 53.3 percent — a 1.47 times improvement. The more operational number is API behaviour. With the twin, API-call counts stay tight at 10.9 with a standard deviation of 1.1. Without the twin, they range from eight to five-hundred-and-seventeen with a standard deviation of 109.4 — about ten times higher variability. Without simulation, the agent enters unproductive retry loops that are not just slower; they are operationally unsafe, because every retry touches production. The twin is therefore structural: it lifts success *and* collapses variance. The last experiment asks how this behaviour changes as the infrastructure grows.

### Slide 45 · Does the agent keep saving energy as infrastructure grows?

The scalability experiment asks a practical question: does AgentEdge keep saving energy as the infrastructure grows? The three scales on the slide are eight nodes, twenty nodes, and thirty-five nodes. The task is the same at each size — consolidate energy while preserving the SLA. The main metric is power saved in watts, and each number is also contextualised on-slide as a percentage of baseline rack power, so it is not just a floating watt figure. Response time is shown alongside it, because AgentEdge is strategic orchestration, not a fast control loop.

### Slide 46 · Energy saved vs baseline — twenty nodes is the peak

Three bars, three findings, and one shared scale across all scales. At eight nodes, AgentEdge saves 89 watts, a 20.6 percent efficiency gain. At twenty nodes, it saves 300.8 watts, a 55.5 percent gain — the peak, and the one I want the committee to remember. At thirty-five nodes, it saves 185.2 watts, a 9.5 percent gain. A reasonable follow-up is *why does twenty beat thirty-five?* The honest answer on-slide is that it is a context-window artefact, not a fundamental limit; the full node state overflows the prompt. With summarisation or sharding, the gain would continue to scale. The shared y-axis and ten runs per scale make these numbers directly comparable. Response time still grows with infrastructure size, which is exactly why real-time agent infrastructure appears again in future work. The key claim on this slide is not that scale is free; it is that validated autonomy remains useful and energy-relevant at production scale, and that the peak is explained rather than hidden.

### Slide 47 · State-of-the-art operator stack

This is the payoff slide. The same four-layer stack we started with on slide three, now populated with the three contributions and their anchor numbers. Layer one, the operator, is now handled by AgentEdge — the operator sets intent and reviews exceptions only, instead of driving the stack by hand. Layer two, decision, is also AgentEdge — natural-language intent becomes validated orchestration action, with a 78.3 percent success rate over sixty runs and a 55.5 percent energy saving at eighteen nodes. Layer three, prediction, is shared between two contributions: AERO at the far edge with 599 parameters and 0.38-millisecond inference, and OmniFORE as the shared cross-service predictor with 30.41 percent lower cross-dataset error and zero-shot deployment to new services. Layer four and five, service orchestration and infrastructure, are the given environment — no dissertation contribution, but the one the other three now serve well. Operator impact folds in at this level: repeated manual intervention becomes exception review, actions become traceable via simulation-backed reasoning, and safety and optimisation sit together in one loop. Eight publications, colour-coded by contribution, the full list is on backup slide B7.

### Slide 48 · Future work · agentic era

The same stack appears one more time, but now layers three and four are dimmed and explicitly marked *solved*, while layer one and layer two stay lit. The message is that the open frontier is now at the agentic layers, not at the predictor. Three future challenges follow, each with its own slide: reliability and trust, real-time agent infrastructure, and distributed orchestration ecosystems. AgentEdge works, but three new challenges emerge once it leaves the lab and starts operating at production scale.

### Slide 49 · Benchmarks do not exist yet

Let me start with the first trust problem: benchmarking. At the moment, we simply do not have benchmark suites for agentic orchestration, and without them developers cannot know whether a change helps or hurts. The reason this is hard is that these tasks rarely have one ground-truth label; several plans can be valid at once. On top of that, LLM non-determinism means a fix that improves one scenario can break another. And if we had good benchmark data, it would not only improve evaluation, it would also enable fine-tuning smaller, orchestration-specific models. So trust begins with evaluation engineering. Before these systems can be deployed confidently, the field needs shared test suites, and research should characterise *equivalence classes* of correct orchestration plans; expand LLM evaluation theory into orchestration; and build orchestration-trace datasets — plan, state, outcome — that enable small LoRA/SFT models that are cheaper and easier to audit.

### Slide 50 · Latencies accumulate to tens of seconds

The second barrier is real-time performance. Even simple orchestration tasks can take tens of seconds because the planner iterates, calls tools, revises, and reasons again, and token costs compound at scale. This is ultimately a context-engineering problem, not a hardware one. The three barriers on this slide: first, the state the agent sees when reasoning starts may already differ by the time it executes. Second, accuracy drops once the tool surface gets too large — in our experiments, beyond roughly thirty tools, and in some cases removing tools actually improved results. Third, latency points toward the same lesson AERO taught us at the prediction layer: smaller, fine-tuned models may be the only practical way to break the latency barrier. State summarisation, tool sharding, retrieval-over-state; specialised models per decision — scale, migrate, placement; and, further out, agent loops fused with the RAN and core on sub-millisecond radio loops, unifying signal-theory timing budgets with LLM inference budgets.

### Slide 51 · Parallel instances conflict on shared infra

The third direction is system architecture at scale. Once orchestration is deployed across regions, providers, or administrative domains, the problem is no longer one agent in one cluster; it is many agent instances acting on shared infrastructure. The slide gives three open questions. First, the same prompt routed through a different model or provider can break because the output format shifts; we need an OpenAPI-equivalent for agent tool-calls, so that swapping provider X for provider Y preserves agent behaviour. Second, consensus or lock-lease schemes for *intended* actions, so conflicts are detected *before* actuation, not after. And third, scaling will come from parallelising across regions, not from adding more agents in sequence. Without these protocols, one agent may consolidate onto a node while another powers it down.

### Slide 52 · Three layers · one systems thesis

Three claims, each defended with three anchor numbers, nine anchors in total. Claim one, AERO — 599 parameters, eight-times-lower error under drift, and fifty-percent fewer migrations than SOTA: edge-real-time prediction is feasible with a sub-one-thousand-parameter model, with accuracy preserved. Claim two, OmniFORE — 30.41 percent lower MAE versus ModernTCN, a 20.66 percent MAE gain from clustering, and zero-shot deployment on an unseen cloud: a single attention-based model generalises across services, no per-service retraining. Claim three, AgentEdge — 1.47 times twin-on versus twin-off, ten-times-lower API-call variance, and 300.8 watts peak savings at eighteen nodes: validated autonomous orchestration — planning plus twin plus critic — is reliable and saves energy. The banner quote captures the thesis in one line: *orchestration turned from reactive supervision into a proactive, validated control stack; across three layers, with nine anchor numbers to defend it.* That is what I defend.

### Slide 53 · Questions

Thank you. I welcome your questions on the three flagged topics — deployability, generalisation, and validated autonomy — and on the three neutrals — baselines, evaluation methodology, and future work. I hand the floor.

### Backup B1 · AgentEdge S35 result

Use this slide if the committee asks why the 35-node scenario drops to 9.5 percent while the medium-scale case peaks much higher. The answer is context bloat, not an architectural contradiction. The same AgentEdge architecture and the same base model are used; what changes is the amount of cluster state the LLM must ingest and reason over at once.

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
