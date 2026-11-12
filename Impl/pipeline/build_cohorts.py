import duckdb

con = duckdb.connect()
con.execute("SET memory_limit='10GB'")
P = "/srv/mimic/parquet"
q = lambda s: con.sql(s).show()

con.execute(f"""
CREATE TABLE flags AS
SELECT encounter_id,
  bool_or(code LIKE '2501%' OR code LIKE 'E101%' OR code LIKE 'E111%' OR code LIKE 'E131%') AS is_dka,
  bool_or(code IN ('42821','42823','42831','42833','42841','42843',
                   'I5021','I5023','I5031','I5033','I5041','I5043')) AS is_hf_acute,
  bool_or(code LIKE '038%' OR code IN ('99591','99592','78552')
          OR code LIKE 'A40%' OR code LIKE 'A41%' OR code LIKE 'R652%') AS is_sepsis
FROM '{P}/MimicCondition.parquet' GROUP BY encounter_id""")

con.execute(f"""
CREATE TABLE stays AS
SELECT i.icu_encounter_id, i.encounter_id, i.patient_id, p.gender,
  try_cast(i.start_dt AS TIMESTAMPTZ) AS icu_start,
  try_cast(i.end_dt AS TIMESTAMPTZ)   AS icu_end,
  (epoch(try_cast(i.end_dt AS TIMESTAMPTZ)) - epoch(try_cast(i.start_dt AS TIMESTAMPTZ))) / 3600.0 AS los_h,
  year(try_cast(i.start_dt AS TIMESTAMPTZ)) - year(try_cast(p.birth_date AS DATE)) AS age_approx,
  count(*) OVER (PARTITION BY i.encounter_id) AS n_icu_in_hosp,
  coalesce(f.is_dka, false)      AS is_dka,
  coalesce(f.is_hf_acute, false) AS is_hf_acute,
  coalesce(f.is_sepsis, false)   AS is_sepsis
FROM '{P}/MimicEncounterICU.parquet' i
JOIN '{P}/MimicPatient.parquet' p ON i.patient_id = p.patient_id
LEFT JOIN flags f ON i.encounter_id = f.encounter_id""")

print("== Datenqualität ==")
q("SELECT count(*) AS icu_gesamt, count(los_h) AS los_lesbar, count(age_approx) AS alter_lesbar FROM stays")

print("== Trichter je Kohorte ==")
for flag in ["is_dka", "is_hf_acute", "is_sepsis"]:
    q(f"""SELECT '{flag}' AS kohorte,
      count(*) FILTER (WHERE {flag}) AS mit_code,
      count(*) FILTER (WHERE {flag} AND age_approx >= 18) AS erwachsen,
      count(*) FILTER (WHERE {flag} AND age_approx >= 18 AND los_h >= 24) AS los_24h,
      count(*) FILTER (WHERE {flag} AND age_approx >= 18 AND los_h >= 24 AND n_icu_in_hosp = 1) AS ein_icu
    FROM stays""")

print("== Überschneidung der Kohorten (nach allen Kriterien) ==")
q("""SELECT is_dka, is_hf_acute, is_sepsis, count(*) AS n FROM stays
     WHERE age_approx >= 18 AND los_h >= 24 AND n_icu_in_hosp = 1
     GROUP BY ALL ORDER BY n DESC""")

print("== ICU-Dauer in Stunden (10/50/90 Prozent) ==")
for flag in ["is_dka", "is_hf_acute", "is_sepsis"]:
    q(f"""SELECT '{flag}' AS kohorte, count(*) AS n,
      round(quantile_cont(los_h, 0.1), 1) AS p10,
      round(quantile_cont(los_h, 0.5), 1) AS p50,
      round(quantile_cont(los_h, 0.9), 1) AS p90
    FROM stays WHERE {flag} AND age_approx >= 18 AND los_h >= 24 AND n_icu_in_hosp = 1""")

con.execute(f"""COPY (SELECT * FROM stays
  WHERE (is_dka OR is_hf_acute OR is_sepsis)
    AND age_approx >= 18 AND los_h >= 24 AND n_icu_in_hosp = 1)
  TO '{P}/cohort_stays.parquet' (FORMAT parquet, COMPRESSION zstd)""")
print("cohort_stays.parquet geschrieben")
