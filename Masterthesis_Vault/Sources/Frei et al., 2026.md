---
Author: "[[Johann Frei]]"
Journal: "[[PrePrint]]"
Title: "Infherno: End-to-end Agent-based FHIR Resource Synthesis from Free-form Clinical Notes"
---

# [[Frei et al., 2026.pdf|Infherno: End-to-end Agent-based FHIR Resource Synthesis from Free-form Clinical Notes]]

### Research Gap:

> ([[Frei et al., 2026.pdf#page=1&annotation=1009R|Frei et al., 2026, p.1]])
> Previous attempts at automating the translation from freeform clinical notes into structured [[FHIR]] resources address narrowly defined tasks and rely on modular approaches or LLMs with instruction tuning and constrained decoding.
> ([[Frei et al., 2026.pdf#page=1&annotation=1011R|Frei et al., 2026, p.1]])
> As those solutions frequently suffer from limited generalizability and structural inconformity

> ([[Frei et al., 2026.pdf#page=2&annotation=1013R|Frei et al., 2026, p.2]])
> A recurring challenge in such tasks is ensuring that the output adheres to a specified schema


### Methodik:

> ([[Frei et al., 2026.pdf#page=1&annotation=1015R|Frei et al., 2026, p.1]])
> we propose an end-to-end framework powered by LLM agents, code execution, and healthcare terminology database tools to address these issues.

> ([[Frei et al., 2026.pdf#page=3&annotation=1017R|Frei et al., 2026, p.3]])
> Our approach follows the ThoughtCode-Observation structure proposed as the ReAct framework by Yao et al. (2023), and is implemented using the Smolagents (Roucher et al., 2025) library

Tools:
- Terminology Search (SNOMED CT über FHIR-Terminologieserver) [[Frei et al., 2026.pdf#page=3&annotation=1019R|Frei et al., 2026, p.3]]
- fhir.resources (Python) zum Erzeugen valider FHIR-Objekte [[Frei et al., 2026.pdf#page=4&annotation=1021R|Frei et al., 2026, p.4]]
- Output als FHIR Bundle [[Frei et al., 2026.pdf#page=4&annotation=1023R|Frei et al., 2026, p.4]]

Datasets:
> ([[Frei et al., 2026.pdf#page=5&annotation=1025R|Frei et al., 2026, p.5]])
> We source ten anonymized English EHR documents from the n2c2 2018 challenge
> ([[Frei et al., 2026.pdf#page=5&annotation=1027R|Frei et al., 2026, p.5]])
> We also rely on ten ChatGPT-synthesized documents resembling medical discharge letters in German

> ([[Frei et al., 2026.pdf#page=5&annotation=1029R|Frei et al., 2026, p.5]])
> we support Patient, Condition, and MedicationStatement as FHIR resources

Models: [[Claude Sonnet 4.5]], [[Gemini 2.5 Pro]], [[GPT-5]], [[DeepSeek V3.1]], [[Qwen3-235B-A22B-2507]], [[Qwen3-8B]] [[Frei et al., 2026.pdf#page=5&annotation=1031R|Frei et al., 2026, p.5]]


### Main Finding:

> ([[Frei et al., 2026.pdf#page=5&annotation=1033R|Frei et al., 2026, p.5]])
> all LLMs demonstrate high precision with minimal fabrication

-> [[Gemini 2.5 Pro]] mit dem besten Recall auf n2c2

> ([[Frei et al., 2026.pdf#page=6&annotation=1035R|Frei et al., 2026, p.6]])
> Notably, in nearly twice as many cases of quality differences, the model performed better than the human baseline rather than worse.

> ([[Frei et al., 2026.pdf#page=6&annotation=1037R|Frei et al., 2026, p.6]])
> First, the phrasing of the input text plays a critical role in annotation consistency.

> ([[Frei et al., 2026.pdf#page=6&annotation=1039R|Frei et al., 2026, p.6]])
> the partially subjective nature of FHIR in fringe cases.


### Limitation:

> ([[Frei et al., 2026.pdf#page=1&annotation=1047R|Frei et al., 2026, p.1]])
> yet ambiguity and feasibility of collecting groundtruth data remain open problems.

> ([[Frei et al., 2026.pdf#page=7&annotation=1041R|Frei et al., 2026, p.7]])
> We rely on a single annotator for the human baseline, which inherently introduces a degree of subjectivity.

> ([[Frei et al., 2026.pdf#page=7&annotation=1043R|Frei et al., 2026, p.7]])
> our scope was intentionally limited to a subset of FHIR resource types (Patient, Condition, MedicationStatement).

> ([[Frei et al., 2026.pdf#page=7&annotation=1045R|Frei et al., 2026, p.7]])
> a SNOMED CT license may be required if selfhosting a FHIR terminology server is desired.



### Zentrales Zitat:
> ([[Frei et al., 2026.pdf#page=7&annotation=1049R|Frei et al., 2026, p.7]])
> An agentic-based flow allows for certain semantic cross-checks within a FHIR Bundle, that cannot be verified through a CFG-based approach.



---
Abgrenzung zu meiner Arbeit :

Infherno übersetzt echte Freitexte in FHIR (Text-to-FHIR), generiert also keine neuen Patienten
- Ich generiere [[Synthetische Patiendendaten]] direkt als FHIR

Ein einzelner ReAct-Agent mit Tools, keine [[Multi Agent Architektur]]
- Tool-Konzept (Terminologie-Suche + fhir.resources-Validierung im Loop) ist aber direkt übernehmbar für meine Agenten

Nur 3 Ressourcentypen (Patient, Condition, MedicationStatement)
- Meine Arbeit kann mehr Ressourcen abdecken (Encounter, Observation, ...)

Argumentation pro agentischen Ansatz gegenüber CFG / Constrained Decoding -> gute Begründung für meine Architekturwahl
