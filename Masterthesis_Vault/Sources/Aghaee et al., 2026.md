---
Author: "[[Arman Aghaee]]"
Journal: "[[PrePrint]]"
Title: "SynthAgent: A Multi-Agent LLM Framework for Realistic Patient Simulation - A Case Study in Obesity with Mental Health Comorbidities"
---

# [[Aghaee et al., 2026.pdf |SynthAgent: A Multi-Agent LLM Framework for Realistic Patient Simulation - A Case Study in Obesity with Mental Health Comorbidities]]

### Research Gap:

> ([[Aghaee et al., 2026.pdf#page=1&annotation=324R|Aghaee et al., 2026, p.1]])
> However, our understanding of obesity patients with mental health comorbidities is constrained in practice by fragmented, sparse, and biased real-world clinical data.
> ([[Aghaee et al., 2026.pdf#page=1&annotation=327R|Aghaee et al., 2026, p.1]])
> Many cohorts under-represent severe psychiatric phenotypes or lack consistent psychological assessments; missing modalities, inconsistent coding, and data sharing restrictions further limit joint modeling of metabolic and mental health dimensions


### Methodik:
> ([[Aghaee et al., 2026.pdf#page=2&annotation=330R|Aghaee et al., 2026, p.2]])
> Integrated multiple complementary datasets in the [[Multi Agent Architektur|MAS]] framework. 

5 Agents

> ([[Aghaee et al., 2026.pdf#page=3&annotation=333R|Aghaee et al., 2026, p.3]])
> Summarizer Agent
> ([[Aghaee et al., 2026.pdf#page=3&annotation=336R|Aghaee et al., 2026, p.3]])
> Generator Agent
> ([[Aghaee et al., 2026.pdf#page=3&annotation=339R|Aghaee et al., 2026, p.3]])
> Augmenter Agent
> ([[Aghaee et al., 2026.pdf#page=4&annotation=342R|Aghaee et al., 2026, p.4]])
> Evaluator Agent
> ([[Aghaee et al., 2026.pdf#page=4&annotation=345R|Aghaee et al., 2026, p.4]])
> Refiner Agent


4 LLMs
[[GPT-5]]
[[Gemini 2.5 Pro]]
[[Claude Sonnet 4.5]]
[[DeepSeek-R1]]


> ([[Aghaee et al., 2026.pdf#page=5&annotation=360R|Aghaee et al., 2026, p.5]])
> The goal was to have high quality while the cohort is also diverse. Therefore, evaluation combined two complementary analyses: (i) Automated quality assessment, which used an LLM-as-a-Judge framework as an examiner to score based on the coherence, realism, and completeness, and (ii) Latent diversity visualization, which analyzed embedding-based variation among the simulated patients.

### Main Finding:
> ([[Aghaee et al., 2026.pdf#page=5&annotation=363R|Aghaee et al., 2026, p.5]])
> we found that GPT-5 achieved the highest mean quality score (76.27 ± 2.84), followed closely by Claude 4.5 Sonnet (76.17 ± 3.90)

> ([[Aghaee et al., 2026.pdf#page=6&annotation=366R|Aghaee et al., 2026, p.6]])
> Claude 4.5 Sonnet excelled in dimensions such as symptoms, habits, labs, and psychological scales. These findings suggest that GPT-5’s strengths lie in structural and temporal coherence, while Claude 4.5 Sonnet provides richer psychological realism.


### Limitation:

> ([[Aghaee et al., 2026.pdf#page=8&annotation=369R|Aghaee et al., 2026, p.8]])
> he current evaluation focuses on internal quality and semantic diversity rather than external clinical validation.
> ([[Aghaee et al., 2026.pdf#page=8&annotation=372R|Aghaee et al., 2026, p.8]])
> although the MAS framework enables modular coordination among agents, inter-agent reasoning and conflict resolution remain partially rule-based, limiting emergent behavioral complexity















[[Synthetische Patiendendaten]]
[[Large Language Models]]