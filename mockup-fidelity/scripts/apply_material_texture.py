#!/usr/bin/env python3
"""
Add subtle deterministic substrate texture to a blank/clean material image.
Use before artwork compositing. Never use this script on the final mockup.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter

PRESETS = {
    "uncoated-cardstock": dict(grain=1.35, lowfreq=2.2, warm=1.0),
    "coated-paper": dict(grain=0.55, lowfreq=0.7, warm=0.3),
    "ivory-card": dict(grain=1.10, lowfreq=1.6, warm=2.2),
    "cotton-paper": dict(grain=1.75, lowfreq=2.6, warm=0.8),
    "recycled-paper": dict(grain=2.05, lowfreq=3.0, warm=1.7),
    "matte-paper": dict(grain=0.85, lowfreq=1.0, warm=0.5),
}

def make_noise(h, w, rng, blur_radius):
    small_h = max(8, h // 8)
    small_w = max(8, w // 8)
    a = rng.normal(127.5, 32.0, (small_h, small_w)).clip(0,255).astype(np.uint8)
    im = Image.fromarray(a, "L").resize((w,h), Image.Resampling.BICUBIC)
    if blur_radius > 0:
        im = im.filter(ImageFilter.GaussianBlur(blur_radius))
    return (np.asarray(im).astype(np.float32) - 127.5) / 127.5

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--material", choices=sorted(PRESETS), default="uncoated-cardstock")
    p.add_argument("--strength", type=float, default=0.32)
    p.add_argument("--seed", type=int, default=41)
    a = p.parse_args()

    src = Image.open(a.input).convert("RGBA")
    arr = np.asarray(src).astype(np.float32)
    h,w = arr.shape[:2]
    cfg = PRESETS[a.material]
    rng = np.random.default_rng(a.seed)

    fine = rng.normal(0, 1.0, (h,w)).astype(np.float32)
    low = make_noise(h,w,rng,1.2)
    delta = a.strength * (cfg["grain"] * fine + cfg["lowfreq"] * low)
    rgb = arr[...,:3]
    rgb += delta[...,None]
    if cfg["warm"]:
        rgb[...,0] += a.strength * cfg["warm"] * 0.45
        rgb[...,2] -= a.strength * cfg["warm"] * 0.28
    arr[...,:3] = np.clip(rgb, 0, 255)
    Image.fromarray(arr.astype(np.uint8), "RGBA").save(a.output)
    print(a.output)

if __name__ == "__main__":
    main()
