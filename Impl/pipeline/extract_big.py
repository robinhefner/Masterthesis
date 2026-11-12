import sys, os, time, duckdb

name = sys.argv[1]
test = len(sys.argv) > 2 and sys.argv[2] == "test"
D, P = "/srv/mimic/mimic-iv-fhir/2.1/fhir", "/srv/mimic/parquet"

REF = "STRUCT(reference VARCHAR)"
COD = "STRUCT(coding STRUCT(system VARCHAR, code VARCHAR, display VARCHAR)[])"
OBS_COLS = {"subject": REF, "encounter": REF, "code": COD, "effectiveDateTime": "VARCHAR",
            "valueQuantity": "STRUCT(value DOUBLE, unit VARCHAR)", "valueString": "VARCHAR"}
OBS_SEL = """replace(encounter.reference, 'Encounter/', '') AS {key},
  replace(subject.reference, 'Patient/', '') AS patient_id,
  code.coding[1].system AS code_system, code.coding[1].code AS code,
  code.coding[1].display AS display, effectiveDateTime AS ts,
  valueQuantity.value AS value, valueQuantity.unit AS unit, valueString AS value_str"""
LAB_COLS = {**OBS_COLS, "referenceRange":
            "STRUCT(low STRUCT(value DOUBLE), high STRUCT(value DOUBLE))[]"}
LAB_SEL = OBS_SEL.format(key="encounter_id") + """,
  referenceRange[1].low.value AS ref_low, referenceRange[1].high.value AS ref_high"""
MED_COLS = {"subject": REF, "context": REF,
            "category": "STRUCT(coding STRUCT(code VARCHAR)[])",
            "medicationCodeableConcept": COD, "effectiveDateTime": "VARCHAR",
            "effectivePeriod": 'STRUCT(start VARCHAR, "end" VARCHAR)',
            "dosage": "STRUCT(dose STRUCT(value DOUBLE, unit VARCHAR), rateQuantity STRUCT(value DOUBLE, unit VARCHAR), method STRUCT(coding STRUCT(code VARCHAR)[]))",
            "status": "VARCHAR"}
MED_SEL = """replace(context.reference, 'Encounter/', '') AS icu_encounter_id,
  replace(subject.reference, 'Patient/', '') AS patient_id,
  category.coding[1].code AS category_code,
  medicationCodeableConcept.coding[1].system AS code_system,
  medicationCodeableConcept.coding[1].code AS code,
  medicationCodeableConcept.coding[1].display AS display,
  coalesce(effectiveDateTime, effectivePeriod.start) AS ts_start,
  effectivePeriod."end" AS ts_end,
  dosage.dose.value AS dose, dosage.dose.unit AS dose_unit,
  dosage.rateQuantity.value AS rate, dosage.rateQuantity.unit AS rate_unit,
  dosage.method.coding[1].code AS method_code, status"""
ENC = "replace(encounter.reference, 'Encounter/', '')"

JOBS = {
  "chartevents":  ("MimicObservationChartevents", OBS_COLS, OBS_SEL.format(key="icu_encounter_id"), ENC, "icu"),
  "outputevents": ("MimicObservationOutputevents", OBS_COLS, OBS_SEL.format(key="icu_encounter_id"), ENC, "icu"),
  "labevents":    ("MimicObservationLabevents", LAB_COLS, LAB_SEL, ENC, "hosp"),
  "medicationicu": ("MimicMedicationAdministrationICU", MED_COLS, MED_SEL,
                    "replace(context.reference, 'Encounter/', '')", "icu"),
}
file, cols, sel, idexpr, keyset = JOBS[name]

con = duckdb.connect()
con.execute("SET memory_limit='10GB'")
con.execute("SET temp_directory='/srv/mimic/duck_tmp'")
con.execute("SET threads=2")
con.execute("SET preserve_insertion_order=false")
con.execute("SET max_temp_directory_size='50GB'")
con.execute("SET max_temp_directory_size='50GB'")
con.execute(f"CREATE TABLE icu_keys AS SELECT DISTINCT icu_encounter_id AS k FROM '{P}/cohort_stays.parquet'")
con.execute(f"CREATE TABLE hosp_keys AS SELECT DISTINCT encounter_id AS k FROM '{P}/cohort_stays.parquet'")

colspec = ", ".join(f"'{k}': '{v}'" for k, v in cols.items())
src = f"read_ndjson('/srv/mimic/filtered/{name}/*.ndjson.gz', columns={{{colspec}}})"
if test:
    src = f"(SELECT * FROM {src} LIMIT 2000000)"
out = f"{P}/{name}_cohort{'_test' if test else ''}.parquet"
t0 = time.time()
con.execute(f"""COPY (SELECT {sel} FROM {src}
                 WHERE {idexpr} IN (SELECT k FROM {keyset}_keys))
                TO '{out}.tmp' (FORMAT parquet, COMPRESSION zstd)""")
os.replace(out + ".tmp", out)
n = con.execute(f"SELECT count(*) FROM '{out}'").fetchone()[0]
print(f"{name}: {n} Zeilen, {os.path.getsize(out)/1e6:.0f} MB, {(time.time()-t0)/60:.1f} min", flush=True)
