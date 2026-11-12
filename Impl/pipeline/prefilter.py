import sys, re
field, keyfile = sys.argv[1], sys.argv[2]        # field: encounter | context
keys = set(l.strip() for l in open(keyfile, "rb"))
rx = re.compile(rb'"' + field.encode() + rb'"\s*:\s*\{\s*"reference"\s*:\s*"Encounter/([^"]+)"')
out = sys.stdout.buffer
n = hit = 0
for line in sys.stdin.buffer:
    n += 1
    m = rx.search(line)
    if m and m.group(1) in keys:
        out.write(line); hit += 1
    if n % 5_000_000 == 0:
        print(f"{n} Zeilen, {hit} Treffer", file=sys.stderr, flush=True)
print(f"FERTIG: {n} Zeilen, {hit} Treffer", file=sys.stderr)
