---
Author: "[[Jason Walonoski]]"
Journal: "[[AMIA]]"
Title: "Synthea: An approach, method, and software mechanism for generating synthetic patients and the synthetic electronic health care record"
---

# [[Walonoski et al., 2017.pdf|Synthea: An approach, method, and software mechanism for generating synthetic patients and the synthetic electronic health care record]]

### Research Gap:

> ([[Walonoski et al., 2017.pdf#page=1&annotation=288R|Walonoski et al., 2017, p.1]])
> Our objective is to create a source of synthetic electronic health records that is readily available; suited to industrial, innovation, research, and educational uses; and free of legal, privacy, security, and intellectual property restrictions.

> ([[Walonoski et al., 2017.pdf#page=2&annotation=290R|Walonoski et al., 2017, p.2]])
> The most promising published attempts to generate high-quality RS-EHRs are limited in their reliance on real patient records, scope, or quality.

> ([[Walonoski et al., 2017.pdf#page=2&annotation=292R|Walonoski et al., 2017, p.2]])
> there are few systematic methods for assessing the quality and realism of synthetic health record data.


### Methodik:

> ([[Walonoski et al., 2017.pdf#page=1&annotation=294R|Walonoski et al., 2017, p.1]])
> We developed Synthea, an open-source software package that simulates the lifespans of synthetic patients, modeling the 10 most frequent reasons for primary care encounters and the 10 chronic conditions with the highest morbidity in the United States.

> ([[Walonoski et al., 2017.pdf#page=2&annotation=296R|Walonoski et al., 2017, p.2]])
> our approach guarantees fully synthetic output by accepting only publicly available information and health statistics as inputs.

> ([[Walonoski et al., 2017.pdf#page=2&annotation=298R|Walonoski et al., 2017, p.2]])
> The framework for the synthetic data generation process utilized by Synthea is based on the use of PADARSER, the Publicly Available Data Approach to the Realistic Synthetic EHR.

> ([[Walonoski et al., 2017.pdf#page=3&annotation=300R|Walonoski et al., 2017, p.3]])
> Clinical care maps and statistics are used to construct models of disease progression and treatment in a Generic Module Framework that encodes these models as state transition machines in an open and documented JSON format.

> ([[Walonoski et al., 2017.pdf#page=3&annotation=302R|Walonoski et al., 2017, p.3]])
> generates a skeletal synthetic EHR with coded entries in the Health Level-7 (HL7) Fast Healthcare Interoperability Resources ([[FHIR]]) standard format for the entire lifetime of the synthetic patient.

Module:
- States [[Walonoski et al., 2017.pdf#page=4&annotation=304R|Walonoski et al., 2017, p.4]]
- Transitions [[Walonoski et al., 2017.pdf#page=5&annotation=306R|Walonoski et al., 2017, p.5]]


### Main Finding:

> ([[Walonoski et al., 2017.pdf#page=3&annotation=308R|Walonoski et al., 2017, p.3]])
> A million patient records are freely available on the Internet using standard formats (HL7 FHIR and Consolidated-Clinical Document Architecture)

Validierung am Typ-2-Diabetes-Modul:
> ([[Walonoski et al., 2017.pdf#page=6&annotation=310R|Walonoski et al., 2017, p.6]])
> a Synthea patient was 4000 times more likely to undergo a diabetes-related amputation than the national or state average.

> ([[Walonoski et al., 2017.pdf#page=6&annotation=312R|Walonoski et al., 2017, p.6]])
> Subsequent runs of the simulation produced individual patient records with realistic disease progression and treatments. However, due to the variability of the simulation, replicating population-level statistics proved challenging.

> ([[Walonoski et al., 2017.pdf#page=7&annotation=314R|Walonoski et al., 2017, p.7]])
> medications are often overestimated, probably due to exact prescribing by doctors according to the standard of care and complete medication adherence by patients.


### Limitation:

> ([[Walonoski et al., 2017.pdf#page=3&annotation=316R|Walonoski et al., 2017, p.3]])
> real clinical discovery requires real data.

> ([[Walonoski et al., 2017.pdf#page=8&annotation=318R|Walonoski et al., 2017, p.8]])
> The synthetic data are not suitable or appropriate for research into diseases not covered by the project or research focused on clinical discovery.

> ([[Walonoski et al., 2017.pdf#page=8&annotation=320R|Walonoski et al., 2017, p.8]])
> Varying quality of clinicians – currently all clinicians act perfectly according to the modeled standard of care



### Zentrales Zitat:
> ([[Walonoski et al., 2017.pdf#page=1&annotation=322R|Walonoski et al., 2017, p.1]])
> Synthetic patients can be simulated with models of disease progression and corresponding standards of care to produce risk-free realistic synthetic health care records at scale.



---
Abgrenzung zu meiner Arbeit :

Synthea ist regelbasiert (handgeschriebene State Machines pro Krankheit), kein LLM
- Mein Ansatz nutzt LLM-Agenten und ist damit nicht auf vorhandene Module beschränkt (Erweiterung der Module per LLM: [[Kramer et al., 2025]])

Synthea erzeugt direkt FHIR -> wichtigste Baseline / Vergleich für meine Arbeit
- Kritik an Synthea in anderen Papern: begrenzter Nutzen für Outcome-Modelle ([[Hao et al., 2024]], [[Bennett et al., 2023]]), keine Narrative ([[Park et al., 2026]])

Alle Patienten verhalten sich "perfekt" (Therapietreue, Ärzte nach Leitlinie)
- LLM-generierte Daten können realistischere Abweichungen enthalten, müssen dann aber klinisch geprüft werden (Medical Review)
