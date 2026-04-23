# Committee Defense Notes

This file is a fast pre-defense brief for the three committee members: generic background, visible research profile, and the kinds of technical questions they are most likely to care about. Recent paper notes live in the full-name folders inside this directory.

## Ferran Adelantado i Freixer

| Field | Value |
|-------|-------|
| **Current roles** | Associate Professor at UOC; Adjunct Associate Professor at UB |
| **Group** | Wireless Networks Research Lab (WiNe), UOC |
| **Training** | Telecommunications Engineering (UPC, 2001); Ph.D. (UPC, 2007); B.Sc. Business Sciences (UOC, 2014) |
| **Useful links** | [UOC profile](https://recerca.uoc.edu/investigadores/881908/detalle?lang=en), [personal site](https://www.ferranadelantado.com/), [ORCID](https://orcid.org/0000-0002-9696-1169), [Google Scholar](https://scholar.google.com/citations?user=WFiOI9cAAAAJ) |

### Research profile

- LPWAN / LoRaWAN and IoT connectivity
- 5G/6G network slicing and wireless optimization
- AI and DRL for O-RAN resource management
- Non-terrestrial networks and satellite-assisted IoT
- V2X and network-aware QoS optimization

### Useful for your defense

- Strong overlap with AI-enabled orchestration, slicing, and distributed edge/network intelligence
- Likely to value technically grounded claims about constraints, scalability, and deployment realism
- Recent work spans theory plus implementable wireless-system decisions, not only abstract optimization

### Likely question angles

- Why is your controller or orchestration policy better than simpler heuristics or static allocation?
- How do you manage cross-slice trade-offs, QoS guarantees, and fairness?
- How sensitive are your results to wireless constraints, traffic variation, or deployment assumptions?
- How realistic is the path from simulation or prototype to operational O-RAN / NTN settings?

## Jordi Pérez-Romero

| Field | Value |
|-------|-------|
| **Current role** | Full Professor (Catedrático), Universitat Politècnica de Catalunya |
| **Group** | Mobile Communications Research Group (GRCM), Dept. of Signal Theory and Communications |
| **Training** | Telecommunications Engineering (UPC, 1997); Ph.D. (UPC, 2001) |
| **Useful links** | [UPC profile](https://grcm.tsc.upc.edu/en/about-the-group/faculty/jordi-perez-romero), [Google Scholar](https://scholar.google.com/citations?user=hJYxus0AAAAJ), [DBLP](https://dblp.org/pid/74/84.html) |

### Research profile

- Radio resource management and QoS provisioning
- Heterogeneous and cognitive wireless networks
- Network slicing and slice management
- Self-organizing networks and AI-based RRM
- O-RAN / disaggregated RAN functional split management

### Useful for your defense

- Very likely to test the rigor of your system model, optimization objective, and evaluation methodology
- Strong standardization and systems background means he may ask whether the work is deployable, not only interesting
- Good person to anticipate questions about baselines, KPIs, and resource-allocation logic

### Likely question angles

- Why these KPIs, constraints, and optimization objectives?
- What trade-off do you make between utilization, QoS, fairness, and complexity?
- How does your approach compare with classical RRM, SON, or network slicing controllers?
- Which assumptions would break first in a real deployment?
- How does the work map to current 5G / O-RAN practice rather than a fully custom stack?

### Committee note

- Because he is a UPC full professor, double-check whether he counts as internal vs external under the program rules.

## Lorenza Giupponi

| Field | Value |
|-------|-------|
| **Public background** | Ph.D. from UPC (2007); long public CTTC / MONET track record; Google Scholar profile verified at `ericsson.com` |
| **Visible recent themes** | ML for RAN automation, SON, 5G/NR, coexistence, NR V2X, system-level simulation |
| **Useful links** | [Google Scholar](https://scholar.google.com/citations?user=nPKg7R8AAAAJ), [DBLP](https://dblp.org/pid/18/3312.html), [CTTC ML for RAN project](https://www.cttc.cat/project/efficient-machine-learning-for-ran/), [CTTC NR V2X project](https://www.cttc.cat/project/modeling-simulation-and-performance-evaluation-of-nr-v2x/) |

### Research profile

- Machine learning for RAN automation and control loops
- Self-organizing networks and traffic prediction
- 5G/NR coexistence and unlicensed-spectrum behavior
- NR V2X and mobility-aware performance evaluation
- System-level modeling and simulation for realistic wireless studies

### Useful for your defense

- Especially relevant if your thesis relies on simulation, adaptive control, or ML-driven decision-making
- Likely to care about robustness outside the exact training or evaluation setting
- May focus on reproducibility, deployment realism, and behavior under mobility, interference, or heterogeneous services

### Likely question angles

- Which simulator, workload, or channel assumptions matter most to your conclusions?
- How well does the approach generalize across scenarios, traffic patterns, or radio conditions?
- How much data, observability, or feedback does the controller need to work well?
- How do you prevent instability, overfitting, or failure under distribution shift?
- What changes when the environment becomes more mobile, interference-limited, or heterogeneous?
