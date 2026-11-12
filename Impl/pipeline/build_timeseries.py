import sys, duckdb

H = int(sys.argv[1]) if len(sys.argv) > 1 else 72
P = "/srv/mimic/parquet"
con = duckdb.connect()
def run(sql):
    return con.execute(sql).fetchall()
def inl(codes):
    return ",".join(f"'{c}'" for c in codes)

run("SET memory_limit='12GB'")
run("SET temp_directory='/srv/mimic/duck_tmp'")
run("SET max_temp_directory_size='50GB'")
run("SET threads=4")

MAP = [
 ("chart","220045","hr",1,0), ("chart","220210","rr",1,0), ("chart","220277","spo2",1,0),
 ("chart","220052","map_inv",1,0), ("chart","220181","map_nibp",1,0),
 ("chart","223762","temp_c",1,0), ("chart","223761","temp_c",5/9,-160/9),
 ("chart","223835","fio2",1,0),
 ("chart","220621","glucose",1,0), ("chart","225664","glucose",1,0), ("lab","50931","glucose",1,0),
 ("chart","223830","ph",1,0), ("lab","50820","ph",1,0),
 ("chart","220739","gcs_e",1,0), ("chart","223900","gcs_v",1,0), ("chart","223901","gcs_m",1,0),
 ("out","226559","urine_ml",1,0), ("out","226560","urine_ml",1,0),
]
LABS = {"50813":"lactate","50912":"creatinine","51006":"bun","50971":"potassium","50983":"sodium",
        "50882":"bicarbonate","50868":"anion_gap","51301":"wbc","51265":"platelets","50885":"bilirubin",
        "51237":"inr","50818":"pco2","50821":"po2","50802":"base_excess","50963":"ntprobnp","51003":"troponin_t"}
MAP += [("lab", c, v, 1, 0) for c, v in LABS.items()]
AVG = {"hr","rr","spo2","map_inv","map_nibp","temp_c","fio2","glucose","ph"}
SUM = {"urine_ml"}
RATE = {
 "norepi_rate": (["221906"], "mcg/kg/min"), "vasopressin_rate": (["222315"], "units/hour"),
 "phenylephrine_rate": (["221749","229630"], "mcg/kg/min"), "epinephrine_rate": (["221289"], "mcg/kg/min"),
 "dopamine_rate": (["221662"], "mcg/kg/min"), "dobutamine_rate": (["221653"], "mcg/kg/min"),
 "milrinone_rate": (["221986"], "mcg/kg/min"), "insulin_rate": (["223258"], "units/hour"),
 "furosemide_rate": (["221794","228340"], "mg/hour"), "nacl_rate": (["225158"], "mL/hour"),
 "lr_rate": (["225828"], "mL/hour"),
}
BOLUS = {
 "insulin_bolus_u": (["223258","223262","223260"], "units"), "furosemide_bolus_mg": (["221794"], "mg"),
 "kcl_meq": (["225166"], "mEq"), "nacl_bolus_ml": (["225158"], "ml"), "lr_bolus_ml": (["225828"], "ml"),
}
ABX = ["225798","225893","225851","225883","225884","225855","225892"]

print("== Textwerte im Labor (nur ab 50 Vorkommen)")
for code, name in [("51003","Troponin T"),("50963","NT-proBNP"),("50885","Bilirubin gesamt"),("51237","INR")]:
    rows = run(f"""SELECT value_str, count(*) c FROM '{P}/labevents_cohort.parquet'
                   WHERE code='{code}' AND value IS NULL AND value_str IS NOT NULL
                   GROUP BY 1 HAVING count(*) >= 50 ORDER BY c DESC LIMIT 6""")
    print(f"{name}: {rows}")

run(f"""CREATE TABLE stays AS
SELECT icu_encounter_id, encounter_id, icu_start, los_h,
  CASE WHEN is_sepsis AND NOT is_dka AND NOT is_hf_acute THEN 'sepsis'
       WHEN is_dka AND NOT is_sepsis AND NOT is_hf_acute THEN 'dka'
       WHEN is_hf_acute AND NOT is_sepsis AND NOT is_dka THEN 'hf'
       ELSE 'mixed' END AS cohort
FROM '{P}/cohort_stays.parquet'""")
run(f"""CREATE TABLE grid AS
SELECT s.icu_encounter_id, s.cohort, g.h AS hour,
       s.icu_start + to_hours(g.h) AS t0, s.icu_start + to_hours(g.h + 1) AS t1
FROM stays s CROSS JOIN generate_series(0, {H-1}) AS g(h)
WHERE g.h < ceil(s.los_h)""")

run("CREATE TABLE vmap(src VARCHAR, code VARCHAR, var VARCHAR, f DOUBLE, o DOUBLE)")
run("INSERT INTO vmap VALUES " + ",".join(f"('{s}','{c}','{v}',{f},{o})" for s, c, v, f, o in MAP))
run(f"""CREATE TABLE raw AS
SELECT 'chart' AS src, x.icu_encounter_id AS k, x.code, try_cast(x.ts AS TIMESTAMPTZ) AS t, x.value AS v
FROM '{P}/chartevents_cohort.parquet' x
WHERE x.value IS NOT NULL AND x.code IN (SELECT code FROM vmap WHERE src='chart')
UNION ALL
SELECT 'out', x.icu_encounter_id, x.code, try_cast(x.ts AS TIMESTAMPTZ), x.value
FROM '{P}/outputevents_cohort.parquet' x
WHERE x.value IS NOT NULL AND x.code IN (SELECT code FROM vmap WHERE src='out')
UNION ALL
SELECT 'lab', s.icu_encounter_id, x.code, try_cast(x.ts AS TIMESTAMPTZ), x.value
FROM '{P}/labevents_cohort.parquet' x JOIN stays s ON x.encounter_id = s.encounter_id
WHERE x.value IS NOT NULL AND x.code IN (SELECT code FROM vmap WHERE src='lab')""")
run(f"""CREATE TABLE obs AS
SELECT r.k AS icu_encounter_id, floor((epoch(r.t) - epoch(s.icu_start)) / 3600)::INTEGER AS hour,
       m.var, r.v * m.f + m.o AS v, r.t
FROM raw r JOIN vmap m ON r.src = m.src AND r.code = m.code
JOIN stays s ON s.icu_encounter_id = r.k
WHERE r.t >= s.icu_start AND r.t < s.icu_start + to_hours({H})""")

OBS_VARS = list(dict.fromkeys(v for _, _, v, _, _ in MAP))
ex = []
for v in OBS_VARS:
    if v in AVG: ex.append(f"avg(v) FILTER (WHERE var='{v}') AS {v}")
    elif v in SUM: ex.append(f"sum(v) FILTER (WHERE var='{v}') AS {v}")
    else: ex.append(f"arg_max(v, t) FILTER (WHERE var='{v}') AS {v}")
run(f"CREATE TABLE obs_h AS SELECT icu_encounter_id, hour, {', '.join(ex)} FROM obs GROUP BY 1, 2")

run(f"""CREATE TABLE med AS
SELECT icu_encounter_id AS k, code, try_cast(ts_start AS TIMESTAMPTZ) AS t0, try_cast(ts_end AS TIMESTAMPTZ) AS t1,
       dose, dose_unit, rate, rate_unit FROM '{P}/medicationicu_cohort.parquet'""")
print("\n== Medikation: Anteil der Raten-Zeilen mit Endzeit (%)")
print(run("SELECT round(100.0*count(t1)/count(*),1) FROM med WHERE rate IS NOT NULL"))
print("Nitroglycerin (dose_unit, rate_unit, n):", run("SELECT dose_unit, rate_unit, count(*) FROM med WHERE code='222056' GROUP BY 1,2 ORDER BY 3 DESC"))

sel = [f"avg(m.rate) FILTER (WHERE m.code IN ({inl(c)}) AND m.rate_unit='{u}') AS {v}" for v, (c, u) in RATE.items()]
run(f"""CREATE TABLE rate_h AS
SELECT g.icu_encounter_id, g.hour, {', '.join(sel)}
FROM grid g JOIN med m ON m.k = g.icu_encounter_id AND m.rate IS NOT NULL
  AND m.t0 < g.t1 AND coalesce(m.t1, m.t0) >= g.t0
GROUP BY 1, 2""")
sel = [f"sum(m.dose) FILTER (WHERE m.rate IS NULL AND m.code IN ({inl(c)}) AND m.dose_unit='{u}') AS {v}" for v, (c, u) in BOLUS.items()]
sel.append(f"count(*) FILTER (WHERE m.code IN ({inl(ABX)})) AS abx_n")
run(f"""CREATE TABLE bolus_h AS
SELECT s.icu_encounter_id, floor((epoch(m.t0) - epoch(s.icu_start)) / 3600)::INTEGER AS hour, {', '.join(sel)}
FROM med m JOIN stays s ON s.icu_encounter_id = m.k
WHERE m.t0 >= s.icu_start AND m.t0 < s.icu_start + to_hours({H})
GROUP BY 1, 2""")

GCS = ("gcs_e", "gcs_v", "gcs_m")
so = [f"o.{v}" for v in OBS_VARS if v not in GCS]
so += ["coalesce(o.map_inv, o.map_nibp) AS map_mmhg",
       "CASE WHEN o.gcs_e IS NOT NULL AND o.gcs_v IS NOT NULL AND o.gcs_m IS NOT NULL THEN o.gcs_e + o.gcs_v + o.gcs_m END AS gcs"]
sr = [f"r.{v}" for v in RATE]
sb = [f"b.{v}" for v in BOLUS] + ["b.abx_n"]
run(f"""CREATE TABLE ts AS
SELECT g.icu_encounter_id, g.cohort, g.hour, {', '.join(so + sr + sb)}
FROM grid g
LEFT JOIN obs_h o ON o.icu_encounter_id = g.icu_encounter_id AND o.hour = g.hour
LEFT JOIN rate_h r ON r.icu_encounter_id = g.icu_encounter_id AND r.hour = g.hour
LEFT JOIN bolus_h b ON b.icu_encounter_id = g.icu_encounter_id AND b.hour = g.hour""")
run(f"COPY (SELECT * FROM ts ORDER BY icu_encounter_id, hour) TO '{P}/timeseries_h{H}.parquet' (FORMAT parquet, COMPRESSION zstd)")
print(f"\ntimeseries_h{H}.parquet geschrieben:", run("SELECT count(*), count(DISTINCT icu_encounter_id) FROM ts")[0])

STAT_VARS = [v for v in OBS_VARS if v not in GCS] + ["map_mmhg", "gcs"] + list(RATE) + list(BOLUS) + ["abx_n"]
for coh in ["sepsis", "dka", "hf"]:
    n = run(f"SELECT count(*) FROM stays WHERE cohort='{coh}'")[0][0]
    hrs = run(f"SELECT count(*) FROM ts WHERE cohort='{coh}'")[0][0]
    print(f"\n### {coh}: {n} Aufenthalte, {hrs} Stunden-Zeilen (Zellen unter 20 Werten werden ausgeblendet)")
    q = " UNION ALL ".join(
        f"""SELECT '{v}', count(DISTINCT icu_encounter_id) FILTER (WHERE {v} IS NOT NULL), count({v}),
            median({v}), quantile_cont({v}, 0.05), quantile_cont({v}, 0.95) FROM ts WHERE cohort='{coh}'""" for v in STAT_VARS)
    for var, ns, n_obs, med, p05, p95 in run(q):
        if n_obs >= 20:
            print(f"{var:<20} {100*ns/n:5.1f}% Aufenth. {n_obs:>8} Werte  med {med:9.2f}  p05 {p05:9.2f}  p95 {p95:9.2f}")

BLOCKS = [(0, 6), (6, 12), (12, 24), (24, 48), (48, H)]
KEY = {"sepsis": ["map_mmhg","hr","lactate","creatinine","norepi_rate"],
       "dka": ["glucose","potassium","bicarbonate","ph","anion_gap","insulin_rate"],
       "hf": ["creatinine","sodium","furosemide_rate","urine_ml","hr","map_mmhg"]}
for coh, vs in KEY.items():
    print(f"\n### Median je Zeitblock ({coh}), Stunden: " + " | ".join(f"{a}-{b}" for a, b in BLOCKS))
    for v in vs:
        cells = []
        for a, b in BLOCKS:
            r = run(f"SELECT median({v}), count({v}) FROM ts WHERE cohort='{coh}' AND hour >= {a} AND hour < {b}")[0]
            cells.append(f"{r[0]:8.2f}" if r[0] is not None and r[1] >= 20 else "       -")
        print(f"{v:<18}" + " | ".join(cells))

print("\n### Regelprüfung Sepsis: Vasopressor-Rate in Stunden mit MAP < 65 (True) oder >= 65 (False)")
for r in run("""SELECT map_mmhg < 65, count(*) AS stunden,
  round(100.0*avg(((coalesce(norepi_rate,0) > 0 OR coalesce(vasopressin_rate,0) > 0 OR coalesce(phenylephrine_rate,0) > 0
                    OR coalesce(epinephrine_rate,0) > 0 OR coalesce(dopamine_rate,0) > 0))::INT), 1) AS pct_vaso
  FROM ts WHERE cohort='sepsis' AND map_mmhg IS NOT NULL GROUP BY 1 ORDER BY 1"""):
    print(r)
print("\n### Regelprüfung DKA: Insulin-Infusion in Stunden mit Kalium < 3,3 (True) oder >= 3,3 (False)")
for r in run("""SELECT potassium < 3.3, count(*) AS stunden,
  round(100.0*avg((coalesce(insulin_rate,0) > 0)::INT), 1) AS pct_insulin_infusion
  FROM ts WHERE cohort='dka' AND potassium IS NOT NULL GROUP BY 1 ORDER BY 1"""):
    print(r)
