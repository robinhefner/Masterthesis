import sys, duckdb

suffix = sys.argv[1]   # "" für die echten Dateien
cohort = sys.argv[2]   # sepsis | dka | hf
P = "/srv/mimic/parquet"
COND = {"sepsis": "is_sepsis AND NOT is_dka AND NOT is_hf_acute",
        "dka":    "is_dka AND NOT is_sepsis AND NOT is_hf_acute",
        "hf":     "is_hf_acute AND NOT is_sepsis AND NOT is_dka"}[cohort]
SRC = {"chartevents":   ("icu_encounter_id", "unit"),
       "labevents":     ("encounter_id", "unit"),
       "outputevents":  ("icu_encounter_id", "unit"),
       "medicationicu": ("icu_encounter_id", "dose_unit")}

con = duckdb.connect()
con.execute("SET memory_limit='10GB'").fetchall()
con.execute(f"CREATE VIEW stays AS SELECT * FROM '{P}/cohort_stays.parquet' WHERE {COND}").fetchall()
n = con.execute("SELECT count(*) FROM stays").fetchall()[0][0]
print(f"Kohorte {cohort}: {n} ICU-Aufenthalte (reine Kohorte)")

for name, (key, unit) in SRC.items():
    print(f"\n== {name} (Top 25 nach Anteil der Aufenthalte)")
    con.sql(f"""
      SELECT x.code, any_value(x.display) AS bezeichnung, any_value(x.{unit}) AS einheit,
             count(DISTINCT s.icu_encounter_id) AS n_stays,
             round(100.0 * count(DISTINCT s.icu_encounter_id) / {n}, 1) AS pct_stays,
             round(count(*) * 1.0 / count(DISTINCT s.icu_encounter_id), 1) AS werte_pro_stay
      FROM '{P}/{name}_cohort{suffix}.parquet' x JOIN stays s ON x.{key} = s.{key}
      GROUP BY x.code ORDER BY n_stays DESC LIMIT 25""").show(max_width=140)
