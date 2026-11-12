import duckdb

P = "/srv/mimic/parquet"
con = duckdb.connect()
con.execute(f"CREATE VIEW ts AS SELECT * FROM '{P}/timeseries_h72.parquet'").fetchall()
con.execute(f"CREATE VIEW st AS SELECT * FROM '{P}/cohort_stays.parquet'").fetchall()

VARS = {
 "hr": "Herzfrequenz (1/min)", "rr": "Atemfrequenz (1/min)", "spo2": "SpO2 (%)", "map_mmhg": "MAP (mmHg)",
 "temp_c": "Temperatur (°C)", "gcs": "GCS (3-15)", "fio2": "FiO2 (%)", "glucose": "Glukose (mg/dL)",
 "ph": "pH", "pco2": "pCO2 (mmHg)", "po2": "pO2 (mmHg)", "base_excess": "Base Excess (mEq/L)",
 "lactate": "Laktat (mmol/L)", "creatinine": "Kreatinin (mg/dL)", "bun": "Harnstoff-N (mg/dL)",
 "potassium": "Kalium (mEq/L)", "sodium": "Natrium (mEq/L)", "bicarbonate": "Bikarbonat (mEq/L)",
 "anion_gap": "Anion Gap (mEq/L)", "wbc": "Leukozyten (K/uL)", "platelets": "Thrombozyten (K/uL)",
 "bilirubin": "Bilirubin gesamt (mg/dL)", "inr": "INR", "urine_ml": "Urin (ml/h)",
}
THER = {
 "norepi_rate": "Noradrenalin (µg/kg/min)", "vasopressin_rate": "Vasopressin (E/h)",
 "phenylephrine_rate": "Phenylephrin (µg/kg/min)", "insulin_rate": "Insulin-Infusion (E/h)",
 "furosemide_rate": "Furosemid-Infusion (mg/h)", "nacl_rate": "NaCl 0,9 % (ml/h)", "lr_rate": "Ringer-Laktat (ml/h)",
 "dobutamine_rate": "Dobutamin (µg/kg/min)", "milrinone_rate": "Milrinon (µg/kg/min)",
}
BOL = {"insulin_bolus_u": "Insulin-Einzelgabe (E)", "furosemide_bolus_mg": "Furosemid-Bolus (mg)",
       "kcl_meq": "KCl (mEq)", "nacl_bolus_ml": "NaCl-Bolus (ml)", "lr_bolus_ml": "LR-Bolus (ml)"}
BLOCKS = [(0, 6), (6, 12), (12, 24), (24, 48), (48, 72)]
KEY = {"sepsis": ["map_mmhg", "hr", "lactate", "creatinine", "norepi_rate"],
       "dka": ["glucose", "potassium", "bicarbonate", "ph", "anion_gap", "insulin_rate"],
       "hf": ["creatinine", "sodium", "furosemide_rate", "urine_ml", "hr", "map_mmhg"]}
NAME = {"sepsis": "Sepsis", "dka": "Diabetische Ketoazidose", "hf": "Akut dekompensierte Herzinsuffizienz"}
COND = {"sepsis": "is_sepsis AND NOT is_dka AND NOT is_hf_acute", "dka": "is_dka AND NOT is_sepsis AND NOT is_hf_acute",
        "hf": "is_hf_acute AND NOT is_sepsis AND NOT is_dka"}
def f(x):
    return "-" if x is None else f"{x:.2f}" if abs(x) < 10 else f"{x:.1f}" if abs(x) < 100 else f"{x:.0f}"

for coh in ["sepsis", "dka", "hf"]:
    n = con.execute(f"SELECT count(*) FROM st WHERE {COND[coh]}").fetchall()[0][0]
    d = con.execute(f"SELECT quantile_cont(los_h,0.1), median(los_h), quantile_cont(los_h,0.9), median(age_approx), "
                    f"100.0*avg((lower(gender)='female')::INT) FROM st WHERE {COND[coh]}").fetchall()[0]
    L = [f"# Profil {NAME[coh]} (MIMIC-IV, nur Aggregate, erste 72 ICU-Stunden)",
         f"- Aufenthalte: {n}; ICU-Dauer in h P10/Median/P90: {d[0]:.0f}/{d[1]:.0f}/{d[2]:.0f}; Alter Median ca. {d[3]:.0f}; Frauen {d[4]:.0f} %", "",
         "## Messgrößen: Anteil Aufenthalte mit Messung | Anteil Stunden mit Wert | P05 / Median / P95",
         "(Stunden-Aggregation: Vitalwerte Mittel, Labor letzter Wert)"]
    tot = con.execute(f"SELECT count(*), count(DISTINCT icu_encounter_id) FROM ts WHERE cohort='{coh}'").fetchall()[0]
    for v, lab in VARS.items():
        r = con.execute(f"SELECT count(DISTINCT icu_encounter_id) FILTER (WHERE {v} IS NOT NULL), count({v}), "
                        f"quantile_cont({v},0.05), median({v}), quantile_cont({v},0.95) FROM ts WHERE cohort='{coh}'").fetchall()[0]
        if r[1] >= 20:
            L.append(f"- {lab}: {100*r[0]/tot[1]:.0f} % | {r[1]/tot[0]:.2f} | {f(r[2])} / {f(r[3])} / {f(r[4])}")
    L += ["", "## Therapie (nur Stunden mit Gabe): Anteil Aufenthalte | P05 / Median / P95"]
    for v, lab in {**THER, **BOL}.items():
        r = con.execute(f"SELECT count(DISTINCT icu_encounter_id) FILTER (WHERE {v} > 0), count(*) FILTER (WHERE {v} > 0), "
                        f"quantile_cont({v},0.05) FILTER (WHERE {v} > 0), median({v}) FILTER (WHERE {v} > 0), "
                        f"quantile_cont({v},0.95) FILTER (WHERE {v} > 0) FROM ts WHERE cohort='{coh}'").fetchall()[0]
        if r[1] >= 20:
            L.append(f"- {lab}: {100*r[0]/tot[1]:.0f} % | {f(r[2])} / {f(r[3])} / {f(r[4])}")
    L += ["", "## Verlauf: Median je Zeitblock (Stunden " + ", ".join(f"{a}-{b}" for a, b in BLOCKS) + ")"]
    for v in KEY[coh]:
        cells = []
        for a, b in BLOCKS:
            r = con.execute(f"SELECT median({v}), count({v}) FROM ts WHERE cohort='{coh}' AND hour>={a} AND hour<{b}").fetchall()[0]
            cells.append(f(r[0]) if r[0] is not None and r[1] >= 20 else "-")
        L.append(f"- {VARS.get(v, THER.get(v, v))}: " + " | ".join(cells))
    txt = "\n".join(L) + "\n"
    open(f"profiles/{coh}.md", "w").write(txt)
    print(f"{coh}: {len(txt)} Zeichen, ca. {len(txt)//3} Token")
