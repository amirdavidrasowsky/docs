# Reproduction guide

## Physical artwork geometry

The finished plaque is exactly **200 x 300 mm** in portrait orientation. The artwork is a white 200 x 300 mm page/panel with a photograph inset from the edges and a two-line Hebrew caption in the bottom white band.

- Panel: 200 x 300 mm.
- Material: 5 mm clear acrylic / clear plastic.
- Photo: 176 x 247 mm.
- Photo placement: 12 mm from the left, 12 mm from the right, 12 mm from the top, leaving a 41 mm bottom caption band.
- In bottom-left PDF coordinates, the photo rectangle is x=12 mm, y=41 mm, w=176 mm, h=247 mm.
- Name: `ניר דהן`.
- Date: `אפריל 2023 - אוקטובר 2025`.
- Both caption lines are horizontally centered.
- Hole diameter: 5.5 mm.
- Hole-center inset: 15.5 mm from each adjacent finished edge.
- Hole centers from bottom-left: (15.5,15.5), (184.5,15.5), (15.5,284.5), (184.5,284.5) mm.

The top two holes overlap the photograph because their centers are 15.5 mm from the top and the photo starts 12 mm from the top. This is intentional.

## Source portrait and crop

`assets/nir_dahan_portrait_original.png` is 1118 x 1536 pixels. The print crop is a centered horizontal crop to the physical photo aspect ratio 176/247. For the supplied source, that removes 12 pixels from each side and produces 1094 x 1536 pixels. No vertical crop is applied.

Do not resize the crop before placing it into the PDF. Place the crop into the 176 x 247 mm photo rectangle; effective raster resolution is about 158 ppi, matching the historical PDFs.

## Noto Sans Hebrew Medium historical rendering

The Noto version was produced with ReportLab. It uses `NotoSansHebrew-Medium.ttf` for Hebrew and `NotoSans-Medium.ttf` for digits. Because the historical renderer positioned Hebrew glyphs with ReportLab's basic left-to-right text operators, the source strings are explicitly reversed for visual RTL output. Do not enable shaping on this exact-reproduction path.

Exact front-view metrics:

- Name: 33 pt.
- Name baseline: 27.944445 mm from bottom.
- Date: 17 pt.
- Date baseline: 17.241668 mm from bottom.
- Name visual string sent to ReportLab: `ןהד רינ`.
- Date left-to-right drawing sequence: `2025`, space, `רבוטקוא`, space, `-`, space, `2023`, space, `לירפא`.

The historical Noto fabrication-overlay PDF accidentally/uniquely used an 18 pt date line on a 16.888890 mm baseline. The preset retains this only so the old overlay can be recreated exactly. For a new consistent overlay, disable `reproduce_legacy_caption_difference` and use the normal 17 pt date settings.

The clean front-view and print-ready Noto files are visually identical. The mirrored file wraps the entire clean artwork in a horizontal mirror transform.

## Narkis Tam Medium alternative historical rendering

The available licensed outline was `Narkiss Tam Regular`. The historical "Medium" alternative simulated a slightly heavier weight by using a small black outline stroke and then converting the text to paths in Inkscape 1.4.

Reconstruction parameters:

- Font family: `Narkiss Tam` / Regular.
- Name size: approximately 35 pt (the tuned preset uses 35.007 pt to match the historical render).
- Date size: approximately 16 pt (the tuned preset uses 15.987 pt).
- Name baseline in SVG top-origin coordinates: 271.698 mm.
- Date baseline in SVG top-origin coordinates: 282.4005 mm.
- Name stroke expansion: 0.13 mm, black.
- Date stroke expansion: 0.094 mm, black.
- Text anchor: center at x=100 mm.
- Direction: RTL.
- Export text to paths. The print shop does not need the font.

Measured historical path bounding boxes in top-origin millimeters:

- Name: x=84.994..115.117, y=265.278..273.861.
- Date: x=69.894..130.157, y=278.507..283.386.

This puts the caption visibly closer to the photograph than to the bottom edge, matching the photographed reference plaque.

## David Libre historical rendering

A prior alternative used David Libre Regular:

- Name: 34 pt, baseline 23.029168 mm from bottom.
- Date: 16 pt, baseline 12.326387 mm from bottom.
- The text block sits lower/more vertically centered in the 41 mm caption band than the later reference-matched Noto/Narkis variants.

## Second-surface printing

The artwork is intended for printing on the rear face of the clear 5 mm acrylic and viewing through the front. This protects the ink from scratches.

Use exactly one mirroring step:

1. Use the normal front-view/print-ready PDF and tell the RIP/printer to mirror for second-surface printing, **or**
2. Use the supplied `second_surface_MIRRORED` PDF as-is when the printer expects pre-mirrored artwork.

Do not mirror both in the file and again in the RIP. Use an opaque white ink/backing layer behind the whole image/text area (or the shop's equivalent white backer) so the white border remains opaque and the photograph retains density.

## Running the renderer

Create a Python environment and install:

```bash
python -m pip install -r src/requirements.txt
```

Install Inkscape 1.4 or compatible for the outline-based backend.

Fonts are intentionally not stored in this repository. Put required TTF files into a local `fonts/` directory for ReportLab presets. For Narkiss Tam, install your licensed font in the OS/fontconfig so `fc-match "Narkiss Tam"` finds it.

Examples:

```bash
python src/render_plaque.py \
  --photo assets/nir_dahan_portrait_original.png \
  --preset presets/noto_sans_hebrew_medium.json \
  --font-dir ./fonts \
  --out-dir out/noto

python src/render_plaque.py \
  --photo assets/nir_dahan_portrait_original.png \
  --preset presets/narkis_tam_medium_sim.json \
  --out-dir out/narkis
```

Each run produces a cropped source image, clean front-view PDF, print-ready PDF, pre-mirrored second-surface PDF, fabrication overlay, production-spec PDF, 300-dpi preview PNG, print-shop notes, ZIP package, and SHA-256 manifest.

## Visual QA

Always render the front-view PDF and inspect it before sending to the printer. Verify:

- page is exactly 200 x 300 mm;
- photo is 176 x 247 mm and starts 12 mm from the top/left/right;
- no photo distortion;
- Hebrew reads `ניר דהן` and `אפריל 2023 - אוקטובר 2025` in the normal front-view PDF;
- caption is centered horizontally;
- mirrored file is actually mirrored and is used only once in the print workflow;
- hole circles are 5.5 mm diameter and centered 15.5 mm from the edges;
- clean print-ready file has no red drilling marks.

For a strict regression test, render historical and reconstructed PDFs at the same DPI and compare pixels. The Noto front-view preset has been verified pixel-identical at 200 dpi with the reference font hashes listed in the preset.
