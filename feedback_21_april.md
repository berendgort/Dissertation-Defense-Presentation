## 3. Cross-Cutting Principles Still Violated

These are the same rules from 17 April; they have been partially honored in v1 but re-emerged in specific places.

### 3.1 "Everything must appear before being used"

Re-surfacing violations in v1:

- **`attention mechanism`** — used in AERO, OmniFORE, and implicitly in AgentEdge, but never introduced. Angel (12.31): *"I missed attention models. I mean, you don't mention at all … the first two works are based on attention models. They, for example, you don't mention the capability of capturing past and longer periods, etc."*
- **`informer` / `Informers magazine paper`** — the magazine publication is cited but informers are not introduced anywhere in the talk (12.31).
- **`PARES`** — still used in the SotA table (Slide 37) before the capability contract is itself introduced (13.08).
- **`single-agent baseline`** — the concept appears in Slide 43/44 results but is not defined in state-of-the-art. Angel (13.08): *"the single agent part that I don't know now how we will change it. But try to introduce a bit the concept of single agent. I mean, if… you can do it even in the state of the art."*
- **`smart picking`** — appears as a chart title on Slide 31 but has not been named anywhere earlier. Godfrey (11.35): *"because what is smart picking comes what is smart picking? That means you have to go again to this because this is the impact of clustering. I would be very comfortable say the impact of clustering. Then smart picking can come into explanation."*
- **`bursty / steady / periodic families`** — visualized on Slide 27 but the *bursty* trace is drawn too periodic. Angel (12.31): *"It's stupid. But I don't know if you can find a better representation for bursty traffic because now it's like periodic. So maybe best is like more spiky."*

### 3.2 "Every number needs a baseline anchor or human-scale meaning"

- **`300.8 W` saved (Slide 48)** — still naked. Angel (13.08): *"300.8 — someone can say okay, if it's for a country, no one cares. If it's for your home, maybe it's very important."* Unlike 17 April, Angel *withdrew* the "use percentages" suggestion ("I'm not saying. I mean what I said before is that percentages do not make sense to compare"); the fix is instead to **share the same y-axis scale across the 8/20/35 plots** so absolute savings can be read visually.
- **`150 ms` inference budget (AgentEdge)** — mentioned but the origin is unclear. Angel (13.08): *"150 milliseconds. We had a 50 milliseconds budget for [the edge]… then you must have it of tickets by 50 milliseconds for the edge because this is the target we target for."*
- **`599 / 30.41% / 2.76x` (Conclusions slide)** — anchored but Angel wants them folded into *bullets*, not as the headline. 13.08: *"maybe it's like you need to highlight 2, 3 numbers for each one. Okay, what more numbers? It's about what are the conclusions?… having us bullets some numbers than focusing on the numbers."*

### 3.3 "Connect to orchestration everywhere, not just at the end"

- Slide 3/4 still does not motivate **why prediction is needed** at all. Godfrey (11.35): *"when you're talking about here you say up to the end you didn't motivate why prediction is important because I kept following no motivation for the need for prediction. The justification you gave, the need for generalization, also the need for smaller models. But the essence of the importance of prediction wasn't motivated anywhere up to the conclusion."*

### 3.4 "Same colors, same vocabulary, same block layout across the deck"

- Slides 02/03/50/51 bottom "infrastructure layer" colors — the layer is rendered with the AERO/OmniFORE solution colors, which is confusing. Angel (12.31): *"the last infrastructure layer here it's like the colors are same as the solutions, but it's confusing. I would prefer a more natural. I mean in the last one you have it just gray."* Fix: bottom infrastructure layer → neutral gray; solution colors reserved for contribution layers only.

## 4. Slide-By-Slide Feedback (v1 Numbering, 56 Slides)

> Legend: `[P0]` must-fix · `[P1]` strong recommendation · `[P2]` polish · `[Q]` open question · `[KEEP]` explicit positive signal
>
> Numbering below matches `DEFENSE_SPEAKER_NOTES_FULL.md` (Slide 01 … Slide 56). For slides the committee did not discuss in 21 April, this section is silent and the v0→v1 resolution should stand.

### Slide 01 — Title
- No comment. Keep.

### Slide 02 — From framing to validated autonomy
- `[P1]` Pagination: redesign header/footer so there is *one* page number and it is visible. Remove bottom thin bar; keep top-right contribution marker only, enlarged. (11.35, 12.31).
- `[P1]` Consider removing the "SME" wording on the bottom strip. Angel (12.31): *"this is fine. Just don't mention small SME. I mean, we are no longer."*

### Slide 03 — Manual reality today
- `[P0]` **Infrastructure layer color clash.** Angel (12.31): *"the last infrastructure layer here it's like the colors are same as the solutions, but it's confusing. I would prefer a more natural. I mean in the last one you have it just gray. Here I don't understand why you have it like blue and the other like [solution colors]. It's like the solution applied to this."* Fix: bottom layer → gray.
- `[P0]` **Prediction need is not motivated.** The slide labels layer-3 problems ("no accurate per-node forecast", "new model per service") but never says *why* forecasting matters for orchestration at all. Godfrey (11.35): *"you didn't motivate why prediction is important because I kept following no motivation for the need for prediction … the essence of the importance of prediction wasn't motivated anywhere up to the conclusion."* Add one sentence (on Slide 02 or 03 or 04, operator's choice) linking prediction to the orchestration loop: *a controller that cannot anticipate load is reactive by construction; every SLA violation is a forecast that did not exist.*

### Slide 04 — Zero-touch: operator sets intent, not actions
- `[P1]` Same color-coding fix as Slide 03 (bottom infra → gray).
- `[P1]` Add the explicit *"why prediction?"* sentence here or on Slide 03 — whichever reads more naturally. Both slides are fair game, but it must exist before Slide 05.

### Slide 05 — Forecasting must run where the service runs
- `[P1]` The Pathformer 2.4 M vs SparseTSF 50 k framing survived from v0; no new complaint. Keep.
- `[P1]` State of the art for AERO is previewed here; the full SotA slide is 12 — see note on color coding there.

### Slide 06 — One model for many services
- `[P1]` Clean. Committee did not stop on this slide in 21 April.
- `[P1]` Minor: the "300+ microservices at 6G scale" figure — Angel warned about claiming types of services on the *AgentEdge* side (see Slide 10 note), but on the prediction side the framing survived. Keep the *number*, drop any subclaim about what *kind* of services they are.

### Slide 07 — From natural-language intent to intelligent orchestration action
- `[P1]` Clean. No substantive comment.

### Slide 08 — One orchestration stack that predicts, generalizes, and acts on intent
- `[P1]` Bottom infrastructure row should be gray too (same fix as Slide 03). Angel compared this slide favorably to the later "prediction layer" slide — it is closer to what a proper overview should look like.
- `[P1]` Angel (12.31): *"50, 50, 55, 0. Yeah. Here you don't have colors. Here it's like an infrastructure layer and you have three solutions. I mean, this is better. I would expect something like this in the beginning."* Reading: the contribution-map landscape on this slide is the *target* aesthetic for Slides 02/03/04 — propagate its neutral-infra styling *up* to the earlier framing slides.

### Slide 09 — AERO header
- `[P1]` Clean. The title + "<1000 parameters" target line is what v0 was missing; now it is on-slide.

### Slide 10 — Forecast the next load window inside an edge budget
- `[P0]` **"Where AERO runs" is not a system model.** Same critique as 17 April survived. Angel (12.31): *"Okay, here. Okay. Some similar [comment]… this is not system model. The last time we talked about it."* And again (12.31, at length):
  > "If you present [this] as system model. But system model should be generic as we discussed. It's not about your solution, it's about… if you want to present a system model, you need… it would need to be a bit more generic and this would be like system model, not where AERO runs. It should be like… you would need to have like small loops here to show that they need to run it locally, for example, and say, I mean all the discussion you had with Godfrey before. I mean to have small schedulers, small loops, decision engine, analytics. This could be a system model, not AERO there for sure."
- `[P0]` Fix: redraw Slide 10 as a **generic edge decision loop** — scheduler + observability + small control loop inside an edge node, with a placeholder "ML model" box where AERO will later sit. *Another prediction method should be able to inhabit the exact same drawing.* Angel's own sketch: *"here is the infrastructure and inside its node you can have this. And here is the Kubernetes API. So maybe this is the slide for the loop … observe, blah, blah, blah. And then here maybe there is a model ML… if you go to slide four, I think one of them is predict. So yes, this one is the ML model."*
- `[P0]` If the System Model slide is made generic (as above), then "where AERO runs" becomes a *second* slide where the generic ML-model placeholder is replaced by AERO's name, parameter budget, and latency budget.

### Slide 11 — Where AERO runs *(currently the system-model slide)*
- `[P0]` See Slide 10 above — the current Slide 11 is actually where the AERO-specific claim should live, *after* a proper generic system model. Angel (12.31): *"system model is not where AERO runs. It's a coincidence. Let's say not coincidence, but it's system model. Also other model run there."*
- `[P0]` **"Each node runs AERO" framing must change.** Godfrey (11.35):
  > "each node runs AERO. Is it a design constraint that the AERO must run on each node? … by designing that it must run here. It's not a design constraint that must run on the local node."
  > "why does it have to run on each node? If I want to run it somewhere else, what do I need to change?"
- `[P0]` Replace the sentence "each node runs AERO" with "**AERO has the *capability* to run on each node because of its lightweight nature — it can also be deployed at the scheduler level, the edge regional scheduler, or the container level.**" Godfrey's own phrasing, dictated verbatim: *"what I would say [is] that as you can see because insulated nature AERO has the capability to run at each node. It can be executed but capability or to execute but not to say … okay, every node runs AERO."*
- `[P0]` Angel strengthens the same concern (11.35): *"if we think our orchestrator we don't run things on the edge, we run things on cloud and we can fit there every prediction. So Godfrey has maybe has this in mind. If you want to motivate this, then you need some motivation because otherwise … even for edge orchestration you can have the predictions in the higher level. You just get observability stack and you have a good model on the Amazon at Amazon."*
- `[P1]` Add a one-line motivator for local-edge deployment: traffic-light-intersection / real-time safety example. Berend's own phrasing (11.35): *"you have for example a bunch of edge nodes which are for… at let's say an intersection of traffic light. Where real time is important."* Angel: *"Yes, exactly."*
- `[Q]` Berend should decide whether the scheduler-on-top diagram becomes the canonical Slide 11, or stays implicit. Godfrey is neutral as long as the framing is *capability, not constraint*.

### Slide 12 — Accurate or deployable, not both *(AERO State of the Art)*
- `[P0]` **Add red/green color coding to the SotA models.** Angel (12.31):
  > "you need to highlight this because then you have the same issues in ModernTCN and Pathformer. Maybe here you need to spend a bit more time or put some colors, maybe red or something like this, and highlight that these models can be accurate. But [they cannot be deployed]."
  > "I would go to the state of the art and red are [the ones that cannot deploy]. And then the other could be orange or something like this or I don't know if it's green or. But I would group them according to the state of the art … the models in red are most heavy. So they can have maybe better performance in some cases, but they cannot be deployed. And then we can see models that are lightweight that here we saw for the trade-offs."
- `[P0]` Minimum palette: **red** = Pathformer, WGAN, ModernTCN, FourierGNN (heavy / undeployable at edge); **green** = SparseTSF (lightweight baseline). AERO sits in the empty target quadrant.
- `[P1]` Carry the same color code across to the efficiency-result bars (Slide 16) so that "red models win accuracy / green model wins deployability / AERO wins both" is visually trivial.

### Slide 13 — Edge efficiency comes from exploiting signal structure
- `[P1]` Inference latency is already on-slide (0.38 ms) but was not explicitly *called out* in delivery. Angel (12.31): *"you didn't mention also the inference. Inference latency."* Fix by narration, not layout.
- `[P1]` "The two halves of the slide are the same thing twice" — the rationale figure + figure caption duplicate content. Angel (12.31): *"I think I can also delete it because it's this. Basically this design is the same thing two times. I would try… maybe to melt this."* Either consolidate panels or move the redundant piece to Slide 14.
- `[P1]` Consider moving the text panel from Slide 13 to Slide 12 so that Slide 13 carries only the mechanism figure. Angel (12.31): *"I mean the previous one you could also mention. So this, not this. I mean maybe. Yeah, this one. So remove this text and put this other [here]. I think this is much more clear."*

### Slide 14 — Adaptive periodicity in three steps
- `[P0]` **Periodicity visualization is too subtle.** Angel (12.31):
  > "In the AERO part, I missed the periodicity, which is the main [mechanism]. You mention it, but not [visibly]. What I missed here is to have different traces or the figures that shows from one periodicity to the other. You have it later with [another figure]. I would expect something better, much more intense. This is like, you know, very, very hard to [read]. We have better figures like when you are first in and then very, very close. So to be better visible. And this is also the motivation."
- `[P0]` Redraw as a **three-panel progression**: raw trace with shifting dominant period → period detection highlighting τ (with labels τ₁, τ₂, τ₃) → layer-cached head consuming the reshaped input.
- `[P1]` Explicit numeric labels on-slide: τ₁ = 24 h, τ₂ = 12 h, τ₃ = 6 h (or whatever the real example uses), showing three different aligned reshapes.
- `[P1]` Narrate what the neural network head is actually doing per period. Angel (12.31): *"maybe also the same, because what actually happens is that there's a neural network for each period, then it starts predicting these periods and then starts just adding them."*
- `[P1]` Add an attention-mechanism introduction mini-panel — see the cross-cutting "attention never introduced" complaint (Section 3.1). Angel (12.31): *"here again we go again to do the informers and attention mechanisms, the capabilities, etc. Here. Because you use this, right?"* Berend clarification: *AERO does not use informers*; informers are only in the magazine paper. Fix: attention introduction lives here; informers are declared *only* in the publications slide.

### Slide 15 — Can AERO match larger models on accuracy benchmarks?
- `[P0]` **This is billed as the scenario slide but it is actually a metrics slide.** Angel (12.31), extended:
  > "the scenario I think is not very clear … you present some results. But which is the scenario? This is an efficiency benchmark. So we'd select these [metrics]. No, no, when you present the … which is the scenario here? This is the scenario slide? This is not the scenario. This is like number of parameters, latency. These are the metrics. But which is the scenario? I mean, where have you tested? How did you get these values for latency error? Where have you…"
  > "Scenario means as you have in agentic [section]. We have 18 nodes. Yes, this is closer. But this is… Yeah, so just change a bit the analogy."
- `[P0]` Add an *actual* scenario slide *before* the metrics card. Minimum content:
  - dataset(s) (e.g., Alibaba cluster trace — 2,000 traces — mention the real number)
  - number of training traces / held-out traces / training period
  - hardware used to measure inference (laptop model, CPU, RAM, GPU if any)
  - which baselines / hyperparameters and tuning procedure ("Bayesian optimization for each model")
  - explicit mention: *"this is the efficiency benchmark scenario"*
- `[P0]` Angel's verbatim answer template (12.31):
  > "What [I] would be answering there… what the scenarios? Then I would say that we trained the model and we did Bayesian optimization for each model and for all of the models in which data in Google cluster. And why don't you put all this instead of saving all this information, why don't you put one slide to explain and save yourself from this kind of question?"
- `[P1]` Scenario slide can be dense-text bullets — Angel explicitly said it does not need fancy visuals: *"why need to be a weird slide to explain? I mean this is everywhere, scenario and metrics. No need to be weird."*

### Slide 16 — Efficiency result
- `[P0]` **Pathformer/AERO confusion on CPU/RAM utilization bars — the chart currently contradicts the story.** Godfrey (11.35), at length:
  > "platformer, which is the [model] you started by critiquing, saying these are heavy models. No sir, the platformer… but what this graph shows that the platformer performs low in RAM utilization. It performs low in CPU utilization, compared almost even lower actually compared to AERO. The question would be in practice, what is the benefit of AERO over platformer? Because in terms of CPU and memory, which will be the constraint for every model, it seems to be performing a lot better than AERO here. So that graph is not clear."
  > "platformer seems to be performing better here. Do you have a justification for this? … That means platformer, we don't have any advantage over platformer."
- `[P0]` The confusion is that the CPU/RAM bars reflect the *infrastructure*'s CPU/RAM while the Pathformer/AERO bars are in a *different* sense (model fit vs runtime utilization). Berend's explanation landed only after an extended exchange: the Pathformer model *cannot run on the edge at all*, so its CPU/RAM "low value" is actually because it does not fit the node; AERO *does* run. The chart as drawn does not convey this.
- `[P0]` **Delete the CPU/RAM infrastructure-utilization bars from Slide 16.** Berend (11.35): *"maybe I should remove a couple of things here because if you know what it [is]… because I only want to show that actual run that it runs better. So we only need the top two figures and the task migrations. And I think this CPU utilization RAM is kind of useless."* Angel/Godfrey agreed.
- `[P0]` Keep on Slide 16: (a) parameter count bars, (b) inference latency bars, (c) MAE/RMSE bars, (d) task migrations or orchestration-quality metric; drop the infrastructure CPU and RAM utilization bars.
- `[P0]` **ModernTCN caveat.** Angel (12.31): *"here it appears that ModernTCN is better for your solution. Much better. Because it has much better memory error and latency. I don't know why with all these parameters, it's that efficient. So it's a convolution. Convolutions are fast."* Resolution: same red-coding treatment as Pathformer — *ModernTCN is accurate but too big to deploy at the edge*. Color-code it red on Slide 12 AND call out on Slide 16.
- `[P0]` **Order the bars so AERO wins first, baselines second.** Same 17 April note — do not start with a baseline winning.
- `[P1]` Narrate explicitly on-slide: *"the argument that [AERO is better] is based on parameters, not on CPU or memory of the running stack."* Angel/Godfrey (11.35): *"Okay, so the fitting is based on the parameters. Not from what we show here."* Berend agreed; put this sentence on the slide.

### Slide 17 — Does a better forecast lead to better scheduling decisions?
- `[P1]` Same scenario rigor as Slide 15 — name the simulator (COSCO), the workload (BitBrains, 500 VMs, 8,000+ samples), the node mix (50 heterogeneous, 60% edge / 40% cloud), the cycle length (2,000 × 300 ms), and the comparison arms explicitly on-slide, not only in notes.

### Slide 18 — Simulation result
- `[P1]` Angel (12.31): *"Yes. Here it's a Pathformer. For me it's faster. But we discussed about this. Or maybe here you could do something."* Reading: the committee is not objecting — the chart correctly shows Pathformer slightly ahead on raw accuracy, and AERO matching on orchestration outcome. But make sure the narration explicitly says: *"Pathformer is 4000× larger and is not deployable; AERO matches it on orchestration outcome at 599 parameters."*
- `[P1]` Consider adding the "on-par with a 4000× larger model" claim-line explicitly.

### Slide 19 — Does AERO hold up when real production traffic shifts?
- `[P1]` Balance the talk-time. Angel (12.31): *"here you spent. I think you spent more time in the left part than in the right one. I would change a bit the balance on how I explained these things and I would motivate more the right part."* The right panel (live phase) is the stronger story and is being rushed.

### Slide 20 — Live deployment results under real-world drift
- `[P1]` Clean. Committee did not stop here.

### Slide 21 — OmniFORE header
- `[P1]` Clean.

### Slide 22 — Train on a service catalogue, forecast any service in it
- `[P1]` The bursty/steady toy visualization is OK but the *bursty* trace is too periodic. Angel (12.31): *"here that's the only slide I talk about attention, but I didn't name attention."* (Note: this quote actually refers to Slide 27/28 — but the bursty-vs-steady art style point survives here too.)

### Slide 23 — Where OmniFORE runs *(currently OmniFORE system model)*
- `[P0]` **Same system-model problem as Slide 10/11.** Angel (12.31):
  > "system model is not like this. Scheduler actor, prediction model. Yeah, an observability stack. So you think this is the system model. I'm saying use… what you're suggesting is then in my mind would look like this."
- `[P0]` **Delete the "regional cluster" / "far edge" split on OmniFORE.** Angel has changed position on the "OmniFORE is for regional" framing. 12.31 (long exchange):
  > "Why you insist that OmniFORE is for the region? Because the person will say that [regional] is an example."
  > "don't focus it. Don't change it at the regional. Because it could be bringing the region when they ask in terms of deployment. Then we can represent at regional data centers which have compute resources. But don't start by saying you design it for the regional case scenario."
  > "okay, so we design it for the problem. Yes, the problem. The need for generalization."
- `[P0]` Reframe OmniFORE's system model as *"one prediction layer serving many services, location-agnostic"* — not *"regional"*. Remove "far edge" / "regional cluster" tags above the figure. Angel (12.31): *"you can remove also far edge and regional cluster. It's like you can put a problem, you can just remove. Just get rid of it. Lightweight [prediction] and generalization."*
- `[P0]` If a system model is retained, it is the **same generic figure** used for AERO (scheduler + observability + ML-model box inside an edge node) — only the box-label changes. Angel endorsed this from 17 April onward and it still applies.
- `[P1]` Angel (12.31, about 6G services question): *"be careful because here won't be careful. What do you mean at 6G you expect this type of services or what services are you expecting especially for 6G?"* → on Slide 6 *and* here, be generic about services ("network + application") rather than naming specific 6G services. The committee can bait on this.

### Slide 24 — No prior method lives in the top-right *(OmniFORE SotA)*
- `[P0]` Same red/green color-coding requirement as Slide 12. ModernTCN → red (heavy per-service), AGCRN/LSTNet → red (per-service retraining), foundation models → red (general-purpose but resource-heavy).
- `[P1]` Right-side clean-up — Angel (12.31): *"24. Yeah, the right part. I don't know, it's a bit messy. I'll clean it up."* Berend agreed.

### Slide 25 — Generalization comes from the training set, not the model
- `[P1]` Clean. Committee did not stop here.

### Slide 26 — Three phases, seven stages, one generalizing forecaster
- `[P1]` Clean.

### Slide 27 — Designing the training set
- `[P0]` **Bursty toy too periodic.** Angel (12.31): *"this is. It's stupid. But I don't know if you can find a better representation for bursty traffic because now it's like periodic. So maybe best is like more spiky."* Redraw with an actual spiky, irregular pattern for bursty; keep the steady trace clean.
- `[P0]` **Introduce attention mechanism here.** This is the one place in OmniFORE where attention is explicitly leveraged, and it is also the cleanest place to define it. Angel (12.31):
  > "that's the only slide I talk about attention, but I didn't name attention. I think that's probably should put attention mechanism."
  > "for me I would… I mean, I would spend a bit more. I could spend a lot of time there. But no… no need to spend. But I mean some introduction you need it. It's true because. Okay, all models forget. But some have better memory."
- `[P0]` Add a *Current models forget past points* sub-panel (or a new slide 27b). Berend's own proposal, accepted: *"I could have another problem slide here where I say something about that models forget data points that are far in the past."* Frame it as *"attention gives OmniFORE longer effective memory → better at generalization across services."*

### Slide 28 — Putting every service on the same scale and letting the model focus
- `[P1]` Clean. The "why attention?" chip is the right landing spot for the attention introduction.

### Slide 29 — Tuning so it transfers
- `[P1]` Clean.

### Slide 30 — Does picking smart training data really help?
- `[P0]` **Title "smart picking" not introduced.** Godfrey (11.35): *"what you do resource the smart picking speaking. Does speaking smart training data really help? Because somewhere I think you're talking about the clustering impact of clustering. So some because in the steps discussing clustering optimization parameter optimization. So how does someone map this to the clustering for instance, very hard."*
- `[P0]` Rename the slide title: **"Does clustering-based training data selection really help?"** or **"Impact of clustering on generalization"**. The term *smart picking* must either be (a) introduced earlier in Phase 1 / Slide 27 (with a clear link to clustering), or (b) dropped entirely.
- `[P0]` Berend (11.35): *"also the title I don't want to put cluster clustering. For me it's the first time smart picking is coming in. So the people now [need] to understand what is smart picking."* Resolution from the session: prefer *"impact of clustering"* wording.

### Slide 31 — Smart picking wins by about twenty percent, on every metric
- `[P0]` **Drop the silhouette-score paragraph from this slide.** Angel (12.31): *"31. Well, there's a problem here. Again. I should not talk about silhouette score[ing]."* Berend: *"remove silhouette score. No, I don't. I don't understand what I have written here."*
- `[P1]` Keep the three primary metrics (MAE, RMSE, SMAPE). Silhouette is a diagnostic, not a headline.
- `[P1]` Same "impact of clustering" renaming logic as Slide 30.

### Slide 32 — Test it on a dataset it has never seen
- `[P1]` Layout: put plots on the left, conclusions on the right. Angel (12.31):
  > "33. Maybe it's better to have the plots on this part and then the conclusions on the right. So just to explain first the bars more or less. And then okay, maybe you can reduce a bit the fonts on minus these. But this can be like on the left on the right side as explained … First always it's better to explain the plot and then the conclusions in the summary etc. Are either below or on the right part because it's much easier."
- `[P1]` Reduce font on sub-findings to fit the re-layout.

### Slide 33 — Predicts any new service effectively, no retraining needed
- `[P1]` Same left-plot / right-summary layout fix as Slide 32 (Angel grouped them together).

### Slide 34 — AgentEdge header
- `[P1]` Clean.

### Slide 35 — No system can turn operator intent into orchestration actions
- `[P1]` Clean.

### Slide 36 — Where AgentEdge runs *(currently AgentEdge system model)*
- `[P0]` **Kubernetes placement is confusing.** Extended exchange, 12.31:
  > Angel: "it's confusing having Kubernetes API here, because Kubernetes should be here… where is Kubernetes in the infrastructure? If it's in the infrastructure. If it's infrastructure, then it's not service orchestration."
  > Angel: "Kubernetes is green. Lay in the green part."
  > Angel: "infrastructure lay… infrastructure layer. It's not orchestration layer for sure. Now if it's service infrastructures, it's like things that are running. Yeah. Things are not control plane. Things are like. Yeah."
- `[P0]` Fix: **Kubernetes API sits inside the service-orchestration layer (green), not inside the infrastructure layer.** The infrastructure layer is metal + services. Service orchestration is split into *inter-node* (above) and *intra-node* (below); prediction models feed either level. Relabel accordingly.
- `[P0]` **Prediction-model box must be repositioned.** Angel (12.31):
  > "if you want here to say that this is a service orchestration layer, we don't care if it's multi or whatever. Kubernetes is in the green part, not in the infrastructure."
  > "the models talk to both. … if you want to make this compliant with this, all this part needs to be green because models talk to both."
- `[P1]` Upper-left "intent-observability-planning-action" lifecycle (PARES cycle) is rendered too small; Angel says *it is OK* but the layout can be cleaned up. Keep.
- `[P1]` Angel (12.31): *"this likes. It's too much. I think now it's like boom, too much."* — remove the redundant lower-right detail box from the AgentEdge system-model slide; the PARES lifecycle graphic on the left carries the same information.
- `[Q]` Whether to split the AgentEdge system-model into **two slides** (paper-level architecture + AgentEdge-block highlight) as 17 April originally suggested — currently v1 keeps it as one dense slide. Acceptable if the above relabeling is done.

### Slide 37 — Every prior system is missing load-bearing capabilities *(AgentEdge SotA)*
- `[P0]` **PARES is introduced inside this comparison table — wrong order.** 13.08:
  > Berend: "after analyzing a lot of papers from state of the art machine learning and agentic papers, we came to these five capabilities PARES and then before to explain PARES before any… anything."
  > Angel: "more like an answer to the question. And then. But you can do it also like this. Okay. I mean I'm just saying not to put the whole slide before [introducing PARES]."
- `[P0]` **Split the slide into two:**
  - **Slide 37a — What is an agent? (PARES)** — define *Perceive, Act, Reason, Evaluate, Sustain*. Frame the recurring theme: *"many papers claim to be agentic but are single LLM calls without real perception or action."*
  - **Slide 37b — State of the Art & Baselines** — the capability-matrix table, now safely referring to PARES by name.
- `[P0]` **State-of-the-art entries need better names.** Angel (13.08): *"papers are not clear. Find a better name for 'more service orchestration'. You know, it's like paper names if possible. If as it is 'Agent Edge', for example. If they have. Or just put the numbers and the numbers and the reference as you prefer."* Use published paper titles where available, else reference numbers with a footnote.
- `[P0]` **Explain why ReAct and LATS are *adapted baselines*, not native orchestration baselines.** Extended exchange (13.08):
  > Angel: "you need also I think to speak a bit about [why no native baseline]… if there are already agentic papers or… at some point you compare to single agent… I don't know, it was a bit for me, it's like the goal is to explain state of the art. And the state of the art every… everybody is claiming agentic systems, but what they do is a simple LLM call based [tool use]."
  > Angel: "none of these function in the setting we want. Okay, so I could delete it as well. And it's not about deleted, it's about explaining properly. I mean whatever you explain to me now, it's a matter of explaining to anyone."
- `[P0]` On-slide phrasing: *"no prior system satisfies PARES across the whole orchestration cycle; we therefore adapted ReAct (reason-act loop) and LATS (tree-search over LLM rollouts) as our comparable baselines by retargeting them to our tool surface."*
- `[P1]` PARES-green ticks should be applied only to *our baselines* (ReAct/LATS when adapted) and *AgentEdge*. Other rows (generic agentic claims) should mostly be white/empty with one or two partial ticks. Angel (13.08):
  > "for me I would try to combine everything as state of the art somehow or I don't know if it makes sense to have the others. It could make sense. Like I put PARES here, I put multi-agent and agent framework and then I could have… our baselines which we are comparing against is all of this like what we have now and we have PARES here."
  > "so the others would have some in the PARES some green and some [white]. They would have all green the other ones our baseline."
- `[P1]` Color code the baselines differently from the rest of the SotA rows ("differentiate the SotA with what we adapted to create the baselines"). Suggest: SotA rows neutral gray; adapted baselines orange/amber; AgentEdge full color.

### Slide 38 — Each pain-point forces exactly one design decision
- `[P1]` Clean. The rationale table survived review.

### Slide 39 — Graph-of-graphs, four specialized agents
- `[P1]` Clean.

### Slide 40 — How the agent reads intent and observes the cluster
- `[P1]` Clean.

### Slide 41 — How the agent plans, simulates, and executes safely
- `[P0]` **Orange color inside the ActSimCrit block is miscoded.** Godfrey (11.35): *"why this is an orange? Because you said this orange is the agent [block] means this is not part of AgentEdge."* Fix: recolor the ActSimCrit sub-flow to match the Planning-agent color, not the external-agent orange.
- `[P1]` Delivery note: Godfrey (11.35): *"Even here why this is an orange?… the color code, the color choice. And also this slide can be a lot better. Yeah, that's trouble explaining this basically as it's. It's like it's very hard to explain what happened."* The slide is information-dense; rehearse the narration slowly.
- `[P1]` Angel (13.08): *"I miss infra agent. So for in terms of completeness, you need to put somehow to appear at least the infra [agent]."* Add a small infra-action chip on the Planning-loop output so the plan visibly hands off to the Infra Action agent. Berend proposes: *"I can just put it here on the bottom and like the plan goes to the infra."*

### Slide 42 — Infrastructure simulator, testbed for safe agent evaluation
- `[P0]` Delivery skip — this slide was rushed in rehearsal. Angel (13.08):
  > "here you need use, you know, in the 42 a better explanation. Now I think from here you started a bit skipping."
  > "try to reduce a bit the first part. Or try to rebalance a bit. But try to explain this a bit better. I mean, the different scenario. Because for me it's important. This should be maybe be with the scenarios."
- `[P0]` Consider merging Slide 42 with the AgentEdge scenario table (currently implicit on Slides 43/47). Angel: *"this should be maybe be with the scenarios. Because this is… No, this. This is the scenario. No. Okay. This [is the] arsenal. But the previous is a topology, right?"* Fix: frame Slide 42 as **"AgentEdge Scenarios & Simulator"** — the tier table + the 12-API surface + the 3-scenario description + the 8/20/35-node scalability scenarios, all in one place. Angel (13.08): *"I could collapse this into one slide. The most important for me is how to… to at least to explain the key parts. Spend the time that needed not to just keep it just [skip]."*
- `[P1]` Angel (13.08) on his own distaste for tables: *"[yes, tables are boring] but it's not only about making fancy or simple things and be aesthetically good presentations about. Okay, yeah, we have this. And someone can go here and ask some ask you something if they have any question… these slides are fundamental for any presentations technical especially."*

### Slide 43 — Does the multi-agent design outperform single-agent baselines?
- `[P0]` **Introduce the "single-agent baseline" concept.** Angel (13.08): *"the single agent part that I don't know now how we will change it. But try to introduce a bit the concept of single agent."*
- `[P0]` **Merge scenario-table with infrastructure context.** 13.08:
  > Angel: "what you don't need here is this for example, or this is useful but you can also say it. So for me I would try to merge probably this part which is with the infrastructure part. So to say these are the scenarios and these are. This is the infrastructure and we consider three different scenarios. Blah blah blah. I don't know. I would spend one minute for someone to understand one second."
- `[P0]` **Split confusion 1–3 vs 4–6 scenarios.** 13.08:
  > Berend: "the reason why I split like this is because we first have this then scenario one and then this is basically scenario two… This is four, five and six."
  > Angel: "but you don't replicate a similar table for this and for the scenarios of the other. No. So do it. I mean, why don't you replicate at least to say. I mean, try to someone to understand and follow."
- `[P0]` Fix: either replicate the scenario table at each result-family (Slide 43/44 scenarios 1-2-3, Slide 47/48 scenarios 4-5-6) or produce **one master scenario table on Slide 42** and reference it explicitly at each result slide. Prefer the single master table.

### Slide 44 — Multi-agent architecture beats every SOTA single-agent baseline
- `[P1]` Blow up AgentEdge, ReAct, LATS — the three bars that matter. Berend own proposal (13.08): *"I should blow up here the remove everything except the AgentEdge, ReAct and LATS. And then have some sort of figure or explanation explaining what they are."* Angel agrees conditionally: they must be defined in SotA first (Slide 37).

### Slide 45 — Is the twin structural or decorative?
- `[P0]` **Digital-twin ablation semantics under-defended.** Long exchange (13.08):
  > Godfrey: "why for example, why without digital twin you have this failure? I mean, why the success rate reduces without digital twin?"
  > Berend: "because here we have the simulated output after doing the actions is directly critiqued on this new state of the system. And the LLM is critiquing that state of the system."
  > Godfrey: "but if you go to the… even here, when you execute on the infra, you may fail. But then you feed again the plan. So you just execute one plan."
  > Angel: "still for me it's not clear, to be honest. I mean, if we, if we need to have the… I don't understand why the fair comparison for me would be [this]."
- `[P0]` **The question the committee wants answered on-slide** (not only in speech): what does the *WITHOUT digital twin* arm actually do on plan failure? Three candidate answers were explored in the session:
  1. *Single-agent fallback* — the Infra Action agent locally mutates the plan without re-invoking Planning. (Current implementation.)
  2. *Full re-planning on failure* — go back to Planning agent with a new API-call, which Angel argues is the *fairer* comparison.
  3. *No retry* — one-shot execution; failures are terminal.
- `[P0]` **Resolution recommended:** rewrite the ablation so that *WITHOUT* = option 2 (full re-planning on failure). This isolates the digital twin's value clearly — *"without the twin, how many re-plans does it take to succeed?"* The API-call variance (10.9 ± 1.1 vs 8–517 ± 109.4) then reads as *retry cost*. Angel (13.08):
  > "for me, I would prioritize the result over the intelligence of an agent. I mean, I don't care if it's. If the green part is. Or the red are intelligent. But we have 70. I mean, if you tell me that going back from the green one to the plan which is one API call brings us to 100 [success]. And this is a dummy. If-else I would go with this."
- `[P0]` **Pre-seed the defense answer for "why 78.3 %, not 100 %?"** Godfrey (13.08):
  > "Y is 78.3, not 100% because you're excluding the plan after validation. What is causing the draw here? Because after validation you get a success rate of this and then the presentation somewhere you said we validate. Once you validate, the plan is always guaranteed to be executed correctly. Is it be a wrong plan? What is changing here is the infrastructure changing after validation. So the agent still comes up with infeasible things."
- `[P0]` Candidate answer (to rehearse): *"the residual ~22 % failures are attributable to (a) the critic LLM occasionally admitting an infeasible plan to execution, and (b) a small mismatch between the digital-twin state and the live-infrastructure state at execution time. The twin is a high-fidelity but not 1:1 sandbox — we explicitly scope this limitation on the slide."*

### Slide 46 — Sandbox validation reduces costly trial-and-error
- `[P1]` Keep the 1.47× / 10× headline. The variance number (109.4 → 1.1) is the strongest operational argument in the whole AgentEdge chapter; do not bury.

### Slide 47 — Does the agent keep saving energy as infrastructure grows?
- `[P0]` **Single-scenario-table tie-in.** See Slide 43 note — the 8/20/35-node scenarios must be previewed on Slide 42's master scenario table.
- `[P0]` Re-render the power-saved plot with **the same y-axis scale across all three node-counts**. Angel (13.08):
  > "it's bad that the scale. Usually the scale should be the same in general. Yeah, always to be visible. … if you look at the plot, it seems pretty interesting. But actually this percentage reduction is not much. This is quite a lot. And there's no [visual reference]."
  > "the scale here could be from 0 to 1,300. And then you could have this part like this. This would be like this. And this would be like as it is. But the scale here would be the same. And then you visually you could see this. This arrow would be something like this."
- `[P0]` **Do not switch to percentages.** Angel explicitly withdrew that earlier suggestion (13.08): *"When did I tell you [percentages]? I didn't tell you to put percentages. Maybe I told you. What does it mean, 3,300? Yeah, but now this one. But it's one thing what does it mean, 300. And another thing, replace this with percentages. I'm not saying."* Keep absolute watts; fix scale and anchor.

### Slide 48 — Energy saved vs baseline, response time grows with scale
- `[P0]` **Must have a clean answer ready for: "why does 20 nodes beat both 8 and 35?"** Godfrey (13.08):
  > "This is the graph where you had the team nodes [performing] better. Yeah, I was thinking about maybe I just deleted. I don't like this graph. It appears in the [thesis]. Whether they come with a note, you [need to] page your thesis as well. Sometimes they come with notes because they are brain. So we must be very careful now to define this because the question would be this was the optimal thing. What happens at 19, what happens at 22? Is it possible that once we get here there's a chance that after 35 we get a bigger graph? Why was the optimal 17 better than this?"
- `[P0]` **Pre-seed the defense answer.** Berend's own version, acknowledged by Godfrey: *"at 35 nodes with all of these metrics [the planning agent is] completely bloated and it has to read all of these metrics. So I think in order to scale properly to a large set of nodes, you have to come up with some context engineering."* Godfrey's refinement: *"either we say we just did this to evaluate the complexity of the problem … someone said why 8 which is a smaller context problem, why did it perform well? … maybe 18 [nodes] were saturated so we couldn't do better than 18. We have more free space and for random choices we get correct answers. Then why 35? So I said that just in case that comes up. You must have a clear way."*
- `[P0]` On-slide, add an explicit caveat: *"the 8/20/35 points characterize the behavior of a single planning-agent context-window configuration; scaling beyond 35 nodes requires context engineering — see Future Work."* Tie directly to Slide 53 future-work bullet.
- `[P1]` **Remove the latency/speed plot that shows 20-node case as "faster than 8 and 35"** if it triggers more questions than it answers. Berend (13.08): *"here my name. Yeah, this. I should have never put that. I don't understand this. I mean, I cannot understand how in this scenario we solve it. It takes. It is faster than the other one now. Just get rid of that."* Angel countered: *"no, they will have the thesis … but maybe they will come with printed, etc, but they may ask things from the thesis. So you need to have a reference."*
- `[P1]` **Bring one printed copy of the thesis to the defense.** Angel (13.08): *"you should have at least one for yourself in the presentation. Also for them, I would suggest. But maybe they will come with printed, etc."*

### Slide 49 — Three sub-problems answered *(Objective / Publications recap)*
- `[P0]` **Slide 49 purpose is unclear — it reads like a second conclusion.** Godfrey (13.08, emphatic):
  > "I think 50 and 50 it was the same. I mean then after this in the conclusions was a bit. 50 already seemed like conclusion. This is something that for me it was confusing."
  > "you start already one conclusion, then you go to the other conclusion without numbers. Okay, so I think just get rid of this one here."
- `[P0]` **Restructure the end-of-deck flow.** Extensive discussion (13.08). Preferred resolution:
  ```
  Current v1 order:
     49 (sub-problems + publications)
     50 (stack-with-contributions — operator impact)
     51 (stack-with-contributions dimmed — future work header)
     52–54 (future-work sub-problems)
     55 (conclusions)
     56 (questions)
  
  Proposed v2 order:
     49 → merge the "three sub-problems answered" panel INTO slide 50 on the left,
          and MOVE the publications into Q&A (56) or to after conclusions.
     50 = objective assessment + stack populated with contributions (left half)
          + publications mapping (right half). Keep operator-impact block.
     51 = future-work header — lit/dimmed stack as today, BUT tie problem 1 (reliability)
          to only one location (top OR bottom, not both — see Slide 51 note).
     52 / 53 / 54 = future-work sub-problems with extra depth (see Section 5).
     55 = conclusions (three claims + publications recap if moved here).
     56 = questions.
  ```
- `[P0]` **Publications formatting:**
  - Drop the J1/J2/C1 codes — already done in v1 (full names on-slide). Keep.
  - Godfrey (11.35): *"I should just mention that 8 publications, 4 journals, 3 conferences, 1 book chapter. But you can… you can. You can. You can associate them. For me it's both of them. And it's good to say it, but you can say it in 10 seconds."*
  - Angel (11.35): *"you can speak in general. So this work in general was ended up… in 8 publications, 4 of them journals, 3 conferences and one book chapter. And here you could see how these are associated with the colors correspond to the different [contributions]."*
  - **Color-code J4 correctly.** Godfrey (11.35): *"AERO is not… the magazine is not about AERO too. I delete the wrong one."* Berend and Godfrey disagreed live on whether J4 (the Informers / Communications Magazine paper) maps to AERO or OmniFORE. Resolution: **check the magazine paper's content** — if the results are on prediction improvement it is AERO; if on generalization it is OmniFORE. Angel (11.35): *"It's about forecasting trends is mostly about attention mechanism. And attention mechanism is about generalization. But also AERO uses attention mechanism… I think the results we had in the paper was about improving prediction."* If results are on prediction-quality improvement → color it AERO. Berend had (for the thesis) already copy-pasted one assignment; Angel: *"it's minor, but yeah, in general, as I close. It's about… check, double check."*
- `[P1]` If publications are *moved* to after conclusions, Slide 49's left half (RQ-to-contribution + anchor numbers: 599, 30.41 %, 2.76×) can merge directly into Slide 50.
- `[P1]` Narration guideline (Angel, 13.08): keep the publication-reference introduction short — *"10 seconds"* — and use the color code to do the heavy lifting visually.

### Slide 50 — State-of-the-art operator stack
- `[P0]` **Slide 50 is confusing because it appears to repeat the problems stack from Slide 3.** Godfrey (11.35), emphatic:
  > "what is the purpose of this slide? For sure you didn't know. I didn't why so like I started with slide one. So here's like the problems and then in 50 I show the again because we didn't discuss them here even what it for me it was hard just to… this could come in the conclusion, the wrap up of the [contribution]."
  > "it was hard to follow to connect because this one I [have] seen it before when you're starting then it appears again here then same structure here. Like I know like it's like here's the problems. Yeah and then I basically have bring back the same slide bring the solutions and where are they placed and then we go back to problems like we could start the next presentation."
- `[P0]` **Clarify Slide 50's role.** v1 intent: "payoff slide — the same four-layer stack from Slide 3 now populated with contributions." Committee reading: "you are showing the original problems *again*; it feels like we are starting a new presentation." Fix by *title* and *annotation*:
  - Title change: "Where the three contributions live" or "Contributions map to the stack", not a stack that looks like slide 3.
  - Annotate each layer with the contribution name (AERO / OmniFORE / AgentEdge) *in* the layer, not as a legend.
  - Explicit text: *"compared to Slide 3, layers 1–3 are now populated; layer 4 is unchanged."*
- `[P0]` **Operator-impact block is good — keep.** Committee did not re-raise; this was the major 17 April rewrite and it landed.
- `[P1]` Can merge the "three sub-problems answered" card from Slide 49 into Slide 50's left half (see Slide 49 note).

### Slide 51 — Future Work · Agentic Era header
- `[P0]` **Problem 1 appears both at top and bottom — remove duplication.** Godfrey (13.08):
  > "what is confusing to me here is like you have problem one and above and below. And it was a bit strange in the beginning… the first slide here you have problem one again, problem one. And reliability. Trust goes… why don't you keep it just one. Just problem one. And then problem two and three goes to. Okay, so yeah, just remove it. Yes. From the very bottom."
- `[P0]` Fix: render problems 1/2/3 in one tier (top), solutions/contributions in the bottom tier. Do not list problem-1 twice.

### Slide 52 — Benchmarks do not exist yet
- `[P1]` Content is fine; keep. Angel did not object to this sub-slide in 21 April.
- `[P1]` Delivery: do not dismiss future work as *"use another model"*. Angel (13.08, emphatic):
  > "here again here the goal is to show also to motivate. So someone now comes to start a PhD. It's not about telling him use another model because this does not have a big value. So it's about… really a clear, clear directions. Clear and more research wise directions than just use other tools."

### Slide 53 — Latencies accumulate to tens of seconds
- `[P0]` **Tie directly to the 35-node scalability question** (see Slide 48). This slide is where the "context engineering" future direction lives. Berend (13.08): *"what really a problem is like okay, I had tunnels, then I add the NBI and that's like 20 tools. And then I add Kubernetes MCP [at] which point are tools coming? And then everything breaks."* Put that concrete anecdote on-slide or in speaker notes.
- `[P0]` Expand the *"smaller fine-tuned models could break the latency barrier"* bullet into a real research direction, not a tool-swap. Angel (13.08): *"it's like smaller function model models can break the lineage. Okay. It's like what is the challenge? I mean it's not that clear. It's like use them another model and you will do it."*
- `[P1]` Add a 6G integration angle. Angel (13.08): *"as a future work, for example, one thing that I would put would be also how challenges on including this to 6G. Like to show that big picture to go back to the signal theory and communications department. It's also their background. For example, you will have different agents in the core in the RAN. It's like the paper, the magazine that we wrote for one proposal."*

### Slide 54 — Parallel instances conflict on shared infra
- `[P1]` Content is aligned with what Angel asked for on 21 April — coordination, model-agnostic, conflict detection. Keep.
- `[P1]` Can reference the magazine paper (*"parallel agents in core/RAN"*) explicitly — Angel hinted at this.

### Slide 55 — Three layers · one systems thesis *(Conclusions)*
- `[P0]` **Rebalance: highlight 2–3 numbers per contribution as bullets, not just 599 / 30.4 % / 2.76×.** Angel (13.08):
  > "these are the three. So the three big conclusions for your thesis. Are these for you like these specific numbers you need to highlight: 599, 30.4 and 1.2. I mean exactly. Because they are not these numbers that need to be highlighted only. And there are for example 1.2. Now I don't remember. I remember. 1.47. 2.76. I don't know, 1.47 also I think somewhere so you can focus more on the text. Having us bullets some numbers than focusing on the numbers. Because it's not about less. Less error. It's fine. Or yeah, It's just to put some quantification."
- `[P0]` Suggested 2–3 per contribution:
  - AERO: 599 parameters, 8× lower error under drift, 99 % fewer SLA violations.
  - OmniFORE: 30.41 % lower MAE vs ModernTCN, +20.66 % MAE gain from clustering, zero-shot on unseen cloud.
  - AgentEdge: 2.76× ReAct success, 1.47× with-vs-without twin, ~10× API-variance reduction.
- `[P1]` **Publications block — decide placement.** Angel (13.08):
  > "I'm not sure if you could have a very high level on future work summary. As a last conclusion. Like to finish with this and say that. And to be honest, the publication slide could fit even after conclusions having conclusions and say, okay, the work in this thesis has been published. So I can remove this slide. I could put publication mapping. But then I don't need the publications here."
- `[P1]` Recommendation: keep publications on Slide 49/50 combined panel; reference them on Slide 55 in one sentence: *"the three contributions together appeared across 8 peer-reviewed outputs — full list on Slide 50 and Q&A."*

### Slide 56 — Questions
- `[P1]` Publication recap color code must match Slide 49/50 exactly.
- `[P2]` Committee did not stop here. Keep.

---

## 5. Recommended Q&A Backup Slides

Based on what the committee bait-tested, prepare at least the following backup slides (hidden behind Slide 56 or in an appendix file):

1. **AERO vs Pathformer "CPU/RAM utilization"** — extended explanation of why Pathformer's low CPU/RAM means it *does not fit*, not that it is better. Include one chart: "where each model runs" × "fits in edge budget? yes/no".
2. **OmniFORE deployment granularity** — "OmniFORE can run at far edge, regional, or cloud; we designed for *the problem of generalization*, not for a layer." One-line answer. (Angel repeatedly warned against saying "we designed for the regional cluster".)
3. **Digital-twin 78.3 % vs 100 %** — rehearsed answer: critic admits a residual % of infeasible plans; twin-live mismatch; limit explicitly scoped. See Slide 45.
4. **Why 20 nodes beats 35** — context-window saturation explanation; tie to future-work Slide 53.
5. **Why not compare to other "agentic" 6G papers** — because they fail PARES; we adapted ReAct / LATS instead. See Slide 37.
6. **6G services expected** — network + application both, non-committal on mix. (Angel warned about reviewer bait on "what kind of services?")
7. **Magazine paper J4 contribution** — depending on fact-check, AERO or OmniFORE. See Slide 49 note.
8. **50 ms vs 150 ms budget origin** — cite the edge-orchestration reference.
9. **Informers vs Pathformer vs AERO** — AERO does not use informers; informers appear only in the magazine; the main AERO-vs-SotA comparison is against Pathformer.
10. **Can AERO apply to other 6G signals?** — yes, any time-series (user traffic, physical resource blocks). Berend's verbatim answer rehearsed in 11.35.

---

## 6. Delivery & Body Language (Carryover)

The 17 April delivery critique (clock-checking, screen-reading, rushing) is *mostly* resolved in v1 — neither Angel nor Godfrey raised it in 21 April. The two remaining items:

- `[P1]` **Talk-time balance per panel.** Angel (12.31): *"here you spent. I think you spent more time in the left part than in the right one. I would change a bit the balance on how I explained these things and I would motivate more the right part."* Right-panels on Slides 19, 24, 32 are being shortchanged.
- `[P1]` **Understand the question fast.** Angel (11.35), on the Pathformer/CPU exchange:
  > "you need to try to understand the question and faster and go to where you have. You have to go… the faster you understand something… this was a good example on this situation."
  > Later: *"it's experience or I don't know what it is. Sometimes it's also I have to filter. Filter what the problem is faster."*

Rehearsal notes:

- Practice reframing committee questions *before* answering — *"so the concern is X; let me address X…"*
- Expect bait questions specifically on: 6G services types, informers vs Pathformer, regional vs edge deployment of OmniFORE, agentic 6G papers, digital-twin fidelity.
- `[P2]` Bring one printed copy of the thesis to the defense (Angel, 13.08).

---

## 7. Timing Plan (Unchanged From 17 April)

v1 rehearsal ran ~55 min — inside target. The committee's reaction was *"it was 55 minutes, but better"* (Angel, 11.35). No timing re-plan is required.

Micro-trim targets (each worth 30–90 seconds):

- Slide 13 redundancy (two halves say the same thing) → 60 s
- Slide 24 right-side mess → 30 s
- Slide 36 redundant lower-right box → 30 s
- Slide 42 rushed explanation → compensate from above trims (give it back 90 s)
- Slide 49–50 duplication → merge → 60 s
- Slide 51 duplicated Problem 1 → 15 s

Net result: roughly neutral on time, better-distributed across sections.

---

## 8. Missing Content Inventory (v1 → v2)

Only items the committee said are still missing from v1:

| Ref  | Missing element                                                                                    | Slide target           | Priority |
|------|----------------------------------------------------------------------------------------------------|------------------------|----------|
| M1   | Explicit "why prediction?" motivation sentence (orchestration loop needs forecasts)                | 02 / 03 / 04           | P0       |
| M2   | Generic AERO system model (scheduler + observability + ML-model box inside edge node)              | 10 (redraw)            | P0       |
| M3   | Rewritten "where AERO runs" framing — capability, not design constraint                            | 11                     | P0       |
| M4   | AERO SotA color coding: red = undeployable, green = lightweight                                    | 12                     | P0       |
| M5   | Rebuilt AERO efficiency chart: drop CPU/RAM infra bars, keep parameters + latency + task migr.     | 16                     | P0       |
| M6   | AERO Scenario slide: Alibaba traces, training split, reference hardware, BayesOpt tuning            | 15 (prepend)           | P0       |
| M7   | Attention-mechanism introduction (either AERO Slide 14 or OmniFORE Slide 27)                        | 14 or 27               | P0       |
| M8   | "Current models forget past" + "attention → longer memory → generalization" framing                | 27 (append)            | P0       |
| M9   | Generic OmniFORE system model (remove "far edge" / "regional cluster" tags)                         | 23                     | P0       |
| M10  | OmniFORE SotA color coding: same red/green treatment as Slide 12                                    | 24                     | P0       |
| M11  | Slide 30/31 title rename: "impact of clustering", silhouette-score removed                          | 30 / 31                | P0       |
| M12  | Kubernetes relocated to service-orchestration layer; infra = metal + services only                 | 36                     | P0       |
| M13  | PARES capability contract introduced on its own slide BEFORE the SotA table                        | 37a (new)              | P0       |
| M14  | AgentEdge "adapted baselines" narrative (why no native baselines; ReAct / LATS adapted)            | 37b                    | P0       |
| M15  | Single-agent baseline definition                                                                   | 37 or 43               | P0       |
| M16  | Master AgentEdge scenario table (S1-S3 + S4-S6 + node counts + hardware + tasks)                   | 42                     | P0       |
| M17  | Digital-twin ablation semantics — re-define "WITHOUT" as full re-planning; pre-seed Q&A            | 45 + backup            | P0       |
| M18  | Scalability plot with uniform y-axis (0–1300 W across all three node-counts)                        | 48                     | P0       |
| M19  | Slide 50 retitle + annotation so it does not read as "start of a new talk"                         | 50                     | P0       |
| M20  | Slide 51: delete duplicate Problem-1 at the bottom                                                 | 51                     | P0       |
| M21  | Future-work (52/53/54) rewritten with research challenges, not "use better models"                  | 52 / 53 / 54           | P0       |
| M22  | Conclusions (55) with 2–3 anchor numbers per contribution as bullets                               | 55                     | P0       |
| M23  | Pagination redesign — one large page number, darker, no bottom strip                                | all                    | P1       |
| M24  | Bottom infrastructure layer recolored gray (across slides 03 / 04 / 50 / 51)                       | 03 / 04 / 50 / 51      | P1       |
| M25  | Remove orange inside ActSimCrit sub-flow; align with Planning-agent palette                        | 41                     | P1       |
| M26  | Infra Action agent chip at end of Planning loop                                                    | 41                     | P1       |
| M27  | Q&A backup slides (10 topics — see Section 5)                                                      | 56 / appendix          | P1       |
| M28  | Fact-check J4 (Communications Magazine) contribution assignment                                    | 49                     | P1       |
| M29  | Print one bound copy of thesis for candidate's own reference                                       | logistics              | P1       |

---

## 9. Scientific / Methodological Notes

Content-level corrections from 21 April, beyond presentation style:

- `[P0]` **AERO's advantage is parameters, not CPU/RAM.** The pitch "AERO is better because it uses less CPU/RAM" is wrong — Pathformer uses less CPU/RAM when measured, precisely because *it does not run on the node*. The correct pitch is: *"AERO has 599 parameters and 0.38 ms inference at the edge; Pathformer has 2.4 M parameters and does not fit."* Orchestration quality (task migrations, SLA) is on-par with Pathformer; that is the whole point.
- `[P0]` **OmniFORE is a problem about generalization, not about regional deployment.** Do not claim OmniFORE was "designed for the regional cluster." Say: *"OmniFORE solves the generalization problem; it can be deployed at any layer, and we demonstrate it at the regional cluster because that is where cross-service forecasting is operationally relevant."*
- `[P0]` **The digital-twin ablation "WITHOUT" arm must be re-defined** for the comparison to isolate the twin's contribution. Current implementation falls back to single-agent mutation; Angel prefers full re-planning on failure. Either fix the code OR scope the claim on-slide. **Do not leave the semantics ambiguous.**
- `[P0]` **Scenarios 8/20/35 nodes — the optimum at 20 is a context-window effect.** Pre-seed this explanation on-slide 48 AND in future-work 53 AND as a Q&A backup.
- `[P0]` **ReAct and LATS are adapted baselines.** Never claim they were native agentic orchestration baselines — say *"we adapted them because no prior system met PARES."*
- `[P0]` **PARES is the formal contract that defines what "agent" means in this work.** Introduce it *before* using it in the SotA table. Otherwise the audience sees a capability table with an unexplained column called PARES.
- `[P1]` **Pathformer parameter count sanity.** Berend quoted 2.4 M throughout the deck; Angel did not object. Keep.
- `[P1]` **Informers.** AERO does not use informers. Only the Communications Magazine paper does. Remove any residual mention of informers in the AERO section (candidate thought he had cleaned this; double-check slides 11–18).
- `[P1]` **ModernTCN.** Convolutional, therefore fast on CPU; Angel flagged its speed as potentially misleading. Color-code it red for "heavy by parameter count" and keep the on-par latency but call out the parameter penalty.

---

## 10. Open Structural Questions

Questions the committee left unresolved; candidate should decide before building v2.

1. **Q1.** Where does the PARES introduction slide (37a) sit — standalone, or appended to Slide 36 (AgentEdge system model)? Recommendation: standalone, short (one slide), immediately before 37b (SotA table).
2. **Q2.** Should the "digital twin WITHOUT" arm be re-implemented with full re-planning on failure, or stay as single-agent fallback with the semantics explicitly scoped on-slide? Recommendation: **re-implement if feasible**; else scope explicitly.
3. **Q3.** Publications placement: (a) merged into Slide 49/50 left/right panel, (b) after conclusions Slide 55, or (c) on the Q&A slide 56? Recommendation: (a) with a one-sentence recap on (c).
4. **Q4.** Should the AERO and OmniFORE system-model slides share *one generic* figure with different highlights, or each carry their own? Recommendation: share (reuses 17 April consensus).
5. **Q5.** 6G service subtype claim — drop entirely or bracket as "we focus on microservices generically, both application and network"? Recommendation: bracket, non-committal.
6. **Q6.** Slide 48 "response-time faster at 20 nodes" plot — keep (with caveat) or remove? Berend wants to remove; Angel wants to keep because the thesis contains it and the committee will have the thesis. Recommendation: **keep** with on-slide caveat pointing to future-work 53.

---

## 11. Contradictions And Judgment Calls

- **C1.** Angel on 17 April: *"prefer percentage framing over absolute-number framing (energy)"*. Angel on 21 April: *"I didn't tell you to put percentages … percentages do not make sense to compare because it's like 20%. You don't know."* Resolution: **keep absolute watts on Slide 48, but share the y-axis scale across the three scenarios.**
- **C2.** Angel (12.31) on OmniFORE regional framing: *"don't focus it. Don't change it at the regional."* Earlier versions of the slide emphasized regional deployment. Resolution: **reframe as a problem of generalization, location-agnostic.**
- **C3.** Berend vs Angel on J4 (Communications Magazine paper) contribution color. Berend: *"it's about AERO because the magazine was for me AERO."* Angel: *"it's about forecasting trends is mostly about attention mechanism. And attention mechanism is about generalization."* Resolution: **fact-check the paper's primary result, then color accordingly.**
- **C4.** Godfrey vs Berend on digital-twin failure semantics. Godfrey: *"after validation you should loop back to Planning, not fall back to single-agent."* Berend: *"we loop locally on the Infra Action agent."* Angel sided with Godfrey. Resolution: see M17 above.
- **C5.** Berend vs Angel on Slide 48 speed-at-20-nodes plot. Berend: "remove it". Angel: "keep it, they will find it in the thesis". Resolution: keep, caveat, prep backup slide.

---

## 12. Priority-Ranked Revision Backlog (v1 → v2 Plan)

### P0 — must-fix before the next rehearsal

1. Rebuild AERO efficiency chart (Slide 16): drop CPU/RAM infrastructure bars, keep parameters + latency + MAE + task-migration / orchestration-quality.
2. Add prediction-need motivation sentence on Slide 3 or 4.
3. Replace "each node runs AERO" with "AERO has the capability to run on each node" everywhere (Slides 4, 11, 50, 51).
4. Redraw Slide 10 as a generic edge decision-loop system model (not AERO-specific).
5. Rewrite Slide 23 similarly — remove far-edge/regional tags; reuse the same generic figure.
6. Add red/green SotA color coding on Slides 12 and 24.
7. Add AERO Scenario slide (before Slide 15): traces, training split, hardware, BayesOpt.
8. Add AgentEdge master Scenario slide (expand Slide 42): S1-S3 + S4-S6 + node counts + API surface.
9. Introduce attention mechanism on Slide 14 (AERO) or Slide 27 (OmniFORE) — pick one; propagate.
10. Rename Slide 30/31 title to "Impact of clustering"; remove silhouette-score text.
11. Fix Kubernetes placement on Slide 36 (inside service-orchestration layer, not infrastructure).
12. Split Slide 37 into PARES introduction (37a) and SotA/baselines (37b).
13. Add single-agent baseline definition in state-of-the-art section.
14. Resolve digital-twin "WITHOUT" arm semantics (Slide 45) — re-implement with full re-planning OR scope the claim on-slide.
15. Pre-seed defense answer for the 78.3 % vs 100 % question (Slide 45 backup).
16. Re-render Slide 48 scalability plot with uniform 0–1300 W y-axis.
17. Pre-seed defense answer for "why 20 nodes beats 35" (Slide 48 + Slide 53).
18. Retitle and re-annotate Slide 50 so it does not read as a restart of the talk.
19. Delete duplicate Problem-1 at the bottom of Slide 51.
20. Rewrite Future Work (52/53/54) with research-level challenges: benchmarking, context engineering, 6G integration, conflict protocols.
21. Rewrite Conclusions (Slide 55) as 2–3 anchor numbers per contribution in bullet form.
22. Fact-check J4 (Communications Magazine) contribution color-coding on Slide 49.

### P1 — strong recommendations

1. Redesign pagination: one large, darker page number; drop the bottom thin bar.
2. Recolor bottom infrastructure layer (Slides 03 / 04 / 50 / 51) to neutral gray.
3. Replace orange inside ActSimCrit sub-flow on Slide 41 with the Planning-agent color.
4. Add Infra Action agent chip at the end of the Planning loop on Slide 41.
5. Rebalance talk-time across left/right panels on Slides 19, 24, 32.
6. Improve bursty-trace visualization on Slide 27 (more spiky, less periodic).
7. Add a "current models forget past" panel on Slide 27 to introduce attention's memory benefit.
8. Merge or de-duplicate the Slide 13 two-panel redundancy.
9. Prepare Q&A backup slides (10 items — Section 5).
10. Print one bound copy of the thesis for the candidate's own reference at the defense.

### P2 — polish

1. Remove the "small SME" phrasing on Slide 02 (no longer relevant).
2. Consolidate Slide 49 into Slide 50 where possible.
3. Color-differentiate adapted baselines vs SotA rows on Slide 37b.
4. Ensure OmniFORE SotA (Slide 24) right-side panel is not visually messy.
5. Add 6G integration as a bullet under the Future-Work "distributed orchestration ecosystems" direction (Slide 54).

---

## 13. Verbatim Quote Bank (21 April)

Grouped by theme. Letters: `A` = Angel, `G` = Godfrey, `B` = Berend.

### Chart clarity / comparison framing

- "in terms of CPU and memory, which will be the constraint for every model, it seems to be [Pathformer] performing a lot better than AERO here." — G (11.35)
- "Okay, so the fitting is based on the parameters. Not from what we show here." — G (11.35, resolution)
- "I agree with you. And this, this platformer cannot even run there. So that's why we just have the platformer as a baseline to show how good we actually are." — B (11.35)
- "I think this CPU utilization RAM is kind of useless. Or you could use orchestration." — B (11.35)
- "here it appears that ModernTCN is better for your solution. Much better. Because it has much better memory error and latency. I don't know why with all these parameters, it's that efficient. So it's a convolution." — A (12.31)

### "Where AERO runs" — capability vs constraint

- "each node runs AERO. Is it a design constraint that the AERO must run on each node?" — G (11.35)
- "it's not a design constraint that must run on the local node." — G (11.35)
- "I can say it has the capability to execute on each node because it's all [edge] level, even at container level." — B (11.35)
- "if we think our orchestrator we don't run things on the edge, we run things on cloud and we can fit there every prediction." — A (11.35)
- "this is about motivating why models should run at the edge." — A (11.35)

### System model purity

- "system model is not where AERO runs. It's a coincidence. Also other model run there. It's not only where AERO runs." — A (12.31)
- "this is not system model. The last time we talked about it." — A (12.31)
- "you would need to have like small loops here to show that they need to run it locally … small schedulers, small loops, decision engine, analytics. This could be a system model, not AERO there for sure." — A (12.31)

### Missing prediction motivation

- "you didn't motivate why prediction is important because I kept following no motivation for the need for prediction." — G (11.35)
- "the essence of the importance of prediction wasn't motivated anywhere up to the conclusion." — G (11.35)

### Attention mechanism never named

- "I missed attention models. I mean, you don't mention at all… the first two works are based on attention models." — A (12.31)
- "you don't mention the capability of capturing past and longer periods, etc." — A (12.31)
- "that's the only slide I talk about attention, but I didn't name attention. I think that's probably should put attention mechanism." — A (12.31)
- "all models forget. But some have better memory." — A (12.31)

### SotA color coding

- "you need to highlight this because then you have the same issues in ModernTCN and Pathformer. Maybe here you need to spend a bit more time or put some colors, maybe red or something like this." — A (12.31)
- "I would go to the state of the art and red are [undeployable]. And then the other could be orange or something like this." — A (12.31)
- "models in red are most heavy. So they can have maybe better performance in some cases, but they cannot be deployed." — A (12.31)

### Scenario rigor

- "which is the scenario here? This is the scenario slide? This is not the scenario. This is like number of parameters, latency. These are the metrics." — A (12.31)
- "for which traces, for which training period, for which computational resources did you use?" — A (12.31)
- "why don't you put one slide to explain and save yourself from this kind of question?" — A (12.31)
- "no need to be weird. Eighteen. Yes. Here it's everywhere scenario and metrics. No need to be weird." — A (12.31)

### OmniFORE deployment framing

- "why you insist that OmniFORE is for the region? Because the person will say that [regional] is an example." — A (12.31)
- "don't focus it. Don't change it at the regional … but don't start by saying you design it for the regional case scenario." — A (12.31)
- "we design it for the problem. Yes, the problem. The need for generalization." — A (12.31, resolution)

### Kubernetes / infrastructure / control plane

- "Kubernetes is green. Lay in the green part. … models talk to both. If you want to make this compliant with this, all this part needs to be green because models talk to both." — A (12.31)
- "infrastructure layer. It's not orchestration layer for sure … things that are running. Yeah. Things are not control plane." — A (12.31)

### PARES and baselines

- "after analyzing a lot of papers from state of the art machine learning and agentic papers, we came to these five capabilities PARES and then before to explain PARES before any." — B (13.08)
- "more like an answer to the question. And then. But you can do it also like this." — A (13.08)
- "the goal is to explain state of the art. And the state of the art every… everybody is claiming agentic systems, but what they do is a simple LLM call based [tool use]." — A (13.08)
- "none of these function in the setting we want." — B (13.08)
- "try to introduce a bit the concept of single agent." — A (13.08)

### Digital-twin ablation

- "why without digital twin you have this failure? I mean, why the success rate reduces without digital twin?" — G (13.08)
- "even here, when you execute on the infra, you may fail. But then you feed again the plan." — G (13.08)
- "for me, I would prioritize the result over the intelligence of an agent." — A (13.08)
- "Y is 78.3, not 100% because you're excluding the plan after validation. What is causing the draw here?" — G (13.08)
- "the agent still comes up with infeasible things." — G (13.08)
- "the LLM the critic allows some infeasible plans to pass to the execution agent." — B (13.08)

### Scalability 8/20/35

- "this was the optimal thing. What happens at 19, what happens at 22? Is it possible that once we get here there's a chance that after 35 we get a bigger graph? Why is the optimal was 17 better than this?" — G (13.08)
- "at 35 nodes with all of these metrics is completely bloated and it has to read all of these metrics. So I think in order to scale properly to a large set of nodes, you have to come up with some context engineering." — B (13.08)
- "maybe 18 [nodes] were saturated so we couldn't do better than 18 … you must have a clear way." — G (13.08)

### Scale uniformity on plots

- "it's bad that the scale. Usually the scale should be the same in general." — A (13.08)
- "the scale here could be from 0 to 1,300. And then you could have this part like this … visually you could see this." — A (13.08)
- "I didn't tell you [percentages]. Maybe I told you. What does it mean, 3,300?" — A (13.08)

### Slide 50 confusion

- "what is the purpose of this slide? For sure you didn't know. I didn't why so like I started with slide one. So here's like the problems and then in 50 I show the again because we didn't discuss them here." — G (13.08)
- "it was hard to follow to connect because this one I [have] seen it before when you're starting then it appears again here." — G (13.08)

### Future work depth

- "you need to expand much better this part." — A (carried from 17 April, re-endorsed 13.08 implicitly)
- "it's about… really a clear, clear directions. Clear and more research wise directions than just use other tools." — A (13.08)
- "as a future work, for example, one thing that I would put would be also how challenges on including this to 6G." — A (13.08)

### Conclusions

- "maybe it's like you need to highlight 2, 3 numbers for each one." — A (13.08)
- "you can focus more on the text. Having us bullets some numbers than focusing on the numbers." — A (13.08)
- "Because they are not these numbers that need to be highlighted only." — A (13.08)

### Publications

- "I should just mention that 8 publications, 4 journals, 3 conferences, 1 book chapter. But you can… you can associate them." — G (11.35)
- "you can speak in general. So this work in general was ended up… in 8 publications, 4 of them journals, 3 conferences and one book chapter." — A (11.35)
- "AERO is not… the magazine is not about AERO too. I delete the wrong one." — G (11.35)
- "the publication slide could fit even after conclusions having conclusions and say, okay, the work in this thesis has been published." — A (13.08)

### Delivery

- "you need to try to understand the question and faster and go to where you have you have to go." — A (11.35)
- "I have to filter. Filter what the problem is faster." — A (11.35)
- "you should have at least one [printed thesis] for yourself in the presentation. Also for them, I would suggest." — A (13.08)
- "it was 55 minutes, but better. 55. I can cut." — A (11.35, opening)

### Color / visual discipline

- "the last infrastructure layer here it's like the colors are same as the solutions, but it's confusing. I would prefer a more natural. I mean in the last one you have it just gray." — A (12.31)
- "why this is an orange? Because you said this orange is the agent[edge] means this is not part of AgentEdge." — G (11.35)
- "these are minor. These ones have the same value … then just remove the bottom bar." — G (11.35)
- "bigger fonts with the slides … it was hard for me for the beginning to check where the page is." — A (12.31)

### Pagination

- "when I was looking for page numbers I was looking here and I noticed they were here. So usually the focus is here." — G (11.35)
- "it's quite a look what follows? Do I follow this? Do I follow this? Because it's the same font. They are great. Very tiny." — G (11.35)

---

## 14. What Already Works In v1 (Do Not Break In v2)

Explicit positive or neutral signals in 21 April — preserve:

- `[KEEP]` Title slide — no critique, clean.
- `[KEEP]` Three-contribution spine (AERO → OmniFORE → AgentEdge) with consistent coloring survived the rewrite.
- `[KEEP]` AERO live-deployment narrative (Slide 20) — the 8×-lower-error-under-drift story lands.
- `[KEEP]` AgentEdge architecture-vs-architecture fairness on Slide 44 (same LLM, same tools, same scenarios).
- `[KEEP]` Digital-twin conceptual framing (Slide 45) — the *idea* is correct; only its defense needs work.
- `[KEEP]` Slide 50 operator-impact block — the 17 April rewrite landed.
- `[KEEP]` Conclusions' three-claim structure (Slide 55) — but rebalance numbers as bullets (P0 above).
- `[KEEP]` Slide 08 contribution-map table — committee jumped past it; it works.
- `[KEEP]` Slide 06 generalization framing — committee accepted the 300+ microservices claim.
- `[KEEP]` Overall 55-minute pacing — inside the committee's 45–50 target with micro-trims possible.
- `[KEEP]` Informer exclusion from AERO storyline — Berend correctly clarified AERO does not use informers.
- `[KEEP]` The ActSimCrit concrete flow figure (Slide 41 body) — substantially better than v0's schematic. Only the orange color needs fixing.

---

## 15. Coverage & Source Traceability

Every 21 April transcript has been processed below.

| File                                            | Approx. runtime | Primary contributions to this feedback file                                                                                        |
|-------------------------------------------------|------------------|------------------------------------------------------------------------------------------------------------------------------------|
| `WhatsApp Ptt 2026-04-21 at 11.35.00.ogg`       | ~12 min         | AERO efficiency chart confusion (Pathformer CPU/RAM), "each node runs AERO" capability framing, prediction-motivation gap, pagination, publications list structure, J4 contribution mis-assignment, Slide 48 scalability questions |
| `WhatsApp Ptt 2026-04-21 at 12.31.41.ogg`       | ~16 min         | Attention-mechanism gap, AERO periodicity visualization, system-model generic-vs-specific, SotA red/green color coding, scenario-slide missing, OmniFORE regional-vs-problem framing, OmniFORE bursty trace, Slide 36 Kubernetes placement |
| `WhatsApp Ptt 2026-04-21 at 13.08.11.ogg`       | ~10 min         | PARES introduction ordering, adapted-baselines narrative, digital-twin ablation semantics, 8/20/35 scalability explanation, scale uniformity on energy plot, Slide 49-51 end-of-deck flow, future-work depth, conclusions number rebalance |

---

## 16. Pre-Defense Checklist (v1 → v2)

Before the real defense, confirm each of the following is done:

### Deck rewrites

- [ ] Slide 02/03/04: bottom infrastructure layer recolored gray; prediction-need motivation sentence added.
- [ ] Slide 10: generic edge decision-loop system model; AERO name pushed to Slide 11.
- [ ] Slide 11: "AERO has the capability to run on each node" framing; edge-real-time motivation example.
- [ ] Slide 12: red/green SotA color coding (red = undeployable, green = lightweight).
- [ ] Slide 13: two-panel redundancy removed; latency narration written into speaker notes.
- [ ] Slide 14: periodicity visualization redrawn with τ₁/τ₂/τ₃ labels; attention introduction candidate.
- [ ] Slide 15: new Scenario slide prepended (dataset, hardware, BayesOpt).
- [ ] Slide 16: CPU/RAM infrastructure bars removed; parameters + latency + MAE + task-migration bars kept; explicit "fitting is about parameters" sentence on-slide.
- [ ] Slide 19: left/right panel talk-time rebalanced.
- [ ] Slide 23: "far edge / regional cluster" tags removed; OmniFORE framed as location-agnostic generalization.
- [ ] Slide 24: red/green SotA color coding; right-side cleanup.
- [ ] Slide 27: bursty trace redrawn (spiky, irregular); attention introduction (if not on 14).
- [ ] Slide 30/31: title "Impact of clustering"; silhouette-score text removed.
- [ ] Slide 32/33: plots on left, conclusions on right; fonts rebalanced.
- [ ] Slide 36: Kubernetes relocated to service-orchestration layer; redundant lower-right box removed.
- [ ] Slide 37: split into 37a (PARES intro) + 37b (SotA + adapted baselines); adapted-baselines narrative on-slide.
- [ ] Slide 41: orange in ActSimCrit recolored; Infra Action chip appended.
- [ ] Slide 42: expanded into master Scenario table (S1–S6, 8/20/35 nodes, 12 APIs, hardware).
- [ ] Slide 43/44: single-agent baseline defined; scenario tie-in to Slide 42.
- [ ] Slide 45: ablation semantics scoped on-slide ("WITHOUT = ?"); Q&A answer drafted.
- [ ] Slide 48: uniform y-axis; caveat linking to context-engineering future work.
- [ ] Slide 49: merge-or-move publications; fact-check J4 color.
- [ ] Slide 50: retitled + annotated so it does not read as "start of talk 2".
- [ ] Slide 51: duplicate Problem-1 removed.
- [ ] Slide 52–54: future-work rewritten with research-level challenges.
- [ ] Slide 55: 2–3 anchor numbers per contribution as bullets, not headline.
- [ ] Slide 56: publication recap color-aligned.
- [ ] Pagination: one darker page number, bottom bar removed, font enlarged.

### Q&A backup slides

- [ ] AERO vs Pathformer CPU/RAM
- [ ] OmniFORE deployment granularity
- [ ] Digital-twin 78.3 % answer
- [ ] Why 20 nodes beats 35
- [ ] Adapted baselines via PARES
- [ ] 6G services subtype
- [ ] J4 contribution assignment
- [ ] 50 ms / 150 ms budget origin
- [ ] Informers vs Pathformer vs AERO
- [ ] AERO to other 6G time-series

### Delivery / logistics

- [ ] Practice fast-filtering committee questions.
- [ ] Bring one printed bound thesis copy.
- [ ] Rehearse Slide 42 explanation at full depth (rushed last time).
- [ ] Rehearse Slide 19 right-panel (rushed last time).
- [ ] Rehearse Slide 45 digital-twin defense.
- [ ] Rehearse Slide 48 scalability defense.

---

*This file captures every actionable sentence from the three 21 April transcripts. Everything not captured here was either non-substantive agreement ("okay, next") or was already resolved in the 17 April → 21 April rewrite.*
