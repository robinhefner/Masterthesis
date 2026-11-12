#!/usr/bin/env bash
# Datenaufbereitung MIMIC-IV on FHIR 2.1 -> Parquet, Zeitreihe, Profile.
# Voraussetzung: Rohdaten (*.ndjson.gz) liegen in $RAW (Download mit PhysioNet-Zugang,
# Passwort nie in ein Skript schreiben; wget -c -r -np --user <name> --ask-password ...).
#
# Aufruf (am besten in tmux):
#   bash pipeline/run_all.sh                  alle Schritte, vorhandene Ergebnisse werden übersprungen
#   bash pipeline/run_all.sh check            nur vorhandene Ergebnisse prüfen
#   bash pipeline/run_all.sh filter extract   einzelne Schritte
#   FORCE=1 bash pipeline/run_all.sh extract  Schritt neu rechnen
#   VERIFY=0 ...                              Zeilenzählung der gefilterten Dateien überspringen
# Schritte: flatten cohorts keys filter extract timeseries profiles rules
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RAW=/srv/mimic/mimic-iv-fhir/2.1/fhir
P=/srv/mimic/parquet
F=/srv/mimic/filtered
TMP=/srv/mimic/duck_tmp
FORCE="${FORCE:-0}"
VERIFY="${VERIFY:-1}"
cd "$ROOT"
mkdir -p runs "$P" "$F" "$TMP"
exec > >(tee -a "runs/run_all_$(date +%Y%m%d-%H%M).log") 2>&1

# Erwartete Zeilenzahlen (Stand 12.11.2026, MIMIC-IV on FHIR 2.1). Bei anderer Version anpassen.
declare -A EXP=(
  [MimicPatient]=299712 [MimicEncounter]=431231 [MimicEncounterICU]=73181
  [MimicCondition]=4756326 [MimicProcedureICU]=696092
  [cohort_stays]=13377
  [chartevents_cohort]=88451563 [labevents_cohort]=7827978
  [outputevents_cohort]=1126979 [medicationicu_cohort]=2850796
  [timeseries_h72]=784779
)

log()  { echo "[$(date +%H:%M:%S)] $*"; }
die()  { echo "FEHLER: $*" >&2; exit 1; }
need_space() {
  local free; free=$(df --output=avail -BG / | tail -n 1 | tr -dc '0-9')
  [ "$free" -ge "$1" ] || die "nur $free GB frei, benötigt $1 GB"
}
count_parquet() {
  uv run python -c "import duckdb,sys; print(duckdb.sql(f\"SELECT count(*) FROM '{sys.argv[1]}'\").fetchall()[0][0])" "$1"
}
check_parquet() {   # Name (Datei: $P/Name.parquet)
  local got; got=$(count_parquet "$P/$1.parquet")
  [ "$got" = "${EXP[$1]}" ] || die "$1: $got Zeilen, erwartet ${EXP[$1]}"
  log "ok  $1: $got Zeilen"
}
check_lines() {     # Quelle (Ordner: $F/Quelle, erwartet EXP[Quelle_cohort])
  [ "$VERIFY" = "1" ] || { log "übersprungen (VERIFY=0): $1"; return 0; }
  local got; got=$(zcat "$F/$1"/part_*.ndjson.gz | wc -l)
  [ "$got" = "${EXP[${1}_cohort]}" ] || die "gefiltert $1: $got Zeilen, erwartet ${EXP[${1}_cohort]}"
  log "ok  gefiltert $1: $got Zeilen"
}
done_all() { for f in "$@"; do [ -s "$f" ] || return 1; done; [ "$FORCE" != "1" ]; }

step_flatten() {
  local small=(MimicPatient MimicEncounter MimicEncounterICU MimicCondition MimicProcedureICU)
  if done_all "${small[@]/#/$P/}"; then :; fi
  local files=(); for n in "${small[@]}"; do files+=("$P/$n.parquet"); done
  if done_all "${files[@]}"; then log "flatten: vorhanden"; else
    need_space 5; log "flatten ..."; uv run python -u pipeline/flatten_small.py
  fi
  for n in "${small[@]}"; do check_parquet "$n"; done
}
step_cohorts() {
  if done_all "$P/cohort_stays.parquet"; then log "cohorts: vorhanden"; else
    log "cohorts ..."; uv run python -u pipeline/build_cohorts.py | tee runs/cohorts_out.txt
  fi
  check_parquet cohort_stays
}
step_keys() {
  if done_all "$F/keys_icu.txt" "$F/keys_hosp.txt"; then log "keys: vorhanden"; else
    uv run python - <<'PY'
import duckdb
P, F = "/srv/mimic/parquet", "/srv/mimic/filtered"
duckdb.sql(f"COPY (SELECT DISTINCT icu_encounter_id FROM '{P}/cohort_stays.parquet') TO '{F}/keys_icu.txt' (FORMAT csv, HEADER false)")
duckdb.sql(f"COPY (SELECT DISTINCT encounter_id FROM '{P}/cohort_stays.parquet') TO '{F}/keys_hosp.txt' (FORMAT csv, HEADER false)")
PY
  fi
  for k in icu hosp; do
    [ "$(wc -l < "$F/keys_$k.txt")" = "${EXP[cohort_stays]}" ] || die "keys_$k.txt hat nicht ${EXP[cohort_stays]} Zeilen"
  done
  log "ok  Schlüsseldateien: ${EXP[cohort_stays]} Zeilen"
}
filter_one() {      # Name Rohdatei Feld Schlüssel
  local name=$1 file=$2 field=$3 keys=$4
  if done_all "$F/$name/part_00.ndjson.gz"; then log "filter $name: vorhanden"; else
    need_space 15; rm -rf "$F/$name" "$F/$name.tmp"; mkdir -p "$F/$name.tmp"
    log "filter $name ..."
    if [ "$name" = chartevents ]; then     # in Stücke zu 10 Mio. Zeilen teilen (hält DuckDB schlank)
      zcat "$RAW/$file.ndjson.gz" | python3 pipeline/prefilter.py "$field" "$F/keys_$keys.txt" \
        | split -l 10000000 -d -a 2 --filter="gzip -1 > $F/$name.tmp/\$FILE.ndjson.gz" - part_
    else
      zcat "$RAW/$file.ndjson.gz" | python3 pipeline/prefilter.py "$field" "$F/keys_$keys.txt" \
        | gzip -1 > "$F/$name.tmp/part_00.ndjson.gz"
    fi
    mv "$F/$name.tmp" "$F/$name"
  fi
  check_lines "$name"
}
step_filter() {
  filter_one chartevents    MimicObservationChartevents       encounter icu
  filter_one outputevents   MimicObservationOutputevents      encounter icu
  filter_one medicationicu  MimicMedicationAdministrationICU  context   icu
  filter_one labevents      MimicObservationLabevents         encounter hosp
}
step_extract() {
  for n in outputevents medicationicu labevents chartevents; do
    if done_all "$P/${n}_cohort.parquet"; then log "extract $n: vorhanden"; else
      need_space 10; log "extract $n ..."; uv run python -u pipeline/extract_big.py "$n"; rm -rf "${TMP:?}"/*
    fi
    check_parquet "${n}_cohort"
  done
}
step_timeseries() {
  if done_all "$P/timeseries_h72.parquet"; then log "timeseries: vorhanden"; else
    need_space 10; log "timeseries ..."
    uv run python -u pipeline/build_timeseries.py 72 > runs/timeseries_h72_out.txt
    rm -rf "${TMP:?}"/*
  fi
  check_parquet timeseries_h72
}
step_profiles() { log "profiles ..."; uv run python -u pipeline/build_profiles.py; }
step_rules()    { log "rules ...";    uv run python -u pipeline/rule_onset.py | tee runs/rule_onset_out.txt; }
step_check() {
  for n in MimicPatient MimicEncounter MimicEncounterICU MimicCondition MimicProcedureICU cohort_stays \
           chartevents_cohort labevents_cohort outputevents_cohort medicationicu_cohort timeseries_h72; do
    check_parquet "$n"
  done
  for n in chartevents outputevents medicationicu labevents; do check_lines "$n"; done
}

STEPS=("$@")
if [ ${#STEPS[@]} -eq 0 ]; then STEPS=(flatten cohorts keys filter extract timeseries profiles rules); fi
for s in "${STEPS[@]}"; do
  case "$s" in
    flatten|cohorts|keys|filter|extract|timeseries|profiles|rules|check) "step_$s" ;;
    *) die "unbekannter Schritt: $s" ;;
  esac
done
log "fertig"
