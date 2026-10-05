#!/usr/bin/env bash
set -euo pipefail

PHOTO="${1:-assets/nir_dahan_portrait_original.png}"
FONT_DIR="${FONT_DIR:-./fonts}"

mkdir -p out

python src/render_plaque.py   --photo "$PHOTO"   --preset presets/noto_sans_hebrew_medium.json   --font-dir "$FONT_DIR"   --out-dir out/noto

python src/render_plaque.py   --photo "$PHOTO"   --preset presets/david_libre_regular.json   --font-dir "$FONT_DIR"   --out-dir out/david

python src/render_plaque.py   --photo "$PHOTO"   --preset presets/narkis_tam_medium_sim.json   --out-dir out/narkis
