---
Author: "[[Alex Benett]]"
Journal: "[[AMIA]]"
Title: "MIMIC-IV on FHIR: converting a decade of in-patient data into an exchangeable, interoperable format"
---

# [[Bennett et al., 2023.pdf| MIMIC-IV on FHIR: converting a decade of in-patient data into an exchangeable, interoperable format]]


### Research Gap:

> ([[Bennett et al., 2023.pdf#page=2&annotation=291R|Bennett et al., 2023, p.2]])
> However, synthetic data generated using a data-free model has limited utility in the research context as analyses can only recapitulate known clinical knowledge encoded by domain experts in the generative algorithm.

-> bezogen auf [[Walonoski et al., 2017|Synthea]] / SyntheticMass

> ([[Bennett et al., 2023.pdf#page=2&annotation=293R|Bennett et al., 2023, p.2]])
> To the best of our knowledge, however, no publicly available deidentified datasets currently exist in [[FHIR]].


### Methodik:

> ([[Bennett et al., 2023.pdf#page=2&annotation=295R|Bennett et al., 2023, p.2]])
> The objective of this work is to convert the deidentified realworld EHR database, [[MIMIC-IV]],

> ([[Bennett et al., 2023.pdf#page=2&annotation=297R|Bennett et al., 2023, p.2]])
> The conversion of MIMIC-IV into FHIR was accomplished in 4 stages: Model, Generate, Validate, and Publish.

Model:
> ([[Bennett et al., 2023.pdf#page=2&annotation=299R|Bennett et al., 2023, p.2]])
> Profiles were derived from the base FHIR R4 resources with heavy influence from US Core STU4
> ([[Bennett et al., 2023.pdf#page=3&annotation=301R|Bennett et al., 2023, p.3]])
> FHIR modeling was accomplished using the FHIR ShortHand (FSH) language.

Generate:
> ([[Bennett et al., 2023.pdf#page=3&annotation=303R|Bennett et al., 2023, p.3]])
> Conversion of MIMIC-IV data into the format stipulated by the developed FHIR profiles was then accomplished through custom Structured Query Language (SQL) scripts.

Validate:
> ([[Bennett et al., 2023.pdf#page=4&annotation=305R|Bennett et al., 2023, p.4]])
> Validation was completed using an open-source FHIR server called HAPI-FHIR.
> ([[Bennett et al., 2023.pdf#page=4&annotation=307R|Bennett et al., 2023, p.4]])
> To enable cross-resource validation, resources for an individual patient were ensembled into “bundles” and sent to the FHIR server for validation.


### Main Finding:

Ergebnis: [[MIMIC IV on FHIR]]

> ([[Bennett et al., 2023.pdf#page=4&annotation=309R|Bennett et al., 2023, p.4]])
> Overall, 25 profiles were derived from the base FHIR R4 resources.

> ([[Bennett et al., 2023.pdf#page=1&annotation=311R|Bennett et al., 2023, p.1]])
> The generated demo dataset contained 100 patients and over 915 000 resources.

> ([[Bennett et al., 2023.pdf#page=4&annotation=313R|Bennett et al., 2023, p.4]])
> The validation of the demo resources took a further 112 minutes, resulting in 1:07 minutes per patient for validation.

> ([[Bennett et al., 2023.pdf#page=5&annotation=315R|Bennett et al., 2023, p.5]])
> We found validation of FHIR profiles a powerful tool in minimizing errors in our transformation code.

> ([[Bennett et al., 2023.pdf#page=6&annotation=317R|Bennett et al., 2023, p.6]])
> We found representing MIMIC-IV as FHIR resources in a database required 7.5

-> 7.5x mehr Speicher als die relationale Struktur, im FHIR-Server sogar ~50x


### Limitation:

> ([[Bennett et al., 2023.pdf#page=6&annotation=319R|Bennett et al., 2023, p.6]])
> We did not map to US Core as this would require extensive terminology mapping for compliance with US Core specific ValueSet resources.

> ([[Bennett et al., 2023.pdf#page=6&annotation=321R|Bennett et al., 2023, p.6]])
> Terminology present in MIMIC-IV-on-FHIR is local to the source hospital and requires mapping to standard ontologies.

> ([[Bennett et al., 2023.pdf#page=6&annotation=323R|Bennett et al., 2023, p.6]])
> The status element in multiple resources was required but not found, so was imputed as a value of unknown.

> ([[Bennett et al., 2023.pdf#page=6&annotation=325R|Bennett et al., 2023, p.6]])
> we did not curate any data during our transform, and the database contains a number of biases which occur in data collected during routine clinical practice.



### Zentrales Zitat:
> ([[Bennett et al., 2023.pdf#page=4&annotation=327R|Bennett et al., 2023, p.4]])
> MIMIC-IV-on-FHIR builds on the success SyntheticMass and other synthetic datasets by providing real-world clinical data in FHIR.



---
Abgrenzung zu meiner Arbeit :

Keine Generierung, sondern Konvertierung echter Daten nach FHIR (SQL, regelbasiert)
- Liefert aber die Referenz: echte FHIR-Patienten, gegen die ich meine synthetischen FHIR-Daten vergleichen kann

Validierung über HAPI-FHIR mit Bundles pro Patient
- Direkt übertragbar auf meinen Validator (Strukturvalidierung gegen Profile)

Lokale Terminologie statt Standard-Codes (z.B. SNOMED CT, LOINC)
- Für synthetische Daten muss ich entscheiden, ob ich gegen MIMIC-Profile oder Standard-Terminologien validiere
