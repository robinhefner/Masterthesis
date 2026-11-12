import json, time, urllib.request, duckdb

P = "/srv/mimic/parquet"
COLS = ["hour", "hr", "rr", "spo2", "map_mmhg", "temp_c", "gcs", "glucose", "ph", "lactate", "creatinine",
        "potassium", "sodium", "bicarbonate", "anion_gap", "urine_ml", "norepi_rate", "insulin_rate", "nacl_rate"]

def fmt(v):
    return "" if v is None else f"{round(v, 2):g}"

def tokens(text):
    body = json.dumps({"model": "qwen14b-16k", "prompt": text, "stream": False,
                       "options": {"num_predict": 1}}).encode()
    req = urllib.request.Request("http://127.0.0.1:11434/api/generate", body, {"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req))["prompt_eval_count"]

con = duckdb.connect()
for coh in ["sepsis", "dka", "hf"]:
    rows = con.execute(f"""
      SELECT {', '.join(COLS)} FROM '{P}/timeseries_h72.parquet'
      WHERE icu_encounter_id = (SELECT icu_encounter_id FROM '{P}/timeseries_h72.parquet'
                                WHERE cohort='{coh}' GROUP BY 1 HAVING count(*) >= 72
                                ORDER BY hash(icu_encounter_id) LIMIT 1)
      ORDER BY hour""").fetchall()
    stamp = f"{coh}-{time.time()}\n"      # verhindert Cache-Treffer auf gleiche Präfixe
    full = "\n".join([",".join(COLS)] + [",".join(fmt(v) for v in r) for r in rows])
    third = "\n".join([",".join(COLS)] + [",".join(fmt(v) for v in r) for r in rows[::3]])
    t_full, t_third = tokens(stamp + full), tokens(stamp + third)
    print(f"{coh}: {len(rows)} Zeilen | stündlich: {t_full} Token ({t_full/len(rows):.0f}/Zeile) | "
          f"jede 3. Stunde: {t_third} Token | {len(COLS)} Spalten")
