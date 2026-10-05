#!/usr/bin/env python3
"""Basic PDF preflight for plaque artwork geometry."""
import argparse
from pathlib import Path
import fitz

PT_PER_MM = 72/25.4

def mm(v):
    return v / PT_PER_MM

ap = argparse.ArgumentParser()
ap.add_argument("pdf", type=Path, nargs="+")
args = ap.parse_args()

for p in args.pdf:
    d = fitz.open(p)
    page = d[0]
    w, h = mm(page.rect.width), mm(page.rect.height)
    ok = abs(w - 200) < 0.01 and abs(h - 300) < 0.01
    print(f"{p}: {w:.4f} x {h:.4f} mm  page_size_ok={ok}")
    imgs = page.get_images(full=True)
    if imgs:
        r = page.get_image_rects(imgs[0][0])[0]
        print(
            f"  photo rect top-origin mm: x={mm(r.x0):.4f}, y={mm(r.y0):.4f}, "
            f"w={mm(r.width):.4f}, h={mm(r.height):.4f}"
        )
