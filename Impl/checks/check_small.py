import duckdb

con = duckdb.connect()
P = "/srv/mimic/parquet"
q = lambda s: con.sql(s).show()

q(f"""SELECT code_system, n_coding, count(*) AS n
      FROM '{P}/MimicCondition.parquet' GROUP BY ALL ORDER BY n DESC LIMIT 20""")
q(f"""SELECT length(start_dt) AS laenge_start, count(*) AS n
      FROM '{P}/MimicEncounter.parquet' GROUP BY 1""")
q(f"""SELECT count(*) AS encounters, count(p.patient_id) AS mit_patient
      FROM '{P}/MimicEncounter.parquet' e
      LEFT JOIN '{P}/MimicPatient.parquet' p ON e.patient_id = p.patient_id""")
q(f"""SELECT count(*) AS icu, count(e.encounter_id) AS mit_krankenhausaufenthalt
      FROM '{P}/MimicEncounterICU.parquet' i
      LEFT JOIN '{P}/MimicEncounter.parquet' e ON i.encounter_id = e.encounter_id""")
q(f"""SELECT count(*) AS conditions, count(e.encounter_id) AS mit_encounter
      FROM '{P}/MimicCondition.parquet' c
      LEFT JOIN '{P}/MimicEncounter.parquet' e ON c.encounter_id = e.encounter_id""")
