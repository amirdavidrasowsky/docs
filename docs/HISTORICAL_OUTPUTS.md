# Historical output sets

This file records the finished variants created during the originating plaque-design conversation.

## Noto Sans Hebrew Medium

Production set:

- print-ready artwork
- normal front-view artwork
- pre-mirrored second-surface artwork
- fabrication overlay with 5.5 mm holes at 15.5 mm inset
- production specification

Key historical hashes are stored in `reference/historical_artifacts.json`.

Important implementation detail: the Noto front view uses 33 pt name text and 17 pt date text. The historical fabrication overlay uniquely used an 18 pt date line; the preset preserves that behavior for exact regression reproduction.

## Narkis Tam Medium alternative

Production set:

- print-ready artwork
- normal front-view artwork
- pre-mirrored second-surface artwork
- fabrication overlay
- production specification
- 300-dpi preview
- print-shop notes

The lettering was created from Narkiss Tam Regular, synthetically expanded with a small black stroke, and converted to vector paths in Inkscape. The font binary is not redistributed.

## David Libre Regular

Earlier production set:

- print-ready artwork
- fabrication overlay
- production guide
- 300-dpi preview

The David Libre version placed the caption block lower in the 41 mm bottom band than the later reference-matched versions. Preserve it as a historical comparison rather than using its vertical placement as the default for new alternatives.

## Second-surface workflow

The normal front-view PDF and the pre-mirrored PDF are alternate production inputs. Use exactly one mirroring operation. The clean print-ready PDF must never include red fabrication marks.
