import duckdb
P = "/srv/mimic/parquet"

def vals(name, codes, unit):
    lst = ",".join(f"'{c}'" for c in codes)
    print(f"\n== {name}")
    duckdb.sql(f"""
      SELECT code, any_value(display) AS bezeichnung, any_value({unit}) AS einheit,
             count(*) AS n, count(value) AS n_zahl, count(value_str) AS n_text,
             round(quantile_cont(value, 0.01), 1) AS p01, round(median(value), 1) AS median,
             round(quantile_cont(value, 0.99), 1) AS p99
      FROM '{P}/{name}_cohort.parquet' WHERE code IN ({lst}) GROUP BY code ORDER BY code""").show(max_width=170)

vals("chartevents", ["220045","220210","220277","220052","220181","223761","223762","223835",
                     "220739","223900","223901","225664","220621","223830","224639","226512"], "unit")
vals("labevents", ["50813","50931","50971","50983","50882","50868","50912","51006","50820",
                   "50818","50821","50802","50885","51265","51301","51237","50963","51003"], "unit")

print("\n== medicationicu (dose und rate)")
duckdb.sql(f"""
  SELECT code, any_value(display) AS name, dose_unit, rate_unit, count(*) AS n,
         count(dose) AS n_dose, count(rate) AS n_rate,
         round(median(dose), 3) AS med_dose, round(median(rate), 3) AS med_rate
  FROM '{P}/medicationicu_cohort.parquet'
  WHERE code IN ('221906','222315','221749','221653','221986','222056','221347','223258','223262','223260',
                 '225166','225158','225828','221794','228340')
  GROUP BY code, dose_unit, rate_unit ORDER BY code, n DESC""").show(max_width=170)
