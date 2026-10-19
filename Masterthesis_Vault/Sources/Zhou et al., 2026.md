---
Author: "[[Guanglin Zhou]]"
Journal: PrePrint
Title: "From Statistical Fidelity to Clinical Consistency: Scalable Generation and Auditing of Synthetic Patient Trajectories"
---

# [[Zhou et al., 2026.pdf|From Statistical Fidelity to Clinical Consistency: Scalable Generation and Auditing of Synthetic Patient Trajectories]]

### Research Gap:
> ([[Zhou et al., 2026.pdf#page=2&annotation=783R|Zhou et al., 2026, p.2]])
> statistical fidelity does not guarantee clinical consistency
> ([[Zhou et al., 2026.pdf#page=2&annotation=801R|Zhou et al., 2026, p.2]])
> Thus, synthetic datasets remain statistically plausible but clinically untrustworthy


### Methodik:


> ([[Zhou et al., 2026.pdf#page=2&annotation=765R|Zhou et al., 2026, p.2]])
> To close these gaps, we introduce Coogee, a two-step framework for generating and auditing clinically consistent synthetic patient trajectories


[[MIMIC-IV]] as a data source [[Zhou et al., 2026.pdf#page=2&annotation=768R|Zhou et al., 2026, p.2]] 

[[Qwen3-30B]]
### Main Finding:

> ([[Zhou et al., 2026.pdf#page=7&annotation=810R|Zhou et al., 2026, p.7]])
> Coogee couples knowledge-grounded generation with scalable automated auditing to resolve the tension between statistical probability and clinical validity:


### Limitation:

> ([[Zhou et al., 2026.pdf#page=7&annotation=807R|Zhou et al., 2026, p.7]])
> Coogee cohorts inherently reflect the biases and care patterns of the source training data, i.e., in this case, tertiary care from MIMIC-IV database



### Zentrales Zitat: 
> ([[Zhou et al., 2026.pdf#page=1&annotation=804R|Zhou et al., 2026, p.1]])
> Statistical fidelity is a necessary but potentially insufficient condition for creating useful synthetic clinical data. 

Gut Für die Einleitung der Thesis 



---
Abgrenzung zu meiner Arbeit : 

Zhou et al. nutzt ein einziges Qwen3-30B Modell als "Chief Medical Officer" zum Auditing
- Meine MAA kann dort ansetzen und die Aufgabe verteilen und vorrausichtlich bessere Ergebnisse erzeugen durch speziallisiertere Agenten 

Zudem wird hier mit Tabellen gearbeitet
 - Ich arbeite mit FHIR, was bei der validierung vorteile bietet

Drei Ärzte fanden in einer Stichprobe von 20 [[Synthetische Patiendendaten]] bei 45 bis 60 % Inkonsistenzen, obwohl die statistische Übereinstimmung sehr hoch war.
 - Rechtfertigung für meinen Validator und mein Medical Review
