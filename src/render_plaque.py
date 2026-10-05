#!/usr/bin/env python3
"""Rebuild the Nir Dahan 200 x 300 mm memorial plaque artwork.

Backends:
- reportlab: exact legacy reconstruction for Noto Sans Hebrew Medium / David Libre TTF files.
- inkscape: vector-outline workflow for Narkiss Tam and arbitrary installed fonts.

The clean artwork PDFs contain no drill marks. A separate fabrication-overlay PDF
shows the 5.5 mm holes and crosshairs. The mirrored PDF is for second-surface
printing when the print shop does NOT mirror in its RIP.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import shutil
import subprocess
import textwrap
import zipfile
from pathlib import Path

from PIL import Image
import fitz
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "presets" / "plaque_spec.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def hex_rgb(value: str):
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


def resolve_font(filename: str | None, font_dir: Path | None) -> Path | None:
    if not filename:
        return None
    p = Path(filename)
    if p.is_file():
        return p
    candidates = []
    if font_dir:
        candidates.append(font_dir / filename)
    candidates += [
        Path("/usr/share/fonts/truetype/noto") / filename,
        Path("/usr/share/fonts/truetype") / filename,
        Path.home() / ".local/share/fonts" / filename,
    ]
    for c in candidates:
        if c.is_file():
            return c
    return None


def crop_photo(src: Path, dst: Path, spec: dict) -> None:
    """Center-crop to the physical photo aspect ratio, preserving full height when possible."""
    with Image.open(src) as im:
        im = im.convert("RGB")
        target_aspect = spec["photo_width_mm"] / spec["photo_height_mm"]
        w, h = im.size
        aspect = w / h
        if abs(aspect - target_aspect) < 1e-8:
            crop = im
        elif aspect > target_aspect:
            new_w = round(h * target_aspect)
            left = (w - new_w) // 2
            crop = im.crop((left, 0, left + new_w, h))
        else:
            new_h = round(w / target_aspect)
            top = (h - new_h) // 2
            crop = im.crop((0, top, w, top + new_h))
        dst.parent.mkdir(parents=True, exist_ok=True)
        crop.save(dst, "PNG", optimize=False)


def register_font(alias: str, path: Path) -> None:
    if alias not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont(alias, str(path)))


def draw_reportlab_caption(
    c: canvas.Canvas,
    spec: dict,
    preset: dict,
    heb_alias: str,
    lat_alias: str,
    fabrication: bool = False,
) -> None:
    name_size = float(preset["name_font_size_pt"])
    date_size = float(preset["date_font_size_pt"])
    name_baseline = float(preset["name_baseline_from_bottom_mm"]) * mm
    date_baseline = float(preset["date_baseline_from_bottom_mm"]) * mm

    if fabrication:
        fab = preset.get("fabrication_overlay", {})
        if fab.get("reproduce_legacy_caption_difference"):
            date_size = float(fab.get("date_font_size_pt", date_size))
            date_baseline = float(
                fab.get("date_baseline_from_bottom_mm", date_baseline / mm)
            ) * mm

    c.setFillColorRGB(0, 0, 0)

    # ReportLab's basic text renderer is LTR. The supplied strings are pre-reversed
    # so the visual result is correct Hebrew when read right-to-left.
    visual_name = spec["name_he_visual_ltr_for_reportlab"]
    c.setFont(heb_alias, name_size)
    name_w = pdfmetrics.stringWidth(visual_name, heb_alias, name_size)
    c.drawString(100 * mm - name_w / 2, name_baseline, visual_name)

    segments = spec["date_visual_segments_ltr_for_reportlab"]
    widths = []
    for seg in segments:
        alias = heb_alias if seg["script"] == "hebrew" else lat_alias
        widths.append(pdfmetrics.stringWidth(seg["text"], alias, date_size))

    x = 100 * mm - sum(widths) / 2
    for seg, width in zip(segments, widths):
        alias = heb_alias if seg["script"] == "hebrew" else lat_alias
        c.setFont(alias, date_size)
        c.drawString(x, date_baseline, seg["text"])
        x += width


def draw_reportlab_base(
    c: canvas.Canvas,
    photo: Path,
    spec: dict,
    preset: dict,
    heb_alias: str,
    lat_alias: str,
    mirrored: bool = False,
    fabrication: bool = False,
) -> None:
    pw = spec["finished_width_mm"] * mm
    ph = spec["finished_height_mm"] * mm

    c.saveState()
    if mirrored:
        c.translate(pw, 0)
        c.scale(-1, 1)

    c.setFillColorRGB(1, 1, 1)
    c.rect(0, 0, pw, ph, stroke=0, fill=1)

    c.drawImage(
        str(photo),
        spec["photo_x_mm"] * mm,
        spec["photo_y_from_bottom_mm"] * mm,
        width=spec["photo_width_mm"] * mm,
        height=spec["photo_height_mm"] * mm,
        mask="auto",
    )

    draw_reportlab_caption(
        c,
        spec,
        preset,
        heb_alias,
        lat_alias,
        fabrication=fabrication,
    )
    c.restoreState()

    if fabrication:
        draw_reportlab_holes(c, spec, preset)


def draw_reportlab_holes(c: canvas.Canvas, spec: dict, preset: dict) -> None:
    fab = preset.get("fabrication_overlay", {})
    rgb = hex_rgb(fab.get("stroke_color", "#d32222"))
    c.setStrokeColorRGB(*rgb)

    if "stroke_width_pt" in fab:
        c.setLineWidth(float(fab["stroke_width_pt"]))
    else:
        c.setLineWidth(float(fab.get("stroke_width_mm", 0.35)) * mm)

    radius = spec["hole_diameter_mm"] * mm / 2
    half_cross = float(fab.get("crosshair_total_length_mm", 8.0)) * mm / 2

    for x_mm, y_mm in spec["hole_centers_from_bottom_left_mm"]:
        x, y = x_mm * mm, y_mm * mm
        c.circle(x, y, radius, stroke=1, fill=0)
        c.line(x - half_cross, y, x + half_cross, y)
        c.line(x, y - half_cross, x, y + half_cross)

    footer = fab.get("footer_text")
    if footer:
        c.setFillColorRGB(*rgb)
        font_name = "LATIN"
        if font_name not in pdfmetrics.getRegisteredFontNames():
            font_name = "Helvetica"
        c.setFont(font_name, float(fab.get("footer_font_size_pt", 5.5)))
        y = float(fab.get("footer_baseline_from_bottom_mm", 1.8)) * mm
        c.drawCentredString(100 * mm, y, footer)


def render_reportlab_pdf(
    out: Path,
    photo: Path,
    spec: dict,
    preset: dict,
    font_dir: Path | None,
    mirrored: bool = False,
    fabrication: bool = False,
) -> None:
    heb = resolve_font(preset["font"].get("hebrew_file"), font_dir)
    lat = resolve_font(preset["font"].get("latin_file"), font_dir) or heb

    if not heb or not lat:
        raise FileNotFoundError(
            "Required font file(s) not found. "
            f"Hebrew={preset['font'].get('hebrew_file')} "
            f"Latin={preset['font'].get('latin_file')}. Use --font-dir."
        )

    register_font("HEBREW", heb)
    register_font("LATIN", lat)

    c = canvas.Canvas(
        str(out),
        pagesize=(
            spec["finished_width_mm"] * mm,
            spec["finished_height_mm"] * mm,
        ),
    )
    draw_reportlab_base(
        c,
        photo,
        spec,
        preset,
        "HEBREW",
        "LATIN",
        mirrored=mirrored,
        fabrication=fabrication,
    )
    c.showPage()
    c.save()


def svg_image_data_uri(path: Path) -> str:
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    return (
        f"data:{mime};base64,"
        + base64.b64encode(path.read_bytes()).decode("ascii")
    )


def make_inkscape_svg(
    photo: Path,
    spec: dict,
    preset: dict,
    mirrored: bool = False,
    fabrication: bool = False,
) -> str:
    family = preset["font"]["family"]
    name_size_mm = float(preset["name_font_size_pt"]) * 25.4 / 72.0
    date_size_mm = float(preset["date_font_size_pt"]) * 25.4 / 72.0
    name_y = float(preset["name_baseline_from_top_mm"])
    date_y = float(preset["date_baseline_from_top_mm"])
    name_stroke = float(preset.get("name_stroke_width_mm", 0.0))
    date_stroke = float(preset.get("date_stroke_width_mm", 0.0))
    fill = preset.get("fill_color", "#000000")
    stroke = preset.get("stroke_color", fill)

    photo_y_top = (
        spec["finished_height_mm"]
        - spec["photo_y_from_bottom_mm"]
        - spec["photo_height_mm"]
    )

    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" '
        'width="200mm" height="300mm" viewBox="0 0 200 300">',
        '<rect x="0" y="0" width="200" height="300" fill="white"/>',
    ]

    if mirrored:
        parts.append('<g transform="translate(200 0) scale(-1 1)">')

    parts.append(
        f'<image x="{spec["photo_x_mm"]}" y="{photo_y_top}" '
        f'width="{spec["photo_width_mm"]}" height="{spec["photo_height_mm"]}" '
        f'preserveAspectRatio="none" href="{svg_image_data_uri(photo)}"/>'
    )

    def text_svg(text, y, size_mm, stroke_mm):
        stroke_attrs = (
            f' stroke="{stroke}" stroke-width="{stroke_mm}" '
            'paint-order="stroke fill"'
            if stroke_mm
            else ""
        )
        return (
            f'<text x="100" y="{y}" text-anchor="middle" '
            f'font-family="{family}" font-size="{size_mm}" '
            'direction="rtl" unicode-bidi="bidi-override" '
            f'fill="{fill}"{stroke_attrs}>{text}</text>'
        )

    parts.append(
        text_svg(
            spec["name_he"],
            name_y,
            name_size_mm,
            name_stroke,
        )
    )
    parts.append(
        text_svg(
            spec["date_he"],
            date_y,
            date_size_mm,
            date_stroke,
        )
    )

    if mirrored:
        parts.append("</g>")

    if fabrication:
        fab = preset.get("fabrication_overlay", {})
        color = fab.get("stroke_color", "#d32222")
        width = float(fab.get("stroke_width_mm", 0.35))
        half = float(fab.get("crosshair_total_length_mm", 8.0)) / 2.0
        radius = spec["hole_diameter_mm"] / 2.0

        # SVG y is top-down, so convert from bottom-left coordinates.
        for x, y_bottom in spec["hole_centers_from_bottom_left_mm"]:
            y = spec["finished_height_mm"] - y_bottom
            parts.append(
                f'<circle cx="{x}" cy="{y}" r="{radius}" '
                f'fill="none" stroke="{color}" stroke-width="{width}"/>'
            )
            parts.append(
                f'<line x1="{x - half}" y1="{y}" x2="{x + half}" y2="{y}" '
                f'stroke="{color}" stroke-width="{width}"/>'
            )
            parts.append(
                f'<line x1="{x}" y1="{y - half}" x2="{x}" y2="{y + half}" '
                f'stroke="{color}" stroke-width="{width}"/>'
            )

    parts.append("</svg>")
    return "\n".join(parts)


def check_font_family_available(family: str) -> None:
    if not shutil.which("fc-match"):
        return

    proc = subprocess.run(
        ["fc-match", family, "-f", "%{family}\n"],
        capture_output=True,
        text=True,
    )
    got = proc.stdout.strip().lower()

    if family.lower() not in got:
        raise RuntimeError(
            "Inkscape backend needs the font installed in fontconfig. "
            f"Requested '{family}', fc-match returned '{got}'."
        )


def render_inkscape_pdf(
    out: Path,
    photo: Path,
    spec: dict,
    preset: dict,
    mirrored: bool = False,
    fabrication: bool = False,
) -> None:
    if not shutil.which("inkscape"):
        raise RuntimeError("Inkscape is required for the inkscape backend.")

    check_font_family_available(preset["font"]["family"])

    svg = make_inkscape_svg(
        photo,
        spec,
        preset,
        mirrored=mirrored,
        fabrication=fabrication,
    )
    svg_path = out.with_suffix(".svg")
    svg_path.write_text(svg, encoding="utf-8")

    subprocess.run(
        [
            "inkscape",
            str(svg_path),
            f"--export-filename={out}",
            "--export-type=pdf",
            "--export-text-to-path",
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    svg_path.unlink(missing_ok=True)


def render_preview(pdf: Path, png: Path, dpi: int = 300) -> None:
    doc = fitz.open(pdf)
    page = doc[0]
    pix = page.get_pixmap(dpi=dpi, alpha=False)
    pix.save(str(png))


def write_production_spec(pdf: Path, spec: dict, preset: dict) -> None:
    c = canvas.Canvas(str(pdf), pagesize=(210 * mm, 297 * mm))
    _, h = 210 * mm, 297 * mm
    c.setTitle("Nir Dahan plaque - production specification")

    y = h - 22 * mm
    c.setFont("Helvetica-Bold", 17)
    c.drawString(
        18 * mm,
        y,
        "Nir Dahan plaque - production specification",
    )
    y -= 11 * mm

    rows = [
        ("Finished panel", "200 x 300 mm"),
        ("Material", "5 mm clear acrylic / clear plastic"),
        ("Photo area", "176 x 247 mm"),
        ("White margins", "12 mm left, right, and top; 41 mm bottom"),
        (
            "Caption",
            "Centered horizontally; positioned close to photograph per reference plaque",
        ),
        ("Name", spec["name_he"]),
        ("Date", spec["date_he"]),
        ("Artwork typeface", preset["display_name"]),
        ("Hole diameter", "5.5 mm"),
        ("Hole centers", "15.5 mm from each adjacent finished edge"),
        (
            "Printing",
            "Second-surface / reverse print on rear face of clear acrylic",
        ),
        (
            "White backing",
            "Use opaque white ink/backing behind the full artwork as appropriate",
        ),
    ]

    for label, value in rows:
        c.setFont("Helvetica-Bold", 9.5)
        c.drawString(18 * mm, y, label)
        c.setFont("Helvetica", 9.5)

        # Helvetica cannot render Hebrew. The artwork PDFs contain the real Hebrew.
        if any(ord(ch) > 127 for ch in str(value)):
            value = (
                "Nir Dahan (Hebrew text is in artwork)"
                if label == "Name"
                else "April 2023 - October 2025 (Hebrew text is in artwork)"
            )

        c.drawString(62 * mm, y, str(value))
        y -= 7 * mm

    y -= 4 * mm
    c.setFont("Helvetica-Bold", 11)
    c.drawString(18 * mm, y, "Second-surface file usage")
    y -= 6 * mm

    c.setFont("Helvetica", 9.5)
    second_surface_note = (
        "Use either the normal front-view artwork and mirror it once in the "
        "printer RIP, or use the supplied pre-mirrored second-surface PDF as-is. "
        "Do not mirror twice. The fabrication overlay is a drilling reference, "
        "not the clean artwork file."
    )
    for line in textwrap.wrap(second_surface_note, 105):
        c.drawString(18 * mm, y, line)
        y -= 5 * mm

    y -= 3 * mm
    c.setFont("Helvetica-Bold", 10)
    c.drawString(18 * mm, y, "Typeface / reproducibility note")
    y -= 5.5 * mm

    c.setFont("Helvetica", 9)
    note = preset.get(
        "historical_note",
        "Fonts are not bundled. Provide the font locally when rebuilding.",
    )
    for line in textwrap.wrap(note, 112):
        c.drawString(18 * mm, y, line)
        y -= 4.7 * mm

    c.showPage()
    c.save()


def write_notes(path: Path, spec: dict, preset: dict) -> None:
    text = (
        f"NIR DAHAN PLAQUE - PRINT SHOP NOTES - "
        f"{preset['display_name'].upper()}\n\n"
        "Finished size: 200 x 300 mm\n"
        "Material: 5 mm clear acrylic/plastic\n"
        "Hole diameter: 5.5 mm\n"
        "Hole centers: 15.5 mm from each finished edge\n"
        "Photo: 176 x 247 mm\n"
        "Margins: 12 mm left/right/top; 41 mm bottom\n"
        "Printing: second-surface/reverse print on the back of clear acrylic.\n"
        "Use opaque white ink/backing where needed.\n\n"
        "Use ONE mirroring method only:\n"
        "1) front-view PDF + mirror in RIP, OR\n"
        "2) pre-mirrored second-surface PDF as supplied.\n\n"
        f"Caption typeface: {preset['display_name']}\n"
        f"Name: {spec['name_he']}\n"
        f"Date: {spec['date_he']}\n"
    )
    path.write_text(text, encoding="utf-8")


def package_zip(out_zip: Path, files: list[Path]) -> None:
    with zipfile.ZipFile(
        out_zip,
        "w",
        zipfile.ZIP_DEFLATED,
    ) as z:
        for f in files:
            z.write(f, f.name)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--photo",
        required=True,
        type=Path,
        help="Original portrait source image",
    )
    ap.add_argument(
        "--preset",
        required=True,
        type=Path,
        help="Typography preset JSON",
    )
    ap.add_argument(
        "--out-dir",
        default=Path("out"),
        type=Path,
    )
    ap.add_argument(
        "--font-dir",
        type=Path,
        default=None,
        help="Directory containing required TTF files for reportlab presets",
    )
    ap.add_argument(
        "--prefix",
        default="nir_dahan_plaque",
    )
    args = ap.parse_args()

    spec = load_json(SPEC_PATH)
    preset = load_json(args.preset)

    outdir = args.out_dir
    outdir.mkdir(parents=True, exist_ok=True)

    cropped = outdir / f"{args.prefix}_photo_cropped.png"
    crop_photo(args.photo, cropped, spec)

    tag = preset["id"]
    front = outdir / f"{args.prefix}_front_view_{tag}.pdf"
    mirrored = outdir / f"{args.prefix}_second_surface_MIRRORED_{tag}.pdf"
    fabrication = outdir / f"{args.prefix}_fabrication_5p5mm_holes_{tag}.pdf"
    print_ready = outdir / f"{args.prefix}_print_ready_{tag}.pdf"
    spec_pdf = outdir / f"{args.prefix}_production_spec_{tag}.pdf"
    preview = outdir / f"{args.prefix}_preview_{tag}_300dpi.png"
    notes = outdir / f"{args.prefix}_PRINT_SHOP_NOTES_{tag}.txt"
    package = outdir / f"{args.prefix}_FINAL_{tag}.zip"

    backend = preset["backend"]

    if backend == "reportlab":
        render_reportlab_pdf(
            front,
            cropped,
            spec,
            preset,
            args.font_dir,
            mirrored=False,
            fabrication=False,
        )
        render_reportlab_pdf(
            mirrored,
            cropped,
            spec,
            preset,
            args.font_dir,
            mirrored=True,
            fabrication=False,
        )
        render_reportlab_pdf(
            fabrication,
            cropped,
            spec,
            preset,
            args.font_dir,
            mirrored=False,
            fabrication=True,
        )
    elif backend == "inkscape":
        render_inkscape_pdf(
            front,
            cropped,
            spec,
            preset,
            mirrored=False,
            fabrication=False,
        )
        render_inkscape_pdf(
            mirrored,
            cropped,
            spec,
            preset,
            mirrored=True,
            fabrication=False,
        )
        render_inkscape_pdf(
            fabrication,
            cropped,
            spec,
            preset,
            mirrored=False,
            fabrication=True,
        )
    else:
        raise ValueError(f"Unknown backend: {backend}")

    shutil.copy2(front, print_ready)
    write_production_spec(spec_pdf, spec, preset)
    render_preview(front, preview, 300)
    write_notes(notes, spec, preset)

    package_zip(
        package,
        [
            print_ready,
            front,
            mirrored,
            fabrication,
            spec_pdf,
            preview,
            notes,
        ],
    )

    manifest = {
        "preset": preset["id"],
        "source_photo_sha256": sha256(args.photo),
        "cropped_photo_sha256": sha256(cropped),
        "outputs": {
            f.name: sha256(f)
            for f in [
                print_ready,
                front,
                mirrored,
                fabrication,
                spec_pdf,
                preview,
                notes,
                package,
            ]
        },
    }

    manifest_path = outdir / f"{args.prefix}_manifest_{tag}.json"
    manifest_path.write_text(
        json.dumps(
            manifest,
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        json.dumps(
            manifest,
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
