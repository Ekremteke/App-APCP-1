"""
docx_generator.py
Fills APSS_Simple_Template.docx with resolved APSS field values.
Parses markdown APSS output and maps values to template placeholders.
"""

import re
import copy
from docx import Document
from docx.oxml.ns import qn
from lxml import etree


# ─────────────────────────────────────────────
# PLACEHOLDER EXTRACTION FROM MARKDOWN
# ─────────────────────────────────────────────

PLACEHOLDER_MAP = {
    # Property Overview
    "propertyAddress":                  r"(?:property address|address)[:\s]+(.+?)(?:\n|Evidence:)",
    "tenure":                           r"Tenure[|\s]+(.+?)(?:\n|Evidence:)",
    "propertyType":                     r"Property Type[|\s]+(.+?)(?:\n|Evidence:)",
    "leaseTerm":                        r"Lease Term[^|]*[|\s]+(.+?)(?:\n|Evidence:)",
    "councilTaxBand":                   r"Council Tax Band[|\s]+(.+?)(?:\n|Evidence:)",
    "listedBuildingOrConservationArea": r"Listed Building[^|]*[|\s]+(.+?)(?:\n|Evidence:)",
    "parkingArrangements":              r"Parking Arrangements[|\s]+(.+?)(?:\n|Evidence:)",
    "constructionType":                 r"Construction Type[|\s]+(.+?)(?:\n|Evidence:)",
    "serviceRentGrounds":               r"Service Charge[^|]*[|\s]+(.+?)(?:\n|⚠|❌|Evidence:)",
    "sharedOwnershipPercent":           r"Shared Ownership[^|]*[|\s]+(.+?)(?:\n|Evidence:)",
    "materialPropertyNotes":            r"Material Information Note\(s\)[^|]*\n+(.+?)(?:\n\n|\*\*Key)",
}

STATUS_PLACEHOLDERS = [
    "titleStatus", "titleComments",
    "ta6Status", "ta6Comments",
    "ta10Status", "ta10Comments",
    "addInfoStatus", "addInfoComments",
    "epcStatus", "epcComments",
    "searchStatus", "searchComments",
    "leaseInfoStatus", "leaseInfoComments",
    "planningStatus", "planningComments",
    "tenancyStatus", "tenancyComments",
    "probateStatus", "probateComments",
    "hmoStatus", "hmoComments",
    "miNotesStatus", "materialPropertyNotesComments",
]

FLAG_PLACEHOLDERS = [
    "flagTitleDiscrepancies",
    "flagRightsOfWay",
    "flagRestrictiveCovenants",
    "flagPlanningIssues",
    "flagEpcBelowE",
    "flagUnregisteredTitle",
    "flagHmoLicensing",
    "flagLeaseholdInfo",
    "flagEnvironmentalRisks",
    "flagOccupiersTenancy",
    "flagSoldAsSeen",
]


def extract_value_from_markdown(markdown: str, placeholder: str) -> str:
    """Extract a field value from the APSS markdown output."""
    # Try direct placeholder lookup
    pattern = PLACEHOLDER_MAP.get(placeholder)
    if pattern:
        match = re.search(pattern, markdown, re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1).strip()

    # Generic table cell extraction
    escaped = re.escape(placeholder.replace("{{", "").replace("}}", ""))
    return ""


def parse_apss_markdown(markdown: str) -> dict:
    """
    Parse APSS markdown into a flat dict of placeholder → value.
    This is a best-effort parser. The AI output follows the template structure.
    """
    values = {}

    # Extract property address from header
    addr_match = re.search(r"#\s*Auction Pack Summary Sheet\s*\n+(.+?)(?:\n)", markdown)
    if addr_match:
        values["propertyAddress"] = addr_match.group(1).strip()

    # Parse Property Overview table rows
    # Pattern: | Field Name | Value |
    prop_table_match = re.search(
        r"Property Overview.*?\n(.*?)(?:\*\*Key Document|Key Document Status)",
        markdown, re.DOTALL | re.IGNORECASE
    )
    if prop_table_match:
        table_text = prop_table_match.group(1)
        rows = re.findall(r"\|\s*(.+?)\s*\|\s*(.+?)\s*\|", table_text)
        field_map = {
            "tenure": "tenure",
            "property type": "propertyType",
            "lease term": "leaseTerm",
            "council tax band": "councilTaxBand",
            "listed building": "listedBuildingOrConservationArea",
            "parking arrangements": "parkingArrangements",
            "construction type": "constructionType",
            "service charges": "serviceRentGrounds",
            "shared ownership": "sharedOwnershipPercent",
            "material information note": "materialPropertyNotes",
        }
        for field, val in rows:
            field_lower = field.lower().strip()
            for key, ph in field_map.items():
                if key in field_lower:
                    # Strip evidence anchors
                    clean_val = re.sub(r"Evidence:.*", "", val, flags=re.DOTALL).strip()
                    values[ph] = clean_val
                    break

    # Parse Key Document Status table
    kds_match = re.search(
        r"Key Document Status.*?\n(.*?)(?:\*\*Material Flags|Material Flags)",
        markdown, re.DOTALL | re.IGNORECASE
    )
    if kds_match:
        kds_text = kds_match.group(1)
        rows = re.findall(r"\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|", kds_text)

        doc_ph_map = {
            "title register": ("titleStatus", "titleComments"),
            "ta6": ("ta6Status", "ta6Comments"),
            "ta10": ("ta10Status", "ta10Comments"),
            "additional information": ("addInfoStatus", "addInfoComments"),
            "epc": ("epcStatus", "epcComments"),
            "searches": ("searchStatus", "searchComments"),
            "leasehold information": ("leaseInfoStatus", "leaseInfoComments"),
            "planning": ("planningStatus", "planningComments"),
            "tenancy agreements": ("tenancyStatus", "tenancyComments"),
            "probate": ("probateStatus", "probateComments"),
            "hmo": ("hmoStatus", "hmoComments"),
            "material information note": ("miNotesStatus", "materialPropertyNotesComments"),
        }

        for doc, status, comments in rows:
            doc_lower = doc.lower().strip()
            for key, (status_ph, comments_ph) in doc_ph_map.items():
                if key in doc_lower:
                    values[status_ph] = _clean_status(status.strip())
                    values[comments_ph] = comments.strip()
                    break

    # Parse Material Flags table
    flags_match = re.search(
        r"Material Flags.*?\n(.*?)(?:\*\*Additional Tools|Additional Tools|$)",
        markdown, re.DOTALL | re.IGNORECASE
    )
    if flags_match:
        flags_text = flags_match.group(1)
        rows = re.findall(r"\|\s*(.+?)\s*\|\s*(Yes|No)\s*\|", flags_text, re.IGNORECASE)

        flag_map = {
            "title discrepancies": "flagTitleDiscrepancies",
            "rights of way": "flagRightsOfWay",
            "restrictive covenants": "flagRestrictiveCovenants",
            "planning issues": "flagPlanningIssues",
            "epc": "flagEpcBelowE",
            "unregistered": "flagUnregisteredTitle",
            "hmo": "flagHmoLicensing",
            "leasehold information": "flagLeaseholdInfo",
            "coastal": "flagEnvironmentalRisks",
            "occupiers": "flagOccupiersTenancy",
            "sold": "flagSoldAsSeen",
        }

        for risk_area, flagged in rows:
            risk_lower = risk_area.lower().strip()
            for key, ph in flag_map.items():
                if key in risk_lower:
                    values[ph] = flagged.strip()
                    break

    return values


def _clean_status(raw: str) -> str:
    """Normalise status cell value to approved labels."""
    raw = raw.strip()
    if "✅" in raw and "Provided" in raw:
        return "✅ Provided"
    if "✅" in raw and "Not applicable" in raw:
        return "✅ Not applicable"
    if "❌" in raw:
        return "❌ Information not available in pack – requires manual review"
    if "⚠️" in raw or "Requires manual" in raw:
        return "⚠️ Requires manual verification"
    return raw


# ─────────────────────────────────────────────
# DOCX TEMPLATE FILLING
# ─────────────────────────────────────────────

def _replace_in_runs(paragraph, placeholder: str, value: str):
    """Replace placeholder in paragraph runs, handling split-run placeholders."""
    full_text = "".join(r.text for r in paragraph.runs)
    if placeholder not in full_text:
        return False
    new_text = full_text.replace(placeholder, value)
    # Clear all runs, put new text in first
    for i, run in enumerate(paragraph.runs):
        run.text = new_text if i == 0 else ""
    return True


def _replace_in_cell(cell, placeholder: str, value: str):
    """Replace placeholder in all paragraphs of a table cell."""
    for para in cell.paragraphs:
        _replace_in_runs(para, placeholder, value)


def _replace_in_document(doc: Document, placeholder: str, value: str):
    """Replace placeholder throughout the entire document."""
    # In paragraphs
    for para in doc.paragraphs:
        _replace_in_runs(para, placeholder, value)
    # In tables (including nested)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                _replace_in_cell(cell, placeholder, value)
                # Nested tables
                for nested_table in cell.tables:
                    for nested_row in nested_table.rows:
                        for nested_cell in nested_row.cells:
                            _replace_in_cell(nested_cell, placeholder, value)


def fill_template(template_path: str, apss_markdown: str, output_path: str) -> bool:
    """
    Fill APSS_Simple_Template.docx with values parsed from APSS markdown.
    Saves to output_path. Returns True on success.
    """
    try:
        doc = Document(template_path)
    except Exception as e:
        raise RuntimeError(f"Could not open template: {e}")

    # Parse markdown into values
    values = parse_apss_markdown(apss_markdown)

    # Build complete placeholder → value mapping
    all_placeholders = (
        list(PLACEHOLDER_MAP.keys()) +
        STATUS_PLACEHOLDERS +
        FLAG_PLACEHOLDERS
    )

    replaced_count = 0
    for ph in all_placeholders:
        template_ph = "{{" + ph + "}}"
        value = values.get(ph, "")
        if not value:
            # Leave unfilled placeholders as empty string rather than visible {{...}}
            value = ""
        _replace_in_document(doc, template_ph, value)
        if value:
            replaced_count += 1

    # Safety check: remove any remaining {{ }} placeholders
    for ph in all_placeholders:
        template_ph = "{{" + ph + "}}"
        _replace_in_document(doc, template_ph, "")

    doc.save(output_path)
    return True


# ─────────────────────────────────────────────
# VALIDATION: CHECK FOR REMAINING PLACEHOLDERS
# ─────────────────────────────────────────────

def check_remaining_placeholders(docx_path: str) -> list:
    """Check if any {{ }} placeholders remain in the DOCX."""
    doc = Document(docx_path)
    remaining = []

    def check_text(text, location):
        matches = re.findall(r"\{\{[^}]+\}\}", text)
        for m in matches:
            remaining.append(f"{location}: {m}")

    for para in doc.paragraphs:
        check_text(para.text, "paragraph")
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                check_text(cell.text, f"table cell")

    return remaining
