# Backup Slide Quick Index

Printable Q&A sheet for the backup slides.

`BRACE`: `Breathe -> Restate -> Answer first -> Cite one anchor -> Edge and end`

## Fast jump by question type

- Runtime, practicality, staleness: `B1`, `B2`, `B10`, `B12`
- Methodology, rigor, fairness, datasets, reproducibility: `B3` to `B7`
- Agent definition, success rate, metric validity: `B8`, `B9`, `B11`
- `AERO` / `OmniFORE` technical follow-ups: `B13` to `B16`
- 6G scope and outputs: `B17`, `B18`

## Slide-by-slide index

| Slide | Topic / use | One anchor to remember |
| --- | --- | --- |
| `B0` | Use if you want a visual menu before jumping to a backup. | Backup index slide |
| `B1` | Planning is too slow; the plan may be stale before execution; `700 s` sounds impractical. | `107 s -> 48 s`; `0` unsafe actions |
| `B2` | Runtime will improve without redesign; newer smaller models make the planner more practical. | `~7x` smaller model already scores higher |
| `B3` | Are the gains statistically real, or just split noise? | `630` runs; `2.76x` uplift; `10x` lower variance |
| `B4` | Were the baselines given a fair chance? | Shared `50`-trial tuning budget; shared `12` APIs |
| `B5` | Why these traces, pods, cells, or datasets? Is there selection bias? | `100` Google traces; `6 x 60` AgentEdge matrix |
| `B6` | Is the simulator too friendly? Can the twin be trusted? | `15-25%` injected jitter; live `AERO` validation |
| `B7` | How is this reproducible if the LLM changes? | `60` runs per arm; same LLM across agent baselines |
| `B8` | What exactly counts as an agent here? Is AgentEdge really agentic? | `PARES` = `5` capabilities |
| `B9` | If the twin validates plans, why is success `78.3%` and not `100%`? | `78.3%` vs `53.3%`; `1.47x` uplift from `ActSimCrit` |
| `B10` | Why does scaling peak at `20` nodes and drop at `35`? What about the `150 ms` target? | `300.8 W` peak saving at `20` nodes |
| `B11` | Is exact end-state matching a fair success metric? | `6` scenarios x `60` runs; multiple valid end-states |
| `B12` | What happens if live state changes between planning and execution? | Three-tier state isolation; per-call recovery |
| `B13` | Why does `Pathformer` look lighter in the CPU/RAM chart? | `2.4 M` vs `599` params; `~4000x` smaller |
| `B14` | Why did you not benchmark `AERO` directly against `Informer`? | Beat the stronger heavy baseline: `Pathformer` |
| `B15` | Can `AERO` work beyond CPU/RAM, e.g. other recurrent 6G signals? | `599` params; `0.38 ms` inference |
| `B16` | Where does `OmniFORE` run, and is the zero-shot transfer protocol leak-free? | Train on `A-F`, freeze, test held-out target |
| `B17` | Is this really a 6G thesis, or mainly a cloud thesis? | Orchestration layer above radio; `Nearby Computing` |
| `B18` | Show the publication list / research outputs. | `8` publications with full bibliographic data |

## Short routing rules

- If the question is about **"too slow today"**, start with `B1`.
- If the question is about **"why this gets better tomorrow"**, go to `B2`.
- If the question is about **fairness or rigor**, stay in `B3` to `B7`.
- If the question is about **what AgentEdge really claims**, stay in `B8` to `B12`.
- If the question is about **forecasting-model details**, go to `B13` to `B16`.
- If the question is about **thesis scope or track record**, end on `B17` or `B18`.
