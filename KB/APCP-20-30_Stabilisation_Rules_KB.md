# Legal Packs Co-Pilot - Stabilisation and Workflow Rules

## Status
This file is the runtime authority for extraction logic, field decision rules, hierarchy, disclaimer selection, and chat-to-DOCX parity.
It is not property evidence.

## Scope
These rules support the APSS workflow for Medway Law and iamsold.
They govern:
- evidence-based extraction
- field decision logic
- source hierarchy
- disclaimer selection logic
- Council Tax Band lookup exception
- chat-to-DOCX content parity

Technical placeholder replacement, DOCX validity, status rendering mechanics, and disclaimer placement are governed separately by Word_Template_Handling_(APSS).md.
Evidence Ledger process is governed separately by Evidence_Ledger_KB.md.
Disclaimer family routing, condition logic, and mutual exclusions are governed separately by Disclaimer_Routing_Map_KB.md.

## APCP-21 - Controlled external lookup exception (Council Tax only)
External lookups remain prohibited except for Council Tax Band where this is expressly permitted.
Council Tax Band source priority is:
1. uploaded auction-pack evidence
2. approved official external lookup via the approved action

Use the approved Council Tax action only when:
- Council Tax Band is not clearly evidenced in-pack
- the target property address is clearly resolved from pack evidence
- minimum required lookup inputs are available

If no single clear match is returned, or the lookup conflicts with pack evidence, output `Requires manual verification`.
Do not ask a duplicate conversational permission question before invoking the action.

## APCP-25 - Charges accuracy
Ground Rent and Service Charge must be resolved as separate internal facts before being combined into the APSS field.
For each charge, determine one of:
- PAYABLE
- NOT PAYABLE
- UNCLEAR

Only publish a definitive payable amount where both amount and payability are clearly evidenced in-pack.
If evidence conflicts or current payability is ambiguous, output `Requires manual verification` and do not publish a definitive payable amount.
Historic demands, arrears, budgets, reserve fund entries, or generic lease wording do not by themselves prove the current payable amount.

## APCP-26 - Core field completeness and mixed-row status logic

### Mixed-category Key Document Status rows
For mixed rows such as `HMO / Licences / Safety Docs`, resolve status at row level, not sub-scenario level.
If at least one genuine document in that row is present, the row is `Provided`.
Comments must separate:
1. what is present
2. what is not evidenced

### Core completeness rules
- If an EPC document is present, EPC rating must be populated from that EPC.
- Parking Arrangements must be populated where clearly stated in TA6, lease, lease plan, or equivalent direct evidence.
- Water and drainage must be resolved as separate facts first.
- Never invert a positive or negative water-search result.
- Lease Plan is present only if an actual lease plan is included in the pack.
- Planning and Certificates status is presence-only and must not be guessed from indirect references.

### Construction Type
Construction Type must be resolved using the most field-fit source in this priority order:
1. Additional Enquiries or Additional Information explicit whole-property or whole-building wording
2. Fire Risk Assessment or Management Pack explicit building construction wording
3. EPC construction elements only if no stronger field-fit source exists
4. other direct technical wording in-pack

Do not populate Construction Type with a single component description where a stronger whole-building description is clearly evidenced elsewhere.
If the only permitted source wording contains terms such as `assumed`, preserve the source wording exactly.
Do not harden that wording into a cleaner fact.
If no safe field-fit construction wording can be resolved after targeted re-check, output `Requires manual verification`.

## APCP-26D - Referenced but missing is not evidence
A document being mentioned, requested, referred to, or described elsewhere in the pack does not make that document present.
A document is present only if the actual document, image, plan, schedule, notice, certificate, agreement, or copy is included in the uploaded evidence set.

## APCP-27 - Tenure recognition and title relevance
Tenure must be determined only from direct pack evidence such as title register, lease, contract, or special conditions.
A superior freehold or landlord title must not be treated as a sale title unless the pack explicitly confirms it is included in the sale.
Multiple title numbers alone do not create a multi-property sale.

## APCP-28 - Checkbox and scanned-form verification gate
For checkbox, handwritten, or scan-dependent fields:
- clearly marked = extract deterministically
- clearly blank = unanswered
- unclear or unreadable = `Requires manual verification`

Never convert an unclear checkbox into a factual Yes or No statement.

## APCP-29 - Disclaimer selection and contradiction prevention

### Core selection rule
Disclaimer wording must be selected deterministically from APSS_Disclaimer_Library.md and inserted verbatim only.
Disclaimer selection must follow the routing logic defined in Disclaimer_Routing_Map_KB.md.
A generic disclaimer must never be used where a more specific evidenced or missing-document variant applies.
Do not insert any disclaimer whose wording contradicts:
- the resolved document presence status
- the resolved field value
- another disclaimer already selected in the same family
- the evidence summary already stated in the same Comments cell

### Disclaimer routing order
Disclaimer routing must begin only after all of the following are complete:
1. Evidence Ledger (per Evidence_Ledger_KB.md)
2. All APSS field extractions
3. Key Document Status completion
4. Material Flags completion

### Mutual exclusion rules
The following groups are mutually exclusive. Selecting more than one from a mutually exclusive group is a publication error.

**EPC family** — {{epcComments}}
- #06, #07, #08 are mutually exclusive. Select exactly one.
- #08 = EPC absent. #06 = EPC present, rating E or lower. #07 = EPC present, general fallback.

**Vacant possession family** — {{addInfoComments}}
- #03 and #04 are mutually exclusive.
- #04 = seller confirmed error. #03 = no seller confirmation received.

**Leasehold lease document family** — {{leaseInfoComments}}
- #11, #12, #13, #14, #15 are mutually exclusive. Select the most specific one only.

**Leasehold management family** — {{leaseInfoComments}}
- #09, #17, #19, #21, #22 are mutually exclusive. Select the most specific one only.

**Leasehold property type family** — {{leaseInfoComments}}
- #16 and #20 are mutually exclusive.

**Title registration family** — {{titleComments}}
- #77, #78, #79, #80, #81, #82, #83, #84 are mutually exclusive. Select the most specific one only.
- #77 is the general unregistered fallback. Only use it if no more specific unregistered disclaimer applies.

**NHBC family** — {{planningComments}}
- #30 and #31 are mutually exclusive.

**Solar panels**
- #65 and #66 are mutually exclusive (seller-owned: transferring vs removing).
- #47 is mutually exclusive with #65 and #66. #47 applies to leased panels. #65 and #66 apply to seller-owned panels.

**Criminal activity family** — {{materialPropertyNotesComments}}
- #32 and #33 are mutually exclusive.
- #33 and #34 are mutually exclusive.

**Flying freehold family**
- #42 ({{materialPropertyNotesComments}}) and #79 ({{titleComments}}) are mutually exclusive.
- If property is unregistered AND flying freehold suspected: use #79 only.
- If property is registered AND flying freehold suspected: use #42 only.

**Tenancy family** — {{tenancyComments}}
- #71, #72, #73, #74 are mutually exclusive. Select at most one.
- #75 (HMO licence missing) may be added alongside any of #71–#74 if both conditions are independently met.

**Knotweed family** — {{ta6Comments}}
- #41 and #48 are mutually exclusive.

**Probate executors** — {{probateComments}}
- #27 and #28 are mutually exclusive.

**Probate administrators** — {{probateComments}}
- #23 and #24 are mutually exclusive.

**Searches** — {{searchComments}}
- #59 is a fallback only. Do not select #59 if any of #60, #61, #62, #63 already covers the missing item.
- #61 and #62 are mutually exclusive. #61 = search missing. #62 = search present and confirms non-connection.

### Specificity rule
Where multiple disclaimers in the same family could technically apply, always prefer the more specific disclaimer over the more general one.
The general fallback disclaimer in any family must only be used when no more specific disclaimer in that family applies.

### Cross-placeholder contradiction prevention
Before finalising, check the following cross-placeholder pairs for contradiction:

| Check | Rule |
|---|---|
| {{epcStatus}} = Provided | Comments must not contain #08 (EPC missing). |
| {{epcStatus}} = Not applicable | No EPC disclaimer should appear in comments. |
| {{leaseInfoStatus}} = Not applicable | No leasehold disclaimer should appear in comments. |
| {{tenancyStatus}} = Not applicable | No tenancy disclaimer should appear in comments. |
| {{probateStatus}} = Not applicable | No probate disclaimer should appear in comments. |
| {{searchStatus}} = Provided | Comments must not contain missing-search disclaimers #59, #60, #61. |
| {{planningStatus}} = Not applicable | #30 and #31 should not appear. |
| #06 selected | {{flagEpcBelowE}} must be Yes. |
| Any of #71–#75 selected | {{flagOccupiersTenancy}} must be Yes. |
| Any leasehold disclaimer selected and leasehold info incomplete | {{flagLeaseholdInfo}} must be Yes. |
| Any of #12, #56, #57, #77–#84 selected | {{flagTitleDiscrepancies}} or {{flagUnregisteredTitle}} must be Yes as applicable. |

If a contradiction is found, resolve it before publishing.
If the contradiction cannot be cleanly resolved, apply `Requires manual verification` to the affected field and note the conflict.

## APCP-30 - Output parity and evidence hygiene
Chat APSS is the canonical content source for the session.
DOCX must be generated from the exact same resolved field values and disclaimer blocks already used in chat.
At DOCX stage, do not:
- re-read the pack
- re-extract facts
- reinterpret evidence
- change resolved field values
- reroute disclaimer families
- change flag outcomes

User-facing evidence references must use normalised document labels only.
Do not output raw upload filenames, ZIP paths, temporary OCR names, or internal file codes in the APSS.

## APCP-30B - Material Flags must reflect final resolved field state
Material Flags must be derived from the same final resolved fact set used for:
- APSS fields
- Key Document Status comments
- routed disclaimer blocks

If a final resolved field contains a key conflict or manual-verification outcome directly mapped to a flag category, the corresponding flag must not remain `No`.
