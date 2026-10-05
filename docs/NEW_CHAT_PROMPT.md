# Complete prompt for a new ChatGPT chat

Copy everything between `BEGIN PROMPT` and `END PROMPT` into a new chat.

---

BEGIN PROMPT

I need you to continue a memorial-plaque print-production project. The complete reproducibility source is in my GitHub repository:

`amirdavidrasowsky/docs`

Please use the connected GitHub integration to read the repository before doing any design work. Treat the repository files as the authoritative source of dimensions, source images, captions, historical output hashes, font presets, and reproduction code. In particular read:

- `README.md`
- `presets/plaque_spec.json`
- `presets/noto_sans_hebrew_medium.json`
- `presets/narkis_tam_medium_sim.json`
- `presets/david_libre_regular.json`
- `docs/REPRODUCTION.md`
- `docs/FONT_ALTERNATIVES.md`
- `reference/historical_artifacts.json`
- `src/render_plaque.py`
- the source-asset manifest under `assets/`

The project is a single clear-acrylic memorial plaque. Do not change the physical geometry unless I explicitly tell you to. The finished plaque is exactly 200 mm wide x 300 mm high, 5 mm clear acrylic/plastic. The photograph is exactly 176 x 247 mm, with white margins of 12 mm left, 12 mm right, 12 mm top, and 41 mm bottom. In bottom-left PDF coordinates the photo is at x=12 mm, y=41 mm, w=176 mm, h=247 mm.

The four mounting holes are 5.5 mm diameter. Each hole center is exactly 15.5 mm in from both adjacent finished edges. Centers from the bottom-left are (15.5,15.5), (184.5,15.5), (15.5,284.5), and (184.5,284.5) mm. The upper holes therefore overlap the photograph slightly; that is intentional.

The Hebrew caption text is fixed:

Name: `ניר דהן`

Date: `אפריל 2023 - אוקטובר 2025`

Both lines must be horizontally centered. The intended optical placement follows the photographed reference plaque: the text is visibly closer to the bottom of the photograph than to the bottom edge of the plaque. As a general target, the name is about 9 mm visibly high, the date about 5 mm visibly high, there is about a 6 mm visible gap from the photo to the name, and about a 4 mm visual gap between the two lines. Because font metrics vary, judge this from rendered glyph bounds, not just nominal point size.

The canonical source portrait is 1118 x 1536 px. The canonical crop is a centered horizontal crop to the 176:247 photo aspect ratio, producing 1094 x 1536 px; do not crop vertically for this source. Verify the source asset by SHA-256 against the manifest in the repository. If the binary source image is not present in the repo or connected object storage, ask me only to upload that source image; do not ask me to repeat any dimensions or caption text.

The plaque is intended for second-surface/reverse printing: print on the rear face of the clear acrylic and view through the front. Provide both a normal front-view PDF and a pre-mirrored PDF. The print shop must use exactly one mirroring step: either normal PDF + mirror in the RIP, or the pre-mirrored PDF as supplied, never both. Recommend an opaque white ink/backing layer behind the artwork so the white margins and photo density remain correct.

Existing font variants that must remain reproducible are:

1. Noto Sans Hebrew Medium. The historical front-view was created with ReportLab using Noto Sans Hebrew Medium for Hebrew and Noto Sans Medium for digits. The repository preset contains exact sizes/baselines and the deliberately reversed visual Hebrew strings required for pixel-identical reproduction. Do not "fix" the RTL implementation on the exact historical-reproduction path unless you intentionally create a new variant.

2. Narkis Tam Medium alternative. The available face was Narkiss Tam Regular, synthetically expanded with a small black stroke and converted to paths in Inkscape to simulate Medium/500. Use the exact tuned values in `presets/narkis_tam_medium_sim.json`. Do not redistribute the commercial/proprietary Narkiss Tam font binary; use a locally installed/licensed font. Convert final lettering to vector outlines so the print shop does not need the font.

3. David Libre Regular. Preserve its historical preset as another comparison point.

I now want to create additional font alternatives while preserving all physical geometry, photograph crop, holes, wording, second-surface workflow, and output packaging. For each new font alternative, produce the same deliverables:

- clean print-ready PDF, exactly 200 x 300 mm;
- normal front-view PDF;
- pre-mirrored second-surface PDF;
- fabrication overlay PDF showing 5.5 mm holes centered 15.5 mm from edges, clearly marked as reference only;
- production-specification PDF;
- 300-dpi preview PNG;
- print-shop notes TXT;
- ZIP containing the production set;
- a manifest with SHA-256 hashes and the exact font file/family/version used.

Before finalizing any new variant, render the PDFs to images and visually inspect them. Confirm the Hebrew is in the correct order, the date line is correct, the text is horizontally centered, there is no clipping, photo geometry is unchanged, holes are correct, and the mirrored file is actually mirrored. If possible, compare to the existing reference variants at the same DPI.

For new fonts, prefer vector-outline output when licensing allows local use but the printer may not have the font. Do not put font binaries into the repo unless I explicitly confirm redistribution is allowed; generally store only font names, source/license notes, and SHA-256 hashes. The repo `.gitignore` intentionally excludes font binaries.

If my connected Backblaze B2/S3 storage is available to you in this new chat, use it for large generated PDFs/ZIP archives when that reduces GitHub repository bloat. Keep source code, presets, documentation, manifests, and small source/reference images in GitHub. Never store B2 credentials in GitHub. If B2 is not actually available through your tools, say so and continue using the repository without pretending an upload occurred.

When I name a new font, first determine whether it is installed/available or whether I need to upload/provide a licensed font file. Then create a new preset, render the complete set, visually QA it, and update `amirdavidrasowsky/docs` with the preset, any generator improvements, reproducibility notes, and output manifest. Preserve the historical presets unchanged unless a genuine bug is documented separately.

Do not ask me to repeat any of the plaque dimensions or caption text; all of that is fixed above and in the repo. If you need a font binary that is not available, ask only for that font file or tell me exactly what installation is needed.

END PROMPT
