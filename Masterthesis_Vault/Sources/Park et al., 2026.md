---
Author: "[[Christine Park]]"
Journal: "[[PrePrint]]"
Title: "SYNTHETIC HOSPITAL: AN OPEN, VERIFIABLE, PHYSICIAN-VALIDATED LONGITUDINAL EHR BENCHMARK"
---

# [[Park et al.,2026.pdf|SYNTHETIC HOSPITAL: AN OPEN, VERIFIABLE, PHYSICIAN-VALIDATED LONGITUDINAL EHR BENCHMARK]]

### Research Gap:

> ([[Park et al.,2026.pdf#page=1&annotation=871R|Park et al., 2026, p.1]])
> Frontier language models are rarely used in clinical workflows because the realistic, longitudinal benchmarks needed to develop them are scarce.

> ([[Park et al.,2026.pdf#page=1&annotation=873R|Park et al., 2026, p.1]])
> Real electronic health record (EHR) data cannot be openly shared due to privacy, ethics or data use issues and it does not contain verifiable ground truth since the chart records only reflect what clinicians documented.

> ([[Park et al.,2026.pdf#page=1&annotation=875R|Park et al., 2026, p.1]])
> However, using real EHR data as a starting point for a benchmark fails in two ways: it cannot be shared openly and it cannot consistently supply verifiable ground truth.

Bisherige [[Synthetische Patiendendaten]]:
> ([[Park et al.,2026.pdf#page=4&annotation=877R|Park et al., 2026, p.4]])
> Rule-based simulators such as Synthea (Walonoski et al., 2018) produce standards-compliant FHIR records but structured codes rather than narratives
> ([[Park et al.,2026.pdf#page=4&annotation=879R|Park et al., 2026, p.4]])
> LLM-generated records such as SimSUM (Rabaey et al., 2024) produce fluent narratives without a provenance chain linking statements to underlying clinical facts.

-> vgl. [[Walonoski et al., 2017]]


### Methodik:

> ([[Park et al.,2026.pdf#page=4&annotation=881R|Park et al., 2026, p.4]])
> We introduce Synthetic Hospital, a deterministic five-stage pipeline that transforms publicly available medical educational resources into a longitudinal EHR benchmark with ontology-grounded provenance.

> ([[Park et al.,2026.pdf#page=4&annotation=883R|Park et al., 2026, p.4]])
> the pipeline first constructs a structured medical knowledge graph from source material and then renders that graph into realistic clinical documentation.

5 Stages:
1. Knowledge Ingestion [[Park et al.,2026.pdf#page=4&annotation=885R|Park et al., 2026, p.4]]
2. Ontology Grounding + Knowledge Graph [[Park et al.,2026.pdf#page=4&annotation=887R|Park et al., 2026, p.4]]
> ([[Park et al.,2026.pdf#page=4&annotation=889R|Park et al., 2026, p.4]])
> We then ground these concepts deterministically to ICD-10-CM, SNOMED CT, and LOINC; the LLM-proposed codes are treated only as candidates.
3. Longitudinal Patient Generation [[Park et al.,2026.pdf#page=4&annotation=891R|Park et al., 2026, p.4]]
> ([[Park et al.,2026.pdf#page=5&annotation=893R|Park et al., 2026, p.5]])
> Thus, narrative generation occurs only after the patient state is fixed and does not determine benchmark ground truth.
4. Benchmark Construction
5. Domain-faithful Simulation
> ([[Park et al.,2026.pdf#page=5&annotation=895R|Park et al., 2026, p.5]])
> The completed records are served through a production-style clinical environment implementing [[FHIR]] R4 resources, role-based access control, Epic-style workflows, and a function-calling agent interface.

Model (Generierung): [[Kimi 2.5]] [[Park et al.,2026.pdf#page=4&annotation=887R|Park et al., 2026, p.4]]

> ([[Park et al.,2026.pdf#page=1&annotation=897R|Park et al., 2026, p.1]])
> it comprises 1,268 longitudinal patients and 5,602 encounters

Realismus-Test (Turing-Test mit Ärzten gegen [[MIMIC-IV]]):
> ([[Park et al.,2026.pdf#page=6&annotation=899R|Park et al., 2026, p.6]])
> licensed physicians reviewed synthetic and real patient records presented through our Epic-like interface and labeled each chart as synthetic or real


### Main Finding:

> ([[Park et al.,2026.pdf#page=7&annotation=901R|Park et al., 2026, p.7]])
> Across 100 judgments, physicians identified whether a record was real or synthetic with 53% accuracy, which did not differ from chance

> ([[Park et al.,2026.pdf#page=7&annotation=903R|Park et al., 2026, p.7]])
> The graph recovered 111 of the 119 relationships (93%)

> ([[Park et al.,2026.pdf#page=8&annotation=905R|Park et al., 2026, p.8]])
> First, no model approaches ceiling performance on any task, indicating that the benchmark meaningfully separates systems and that current frontier models remain unreliable on these clinical tasks.

> ([[Park et al.,2026.pdf#page=14&annotation=907R|Park et al., 2026, p.14]])
> Instead, the dominant failure mode is omission.

> ([[Park et al.,2026.pdf#page=9&annotation=909R|Park et al., 2026, p.9]])
> Multi-turn agency does not improve on single-turn inference when the relevant chart context is available upfront.


### Limitation:

> ([[Park et al.,2026.pdf#page=9&annotation=911R|Park et al., 2026, p.9]])
> Our physician study evaluates record-level realism in a small sample, not population-level fidelity, and the education-derived case mix may under-represent rare or atypical presentations

> ([[Park et al.,2026.pdf#page=9&annotation=913R|Park et al., 2026, p.9]])
> The benchmark also does not explicitly simulate missingness, contradictions, or documentation errors.

> ([[Park et al.,2026.pdf#page=9&annotation=915R|Park et al., 2026, p.9]])
> Our agentic evaluation is limited to three models, three conditions, 100 patients, and one scaffold

> ([[Park et al.,2026.pdf#page=25&annotation=917R|Park et al., 2026, p.25]])
> it is designed for zero-/few-shot evaluation of clinical AI systems, not as a synthetic replacement for population-calibrated EHR data for model training or epidemiologic inference.



### Zentrales Zitat:
> ([[Park et al.,2026.pdf#page=2&annotation=919R|Park et al., 2026, p.2]])
> Of note, the record shown to a model still reads like a chart; it is the ground truth behind the record, not the record itself, that is complete.



---
Abgrenzung zu meiner Arbeit :

Ground Truth wird zuerst deterministisch als Knowledge Graph festgelegt, das LLM schreibt nur die Narrative
- Gute Idee für meine Arbeit: klinischen Zustand erst strukturiert festlegen, dann generieren lassen -> Validator kann gegen diesen Zustand prüfen

LLM-Codes werden nur als Kandidaten behandelt und deterministisch gegen Ontologien geprüft
- Gleiche Problematik wie halluzinierte Codes bei [[Kramer et al., 2025]], Rechtfertigung für Terminologie-Prüfung im Validator

Realismus-Test mit Ärzten (53 %, Zufallsniveau) als Evaluationsdesign
- Übernehmbar für mein Medical Review / meine Evaluation

Ziel ist ein Benchmark für klinische KI, nicht die Generierung von FHIR-Daten an sich; FHIR dient nur als Zugriffsschicht
