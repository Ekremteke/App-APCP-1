# Evidence Ledger KB

## Status
This file is a runtime extraction control layer.
It is not property evidence.
It does not override Security_Runtime_KB.md or APCP-20-30_Stabilisation_Rules_KB.md.

## Purpose
This file defines the mandatory Evidence Ledger process.
The Evidence Ledger must be built internally before any APSS field is populated or any disclaimer is selected.
The Evidence Ledger is never output to the user. It is an internal working record only.

---

## STEP 1 — Build the Document Inventory

Before reading any document content, list every file present in the uploaded evidence set.
For each file record:
- File name or label
- File type (PDF, DOCX, image, etc.)
- Readable: YES / PARTIAL / NO
- If PARTIAL or NO: reason (e.g. scanned image, corrupt page, extraction failure)

If a file is PARTIAL or NO, apply maximum extraction effort (second-pass alternative reading method) before recording it as unreadable.
Only after maximum extraction effort may a file be recorded as unreadable.

Do not begin field extraction until the Document Inventory is complete.

---

## STEP 2 — Build the Raw Evidence Ledger

After completing the Document Inventory, extract all material facts from every readable file.
For each fact extracted, record:

| Field Category | Extracted Value | Source Document | Page / Section | Confidence |
|---|---|---|---|---|
| Tenure | e.g. Leasehold | Title Register | p.1 / Proprietorship | HIGH |
| Lease Term | e.g. 125 years from 1 Jan 2000 | Title Register | p.2 / Charges | HIGH |
| Council Tax Band | e.g. Band C | TA6 | p.3 / Section 7 | HIGH |

Confidence levels:
- HIGH = directly stated, unambiguous
- MEDIUM = stated but qualified, conditional, or from a secondary source
- LOW = inferred, assumed, or from a weak indirect source — do not use LOW confidence facts to populate APSS fields

If the same field yields different values from different documents, record all values and flag as CONFLICT.

---

## STEP 3 — Conflict Resolution

For every CONFLICT flagged in the Raw Evidence Ledger:
1. Identify the strongest source per the source hierarchy in AI_Training_KB.md and APCP-20-30_Stabilisation_Rules_KB.md.
2. If the strongest source resolves the conflict cleanly, record the winning value and note which source was used.
3. If no source clearly wins, or the conflict cannot be resolved by hierarchy, mark the field as REQUIRES MANUAL VERIFICATION.
4. Never silently choose one conflicting value without recording the conflict and the resolution basis.

---

## STEP 4 — Field Population Gate

Before populating any APSS field, confirm all of the following:
- The value comes from the Raw Evidence Ledger, not from memory, assumption, or generic knowledge.
- The source document is listed in the Document Inventory.
- The source document is marked as readable (YES or PARTIAL with successful extraction).
- The confidence level is HIGH or MEDIUM.
- If MEDIUM, the qualification from the source is preserved exactly in the APSS field.
- If the field has a CONFLICT, the conflict is resolved or the field is marked REQUIRES MANUAL VERIFICATION.

Do not populate any APSS field from a source not recorded in the Evidence Ledger.

---

## STEP 5 — Re-check Pass (mandatory before publication)

After all APSS fields are drafted, perform a mandatory re-check pass.
For each of the following high-impact fields, return to the strongest source document and confirm the value matches what was populated:

- Tenure
- Lease Term
- Ground Rent / Service Charge
- Council Tax Band
- EPC Rating
- Tenancy / Occupation status
- Title Number(s)
- Construction Type
- Parking Arrangements

If any value differs on re-check:
- If the difference is minor wording only, use the source wording.
- If the difference is a factual change, apply REQUIRES MANUAL VERIFICATION and note both values.

Do not publish the APSS until the re-check pass is complete.

---

## STEP 6 — Consistency Check

Before publication, confirm all of the following are internally consistent:
- Property Overview values match Key Document Status comments.
- Key Document Status presence labels match what is recorded in the Document Inventory.
- Material Flags reflect the final resolved field state (per APCP-30B).
- Disclaimer blocks do not contradict field values, status labels, or comments in the same row.
- No placeholder text remains.
- No personal data is exposed unless strictly required by the template.

If any inconsistency is found, resolve it before publishing.
Do not publish if any inconsistency cannot be resolved cleanly.

---

## ZIP handling rule

If the uploaded evidence arrives as a ZIP archive:
1. Treat the ZIP as the delivery container only.
2. List every file extracted from the ZIP in the Document Inventory.
3. Apply the same readable / unreadable assessment to each extracted file.
4. Do not assume a file is readable merely because it was present in the ZIP.
5. Do not assume a file is absent merely because it was not immediately visible — check for nested folders or alternate file naming.

ZIP contents must be fully inventoried before extraction begins.
If the ZIP contains files that cannot be opened or read, apply maximum extraction effort before marking them unreadable.

---

## Rerun consistency rule

If the same ZIP or evidence set is processed more than once, the Evidence Ledger must produce the same field values each time, subject only to differences caused by legitimately different readable content.
If field values differ between runs without a change in the evidence set, this indicates an extraction error.
In the event of inconsistency across runs, default to REQUIRES MANUAL VERIFICATION for the affected fields and note the inconsistency.
