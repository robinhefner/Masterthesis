---
Author: "[[Austin Barr]]"
Journal: "[[Frontiers in Artificial Intelligence]]"
Title: "Large language models generating synthetic clinical datasets: a feasibility and comparative analysis with real-world perioperative data"
---

# [[Barr et al. 2025.pdf|Large language models generating synthetic clinical datasets: a feasibility and comparative analysis with real-world perioperative data]]


### Research Gap:

> ([[Barr et al. 2025.pdf#page=2&annotation=1278R|Barr et al. 2025, p.2]])
> Use of LLMs for [[Synthetische Patiendendaten|synthetic data generation]] may offer an accessible alternative to [[GAN]]s and [[VAE]]s, reducing the need for specialized knowledge and computational resources, which could broaden the reach of synthetic data use in research and [[ML]] model development.

> ([[Barr et al. 2025.pdf#page=2&annotation=1281R|Barr et al. 2025, p.2]])
> This study aims to assess the feasibility of generating realistic tabular clinical data with OpenAI’s GPT-4o (Hurst et al., 2024) using zero-shot prompting, and evaluate the fidelity of LLM-generated data by comparing its statistical properties to the Vital Signs DataBase (VitalDB) (Lee et al., 2022), a real open-source multi-parameter perioperative dataset.


### Methodik:

Model: [[GPT-4o]]

Dataset: [[VitalDB]] [[Barr et al. 2025.pdf#page=2&annotation=1287R|Barr et al. 2025, p.2]]

2 Phasen:
> ([[Barr et al. 2025.pdf#page=2&annotation=1316R|Barr et al. 2025, p.2]])
> In Phase 1, GPT-4o was prompted with high-level qualitative descriptions of the 13 clinical parameters, to assess its ability to generate a complete and contextually relevant tabular dataset without guiding statistics.
> ([[Barr et al. 2025.pdf#page=2&annotation=1318R|Barr et al. 2025, p.2]])
> In Phase 2, GTP-4o was prompted to generate a synthetic dataset using descriptive statistics of the VitalDB dataset.

> ([[Barr et al. 2025.pdf#page=3&annotation=1320R|Barr et al. 2025, p.3]])
> GPT-4o application programming interfaces (API) were not used in order to determine feasibility of data generation without further technical expertise and resources.

> ([[Barr et al. 2025.pdf#page=3&annotation=1322R|Barr et al. 2025, p.3]])
> Continuous variables were compared using two-sample t-tests and 95% CI overlap.

### Main Finding:

> ([[Barr et al. 2025.pdf#page=4&annotation=1324R|Barr et al. 2025, p.4]])
> 12/13 (92.31%) parameters from the Phase 2 dataset did not show statistically significant differences from VitalDB

> ([[Barr et al. 2025.pdf#page=4&annotation=1326R|Barr et al. 2025, p.4]])
> Overall, generated data in Phase 1 was realistic, displayed appropriate ranges, included correct calculations without the provision of descriptive statistics, formulas, or unit conversions

> ([[Barr et al. 2025.pdf#page=4&annotation=1328R|Barr et al. 2025, p.4]])
> However, proportions among categorical and binary variables did not differ based on context.

-> ohne Statistiken im Prompt verteilt GPT-4o Kategorien einfach gleichmäßig

> ([[Barr et al. 2025.pdf#page=6&annotation=1330R|Barr et al. 2025, p.6]])
> data generation using LLMs is accessible to anyone with an internet connection


### Limitation:

> ([[Barr et al. 2025.pdf#page=6&annotation=1332R|Barr et al. 2025, p.6]])
> this study focused solely on GPT-4o, and it remains uncertain whether similar results would be achieved using other LLMs.

> ([[Barr et al. 2025.pdf#page=6&annotation=1334R|Barr et al. 2025, p.6]])
> it is unclear whether bivariate and multivariate relationships were retained by the LLM-based approach, as this was not directly assessed.



### Zentrales Zitat:
> ([[Barr et al. 2025.pdf#page=7&annotation=1336R|Barr et al. 2025, p.7]])
> without explicit guidance, LLMs may produce plausible but statistically unaligned data.



---
Abgrenzung zu meiner Arbeit :

Ein einziger Zero-Shot-Prompt im ChatGPT-Interface, kein Agent, keine API
- Meine MAA arbeitet mit spezialisierten Agenten und automatisierter Pipeline

Output ist eine flache Tabelle (13 Parameter), keine Zusammenhänge zwischen Variablen geprüft
- Ich arbeite mit [[FHIR]], wo Beziehungen zwischen Ressourcen (Patient, Encounter, Condition ...) explizit sind und validiert werden können

Evaluation nur statistisch (t-Tests, CI-Overlap), keine klinische Plausibilitätsprüfung pro Patient
- Rechtfertigung für meinen Validator und mein Medical Review

Phase 1 vs. Phase 2 zeigt: Statistiken im Prompt verbessern die Fidelity stark (vgl. Prior Knowledge bei [[Hao et al., 2024]])
