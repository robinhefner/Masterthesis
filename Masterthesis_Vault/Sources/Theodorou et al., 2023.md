---
Author: "[[Brandon Theodorou]]"
Journal: "[[Nature Communications]]"
Title: |-
  Synthesize high-dimensional longitudinal electronic health records via hierarchical
  autoregressive language model
---

# [[Theodorou et al., 2023.pdf|Synthesize high-dimensional longitudinal electronic health records via hierarchical autoregressive language model]]


### Research Gap:
> ([[Theodorou et al., 2023.pdf#page=1&annotation=670R|Theodorou et al., 2023, p.1]])
> To date, existing methods cannot generate realistic [[Synthetische Patiendendaten|EHR]] data in its original, high-dimensional form. The high dimensionality of EHR data, along with rare and sparse variables and complex relationships among variables, makes the generation task a difficult one.


### Methodik:

> ([[Theodorou et al., 2023.pdf#page=10&annotation=673R|Theodorou et al., 2023, p.10]])
> We model the probability of patient record R, P(R), via a hierarchical autoregressive model, which utilizes both visit- and code-level structures of a patient record. 

Datasets: 
> ([[Theodorou et al., 2023.pdf#page=3&annotation=676R|Theodorou et al., 2023, p.3]])
> The outpatient EHR is from a large real-world US claims data.
> ([[Theodorou et al., 2023.pdf#page=4&annotation=679R|Theodorou et al., 2023, p.4]])
> The inpatient EHR is from the [[MIMIC-IV|MIMIC-III]] ICU stay dataset


> ([[Theodorou et al., 2023.pdf#page=4&annotation=682R|Theodorou et al., 2023, p.4]])
> Experiment setup.

### Main Finding:


![[Theodorou et al.,2023  Fig. 3.png]]
> ([[Theodorou et al., 2023.pdf#page=6&annotation=694R|Theodorou et al., 2023, p.6]])
> Fig. 3 | Code probability plots.


![[Theodorou et al.,2023  Table 4.png]]
> ([[Theodorou et al., 2023.pdf#page=7&annotation=697R|Theodorou et al., 2023, p.7]])
> Table 4 | Chronic disease classification model performance trained on synthetic data



![[Theodorou et al.,2023  Table 5.png]]
> ([[Theodorou et al., 2023.pdf#page=7&annotation=700R|Theodorou et al., 2023, p.7]])
> Table 5 | Rare disease detection performance on synthetic balanced datasets

### Limitation:

> ([[Theodorou et al., 2023.pdf#page=9&annotation=685R|Theodorou et al., 2023, p.9]])
> First, the architecture is designed in the model of a large language model. 
> ([[Theodorou et al., 2023.pdf#page=9&annotation=688R|Theodorou et al., 2023, p.9]])
> Another important aspect of our model is that it generates synthetic records through a probabilistic process.
> ([[Theodorou et al., 2023.pdf#page=9&annotation=691R|Theodorou et al., 2023, p.9]])
> Finally, our HALO model focuses on generating longitudinal EHR data, such as medical codes and lab results.
