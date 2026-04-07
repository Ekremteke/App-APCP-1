# AI Training KB

## Status
This file is a behavioural reinforcement layer.
It is not the primary runtime control layer.
It must not override Security_Runtime_KB.md, APCP-20-30_Stabilisation_Rules_KB.md, or Word_Template_Handling_(APSS).md.
It is not property evidence.

## Purpose
This file exists to prevent recurring APSS defects.
Use it as a defect-lock and field-priority reinforcement layer.
It incorporates defects identified during UAT testing and ongoing quality review.

## Golden rule
Never write any property fact unless it is supported by permitted evidence in the uploaded pack or by a separately permitted controlled action explicitly allowed by the authority KB.

## Absolute anti-hallucination rule
Never:
- fabricate facts
- assume missing values
- guess likely values
- fill silent fields with defaults
- convert generic background text into property facts
- convert user wording into evidence
- use previous packs as evidence
- output sensible defaults such as `0%`, `0`, `No`, `None`, `Not applicable`, `Allocated parking`, `Brick and block`, or similar unless directly evidenced or expressly permitted by runtime rules

## Referenced-but-missing rule
If the pack says a document exists, but the actual document is not in the evidence set, it is not provided and its contents are not evidenced.
Do not treat it as present merely because another document refers to it.

## Silence does not equal No
Absence of evidence is not evidence of:
- no issue
- no occupier
- no dispute
- no planning matter
- no cladding
- no HMO issue
- no safety issue
- no charge
- not applicable

---

## Field source priority map

### Council Tax Band
1. direct pack evidence
2. approved Council Tax action

If the pack does not explicitly state the band, but the target property address is clearly resolved from pack evidence, the approved action is mandatory before publish.
Do not downgrade a mandatory action to a manual-review shortcut.

### Construction Type
1. Additional Enquiries Form or Additional Information Form explicit whole-property or whole-building wording
2. Fire Risk Assessment or Management Pack explicit building construction wording
3. EPC construction elements only if no stronger field-fit source exists
4. other direct technical wording in-pack

The Additional Enquiries Form question "Is the property constructed of brick or stone?" is direct priority-1 evidence. Do not skip it.
If the permitted source wording includes `assumed`, preserve that wording exactly.
Do not invent `assumed` wording where the source does not use it.
Do not harden source uncertainty into a cleaner fact.

### Ground Rent
1. TA7
2. Management Pack or LPE1
3. Buyer Pack Summary Note

If values conflict, surface the evidenced values and mark `Requires manual verification`.
If TA7 or seller forms confirm ground rent is NOT payable, do not populate a ground rent figure.

### Service Charge
1. Management Pack or LPE1
2. TA7
3. TA6
4. Buyer Pack Summary Note

If values conflict, surface the evidenced values and mark `Requires manual verification`.
The Management Pack is the primary source for the current annual service charge figure. Do not leave service charge blank if the Management Pack clearly states a figure.

### Tenancy and Occupation
1. tenancy agreement
2. TA6
3. Additional Information Form
4. Buyer Pack Summary Note
5. correspondence

Do not overstate the sale state.
Do not treat a referenced but missing Section 21 notice as documentary proof of valid notice.

### Shared Ownership Percent
Direct percentage evidence only.
If no percentage is evidenced, do not output `0%`.

### Listed and Conservation
1. local authority search
2. TA6

### Parking
1. lease or lease plan
2. TA6
3. management pack

### Lease Term
1. leasehold title register
2. lease

---

## DEFECT LOCKS — FIELD LEVEL

### DL-01: EPC rating must be populated when EPC is present
If EPC Key Document Status = ✅ Provided, the EPC rating MUST be populated in the Property Overview.
Do not mark EPC as ✅ Provided and leave the EPC rating blank or absent from the Property Overview.
Source: EPC document — the rating letter (A through G) must be extracted directly.
UAT reference: Defects 4a, 5, 8a (multiple testers), confirmed in current pack review.

### DL-02: EPC rating must appear in Key Document Status comments before disclaimers
When EPC is provided, the first line of {{epcComments}} must state the rating with evidence.
Format: `EPC rating: [X]. Evidence: EPC p.1 / Energy rating.`
Place this before any disclaimer wording.
User finding confirmed.

### DL-03: Construction Type — check Additional Enquiries Form first
The Additional Enquiries Form question "Is the property constructed of brick or stone?" is priority-1 evidence.
Always check this question before concluding Construction Type is unknown.
Also check the Management Pack Fire Risk Assessment for a whole-building description.
UAT reference: Defects 1b (first batch), 8b.

### DL-04: Planning & Certificates — correct status decision
Follow this decision tree:
- Seller disclosed no works requiring planning in TA6 4.1 AND no planning issues in TA6 4.5 AND no works in Additional Enquiries → ✅ Not applicable.
- Seller disclosed works AND planning/BR documents are in the pack → ✅ Provided.
- Seller disclosed works AND planning/BR documents are NOT in the pack → ❌ requires manual review. Use disclaimer #54.
Do NOT mark ❌ and trigger #54 merely because no planning documents exist in the pack. Only trigger if seller disclosed works requiring such documents.
Current pack finding confirmed.

### DL-05: Rentcharge — always check LH Register Charges Register (C section)
For every leasehold property, re-read the C: Charges Register of the Leasehold Title Register before publishing.
If any entry mentions a reservation of a rentcharge, trigger disclaimer #46 in {{materialPropertyNotesComments}}.
Do not omit this check.
Current pack finding confirmed: LH Register p.3, entry 3.

### DL-06: Cladding — cross-check TA7 5.8 AND Management Pack
For leasehold flats, always check:
1. TA7 question 5.8 — cladding or building safety risk defects
2. Management Pack building element schedule or property description — any mention of cladding, cedar cladding, external wall system materials
If either source evidences cladding, trigger disclaimer #39 in {{materialPropertyNotesComments}}.
The presence of an EWS1 certificate does not eliminate #39. EWS1 assesses fire risk; #39 informs buyers cladding is present.
Current pack finding: MP p.152 — "External brickwork: Stone and cedar cladding".

### DL-07: LPE1 completion — always check who completed it
For leasehold properties, check who completed the LPE1.
If a managing agent or management company (not an RTM company) completed it → trigger #22.
If an RTM company completed it → do not trigger #22.
Current pack finding confirmed: Complete Property Management Solutions Ltd (managing agent, not RTM).

### DL-08A: TA6 incomplete form — always check for #50 trigger
Before finalising the TA6 Key Document Status row, check whether the TA6 has unanswered questions or multiple "Not Known" responses.
If TA6 is present AND incomplete or contains multiple "Not Known" responses, trigger disclaimer #50 in {{ta6Comments}}.
Do not leave the TA6 comments cell empty when the form is visibly incomplete.
Exception: if the only incompleteness is the knotweed "Not Known" response already covered by #48, do not also trigger #50.
Current pack finding confirmed: TA6 contains multiple incomplete sections.

### DL-08: Environmental search — always note if missing
If the environmental search is not present in the pack, add a plain-text note in {{searchComments}} even when other searches are present.
Use this exact wording: "An environmental search is not included in this pack. Prospective buyers are strongly advised to obtain this independently before bidding."
Do not use disclaimer #59 for a missing environmental search if other searches are present.
Current pack finding confirmed.

### DL-09: Japanese Knotweed — verify actual TA6 checkbox state
Before triggering any knotweed disclaimer, verify the actual TA6 knotweed answer:
- Yes → use #41
- Not Known → use #48
- No → do NOT use any knotweed disclaimer
Do not trigger a knotweed disclaimer based on indirect references or assumption.
UAT reference: Defects 8b (first batch), 7, 18 — false positives across multiple test cases.

### DL-10: Solar panels — verify actual seller declaration
Verify TA6 section 4.6 before triggering any solar panel disclaimer.
- 4.6 Yes → determine ownership type and select appropriate disclaimer
- 4.6 No or blank → do NOT trigger any solar panel disclaimer
UAT reference: Defect 11 — solar panels incorrectly added.

### DL-11: Water search result — must not be inverted
Extract the actual stated finding from the water and drainage search. Do not invert it.
If the search confirms connected to mains → state connected.
If the search confirms not connected → state not connected and trigger #62.
UAT reference: Defect 6 — result inverted, property stated as not connected when search confirmed it is connected.

### DL-12: Leasehold house recognition
A leasehold house is a distinct property type.
Before selecting any management pack disclaimer, determine property type.
If property is a leasehold house: do not apply flat-based management disclaimers (#17, #19, #22). Always trigger #16.
UAT reference: Defects 2a, 8a — leasehold house not recognised, wrong management pack disclaimer applied.

### DL-13: Management pack disclaimer — correct variant
Determine the exact management pack status from pack evidence before selecting a disclaimer:
- Management pack is in the pack → ✅ Provided, no management pack disclaimer needed
- Ordered but not yet received → use #17
- Seller declined to obtain → use #19
- LPE1 not completed by RTM → use #22
- Managed freehold, no FME1 → use #09
Never select #19 unless there is direct evidence the seller declined to request a management pack.
UAT reference: Most frequently occurring defect across all test batches (Defects 3, 7, 4a, 6a, 8a, 11d, 13, 14b, 16c, 21a, 29a, 1d, 4b, 8b and others).

### DL-14: Tenancy disclaimer — correct variant based on S21 status
Before selecting a tenancy disclaimer, determine S21 status:
- S21 notice copy IS in the pack → use #73
- S21 notice referenced but copy NOT in pack → use #74
- Occupier is a relative of seller → use #72
- Tenanted, none of the above → use #71
Never use #71 where a more specific S21 disclaimer applies.
UAT reference: Defect 5b — general tenancy disclaimer used instead of S21 notice served disclaimer.

### DL-15: Probate and LRTS — always check for sale authority
For every property, check whether the sale is by executors, administrators, attorneys, or Court of Protection.
Check: probate documents, LPA documents, Buyer Pack Summary Note, correspondence, TA6, Additional Enquiries Form.
Do not omit probate or LRTS disclaimers when evidence confirms representative sale.
UAT reference: Defects 29b, 33a (first batch), 4 (third batch), 9a, 10 — missed across multiple test batches.

### DL-16: Parking — always read TA6 section 9.1
Populate Parking Arrangements whenever TA6 section 9.1 contains a disclosed arrangement.
Only trigger disclaimer #49 if TA6 9.1 is genuinely blank or unanswered.
Do not trigger #49 if parking is stated in TA6 9.1.
UAT reference: Defects 14a, 6d, 13 — parking missed or #49 wrongly triggered.

### DL-17: Multiple title numbers — FH title is not a sale title
For leasehold properties, the FH register is the landlord's title, present for reference only.
Do not treat the FH register as a second sale title.
Do not trigger disclaimer #02 solely because FH and LH registers are both present.
Only trigger #02 if the pack explicitly confirms multiple titles together form the sale extent.
UAT reference: Defects 3a, 16b, 22 — freehold title incorrectly treated as additional sale title.

### DL-18: File names must not appear in user-facing output
Evidence anchors must use normalised document labels only.
Correct: "LH Title Register", "TA6", "Management Pack", "EPC", "Local Authority Search".
Prohibited: any raw filename, ZIP path, or internal file code such as "Title_Plan_MM92604.pdf", "LH - Register - MAN113127.pdf", "3226952 27907286 PLAS_Template.pdf".
UAT reference: Defects 1a, 1b, 2a, 2b, 3a, 3b (UAT batch 3) — file codes appeared in evidence fields.

### DL-19: Lease plan presence rule
Mark Lease Plan as ✅ Provided only if an actual lease plan image or document is present in the pack.
Do not mark as provided because the lease refers to a plan.
UAT reference: Defect 1c (UAT batch 3).

### DL-20: Low lease term disclaimer
If remaining lease term is under 85 years, trigger disclaimer #18 in {{leaseInfoComments}}.
Also consider #38 in {{materialPropertyNotesComments}} if the short lease warrants a material property note.
UAT reference: Defect 16d — low lease term disclaimer missed.

### DL-21: Ground rent — do not include if not payable
If seller confirms ground rent is not payable, do not populate a ground rent figure in the APSS.
The Service Charges / Ground Rent field must reflect the evidenced payability status accurately.
UAT reference: Defect 7 (first batch) — ground rent figure included when seller confirmed not payable.

### DL-22: PIF rows must be present in both chat APSS and DOCX
TA6, TA7, and TA10 Key Document Status rows must be populated in the chat APSS.
When converting to DOCX, these rows must carry through from the chat APSS.
Do not omit PIF rows in the DOCX that were populated in the chat.
UAT reference: Defect 1 (second batch), 16c — PIF details excluded from DOCX.

---

## DEFECT LOCKS — DOCX OUTPUT

### DL-23: DOCX must use APSS_Simple_Template exactly
When producing the DOCX version of the APSS, the base document must be APSS_Simple_Template.docx.
Do not create a new Word document from scratch.
Do not use a different template, layout, or structure.
The template contains logos, header design, table formatting, static boilerplate, and footer elements that must be preserved exactly.
All placeholder values are replaced with resolved APSS field values from the chat APSS.
No new sections, tables, rows, or formatting may be added.
No existing sections, tables, rows, or static text may be removed or restyled.
Producing a DOCX that does not match the template structure and visual appearance is a publication error.
User finding confirmed.

### DL-24: DOCX content must match chat APSS exactly
Per APCP-30: DOCX is generated from the exact same resolved field values and disclaimer blocks used in the chat APSS.
Do not re-extract, re-interpret, or change any field value at DOCX stage.

---

## DEFECT LOCKS — TITLE AND TENURE

### DL-25: Cladding and EWS1 must be noted separately
If cladding is evidenced, trigger #39 regardless of EWS1 outcome.
If an EWS1 certificate is present, note it in HMO/Licences/Safety Docs comments as a document presence.
These are two separate items and must not be conflated.

---

## One-line behavioural summary
If it is not clearly evidenced, do not write it.
If it is conflicted, do not resolve it by guesswork.
If it is missing, say it is missing.
If an approved action is mandatory, run it before publish.
If a defect lock above applies, follow it without exception.
