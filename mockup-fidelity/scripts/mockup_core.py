#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import hashlib, json, math
import numpy as np
from PIL import Image

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def parse_quad(s):
    pts = []
    for token in s.strip().split():
        x, y = token.split(",")
        pts.append((float(x), float(y)))
    if len(pts) != 4:
        raise ValueError("quad needs 4 points: TL TR BR BL")
    return pts

def _dist(a, b):
    return math.hypot(b[0]-a[0], b[1]-a[1])

def _bilinear(q, u, v):
    tl, tr, br, bl = [np.array(p, dtype=float) for p in q]
    p = (1-u)*(1-v)*tl + u*(1-v)*tr + u*v*br + (1-u)*v*bl
    return tuple(float(x) for x in p)

def contain_quad(q, source_aspect):
    top = _dist(q[0], q[1]); bottom = _dist(q[3], q[2])
    left = _dist(q[0], q[3]); right = _dist(q[1], q[2])
    target_aspect = max(1e-9, (top + bottom) / max(1e-9, left + right))
    if abs(target_aspect - source_aspect) / source_aspect < 0.01:
        return q
    if target_aspect > source_aspect:
        f = source_aspect / target_aspect
        u0, u1, v0, v1 = (1-f)/2, 1-(1-f)/2, 0, 1
    else:
        f = target_aspect / source_aspect
        u0, u1, v0, v1 = 0, 1, (1-f)/2, 1-(1-f)/2
    return [
        _bilinear(q, u0, v0), _bilinear(q, u1, v0),
        _bilinear(q, u1, v1), _bilinear(q, u0, v1)
    ]

def crop_for_cover(img, target_aspect):
    w, h = img.size
    src_aspect = w / h
    if abs(src_aspect - target_aspect) / src_aspect < 0.01:
        return img, [0, 0, w, h]
    if src_aspect > target_aspect:
        new_w = int(round(h * target_aspect))
        x0 = (w - new_w) // 2
        box = [x0, 0, x0 + new_w, h]
    else:
        new_h = int(round(w / target_aspect))
        y0 = (h - new_h) // 2
        box = [0, y0, w, y0 + new_h]
    return img.crop(tuple(box)), box

def _perspective_coeffs(out_pts, in_pts):
    A, B = [], []
    for (x, y), (u, v) in zip(out_pts, in_pts):
        A.append([x, y, 1, 0, 0, 0, -u*x, -u*y]); B.append(u)
        A.append([0, 0, 0, x, y, 1, -v*x, -v*y]); B.append(v)
    coeffs = np.linalg.solve(np.asarray(A, float), np.asarray(B, float))
    return tuple(float(x) for x in coeffs)

def warp_artwork(artwork, canvas_size, quad):
    artwork = artwork.convert("RGBA")
    w, h = artwork.size
    src = [(0,0), (w-1,0), (w-1,h-1), (0,h-1)]
    coeffs = _perspective_coeffs(quad, src)
    return artwork.transform(
        canvas_size,
        Image.Transform.PERSPECTIVE,
        coeffs,
        resample=Image.Resampling.BICUBIC,
        fillcolor=(0,0,0,0)
    )

def apply_lighting(base, warped, strength):
    base = base.convert("RGBA")
    w = np.asarray(warped.convert("RGBA")).astype(np.float32)
    b = np.asarray(base.convert("RGB")).astype(np.float32)
    alpha = w[...,3] / 255.0
    region = alpha > 0.05
    if not np.any(region) or strength <= 0:
        return warped.convert("RGBA")
    gray = 0.2126*b[...,0] + 0.7152*b[...,1] + 0.0722*b[...,2]
    med = float(np.median(gray[region]))
    med = max(med, 1.0)
    factor = 1.0 + float(strength) * (gray / med - 1.0)
    factor = np.clip(factor, 0.72, 1.28)
    out = w.copy()
    out[...,:3] = np.clip(out[...,:3] * factor[...,None], 0, 255)
    return Image.fromarray(out.astype(np.uint8), "RGBA")

def render(base_path, artwork_path, quad, fit="contain", fidelity="general", lighting_strength=None):
    base = Image.open(base_path).convert("RGBA")
    art0 = Image.open(artwork_path).convert("RGBA")
    q0 = [tuple(map(float,p)) for p in quad]
    top = _dist(q0[0], q0[1]); bottom = _dist(q0[3], q0[2])
    left = _dist(q0[0], q0[3]); right = _dist(q0[1], q0[2])
    target_aspect = (top + bottom) / max(1e-9, left + right)
    crop_box = None
    if fit == "contain":
        art = art0
        q = contain_quad(q0, art.width / art.height)
    elif fit == "cover":
        art, crop_box = crop_for_cover(art0, target_aspect)
        q = q0
    else:
        raise ValueError("fit must be contain or cover")
    warped = warp_artwork(art, base.size, q)
    if lighting_strength is None:
        lighting_strength = 0.32 if fidelity == "general" else 0.22
    presentation = apply_lighting(base, warped, lighting_strength)
    mockup = Image.alpha_composite(base, presentation)
    return {
        "base": base, "artwork_used": art, "warped": warped,
        "presentation": presentation, "mockup": mockup,
        "quad_requested": q0, "quad_used": q, "crop_box": crop_box,
        "lighting_strength": float(lighting_strength),
    }
