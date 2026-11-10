#!/usr/bin/env python3
"""Create or validate a mockup regression report."""
from __future__ import annotations
import argparse, json
from pathlib import Path

P0 = {"R01","R02","R03","R04","R05","R06","R07","R10","R12","R15","R16","R17","R18","R20"}
ALL = [f"R{i:02d}" for i in range(1,21)]
VALID = {"PASS","FAIL","BLOCKED","NOT_RUN"}

def init_report():
    return {
        "suite": "mockup-fidelity",
        "version": 1,
        "cases": [
            {
                "case_id": cid,
                "result": "NOT_RUN",
                "failure_codes": [],
                "notes": "",
                "artifact": ""
            } for cid in ALL
        ]
    }

def validate(data):
    by_id = {c.get("case_id"): c for c in data.get("cases", [])}
    errors = []
    for cid in ALL:
        if cid not in by_id:
            errors.append(f"missing case {cid}")
            continue
        if by_id[cid].get("result") not in VALID:
            errors.append(f"{cid}: invalid result")
    p0_fail = [cid for cid in P0 if by_id.get(cid,{}).get("result") in {"FAIL","BLOCKED","NOT_RUN"}]
    ready = not errors and not p0_fail
    return {
        "ready_for_release": ready,
        "errors": errors,
        "blocking_p0": sorted(p0_fail),
        "counts": {s: sum(1 for c in by_id.values() if c.get("result")==s) for s in sorted(VALID)}
    }

def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    p_init = sub.add_parser("init")
    p_init.add_argument("--output", required=True)
    p_check = sub.add_parser("check")
    p_check.add_argument("--report", required=True)
    args = p.parse_args()

    if args.cmd == "init":
        out = Path(args.output)
        out.write_text(json.dumps(init_report(), indent=2), encoding="utf-8")
        print(out)
        return
    data = json.loads(Path(args.report).read_text(encoding="utf-8"))
    result = validate(data)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["ready_for_release"] else 2)

if __name__ == "__main__":
    main()
