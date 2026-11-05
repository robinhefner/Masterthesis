---
Author: "[[Yijie Hao]]"
Journal: "[[PMLR]]"
Title: "LLMSYN: Generating Synthetic Electronic Health Records Without Patient-Level Data"
---

# [[Hao et al., 2024.pdf |LLMSYN: Generating Synthetic Electronic Health Records Without Patient-Level Data]]

### Research Gap:

> ([[Hao et al., 2024.pdf#page=1&annotation=710R|Hao et al., 2024, p.1]])
> Although feeding real-world data to [[Large Language Models|LLMs]] can potentially mitigate this issue, it also raises privacy concerns as this transmits patients’ information to the LLM API.

> ([[Hao et al., 2024.pdf#page=2&annotation=712R|Hao et al., 2024, p.2]])
> Yet these architectures require real EHRs, which can be challenging to obtain access or may generate skewed results when the training sample is small.

-> gemeint sind [[GAN]]s, Autoencoder ([[VAE]]) und Diffusion Models

> ([[Hao et al., 2024.pdf#page=2&annotation=714R|Hao et al., 2024, p.2]])
> Unfortunately, the data has limited utility, especially for modeling health outcomes and other discriminative tasks

-> bezogen auf [[Walonoski et al., 2017|Synthea]]

> ([[Hao et al., 2024.pdf#page=2&annotation=716R|Hao et al., 2024, p.2]])
> the question is whether LLMs can generate [[Synthetische Patiendendaten|synthetic EHRs]] without requiring access to patient records.


### Methodik:

> ([[Hao et al., 2024.pdf#page=1&annotation=718R|Hao et al., 2024, p.1]])
> Our pipeline utilizes only high-level statistical information from datasets and publicly available medical knowledge.

4 Components (inspiriert von CoT, RAG und ICL):
> ([[Hao et al., 2024.pdf#page=4&annotation=720R|Hao et al., 2024, p.4]])
> Markov-based Generation Process: Rather than using a single prompt
> ([[Hao et al., 2024.pdf#page=4&annotation=722R|Hao et al., 2024, p.4]])
> Prior Knowledge Retrieval: We leverage prior statistical knowledge
> ([[Hao et al., 2024.pdf#page=5&annotation=724R|Hao et al., 2024, p.5]])
> Relevant Knowledge Retrieval: Given an intermediate generated response
> ([[Hao et al., 2024.pdf#page=5&annotation=726R|Hao et al., 2024, p.5]])
> Prompt Adaptor: We propose a prompt adapter

4 Schritte: Demographics -> Main Diagnosis (ICD-9) -> Complications -> Procedures (CPT)

> ([[Hao et al., 2024.pdf#page=6&annotation=728R|Hao et al., 2024, p.6]])
> we extracted information based on two key aspects: the distribution of diagnosed diseases and mortality rates.

> ([[Hao et al., 2024.pdf#page=7&annotation=730R|Hao et al., 2024, p.7]])
> In our experiments, we use Mayo Clinic as our Relevant Knowledge Source

Dataset: [[MIMIC-IV|MIMIC-III]] [[Hao et al., 2024.pdf#page=9&annotation=732R|Hao et al., 2024, p.9]]

Models: [[LLaMA2-70B]], [[GPT-3.5]] [[Hao et al., 2024.pdf#page=9&annotation=734R|Hao et al., 2024, p.9]]

Baseline: [[Walonoski et al., 2017|Synthea]]
> ([[Hao et al., 2024.pdf#page=10&annotation=736R|Hao et al., 2024, p.10]])
> we focus on Synthea, a purely inference-based model designed to generate synthetic EHR datasets using pre-defined modules tailored for each disease.

> ([[Hao et al., 2024.pdf#page=10&annotation=738R|Hao et al., 2024, p.10]])
> We evaluate the effectiveness of LLM-generated synthetic EHR records along the following 3 dimensions: utility, fidelity, and privacy.


### Main Finding:

> ([[Hao et al., 2024.pdf#page=14&annotation=740R|Hao et al., 2024, p.14]])
> Our findings showed that directly employing LLMs yielded unsatisfactory generation.

> ([[Hao et al., 2024.pdf#page=14&annotation=742R|Hao et al., 2024, p.14]])
> when LLMs are injected with high-level statistical information and external medical knowledge, the generated EHRs closely resemble real data and exhibit high utility in downstream tasks, while presenting minimal privacy risks.

> ([[Hao et al., 2024.pdf#page=12&annotation=744R|Hao et al., 2024, p.12]])
> data augmentation using synthetic data outperforms models using only real data in both base models

> ([[Hao et al., 2024.pdf#page=12&annotation=746R|Hao et al., 2024, p.12]])
> Although training directly on a purely synthetic dataset (FS) reveals discrepancies in AUROC

-> rein synthetisch (FS) liegt die AUROC bei ca. 0.5, Nutzen also v.a. als Data Augmentation

> ([[Hao et al., 2024.pdf#page=14&annotation=748R|Hao et al., 2024, p.14]])
> compared to Synthea, the results from LLMSYN show a distribution more similar to that of MIMIC-III.


### Limitation:

> ([[Hao et al., 2024.pdf#page=14&annotation=750R|Hao et al., 2024, p.14]])
> we focus on structured codes and did not consider both unstructured (i.e., clinical notes) and temporal EHR data (e.g., vital signs).

> ([[Hao et al., 2024.pdf#page=9&annotation=752R|Hao et al., 2024, p.9]])
> smaller LLMs (for instance, LLaMA2-7B, Falcon-7B) struggle significantly with executing our pipeline.

> ([[Hao et al., 2024.pdf#page=13&annotation=754R|Hao et al., 2024, p.13]])
> yet it introduces a bias towards certain feature groups compared to

-> mehr Wissen (Mayo Clinic) verbessert Fidelity/Utility, verschlechtert aber k-Anonymity



### Zentrales Zitat:
> ([[Hao et al., 2024.pdf#page=2&annotation=756R|Hao et al., 2024, p.2]])
> The quality of the generated synthetic records does not rely on the quality of the underlying EHR data but instead on the capability of the LLM model.



---
Abgrenzung zu meiner Arbeit :

LLMSYN ist eine sequenzielle Pipeline mit einem einzigen LLM (4 Markov-Schritte), keine echten Agenten
- Meine MAA kann die Schritte auf spezialisierte Agenten verteilen

Output ist tabellarisch (ICD-9 / CPT im MIMIC-III-Schema)
- Ich arbeite mit [[FHIR]]

Evaluation nur statistisch (KS, MMD, k-Anonymity), keine Prüfung der klinischen Konsistenz
- Rechtfertigung für meinen Validator und mein Medical Review (vgl. [[Zhou et al., 2026]])

Idee übernehmbar: Prior Knowledge (Verteilungen aus echten Daten) + RAG (Mayo Clinic) zur Steuerung der Generierung, ohne Patientendaten an die API zu geben
