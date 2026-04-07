# Disclaimer Routing Map

## Status
This file is a runtime disclaimer selection control layer.
It works alongside APSS_Disclaimer_Library.md.
It does not replace APSS_Disclaimer_Library.md.
Disclaimer wording must always be taken verbatim from APSS_Disclaimer_Library.md only.
This file governs which disclaimer to select and when. Nothing more.

## Core selection rules
1. Work through each family below in order.
2. For each family, evaluate the conditions from top to bottom and stop at the first match.
3. Select at most one disclaimer per family unless the family explicitly permits multiple.
4. Insert verbatim wording from APSS_Disclaimer_Library.md into the TARGET_PLACEHOLDER shown.
5. Never select a disclaimer whose wording contradicts a resolved field value, a status label, or another disclaimer already selected.
6. If no condition in a family is met, select nothing for that family.

---

## FAMILY: EPC
Maximum selections from this family: 1
TARGET_PLACEHOLDER: {{epcComments}}

STEP 1: Is a valid EPC document present in the pack?
- NO → select #08 (EPC missing). STOP.
- YES → continue.

STEP 2: What is the EPC rating?
- F or G → select #06 (EPC rating E or lower). STOP.
- E → select #06 (EPC rating E or lower). STOP.
- A, B, C, or D → select #07 (EPC present, general). STOP.
- Rating unreadable or unclear → select #07 (EPC present, general). STOP.

MUTUAL EXCLUSION: #06, #07, and #08 are mutually exclusive. Never select more than one.

---

## FAMILY: SEARCHES — GENERAL
Maximum selections from this family: 1 (general fallback only; specific search disclaimers are separate)
TARGET_PLACEHOLDER: {{searchComments}}

STEP 1: Are all standard searches present (local authority, water and drainage, environmental)?
- YES → select nothing from this family. STOP.
- NO → identify which specific searches are missing and go to FAMILY: SEARCHES — SPECIFIC below.

STEP 2: If multiple specific searches are missing and no single specific disclaimer covers all of them:
- Select #59 (general searches missing). STOP.

MUTUAL EXCLUSION: Do not select #59 if a more specific search disclaimer (#60, #61, #62, #63) already covers the missing item.

---

## FAMILY: SEARCHES — SPECIFIC
Maximum selections from this family: multiple permitted if different search types are missing
TARGET_PLACEHOLDER: {{searchComments}}

Evaluate each condition independently:

CONDITION A — Local authority search missing:
- Local authority search not present in pack → select #60.

CONDITION B — Water and drainage search missing:
- Water and drainage search not present in pack → select #61.

CONDITION C — Water and drainage search present and confirms not connected to mains drainage:
- Search present AND confirms property is not connected to public sewer → select #62.
- NOTE: #61 and #62 are mutually exclusive. If the search is missing, use #61. If the search is present and reveals non-connection, use #62. Never both.

CONDITION D — Unadopted road or accessway:
- Local authority search present AND indicates serving road/path/accessway is not adopted → select #63.

CONDITION E — All searches missing and no specific disclaimer applies:
- Use #59 only as a fallback when searches are missing and none of the above specific disclaimers apply.

---

## FAMILY: LEASEHOLD — LEASE DOCUMENT
Maximum selections from this family: 1
TARGET_PLACEHOLDER: {{leaseInfoComments}}
PREREQUISITE: Property must be leasehold. Do not select any item from this family for freehold properties.

Evaluate conditions in order and stop at first match:

CONDITION 1 — Missing lease pages:
- Tenure = LEASEHOLD AND pages are confirmed missing from the lease → select #13. STOP.

CONDITION 2 — Lease plan refers to colour but only black and white available:
- Tenure = LEASEHOLD AND lease plan references colour AND only black-and-white copy available → select #11. STOP.

CONDITION 3 — Lease plan referred to but not obtained:
- Tenure = LEASEHOLD AND lease references a plan AND plan not present in pack → select #15. STOP.

CONDITION 4 — Restriction in lease not noted on Title Register:
- Tenure = LEASEHOLD AND restriction appears in lease body AND restriction not noted on Title Register → select #14. STOP.

CONDITION 5 — Discrepancy between Title Register and lease:
- Tenure = LEASEHOLD AND title register description conflicts with lease description → select #12. STOP.

CONDITION 6 — No specific lease document issue:
- None of the above → select nothing from this family.

MUTUAL EXCLUSION: #11, #12, #13, #14, and #15 are mutually exclusive within this family.

---

## FAMILY: LEASEHOLD — MANAGEMENT AND INFORMATION
Maximum selections from this family: 1
TARGET_PLACEHOLDER: {{leaseInfoComments}}
PREREQUISITE: Property must be leasehold (or managed freehold for #09 only).

Evaluate conditions in order and stop at first match:

CONDITION 1 — Managed freehold, no FME1 obtained:
- Tenure = FREEHOLD AND property is on managed estate AND no FME1 or freehold management pack provided → select #09. STOP.

CONDITION 2 — Management pack ordered but not yet received:
- Tenure = LEASEHOLD AND management pack ordered AND not yet received → select #17. STOP.

CONDITION 3 — Seller declined to obtain management pack:
- Tenure = LEASEHOLD AND seller has declined to obtain management pack → select #19. STOP.

CONDITION 4 — Informal resident management:
- Tenure = LEASEHOLD AND property managed informally by residents (no formal management structure) → select #21. STOP.

CONDITION 5 — LPE1 not completed by RTM company:
- Tenure = LEASEHOLD AND LPE1 present AND not completed by a Right to Manage company AND no more specific management disclaimer applies → select #22. STOP.

CONDITION 6 — No management issue identified:
- None of the above → select nothing from this family.

MUTUAL EXCLUSION: #09, #17, #19, #21, and #22 are mutually exclusive within this family.

---

## FAMILY: LEASEHOLD — PROPERTY TYPE
Maximum selections from this family: 1
TARGET_PLACEHOLDER: {{leaseInfoComments}}
PREREQUISITE: Property must be leasehold.

CONDITION 1 — Leasehold house:
- Tenure = LEASEHOLD AND property type = HOUSE → select #16. STOP.

CONDITION 2 — Subject to a noted lease:
- Property is subject to a noted lease (leasehold title unregistered, noted on freehold) → select #20. STOP.

CONDITION 3 — No specific property type issue:
- None of the above → select nothing from this family.

---

## FAMILY: LEASEHOLD — LEASE TERM
Maximum selections from this family: 1
TARGET_PLACEHOLDER: {{leaseInfoComments}}

CONDITION 1 — Remaining lease term under 85 years:
- Tenure = LEASEHOLD AND remaining lease term is under 85 years → select #18. STOP.

CONDITION 2 — Lease term acceptable:
- None of the above → select nothing from this family.

SECONDARY NOTE: If the short lease also warrants a material property note, additionally select #38 into {{materialPropertyNotesComments}}. These two do not conflict as they route to different placeholders.

---

## FAMILY: LEASEHOLD — TA7
Maximum selections from this family: 1
TARGET_PLACEHOLDER: {{leaseInfoComments}}

CONDITION 1 — TA7 present but incomplete:
- TA7 is present AND has unanswered or incomplete sections → select #52. STOP.

CONDITION 2 — TA7 not applicable or complete:
- None of the above → select nothing from this family.

---

## FAMILY: TITLE — REGISTRATION STATUS
Maximum selections from this family: 1
TARGET_PLACEHOLDER: {{titleComments}}

Evaluate conditions in order and stop at first match:

CONDITION 1 — Unregistered, unreceipted legal charge:
- Property is unregistered AND title bundle contains an unreceipted or incorrectly receipted mortgage deed or charge → select #84. STOP.

CONDITION 2 — Unregistered, inadequate deed description:
- Property is unregistered AND title deeds do not contain an adequate description of the property → select #82. STOP.

CONDITION 3 — Unregistered, only copies of deeds available:
- Property is unregistered AND seller holds copies only (not original deeds) → select #81. STOP.

CONDITION 4 — Unregistered, missing or unavailable deeds:
- Property is unregistered AND deeds referred to in the title bundle are missing or unavailable → select #83. STOP.

CONDITION 5 — Unregistered, address not reflected in deeds:
- Property is unregistered AND current address is not reflected in title deeds → select #78. STOP.

CONDITION 6 — Unregistered, boundary discrepancy between deeds plan and site:
- Property is unregistered AND discrepancy exists between deeds plan and physical boundary → select #80. STOP.

CONDITION 7 — Unregistered, flying freehold not in deeds:
- Property is unregistered AND there is reason to believe a flying freehold exists not reflected in deeds → select #79. STOP.

CONDITION 8 — Unregistered, no more specific unregistered disclaimer applies:
- Property is unregistered AND none of conditions 1–7 apply → select #77. STOP.

CONDITION 9 — Possessory title:
- Title class = POSSESSORY → select #57. STOP.

CONDITION 10 — No registration issue:
- None of the above → select nothing from this family.

MUTUAL EXCLUSION: #77, #78, #79, #80, #81, #82, #83, #84 are mutually exclusive within this family. Select the most specific applicable disclaimer only.

---

## FAMILY: TITLE — BOUNDARIES AND EXTENT
Maximum selections from this family: 1
TARGET_PLACEHOLDER: {{titleComments}}

CONDITION 1 — Multiple sale titles, boundaries require clarification:
- Pack includes multiple Land Registry title numbers forming the sale AND boundaries/extent require clarification → select #02. STOP.

CONDITION 2 — Transfer of part:
- Sale is a transfer of part (only part of a title is being sold) → select #76. STOP.

CONDITION 3 — Pending Land Registry applications:
- There are pending applications lodged with HM Land Registry → select #56. STOP.

CONDITION 4 — Short ownership period:
- Seller has owned the property for less than six months → select #64. STOP.

CONDITION 5 — No title boundary issue:
- None of the above → select nothing from this family.

NOTE: #02, #76, #56, and #64 are separate concerns and may co-exist if each condition is independently met. In that case append in library order to the same placeholder.

---

## FAMILY: ADDITIONAL INFORMATION — BOUNDARIES
Maximum selections from this family: 1
TARGET_PLACEHOLDER: {{addInfoComments}}

CONDITION 1 — Boundaries marked incorrect in error, seller confirmed correct:
- Additional Enquiries Form states boundaries are not correct AND seller subsequently confirmed this was marked in error → select #01. STOP.

CONDITION 2 — No boundary correction issue:
- None of the above → select nothing from this family.

---

## FAMILY: ADDITIONAL INFORMATION — VACANT POSSESSION
Maximum selections from this family: 1
TARGET_PLACEHOLDER: {{addInfoComments}}

Evaluate conditions in order and stop at first match:

CONDITION 1 — Conflicting Q11.5, seller confirmed error:
- Additional Enquiries Form Q11.5 marked No AND this conflicts with vacant possession marketing AND seller has confirmed the response was an error → select #04. STOP.

CONDITION 2 — Conflicting Q11.5, no seller confirmation:
- Additional Enquiries Form Q11.5 marked No AND this conflicts with vacant possession marketing AND no seller confirmation received → select #03. STOP.

CONDITION 3 — No vacant possession conflict:
- None of the above → select nothing from this family.

MUTUAL EXCLUSION: #03 and #04 are mutually exclusive.

---

## FAMILY: ADDITIONAL INFORMATION — PROPERTY SPLIT
Maximum selections from this family: 1
TARGET_PLACEHOLDER: {{addInfoComments}}

CONDITION 1 — Property split into flats or apartments:
- Pack evidence confirms property has been split into flats or apartments → select #58. STOP.

CONDITION 2 — No split:
- None of the above → select nothing from this family.

---

## FAMILY: TA6 — INSURANCE
Maximum selections from this family: 1
TARGET_PLACEHOLDER: {{ta6Comments}}

CONDITION 1 — TA6 confirms not currently insured:
- TA6 present AND seller has confirmed property is not currently insured → select #10. STOP.

CONDITION 2 — No insurance issue:
- None of the above → select nothing from this family.

---

## FAMILY: TA6 — JAPANESE KNOTWEED
Maximum selections from this family: 1
TARGET_PLACEHOLDER: {{ta6Comments}}

Evaluate conditions in order and stop at first match:

CONDITION 1 — Knotweed confirmed present or previously present:
- TA6 or other pack evidence confirms Japanese Knotweed is present or has previously affected the property → select #41. STOP.

CONDITION 2 — Knotweed marked Not Known:
- TA6 response to knotweed question is "Not Known" → select #48. STOP.

CONDITION 3 — No knotweed issue:
- None of the above → select nothing from this family.

MUTUAL EXCLUSION: #41 and #48 are mutually exclusive.

---

## FAMILY: TA6 — PARKING
Maximum selections from this family: 1
TARGET_PLACEHOLDER: {{ta6Comments}}

CONDITION 1 — TA6 does not disclose parking arrangements:
- TA6 present AND parking arrangements not disclosed within TA6 → select #49. STOP.

CONDITION 2 — No parking disclosure issue:
- None of the above → select nothing from this family.

---

## FAMILY: TA6 — INCOMPLETE FORM
Maximum selections from this family: 1
TARGET_PLACEHOLDER: {{ta6Comments}}

CONDITION 1 — TA6 present but incomplete or contains multiple Not Known responses:
- TA6 present AND incomplete or contains multiple "Not Known" responses → select #50. STOP.

CONDITION 2 — TA6 complete:
- None of the above → select nothing from this family.

NOTE: #10, #41, #48, #49, and #50 all route to {{ta6Comments}} but address different topics. They may co-exist if independently triggered. Append in library number order. However, do not select #50 if the only incompleteness is the knotweed Not Known response already covered by #48.

---

## FAMILY: TA10 — INCOMPLETE FORM
Maximum selections from this family: 1
TARGET_PLACEHOLDER: {{ta10Comments}}

CONDITION 1 — TA10 present but incomplete or unclear:
- TA10 present AND incomplete or unclear → select #51. STOP.

CONDITION 2 — TA10 complete or not applicable:
- None of the above → select nothing from this family.

---

## FAMILY: PROBATE AND LRTS
Maximum selections from this family: 1 per sub-type

TARGET_PLACEHOLDER: {{probateComments}}

Each condition below is independent. Multiple may apply if the pack supports it.

CONDITION A — Sale subject to death certificate:
- Sale is expressly subject to a death certificate → select #68.

CONDITION B — Sale subject to marriage certificate:
- Sale is expressly subject to a marriage certificate → select #69.

CONDITION C — Sale subject to change of name documentation:
- Sale is expressly subject to change of name documentation → select #70.

CONDITION D — Coroner's report accepted, death certificate not yet available:
- Coroner's report accepted as evidence of death AND formal death certificate not yet available → select #05.

CONDITION E — Sold by executors, probate granted:
- Property sold by executors AND probate has been granted → select #27.

CONDITION F — Sold by executors, probate not yet granted:
- Property sold by executors AND probate not yet granted → select #28.

CONDITION G — Sold by administrators, Letters of Administration granted:
- Property sold by administrators AND Letters of Administration have been granted → select #23.

CONDITION H — Sold by administrators, Letters of Administration not yet granted:
- Property sold by administrators AND Letters of Administration not yet granted → select #24.

CONDITION I — Court of Protection order:
- Property sold under a Court of Protection order → select #25.

CONDITION J — Power of Attorney:
- Property sold by attorneys under LPA, EPA, or similar → select #26.

CONDITION K — Property information forms not completed by all sellers:
- Forms not completed or signed by all required sellers, executors, or attorneys → select #29.

MUTUAL EXCLUSIONS within this family:
- #23 and #24 are mutually exclusive (Letters of Administration either granted or not).
- #27 and #28 are mutually exclusive (probate either granted or not).
- #05 is independent of #27/#28 and may co-exist if both conditions are met.

---

## FAMILY: PLANNING AND CERTIFICATES
Maximum selections from this family: multiple permitted if independently triggered
TARGET_PLACEHOLDER: {{planningComments}}

CONDITION A — NHBC certificate present:
- NHBC certificate copy is included in the pack → select #30.

CONDITION B — NHBC certificate expected but not provided:
- Property is newly built or NHBC certificate is expected AND no copy is in the pack → select #31.
- MUTUAL EXCLUSION: #30 and #31 are mutually exclusive.

CONDITION C — Solar panels, seller-owned, transferring to buyer:
- Solar panels present AND seller owns them AND will transfer to buyer on completion → select #65.

CONDITION D — Solar panels, seller-owned, being removed:
- Solar panels present AND seller owns them AND will be removed before completion → select #66.
- MUTUAL EXCLUSION: #65 and #66 are mutually exclusive.

CONDITION E — Warranty documents referenced but not provided:
- Warranty documents referenced or expected AND copies not included → select #53.

CONDITION F — Planning permission or building regulation documents missing:
- Planning permission and/or building regulation documents missing from pack → select #54.

---

## FAMILY: MATERIAL PROPERTY NOTES
Maximum selections from this family: multiple permitted if independently triggered
TARGET_PLACEHOLDER: {{materialPropertyNotesComments}}

Each condition is independent:

CONDITION A — Criminal activity at property:
- Pack evidence indicates criminal activity may have taken place at the property (not death-related) → select #32.

CONDITION B — Death at property due to criminal activity:
- Pack evidence indicates a death occurred at the property as a result of criminal activity → select #33.

CONDITION C — Death at property due to natural causes:
- Pack evidence indicates a death occurred at the property due to natural causes → select #34.

CONDITION D — Vendor incarcerated:
- Pack evidence indicates the vendor is currently incarcerated in connection with criminal activity → select #35.

CONDITION E — Structural issues or subsidence:
- Pack evidence confirms or suggests structural issues or subsidence → select #36.

CONDITION F — Damp or moisture-related defects:
- Pack evidence confirms or suggests damp or moisture-related defects → select #37.

CONDITION G — Short lease (material notes version):
- Remaining lease term under 85 years AND this warning also belongs in material property notes → select #38.
- NOTE: #38 and #18 may both be selected as they route to different placeholders.

CONDITION H — Cladding:
- Pack evidence indicates the property has cladding → select #39.

CONDITION I — Non-standard construction:
- Pack evidence confirms or suggests non-standard construction type → select #40.

CONDITION J — Flying freehold (not unregistered):
- There is reason to believe the property has a flying freehold AND this is not the unregistered-title variant → select #42.
- NOTE: If property is unregistered AND flying freehold, use #79 (Title family) not #42.

CONDITION K — Bankruptcy notice on title:
- A bankruptcy notice is lodged against the title → select #43.

CONDITION L — Not connected to mains drainage (material notes):
- Pack evidence confirms property is not connected to mains drainage AND this belongs in material notes → select #44.
- NOTE: If water and drainage search is also present and confirms this, additionally select #62 into {{searchComments}}.

CONDITION M — Adverse possession risk:
- Pack evidence indicates a risk of adverse possession → select #45.

CONDITION N — Rentcharge:
- Property is subject to a rentcharge → select #46.

CONDITION O — Solar panels under lease or contractual arrangement:
- Solar panels are installed under a lease or similar agreement (not seller-owned outright) → select #47.
- NOTE: #47 and #65/#66 are mutually exclusive. #47 applies to leased panels; #65/#66 apply to seller-owned panels.

CONDITION P — Commercial/short-term letting use:
- Property has been used for short-term letting or is registered as commercial/business rates → select #55.

CONDITION Q — Sold as seen:
- Property is explicitly being sold "as seen" → select #67.

MUTUAL EXCLUSIONS within this family:
- #32 and #33 are mutually exclusive (criminal activity with or without death).
- #33 and #34 are mutually exclusive (criminal death vs natural death).
- #47 is mutually exclusive with #65 and #66.
- #42 and #79 are mutually exclusive (choose based on registered/unregistered status).

---

## FAMILY: TENANCY
Maximum selections from this family: 1 primary + #75 if HMO
TARGET_PLACEHOLDER: {{tenancyComments}}

Evaluate primary conditions in order and stop at first match:

CONDITION 1 — HMO, licence not provided:
- Property is or is being sold as an HMO AND HMO licence documents not provided → select #75.
- NOTE: #75 may be selected alongside the applicable tenancy disclaimer below if both conditions are met.

CONDITION 2 — Tenanted with Section 21 notice included in pack:
- Property tenanted AND Section 21 notice has been served AND copy is in the pack → select #73. STOP.

CONDITION 3 — Tenanted with Section 21 notice referenced but not in pack:
- Property tenanted AND Section 21 notice has been served AND copy is NOT in the pack → select #74. STOP.

CONDITION 4 — Occupied by relative of seller:
- Occupier is a relative of the seller (with or without formal tenancy) → select #72. STOP.

CONDITION 5 — Tenanted, no more specific tenancy disclaimer applies:
- Property is tenanted AND none of conditions 2–4 apply → select #71. STOP.

CONDITION 6 — Vacant:
- Property is vacant and no tenancy issue exists → select nothing from this family.

MUTUAL EXCLUSIONS: #71, #72, #73, and #74 are mutually exclusive (select only one). #75 may accompany any of them.

---

## Final routing check

Before publishing, verify:
1. No placeholder has received a disclaimer that contradicts its resolved field value.
2. No two disclaimers in the same placeholder family contradict each other.
3. Every selected disclaimer number corresponds to an item in APSS_Disclaimer_Library.md.
4. Wording has been taken verbatim from APSS_Disclaimer_Library.md, not paraphrased.
5. No disclaimer has been selected based on a referenced-but-missing document (per APCP-26D).
6. No placeholder contains duplicate disclaimer blocks.
