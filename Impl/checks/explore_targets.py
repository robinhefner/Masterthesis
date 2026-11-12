import sys, duckdb

cohort = sys.argv[1]   # sepsis | dka | hf
P = "/srv/mimic/parquet"
COND = {"sepsis": "is_sepsis AND NOT is_dka AND NOT is_hf_acute",
        "dka":    "is_dka AND NOT is_sepsis AND NOT is_hf_acute",
        "hf":     "is_hf_acute AND NOT is_sepsis AND NOT is_dka"}[cohort]

SRC = {
 "chartevents": ("icu_encounter_id", "unit",
    "heart rate|respiratory rate|o2 sat|temperature|blood pressure|gcs|inspired o2|fio2|glucose|weight|ph$|ph |pco2|po2|lactate|ketone"),
 "labevents": ("encounter_id", "unit",
    "lactate|^ph$|pco2|po2|base excess|bicarbonate|potassium|sodium|creatinine|glucose|anion gap|ketone|hydroxybut|white blood|wbc|platelet|bilirubin|inr|bnp|troponin|urea nitrogen|calcium|magnesium|osmol"),
 "medicationicu": ("icu_encounter_id", "dose_unit",
    "norepinephrine|epinephrine|vasopressin|phenylephrine|dopamine|dobutamine|milrinone|insulin|furosemide|bumetanide|torsemide|nacl|^lr$|lactated|dextrose|potassium chloride|bicarb|hydrocortisone|vancomycin|piperacillin|meropenem|cefepime|ceftriaxone|metronidazole|heparin|amiodarone|nitroglycerin|propofol|midazolam"),
 "outputevents": ("icu_encounter_id", "unit", "foley|void|urine|nephrostomy|stool|chest tube"),
}

con = duckdb.connect()
con.execute("SET memory_limit='10GB'").fetchall()
con.execute(f"CREATE VIEW stays AS SELECT * FROM '{P}/cohort_stays.parquet' WHERE {COND}").fetchall()
n = con.execute("SELECT count(*) FROM stays").fetchall()[0][0]
r = con.execute("""SELECT round(quantile_cont(los_h,0.1),0), round(quantile_cont(los_h,0.5),0),
                          round(quantile_cont(los_h,0.9),0), round(quantile_cont(age_approx,0.5),0),
                          round(100.0*avg((lower(gender)='female')::int),0) FROM stays""").fetchall()[0]
print(f"Kohorte {cohort}: {n} ICU-Aufenthalte")
print(f"ICU-Dauer in h (P10/P50/P90): {r[0]:.0f} / {r[1]:.0f} / {r[2]:.0f};  Alter (Median, nur ungefähr): {r[3]:.0f};  Anteil F: {r[4]:.0f} %")

for name, (key, unit, rx) in SRC.items():
    print(f"\n== {name}   (Code, Bezeichnung, Einheit, % der Aufenthalte, Werte pro Aufenthalt)")
    rows = con.execute(f"""
      SELECT x.code, any_value(x.display), any_value(x.{unit}),
             count(DISTINCT s.icu_encounter_id), count(*) * 1.0 / count(DISTINCT s.icu_encounter_id)
      FROM '{P}/{name}_cohort.parquet' x JOIN stays s ON x.{key} = s.{key}
      WHERE regexp_matches(x.display, '(?i){rx}') AND NOT regexp_matches(x.display, '(?i)alarm')
      GROUP BY x.code HAVING count(DISTINCT s.icu_encounter_id) >= {0.03 * n}
      ORDER BY 2, 4 DESC""").fetchall()
    for c, d, u, k, per in rows:
        print(f"{c:>8}  {str(d)[:42]:<42} {str(u or '-'):<9} {100*k/n:5.1f}%  {per:7.1f}")
    print(f"({len(rows)} Zeilen)")
