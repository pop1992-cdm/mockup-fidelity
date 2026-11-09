#!/usr/bin/env python3
from pathlib import Path
import argparse, json
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from mockup_core import parse_quad

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--original", required=True)
    p.add_argument("--cleaned", required=True)
    p.add_argument("--quad", required=True)
    p.add_argument("--fidelity", choices=["general","high"], default="general")
    p.add_argument("--report", default="substrate_verification.json")
    a=p.parse_args()

    x=Image.open(a.original).convert("RGB")
    y=Image.open(a.cleaned).convert("RGB")
    if x.size != y.size:
        report={"status":"FAIL","reason":"dimension mismatch","original_size":x.size,"cleaned_size":y.size}
        Path(a.report).write_text(json.dumps(report,indent=2))
        print(json.dumps(report,indent=2)); raise SystemExit(2)

    xb=np.asarray(x.filter(ImageFilter.GaussianBlur(1))).astype(np.int16)
    yb=np.asarray(y.filter(ImageFilter.GaussianBlur(1))).astype(np.int16)
    mask=Image.new("L",x.size,0)
    d=ImageDraw.Draw(mask)
    q=parse_quad(a.quad)
    cx=sum(p[0] for p in q)/4; cy=sum(p[1] for p in q)/4
    scale=1.12
    q2=[(cx+(px-cx)*scale, cy+(py-cy)*scale) for px,py in q]
    d.polygon(q2,fill=255)
    outside=np.asarray(mask)==0
    diff=np.mean(np.abs(xb-yb),axis=2)
    mae=float(np.mean(diff[outside])) if np.any(outside) else 0.0
    changed=float(np.mean(diff[outside] > 20)) if np.any(outside) else 0.0
    if a.fidelity=="high":
        ok=mae<=3 and changed<=0.05
    else:
        ok=mae<=6 and changed<=0.10
    report={"status":"PASS" if ok else "FAIL","outside_mae":round(mae,3),"outside_changed_fraction":round(changed,4)}
    Path(a.report).write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))
    raise SystemExit(0 if ok else 2)

if __name__=="__main__":
    main()
