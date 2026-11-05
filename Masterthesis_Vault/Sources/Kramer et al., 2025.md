---
Author: "[[Mark Kramer]]"
Journal: "[[PrePrint]]"
Title: Leveraging Generative AI to Enhance Synthea Module Development
---

# [[Kramer et al., 2025.pdf|Leveraging Generative AI to Enhance Synthea Module Development]]

### Research Gap:

> ([[Kramer et al., 2025.pdf#page=3&annotation=1713R|Kramer et al., 2025, p.3]])
> Currently, Synthea module design relies on co-development by clinicians and Synthea experts. While this approach ensures understandability, clinical suitability, and reliability, it can be time-consuming and may result in limited treatment variations.

-> [[Walonoski et al., 2017|Synthea]]

> ([[Kramer et al., 2025.pdf#page=4&annotation=1715R|Kramer et al., 2025, p.4]])
> [[GAN]]s, [[VAE]]s, statistical methods, and deep-learning techniques emulate their training data and are limited to the patient population and medical practices represented by that data.

> ([[Kramer et al., 2025.pdf#page=4&annotation=1717R|Kramer et al., 2025, p.4]])
> However, our review of the literature found no evidence of LLMs being used for this purpose.


### Methodik:

Models: [[Claude 3.5 Sonnet]], [[GPT-4o]], [[Gemini 1.5 Pro]] [[Kramer et al., 2025.pdf#page=4&annotation=1719R|Kramer et al., 2025, p.4]]

> ([[Kramer et al., 2025.pdf#page=5&annotation=1721R|Kramer et al., 2025, p.5]])
> We developed a four-stage methodology for creating Synthea modules using LLMs

1. Disease Profile
> ([[Kramer et al., 2025.pdf#page=6&annotation=1723R|Kramer et al., 2025, p.6]])
> A disease profile is defined as a set of statements that describes the key characteristics and management of a specific medical condition.

2. Initial Module Generation
> ([[Kramer et al., 2025.pdf#page=7&annotation=1725R|Kramer et al., 2025, p.7]])
> the LLM was instructed to add a property to each Synthea state that captures the requirement number(s) that justify the state, providing traceability between the disease profile and the module.

3. Validation
> ([[Kramer et al., 2025.pdf#page=7&annotation=1727R|Kramer et al., 2025, p.7]])
> Level 1 validation focuses on verifying that the module adheres to the basic structural requirements of Synthea, including valid JSON formatting and compliance with essential module rules.
> ([[Kramer et al., 2025.pdf#page=7&annotation=1729R|Kramer et al., 2025, p.7]])
> Level 2 involves validating the module's states, transitions, and parameters against the disease profile.
> ([[Kramer et al., 2025.pdf#page=7&annotation=1731R|Kramer et al., 2025, p.7]])
> Level 3 (not implemented) validates the population, incidence, and prevalence associated with a disease process.

4. Progressive Refinement
> ([[Kramer et al., 2025.pdf#page=9&annotation=1733R|Kramer et al., 2025, p.9]])
> The fourth major stage of the process employs a feedback loop that leverages validation results to guide subsequent improvements in the Synthea module.

> ([[Kramer et al., 2025.pdf#page=10&annotation=1735R|Kramer et al., 2025, p.10]])
> to assure an objective result, the review took place in an independent session, i.e., one that does not share history with the generation step.

Beispiel: Hyperthyreose (bisher kein Synthea-Modul)


### Main Finding:

> ([[Kramer et al., 2025.pdf#page=16&annotation=1737R|Kramer et al., 2025, p.16]])
> the progressive refinement methodology proved effective at improving module quality.

> ([[Kramer et al., 2025.pdf#page=16&annotation=1739R|Kramer et al., 2025, p.16]])
> the use of curated knowledge sources significantly improves the quality of disease profiles compared to relying solely on the LLMs' internal knowledge.

> ([[Kramer et al., 2025.pdf#page=16&annotation=1741R|Kramer et al., 2025, p.16]])
> the automated review process proved reliable and consistent, particularly when using Claude as the reviewer

> ([[Kramer et al., 2025.pdf#page=15&annotation=1743R|Kramer et al., 2025, p.15]])
> The evaluations revealed that while the LLMs generated runnable modules, neither produced production-ready code.


### Limitation:

> ([[Kramer et al., 2025.pdf#page=16&annotation=1745R|Kramer et al., 2025, p.16]])
> the codes generated for diagnoses, procedures, and medications are frequently incorrect. A follow-on step to detect and replace hallucinated codes is necessary.

> ([[Kramer et al., 2025.pdf#page=16&annotation=1747R|Kramer et al., 2025, p.16]])
> The current approach treats each disease module in isolation, without considering interactions with other conditions or comorbidities.

> ([[Kramer et al., 2025.pdf#page=16&annotation=1749R|Kramer et al., 2025, p.16]])
> the process still requires significant clinical expertise, particularly in validating disease profiles and reviewing generated modules.

> ([[Kramer et al., 2025.pdf#page=16&annotation=1751R|Kramer et al., 2025, p.16]])
> The current scoring system for Level 2 does not instruct the LLM on what not to do.



### Zentrales Zitat:
> ([[Kramer et al., 2025.pdf#page=17&annotation=1753R|Kramer et al., 2025, p.17]])
> LLMs should be viewed as assistive tools rather than autonomous module creators.



---
Abgrenzung zu meiner Arbeit :

LLM erzeugt hier nicht die Patienten, sondern die Synthea-Module (Regeln), aus denen Synthea dann Patienten simuliert
- Ich generiere die FHIR-Patienten direkt mit LLM-Agenten

Generator und Reviewer sind getrennte Sessions, Feedback-Loop mit Level-1 (Struktur) und Level-2 (klinisch) Validierung
- Entspricht fast genau meiner Aufteilung Validator + Medical Review, gute Referenz für die Architektur

Halluzinierte Codes (SNOMED CT, RxNorm) als Hauptproblem
- Rechtfertigung für Terminologie-Prüfung im Validator (vgl. Terminology Search bei [[Frei et al., 2026]])
