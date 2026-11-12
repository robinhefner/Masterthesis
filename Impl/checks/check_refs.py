import duckdb

con = duckdb.connect()
P, T = "/srv/mimic/parquet", "/srv/mimic/duck_tmp"
con.execute(f"CREATE VIEW hosp AS SELECT encounter_id FROM '{P}/MimicEncounter.parquet'")
con.execute(f"CREATE VIEW icu AS SELECT icu_encounter_id FROM '{P}/MimicEncounterICU.parquet'")

tests = {"MimicObservationChartevents": "encounter", "MimicObservationLabevents": "encounter",
         "MimicObservationOutputevents": "encounter", "MimicProcedureICU": "encounter",
         "MimicMedicationAdministrationICU": "context"}
for name, key in tests.items():
    con.sql(f"""
      WITH s AS (
        SELECT regexp_extract({key}.reference, '^([^/]+)/', 1) AS typ,
               regexp_extract({key}.reference, '([^/]+)$', 1)  AS ref
        FROM read_ndjson('{T}/sample_{name}.ndjson',
             columns={{'{key}': 'STRUCT(reference VARCHAR)'}}))
      SELECT '{name}' AS datei, typ, count(*) AS n,
        count(*) FILTER (WHERE ref IN (SELECT encounter_id FROM hosp))     AS passt_krankenhaus,
        count(*) FILTER (WHERE ref IN (SELECT icu_encounter_id FROM icu))  AS passt_icu
      FROM s GROUP BY ALL""").show()
