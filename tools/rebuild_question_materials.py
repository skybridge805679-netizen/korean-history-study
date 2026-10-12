#!/usr/bin/env python3
"""Rebuild PDF materials using recorded crops; PDFs are supplied separately."""
import argparse
import base64
import copy
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

import fitz
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
NS = "{http://www.w3.org/2000/svg}"
ET.register_namespace("", NS[1:-1])


def digest(data):
    return hashlib.sha256(data).hexdigest()


def render_source(doc, rec):
    parts = []
    for box, origin in zip(rec["segments"], rec["origins"]):
        pix = doc[rec["page"] - 1].get_pixmap(
            matrix=fitz.Matrix(rec["scale"], rec["scale"]),
            clip=fitz.Rect(box), alpha=False,
        )
        assert [pix.x, pix.y] == origin, "PDF raster origin changed"
        parts.append(Image.frombytes("RGB", (pix.width, pix.height), pix.samples))
    image = Image.new("RGB", (max(p.width for p in parts),
                              sum(p.height for p in parts) + 25 * (len(parts) - 1)), "white")
    y = 0
    for part in parts:
        image.paste(part, ((image.width - part.width) // 2, y))
        y += part.height + 25
    assert image.size == (rec["width"], rec["height"]), "PDF raster dimensions changed"
    if rec.get("pixelSha256"):
        assert digest(image.convert("RGBA").tobytes()) == rec["pixelSha256"], "Source pixels changed"
    return image


def render_art(key, rec, source_bytes):
    original = ET.parse(ROOT / "site" / rec["artSource"]).getroot()
    svg = ET.Element(NS + "svg", {"width": str(rec["width"]), "height": str(rec["height"]),
        "viewBox": f'0 0 {rec["width"]} {rec["height"]}'})
    ET.SubElement(svg, NS + "title").text = f'제{rec["exam"]}회 {rec["question"]}번 자료'
    defs = ET.SubElement(svg, NS + "defs")
    ET.SubElement(defs, NS + "image", {"id": "pdf-source", "width": str(rec["width"]),
        "height": str(rec["height"]), "href": "data:image/webp;base64," + base64.b64encode(source_bytes).decode()})
    ET.SubElement(svg, NS + "use", {"href": "#pdf-source"})
    m = rec["artMatrix"]
    transform = f'matrix({m[0][0]:.8f} {m[1][0]:.8f} {m[0][1]:.8f} {m[1][1]:.8f} {m[0][2]:.8f} {m[1][2]:.8f})'
    group = ET.SubElement(svg, NS + "g", {"transform": transform, "data-original-art": key})
    first = True
    for child in original:
        if child.tag == NS + "title":
            continue
        if child.tag == NS + "image" and first:
            first = False
            continue
        group.append(copy.deepcopy(child))
    if rec.get("protectedTextRects"):
        clip = ET.SubElement(defs, NS + "clipPath", {"id": "pdf-text"})
        for x, y, width, height in rec["protectedTextRects"]:
            ET.SubElement(clip, NS + "rect", {"x": f"{x:.4f}", "y": f"{y:.4f}",
                "width": f"{width:.4f}", "height": f"{height:.4f}"})
        ET.SubElement(svg, NS + "use", {"href": "#pdf-source", "clip-path": "url(#pdf-text)"})
    return svg


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True, help="Directory for question-materials/ and question-art/")
    parser.add_argument("--keys", nargs="*", help="Optional question keys, e.g. 72-48 76-6")
    args = parser.parse_args()
    records = json.loads((ROOT / "site/question-materials/source-map.json").read_text())
    keys = args.keys or list(records)
    wanted = {records[k]["sourceSha256"] for k in keys}
    pdfs = {}
    for path in args.pdf_dir.rglob("*.pdf"):
        sha = digest(path.read_bytes())
        if sha in wanted:
            pdfs[sha] = path
    missing = wanted - pdfs.keys()
    if missing:
        parser.error(f"Missing original PDFs with SHA256: {', '.join(sorted(missing))}")
    material_dir = args.output_dir / "question-materials"
    art_dir = args.output_dir / "question-art"
    material_dir.mkdir(parents=True, exist_ok=True)
    art_dir.mkdir(parents=True, exist_ok=True)
    docs = {sha: fitz.open(path) for sha, path in pdfs.items()}
    try:
        for key in keys:
            rec = records[key]
            image = render_source(docs[rec["sourceSha256"]], rec)
            output = material_dir / f"{key}.webp"
            image.save(output, format="WEBP", lossless=True, quality=100, method=4, exact=True)
            with Image.open(output) as decoded:
                assert image.convert("RGBA").tobytes() == decoded.convert("RGBA").tobytes()
            if rec.get("artSource"):
                ET.ElementTree(render_art(key, rec, output.read_bytes())).write(
                    art_dir / f"{key}.svg", encoding="unicode")
            print(f"Rebuilt {key}")
    finally:
        for doc in docs.values():
            doc.close()


if __name__ == "__main__":
    main()
