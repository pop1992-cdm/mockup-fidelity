#!/usr/bin/env python3
from pathlib import Path
import argparse, json
from PIL import Image
from mockup_core import parse_quad, render, sha256_file

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--base", required=True)
    p.add_argument("--artwork", required=True)
    p.add_argument("--quad", required=True, help='TL TR BR BL, e.g. "100,100 500,110 490,400 110,390"')
    p.add_argument("--fit", choices=["contain","cover"], default="contain")
    p.add_argument("--fidelity", choices=["general","high"], default="general")
    p.add_argument("--lighting-strength", type=float, default=None)
    p.add_argument("--out-dir", required=True)
    a = p.parse_args()
    out = Path(a.out_dir); out.mkdir(parents=True, exist_ok=True)
    q = parse_quad(a.quad)
    r = render(a.base, a.artwork, q, a.fit, a.fidelity, a.lighting_strength)

    r["mockup"].save(out/"mockup.png")
    r["warped"].save(out/"warped_artwork.png")
    r["presentation"].save(out/"presentation_artwork.png")
    r["warped"].getchannel("A").save(out/"mask.png")

    manifest = {
        "version": 1,
        "base_path": str(Path(a.base).resolve()),
        "base_sha256": sha256_file(a.base),
        "artwork_path": str(Path(a.artwork).resolve()),
        "artwork_sha256": sha256_file(a.artwork),
        "base_size": list(r["base"].size),
        "artwork_size": list(Image.open(a.artwork).size),
        "quad_requested": r["quad_requested"],
        "quad_used": r["quad_used"],
        "fit": a.fit,
        "fidelity": a.fidelity,
        "crop_box": r["crop_box"],
        "lighting_strength": r["lighting_strength"],
        "content_layer_policy": "locked-source-derived",
        "presentation_layer_policy": "luminance-only",
    }
    (out/"manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(out/"mockup.png")

if __name__ == "__main__":
    main()
