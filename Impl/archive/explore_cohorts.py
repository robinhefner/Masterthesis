import duckdb

con = duckdb.connect()
P = "/srv/mimic/parquet"
con.execute(f"CREATE VIEW cond AS SELECT * FROM '{P}/MimicCondition.parquet'")
con.execute(f"CREATE VIEW icu AS SELECT * FROM '{P}/MimicEncounterICU.parquet'")

patterns = {
    "dka":    ["2501%", "E101%", "E111%", "E131%"],
    "hf":     ["428%", "I50%"],
    "sepsis": ["038%", "99591", "99592", "78552", "A40%", "A41%", "R652%"],
}

for name, pats in patterns.items():
    where = " OR ".join(f"c.code LIKE '{p}'" for p in pats)
    print(f"\n=== {name}: Aufenthalte je Codesystem ===")
    con.sql(f"""
        SELECT c.code_system,
               count(DISTINCT c.encounter_id)     AS krankenhausaufenthalte,
               count(DISTINCT i.icu_encounter_id) AS icu_aufenthalte
        FROM cond c LEFT JOIN icu i ON c.encounter_id = i.encounter_id
        WHERE {where} GROUP BY ALL ORDER BY 2 DESC""").show()
    print(f"=== {name}: häufigste Codes ===")
    con.sql(f"""
        SELECT c.code, any_value(c.display) AS bezeichnung,
               count(DISTINCT i.icu_encounter_id) AS icu_aufenthalte
        FROM cond c JOIN icu i ON c.encounter_id = i.encounter_id
        WHERE {where} GROUP BY c.code ORDER BY 3 DESC LIMIT 15""").show()
