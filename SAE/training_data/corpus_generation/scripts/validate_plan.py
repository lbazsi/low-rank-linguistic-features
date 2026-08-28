#!/usr/bin/env python3
from pathlib import Path
from collections import Counter
import csv, yaml

ROOT = Path(__file__).resolve().parents[1]
plan = list(csv.DictReader((ROOT/"configs"/"batch_plan_150k.csv").open(encoding="utf-8")))
cfg = yaml.safe_load((ROOT/"configs"/"variable_constructions.yaml").read_text(encoding="utf-8"))
vars_by_id = {int(v["id"]): v for v in cfg["variables"]}

assert len(plan) == 3000, f"Expected 3000 batches, got {len(plan)}"
assert sum(int(r["n_examples"]) for r in plan) == 150000
assert [int(r["batch_id"]) for r in plan] == list(range(1,3001))
assert [int(r["start_id"]) for r in plan] == [1 + 50*i for i in range(3000)]
assert [int(r["end_id"]) for r in plan] == [50*(i+1) for i in range(3000)]

vcounts = Counter(int(r["primary_variable_id"]) for r in plan)
assert set(vcounts) == set(range(1,41))
assert all(vcounts[v] == 75 for v in range(1,41)), vcounts

vc = Counter((int(r["primary_variable_id"]), r["construction_family"]) for r in plan)
for vid, v in vars_by_id.items():
    for c in v["construction_families"]:
        assert vc[(vid,c)] == 15, (vid,c,vc[(vid,c)])

for r in plan:
    vid=int(r["primary_variable_id"])
    assert r["construction_family"] in vars_by_id[vid]["construction_families"]
    assert r["language"] in vars_by_id[vid]["preferred_languages"]
    assert int(r["short_count"])+int(r["medium_count"])+int(r["long_count"]) == 50
    assert len(r["domains"].split(";")) == 3

print("Batch plan PASSED: 3000 batches, 150000 examples, 3750 examples/variable, 750 examples/construction.")
