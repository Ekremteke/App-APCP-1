# APSS Word Template Handling

## Status
This file governs technical APSS rendering mechanics only.
It does not govern extraction logic, evidence interpretation, source hierarchy, or disclaimer selection.
It is not property evidence.

## Scope
This file governs:
- placeholder replacement behaviour
- DOCX validity checks
- status label rendering rules by table and column
- disclaimer placement format for already selected disclaimers

## Placeholder replacement scope
Placeholder replacement must run across:
- paragraphs
- tables
- nested tables
- repeated header rows
- multi-page tables
- section breaks
- header and footer regions if present

Placeholders split across runs, rows, or cells must be reconstructed as a single logical placeholder before replacement.

## DOCX validity rule
DOCX output is invalid unless:
- all placeholder replacement has completed successfully
- no `{{` or `}}` remain anywhere
- Key Document Status placeholders are populated correctly
- already triggered disclaimers are placed into the correct comments cells

## Fallback rule
If valid values exist but a placeholder fails due to Word structure, regenerate using table-aware placeholder replacement logic.
Do not mark a field missing unless the information is genuinely absent.

## Approved status labels
Approved user-facing labels are limited to:
- `Provided`
- `Requires manual verification`
- `Information not available in pack - requires manual review`
- `Not applicable`

Do not introduce any additional status-style label.
Do not allow template-external markers.

## Scope lock for status labels
Status labels may be used only where the template expects them.
For Key Document Status, output exactly one label per row.
For Material Flags, output only `Yes` or `No`.
Do not leak document-style status labels into ordinary scalar fields unless the template explicitly defines that field as a status field.

## Disclaimer placement only
This file governs disclaimer placement only, not disclaimer selection.
A disclaimer may be written only into its exact target placeholder.
If nothing routes to a placeholder, leave it blank.

## Multiple disclaimer blocks to the same placeholder
If multiple triggered disclaimers route to the same placeholder:
- append in disclaimer-library order
- do not deduplicate unless the same disclaimer block would be inserted twice with identical `TITLE + TARGET_PLACEHOLDER + verbatim wording`
- separate blocks with one blank line

## Post-render QA gate
Reject and regenerate if any of the following occur:
- a row is marked `Provided` but its routed disclaimer says the same document class is missing
- the same comments cell contains contradictory disclaimer blocks
- any user-facing evidence anchor contains unresolved placeholder-style evidence text
- a field says `Requires manual verification` but the matching Material Flag remains `No` where the category directly matches that uncertainty
- duplicate evidence lines are inserted unnecessarily before the same disclaimer block
- the final APSS contains any internal contradiction between Property Overview, Key Document Status, Material Information notes, Material Flags, and routed disclaimer blocks

## DOCX-stage rule
Once the chat APSS has been resolved, DOCX stage is technical only.
Do not re-read the pack, re-extract facts, reinterpret evidence, reroute disclaimer families, or change resolved outcomes at DOCX stage.
