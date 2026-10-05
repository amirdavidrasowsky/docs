# Historic sample match (reference-plaque reconstruction)

This variant was created from the photographed historic plaque reference supplied in the plaque-design conversation. The reference plaque itself appears to have been manufactured around 2015; the engraved/printed dates shown on it are not its production date.

## What was matched

The fixed physical plaque geometry remains unchanged:

- 200 x 300 mm finished panel
- 5 mm clear acrylic/plastic
- 176 x 247 mm photograph
- 12 mm white margins left/right/top
- 41 mm bottom caption band
- 5.5 mm mounting holes
- hole centers 15.5 mm from each adjacent finished edge

The typography was re-tuned from the reference photograph rather than inherited from the earlier Noto Sans version.

Reference-derived visual targets in the 41 mm caption band:

- ordinary name body starts about 7.2 mm below the bottom of the photograph
- name visible body is about 9 mm tall
- visible gap between the name and date line is about 4.8 mm
- ordinary date-line body is about 5 mm tall
- date line ends about 13.7 mm above the finished bottom edge
- both lines are centered horizontally

## Reproducible type treatment

The closest reproducible match available in the rendering environment is a customized **Noto Serif Hebrew** treatment rather than Noto Sans Hebrew:

- name: 29 pt, Bold (700), 123% horizontal scale
- date: 16 pt, Medium (500), 112% horizontal scale
- name baseline: 272.70 mm from the top of the finished plaque
- date baseline: 284.90 mm from the top
- all final Hebrew lettering is exported to vector paths

This deliberately produces broader, flared Hebrew forms and a heavier name line, closer to the photographed historic plaque.

This is a visual reconstruction from a photograph, not a claim that the original 2015 plaque's font binary has been definitively identified. Perspective, camera distance, and the absence of a physical measurement scale in the reference image prevent a mathematically exact recovery of the original font metrics. The fixed plaque dimensions and caption band are known, so the reference proportions were mapped onto the 41 mm bottom band.

## QA

The production PDFs were rendered at 200 dpi and visually inspected. The following were confirmed:

- finished artwork page: 200 x 300 mm
- photo rectangle: x=12 mm, y=12 mm from top, 176 x 247 mm
- normal front-view Hebrew orientation correct
- mirrored second-surface artwork is actually mirrored
- fabrication overlay retains 5.5 mm holes at 15.5 mm center inset
- clean print-ready file contains no red drill marks

Exact output hashes are in `reference/historic_sample_match_2026-10-05.json`.
