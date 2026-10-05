# Adding font alternatives

The geometry must not move when comparing fonts. Change only the typography preset unless there is a deliberate optical-spacing adjustment.

## Preferred workflow

1. Duplicate the closest preset in `presets/`.
2. Keep the panel/photo/hole geometry in `presets/plaque_spec.json` unchanged.
3. Choose a backend:
   - `reportlab` for TTF fonts when exact font-file loading is desired.
   - `inkscape` for CFF/OpenType fonts, commercial fonts installed in the OS, or when all text should be converted to vector outlines.
4. Render the front-view PDF and 300-dpi preview.
5. Measure visible glyph height and compare the vertical spacing to `assets/reference_plaque_typography.jpg`.
6. Keep both lines centered at x=100 mm.
7. Generate the normal, mirrored, and fabrication files from the same preset.

## Optical targets from the reference plaque

The intended appearance is approximately:

- name visible height: 9 mm;
- date visible height: 5 mm;
- visible gap from photograph to top of name: about 6 mm;
- visible gap between name and date: about 4 mm;
- appreciably more white space below the date than above the name.

Font metrics differ, so equal point sizes do not produce equal visible heights. For a new font, adjust point size and baseline together based on rendered glyph bounds, not solely on nominal point size.

## Suggested alternatives to try

Useful Hebrew faces to compare include Narkis Tam, Narkisim/Narkis, David/David Libre, Frank Ruhl Libre, Noto Serif Hebrew, Noto Sans Hebrew, Miriam Libre, and other licensed memorial/official Hebrew serif faces. Do not redistribute commercial font binaries in this repository.

## Inkscape outline method

For an installed font, set `backend` to `inkscape`, set `font.family`, and specify name/date point sizes plus top-origin baselines. Optional `name_stroke_width_mm` and `date_stroke_width_mm` can create a controlled synthetic weight. The renderer exports with `--export-text-to-path`, so the resulting PDF is printer-safe even when the shop lacks the font.

## ReportLab exact-reproduction method

For TTF fonts, `backend=reportlab` loads font files directly. The legacy Hebrew visual strings in `plaque_spec.json` are reversed intentionally. This is required to reproduce the historical files made with unshaped ReportLab text operators. If you build a new renderer using HarfBuzz/Pango shaping, use the logical Hebrew strings instead and do not also reverse them.
