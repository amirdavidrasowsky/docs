# Nir Dahan memorial plaque - reproducible print artwork

This repository contains the exact physical specifications, typography presets, historical-output hashes, source-code renderer, and handoff documentation needed to recreate the 200 x 300 mm Nir Dahan memorial plaque artwork and produce additional font alternatives without changing the plaque geometry.

## Fixed specification

- Finished panel: **200 x 300 mm** portrait.
- Material: **5 mm clear acrylic/plastic**.
- Photograph: **176 x 247 mm**.
- White margins: **12 mm left/right/top, 41 mm bottom**.
- Caption: `ניר דהן` and `אפריל 2023 - אוקטובר 2025`.
- Holes: **5.5 mm diameter**, centers **15.5 mm** from each adjacent edge.
- Printing: second-surface/reverse print on the rear face, viewed through the front.

## Repository map

- `assets/` - source-asset manifest and hashes.
- `presets/plaque_spec.json` - immutable physical geometry and caption text.
- `presets/noto_sans_hebrew_medium.json` - exact historical Noto preset.
- `presets/narkis_tam_medium_sim.json` - tuned Narkis Tam Medium alternative preset.
- `presets/david_libre_regular.json` - historical David Libre preset.
- `src/render_plaque.py` - renderer for clean, mirrored, fabrication, preview, spec, notes, ZIP, and manifest outputs.
- `src/verify_geometry.py` - PDF page/photo geometry preflight.
- `docs/REPRODUCTION.md` - full technical reconstruction notes.
- `docs/FONT_ALTERNATIVES.md` - how to add new fonts without moving the plaque geometry.
- `docs/B2_STORAGE.md` - recommended Backblaze B2 layout for large generated binaries.
- `docs/NEW_CHAT_PROMPT.md` - complete prompt for handing the project to a fresh ChatGPT conversation.
- `reference/historical_artifacts.json` - SHA-256 hashes and historical-output validation notes.

## Source-asset status

The current ChatGPT session had the exact source portrait and reference-plaque photograph, but the GitHub connector exposed here does not support uploading arbitrary local binary files, and no Backblaze B2/S3 connector was exposed. Therefore the binary images are **not falsely claimed as uploaded**. Their exact filenames, dimensions, and SHA-256 hashes are recorded under `assets/` and `reference/historical_artifacts.json`.

A complete downloadable handoff bundle containing those binaries is generated in the originating chat. Once those two files are added to `assets/` (or uploaded to B2 and referenced by manifest), the repository is fully self-contained for recreation.

Expected source files:

- `assets/nir_dahan_portrait_original.png` - 1118 x 1536 px - SHA-256 `2bbdf94550fb3c907479647e3cfdcf4090cca6c6285f5e39d7d952bcea251c4f`
- `assets/reference_plaque_typography.jpg` - 1536 x 1152 px - SHA-256 `07eac106b62dd80d31eb7f035c7e5513d964efa7eb09786b84b28676c9b13ec8`

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

Keep code/specs/presets/manifests in GitHub. Use Backblaze B2 for large generated PDFs/ZIPs if a B2/S3 integration is actually available. Never store B2 credentials in GitHub. This session did not have a B2 connector, so no B2 upload is claimed.

## Font licensing

Font binaries are intentionally excluded. Noto Sans and David Libre can be obtained under their respective open licenses. Narkiss Tam may be commercial/proprietary; use a licensed local installation and do not redistribute it from this repo.
