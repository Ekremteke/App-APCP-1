"""
document_processor.py
Pre-processes ZIP auction pack into structured data for the AI layer.
Handles: document identification, text extraction, image rendering of key pages,
checkbox detection, and structured JSON output.
"""

import zipfile
import os
import re
import base64
import tempfile
from pathlib import Path
from typing import Optional
from pypdf import PdfReader
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import io


# ─────────────────────────────────────────────
# DOCUMENT IDENTIFICATION
# ─────────────────────────────────────────────

DOCUMENT_PATTERNS = {
    "ta6":             [r"ta6", r"property.info", r"law.society.property.information"],
    "ta7":             [r"ta7", r"leasehold.information"],
    "ta10":            [r"ta10", r"fittings", r"contents.form"],
    "additional_enq":  [r"additional.enquir", r"additional.info"],
    "buyer_note":      [r"buyer.pack.summary", r"buyer.information.pack.notice"],
    "lh_register":     [r"lh.*register", r"leasehold.*register"],
    "lh_plan":         [r"lh.*plan", r"leasehold.*plan"],
    "fh_register":     [r"fh.*register", r"freehold.*register"],
    "fh_plan":         [r"fh.*plan", r"freehold.*plan"],
    "epc":             [r"energy.performance", r"\bepc\b"],
    "lease":           [r"lease.*\d{4}", r"^lease"],
    "management_pack": [r"management.pack", r"lpe1", r"lpe\d"],
    "local_auth_search":[r"plas", r"local.authority.search", r"con29"],
    "water_search":    [r"water.*drainage", r"pw.*template", r"drainage.*search"],
    "env_search":      [r"environmental.search", r"environ.*search"],
    "transfer":        [r"transfer"],
    "correspondence":  [r"correspondence", r"^fw[_\-\s]", r"^re[_\-\s]"],
    "fw_email":        [r"fw[_\-\s].*building", r"fw[_\-\s].*property"],
}


def identify_document(filename: str) -> str:
    """Identify document type from filename."""
    name = filename.lower().replace(" ", ".").replace("_", ".")
    name = re.sub(r"[^a-z0-9.]", ".", name)
    for doc_type, patterns in DOCUMENT_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, name):
                return doc_type
    return "unknown"


# ─────────────────────────────────────────────
# PDF TEXT EXTRACTION
# ─────────────────────────────────────────────

def extract_text_from_pdf(pdf_path: str, max_pages: Optional[int] = None) -> dict:
    """Extract text from all pages of a PDF."""
    try:
        reader = PdfReader(pdf_path)
        pages = {}
        total = len(reader.pages)
        limit = min(total, max_pages) if max_pages else total
        for i in range(limit):
            try:
                text = reader.pages[i].extract_text() or ""
                pages[i + 1] = text.strip()
            except Exception:
                pages[i + 1] = ""
        return {"total_pages": total, "pages": pages, "readable": any(len(t) > 50 for t in pages.values())}
    except Exception as e:
        return {"total_pages": 0, "pages": {}, "readable": False, "error": str(e)}


# ─────────────────────────────────────────────
# IMAGE RENDERING FOR CHECKBOX PAGES
# ─────────────────────────────────────────────

KEY_PAGE_RULES = {
    # doc_type: list of page numbers to render (1-indexed), or "auto" to detect
    "ta6":             [5, 6, 13, 14],   # alterations/planning, parking, occupiers
    "ta7":             [4, 8, 11],        # property type, charges, building safety
    "additional_enq":  [1, 2],            # all questions
    "epc":             [1, 2],            # rating page
}


def render_page_as_image(pdf_path: str, page_num: int, dpi: int = 200) -> Optional[str]:
    """Render a PDF page as base64 PNG image."""
    try:
        images = convert_from_path(
            pdf_path,
            dpi=dpi,
            first_page=page_num,
            last_page=page_num,
        )
        if not images:
            return None
        buf = io.BytesIO()
        images[0].save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode("utf-8")
    except Exception:
        return None


def ocr_page(pdf_path: str, page_num: int, dpi: int = 250) -> str:
    """OCR a PDF page and return extracted text."""
    try:
        images = convert_from_path(pdf_path, dpi=dpi, first_page=page_num, last_page=page_num)
        if not images:
            return ""
        return pytesseract.image_to_string(images[0])
    except Exception:
        return ""


def get_key_page_images(pdf_path: str, doc_type: str) -> dict:
    """Render key pages of a document as base64 images for vision analysis."""
    page_nums = KEY_PAGE_RULES.get(doc_type, [])
    if not page_nums:
        return {}

    try:
        reader = PdfReader(pdf_path)
        total = len(reader.pages)
    except Exception:
        return {}

    images = {}
    for p in page_nums:
        if p <= total:
            img = render_page_as_image(pdf_path, p)
            if img:
                images[p] = img
    return images


# ─────────────────────────────────────────────
# CHECKBOX DETECTION via OCR
# ─────────────────────────────────────────────

def extract_checkboxes_from_ta6(pdf_path: str) -> dict:
    """Extract key TA6 checkbox answers using OCR on rendered pages."""
    results = {}

    # Page 5/6: Alterations and planning (section 4.1, 4.4, 4.5)
    for page_num, section in [(5, "alterations"), (6, "planning_issues")]:
        ocr_text = ocr_page(pdf_path, page_num)
        results[f"page_{page_num}_ocr"] = ocr_text

    # Page 13: Parking (section 9.1)
    ocr_p13 = ocr_page(pdf_path, 13)
    results["parking_ocr"] = ocr_p13

    # Page 14: Occupiers (section 11)
    ocr_p14 = ocr_page(pdf_path, 14)
    results["occupiers_ocr"] = ocr_p14

    return results


def extract_checkboxes_from_additional_enq(pdf_path: str) -> dict:
    """Extract key Additional Enquiries Form checkbox answers."""
    results = {}
    for page_num in [1, 2]:
        try:
            reader = PdfReader(pdf_path)
            if page_num <= len(reader.pages):
                text = reader.pages[page_num - 1].extract_text() or ""
                results[f"page_{page_num}_text"] = text
                # Also render for visual inspection
                img = render_page_as_image(pdf_path, page_num)
                if img:
                    results[f"page_{page_num}_image"] = img
        except Exception:
            pass
    return results


# ─────────────────────────────────────────────
# MAIN PROCESSOR
# ─────────────────────────────────────────────

def process_zip(zip_path: str) -> dict:
    """
    Main entry point. Process auction pack ZIP into structured data.
    Returns a dict with all extracted information ready for the AI layer.
    """
    result = {
        "inventory": [],
        "documents": {},
        "key_images": {},
        "processing_notes": [],
    }

    with tempfile.TemporaryDirectory() as tmpdir:
        # 1. Extract ZIP
        try:
            with zipfile.ZipFile(zip_path, "r") as z:
                z.extractall(tmpdir)
        except Exception as e:
            result["processing_notes"].append(f"ZIP extraction error: {e}")
            return result

        # 2. Inventory all files
        pdf_files = []
        for root, dirs, files in os.walk(tmpdir):
            for fname in files:
                if fname.lower().endswith(".pdf"):
                    fpath = os.path.join(root, fname)
                    doc_type = identify_document(fname)
                    entry = {
                        "filename": fname,
                        "doc_type": doc_type,
                        "path": fpath,
                        "size_kb": round(os.path.getsize(fpath) / 1024, 1),
                    }
                    pdf_files.append(entry)
                    result["inventory"].append({
                        "filename": fname,
                        "doc_type": doc_type,
                        "size_kb": entry["size_kb"],
                    })

        result["processing_notes"].append(f"Found {len(pdf_files)} PDF files in ZIP.")

        # 3. Extract text from all documents
        for entry in pdf_files:
            doc_type = entry["doc_type"]
            fpath = entry["path"]
            fname = entry["filename"]

            # Text extraction — limit pages for large docs
            max_pages = None
            if entry["size_kb"] > 2000:
                max_pages = 30  # Management packs can be 179 pages — take first 30

            text_data = extract_text_from_pdf(fpath, max_pages=max_pages)

            doc_entry = {
                "filename": fname,
                "doc_type": doc_type,
                "total_pages": text_data["total_pages"],
                "readable": text_data["readable"],
                "pages": text_data["pages"],
            }

            if not text_data["readable"]:
                doc_entry["extraction_note"] = "Low text yield — may be scanned/image-based."
                result["processing_notes"].append(
                    f"Low text yield for {fname} — rendering key pages for OCR."
                )

            # 4. Render key pages as images for vision-dependent documents
            if doc_type in KEY_PAGE_RULES:
                images = get_key_page_images(fpath, doc_type)
                if images:
                    doc_entry["key_page_images"] = images
                    result["processing_notes"].append(
                        f"Rendered {len(images)} key page(s) of {fname} for visual inspection."
                    )

            # 5. Additional checkbox extraction for TA6
            if doc_type == "ta6":
                checkbox_data = extract_checkboxes_from_ta6(fpath)
                doc_entry["checkbox_ocr"] = checkbox_data

            # 6. Additional checkbox extraction for Additional Enquiries
            if doc_type == "additional_enq":
                checkbox_data = extract_checkboxes_from_additional_enq(fpath)
                doc_entry["checkbox_data"] = checkbox_data

            # Store using doc_type as key (last one wins if duplicates)
            result["documents"][doc_type] = doc_entry
            # Also keep by filename for duplicates
            result["documents"][fname] = doc_entry

    # 7. Summarise what's found and what's missing
    found_types = set(entry["doc_type"] for entry in result["inventory"])
    critical_docs = ["ta6", "ta7", "lh_register", "epc", "management_pack",
                     "local_auth_search", "water_search", "additional_enq"]
    for doc in critical_docs:
        if doc not in found_types:
            result["processing_notes"].append(
                f"MISSING: No {doc.upper()} identified in pack."
            )

    if "env_search" not in found_types:
        result["processing_notes"].append(
            "MISSING: No environmental search identified in pack."
        )

    result["found_document_types"] = sorted(list(found_types))
    return result


def build_text_summary(processed: dict) -> str:
    """
    Convert processed ZIP data into a compact text block for the AI prompt.
    Images are passed separately as vision inputs.
    """
    lines = []
    lines.append("=== DOCUMENT INVENTORY ===")
    for item in processed["inventory"]:
        lines.append(f"- {item['filename']} → [{item['doc_type']}] ({item['size_kb']} KB)")

    lines.append("\n=== PROCESSING NOTES ===")
    for note in processed["processing_notes"]:
        lines.append(f"- {note}")

    lines.append("\n=== DOCUMENT CONTENTS ===")
    seen = set()
    for key, doc in processed["documents"].items():
        doc_type = doc.get("doc_type", "unknown")
        fname = doc.get("filename", key)
        if fname in seen:
            continue
        seen.add(fname)

        lines.append(f"\n--- {fname} [{doc_type}] ({doc.get('total_pages', '?')} pages) ---")
        if not doc.get("readable"):
            lines.append("  [Low text extraction — see key page images]")

        pages = doc.get("pages", {})
        for page_num in sorted(pages.keys()):
            text = pages[page_num]
            if text and len(text) > 30:
                lines.append(f"  PAGE {page_num}:")
                # Trim very long pages
                if len(text) > 3000:
                    lines.append(text[:3000] + "\n  [... truncated ...]")
                else:
                    lines.append(text)

        # Include OCR data if available
        if "checkbox_ocr" in doc:
            lines.append("  [CHECKBOX OCR DATA]:")
            for k, v in doc["checkbox_ocr"].items():
                if v and len(v) > 20:
                    lines.append(f"    {k}: {v[:500]}")

        if "checkbox_data" in doc:
            lines.append("  [ADDITIONAL ENQUIRIES DATA]:")
            for k, v in doc["checkbox_data"].items():
                if isinstance(v, str) and len(v) > 20:
                    lines.append(f"    {k}: {v[:500]}")

    return "\n".join(lines)


def collect_vision_inputs(processed: dict) -> list:
    """
    Collect all key page images for vision API calls.
    Returns list of dicts: {doc_type, page_num, image_b64}
    """
    inputs = []
    seen = set()
    for key, doc in processed["documents"].items():
        fname = doc.get("filename", key)
        if fname in seen:
            continue
        seen.add(fname)
        doc_type = doc.get("doc_type", "unknown")
        for page_num, img_b64 in doc.get("key_page_images", {}).items():
            inputs.append({
                "doc_type": doc_type,
                "filename": fname,
                "page_num": page_num,
                "image_b64": img_b64,
            })
        # Also from checkbox_data
        for k, v in doc.get("checkbox_data", {}).items():
            if k.endswith("_image") and isinstance(v, str):
                page_num = int(k.replace("page_", "").replace("_image", "")) \
                    if "page_" in k else 0
                inputs.append({
                    "doc_type": doc_type,
                    "filename": fname,
                    "page_num": page_num,
                    "image_b64": v,
                })
    return inputs
