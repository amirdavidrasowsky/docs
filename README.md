# Nir Dahan memorial plaque - reproducible print artwork

This repository contains the source assets, exact physical specifications, typography presets, and generator needed to recreate the 200 x 300 mm Nir Dahan memorial plaque artwork and produce additional font alternatives without changing the plaque geometry.

## Fixed specification

- Finished panel: **200 x 300 mm** portrait.
- Material: **5 mm clear acrylic/plastic**.
- Photograph: **176 x 247 mm**.
- White margins: **12 mm left/right/top, 41 mm bottom**.
- Caption: `ניר דהן` and `אפריל 2023 - אוקטובר 2025`.
- Holes: **5.5 mm diameter**, centers **15.5 mm** from each adjacent edge.
- Printing: second-surface/reverse print on the rear face, viewed through the front.

## Repository map

- `assets/` - original portrait and photographed typography/spacing reference.
- `presets/plaque_spec.json` - immutable physical geometry and caption text.
- `presets/noto_sans_hebrew_medium.json` - exact historical Noto preset.
- `presets/narkis_tam_medium_sim.json` - exact/tuned Narkis Tam Medium alternative preset.
- `presets/david_libre_regular.json` - historical David Libre preset.
- `src/render_plaque.py` - renderer for clean, mirrored, fabrication, preview, spec, notes, ZIP, and manifest outputs.
- `src/verify_geometry.py` - PDF page/photo geometry preflight.
- `docs/REPRODUCTION.md` - full technical reconstruction notes.
- `docs/FONT_ALTERNATIVES.md` - how to add new fonts without moving the plaque geometry.
- `docs/B2_STORAGE.md` - recommended Backblaze B2 layout for large generated binaries.
- `docs/NEW_CHAT_PROMPT.md` - complete prompt for handing the project to a fresh ChatGPT conversation.
- `reference/historical_artifacts.json` - SHA-256 hashes and historical-output validation notes.

## Quick start

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r src/requirements.txt
```

Fonts are not bundled. Place required TTF files under a local `fonts/` directory (ignored by Git) or install the font in the OS when using the Inkscape backend.

Noto example:

```bash
python src/render_plaque.py \
  --photo assets/nir_dahan_portrait_original.png \
  --preset presets/noto_sans_hebrew_medium.json \
  --font-dir ./fonts \
  --out-dir out/noto
```

Narkiss Tam example (requires licensed `Narkiss Tam` installed and Inkscape available):

```bash
python src/render_plaque.py \
  --photo assets/nir_dahan_portrait_original.png \
  --preset presets/narkis_tam_medium_sim.json \
  --out-dir out/narkis
```

See `docs/REPRODUCTION.md` before sending anything to a printer.

## Storage policy

Source code/specs/presets and the two small source images are kept in GitHub. Large generated PDFs/ZIPs do not need to be committed because the repository can reproduce them. If a connected Backblaze B2/S3 integration is available in a future session, use B2 for large generated archives and record object keys + hashes in a GitHub manifest. The ChatGPT session that initialized this repo did **not** expose a Backblaze B2 connector, so no B2 upload is claimed here.

## Font licensing

Font binaries are intentionally excluded. Noto Sans and David Libre can be obtained under their respective open licenses. Narkiss Tam may be commercial/proprietary; use a licensed local installation and do not redistribute it from this repo.
