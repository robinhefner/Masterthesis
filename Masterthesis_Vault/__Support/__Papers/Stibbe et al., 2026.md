---
title: "Position: Synthetic Data Generation for Electronic Health Records Should Be Audited Like LLMs"
source: https://openreview.net/forum?id=ZajJmwVtJy
author:
  - Inigo Stibbe
  - Aldo A. Faisal
  - Padmanabhan Ramnarayan
published:
created: 2026-10-17
description: Synthetic electronic health record (EHR) generation is increasingly adopting large autoregressive models, yet privacy evaluation has not kept pace, relying heavily on similarity-based heuristics and aggregate metrics that can obscure patient-specific memorisation. We argue that these models should additionally undergo LLM-style memorisation audits at the level of individual patient records. We support this position by comparing membership-inference evaluations across four prominent autoregressive EHR generators, highlighting inconsistent evaluation practices in patient representations and attack procedures. We evaluate trajectory reconstruction from partial context and introduce randomly assigned patient-level canaries to distinguish memorised associations from clinical generalisation. We examine these methods in a GPT-2-style model deliberately overfit to 1,000 MIMIC-IV patient trajectories, creating a controlled setting in which memorisation should be readily detectable. The model systematically recovers training patients’ canaries, and their trajectory reconstruction approaches perfect accuracy with increasing context. Held-out patients show no systematic canary recovery, while reconstruction remains low and improves only marginally with additional context. These experiments establish a positive-control baseline for further evaluation of these methods in realistically trained models.
tags:
  - clippings
---
## Position: Synthetic Data Generation for Electronic Health Records Should Be Audited Like LLMs

### Inigo Stibbe1, Padmanabhan Ramnarayan, Aldo A. Faisal1 1 Imperial College London (ic.ac.uk)

NeurIPS 2026 Workshop GenAI4Health Position Paper Track Poster Everyone [Revisions](https://openreview.net/revisions?id=ZajJmwVtJy) [BibTeX](#) [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

**TL;DR:** Synthetic EHR generators should undergo LLM-style patient-level memorisation audits, supported by canary recovery and trajectory reconstruction experiments in a deliberately overfit model.

**Abstract:**

Synthetic electronic health record (EHR) generation is increasingly adopting large autoregressive models, yet privacy evaluation has not kept pace, relying heavily on similarity-based heuristics and aggregate metrics that can obscure patient-specific memorisation. We argue that these models should additionally undergo LLM-style memorisation audits at the level of individual patient records. We support this position by comparing membership-inference evaluations across four prominent autoregressive EHR generators, highlighting inconsistent evaluation practices in patient representations and attack procedures. We evaluate trajectory reconstruction from partial context and introduce randomly assigned patient-level canaries to distinguish memorised associations from clinical generalisation. We examine these methods in a GPT-2-style model deliberately overfit to 1,000 MIMIC-IV patient trajectories, creating a controlled setting in which memorisation should be readily detectable. The model systematically recovers training patients’ canaries, and their trajectory reconstruction approaches perfect accuracy with increasing context. Held-out patients show no systematic canary recovery, while reconstruction remains low and improves only marginally with additional context. These experiments establish a positive-control baseline for further evaluation of these methods in realistically trained models.

**Submission Number:** 35