import duckdb
con = duckdb.connect()
con.execute("CREATE VIEW ts AS SELECT * FROM '/srv/mimic/parquet/timeseries_h72.parquet'").fetchall()

print("== Sepsis: Beginn eines Vasopressors in Stunde t, nach MAP-Stand der 2 Stunden davor (nur Stunden ohne Vasopressor in t-1)")
for r in con.execute("""
WITH a AS (
  SELECT icu_encounter_id, hour, map_mmhg,
    (coalesce(norepi_rate,0)>0 OR coalesce(vasopressin_rate,0)>0 OR coalesce(phenylephrine_rate,0)>0
     OR coalesce(epinephrine_rate,0)>0 OR coalesce(dopamine_rate,0)>0) AS vaso
  FROM ts WHERE cohort='sepsis'),
b AS (
  SELECT *, lag(vaso) OVER w AS vaso_prev,
    last_value(map_mmhg IGNORE NULLS) OVER (PARTITION BY icu_encounter_id ORDER BY hour
        ROWS BETWEEN 2 PRECEDING AND 1 PRECEDING) AS map_prev
  FROM a WINDOW w AS (PARTITION BY icu_encounter_id ORDER BY hour))
SELECT map_prev < 65 AS map_prev_unter_65, count(*) AS stunden, round(100.0*avg(vaso::INT),2) AS pct_beginn
FROM b WHERE vaso_prev = false AND map_prev IS NOT NULL GROUP BY 1 ORDER BY 1""").fetchall():
    print(r)

print("\n== DKA: Ende der Insulin-Infusion in Stunde t, nach Kalium der letzten 6 Stunden (nur Stunden mit Infusion in t-1)")
for r in con.execute("""
WITH a AS (
  SELECT icu_encounter_id, hour, potassium, (coalesce(insulin_rate,0)>0) AS ins
  FROM ts WHERE cohort='dka'),
b AS (
  SELECT *, lag(ins) OVER w AS ins_prev,
    last_value(potassium IGNORE NULLS) OVER (PARTITION BY icu_encounter_id ORDER BY hour
        ROWS BETWEEN 6 PRECEDING AND 1 PRECEDING) AS k_prev
  FROM a WINDOW w AS (PARTITION BY icu_encounter_id ORDER BY hour))
SELECT k_prev < 3.3 AS k_prev_unter_3_3, count(*) AS stunden, round(100.0*avg((NOT ins)::INT),2) AS pct_stopp
FROM b WHERE ins_prev = true AND k_prev IS NOT NULL GROUP BY 1 ORDER BY 1""").fetchall():
    print(r)
