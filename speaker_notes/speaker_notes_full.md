### Slide 01 · Title

Good morning. I am Berend Jelmer Dirk Gort, and today I defend my doctoral thesis, *AI-Driven Zero-Touch Orchestration of Edge-Cloud Services*, within the Doctoral Program in Signal Theory and Telecommunications at Universitat Politècnica de Catalunya. The work was supervised by Dr. Angelos Antonopoulos at Nearby Computing and co-supervised by Associate Professor Dra. Anna Umbert at UPC.

It was developed with Nearby Computing as the industrial partner, which matters because the contributions you will see today were exercised against real infrastructure rather than only offline benchmarks.

### Slide 02 · Defense outline

The defense follows a five-part path. I start with framing, then move through the three contributions in order: AERO, OmniFORE, and AgentEdge, and I close with a synthesis. The color code is consistent throughout the deck: blue for AERO, orange for OmniFORE, and pink for AgentEdge.

The point of this slide is simply to fix the map before the evidence starts: framing first, then the three contributions, then synthesis.

### Slide 03 · Manual reality today

This slide defines the contract we want at the top of the stack: the network operations team, meaning the humans who run the infrastructure today, should set intent, and the loop should do the rest with human review only on exceptions. The reason that contract is still a problem, marked here as Problem 4, is that the layers underneath do not yet support it.

At layer two there is no intelligent path from natural-language intent to orchestration action, so the operations team still ends up bridging the gap manually. At layer three the prediction layer fails in two different ways: at the far edge there are no accurate per-node forecasts, and in larger compute sites a new model must be refit for every service. Layer four is the given environment: heterogeneous far-edge nodes, regional clusters, and the cloud. Four layers, four open problems, one stack that still does not close the loop.

### Slide 04 · Zero-touch: operator sets intent, not actions

The goal is zero-touch: operator sets intent, not actions. Goals, SLAs, and constraints go in; orchestration decisions come out. The left-hand loop is the control cycle: predict, decide, act, observe. Forecasts drive decisions, decisions are executed, the new state is observed, and fresh traces feed the next round. Human review should happen only on exceptions.

The right-hand figure explains why prediction is load-bearing. The black line is demand, and the red staircase is reactive capacity. When demand rises, reactive control scales up late, so the system spends time under-provisioned and accumulates SLA violations. When demand falls, reactive control scales down late, so the system keeps idle capacity online and wastes energy. The dashed blue curve is predictive control: capacity is in place when the spike arrives and released when it leaves. Prediction closes both gaps, which is why two of the three thesis contributions land in the predict stage.

### Slide 05 · Forecasting must run where the service runs

The first sub-problem is a deployability problem at the far edge. Microcontroller-class edge hardware typically gives us about 256 kilobytes of SRAM to work with, so the slide frames a simple constraint: forecasting has to fit where the service runs. Large accurate models are too big for that environment, while lightweight alternatives still collapse under drift.

That leaves the deployability gap (small and accurate at the same time) unfilled. Research question one follows directly, framed as an open research question rather than a yes/no: how can workload prediction be made both deployable and accurate at edge scale? The quantitative target I fix up-front is below one thousand parameters with competitive accuracy. At fp32 that is about four kilobytes, which sits comfortably inside the 256-kilobyte budget. The goal is not to shrink for its own sake, but to fit with headroom.

### Slide 06 · One model for many services

The second sub-problem is generalization. Even if edge prediction works, the default practice is still one model per service, and that cost scales linearly with the catalogue. Each new service or drift event means retraining, monitoring, and maintenance all over again.

At 6G scale that quickly becomes a three-hundred-plus-service problem. On the slide I now anchor that scale cue with Syamkumar, Barford, and Durairajan, whose MEC deployment study shows operator-scale edge footprints already spanning hundreds of sites and far larger national baselines. So the real barrier is not inference cost but retraining burden. Research question two therefore becomes, framed openly: how can one forecasting framework be designed to cover heterogeneous service workloads without per-service retraining?

### Slide 07 · From natural-language intent to intelligent orchestration action

The third and fourth problems belong to the decision layer. The operator can already state intent in natural language, for example, *"reduce energy while keeping SLA"*, but that input does not map cleanly onto classical heuristics or fixed objective functions. Today the bridge is still a human who reads dashboards, chooses services, chooses targets, and executes commands like drain, scale, migrate, or power-off.

That means the control loop still scales with human attention rather than workload. Zero-touch at this layer means two abilities together: understand intent and turn it into safe orchestration action without a person translating each step by hand.

### Slide 08 · One orchestration stack that predicts, generalizes, and acts on intent

These four problems collapse into three research questions, three objectives, and three contributions. Research question one becomes objective one and contribution one, AERO: deployable edge prediction. Research question two becomes objective two and contribution two, OmniFORE: cross-service generalization. Research question three becomes objectives three and four and contribution three, AgentEdge: intelligent action from intent.

The claim at the bottom of the slide is the whole thesis in one line: each contribution removes one blocker, and together they close the zero-touch loop.

### Slide 09 · AERO

Contribution one is AERO, the edge-deployable workload predictor. The banner states the claim very directly: a tiny model that learns its own periodicity can forecast accurately on edge hardware, and the subtitle pins it: we forecast workloads directly on edge hardware.

The quantified goal is fewer than one thousand parameters. That is the constraint that the rest of the AERO section has to defend.

Presenter cue: short pause here; quick sip of water before contribution one.

### Slide 10 · System Model & Motivation

This slide is deliberately generic: it is the system model for the predictor box, not AERO itself yet. On the left, each edge node is a microcontroller-class device running a tight on-node control loop — observability, predictor, and local scheduler. The loop closes through the infrastructure layer below it, meaning the services and workloads actually running on the node: the scheduler applies actions onto that infrastructure, and observability reads the new state back. In a real deployment this can be a single node, a node with a microcontroller right next to it, or several micronodes — but the constraint stays the same: the forecast must reach the scheduler before the slot closes.

On the right, the toy example is a single dispatch window. A queue spike builds at WS-A while WS-B is still free, and the dispatch decision is due in about fifty milliseconds. If the forecast is local, the scheduler routes to WS-B in time. If the loop first goes off-node, the reply comes back after the window has already closed. So the claim here is not about AERO's mechanism; it is about placement and timing: prediction is only operationally useful if it arrives before the slot closes.

### Slide 11 · State-of-the-art: Accurate or deployable, not both

The literature now falls into three color-coded regimes. In red are the heavy, undeployable baselines: Pathformer at 2.4 million parameters, WGAN at 2.9 million, ModernTCN at 247 thousand, and FourierGNN at 228 thousand. In amber is SparseTSF, the adapted lightweight baseline: it fits the budget, but accuracy gives way.

The green target zone at the top-left is the point of the slide: small and accurate. AERO sits there at 599 parameters, and the experiments from here on are about showing it truly belongs in that empty quadrant.

### Slide 12 · Design: How AERO works in three steps

AERO's mechanism is intentionally simple on this slide. Step one is to find the rhythm: the repeating pattern in the trace can change over time, so AERO re-checks it every window. Step two is to align first: once the rhythm is known, the repeated cycles are lined up so a small predictor can work on organized structure rather than raw disorder. Step three is to reuse cached layers: when the same pattern returns, the same block can be reused instead of recomputed from scratch.

The big idea is that AERO makes the signal easier before it asks a tiny model to forecast it.

### Slide 13 · Scenario 1: Workload Prediction

This is the scenario slide for the efficiency benchmark. The dataset is the Alibaba 2022 microservices trace, specifically pod MS_11349, with 18,720 one-minute samples across thirteen days and two normalized features: CPU and memory. The benchmark set is five baselines plus AERO.

All models are trained on the same server: NVIDIA A100 40 GB, 30 CPU cores, 200 GiB RAM, 512 GiB SSD, Ubuntu 20.04.2, using Python and PyTorch. Hyperparameters are tuned with Bayesian optimization using twenty random trials and thirty refinement trials per model. The reported outputs are MAE, RMSE, latency, convergence, parameter count, and memory. The slide fixes the exact setup before I show the efficiency result.

### Slide 14 · Result 1: Small enough and accurate enough

Three columns, one conclusion. The red labels here only identify the heavyweight baselines; the comparison itself is in the values. Each column is ordered top to bottom by performance: smallest, fastest, and lowest error. In parameter count, AERO has 599 parameters, while the heavy baselines range from 228 thousand up to 2.9 million. SparseTSF is smaller at 35 parameters, but size alone is not the goal. In inference latency, AERO is at 0.38 milliseconds, well inside the 50-millisecond budget: that threshold tracks the 5G URLLC real-time target reported by Schulz et al. in 2017, which is also the edge control-cycle constraint we use throughout. Pathformer stays at 0.52 milliseconds, but it does so with a far larger model. In MAE, AERO reaches 2.9 times ten to the minus four, essentially on par with ModernTCN and close to Pathformer.

So the finding is the takeaway: only AERO and SparseTSF seem deployable and accurate.

### Slide 15 · Scenario 2: Orchestration outcomes

Now I move from forecasting quality to control impact. The simulator is COSCO on AzureFog: 50 heterogeneous hosts, sixty percent edge and forty percent cloud, with 3-millisecond edge latency, 76-millisecond cloud latency, and 5-gigabit links. The run lasts 2,000 cycles at 300 milliseconds, with 50 containers and 4 arrivals per step.

Forecast inputs come from the BitBrains Random trace: 500 VM traces, 8,631 samples, and seven workload signals. The compared arms are AERO, Pathformer, SparseTSF, and a reactive controller that bypasses prediction. Same scheduler, same workload stream, same objective of minimizing energy plus response time; only the forecast quality changes.

### Slide 16 · Result 2: Controlled simulation results

The result slide uses four operational metrics. As on the previous result slide, the red label only marks the heavyweight Pathformer baseline; the values carry the comparison, and the rows follow the metric direction. Energy is 1293 joules for the reactive baseline, 1140 for SparseTSF, and 1123 for both AERO and Pathformer. Response time falls from 10.02 seconds for reactive to 6.5 for SparseTSF, 3.29 for AERO, and 2.45 for Pathformer. SLA violations are 22.21 percent for reactive, 4.60 percent with SparseTSF, 0.21 percent with AERO, and 0.10 percent with Pathformer.

Task migrations are 2,026 for reactive, 5,309 for SparseTSF, 7,747 for AERO, and 8,480 for Pathformer. The compact takeaway is that SparseTSF fits edge hardware but fails once we judge it by orchestration outcomes, while AERO stays close to a transformer roughly 4,000 times larger.

### Slide 17 · Scenario 3: Live deployment

The final AERO test is live deployment. The training source is a Google Cluster trace with T equal to 8,930 samples, four features, and five-minute resolution. Both AERO and SparseTSF are trained with the same setup and hyperparameter search, then deployed as microservices on a physical testbed: i9-9900K, 46 GB RAM, RTX 2060, Ubuntu 24.04.1, using Docker Compose.

On the held-out test split the two models look almost indistinguishable; the live unseen workload is where drift exposes the difference. The live evaluation reports normalized MAE, RMSE, and mean inference time under the 50-millisecond real-time threshold.

### Slide 18 · Result 3: Live deployment results under real-world drift

The live deployment numbers are clean. As on the earlier result slides, the rows follow the metric direction and the deployable-model colors stay consistent. A quick word on metrics first, because the deck uses several. MAE is mean absolute error, the typical miss per point. RMSE is root-mean-square error, which penalises large misses more strongly; I show both here so the committee can see not just the average error but also the spread of errors. SMAPE, which appears later in the OmniFORE section, is the scale-free version used to compare across services of different magnitudes. On the unseen workload, AERO reaches a mean absolute error of 0.051, while SparseTSF reaches 0.411, about eight times higher. RMSE tells the same story: 0.079 for AERO and 0.430 for SparseTSF. Inference is 2.65 milliseconds for AERO and 1.12 milliseconds for SparseTSF, so both remain comfortably within the 50-millisecond scheduler budget.

The point is that latency is not the differentiator; drift robustness is. That is why the operator-impact footer matters: roughly fifteen percent lower response time and twelve percent lower energy once the model stays accurate in the live environment. This closes AERO: all three AERO experiments answer RQ1. From here I switch to contribution two, OmniFORE.

### Slide 19 · OmniFORE

Contribution two is OmniFORE, and the banner now reads in the same shape as AERO and AgentEdge: one-line claim, one-number goal. The claim: one frozen model forecasts across services, no retraining. The quantified goal is deliberately blunt &mdash; zero per-service retrains. That is what I will defend in the next ten slides.

The concrete promise I test is zero-shot prediction on services the model never saw during training, up to cross-dataset transfer with frozen weights.

Presenter cue: reset the pace here; quick sip of water before contribution two.

### Slide 20 · Problem: one model, many services

This slide states the OmniFORE problem in operator terms. I want one model trained once on a service catalogue and then able to forecast any service in that catalogue, including services it has never seen. The visual contrast is between bursty and steady families, because the model has to cover both without separate retraining.

Formally, the goal is one shared set of weights, no per-service fine-tuning, and average prediction error minimized across all services, seen and unseen. That is the only path by which the prediction layer actually scales operationally.

### Slide 21 · System Model & Motivation

Again this is the generic setting, not the method. On the left, one prediction layer observes many service traces at a compute site, which could be any tier, and returns per-service forecasts into the same downstream decision stack. On the right, the motivation is operational cost.

Today site 1, site 2, all the way to site N tend to carry their own model 1, model 2, through model N. As the number of sites grows, retraining, memory, and monitoring repeat everywhere. The target is one shared model that can serve many sites and many services, instead of duplicating the machine-learning workload at every location.

### Slide 22 · State-of-the-art: no prior method lives in the top-right

The prior work again falls into two red regimes around one green target. The first red regime is per-service retraining: ModernTCN, AGCRN, and LSTNet can work well on the service they saw, but every new service needs a new model. The second red regime is generic but heavy: foundation models promise reuse, but are too heavy and too generic to be the deployable workload layer.

The top-right quadrant, one model with unseen-service accuracy, is still empty. OmniFORE is designed to occupy that gap.

### Slide 23 · Design: How OmniFORE works in three phases

This slide packages the OmniFORE pipeline. Phase one, stages S1 through S4, designs the training set by encoding traces, clustering shapes, and sampling a balanced catalogue. Phase two, stages S5 and S6, rescales each service and then uses attention over a shared window so one model can learn across heterogeneous services. Phase three, stage S7, tunes hyperparameters on held-out services so the selected setting is rewarded for transfer rather than memorization.

The message is that generalization comes from the whole pipeline: representative data, shared training, and transfer-focused tuning.

### Slide 24 · Building the training set

This slide zooms into phase one. The first card sets the goal: Google's trace catalogue is enormous, so training on all of it is not feasible, and we need a principled way to pick which traces are worth training on. That is what S1 through S4 deliver. S1 fingerprints each trace by compressing it into a shape descriptor. S2 clusters those fingerprints into bursty, steady, and periodic families. S3 tags every trace with its group label. S4 samples proportionally from those groups to build a balanced mix.

The point is that representativeness is engineered before training begins, so the model later sees the catalogue in balanced form instead of allowing one family to dominate the dataset.

### Slide 25 · Training the model

Phase two has two steps. S5 is equal scale: raw services arrive at very different magnitudes, so each trace is rescaled so that large services do not drown out small ones. Every workload gets an equal say in training.

S6 is efficient attention. The top figure shows the head scanning the full recent window and pulling forward the strongest matching moments. The bottom figure contrasts all links with a sparse view, showing why long windows stay cheap instead of paying equal attention to everything.

That is also why the model generalizes: it matches patterns rather than service identity, so after rescaling those patterns can transfer to services it has never seen.

### Slide 26 · Tuning for transfer

Phase three is the single S₇ stage: tune so it transfers. On the left, Bayesian optimisation keeps moving toward the best region, and the star marks the winning setting on the objective-function curve. On the right, the training set is shown separately because it is used to fit the model, not to score the hyperparameters. Only the held-out traces T1, T2, and T3 feed the combined transfer score, so the selected setting is the one that works across new services, not the one that merely fits the training set. The bottom result strip makes the payoff explicit: the winner is chosen for new services.

### Slide 27 · Scenario 1: Clustering Impact

Scenario 1 isolates the impact of clustering in the training-set design. On the left is the clustered sample: a balanced mix of workload patterns. On the right is the random baseline: draw the traces at random, repeat that five times, then average the result. Everything else is held fixed: same model, same tuning, same test services. Only the training traces differ. So if the clustered version wins, the gain comes from the data selection step itself.

### Slide 28 · Result 1: Clustering-based training helps

The percentages matter here because the experimental control is so clean. When the training traces are chosen through clustering instead of random sampling, MAE drops by 20.66 percent, RMSE by 24.63 percent, and SMAPE by 32.71 percent. The model, tuning, and zero-shot test are all unchanged, so the gain comes from the training-set selection step itself.

That is the takeaway: clustering forces the sample to cover bursty, steady, and periodic workload families, whereas random selection over-samples the common shapes and misses rare ones. The next experiment asks whether that representativeness survives a full cross-dataset transfer.

### Slide 29 · Scenario 2: Cross-dataset transfer

The second experiment is the hardest test a forecaster can run: train on Google Borg cells A through F, freeze the weights, and evaluate on Alibaba Cloud 2022, specifically pod MS_11349. No retraining, no fine-tuning, different cloud provider, different workload mix. The three strips on-slide call out exactly what is different between the two environments, and the italic line on the slide is honest about what usually happens here: *this is where benchmark wins usually fall apart*. If the model generalises, it has to generalise without our help.

### Slide 30 · Result 2: Generalises without retraining

This is the transfer result on Alibaba. OmniFORE reaches an MAE of 0.00727, while ModernTCN reaches 0.01045, AGCRN 0.02870, and LSTNet 0.04751 on the same task. Read the bars as "how much worse the baseline is than OmniFORE": ModernTCN is 44 percent higher, AGCRN 295 percent higher, and LSTNet 554 percent higher, all with OmniFORE still running as the same frozen model.

That is why this result matters operationally. The model is learning portable workload patterns rather than provider-specific identities, so a new service can be forecast with the existing model immediately instead of triggering a new training cycle. Said explicitly so it is on the record: this result answers research question two. One frozen model forecasts across providers without retraining. The last missing block in the zero-touch loop is AgentEdge.

### Slide 31 · AgentEdge

Contribution three is AgentEdge, and the banner deliberately reduces it to one line the committee can hold onto: a system that translates operator intent into intelligent orchestration actions. The subtitle says the same thing in the operator's vocabulary: turning plain-language intent into safe autonomous action. The quantified goal stays at above seventy-five percent success. The keywords I want on the record from this slide forward are multi-agent, tool-use, multi-step reasoning, and digital-twin validation. Those are the technical anchors for everything in the rest of this section.

Presenter cue: brief pause and water sip here; this starts the longest section.

### Slide 32 · Problem & Motivation

This slide must make one point absolutely explicit: the decision layer is not a convenience, it is the missing step that turns a human goal into something the platform can actually execute. If an operator says *"reduce energy while keeping SLA"*, Kubernetes cannot do anything with that sentence. Someone still has to decide which service may move, which node must stay pinned, where spare capacity exists, and how to generate the corresponding orchestration procedure rather than merely pick one predefined action. Existing optimizers usually start only after those choices have already been made and written down as formal inputs. That is why this layer is necessary: without it, the control loop still depends on a human in the middle. The last step is also not passive observation, but monitoring whether the deployed behavior still complies with the original intent and remediating when it drifts. The figure then visualizes that exact translation step before the next slide formalizes it as the system model.

### Slide 33 · System Model

This slide is the generic stack, not the AgentEdge architecture yet. The left column compresses the loop into four layers: operator intent, a decision layer, a service-orchestration layer, and the infrastructure itself. In that framing, the prediction step belongs inside the service-orchestration layer rather than standing alone as its own layer. The key point in the right-hand diagram is that the decision layer does not query the prediction layer directly. Instead, service orchestration queries the prediction model, stores the returned predictions in data objects, and the decision layer reads those stored objects together with the live state. Inside that decision layer, the intelligent logic reasons over sets of actions rather than a single raw action. The purpose of this slide is simply to pin down those interfaces before the following slides introduce the concrete AgentEdge design.

### Slide 34 · Design: What is an agent?

Before the state of the art, I first need a precise definition of what I mean by *agent* in this thesis. It is not just one LLM call. Read the slide left to right as five compact cards. To count as an agent here, the system must satisfy PARES: Perceive live bounded state, Act through typed tools, Reason over goals and constraints, Evaluate candidate plans before production, and Sustain behaviour across multi-step interactions. Every card is load-bearing, and if one is missing the system may still be useful automation, but it is not agent-complete.

The reference band below the cards makes an important methodological point: PARES was not copied from one single framework. It was synthesised in Chapter 2 from six representative agentic-framework papers, and that is what justifies using it as the comparison contract on the next slide.

### Slide 35 · State-of-the-art: no prior 6G work is a full agent under PARES

I talk through this slide as A, B, and C so it does not clash with the numbered references in the table. A, in blue, is the 6G literature: these works are not full agents under the highly cited ML definition, and they also do not span both edge and cloud. B, in purple, is the ML baseline side: these frameworks are full agents, but they are generalist single-agent frameworks and were not built or tested for edge-cloud orchestration. C, in pink, is AgentEdge: it spans both edge and cloud, clears the full PARES bar, and uses multi-agent coordination. So the landing point is simple: the 6G rows are domain-relevant but incomplete, the ML rows are full agents but domain-misaligned, and AgentEdge is the only row here that covers both.

### Slide 36 · Graph of graphs and microservice deployment

The architecture is a graph of graphs: a top-level orchestrator routes, from *start* to *end*, through four subgraphs in sequence: Intent, Observability, Planning, and Infra Action. Each of those four agents is itself a small subgraph with its own internal reasoning steps; the legend on the left makes that explicit, one box per specialist, one dashed rectangle per inner subgraph. On the right is the deployment story, stripped to the essentials. Specialist pods (intent, observe, plan, infra_action) are thin, and they share two backend services: a single LLM backend that answers prompt-and-reply traffic, and a single MCP server that exposes typed tool calls. The MCP server then talks to the container orchestrator, which actually executes actions across the three physical tiers (far edge, near edge, cloud) and sends updated state back to observe. Everything agents do is either *prompt/reply* against the LLM or *tool call/result* against MCP: nothing else. On top of that, every specialist still satisfies PARES (Perceive, Act, Reason, Evaluate, Sustain), so these are agents, not prompt chains. The three benefit pills at the bottom are the architectural takeaway: *lightweight*, because thin pods call a shared LLM instead of carrying the heavy model; *flexible*, because the LLM backend can be swapped at deploy time without rewriting the agents; and *typed*, because MCP returns one shared typed interface and result shape no matter which agent called it.

### Slide 37 · AgentEdge splits orchestration across four specialists

This slide walks the committee left-to-right through the four specialists as a numbered pipeline, because each one is the minimal response to one specific failure mode in the intent-to-action path. *01 Intent Agent* takes the operator's ambiguous natural-language request (on the slide, *"cut power, keep SLA"*) and parses it into a typed goal, shown as the JSON block with `"goal": "save_power"` and `"sla": "preserve"`. Without this step, every downstream agent would have to re-interpret the operator sentence and they would disagree. *02 Observability Agent* watches the live system and filters raw telemetry (the rising power trace on the slide) into a small set of structured alerts such as *node_3 hot* and *node_5 has headroom*. Without this step, planning drowns in raw metrics. *03 Planning Agent · ActSimCrit* is the heart of the system, and the loop figure shows why: Plan proposes, Sim runs it in the digital twin, Crit critiques the simulated outcome, and the red dashed *reject* arc sends control back to Plan until the critic accepts; only then does a validated plan leave the box. That inner loop is the whole reason plans do not reach production without validation, and it is expanded on the next slide. *04 Infra Action Agent* takes the validated plan and executes it as concrete API calls: on the slide, *migrate svc → node_5* and *low_power node_3* become `POST /migrate` and `PATCH /power` requests, with retries on failure. The committee takeaway: drop any one of these four and the system fails in a predictable, locatable way (ambiguous intent, state blindness, unvalidated plans, or unreliable execution).

### Slide 38 · Planning Agent · the ActSimCrit loop

This is the core of AgentEdge, and I talk it through as a five-phase loop that runs five LLM calls plus one simulation per iteration. *P1 Plan* sets the end-goal state and the constraints the loop has to respect. *P2 State* reads the current system and identifies the bottlenecks and violations that stand between current and goal. *P3 Actions* picks the next batch of tool calls, skipping any batches the critic has already rejected. *P4 Sim + Critic* is the validation step: the action batch is simulated inside a digital twin (a sandbox, no LLM) and then judged by an independent critic LLM that has no memory of prior attempts. *P5 Intent met?* asks whether the simulated end-state actually satisfies P1; if yes, the loop emits a validated plan to the Infrastructure Action Agent, and if no, control goes back along the red dashed *reject · retry · add actions* arc to P3. If the iteration or rejection caps are hit, the loop terminates cleanly into a DEADLOCK chip and the agent proposes an alternative intent instead of spinning forever. On the right, four mechanisms make this loop actually work in practice. *Action batching* groups logically connected steps (e.g. `migrate + migrate + low-power`) into one LLM call instead of replanning each action. *Three-tier state* separates baseline, accepted, and simulated state, so only validated batches ever promote accepted state and failed batches leave it untouched. *Rejection-feedback* records the structured reason each batch was rejected (on-slide example: *node_5 over capacity (+0.4 core)*, next try *node_7 instead*) and the schema excludes rejected options from the next selection. *Deadlock detection* uses iteration and reject caps to convert infeasible intents into an achievable alternative rather than retrying forever. The output is a validated plan, not a guess; the infra agent executes it, it does not diagnose.

### Slide 39 · Simulator testbed and six evaluation scenarios

This slide does two jobs at once: it introduces the three-tier edge-cloud testbed that I use as the evaluation harness, and it lays out the six scenarios I run on it. On the left, the tiered architecture is stacked from cloud down to far edge. Tier 3, cloud, is zero-to-one node with 64 CPU, 256 GB, power envelope 180-450 W. Tier 2, near edge, is zero-to-ten nodes with 16 CPU, 32 GB, 40-120 W, connected to cloud by a 25-60 ms link. Tier 1, far edge, spans two-to-twenty-four nodes with 4 CPU, 8 GB, 10-35 W, connected to near edge by 10-25 ms. Directly under the tier stack, the table now gives a horizontal summary by tier: node range, per-node capacity, upstream latency, and power draw for far edge, near edge, and cloud. The final *shared model* row keeps only the essentials: the same small service catalogue across tiers, realistic deploy/migrate/scale delays, a bit of random noise and failure, and a *low-power -60%* mode in AgentEdge pink. That is the actuator this chapter actually turns. Same simulator also serves as the digital twin inside ActSimCrit at runtime. On the right, the six scenarios split into two groups, and each card carries its own italic user prompt at the bottom to anchor what the operator actually typed. *Group A · constraint resolution* (S1-S3) uses two nodes to force reasoning under conflict. S1 *Full Node* — prompt "deploy a new service on edge-0" — has edge-0 full and edge-1 idle, so the agent must *find free space first*. S2 *Sleep Conflict* — prompt "sleep edge-1 + scale APIService to 1.4c" — has both nodes active but the user asks to sleep edge-1 while a service on it needs to scale up, so the agent must *move, then sleep*. S3 *Won't Fit* — prompt "sleep edge-1 + scale APIService to 2.4c" — is the same setup with a larger scale target: the service grows so large that straight consolidation onto edge-0 would overflow, shown as a dashed arrow blocked by a red cross, so the agent must *redistribute the load*. *Group B · energy scalability* (S4-S6) all share the same prompt, *"reduce energy whilst keeping SLA"*, and scale the infrastructure up underneath it: S4 small, 8 nodes and 6 services with 2 idle; S5 medium, 18 nodes and 15 services with 3 idle; S6 large, 35 nodes and 30 services with 6 idle. Success is defined by pre-defined valid end-states and an exact match, with no partial credit. The fairness guarantee in the footer of the right panel is critical: *same catalogue, same LLM, only architecture varies*. That is what makes the Experiment 1 comparison honest.

### Slide 40 · Scenario 1 · Multi-agent vs single-agent

The first AgentEdge experiment is an architecture-versus-architecture comparison, and the left side of the slide shows all three arms side by side as diagrams so we can see *why* they differ, not just that they differ. AgentEdge is the graph of graphs: four specialist agents (intent, observe, plan, infra_action) routed sequentially, one graph end-to-end. ReAct is the one-LLM think-act loop: a single model interleaves reasoning, tool calls, and observation, and only stops on a finish action; no specialization, no plan validation. LATS is the same single LLM but wrapped in Monte-Carlo tree search: the model expands, scores, and rolls out over a tree of reasoning steps, keeping the best trajectory; it is the strongest single-agent baseline in the literature. The right side of the slide is the measurement protocol, shown as a picture. Each scenario pre-defines *all valid infrastructure end-states* up front, and a run counts as successful only if the final placement lands in that set, exactly matching one of the predefined configurations. The cartoon on the right makes this concrete with a simple example: the initial state is edge-0 at fifty-percent utilisation and edge-1 at fifty-percent utilisation, and the task is *shut one server off*. The valid end-states panel shows two symmetric configurations (all load consolidated on edge-0 with edge-1 off, or all load consolidated on edge-1 with edge-0 off); both tick. The *anything else · fail* panel shows two ways a run goes wrong: still 50/50 because the task was never completed, or an uneven split such as 75/25 where consolidation stopped halfway. No partial credit. And that is the whole point of this design: same LLM, same tools, same tasks, sixty runs per arm. If the success rates differ, the gap cannot be model capability, it has to come from the architecture itself.

### Slide 41 · Result 1: Multi-agent beats every baseline

The numbers are clean. AgentEdge succeeds on 78.3 percent of trials. LATS succeeds on 65.0 percent. ReAct succeeds on 28.3 percent. As multipliers, which are stickier than raw percentages, that is 1.20 times LATS and 2.76 times ReAct. The finding banner is direct: multi-agent architecture beats every SOTA single-agent baseline, on the same LLM, on the same tasks, in the same simulator. The next experiment takes the next obvious question: is this gain really coming from the digital twin, or from the four-agent structure alone?

### Slide 42 · Scenario 2: Twin ablation

The ablation turns the digital twin on and off and holds everything else constant. The two panels are styled identically on purpose: same title bar, same color scheme, same four boxes (PLAN, SIM, CRIT, EXEC), same red dashed *reject · retry · add actions* arc. The only deliberate visual difference is the SIM box on the right side, where the digital twin is replaced by a red dashed *REMOVED* ghost labelled SIM and Digital Twin. Everything else stays symmetric. On the *TWIN ON* side, PLAN sets the actions, SIM runs them on the digital twin, CRIT (an independent critic LLM) judges the simulated outcome, and only a validated plan reaches EXEC on real infra: this is the full AgentEdge pipeline. On the *TWIN OFF* side, labelled *AgentEdge minus twin*, the PLAN and CRIT boxes are identical, but pre-execution validation is removed. What that means precisely: planning still happens, the *reject · retry · add actions* loop still exists, but there is no sandbox simulation before actions hit production. Plans are pushed straight to EXEC. The bullets under each panel make the consequence concrete: *TWIN ON* → plans validated on the twin before touching infra, retries are *virtual*, bounded by iteration and reject caps; *TWIN OFF* → plans pushed to infra without twin validation, retries are *physical*, bounded by the same iter and reject caps but on real infra. The point of this design is to isolate the twin's contribution as *pre-execution validation*, not as the existence of retries. The twin does not change whether a plan can succeed; it changes how many physical retries it takes and how much damage those retries can do on the way. That is why we report both success rate and API-call count. Failure-shifting cannot hide behind either metric alone.

### Slide 43 · Result 2: Sandbox validation reduces costly trial-and-error

The ablation tells a very direct story. With the twin, success is 78.3 percent; without it, success drops to 53.3 percent, a 1.47 times improvement. The more operational number is API behaviour. With the twin, the standard deviation of API-call counts is 1.1. Without the twin, it jumps to 109.4, about ten times higher variability. Without simulation, the agent enters unproductive retry loops that are not just slower; they are operationally unsafe, because every retry touches production. The twin is therefore structural: it lifts success *and* collapses variance. The last experiment asks how this behaviour changes as the infrastructure grows.

### Slide 44 · Scenario 3: Energy scalability

The last AgentEdge experiment asks a practical question: does the energy saving hold up as the infrastructure grows? I am keeping this slide deliberately visual, because the problem is visual. At every scale the starting pattern is the same: each service is running on its own node at roughly twenty-five percent utilization, and on top of that a few nodes sit fully idle. Busy or not, every one of those nodes still draws baseline power. That is what the three panels show. *Scale A · Small* is eight nodes, six services, two idle. *Scale B · Medium* is eighteen nodes, fifteen services, three idle. *Scale C · Large* is thirty-five nodes, thirty services, five idle. The legend is explicit: the light boxes with a small red band at the bottom are nodes at about a quarter load, the dashed empty boxes are fully idle nodes that are still drawing power. Look at the picture for a few seconds and the committee reaches the same question I want them to reach: *why run thirty nodes at twenty-five percent when eight or ten could run at seventy percent while the rest sit in low-power mode?* The fix is obvious at every scale: consolidate the services onto fewer nodes, power the rest down. The real question is whether the agent still pulls this off as the grid grows. That is what the next slide answers.

### Slide 45 · Result 3: Power drops across every scale

Three panels, one story. The y-axis on each panel is total rack power in watts, and the x-axis is the number of API calls the agent has made. Every green square marks the starting power, every red triangle marks the settled power, and the green arrow in the middle of each panel is the delta-watts: how much power the agent reclaimed. At eight nodes, power drops from about four-hundred-and-sixty watts to roughly three-hundred-and-seventy watts; delta-W equals eighty-nine watts. At eighteen nodes, power drops from about seven-hundred-and-ten watts to four-hundred-and-ten watts; delta-W equals three-hundred-point-eight watts, the peak, and the one I want the committee to remember. At thirty-five nodes, power drops from roughly twelve-hundred-and-fifty watts to just over one-thousand watts; delta-W equals one-hundred-and-eighty-five-point-two watts. A reasonable follow-up is *why does eighteen beat thirty-five?* The thirty-five-node curve flattens early because the full node state overflows the LLM prompt; it is a context-window artefact, not a fundamental limit. With summarisation or sharded context, the curve would keep descending. The bottom-left reference reuses Syamkumar, Barford, and Durairajan as the operator-scale context: reclaiming hundreds of watts per rack matters because these decisions repeat across large MEC footprints. All thirty runs succeeded across every scale. This closes AgentEdge: the three experiments answer RQ3 by showing that AgentEdge beats baselines, plans safely, and still saves power at scale.

### Slide 46 · Slide 03 reprise + publication mapping

This slide is a callback to slide three. The left side is still the same four-layer stack, but L1 and L2 are now visually grouped as one AgentEdge band so the agentic layer reads as one research thread rather than two separate problems. The right side maps the stack onto the thesis publication list, but the numbering now follows the presentation order: AERO is [J1] and [C1], OmniFORE is [J2], [J3], and [C2], AgentEdge is [J4] and [C3], and [B1] remains the related book-chapter output at infrastructure level. The SECON paper is marked accepted.

I keep this one very short in delivery. The point is simply that the publication record lines up with the stack while the numbering still follows the story of the defense. The full bibliographic list remains on backup slide B16.

### Slide 47 · Future Work · The Agentic Intelligence Layer

Same grouped stack as the previous slide. The left column is unchanged on purpose: L1 and L2 are shown as one AgentEdge band, L3 is the prediction layer finished by AERO and OmniFORE, L4 is the hardware we run on. What changed is the right-hand side. The publications are gone, and in their place is a single clear indicator: future work lives on L1 and L2. That is the agentic intelligence layer, and that is where this chapter of research continues.

Three short cards explain why. The first, *prediction is heavily researched*: lightweight nets and attention mechanisms rest on decades of time-series work. It is a mature field with established methodology. The second, *orchestration is a younger field*: which predictor to invoke for each situation, when a forecast warrants action, how to balance objectives that no single model optimizes: those are all still open questions. The third, *predictors become tools the agent selects*: AERO and OmniFORE are tools an agent picks, the same way a human operator picks between monitoring dashboards. Once you frame them as tools, the research question moves one level up, to the entity that chooses between them.

That is the transition. From here, the next three slides open up the specific blockers on L1 and L2.

Presenter cue: another quick sip here if needed before future work and the closing stretch.

### Slide 48 · Future Work 1 · Reliability & Trust

The first future-work slide picks the two blockers that, together, decide whether operators will ever let an agent run unattended. I keep only two per slide, each shown as its own card with a visual.

On the **left card**, the blocker is that *there are no public benchmarks for orchestration*. Every team builds its own bench, runs it on their own workload, and reports numbers that nobody else can reproduce. The visual puts three dashed boxes on the left (team A, team B, team C, each with their *own bench*) and then an arrow into a single shared frame on the right: an open orchestration benchmark fed by real operator traces, a leaderboard, and public competitions. The direction is a concrete programme that can start tomorrow. First, publish open benchmarks built from real, historical operator action traces, not synthetic workloads, the actual actions that humans and schedulers took on production clusters. Second, run public competitions on those benchmarks so the field accumulates a shared research history instead of re-inventing the wheel paper by paper. Third, the same trace datasets are exactly what is needed to train orchestration *world models* (V-JEPA 2 style) so an agent can simulate the consequences of a planned action before it commits.

On the **right card**, the blocker is *security*, and I want to be precise about the threat model. The concern is not external prompt injection: orchestration agents sit inside a protected perimeter where only authorized operators have access. The concern is what happens when an agent with Kubernetes API access makes a mistake. The right side mirrors the left: two small figures above and two concrete research directions below. The first figure, labelled *Q1 · pre-commit gate*, shows a plan of steps with a risky step flagged in AgentEdge pink, routed through a static-plus-learned *safety check* that either blocks and escalates or allows the step — the point is that risk is caught *inside the plan*, not after the action has committed. The second figure, labelled *Q2 · physics-accurate twin*, shows a sandbox that is a physics-accurate twin of production, separated by a dashed air gap from the protected production side. The second direction is where I want to plant a specific claim: the right sandbox is not a simulator with simplifying assumptions, it is a *physics-accurate digital twin of production*, and with a sufficiently faithful twin AgentEdge would reach close to 100% success — because a near-perfect twin is an oracle for every plan it evaluates. The research lever therefore is not AgentEdge's policy, it is the *fidelity gap* between the twin and production, which reframes "build a safer agent" as "build a more faithful twin". So the two directions below say: build pre-commit safety checks that flag risky steps inside the plan, and build a physics-accurate twin of production as the safe-to-fail sandbox — with high fidelity AgentEdge would get close to 100%, and the remaining gap *is* the twin-fidelity gap. The V-JEPA 2 world-model direction on the left card carries its canonical reference on the slide, Assran et al. 2025, so the committee can place it in context.

### Slide 49 · Future Work 2 · Real-time Infrastructure

The second slide narrows to the two most empirically grounded real-time blockers we hit inside AgentEdge.

On the **left card**, *inference efficiency*. Each orchestration is a chain of LLM calls: observe, plan, revise, critique, actuate, and every call is seconds, not milliseconds. The timeline visual stacks those boxes along the real axis, drops a red dashed real-time-SLA line right through the critic step, and the over-budget bracket sits on the bottom axis past the SLA so you can read the blown budget directly off the timeline. I lead with the strongest direction: *train specialised small models for orchestration*, right-sized world models per decision, the same lesson AERO already proved at the forecasting layer. The second direction is *bring algorithmic planners like ILP into the loop*. Integer linear programming turns planning back into a problem we can solve with decades of operations-research tooling instead of leaving it to free-form reasoning, and our own early experiments look very favorable.

On the **right card**, *tool discovery*. This one is an empirical finding from the thesis itself. Tool-pick accuracy stays strong up to roughly thirty tools and then cliffs. The chart shows exactly that shape, with the cliff highlighted at thirty and an annotated AgentEdge point (three MCP servers, about forty tools) sitting right on it. The framing is deliberate here: the failure is at the agent level, not only in its planner, because downstream execution inherits whatever tool the agent picked. Removing an MCP server sometimes *improved* success, which reinforces the point. Two directions. First, *filter the tool surface and deliver only task-relevant context* to the agent: semantic retrieval and hierarchical catalogs so the agent sees a focused relevant set rather than the full shelf every turn. Second, *learn tool selection from past traces*, routed by what actually worked in production, not by tool names and descriptions alone. Latency and tool surface are both context-engineering problems, not hardware ones.

### Slide 50 · Future Work 3 · Distributed Ecosystems

The last future-work slide is the one about what happens when we stop talking about a single AgentEdge instance and start talking about fleets of them. The framing on this slide is deliberately research-first, not engineering-first. Each card is a pair of open research questions rather than a to-do list, because these are the questions that still need study before they become products.

On the **left card**, *multi-agent coordination*. Once we deploy fleets of AgentEdge instances, independent agents on shared infrastructure can still propose contradicting actions. The visual is deliberate: Agent A says consolidate onto node-07, Agent B says power-down node-07, both arrows converge on the same shared node, and the conflict is the red X at the far right, detected only after the fact. The two open research questions sit underneath. First: how can independent agents reach a consistent joint plan before any action commits? Second: when is shared reasoning between LLMs beneficial versus costly under real-time constraints? Both are genuinely open; neither has a known answer in the orchestration literature.

On the **right card**, *model-agnostic design*. This blocker comes straight from the AgentEdge development experience. Swap the LLM provider and the tool calls change shape: provider X returns camelCase JSON, provider Y returns an XML-ish schema, and the same intent suddenly routes through model-specific adapters, prompt re-tuning, and retry regressions: a "glue-code" tax that undermines portability. Again phrased as research questions rather than engineering directions. First: what abstractions make agent tool-calls portable across heterogeneous model providers? Second: how much do we lose when the model is swapped live? These are measurement problems and design-space problems before they are implementation problems. Two cards per slide, four open research questions total. That is the whole future-work section.

### Slide 51 · Three contributions, one systems thesis

Three claims, each defended with three anchor numbers that were already shown on the result slides, nine anchors in total. Claim one, AERO: eight-times-lower live MAE versus the SOTA small model, roughly a hundred-times fewer SLA misses than a reactive baseline, and all of it in 599 parameters: real-time forecasting fits on the edge, SOTA accuracy, stable under drift, and small enough to deploy anywhere. Claim two, OmniFORE: 30.4 percent lower MAE versus ModernTCN, a 20.7 percent gain from clustering-based training, and zero-shot transfer from Google to Alibaba: one attention model generalises across services, no retraining for each new workload. Claim three, AgentEdge: 1.20 times success versus LATS, 1.47 times success twin-on versus twin-off, and 300.8 watts of rack power reclaimed at eighteen nodes: multi-agent orchestration with a digital-twin critic is reliable on live infrastructure and saves energy at scale. The closing line captures the thesis: edge-cloud orchestration moves from reactive supervision to a proactive, validated control stack: three layers, nine anchor numbers. That is what I defend.

### Slide 52 · Questions

BRACE.
Breathe: pause, one breath.
Restate: "If I understand correctly, you are asking whether..."
Answer first: "The short answer is..."
Cite one anchor: one result, one comparison, one reason, or one number.
Edge and end: state the boundary, then land the contribution.

20-second default:
"The short answer is..."
"The main reason is..."
"The strongest evidence is..."
"The boundary is..."
"So the contribution is..."

Rules: answer the actual question, keep it under 30 seconds unless they ask for more, use at most one memorable number, never bluff, stop after the main point.

Leave this slide open during Q&A and use the backup index on the right if needed.

BACKUP INDEX: 17 slides · B0 through B16

· Methodology & rigor (framing color) ·
B1 · Statistical rigor: sample sizes, variance, Wilson CIs
B2 · Baseline fairness: shared BO budget, adapted ReAct/LATS
B3 · Trace & dataset selection: why MS_11349, why a 20 % subsample
B4 · Simulator & twin fidelity: COSCO independence, twin ≠ executor
B5 · LLM reproducibility: pinned model, seeds, hosted-provider drift

· AgentEdge deep dives (pink) ·
B6 · PARES capability contract: the five-letter definition
B7 · Why 78.3 %, not 100 %: three residual failure modes
B8 · Scaling 8 / 20 / 35 nodes: context bloat, 150 ms budget origin
B9 · Success metric: exact match, scenario design, valid-set bias
B10 · Plan–execute staleness: execution-gate re-query, ILP speed-up

· AERO & OmniFORE deep dives ·
B11 · AERO vs Pathformer: the CPU/RAM chart explained (floor artifact)
B12 · Informer / Pathformer / AERO: three models, three roles
B13 · AERO beyond workload traces: other 6G signals, periodicity
B14 · OmniFORE deployment & leakage: tier-agnostic, zero-shot defense

· Context & scope ·
B15 · 6G service mix: payload-agnostic, Nearby scope, J4 → OmniFORE
B16 · Full publications: 9 outputs, bibliographic data by contribution

B0 is the on-slide navigable index if the committee wants to see it.

Opening line: thank you, I welcome your questions. The slide itself shows the compact deck guide on the right (sections 1 through 3 by slide range) and the italic line on the left, "the system is zero-touch · the Q&A should definitely not be", plus supervisors and tribunal.

### Backup B0 · Backup index

Backup slide: self-contained. No spoken script; the slide carries the full answer.

### Backup B1 · Statistical rigor

Backup slide: self-contained. No spoken script; the slide carries the full answer.

### Backup B2 · Baseline fairness

Backup slide: self-contained. No spoken script; the slide carries the full answer.

### Backup B3 · Dataset and trace selection

Backup slide: self-contained. No spoken script; the slide carries the full answer.

### Backup B4 · Simulator and digital-twin fidelity

Backup slide: self-contained. No spoken script; the slide carries the full answer.

### Backup B5 · LLM reproducibility

Backup slide: self-contained. No spoken script; the slide carries the full answer.

### Backup B6 · PARES capability contract

Backup slide: self-contained. No spoken script; the slide carries the full answer.

### Backup B7 · Why 78.3 %, not 100 %

Backup slide: self-contained. No spoken script; the slide carries the full answer.

### Backup B8 · Scaling 8 / 20 / 35 and the 150 ms budget

Backup slide: self-contained. No spoken script; the slide carries the full answer.

### Backup B9 · Success metric and scenario design

Backup slide: self-contained. No spoken script; the slide carries the full answer.

### Backup B10 · Plan–execute state staleness

Backup slide: self-contained. No spoken script; the slide carries the full answer.

### Backup B11 · AERO vs Pathformer (CPU / RAM chart)

Backup slide: self-contained. No spoken script; the slide carries the full answer.

### Backup B12 · Informer / Pathformer / AERO roles

Backup slide: self-contained. No spoken script; the slide carries the full answer.

### Backup B13 · AERO beyond workload traces

Backup slide: self-contained. No spoken script; the slide carries the full answer.

### Backup B14 · OmniFORE deployment and leakage

Backup slide: self-contained. No spoken script; the slide carries the full answer.

### Backup B15 · 6G service mix and industrial scope

Backup slide: self-contained. No spoken script; the slide carries the full answer.

### Backup B16 · Full publications

Backup slide: self-contained. No spoken script; the slide carries the full answer.
