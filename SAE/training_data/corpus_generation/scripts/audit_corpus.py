#!/usr/bin/env python3
from __future__ import annotations
import csv, json, re
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PLAN=ROOT/"configs"/"batch_plan_150k.csv"
BATCH_DIR=ROOT/"data"/"batches"
RAW_DIR=ROOT/"data"/"raw_sentences"
FINAL=ROOT/"data"/"sae_train_150k.jsonl"
PROV=ROOT/"data"/"generation_provenance_150k.jsonl"
REPORT=ROOT/"data"/"reports"/"corpus_audit.json"
SUMMARY=ROOT/"data"/"reports"/"corpus_audit.md"

plan=list(csv.DictReader(PLAN.open(encoding="utf-8")))
plan_by_batch={int(r["batch_id"]):r for r in plan}
all_rows=[]; all_raw=[]; missing=[]

for b in range(1,3001):
    p=BATCH_DIR/f"batch_{b:04d}.jsonl"
    rp=RAW_DIR/f"batch_{b:04d}.jsonl"
    if not p.exists() or not rp.exists():
        missing.append(b); continue
    rows=[json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
    raws=[json.loads(x) for x in rp.read_text(encoding="utf-8").splitlines() if x.strip()]
    if len(rows)!=50 or len(raws)!=50:
        raise SystemExit(f"Batch {b} does not contain 50 final/raw rows.")
    all_rows.extend(rows); all_raw.extend(raws)

if missing:
    raise SystemExit(f"Missing {len(missing)} batches; first missing: {missing[:20]}")

expected=[f"sae_train_{i:06d}" for i in range(1,150001)]
ids=[r["id"] for r in all_rows]
if ids != expected:
    raise SystemExit("IDs are not exactly continuous from sae_train_000001 to sae_train_150000.")

norm=lambda s: re.sub(r"\s+"," ",s.strip()).casefold()
dupes=len(all_rows)-len({norm(r["text"]) for r in all_rows})
if dupes:
    raise SystemExit(f"Found {dupes} exact normalized duplicate texts.")

with FINAL.open("w",encoding="utf-8",newline="\n") as f:
    for r in all_rows: f.write(json.dumps(r,ensure_ascii=False)+"\n")
with PROV.open("w",encoding="utf-8",newline="\n") as f:
    for r in all_raw: f.write(json.dumps(r,ensure_ascii=False)+"\n")

var_counts=Counter(v for r in all_rows for v in r["variables_present"])
lang_counts=Counter(r["language"] for r in all_rows)
domain_counts=Counter(r["lexical_domain"] for r in all_rows)
length_counts=Counter(r["length_bucket"] for r in all_rows)

primary_hits=Counter(); primary_totals=Counter()
language_hits=Counter(); language_totals=Counter()
construction_counts=Counter()
for r,raw in zip(all_rows,all_raw):
    pv=int(raw["primary_variable_id"])
    primary_totals[pv]+=1
    if pv in r["variables_present"]: primary_hits[pv]+=1
    pl=raw["planned_language"]; language_totals[pl]+=1
    if r["language"]==pl: language_hits[pl]+=1
    construction_counts[(pv,raw["construction_family"])]+=1

report={
    "total_examples":len(all_rows),
    "exact_duplicate_count":dupes,
    "annotation_variable_counts":dict(sorted(var_counts.items())),
    "language_counts":dict(lang_counts.most_common()),
    "domain_counts":dict(domain_counts.most_common()),
    "length_counts":dict(length_counts),
    "primary_variable_annotation_hit_rate":{
        str(v):primary_hits[v]/primary_totals[v] for v in sorted(primary_totals)
    },
    "planned_language_match_rate":{
        k:language_hits[k]/language_totals[k] for k in sorted(language_totals)
    },
}
REPORT.parent.mkdir(parents=True,exist_ok=True)
REPORT.write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding="utf-8")

lines=[
    "# 150k SAE Corpus Audit","",
    f"- Total examples: {len(all_rows)}",
    f"- Exact normalized duplicate texts: {dupes}",
    f"- Final corpus: `{FINAL.relative_to(ROOT)}`",
    f"- Generation provenance: `{PROV.relative_to(ROOT)}`","",
    "## Length buckets",""
]
for k in ("short","medium","long"):
    lines.append(f"- {k}: {length_counts[k]}")
lines += ["","## Languages",""]
for k,v in lang_counts.most_common():
    lines.append(f"- {k}: {v}")
lines += ["","## Primary variable annotation hit rate",""]
for v in range(1,41):
    lines.append(f"- {v}: {primary_hits[v]}/{primary_totals[v]} ({primary_hits[v]/primary_totals[v]:.3f})")
SUMMARY.write_text("\n".join(lines)+"\n",encoding="utf-8")
print(f"Audit PASSED. Wrote {FINAL}")
print(f"Wrote {REPORT} and {SUMMARY}")
