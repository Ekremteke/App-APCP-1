"""
ai_caller.py
Sends pre-processed pack data to OpenAI/Claude API.
Returns structured JSON matching template placeholders exactly.
"""

import os
import json
import re
from typing import Optional


def load_kb_files(kb_dir: str) -> str:
    """Load critical KB files - keeps token count manageable."""
    kb_order = [
        "Security_Runtime_KB.md",
        "APCP-20-30_Stabilisation_Rules_KB.md",
        "Disclaimer_Routing_Map_KB.md",
        "AI_Training_KB.md",
        "APSS_Disclaimer_Library.md",
    ]
    blocks = []
    total = 0
    limit = 20000

    for fname in kb_order:
        fpath = os.path.join(kb_dir, fname)
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
            if len(content) > 6000:
                content = content[:6000] + "\n[truncated]"
            block = f"# {fname}\n\n{content}"
            if total + len(block) > limit:
                break
            blocks.append(block)
            total += len(block)

    return "\n\n".join(blocks)


JSON_SYSTEM_PROMPT = """You are Medway Law's Legal Pack Assistant.

Analyse the auction pack evidence provided and return ONLY a valid JSON object.
No markdown. No explanation. No preamble. Just the JSON.

The JSON must contain ALL of these keys:

PROPERTY OVERVIEW KEYS:
- propertyAddress
- tenure (include evidence anchor)
- propertyType (include evidence anchor)
- leaseTerm (include evidence anchor, or "Not applicable")
- councilTaxBand (include evidence anchor, or "Council Tax Band lookup required")
- listedBuildingOrConservationArea (include evidence anchor)
- parkingArrangements (include evidence anchor)
- constructionType (include evidence anchor)
- serviceRentGrounds (full ground rent and service charge details with evidence)
- sharedOwnershipPercent (percentage or "✅ Not applicable. Evidence: TA7 p.4 / 1.1")
- materialPropertyNotes (material information notes about the property itself)

KEY DOCUMENT STATUS KEYS (each needs status + comments):
- titleStatus, titleComments
- ta6Status, ta6Comments
- ta10Status, ta10Comments
- addInfoStatus, addInfoComments
- epcStatus, epcComments
- searchStatus, searchComments
- leaseInfoStatus, leaseInfoComments
- planningStatus, planningComments
- tenancyStatus, tenancyComments
- probateStatus, probateComments
- hmoStatus, hmoComments
- miNotesStatus, materialPropertyNotesComments

STATUS VALUES - use exactly one of:
- "✅ Provided"
- "✅ Not applicable"
- "❌ Information not available in pack – requires manual review"
- "⚠️ Requires manual verification"

MATERIAL FLAGS KEYS (value must be exactly "Yes" or "No"):
- flagTitleDiscrepancies
- flagRightsOfWay
- flagRestrictiveCovenants
- flagPlanningIssues
- flagEpcBelowE
- flagUnregisteredTitle
- flagHmoLicensing
- flagLeaseholdInfo
- flagEnvironmentalRisks
- flagOccupiersTenancy
- flagSoldAsSeen

CRITICAL RULES:
1. EPC rating E, F or G → flagEpcBelowE = "Yes". epcComments must start with "EPC rating: [letter]. Evidence: EPC p.1 / Energy rating."
2. Seller disclosed NO works requiring planning → planningStatus = "✅ Not applicable"
3. FH title register alone does NOT mean multiple boundaries for sale
4. Ground rent confirmed NOT payable → do not state a ground rent figure
5. Shared ownership: if standard leasehold flat → sharedOwnershipPercent = "✅ Not applicable. Evidence: TA7 p.4 / 1.1"
6. Environmental search missing → note in searchComments: "An environmental search is not included in this pack. Prospective buyers are strongly advised to obtain this independently before bidding."
7. LH Register C section mentions rentcharge → add to materialPropertyNotes
8. Cladding in Management Pack or TA7 5.8 → add cladding note to materialPropertyNotes
9. LPE1 by managing agent not RTM → add to leaseInfoComments: "The LPE1 has not been completed by a Right to Manage Company (RTM)..."
10. TA6 has multiple Not Known or incomplete → add to ta6Comments

EVIDENCE ANCHOR FORMAT: "Evidence: [Label] p.[N] / [Section]"
ALLOWED LABELS: "Leasehold Title Register", "Freehold Title Register", "TA6", "TA7", "TA10", "Management Pack", "EPC", "Local Authority Search", "Water and Drainage Search", "Additional Enquiries Form", "Buyer Pack Summary Note", "Lease", "Correspondence"
DO NOT use raw filenames like "TA6 11.6.2020.pdf"

{kb_content}
"""


def call_openai(
    text_evidence: str,
    vision_inputs: list,
    api_key: str,
    kb_dir: Optional[str] = None,
    model: str = "gpt-4o-mini",
) -> dict:
    """Call OpenAI API. Returns JSON dict of APSS field values."""
    from openai import OpenAI
    client = OpenAI(api_key=api_key)

    kb_content = load_kb_files(kb_dir) if kb_dir else ""
    system_prompt = JSON_SYSTEM_PROMPT.format(kb_content=kb_content)

    user_content = []
    user_content.append({
        "type": "text",
        "text": f"Analyse this auction pack evidence and return the JSON:\n\n{text_evidence[:15000]}"
    })

    for vi in vision_inputs[:6]:
        user_content.append({
            "type": "text",
            "text": f"[{vi['doc_type'].upper()} page {vi['page_num']}]"
        })
        user_content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/png;base64,{vi['image_b64']}",
                "detail": "low",
            }
        })

    response = client.chat.completions.create(
        model=model,
        max_tokens=4000,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
    )

    raw = response.choices[0].message.content
    try:
        return json.loads(raw)
    except Exception:
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if match:
            return json.loads(match.group())
        return {}


def call_claude(
    text_evidence: str,
    vision_inputs: list,
    api_key: str,
    kb_dir: Optional[str] = None,
    model: str = "claude-sonnet-4-20250514",
) -> dict:
    """Call Claude API. Returns JSON dict of APSS field values."""
    import anthropic
    client = anthropic.Anthropic(api_key=api_key)

    kb_content = load_kb_files(kb_dir) if kb_dir else ""
    system_prompt = JSON_SYSTEM_PROMPT.format(kb_content=kb_content)

    user_content = []
    user_content.append({
        "type": "text",
        "text": f"Analyse this auction pack evidence and return the JSON:\n\n{text_evidence[:15000]}"
    })

    for vi in vision_inputs[:6]:
        user_content.append({
            "type": "text",
            "text": f"[{vi['doc_type'].upper()} page {vi['page_num']}]"
        })
        user_content.append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": "image/png",
                "data": vi["image_b64"],
            }
        })

    response = client.messages.create(
        model=model,
        max_tokens=4000,
        system=system_prompt,
        messages=[{"role": "user", "content": user_content}],
    )

    raw = response.content[0].text
    try:
        return json.loads(raw)
    except Exception:
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if match:
            return json.loads(match.group())
        return {}