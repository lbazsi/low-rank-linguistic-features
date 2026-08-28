#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import time
from collections import Counter
from pathlib import Path

import yaml
from tqdm import tqdm
from transformers import AutoTokenizer
from vllm import LLM, SamplingParams

ROOT = Path(__file__).resolve().parents[1]

ALLOWED_DOMAINS = [
    "daily_life","family_relationships","social_interaction","workplace","education",
    "science_technology","health","travel_transport","food_household","nature_environment",
    "news_public_affairs","arts_culture","sports_recreation"
]
LENGTH_BUCKETS = {"short","medium","long"}

STYLE_ANGLES = [
    "ordinary conversation","brief narrative","matter-of-fact description","work or institutional context",
    "personal observation","news-like factual statement","technical but natural statement","social interaction",
    "travel or public-space situation","domestic everyday situation","education or research context",
    "arts or cultural context"
]

def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))

def load_plan(path: Path):
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        for k in ("batch_id","start_id","end_id","n_examples","primary_variable_id",
                  "short_count","medium_count","long_count","construction_index","repetition"):
            r[k] = int(r[k])
        r["domains"] = r["domains"].split(";")
    return rows

def compact_variable_catalog(variables):
    lines=[]
    for v in variables:
        lines.append(f'{v["id"]}: {v["name"]} — {v["description"]}')
    return "\n".join(lines)

def render_chat(tokenizer, system: str, user: str) -> str:
    messages=[{"role":"system","content":system},{"role":"user","content":user}]
    kwargs=dict(tokenize=False, add_generation_prompt=True)
    # Qwen3 supports disabling thinking through the chat template.
    try:
        return tokenizer.apply_chat_template(messages, enable_thinking=False, **kwargs)
    except TypeError:
        return tokenizer.apply_chat_template(messages, **kwargs)

def clean_sentence(raw: str) -> str:
    t=raw.strip()
    t=re.sub(r"^```(?:text)?\s*", "", t, flags=re.I)
    t=re.sub(r"\s*```$", "", t)
    t=" ".join(line.strip() for line in t.splitlines() if line.strip())
    if len(t) >= 2 and ((t[0]=='"' and t[-1]=='"') or (t[0]=="“" and t[-1]=="”")):
        t=t[1:-1].strip()
    return t

def extract_json(raw: str):
    t=raw.strip()
    t=re.sub(r"^```(?:json)?\s*", "", t, flags=re.I)
    t=re.sub(r"\s*```$", "", t)
    a=t.find("{"); b=t.rfind("}")
    if a < 0 or b < a:
        raise ValueError("No JSON object found")
    return json.loads(t[a:b+1])

def normalize_text(t: str) -> str:
    return re.sub(r"\s+", " ", t.strip()).casefold()

def batch_is_valid(path: Path, plan_row: dict) -> bool:
    if not path.exists():
        return False
    try:
        rows=[json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]
    except Exception:
        return False
    if len(rows) != plan_row["n_examples"]:
        return False
    ids=[f'sae_train_{i:06d}' for i in range(plan_row["start_id"], plan_row["end_id"]+1)]
    return [r.get("id") for r in rows] == ids

def make_specs(plan_row: dict):
    lengths=(["short"]*plan_row["short_count"] +
             ["medium"]*plan_row["medium_count"] +
             ["long"]*plan_row["long_count"])
    # Deterministic within-batch interleaving, not random text generation.
    # This only distributes prompt metadata.
    interleaved=[]
    s=lengths[:plan_row["short_count"]]
    m=lengths[plan_row["short_count"]:plan_row["short_count"]+plan_row["medium_count"]]
    l=lengths[-plan_row["long_count"]:]
    pools={"short":len(s),"medium":len(m),"long":len(l)}
    pattern=["medium","short","medium","long","medium"]
    while sum(pools.values()):
        for x in pattern:
            if pools[x] > 0:
                interleaved.append(x); pools[x]-=1
    specs=[]
    for j, ex_id in enumerate(range(plan_row["start_id"], plan_row["end_id"]+1)):
        specs.append({
            "id":f"sae_train_{ex_id:06d}",
            "example_number":j+1,
            "domain":plan_row["domains"][j % len(plan_row["domains"])],
            "target_length":interleaved[j],
            "style_angle":STYLE_ANGLES[(plan_row["batch_id"] + j) % len(STYLE_ANGLES)],
        })
    return specs

def sentence_prompt(plan_row, var_cfg, spec):
    length_help={
        "short":"roughly one compact clause or 5–10 words where natural for the language",
        "medium":"roughly 11–20 words or equivalent complexity",
        "long":"roughly 21–35 words or equivalent complexity",
    }[spec["target_length"]]
    return f"""Generate ONE natural standalone sentence.

Language: {plan_row["language_name"]} ({plan_row["language"]})
Primary linguistic variable: {var_cfg["name"]}
Variable meaning: {var_cfg["description"]}
Construction family to realize: {plan_row["construction_family"]}
Lexical domain: {spec["domain"]}
Length target: {spec["target_length"]} — {length_help}
Style angle: {spec["style_angle"]}

Important constraints:
- The sentence must genuinely instantiate the named construction and primary variable.
- Use normal native orthography and script for the language.
- Write plausible human language, not a grammar textbook example.
- Do not mention linguistic terminology or explain the sentence.
- Vary vocabulary, participants, predicates, word order, and discourse setting.
- Other linguistic features may occur naturally.
- {var_cfg["avoid_shortcut"]}
- Do not use templates, slot-filling patterns, pseudo-morphology, or artificial spelling corruption.
- Output the sentence only, with no label, numbering, quotation wrapper, translation, or commentary."""

def annotation_prompt(sentence, plan_row, var_cfg, spec, catalog):
    return f"""Annotate the finished sentence below. This is a NEW task; do not rewrite or improve the sentence.

AUTHORITATIVE ID: {spec["id"]}
AUTHORITATIVE SENTENCE:
{sentence}

Generation context:
- planned language: {plan_row["language"]} ({plan_row["language_name"]})
- planned primary variable: {var_cfg["id"]} — {var_cfg["name"]}
- planned construction: {plan_row["construction_family"]}
- planned lexical domain: {spec["domain"]}

Return exactly one JSON object with exactly these six keys:
{{
  "id": "{spec["id"]}",
  "text": "<copy the authoritative sentence verbatim>",
  "language": "<actual lowercase ISO-style language code>",
  "variables_present": [<sorted unique integer IDs>],
  "lexical_domain": "<one allowed domain>",
  "length_bucket": "<short|medium|long>"
}}

Variable catalog:
{catalog}

Allowed lexical domains:
{", ".join(ALLOWED_DOMAINS)}

Annotation policy:
- Copy `id` and `text` exactly.
- Be CONSERVATIVE with `variables_present`: include only variables with a clear, diagnostically meaningful realization in this sentence. Do not tag every sentence for ordinary tense, word order, number, definiteness, etc. merely because language necessarily has those properties.
- The planned primary variable is context, not a forced label. Include it only if the sentence truly realizes it.
- Do not explain your answer.
- Output JSON only."""

def validate_annotation(obj, sentence, spec, plan_row, require_language, require_primary):
    req=["id","text","language","variables_present","lexical_domain","length_bucket"]
    if list(obj.keys()) != req:
        raise ValueError(f"Wrong keys/order: {list(obj.keys())}")
    if obj["id"] != spec["id"]:
        raise ValueError("ID mismatch")
    if obj["text"] != sentence:
        raise ValueError("Text changed in annotation")
    if not isinstance(obj["language"], str) or not obj["language"]:
        raise ValueError("Invalid language")
    if require_language and obj["language"] != plan_row["language"]:
        raise ValueError(f'Language mismatch {obj["language"]} != {plan_row["language"]}')
    vals=obj["variables_present"]
    if not isinstance(vals,list) or any(not isinstance(v,int) or not 1 <= v <= 40 for v in vals):
        raise ValueError("Invalid variables_present")
    if vals != sorted(set(vals)):
        raise ValueError("variables_present must be sorted and unique")
    if require_primary and plan_row["primary_variable_id"] not in vals:
        raise ValueError("Primary variable absent from conservative annotation")
    if obj["lexical_domain"] not in ALLOWED_DOMAINS:
        raise ValueError("Invalid lexical_domain")
    if obj["length_bucket"] not in LENGTH_BUCKETS:
        raise ValueError("Invalid length_bucket")
    return obj

def load_seen(batch_dir: Path):
    seen=set()
    for p in sorted(batch_dir.glob("batch_*.jsonl")):
        try:
            for line in p.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    seen.add(normalize_text(json.loads(line)["text"]))
        except Exception:
            pass
    return seen

def generate_outputs(llm, prompts, params):
    outputs=llm.generate(prompts, params, use_tqdm=False)
    return [o.outputs[0].text for o in outputs]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/generation.yaml")
    ap.add_argument("--start-batch", type=int, default=1)
    ap.add_argument("--end-batch", type=int, default=None)
    ap.add_argument("--max-batches", type=int, default=None)
    args=ap.parse_args()

    cfg=load_yaml(ROOT/args.config)
    plan=load_plan(ROOT/cfg["batch_plan"])
    var_doc=load_yaml(ROOT/cfg["variable_config"])
    vars_by_id={int(v["id"]):v for v in var_doc["variables"]}
    catalog=compact_variable_catalog(var_doc["variables"])

    outroot=ROOT/cfg["output_root"]
    batch_dir=outroot/"batches"; raw_dir=outroot/"raw_sentences"; report_dir=outroot/"reports"
    for p in (batch_dir,raw_dir,report_dir): p.mkdir(parents=True, exist_ok=True)

    selected=[r for r in plan if r["batch_id"] >= args.start_batch and
              (args.end_batch is None or r["batch_id"] <= args.end_batch)]
    if args.max_batches is not None:
        selected=selected[:args.max_batches]

    tokenizer=AutoTokenizer.from_pretrained(cfg["model_name"], trust_remote_code=False)

    sentence_system="""You are generating a high-quality multilingual linguistic corpus for representation learning.
Follow the requested language and construction exactly. Produce natural human language.
Never explain, translate, enumerate, or discuss grammar. Return only the requested sentence."""
    annotation_system="""You are a conservative linguistic corpus annotator.
Return valid JSON only. Never rewrite the supplied sentence.
Do not over-annotate: mark a variable only when the sentence contains a clear diagnostic realization."""

    print(f'Loading {cfg["model_name"]} with vLLM ...', flush=True)
    llm=LLM(
        model=cfg["model_name"],
        dtype=cfg["dtype"],
        tensor_parallel_size=int(cfg["tensor_parallel_size"]),
        gpu_memory_utilization=float(cfg["gpu_memory_utilization"]),
        max_model_len=int(cfg["max_model_len"]),
        enable_prefix_caching=bool(cfg.get("enable_prefix_caching", True)),
        trust_remote_code=False,
    )
    sentence_params=SamplingParams(**cfg["sentence_sampling"])
    annotation_params=SamplingParams(**cfg["annotation_sampling"])

    seen=load_seen(batch_dir)
    completed=0

    for row in tqdm(selected, desc="150k generation batches"):
        b=row["batch_id"]
        batch_path=batch_dir/f"batch_{b:04d}.jsonl"
        raw_path=raw_dir/f"batch_{b:04d}.jsonl"
        if batch_is_valid(batch_path,row):
            continue

        var_cfg=vars_by_id[row["primary_variable_id"]]
        specs=make_specs(row)
        pending=list(range(len(specs)))
        sentences=[None]*len(specs)
        annotations=[None]*len(specs)
        raw_records=[None]*len(specs)
        failures=Counter()

        for gen_attempt in range(1, int(cfg["max_generation_retries"])+1):
            if not pending: break

            prompts=[]
            for idx in pending:
                user=sentence_prompt(row,var_cfg,specs[idx])
                if gen_attempt > 1:
                    user += f"\nThis is retry {gen_attempt}. Use a substantially different lexical and syntactic realization from any obvious stock example."
                prompts.append(render_chat(tokenizer,sentence_system,user))
            raw_sents=generate_outputs(llm,prompts,sentence_params)

            candidates={}
            next_pending=[]
            local_seen=set()
            for idx, raw in zip(pending,raw_sents):
                sent=clean_sentence(raw)
                norm=normalize_text(sent)
                if not sent or len(sent) < 3:
                    failures["empty_sentence"]+=1; next_pending.append(idx); continue
                if norm in seen or norm in local_seen:
                    failures["exact_duplicate"]+=1; next_pending.append(idx); continue
                candidates[idx]=(sent,raw)
                local_seen.add(norm)

            if not candidates:
                pending=next_pending
                continue

            ann_pending=list(candidates.keys())
            ann_objs={}
            ann_raws={}
            for ann_attempt in range(1, int(cfg["max_annotation_retries"])+1):
                if not ann_pending: break
                ann_prompts=[]
                for idx in ann_pending:
                    sent,_=candidates[idx]
                    ann_prompts.append(render_chat(
                        tokenizer, annotation_system,
                        annotation_prompt(sent,row,var_cfg,specs[idx],catalog)
                    ))
                raw_anns=generate_outputs(llm,ann_prompts,annotation_params)
                retry=[]
                for idx, raw_ann in zip(ann_pending,raw_anns):
                    sent,_=candidates[idx]
                    try:
                        obj=extract_json(raw_ann)
                        obj=validate_annotation(
                            obj,sent,specs[idx],row,
                            bool(cfg["require_planned_language"]),
                            bool(cfg["require_primary_variable_in_annotation"])
                        )
                        ann_objs[idx]=obj; ann_raws[idx]=raw_ann
                    except Exception as e:
                        failures[f"annotation_retry:{type(e).__name__}"]+=1
                        retry.append(idx)
                ann_pending=retry

            accepted=[]
            for idx in candidates:
                if idx not in ann_objs:
                    next_pending.append(idx)
                    continue
                sent,raw_sent=candidates[idx]
                annotations[idx]=ann_objs[idx]
                sentences[idx]=sent
                raw_records[idx]={
                    "id":specs[idx]["id"],
                    "batch_id":b,
                    "primary_variable_id":row["primary_variable_id"],
                    "primary_variable":row["primary_variable"],
                    "construction_family":row["construction_family"],
                    "planned_language":row["language"],
                    "planned_domain":specs[idx]["domain"],
                    "target_length":specs[idx]["target_length"],
                    "style_angle":specs[idx]["style_angle"],
                    "sentence":sent,
                    "raw_sentence_model_output":raw_sent,
                    "raw_annotation_model_output":ann_raws[idx],
                }
                seen.add(normalize_text(sent))
                accepted.append(idx)

            pending=sorted(set(next_pending))

        if pending:
            fail_path=report_dir/f"failed_batch_{b:04d}.json"
            fail_path.write_text(json.dumps({
                "batch_id":b,
                "failed_indices":pending,
                "failed_ids":[specs[i]["id"] for i in pending],
                "failure_counts":dict(failures),
            },indent=2),encoding="utf-8")
            raise RuntimeError(f"Batch {b} failed after retries. See {fail_path}")

        # Atomic batch writes.
        tmp=batch_path.with_suffix(".tmp")
        with tmp.open("w",encoding="utf-8",newline="\n") as f:
            for obj in annotations:
                f.write(json.dumps(obj,ensure_ascii=False)+"\n")
        tmp.replace(batch_path)

        tmp_raw=raw_path.with_suffix(".tmp")
        with tmp_raw.open("w",encoding="utf-8",newline="\n") as f:
            for obj in raw_records:
                f.write(json.dumps(obj,ensure_ascii=False)+"\n")
        tmp_raw.replace(raw_path)
        completed += 1

    print(f"Generation phase finished for selected range; newly completed batches: {completed}")
    print("Run scripts/audit_corpus.py to assemble/audit the final corpus.")

if __name__ == "__main__":
    main()
