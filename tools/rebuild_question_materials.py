#!/usr/bin/env python3
"""Rebuild PDF materials using recorded crops; PDFs are supplied separately."""
import argparse
import base64
import copy
import hashlib
import io
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
    scene = rec.get("appearanceEdit", {}).get("replacesScene", False)
    original = ET.parse(ROOT / "site" / rec["artSource"]).getroot() if rec.get("artSource") and not scene else None
    display_height = rec.get("displayCrop", [0, 0, rec["width"], rec["height"]])[3]
    svg = ET.Element(NS + "svg", {"width": str(rec["width"]), "height": str(display_height),
        "viewBox": f'0 0 {rec["width"]} {display_height}'})
    ET.SubElement(svg, NS + "title").text = f'제{rec["exam"]}회 {rec["question"]}번 자료'
    defs = ET.SubElement(svg, NS + "defs")
    ET.SubElement(defs, NS + "image", {"id": "pdf-source", "width": str(rec["width"]),
        "height": str(rec["height"]), "href": "data:image/webp;base64," + base64.b64encode(source_bytes).decode()})
    ET.SubElement(svg, NS + "use", {"href": "#pdf-source"})
    if original is not None:
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
    edit = rec.get("appearanceEdit")
    if edit:
        asset = (ROOT / "site" / edit["asset"]).read_bytes()
        assert digest(asset) == edit["imageSha256"], "Appearance artwork changed"
        clip = ET.SubElement(defs, NS + "clipPath", {"id": "appearance-edit"})
        for points in edit["polygons"]:
            ET.SubElement(clip, NS + "polygon", {"points": " ".join(f"{x:.4f},{y:.4f}" for x, y in points)})
        x, y, width, height = edit["box"]
        ET.SubElement(svg, NS + "image", {"x": str(x), "y": str(y), "width": str(width),
            "height": str(height), "preserveAspectRatio": "none", "clip-path": "url(#appearance-edit)",
            "data-appearance-edit": key, "href": "data:image/webp;base64," + base64.b64encode(asset).decode()})
        for index, material in enumerate(edit.get("preservedMaterials", [])):
            blob = (ROOT / "site" / material["asset"]).read_bytes()
            assert digest(blob) == material["imageSha256"], "Preserved material changed"
            x, y, width, height = material["targetBox"]
            attrs = {"x": str(x), "y": str(y), "width": str(width),
                "height": str(height), "preserveAspectRatio": "none",
                "data-preserved-material": str(index),
                "href": "data:image/webp;base64," + base64.b64encode(blob).decode()}
            if material.get("clipPoints"):
                name = f"material-{index}"
                clip = ET.SubElement(defs, NS + "clipPath", {"id": name})
                ET.SubElement(clip, NS + "polygon", {"points": " ".join(f"{a},{b}" for a, b in material["clipPoints"])})
                attrs["clip-path"] = f"url(#{name})"
            if material.get("feather"):
                # Soften only the outer border of a native photo; its factual core stays opaque.
                name = f"material-edge-{index}"
                distance = min(material["feather"], width / 8, height / 8)
                mask = ET.SubElement(defs, NS + "mask", {"id": name,
                    "maskUnits": "userSpaceOnUse", "x": str(x), "y": str(y),
                    "width": str(width), "height": str(height)})
                ET.SubElement(mask, NS + "rect", {"x": str(x + distance),
                    "y": str(y + distance), "width": str(width - 2 * distance),
                    "height": str(height - 2 * distance), "fill": "white"})
                for side, values in enumerate([
                    (x, y, width, distance, "0%", "0%", "0%", "100%"),
                    (x, y + height - distance, width, distance, "0%", "100%", "0%", "0%"),
                    (x, y + distance, distance, height - 2 * distance, "0%", "0%", "100%", "0%"),
                    (x + width - distance, y + distance, distance, height - 2 * distance, "100%", "0%", "0%", "0%")]):
                    gx, gy, gw, gh, x1, y1, x2, y2 = values
                    gradient_id = f"{name}-{side}"
                    gradient = ET.SubElement(defs, NS + "linearGradient", {"id": gradient_id,
                        "x1": x1, "y1": y1, "x2": x2, "y2": y2})
                    ET.SubElement(gradient, NS + "stop", {"offset": "0", "stop-color": "black"})
                    ET.SubElement(gradient, NS + "stop", {"offset": "1", "stop-color": "white"})
                    ET.SubElement(mask, NS + "rect", {"x": str(gx), "y": str(gy),
                        "width": str(gw), "height": str(gh), "fill": f"url(#{gradient_id})"})
                attrs["mask"] = f"url(#{name})"
            ET.SubElement(svg, NS + "image", attrs)
        protected = ([] if scene else rec.get("protectedTextRects", [])) + edit.get("protectedRects", [])
        if protected:
            clip = ET.SubElement(defs, NS + "clipPath", {"id": "appearance-facts"})
            for x, y, width, height in protected:
                ET.SubElement(clip, NS + "rect", {"x": str(x), "y": str(y),
                    "width": str(width), "height": str(height)})
            ET.SubElement(svg, NS + "use", {"href": "#pdf-source", "clip-path": "url(#appearance-facts)"})
    return svg


def render_choice(doc, choice):
    pix = fitz.Pixmap(doc, choice["sourceXref"])
    mask = doc.extract_image(choice["sourceXref"]).get("smask", 0)
    if mask:
        pix = fitz.Pixmap(pix, fitz.Pixmap(doc, mask))
    if pix.colorspace.n != 3:
        pix = fitz.Pixmap(fitz.csRGB, pix)
    # PNG export unpremultiplies PDF alpha before compositing onto white.
    image = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGBA")
    background = Image.new("RGBA", image.size, "white")
    background.alpha_composite(image)
    image = background.convert("RGB")
    assert digest(image.tobytes()) == choice["pixelSha256"], "Choice photograph changed"
    return image


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
            if rec.get("artSource") or rec.get("appearanceEdit"):
                ET.ElementTree(render_art(key, rec, output.read_bytes())).write(
                    art_dir / f"{key}.svg", encoding="unicode")
            elif rec.get("displayCrop"):
                prompts = args.output_dir / "question-prompts"
                prompts.mkdir(exist_ok=True)
                image.crop(rec["displayCrop"]).save(prompts / f"{key}.webp",
                    format="WEBP", lossless=True, quality=100, method=4, exact=True)
            for choice in rec.get("choiceImages", []):
                choices = args.output_dir / "choice-art"
                choices.mkdir(exist_ok=True)
                render_choice(docs[rec["sourceSha256"]], choice).save(
                    choices / f'{key}-{choice["number"]}.webp', format="WEBP", lossless=True,
                    quality=100, method=4, exact=True)
            print(f"Rebuilt {key}")
    finally:
        for doc in docs.values():
            doc.close()


if __name__ == "__main__":
    main()
