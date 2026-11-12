import duckdb, pathlib

D = "/srv/mimic/mimic-iv-fhir/2.1/fhir"
OUT = pathlib.Path("/srv/mimic/parquet")
OUT.mkdir(parents=True, exist_ok=True)

con = duckdb.connect()
con.execute("SET memory_limit='10GB'")
con.execute("SET temp_directory='/srv/mimic/duck_tmp'")
con.execute("SET threads=4")

def tail(col):  # 'Patient/abc' -> 'abc'
    return f"regexp_extract({col}, '([^/]+)$', 1)"

def export(name, select_sql, columns):
    cols = ", ".join(f"'{k}': '{v}'" for k, v in columns.items())
    con.execute(f"""
        COPY (
          SELECT {select_sql}
          FROM read_ndjson('{D}/{name}.ndjson.gz', columns={{{cols}}})
        ) TO '{OUT}/{name}.parquet' (FORMAT parquet, COMPRESSION zstd)
    """)
    n = con.execute(f"SELECT count(*) FROM '{OUT}/{name}.parquet'").fetchone()[0]
    print(f"{name}: {n} Zeilen", flush=True)

REF = "STRUCT(reference VARCHAR)"
PER = 'STRUCT(start VARCHAR, "end" VARCHAR)'
COD = "STRUCT(system VARCHAR, code VARCHAR, display VARCHAR)[]"

export("MimicPatient",
  """id AS patient_id, gender, birthDate AS birth_date,
     deceasedDateTime AS deceased_dt, maritalStatus.coding[1].code AS marital_code""",
  {"id": "VARCHAR", "gender": "VARCHAR", "birthDate": "VARCHAR",
   "deceasedDateTime": "VARCHAR",
   "maritalStatus": "STRUCT(coding STRUCT(code VARCHAR)[])"})

export("MimicEncounter",
  f"""id AS encounter_id, {tail('subject.reference')} AS patient_id,
      period.start AS start_dt, period."end" AS end_dt,
      "class".code AS class_code,
      hospitalization.admitSource.coding[1].code AS admit_source,
      hospitalization.dischargeDisposition.coding[1].code AS discharge_disposition,
      serviceType.coding[1].code AS service_type,
      priority.coding[1].code AS priority_code,
      identifier[1].value AS identifier_value""",
  {"id": "VARCHAR", "subject": REF, "period": PER,
   "class": "STRUCT(code VARCHAR)",
   "hospitalization": "STRUCT(admitSource STRUCT(coding STRUCT(code VARCHAR)[]), dischargeDisposition STRUCT(coding STRUCT(code VARCHAR)[]))",
   "serviceType": "STRUCT(coding STRUCT(code VARCHAR)[])",
   "priority": "STRUCT(coding STRUCT(code VARCHAR)[])",
   "identifier": "STRUCT(value VARCHAR)[]"})

export("MimicEncounterICU",
  f"""id AS icu_encounter_id, {tail('partOf.reference')} AS encounter_id,
      {tail('subject.reference')} AS patient_id,
      period.start AS start_dt, period."end" AS end_dt,
      identifier[1].value AS identifier_value""",
  {"id": "VARCHAR", "subject": REF, "partOf": REF, "period": PER,
   "identifier": "STRUCT(value VARCHAR)[]"})

export("MimicCondition",
  f"""id AS condition_id, {tail('subject.reference')} AS patient_id,
      {tail('encounter.reference')} AS encounter_id,
      category[1].coding[1].code AS category_code,
      code.coding[1].system AS code_system, code.coding[1].code AS code,
      code.coding[1].display AS display, len(code.coding) AS n_coding""",
  {"id": "VARCHAR", "subject": REF, "encounter": REF,
   "category": "STRUCT(coding STRUCT(code VARCHAR)[])[]",
   "code": f"STRUCT(coding {COD})"})

export("MimicProcedureICU",
  f"""id AS procedure_id, {tail('subject.reference')} AS patient_id,
      {tail('encounter.reference')} AS encounter_id,
      category.coding[1].code AS category_code,
      code.coding[1].system AS code_system, code.coding[1].code AS code,
      code.coding[1].display AS display,
      performedPeriod.start AS start_dt, performedPeriod."end" AS end_dt""",
  {"id": "VARCHAR", "subject": REF, "encounter": REF,
   "category": "STRUCT(coding STRUCT(code VARCHAR)[])",
   "code": f"STRUCT(coding {COD})", "performedPeriod": PER})
