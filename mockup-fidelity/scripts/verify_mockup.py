#!/usr/bin/env python3
from pathlib import Path
import argparse, json, math, sys
import numpy as np
from PIL import Image
from mockup_core import render, sha256_file

def arr(path):
    return np.asarray(Image.open(path).convert("RGBA"))

def angular_rgb_deg(a, b, mask):
    x = a[...,:3].astype(float)[mask]
    y = b[...,:3].astype(float)[mask]
    nx = np.linalg.norm(x, axis=1); ny = np.linalg.norm(y, axis=1)
    good = (nx > 8) & (ny > 8)
    if not np.any(good):
        return 0.0, 0.0
    x=x[good]; y=y[good]; nx=nx[good]; ny=ny[good]
    cos = np.sum(x*y, axis=1)/(nx*ny)
    deg = np.degrees(np.arccos(np.clip(cos,-1,1)))
    return float(np.median(deg)), float(np.percentile(deg,95))

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out-dir", required=True)
    p.add_argument("--artwork", required=True)
    a=p.parse_args()
    out=Path(a.out_dir)
    m=json.loads((out/"manifest.json").read_text())
    checks=[]

    checks.append(("artwork_hash", sha256_file(a.artwork)==m["artwork_sha256"]))

    base_path=m["base_path"]
    checks.append(("base_hash", Path(base_path).exists() and sha256_file(base_path)==m["base_sha256"]))

    q=m["quad_used"]; W,H=m["base_size"]
    inside=all(0 <= x < W and 0 <= y < H for x,y in q)
    checks.append(("target_inside_canvas", inside))

    rr=render(base_path, a.artwork, m["quad_requested"], m["fit"], m["fidelity"], m["lighting_strength"])
    expected_w=np.asarray(rr["warped"].convert("RGBA"))
    expected_p=np.asarray(rr["presentation"].convert("RGBA"))
    expected_m=np.asarray(rr["mockup"].convert("RGBA"))
    actual_w=arr(out/"warped_artwork.png")
    actual_p=arr(out/"presentation_artwork.png")
    actual_m=arr(out/"mockup.png")

    checks.append(("warped_regenerates_exactly", np.array_equal(expected_w,actual_w)))
    checks.append(("presentation_regenerates_exactly", np.array_equal(expected_p,actual_p)))
    checks.append(("final_composite_regenerates_exactly", np.array_equal(expected_m,actual_m)))

    mask=actual_w[...,3] > 32
    med,p95=angular_rgb_deg(actual_w, actual_p, mask)
    if m["fidelity"]=="high":
        hue_ok=(med <= 1.0 and p95 <= 3.0)
    else:
        hue_ok=(med <= 2.0 and p95 <= 5.0)
    checks.append(("presentation_hue_drift", hue_ok))

    status=all(v for _,v in checks)
    report={
        "status":"PASS" if status else "FAIL",
        "fidelity":m["fidelity"],
        "fit":m["fit"],
        "hue_drift_degrees":{"median":round(med,4),"p95":round(p95,4)},
        "checks":{k:v for k,v in checks},
        "note":"This proves source-derived deterministic integrity; it does not prove perfect geometry on severe 3D curvature."
    }
    (out/"verification.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps(report,indent=2))
    raise SystemExit(0 if status else 2)

if __name__=="__main__":
    main()
