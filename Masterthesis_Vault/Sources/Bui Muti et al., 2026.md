---
Author: "[[Valentina Bui Muti]]"
Journal: "[[AMIA]]"
Title: "MedCase-Structured: A Text-to-FHIR Dataset for Benchmarking Diagnostic Reasoning in Clinically Realistic EHR Settings"
---

# [[Bui Muti et al., 2026.pdf|MedCase-Structured: A Text-to-FHIR Dataset for Benchmarking Diagnostic Reasoning in Clinically Realistic EHR Settings]]

### Research Gap:
> ([[Bui Muti et al., 2026.pdf#page=2&annotation=689R|Bui Muti et al., 2026, p.2]])
> existing approaches do not provide flexible and controllable methods for generating terminology-grounded, [[FHIR]] formatted patient cases that can systematically evaluate model reasoning under diverse and challenging conditions.

### Methodik:

> ([[Bui Muti et al., 2026.pdf#page=3&annotation=692R|Bui Muti et al., 2026, p.3]])
> We address these issues with a multi-stage [[Synthetische Patiendendaten|synthetic]] patient generator

3 models 
[[GPT-5.4-mini]] [[Bui Muti et al., 2026.pdf#page=3&annotation=695R|Bui Muti et al., 2026, p.3]]
[[Gemini 3.5 Flash]] [[Bui Muti et al., 2026.pdf#page=3&annotation=698R|Bui Muti et al., 2026, p.3]]
[[Claude Sonnet 4.5]] [[Bui Muti et al., 2026.pdf#page=3&annotation=701R|Bui Muti et al., 2026, p.3]]

> ([[Bui Muti et al., 2026.pdf#page=4&annotation=709R|Bui Muti et al., 2026, p.4]])
> MedCase-Structured, a synthetic, case-report-derived [[FHIR]] dataset for structured diagnostic reasoning.

### Main Finding:
> ([[Bui Muti et al., 2026.pdf#page=5&annotation=715R|Bui Muti et al., 2026, p.5]])
> Our results show that [[LLM]]s achieve consistently lower diagnostic accuracy when operating over structured FHIR inputs compared to plain text descriptions.

### Limitation:

> ([[Bui Muti et al., 2026.pdf#page=5&annotation=712R|Bui Muti et al., 2026, p.5]])
> It currently supports a limited subset of FHIR resources and represents temporal information through repeated, date-aware resources rather than full longitudinal patient trajectories. 
