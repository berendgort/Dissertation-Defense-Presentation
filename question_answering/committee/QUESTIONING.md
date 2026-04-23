# Defense Question Bank

This file contains `200` possible defense questions and concise model answers.
They are based on:

- your dissertation sections and chapter claims
- your defense presentation structure
- the paper themes collected for `Ferran Adelantado i Freixer`, `Jordi Pérez-Romero`, and `Lorenza Giupponi`

Use these as structured answer starters, not as scripts to memorize word-for-word.

## Fast Evidence Anchors

- `AERO`: `599` parameters, `99.98%` reduction versus Pathformer, `0.38 ms` inference, `13%` energy savings, `99%` fewer SLA violations.
- `OmniFORE`: about `30%` cross-dataset MAE improvement, `19.35%` zero-shot gain, `15x` faster inference than `AGCRN`.
- `AgentEdge`: `78.3%` success, `2.76x` over `ReAct`, `10x` more consistent API interactions, up to `300.8 W` power savings.
- Validation scope: `Google Borg`, `Alibaba`, industrial collaboration with `Nearby Computing S.L.`, and deployment-oriented evaluation.

## A. Big-Picture Thesis Questions

1. **Question:** What is the single-sentence contribution of this dissertation?
**Likely asker:** Any  
**Answer:** The dissertation shows that zero-touch 6G orchestration becomes more practical when prediction is edge-deployable, forecasting generalizes across services, and orchestration actions are validated before execution. The three contributions solve those three linked problems through `AERO`, `OmniFORE`, and `AgentEdge`.

2. **Question:** Why is 6G orchestration still underperforming today?
**Likely asker:** Any  
**Answer:** It underperforms because current systems are still too reactive, too manually configured, and too centralized to scale across heterogeneous services. That creates a gap between available telemetry and timely orchestration decisions. My thesis addresses that gap by moving from reactive control to predictive and validated control.

3. **Question:** Why did you structure the thesis around three separate frameworks instead of one end-to-end model?
**Likely asker:** Ferran, Jordi  
**Answer:** Because the three bottlenecks are different: deployability, generalization, and safe action selection. `AERO` solves the edge-feasibility problem, `OmniFORE` solves the cross-application scalability problem, and `AgentEdge` solves the validated-control problem. A single monolithic model would hide those trade-offs instead of resolving them cleanly.

4. **Question:** What is the main novelty relative to prior work?
**Likely asker:** Any  
**Answer:** The novelty is not one isolated algorithm. It is the integrated progression from lightweight prediction, to generalizable prediction, to validated autonomous orchestration. Each chapter solves a different operational barrier, and together they form one coherent orchestration pipeline.

5. **Question:** Why focus on the edge-cloud continuum instead of conventional cloud-only orchestration?
**Likely asker:** Jordi  
**Answer:** Because orchestration decisions increasingly affect workloads running under latency, energy, and locality constraints that pure cloud settings do not capture well. In edge-cloud environments, prediction and control must happen closer to the workload. That is why deployability and inference latency matter so much in this thesis.

6. **Question:** Why is proactive orchestration better than reactive orchestration?
**Likely asker:** Ferran  
**Answer:** Reactive orchestration typically responds after QoS degradation or overload is already visible. Proactive orchestration uses forecasts early enough to account for action execution time, which is essential for scaling, migration, and consolidation decisions. The thesis shows that this predictive shift improves both energy and SLA outcomes.

7. **Question:** Why did you use production traces such as Google Borg and Alibaba?
**Likely asker:** Lorenza  
**Answer:** Because real workload traces are necessary to demonstrate practical value beyond toy examples. They capture heterogeneity, noise, and operational irregularity that synthetic traces usually miss. I do not claim they are literal 6G radio traces, but they are strong production-scale proxies for orchestration research.

8. **Question:** What is the biggest limitation of the thesis?
**Likely asker:** Any  
**Answer:** The biggest limitation is deployment realism at the full operational-network level. The thesis validates orchestration logic strongly, but it does not yet provide a complete live telco-grade closed loop with wireless-native traces and a production digital twin. That is the natural next step rather than a contradiction of the current contribution.

9. **Question:** How do the dissertation objectives map to the results?
**Likely asker:** Any  
**Answer:** `O1` is met by `AERO`, which achieves a sub-1K-parameter predictor with sub-millisecond inference. `O2` is met by `OmniFORE`, which generalizes across datasets without per-service retraining. `O3` is met by `AgentEdge`, which surpasses the target success rate through validation-first orchestration.

10. **Question:** What should the committee remember if they remember only one thing?
**Likely asker:** Any  
**Answer:** The thesis is strongest when read as one control stack. `AERO` makes forecasting deployable, `OmniFORE` makes it scalable across services, and `AgentEdge` makes autonomy safer through validation before action. That is the central story.

## B. AERO Questions

11. **Question:** Why did you target a sub-1K-parameter forecasting model?
**Likely asker:** Ferran  
**Answer:** Because the problem is not only prediction accuracy, but whether prediction can actually run at the edge under real latency and memory constraints. A tiny model directly addresses deployment feasibility. `AERO` demonstrates that domain-specific design can outperform brute-force model scaling for this use case.

12. **Question:** How does `AERO` work conceptually?
**Likely asker:** Any  
**Answer:** `AERO` uses adaptive period detection to identify dominant periodic structures in multivariate workload traces, then predicts future behavior with a very compact architecture. The key idea is to build periodicity awareness into the model rather than relying on a large generic architecture to discover it implicitly.

13. **Question:** Why is adaptive period detection important?
**Likely asker:** Ferran  
**Answer:** Because real workloads do not all follow one fixed temporal window. If the model assumes one rigid horizon, it drifts when workload rhythm changes. Adaptive period detection lets the model track the relevant structure rather than hard-coding it.

14. **Question:** Why not just compress a larger transformer instead of designing `AERO` from scratch?
**Likely asker:** Jordi  
**Answer:** One of the thesis insights is that edge efficiency benefits more from domain-specific lightweight design than from post hoc compression of heavy models. Large models still carry architectural overhead and deployment complexity. `AERO` was designed for the target environment from the start.

15. **Question:** How can a `599`-parameter model compete with large transformers?
**Likely asker:** Any  
**Answer:** Because it solves a narrower problem with strong inductive bias. Instead of learning everything from scratch, it exploits workload periodicity explicitly. That is why it can stay competitive while reducing parameters by `99.98%` versus Pathformer.

16. **Question:** Why is container-level workload prediction harder than VM-level prediction?
**Likely asker:** Ferran, Lorenza  
**Answer:** Containers are shorter-lived, more numerous, more variable, and usually have sparser history per instance. They also sit inside microservice graphs with interdependencies that VMs often do not expose as strongly. That is why conventional VM-oriented predictors transfer poorly to this setting.

17. **Question:** Why does `0.38 ms` inference matter?
**Likely asker:** Jordi  
**Answer:** Because a predictor that is accurate but too slow is not operationally useful at the edge. `0.38 ms` shows that `AERO` is not only lightweight on paper, but viable for real-time orchestration loops. It directly supports the claim of edge deployability.

18. **Question:** Where do the `13%` energy savings and `99%` fewer SLA violations come from?
**Likely asker:** Any  
**Answer:** They come from integrating the forecasts into orchestration decisions early enough to act before overload or waste accumulates. Better forecasting improves scaling and consolidation timing. The point is that forecast quality only matters if it translates into operator-relevant outcomes.

19. **Question:** Why did you compare `AERO` to Pathformer?
**Likely asker:** Ferran  
**Answer:** Because Pathformer is a strong transformer baseline and represents the high-capacity end of recent forecasting models. The comparison makes the trade-off visible: `AERO` is dramatically smaller while remaining useful for the orchestration objective. That supports the thesis claim about efficiency-oriented design.

20. **Question:** In what scenarios would `AERO` likely fail?
**Likely asker:** Lorenza  
**Answer:** It is most vulnerable when periodicity becomes weak, unstable, or dominated by abrupt regime shifts that the compact structure cannot represent well. In those cases, a richer model or additional context may help. So the claim is strong for edge-feasible forecasting, not for every workload shape imaginable.

## C. OmniFORE Questions

21. **Question:** What exact problem does `OmniFORE` solve that `AERO` does not?
**Likely asker:** Any  
**Answer:** `AERO` proves that forecasting can be edge-deployable, but it does not eliminate the operational burden of maintaining many service-specific predictors. `OmniFORE` addresses that second problem by learning structures that transfer across heterogeneous workloads. So it solves scalability of forecasting maintenance, not only forecasting itself.

22. **Question:** What is the core idea behind `OmniFORE`?
**Likely asker:** Any  
**Answer:** The key idea is that different applications often hide common temporal structures beneath different surface behavior. `OmniFORE` uses temporal clustering to organize workload heterogeneity and multi-scale attention to learn which shared patterns matter for prediction. That lets one model generalize across service families more effectively.

23. **Question:** Why is cross-dataset generalization important in orchestration?
**Likely asker:** Ferran, Jordi  
**Answer:** Because real operators do not want to train and maintain a separate model for every service type and every new deployment. Poor generalization turns prediction into an operations burden. Stronger transfer directly reduces retraining and onboarding cost.

24. **Question:** How did you evaluate cross-dataset generalization?
**Likely asker:** Lorenza  
**Answer:** The key evaluation trained on Google Borg traces and tested on Alibaba traces, which creates a meaningful domain shift instead of an in-distribution test. `OmniFORE` achieved about `30%` better MAE than `ModernTCN` in that setting. That is the central result supporting the generalization claim.

25. **Question:** Why are attention mechanisms suitable here?
**Likely asker:** Any  
**Answer:** Attention lets the model focus on the most relevant temporal patterns rather than applying one fixed temporal filter everywhere. That flexibility is important when workloads differ in shape, scale, and rhythm. It also creates a conceptual bridge to the LLM-based orchestration layer later in the thesis.

26. **Question:** Why add temporal clustering before attention?
**Likely asker:** Any  
**Answer:** Because attention alone still benefits from seeing a structured training space. Temporal clustering organizes heterogeneous traces into representative groups so the model learns from pattern families instead of isolated traces. It reduces the burden of exhaustive per-application training while preserving diversity.

27. **Question:** Why compare against `ModernTCN` and `AGCRN`?
**Likely asker:** Ferran  
**Answer:** They are relevant strong baselines with different inductive biases. `ModernTCN` is a modern convolutional time-series baseline, and `AGCRN` is a graph-aware recurrent baseline. Comparing against both helps show that the improvement is not tied to beating only one weak reference point.

28. **Question:** What does `15x` faster than `AGCRN` actually mean for the thesis?
**Likely asker:** Jordi  
**Answer:** It means the benefit is not only better transfer quality. It also means the generalized model remains practical to deploy, which matters if a single model is expected to serve many workloads. So the contribution is both operational and predictive.

29. **Question:** Does `OmniFORE` eliminate retraining entirely?
**Likely asker:** Any  
**Answer:** No, and I would not claim that. The result is that retraining burden is reduced because one model can transfer better across heterogeneous workloads. Extreme domain shifts or entirely new workload families may still require adaptation.

30. **Question:** When would `OmniFORE` likely break down?
**Likely asker:** Lorenza  
**Answer:** It would likely struggle when target workloads have structural patterns not represented in the learned latent categories, or when telemetry semantics differ too much across domains. That is why the claim is cross-application generalization under meaningful but bounded domain shift, not universal forecasting.

## D. AgentEdge Questions

31. **Question:** Why is forecasting alone not enough for orchestration?
**Likely asker:** Any  
**Answer:** Because forecasts do not choose actions by themselves. Real orchestration still needs intent interpretation, constraint checking, planning, and safe execution. `AgentEdge` exists because the jump from prediction to action is a separate research problem.

32. **Question:** Why did you choose a multi-agent architecture instead of one orchestration agent?
**Likely asker:** Jordi  
**Answer:** A single agent has to context-switch between intent parsing, monitoring, planning, and action execution, which degrades reasoning quality. `AgentEdge` separates those roles so each component reasons within a narrower domain. That specialization improves consistency and control over the workflow.

33. **Question:** Why exactly four agents?
**Likely asker:** Any  
**Answer:** The four-agent split follows the logical orchestration pipeline: `Intent`, `Observe`, `Plan`, and `Act`. That decomposition is grounded in the `PARES` capability view and keeps each role aligned with one major orchestration function. It is not arbitrary; it reflects the minimal structure needed to separate understanding, state analysis, decision-making, and execution.

34. **Question:** What is `ActSimCrit` in one sentence?
**Likely asker:** Any  
**Answer:** `ActSimCrit` is a validation-first loop in which candidate orchestration plans are generated, simulated in a synchronized digital twin, critiqued, and only then executed if they remain feasible and useful. Its purpose is to reduce trial-and-error risk in production orchestration.

35. **Question:** Why is digital-twin validation necessary?
**Likely asker:** Jordi, Lorenza  
**Answer:** Because action-first agentic systems can make attractive but unsafe decisions. The twin gives the system a safe place to test candidate actions before production commitment. So the twin is not decoration; it is the main mechanism that turns autonomy into validated autonomy.

36. **Question:** How do you justify trusting the digital twin?
**Likely asker:** Jordi  
**Answer:** I do not treat it as a perfect oracle. I treat it as a risk-reduction layer that is useful if it is sufficiently synchronized and sufficiently faithful to reject obviously bad actions. The limitation is that twin fidelity still bounds the strength of the final claim.

37. **Question:** Why does `AgentEdge` outperform `ReAct`?
**Likely asker:** Ferran  
**Answer:** Because `ReAct` is action-first and relatively unconstrained, while `AgentEdge` imposes structure through role separation, dynamic schemas, and simulation-based validation. That combination improves both success and stability. The `78.3%` success rate and `2.76x` uplift over `ReAct` reflect that design difference.

38. **Question:** What do you mean by `10x` more consistent API interactions?
**Likely asker:** Lorenza  
**Answer:** It means the system behaves much more predictably across runs instead of producing highly variable tool usage or unstable execution behavior. In orchestration, lower variance is as important as higher average performance because operators care about repeatability. This supports the argument for structured agent design.

39. **Question:** Why use structured outputs and validation schemas?
**Likely asker:** Any  
**Answer:** Because unconstrained outputs let the model propose infeasible or malformed actions. Dynamic schemas shrink the decision space to what is valid in the current state. That improves safety, reduces error propagation, and makes the action layer much easier to defend scientifically.

40. **Question:** How do you handle infeasible user intents?
**Likely asker:** Any  
**Answer:** `AgentEdge` detects deadlock when repeated planning iterations fail under explicit thresholds and accumulated rejection evidence. It then analyzes the failure pattern and proposes a more feasible alternative intent instead of looping forever. That makes the system fail more gracefully than naive action generation.

41. **Question:** What is the computational cost of `AgentEdge`, and does it scale?
**Likely asker:** Jordi  
**Answer:** The dominant cost comes from iterative LLM reasoning, with complexity tied to context length and planning iterations rather than brute-force placement enumeration. The thesis argues that this remains far more practical than exhaustive search, but latency still becomes an issue at scale. That is why inference efficiency and tool selection appear as future-work priorities.

42. **Question:** Where would the different parts of the system actually run in practice?
**Likely asker:** Jordi  
**Answer:** `AERO` belongs close to the edge because its main value is fast local inference. `OmniFORE` can use more central resources for training or transfer. `AgentEdge` naturally spans the edge-cloud continuum because intent, planning, validation, and execution do not all require the same placement or timescale.

## E. Committee-Specific Questions

43. **Question:** How does your thesis relate to O-RAN, slicing, and QoS rather than only to generic cloud operations?
**Likely asker:** Ferran  
**Answer:** The thesis operates at the orchestration layer above low-level radio scheduling, but it is aligned with the same O-RAN and slicing direction: programmable control, heterogeneous services, and QoS-aware decisions. `AERO` and `OmniFORE` support anticipatory service management, while `AgentEdge` turns those predictions into validated control actions. So it is complementary to radio resource management rather than a replacement for it.

44. **Question:** Why not use a DRL-based slice controller instead of your stack?
**Likely asker:** Ferran  
**Answer:** DRL-based slice control is powerful, but it solves a narrower optimization problem than this thesis. My thesis addresses deployable prediction, cross-service transfer, and validated orchestration logic across the edge-cloud continuum. In that sense, the work is broader and more architectural, while DRL slice control is a strong candidate backend for part of the planning layer.

45. **Question:** Would your approach still work in NTN or highly remote environments with intermittent connectivity?
**Likely asker:** Ferran  
**Answer:** The current thesis does not directly validate NTN or satellite-assisted scenarios, so I would not overclaim. Conceptually, the stack still applies, but the twin, timing assumptions, and observability model would need to become delay-aware and connectivity-aware. So I see NTN as a plausible extension, not a validated result.

46. **Question:** How does your dissertation map to current `5G/B5G/O-RAN` practice and future `6G` standards?
**Likely asker:** Jordi  
**Answer:** It maps most directly to the direction of AI-native management, modular control functions, and digital-twin-assisted automation. `AERO` is near-term practical, `OmniFORE` reduces model maintenance burden, and `AgentEdge` supports safer automation. I am not proposing a standard, but I am contributing mechanisms that fit the direction of future standardization.

47. **Question:** Are you optimizing the right layer, or are you ignoring more important decisions such as placement, functional split, or fronthaul?
**Likely asker:** Jordi  
**Answer:** I am intentionally optimizing the orchestration layer where service-level decisions are made. I agree that placement, functional split, and fronthaul are important upstream variables. The thesis scope is to show that even within a fixed infrastructure abstraction, validated orchestration intelligence adds clear value, and those deeper variables are natural extensions.

48. **Question:** How realistic are your simulation and workload assumptions for a wireless-systems audience?
**Likely asker:** Lorenza  
**Answer:** They are realistic at the orchestration and workload-management level, but not a full wireless-physics stack. I use real production traces and deployment-oriented evaluation to avoid toy results, while being explicit that interference, mobility, and detailed fronthaul behavior are abstracted. That makes the claims scoped but still meaningful.

49. **Question:** What happens if fronthaul, interference, mobility, or heterogeneous radio conditions become dominant?
**Likely asker:** Lorenza  
**Answer:** Then the optimal action policy may change, and the digital twin should incorporate those constraints explicitly. The thesis does not claim to have exhausted that part of the realism stack. Instead, it establishes how validated orchestration should be structured so richer communication models can be added later.

50. **Question:** What are the most important next steps to make this production-ready?
**Likely asker:** Any  
**Answer:** The most important next steps are benchmark engineering, explainability and guardrails, stronger digital-twin realism, context management for infrastructure state, faster inference through specialized models, semantic tool discovery, and distributed multi-agent coordination. These are not disconnected ideas. They are exactly the bridge from a strong research prototype to zero-touch production orchestration.

## F. Objectives And Validation Questions

51. **Question:** Why did you define the thesis objective around three simultaneous requirements instead of optimizing them one by one?
**Likely asker:** Any  
**Answer:** Because deployability, generalization, and autonomy interact in practice. A model that is accurate but too heavy to deploy is not useful, and a deployable model that requires endless retraining is not operationally scalable. The thesis objective was designed to capture that real-world coupling instead of reporting isolated improvements.

52. **Question:** Why was `<1000` parameters the right threshold for `AERO`?
**Likely asker:** Jordi  
**Answer:** It is a deliberately strict objective to force true edge feasibility rather than moderate compression. The thesis contrasts this with prior approaches that typically require `500K+` parameters. The exact threshold makes the contribution measurable and keeps the claim honest.

53. **Question:** Why did you define the `AgentEdge` success target as exceeding `75%`?
**Likely asker:** Any  
**Answer:** Because autonomous orchestration needs a clear operational threshold, not just relative improvement over weak baselines. A target above `75%` sets a meaningful bar for zero-touch behavior across diverse scenarios. `AgentEdge` surpasses that with `78.3%`, so the objective is not just aspirational.

54. **Question:** Why is objective-driven validation important in this dissertation?
**Likely asker:** Any  
**Answer:** It prevents the thesis from becoming a collection of disconnected models. Each chapter is mapped to one technical objective, and the conclusion checks whether those objectives were actually met. That keeps the contribution structured, measurable, and defensible.

55. **Question:** Why did you combine production traces, simulation, and live validation instead of choosing only one evaluation style?
**Likely asker:** Lorenza  
**Answer:** Because each evaluation style answers a different question. Production traces test realism, simulation tests orchestration impact at scale under controlled conditions, and live deployment tests operational feasibility. The combination is stronger than any single evaluation mode alone.

56. **Question:** Why did you rely so much on quantitative thresholds and explicit metrics?
**Likely asker:** Jordi  
**Answer:** Because orchestration research can otherwise become vague and architectural without being testable. Explicit thresholds such as parameter count, inference time, cross-dataset performance, and success rate make the claims falsifiable. That was important for keeping the thesis rigorous.

57. **Question:** How do you justify the publication-to-chapter mapping?
**Likely asker:** Any  
**Answer:** Each technical chapter is grounded in one main publication line but expanded into a monograph narrative. In the presentation numbering, `AERO` maps to `[J1]` and `[C1]`, `OmniFORE` maps to `[J2]`, `[J3]`, and `[C2]`, and `AgentEdge` maps to `[J4]` and `[C3]`. That ordering follows the defense logic from deployable forecasting, to cross-service generalization, to validated orchestration action, so the mapping shows one coherent stack rather than fragmented papers.

58. **Question:** Why did you not keep separate related-work sections inside the technical chapters?
**Likely asker:** Any  
**Answer:** Because this is a monograph, not a paper compendium. The literature review is consolidated in the background chapter to avoid repetition and to create a unified gap analysis. That makes the technical chapters more focused on methods and results.

59. **Question:** What is the strongest methodological principle across the entire thesis?
**Likely asker:** Any  
**Answer:** Build only what the target deployment can actually use, and validate every strong claim with realistic evidence. That principle drives the lightweight design in `AERO`, the representative sampling and generalization testing in `OmniFORE`, and the simulation-first safety layer in `AgentEdge`.

60. **Question:** If one objective had failed, would the thesis still be valid?
**Likely asker:** Any  
**Answer:** Yes, but the integrated orchestration claim would be weaker. The value of the thesis comes from showing the three layers work together rather than proving only one isolated component. That is why the final assessment across all objectives is so important.

## G. Additional AERO Questions

61. **Question:** Why did you choose the Alibaba `MS_11349` pod for the detailed `AERO` benchmark?
**Likely asker:** Lorenza  
**Answer:** It provides a realistic multivariate microservice workload with enough duration and variability to test forecasting behavior under nontrivial patterns. It includes both deterministic trends and stochastic fluctuations, which is exactly the regime where adaptive periodicity matters. So it is a good benchmark for comparing architectures fairly.

62. **Question:** Why did the main `AERO` benchmark use only `CPU` and memory features?
**Likely asker:** Ferran  
**Answer:** Because those are the most central and consistently available orchestration signals in container resource management. They are sufficient to test the forecasting core while keeping the comparison to baselines controlled. Additional dimensions were then explored later in the simulation studies.

63. **Question:** Why is `MSE` your training objective while you also report `MAE` and `RMSE`?
**Likely asker:** Any  
**Answer:** `MSE` is a standard smooth optimization objective that penalizes larger errors during training. `MAE` and `RMSE` then provide complementary evaluation views, with `MAE` emphasizing average error magnitude and `RMSE` highlighting larger deviations. Using both gives a more complete performance picture.

64. **Question:** Why did you use Bayesian optimization for hyperparameters?
**Likely asker:** Jordi  
**Answer:** Because the search spaces are too large for naive grid search to be efficient, especially across several architectures. Bayesian optimization gives a principled exploration-exploitation trade-off and is better suited to expensive model training loops. It also keeps the benchmark procedure consistent across models.

65. **Question:** Why did `AERO` need about two new periods to adapt after a periodicity shift?
**Likely asker:** Ferran  
**Answer:** Because the autocorrelation-based period detector needs enough repeated evidence for the new dominant lag to stand out reliably. With only a partial cycle, the new periodic structure is still ambiguous. After roughly two cycles, the signal becomes strong enough for stable reassignment.

66. **Question:** Why did you carry `Pathformer`, `SparseTSF`, and `AERO` forward into the orchestration simulation stage?
**Likely asker:** Any  
**Answer:** Because they represent distinct parts of the trade-off space: high-capacity accuracy, ultra-lightweight simplicity, and adaptive lightweight balance. That makes them the most informative set for studying how forecast characteristics translate into orchestration outcomes. The goal was not to carry every model forward, but to preserve the meaningful contrasts.

67. **Question:** Why use the `COSCO` simulator?
**Likely asker:** Jordi  
**Answer:** Because it already provides a validated discrete-time edge-cloud scheduling environment with realistic infrastructure abstractions and metrics. Extending it with a prediction interface allowed me to test workload forecasting impact systematically without the cost of full physical deployment. It gave a credible orchestration testbed for chapter-level evaluation.

68. **Question:** Why does `AERO` trigger more task migrations than reactive scheduling, and why is that not a weakness?
**Likely asker:** Ferran  
**Answer:** Because predictive orchestration reallocates earlier and more deliberately to prevent overload and enable consolidation. More migrations are acceptable if they reduce energy use, response time, and SLA violations overall. In this case, the additional mobility is a mechanism for better orchestration, not an indicator of instability.

69. **Question:** Why did live deployment show a much bigger gap between `AERO` and `SparseTSF` than the hold-out test?
**Likely asker:** Lorenza  
**Answer:** Because hold-out testing is still closer to the training distribution, while live deployment introduces zero-shot variation and operational drift. `AERO`'s adaptive behavior becomes more valuable in that setting, whereas `SparseTSF`'s fixed periodicity assumption breaks more visibly. That is exactly why live or zero-shot evaluation matters.

70. **Question:** Why is `AERO` still the right choice even though `SparseTSF` is faster and smaller?
**Likely asker:** Any  
**Answer:** Because both are already well within the real-time threshold, so the raw speed gap is not the decisive factor operationally. `AERO` gives up a small amount of latency to gain much stronger adaptability and orchestration value. The thesis claim is about useful edge deployability, not absolute minimal size at any cost.

## H. Additional OmniFORE Questions

71. **Question:** Why did you use Google Cells `A-F` for training and `G-H` for zero-shot testing?
**Likely asker:** Lorenza  
**Answer:** To create a clean separation between seen and unseen infrastructure segments and avoid leakage. That makes the zero-shot evaluation more credible than random splits taken from the same operational slice. It is a stronger test of generalization than a standard in-distribution split.

72. **Question:** Why did you select only `100` traces for the regular and zero-shot sets?
**Likely asker:** Jordi  
**Answer:** To balance diversity with practical training cost on the available hardware. The point of `OmniFORE` is not to brute-force train on everything, but to learn representative structure through clustering and attention. Using `100` traces makes that claim more meaningful.

73. **Question:** Why did you use only `20%` of the Alibaba trace in the cross-dataset test?
**Likely asker:** Lorenza  
**Answer:** Because the purpose of that experiment is not exhaustive fitting to Alibaba but a strong transfer test under limited target exposure. Using a smaller portion keeps the experiment closer to the real deployment question: how well does the model transfer with minimal adaptation? It stresses generalization rather than re-optimization.

74. **Question:** Why did you downsample Alibaba from `1` minute to `5` minutes?
**Likely asker:** Any  
**Answer:** To match the Google trace sampling rate and keep the comparison fair across datasets. Without that temporal alignment, part of the performance difference could come from mismatched resolution rather than genuine transfer difficulty. So the downsampling step controls that confound.

75. **Question:** Why is per-trace scaling so important?
**Likely asker:** Lorenza  
**Answer:** Because global scaling suppresses low-amplitude traces and effectively reduces their gradient contribution during training. Per-trace scaling equalizes learning influence across heterogeneous traces, which is essential when generalization is the target. The measured degradation under global scaling confirms that it is not a cosmetic preprocessing choice.

76. **Question:** Why use a latent space before clustering instead of clustering the raw traces directly?
**Likely asker:** Any  
**Answer:** Raw high-dimensional traces are noisy, computationally expensive, and hard to cluster meaningfully. The latent space compresses them while preserving the patterns most relevant for temporal grouping. That makes clustering more stable and more useful for downstream trace selection.

77. **Question:** Why is `k = 11` the right number of clusters?
**Likely asker:** Any  
**Answer:** It was selected through a consensus of multiple cluster-quality criteria rather than one heuristic alone. The choice is supported by silhouette, Davies-Bouldin, Calinski-Harabasz, and stability analysis. So `11` is justified empirically, not arbitrarily.

78. **Question:** Why does clustering-based trace selection outperform random sampling?
**Likely asker:** Ferran  
**Answer:** Because clustering gives a training set that covers structural diversity more systematically. Random sampling can miss rare but important workload families or overrepresent common patterns. The reduction in zero-shot error shows that representative diversity is more valuable than naive trace quantity.

79. **Question:** Why use Informer-style efficient attention instead of a full transformer?
**Likely asker:** Jordi  
**Answer:** Because the framework needs long-range pattern capture without quadratic cost exploding on longer sequences. Informer gives a practical trade-off through sparse attention, attention distilling, and fast generative decoding. It is a better fit for real-time forecasting deployment than a standard transformer.

80. **Question:** Why is `OmniFORE` still practical despite being much slower than `ModernTCN`?
**Likely asker:** Any  
**Answer:** Because it remains within real-time limits while delivering stronger generalization. `ModernTCN` is exceptionally fast, but that speed comes with lower transfer quality in the more difficult tests. `OmniFORE` is designed to sit at the useful balance point rather than the absolute fastest point.

## I. Additional AgentEdge Questions

81. **Question:** Why did you choose exact end-state matching as the main success criterion?
**Likely asker:** Jordi  
**Answer:** Because orchestration outcomes are operationally meaningful only if the final infrastructure state satisfies the intended constraints. Exact matching against a set of valid target placements avoids vague success definitions. It turns orchestration evaluation into a concrete correctness problem.

82. **Question:** Why do you allow multiple acceptable target placements instead of only one?
**Likely asker:** Any  
**Answer:** Because orchestration is usually not a single-solution problem. Different placements can be equally valid if they satisfy the same constraints and objectives. Allowing multiple valid end states reflects real system flexibility while keeping evaluation strict.

83. **Question:** Why did you use Wilson score intervals for success-rate analysis?
**Likely asker:** Jordi  
**Answer:** Because success is a bounded binary outcome and Wilson intervals behave better than normal approximation, especially away from the center. They avoid misleading confidence intervals that can spill outside `[0,1]`. That makes the statistical reporting more robust.

84. **Question:** Why six scenarios, and why these six?
**Likely asker:** Any  
**Answer:** Because they cover the main orchestration stress points that matter operationally: basic resource conflict, conflicting requirements, deadlock, and scalable energy consolidation across multiple infrastructure sizes. The set is intentionally compact but diverse. It is broad enough to reveal structural strengths and weaknesses without becoming diffuse.

85. **Question:** Why did you run `60` experiments per model or condition in the main comparisons?
**Likely asker:** Lorenza  
**Answer:** To capture variability from stochastic timing, agentic reasoning, and repeated execution across scenarios. Fewer runs would make the reported success rates and variance less trustworthy. The run count is a methodological choice to support credible comparison rather than anecdotal demonstrations.

86. **Question:** Why was `qwen3-235B` the best model for `AgentEdge`?
**Likely asker:** Jordi  
**Answer:** Because it achieved the best balance of cross-scenario success, reasoning quality, and acceptable runtime. Other models were either faster but too unreliable, or slower without better orchestration quality. The selection was empirical, not based on benchmark reputation alone.

87. **Question:** Why compare `AgentEdge` to `ReAct` and `LATS` instead of only classical optimization methods?
**Likely asker:** Any  
**Answer:** Because the thesis is about agentic orchestration, including natural-language intent interpretation and multi-step action planning. Classical optimization solves only the formally specified placement problem after translation, whereas `ReAct` and `LATS` are proper agentic baselines. They test whether generic agent architectures can handle orchestration without specialization.

88. **Question:** Why is the digital twin ablation one of the most important evaluations in the chapter?
**Likely asker:** Lorenza, Jordi  
**Answer:** Because it directly tests the thesis claim that validation-first autonomy matters. Removing the twin while keeping the rest of the stack intact isolates the value of simulation-based prevalidation. The jump in variance and drop in success make that contribution very clear.

89. **Question:** Why is a linear power model acceptable for the energy analysis?
**Likely asker:** Jordi  
**Answer:** Because it is a standard and empirically grounded approximation for data-center-style power behavior, and the chapter uses it consistently across all conditions. The claim is comparative energy optimization under a shared model, not a perfect hardware-electrical reproduction. That scope is sufficient for evaluating orchestration strategy.

90. **Question:** Why are the long runtimes in the energy-optimization scenarios still acceptable?
**Likely asker:** Any  
**Answer:** Because those scenarios represent strategic orchestration tasks, not millisecond control loops. Energy consolidation and low-power transitions typically happen on slower operational timescales where decisions persist for long periods. In that context, minutes of planning time can still be useful if they produce sustained savings.

## J. Future-Work And Advanced Defense Questions

91. **Question:** Why do you say benchmark engineering is one of the most urgent next steps?
**Likely asker:** Lorenza  
**Answer:** Because agentic orchestration cannot be improved systematically without repeatable evaluation suites. Unlike standard supervised tasks, orchestration admits multiple valid outcomes and is sensitive to stochastic reasoning behavior. Benchmark infrastructure is therefore a prerequisite for disciplined progress.

92. **Question:** Why is explainability especially important for orchestration agents?
**Likely asker:** Jordi  
**Answer:** Because operators need to understand not only what action was chosen, but why alternatives were rejected. In infrastructure management, opaque success is not enough for trust. Explainability makes the transition from research prototype to operator-facing tool more realistic.

93. **Question:** Why do you focus more on malfunction and misspecified objectives than on prompt injection?
**Likely asker:** Lorenza  
**Answer:** Because the expected deployment context is relatively protected compared to open consumer chat systems. The more immediate danger is an agent doing the wrong thing with legitimate infrastructure access, not an internet-facing prompt attack. So containment and guardrails are more central than adversarial prompting in this thesis.

94. **Question:** Why is data locality such a major issue for future deployment?
**Likely asker:** Jordi  
**Answer:** Because orchestration requires detailed infrastructure state, and sending that externally may create privacy, compliance, and business risks. Local or hybrid inference architectures can reduce that problem. It is one of the main engineering barriers for production adoption.

95. **Question:** Why is context staleness a serious problem for agentic orchestration?
**Likely asker:** Lorenza  
**Answer:** Because infrastructure state changes continuously while LLM reasoning takes seconds or longer. The world the agent reasons about can differ from the world it finally acts on. That makes revalidation and delta-aware reasoning important future research directions.

96. **Question:** Why is tool discovery likely to become a bottleneck before raw model intelligence does?
**Likely asker:** Jordi  
**Answer:** Because even good models degrade when too many tools compete for attention inside the context window. In my own results, performance already drops once tool catalogs become too large. So semantic retrieval and hierarchical tool organization are likely to matter a lot in real deployments.

97. **Question:** Why is model-agnostic agent design difficult in practice?
**Likely asker:** Any  
**Answer:** Because different models and providers behave differently even when they nominally expose the same capabilities. Output formats, tool-calling conventions, and prompt sensitivities vary enough to break portability. That makes true model-agnostic orchestration harder than it sounds conceptually.

98. **Question:** Why is distributed multi-agent coordination an open research problem rather than a solved systems issue?
**Likely asker:** Jordi  
**Answer:** Because multiple agent instances can produce conflicting actions on shared infrastructure, and resolving those conflicts adds communication overhead and synchronization complexity. The challenge is not only detecting conflicts, but doing so fast enough to remain useful. That trade-off is still open.

99. **Question:** If you had to choose one next production experiment, what would it be?
**Likely asker:** Any  
**Answer:** I would choose a limited-scope live deployment where `AgentEdge` manages a controlled orchestration subset with a synchronized twin, explicit guardrails, and operator review. That would test trust, staleness handling, and action validation under real operational drift. It is the most direct bridge from the thesis to production evidence.

100. **Question:** What is the strongest scientific lesson from the whole dissertation?
**Likely asker:** Any  
**Answer:** That orchestration intelligence should be designed around operational constraints from the start. Prediction must be deployable, learning must generalize across service diversity, and autonomy must be validated before execution. Those three principles are the core scientific takeaway of the thesis.

## K. Theoretical Foundations And Problem Formulation

101. **Question:** Why do you model orchestration as a three-stage problem instead of only as optimization?
**Likely asker:** Jordi  
**Answer:** Because real orchestration begins before optimization and continues after it. First, intent must be translated into formal constraints. Then placement must be optimized. After that, compliance must be monitored as infrastructure evolves. Classical optimization only covers the middle stage.

102. **Question:** Why is placement optimization still the mathematical core of orchestration?
**Likely asker:** Any  
**Answer:** Because every orchestration approach eventually has to decide where services go under finite resources and competing objectives. Even when intent is expressed in natural language, the final action still resolves to a placement or reallocation decision. So placement remains the core constrained decision problem.

103. **Question:** Why do you formulate the orchestration objective as `QoS + lambda R + mu E`?
**Likely asker:** Jordi  
**Answer:** Because it separates the three central concerns cleanly: service quality, infrastructure balance, and energy cost. This formulation keeps the objective interpretable and lets different orchestration modes emphasize different priorities. It is not the only possible formulation, but it is a defensible and operator-meaningful one.

104. **Question:** Why use squared utilization in the load-balancing cost?
**Likely asker:** Jordi  
**Answer:** Squared utilization penalizes concentration of load more heavily than a purely linear term, which makes hotspots more expensive. That helps the optimizer prefer smoother distributions when all else is equal. It is a standard way to increase sensitivity to imbalance.

105. **Question:** Why is the QoS penalty written with the positive-part operator `[x]_+`?
**Likely asker:** Any  
**Answer:** Because only violations should be penalized. If realized QoS is better than the target, the system should not be punished for exceeding expectations. The positive-part term encodes exactly that operational interpretation.

106. **Question:** Why keep the objective generic and move many constraints into user intent instead of hardcoding them?
**Likely asker:** Ferran  
**Answer:** Because orchestration requests vary across scenarios and operators. A rigid objective would limit flexibility and require constant redesign. Letting the intent layer express many constraints keeps the framework adaptable while preserving a stable optimization backbone.

107. **Question:** Why do you model infrastructure as a graph?
**Likely asker:** Any  
**Answer:** Because orchestration decisions depend not only on node capacity but also on connectivity and latency between nodes. The graph abstraction captures both compute placement and inter-node communication structure. That makes it the natural representation for distributed edge-cloud systems.

108. **Question:** Why do you normalize resource utilization to `[0,1]`?
**Likely asker:** Jordi  
**Answer:** It gives a unified way to reason across heterogeneous nodes with different raw capacities. Normalized utilization simplifies constraint checking and comparison between infrastructure tiers. It also helps keep the agent and optimization logic more portable.

109. **Question:** Why is the search space hard enough to justify an agentic approach?
**Likely asker:** Any  
**Answer:** Because the placement space grows as `|N|^|S|`, which becomes combinatorial very quickly. On top of that, the environment is dynamic and objectives conflict. That makes pure brute force or static heuristics inadequate for realistic deployments.

110. **Question:** Why is orchestration harder than standard scheduling?
**Likely asker:** Any  
**Answer:** Because it combines interpretation, constraint reasoning, adaptation, and execution under changing state. Standard scheduling often assumes that the task description and objective are already formalized. Orchestration must derive those from intent and continuously maintain them over time.

## L. Literature Gap And Motivation Questions

111. **Question:** Why are traditional centralized orchestration systems insufficient for 6G environments?
**Likely asker:** Jordi  
**Answer:** Because they introduce sequential bottlenecks, accumulate delay, and create single points of failure across distributed infrastructures. Those weaknesses become more serious as services move across far-edge, near-edge, and cloud tiers. The thesis is motivated by exactly that mismatch.

112. **Question:** Why are RNN-based or CNN-based predictors not enough for your setting?
**Likely asker:** Ferran  
**Answer:** They capture useful temporal structure, but each has limitations under the workload diversity in edge-cloud systems. RNNs struggle with long dependencies and training difficulties, while CNNs can miss broader temporal structure. The thesis responds by using lightweight adaptive design in `AERO` and attention-based generalization in `OmniFORE`.

113. **Question:** Why are generic LLM orchestration systems not already sufficient?
**Likely asker:** Lorenza  
**Answer:** Because generic systems often hallucinate, lack infrastructure-aware tool integration, and are usually designed for centralized or non-safety-critical domains. They also tend to act directly without simulation-based prevalidation. `AgentEdge` is designed specifically to close that gap.

114. **Question:** Why is the safety-autonomy trade-off central to this dissertation?
**Likely asker:** Any  
**Answer:** Because more autonomy usually means less direct human control, which increases the risk of incorrect actions. Existing approaches often force a choice between rigid safety and unsafe flexibility. The thesis argues for a third path: validated autonomy.

115. **Question:** Why does the thesis favor validated autonomy over trial-and-error learning in production?
**Likely asker:** Lorenza  
**Answer:** Because trial-and-error is unacceptable when failures can cascade across distributed services. In production orchestration, a wrong action can disrupt QoS and energy policy simultaneously. Simulation-first validation is a safer mechanism for exploring the action space.

116. **Question:** Why is natural-language intent important in a serious orchestration system?
**Likely asker:** Any  
**Answer:** Because operators already think and communicate in high-level service goals rather than in raw API calls or low-level placement variables. Natural-language intent is therefore not a gimmick; it is the real interface layer. The hard part is translating it safely and systematically.

117. **Question:** Why is microservice growth such a major motivation for your work?
**Likely asker:** Any  
**Answer:** Because microservices increase deployment granularity, heterogeneity, and coordination complexity. They make container-level prediction more difficult and make manual orchestration less scalable. The thesis is shaped around that modern architectural reality.

118. **Question:** Why do you say existing related work is too narrow?
**Likely asker:** Jordi  
**Answer:** Because many systems solve isolated subproblems such as intent parsing, code generation, or resource placement, but not the full end-to-end orchestration chain. Others target only a single domain or assume centralized cloud settings. My thesis tries to connect the missing pieces into one usable stack.

119. **Question:** Why is “validated autonomy” a better framing than “fully autonomous AI”?
**Likely asker:** Any  
**Answer:** Because it is more honest and more defensible. The thesis does not argue for unrestricted autonomous behavior. It argues that autonomy becomes practical only when paired with validation, constraints, and explicit boundaries.

120. **Question:** Why should the committee believe there is still a real research gap here?
**Likely asker:** Any  
**Answer:** Because the evidence from the literature and my own experiments shows that current systems still fail on one or more of the key dimensions: deployability, generalization, or reliable autonomy. If those problems were already solved together, the three contributions would not all be necessary. The thesis exists because that integration gap is still open.

## M. Additional Methodology And Metric Questions

121. **Question:** Why did you report both prediction metrics and orchestration metrics?
**Likely asker:** Any  
**Answer:** Because forecasting quality alone does not prove orchestration usefulness. Prediction metrics show model behavior, while orchestration metrics show system impact. The thesis needs both to connect algorithmic quality to operator value.

122. **Question:** Why do you sometimes emphasize `MAE` over `RMSE`?
**Likely asker:** Lorenza  
**Answer:** `MAE` is easier to interpret and less dominated by outliers, which makes it especially useful when generalization across heterogeneous traces is the main question. `RMSE` is still valuable because it exposes larger deviations. Using both avoids overcommitting to one error view.

123. **Question:** Why introduce `SMAPE` in `OmniFORE` but not emphasize it equally everywhere?
**Likely asker:** Any  
**Answer:** `SMAPE` is especially useful when comparing across scales because it normalizes by signal magnitude. It is more relevant in the generalization chapter where trace diversity is central. In `AERO`, absolute edge-feasibility and orchestration impact are more important than scale-normalized comparison alone.

124. **Question:** Why did you use early stopping with patience in the convergence analysis?
**Likely asker:** Jordi  
**Answer:** Because the goal is generalization, not overtraining until training loss is minimized. Early stopping gives a practical training criterion aligned with real deployment workflows. It also makes convergence comparisons more meaningful across models.

125. **Question:** Why is convergence speed itself a relevant metric?
**Likely asker:** Ferran  
**Answer:** Because models that need frequent updating or retraining become operationally expensive if convergence is slow. Training efficiency matters when workloads evolve and model updates must remain practical. So convergence speed is not just a training detail; it affects operational feasibility.

126. **Question:** Why does the thesis care so much about inference time if some planning stages already take seconds?
**Likely asker:** Jordi  
**Answer:** Because the stack includes components operating at different timescales. Forecasting should remain lightweight and near-real-time, while strategic agentic planning can operate more slowly. Fast local inference is still essential even if some higher-level orchestration loops are slower.

127. **Question:** Why is live deployment still necessary if the simulator is already realistic?
**Likely asker:** Lorenza  
**Answer:** Because simulators can only validate claims up to the fidelity of their assumptions. Live deployment exposes zero-shot drift, system noise, and implementation friction that even a strong simulator cannot fully reproduce. That is why the live `AERO` deployment is an important complement.

128. **Question:** Why use deterministic seeding in the agentic evaluation?
**Likely asker:** Jordi  
**Answer:** To make stochastic evaluation reproducible without pretending the agent itself is deterministic. Deterministic seeds standardize the random environment aspects so model comparisons remain fair. That is a methodological control, not an attempt to erase variability.

129. **Question:** Why do you call the evaluation “deployment-oriented” instead of simply “benchmark-driven”?
**Likely asker:** Any  
**Answer:** Because the experiments were chosen to test operator-relevant behaviors: inference feasibility, cross-dataset transfer, success under infrastructure constraints, and energy savings at scale. The goal was not to maximize benchmark scores in isolation. It was to show practical orchestration value.

130. **Question:** Why should the committee trust your comparisons to baselines?
**Likely asker:** Any  
**Answer:** Because the baselines are strong, relevant, and chosen to represent meaningful alternative architectures rather than weak straw men. The evaluation also keeps metrics, tuning logic, and testing structure explicit. That makes the comparisons defensible even where the trade-offs are not one-sided.

## N. Agentic Architecture And PARES Questions

131. **Question:** Why did you define the `PARES` framework?
**Likely asker:** Jordi  
**Answer:** Because agentic systems are often described qualitatively and inconsistently. `PARES` provides a minimal capability vocabulary for what an orchestration agent must actually do: perceive, act, reason, evaluate, and sustain. That makes the architectural discussion more disciplined.

132. **Question:** Why are those five `PARES` capabilities the right ones?
**Likely asker:** Any  
**Answer:** Because they capture the difference between a stateless prompt-based system and a persistent closed-loop agent. Without perception, action, reasoning, evaluation, and memory, orchestration reduces to a brittle one-shot tool call. The five capabilities together define functional autonomy.

133. **Question:** Why is the role ordering `Intent -> Observe -> Plan -> Act` important?
**Likely asker:** Jordi  
**Answer:** Because the workflow needs to move from meaning to state to decision to execution. If intent is unclear, planning is unconstrained. If current state is unknown, planning is unsafe. The sequence reflects the logic of the orchestration problem rather than an arbitrary software pipeline.

134. **Question:** Why is memory or persistence necessary for orchestration agents?
**Likely asker:** Any  
**Answer:** Because orchestration is not a one-turn problem. The system needs to remember previous failures, rejected plans, and interaction context to improve subsequent decisions. Without persistence, the agent would keep rediscovering the same mistakes.

135. **Question:** Why is tool access such a central part of the agentic framework?
**Likely asker:** Ferran  
**Answer:** Because orchestration agents must inspect infrastructure and act on it through concrete APIs rather than only produce text. Tool access is what turns reasoning into operational behavior. Without it, the system would remain an advisory model rather than an orchestration framework.

136. **Question:** Why does dynamic schema generation matter more than static schema design?
**Likely asker:** Jordi  
**Answer:** Because the set of valid actions changes with infrastructure state. A static schema can enforce format, but not state-aware feasibility. Dynamic schemas let the system remove invalid options before the agent commits to them.

137. **Question:** Why is multi-agent communication modeled as message passing?
**Likely asker:** Any  
**Answer:** Because it provides a clean abstraction for specialization and coordination without merging all reasoning into one context. Each agent can produce structured outputs for the next stage while preserving modularity. It also makes future distributed deployments easier to conceptualize.

138. **Question:** Why is the “structured output error reduction” argument important?
**Likely asker:** Jordi  
**Answer:** Because it gives a formal reason why constrained outputs should fail less often than unconstrained ones. It is not only a software-engineering convenience. It is a theoretical justification for reducing infeasible action probability by shrinking the choice set.

139. **Question:** Why do you claim distributed reasoning benefits grow with task complexity?
**Likely asker:** Any  
**Answer:** Because the monolithic success probability degrades with sequential step interactions, while specialized agents maintain higher local accuracy. The theoretical comparison in the background chapter formalizes that difference. So the architecture is supported both empirically and mathematically.

140. **Question:** Why not let one very strong model reason about everything with chain-of-thought?
**Likely asker:** Any  
**Answer:** Because orchestration involves heterogeneous subtasks with different information needs and failure modes. Even a strong model still suffers when every task is merged into one growing reasoning context. Specialization reduces cognitive overload and makes the workflow easier to validate.

## O. Additional Committee-Specific And Pressure Questions

141. **Question:** If I am a radio-resource-management expert, why should I care about this thesis?
**Likely asker:** Ferran, Jordi  
**Answer:** Because the thesis addresses a complementary but increasingly important control layer above low-level radio scheduling: service orchestration over distributed edge-cloud infrastructure. As networks become more programmable and service-aware, that layer matters more. The work is relevant because it helps connect prediction, transfer, and safe control to real operator workflows.

142. **Question:** If I am skeptical of LLMs in infrastructure, what is your strongest argument?
**Likely asker:** Lorenza  
**Answer:** My strongest argument is not that LLMs are inherently reliable, but that they become more useful when embedded inside constrained, validated workflows. `AgentEdge` does not trust free-form generation blindly. It combines specialization, schemas, and simulation to reduce risk.

143. **Question:** What is the strongest argument against your own thesis?
**Likely asker:** Any  
**Answer:** The strongest argument is that the full telco-grade deployment realism is not yet proven end-to-end. That is a fair criticism. My response is that the thesis still makes a real contribution by establishing the design principles and validated evidence needed before such deployment becomes possible.

144. **Question:** Which result in the thesis are you personally most confident about?
**Likely asker:** Any  
**Answer:** I am most confident about the integrated pattern that lightweight, generalizable, and validated components outperform isolated or naive alternatives when evaluated on operator-relevant criteria. If I had to choose one chapter-specific result, the digital twin ablation in `AgentEdge` is especially compelling because it isolates one core design decision so clearly.

145. **Question:** Which result are you least confident about?
**Likely asker:** Any  
**Answer:** I am least confident about extrapolating the current results directly to every future 6G deployment scenario, especially under richer wireless dynamics. The thesis provides strong evidence at the orchestration level, but not universal proof across all infrastructure realities. That is why I keep the claims carefully scoped.

146. **Question:** If you had six more months, what chapter would improve the most?
**Likely asker:** Any  
**Answer:** `AgentEdge` would improve the most, because agentic orchestration still has the richest open design space around trust, model selection, context management, and distributed coordination. The forecasting chapters are more mature technically. The orchestration chapter still has the biggest headroom for expansion.

147. **Question:** Which committee member are you most prepared for intellectually, and why?
**Likely asker:** Any  
**Answer:** I would answer diplomatically that the dissertation was prepared to engage all three dimensions represented by the committee: wireless systems realism, resource management rigor, and simulation/automation trustworthiness. The thesis structure itself mirrors those concerns. So it is intentionally built for multidimensional scrutiny.

148. **Question:** If your committee says the thesis feels like three papers rather than one dissertation, what do you answer?
**Likely asker:** Any  
**Answer:** I would say the chapters are sequentially interdependent rather than merely adjacent. `AERO` solves deployability, `OmniFORE` solves scalability of forecasting, and `AgentEdge` solves safe action. The connective logic is explicit in the objectives, background gaps, presentation structure, and conclusion chapter.

149. **Question:** If someone says the work is “too systems” and not “AI enough,” what do you answer?
**Likely asker:** Any  
**Answer:** I would say the AI content is substantial but intentionally judged by systems impact rather than model novelty alone. The thesis uses machine learning, attention mechanisms, and agentic AI in service of deployment-ready orchestration. That is appropriate because the research problem itself is systems-oriented.

150. **Question:** If someone says the work is “too AI” and not “networking enough,” what do you answer?
**Likely asker:** Any  
**Answer:** I would answer that the AI methods are only one layer of the contribution. The thesis is grounded in orchestration objectives, infrastructure constraints, QoS, energy trade-offs, service placement, and distributed system realities. In other words, the AI is the means, but the networking-orchestration problem remains the core.

## P. AERO Formalization And Edge-Deployment Questions

151. **Question:** Why did you model workload as a multivariate vector instead of forecasting only one scalar?
**Likely asker:** Ferran  
**Answer:** Because orchestration decisions depend on several resource dimensions jointly, not on CPU alone. A multivariate representation captures interactions between resources such as CPU and memory, which makes the prediction more useful for real scheduling. A scalar-only formulation would simplify the problem too much.

152. **Question:** Why forecast a horizon `lambda` instead of only the next step?
**Likely asker:** Any  
**Answer:** Because orchestration often needs a short planning window rather than a single immediate estimate. A horizon gives the scheduler time to act proactively, for example by reallocating resources before violations occur. One-step prediction would be too reactive for many scenarios.

153. **Question:** Why separate historical context `kappa` from forecast horizon `lambda` in the formulation?
**Likely asker:** Jordi  
**Answer:** Because they play different roles. `kappa` determines how much past evidence the model observes, while `lambda` determines how far ahead the system plans. Keeping them separate makes the forecasting problem more interpretable and tunable.

154. **Question:** Why optimize `AERO` with `MSE` if you later emphasize `MAE` and orchestration outcomes?
**Likely asker:** Lorenza  
**Answer:** `MSE` is a practical training objective because it penalizes larger errors strongly and is stable for optimization. But training loss is not the whole story, so I also report `MAE` and system-level metrics to show deployment relevance. In short, `MSE` supports learning, while the other metrics support evaluation.

155. **Question:** Why was container-level prediction so important in your thesis?
**Likely asker:** Any  
**Answer:** Because microservice systems are orchestrated at fine granularity, and decisions are often made per container or per service unit. Node-level aggregates hide the local dynamics that actually drive elasticity and placement. Container-level prediction is therefore closer to the true control problem.

156. **Question:** Why does the edge-cloud architecture include edge, fog, and cloud tiers instead of a simpler two-tier model?
**Likely asker:** Ferran  
**Answer:** Because the real deployment continuum is heterogeneous, with different latency, capacity, and resource profiles across tiers. A three-tier view better reflects the kinds of trade-offs orchestration must handle. Simplifying that too much would weaken the deployment claim.

157. **Question:** Why include CPU, memory, disk, and network capacities in the simulation architecture?
**Likely asker:** Jordi  
**Answer:** Because real scheduling decisions are constrained by multiple bottlenecks, not only compute. A service can be CPU-light but network-heavy, or memory-limited rather than processor-limited. Modeling several resource dimensions makes the orchestration environment more realistic.

158. **Question:** Why does proactive scheduling depend so strongly on forecast quality?
**Likely asker:** Any  
**Answer:** Because proactive action is only useful when the predicted demand is credible enough to justify acting before the event occurs. If the forecast is poor, early actions can waste resources or introduce instability. So prediction quality directly affects orchestration quality.

159. **Question:** Why is extending `COSCO` with a prediction interface a real contribution rather than an implementation detail?
**Likely asker:** Lorenza  
**Answer:** Because it creates the bridge between forecasting models and orchestration outcomes. Without that bridge, prediction results remain disconnected from scheduler behavior and system impact. The interface turns model accuracy into measurable operational consequences.

160. **Question:** Why is edge deployability more than just model compression?
**Likely asker:** Ferran  
**Answer:** Because deployment feasibility depends on latency, energy use, and operational simplicity, not only parameter count. A compressed model can still be too slow, too brittle, or too costly to run locally. `AERO` matters because it combines small size with practical runtime behavior.

## Q. OmniFORE Pipeline And Generalization Questions

161. **Question:** Why use latent-space clustering before training the forecasting model?
**Likely asker:** Any  
**Answer:** Because the goal is to train on representative workload diversity rather than on an arbitrary subset. Clustering organizes heterogeneous traces by underlying temporal structure, which helps the training set cover the space more intelligently. That directly supports generalization.

162. **Question:** Why cluster in latent space instead of clustering the raw traces directly?
**Likely asker:** Jordi  
**Answer:** Because raw time-series are high-dimensional, noisy, and difficult to cluster reliably. The latent representation compresses them into a denser space that preserves the important temporal structure. That makes clustering both more efficient and more meaningful.

163. **Question:** Why did you prefer unsupervised clustering rather than manual workload labels?
**Likely asker:** Lorenza  
**Answer:** Because workload traces do not come with a clean taxonomy in practice, and manual labeling would not scale. An unsupervised approach is more realistic for large operational datasets. It also lets the structure emerge from the traces themselves rather than from human assumptions.

164. **Question:** Why select training traces proportionally from each cluster?
**Likely asker:** Any  
**Answer:** Because the training set should reflect the empirical structure of the full dataset without collapsing into only the dominant trace types. Proportional sampling preserves diversity while remaining faithful to observed prevalence. It is a practical compromise between coverage and representativeness.

165. **Question:** Why normalize each trace individually instead of applying one global normalization?
**Likely asker:** Lorenza  
**Answer:** Because traces can differ greatly in scale, and global normalization would let large-magnitude traces dominate training. Per-trace normalization lets the model focus on temporal structure rather than raw magnitude alone. That supports cross-application generalization better.

166. **Question:** Why keep the original time-series after clustering instead of training directly on the latent vectors?
**Likely asker:** Jordi  
**Answer:** Because the latent space is mainly a tool for representation and selection, not the final forecasting target. The actual forecasting model still needs the time-series dynamics in their usable temporal form. Keeping the original traces preserves operational meaning.

167. **Question:** Why use attention in `OmniFORE` after the clustering pipeline?
**Likely asker:** Ferran  
**Answer:** Because clustering improves which traces the model sees, while attention improves how dependencies are learned within those traces. They solve different problems. The combination addresses both training-set diversity and sequence modeling quality.

168. **Question:** Why did you instantiate the framework with `Informer` instead of a standard transformer?
**Likely asker:** Any  
**Answer:** Because standard self-attention has quadratic complexity and becomes expensive for long sequences. `Informer` offers a more efficient sparse-attention design while still capturing long-range dependencies. That makes it a better fit for the framework's efficiency goals.

169. **Question:** Why was Bayesian optimization appropriate for the final hyperparameter stage?
**Likely asker:** Jordi  
**Answer:** Because the hyperparameter space is too large for exhaustive search, and the objective is expensive to evaluate. Bayesian optimization uses previous observations to search more efficiently. That is especially valuable when the real target is generalization across many traces rather than one workload.

170. **Question:** What is the main risk if the clustering stage is wrong?
**Likely asker:** Any  
**Answer:** The main risk is that the training subset stops being representative, so the model overfits to the wrong structure and generalizes poorly. In other words, bad clustering does not just hurt preprocessing; it weakens the entire pipeline. That is why the clustering stage matters scientifically.

## R. Trust, Benchmarking, And Security Questions

171. **Question:** Why do you say orchestration benchmarks are harder to build than standard machine-learning benchmarks?
**Likely asker:** Lorenza  
**Answer:** Because orchestration tasks have many acceptable solutions rather than one correct label. A good decision may trade energy, latency, and reliability differently from another good decision. That makes evaluation more complex than simple label matching.

172. **Question:** Why do agentic evaluations need repeated trials and confidence intervals?
**Likely asker:** Jordi  
**Answer:** Because the same system can behave differently across runs due to LLM non-determinism and scenario variation. A single run can therefore misrepresent true performance. Repeated trials make the conclusions statistically more credible.

173. **Question:** Why is it important that orchestration scenarios admit multiple acceptable trajectories?
**Likely asker:** Any  
**Answer:** Because real operators care about satisfying constraints and objectives, not about reproducing one exact action sequence. Two plans can both be valid while using different paths through the solution space. The evaluation methodology must respect that reality.

174. **Question:** Why might smaller fine-tuned models become more attractive than very large general-purpose models?
**Likely asker:** Ferran  
**Answer:** Because orchestration is a narrow but high-value domain where speed, cost, and consistency matter a lot. A specialized smaller model could reason faster and more cheaply while matching or exceeding practical quality. That is a strong future direction for deployment.

175. **Question:** Why are explanation traces important if the outcome metrics are already good?
**Likely asker:** Lorenza  
**Answer:** Because operators need to understand why an agent chose one plan and rejected others before they trust it. Good metrics alone do not guarantee acceptance in operational settings. Explanations are part of the trust mechanism, not just a reporting convenience.

176. **Question:** Why might constraint-clamping guardrails be better than simply rejecting invalid outputs?
**Likely asker:** Jordi  
**Answer:** Because clamping can preserve the conversation and teach the agent what boundary it violated. Pure rejection often just stops the workflow without helping the next step improve. A guided correction loop can be both safer and more useful.

177. **Question:** Why is the separation between planning and execution important for security?
**Likely asker:** Any  
**Answer:** Because it prevents raw reasoning errors from immediately becoming infrastructure actions. The extra validation layer limits blast radius and gives the system a chance to detect problems before commit. That architectural separation is a practical safety mechanism.

178. **Question:** Why is data locality a serious issue for orchestration agents?
**Likely asker:** Lorenza  
**Answer:** Because the agent needs detailed operational state such as resource usage, service configurations, and infrastructure status. Sending that data to external inference providers can create privacy, compliance, and control concerns. This is not only an AI issue; it is an operational-governance issue.

179. **Question:** Why could federated or local inference matter in future orchestration systems?
**Likely asker:** Ferran  
**Answer:** Because they reduce the need to export sensitive state and can improve control over latency and reliability. In infrastructure management, keeping data and inference closer to the system often has practical advantages. That makes local or federated approaches appealing beyond academic interest.

180. **Question:** Why do you emphasize malfunction and misalignment more than classic prompt injection threats?
**Likely asker:** Any  
**Answer:** Because these agents are intended to run in protected operational environments, so the bigger risk is often internal failure rather than open public misuse. A well-authorized but wrong action can still be highly damaging. The safety problem is therefore strongly about containment and verification.

## S. Context Engineering, Latency, And Tooling Questions

181. **Question:** Why is state staleness such a fundamental issue for `AgentEdge`?
**Likely asker:** Jordi  
**Answer:** Because infrastructure changes continuously while LLM reasoning takes time. The world the agent observes may no longer be the world in which it acts. If that gap is ignored, even a logically correct plan can become invalid by execution time.

182. **Question:** Why not just pass the full infrastructure state to the model every time?
**Likely asker:** Lorenza  
**Answer:** Because full state quickly overwhelms the context window and leaves little room for reasoning. It also increases cost and can bury the relevant signals in noise. Better context selection is therefore necessary, not optional.

183. **Question:** Why can having more tools actually reduce agent performance?
**Likely asker:** Any  
**Answer:** Because larger tool catalogs increase selection ambiguity and cognitive load. The model spends more effort deciding what to use and is more likely to choose poorly. Beyond a certain point, more capability becomes less usable capability.

184. **Question:** Why did removing an MCP server sometimes improve success?
**Likely asker:** Jordi  
**Answer:** Because reducing tool and context overload can make the remaining reasoning pipeline clearer. The agent has fewer irrelevant options competing for attention. That result suggests current LLMs still struggle with large orchestration toolspaces.

185. **Question:** Why is semantic tool discovery a promising future direction?
**Likely asker:** Ferran  
**Answer:** Because it could retrieve a small relevant subset of tools before reasoning begins, instead of exposing the model to an entire catalog. That reduces context pressure and improves selection quality. It is a natural next step for production-scale environments.

186. **Question:** Why is model-agnostic agent design still difficult in practice?
**Likely asker:** Any  
**Answer:** Because different models and providers vary in output formatting, tool-calling behavior, and prompt sensitivity. Even when the architecture stays the same, the operational behavior shifts. So portability is harder than simply swapping model names.

187. **Question:** Why can the same model behave differently across providers?
**Likely asker:** Lorenza  
**Answer:** Because providers differ in wrappers, response formatting, API conventions, and sometimes inference behavior. That means portability problems exist at both the model layer and the serving layer. It is a systems-integration challenge as much as an AI one.

188. **Question:** Why does a sequential multi-agent workflow not scale well by simply adding more agents?
**Likely asker:** Jordi  
**Answer:** Because each added stage usually adds more latency and more opportunities for error propagation. A longer chain does not automatically produce better reasoning. Past a point, sequential depth becomes a bottleneck rather than an advantage.

189. **Question:** Why are multiple `AgentEdge` instances harder than a single instance?
**Likely asker:** Any  
**Answer:** Because once several instances act on shared infrastructure, they can produce conflicting plans. Coordination then becomes a distributed systems problem, not only an AI reasoning problem. The hard part shifts from local planning to conflict management.

190. **Question:** Why do future distributed agent instances need explicit coordination protocols?
**Likely asker:** Jordi  
**Answer:** Because implicit coordination through shared infrastructure is too fragile when actions can conflict. Protocols are needed to negotiate resources, detect clashes, and agree before commit. Without that, scaling autonomy could create destructive interference.

## T. Future Research And Brutal Committee Questions

191. **Question:** What new benchmark would most strengthen this dissertation if you could build it next?
**Likely asker:** Any  
**Answer:** A benchmark suite for orchestration agents with diverse intents, infrastructure states, and multiple acceptable outcomes would strengthen it the most. That would make `AgentEdge` evaluation more systematic and comparable across models and architectures. It would directly address one of the clearest open gaps.

192. **Question:** What missing evidence would most convince a skeptical operator?
**Likely asker:** Lorenza  
**Answer:** A controlled live deployment where the agent manages a bounded subset of orchestration tasks with real re-validation and rollback safeguards would be the strongest evidence. That would test trust under operational drift, not only under experimental control. It is the most persuasive next step toward adoption.

193. **Question:** Which future research direction has the highest near-term payoff?
**Likely asker:** Jordi  
**Answer:** Better evaluation engineering and benchmark design likely have the highest near-term payoff. They immediately improve reproducibility, model comparison, and development speed. Without that foundation, many other improvements are harder to measure properly.

194. **Question:** Which future research direction is the most ambitious long-term one?
**Likely asker:** Any  
**Answer:** Distributed multi-agent coordination across shared infrastructure is probably the most ambitious long-term direction. It combines AI reasoning, protocol design, conflict resolution, and systems scalability. Solving that would move the work much closer to truly large-scale zero-touch orchestration.

195. **Question:** If an internal world model and an external digital twin disagree, which would you trust more?
**Likely asker:** Jordi  
**Answer:** I would trust whichever one has stronger validation for the specific operational context, but in the near term I would default to the external twin because it is more inspectable and easier to benchmark explicitly. An internal world model is promising, but it introduces another learned layer that must itself be trusted. So the answer depends on evidence, not on elegance.

196. **Question:** What should happen when operator intent conflicts with feasibility?
**Likely asker:** Ferran  
**Answer:** The system should not pretend the request is feasible. It should surface the conflict clearly, explain which constraint fails, and propose the nearest valid alternatives. That preserves trust better than silently degrading the objective.

197. **Question:** What do you do when QoS, load balancing, and energy cannot all be optimized together?
**Likely asker:** Jordi  
**Answer:** I would state that this is exactly why the thesis uses explicit trade-offs and intent-driven prioritization. The goal is not to eliminate conflict but to manage it transparently. A good orchestration system makes the compromise explicit and aligned with operator goals.

198. **Question:** In the near term, what is the role of the human operator in zero-touch orchestration?
**Likely asker:** Any  
**Answer:** The operator still defines goals, reviews boundaries, and authorizes the degree of autonomy. Near-term zero-touch does not mean zero human governance. It means shifting humans from manual execution toward supervision and policy definition.

199. **Question:** What limitation should you volunteer yourself before the committee points it out?
**Likely asker:** Any  
**Answer:** I would proactively say that the thesis demonstrates validated autonomy convincingly at the research-prototype level, but not yet full telco-production generality across all network conditions and operational stacks. That limitation is real and already informs the future-work agenda. Stating it early makes the scope sound rigorous rather than defensive.

200. **Question:** What is the clearest one-minute statement of the next research step after this dissertation?
**Likely asker:** Any  
**Answer:** The next step is to move from strong prototype evidence to trustworthy production pathways. Concretely, that means better orchestration benchmarks, stronger guardrails and explainability, leaner specialized models, and live bounded deployments with re-validation. In short, the future is not more autonomy alone, but more trustworthy autonomy.
