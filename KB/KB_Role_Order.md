# KB Role and Order Map

## Purpose
Use this file as a quick reference for which uploaded knowledge source controls what.
It is not a replacement for the underlying files.

## Order of application
1. Security_Runtime_KB.md
2. Evidence_Ledger_KB.md
3. APCP-20-30_Stabilisation_Rules_KB.md
4. Disclaimer_Routing_Map_KB.md
5. Word_Template_Handling_(APSS).md
6. APSS_Disclaimer_Library.md
7. AI_Training_KB.md
8. Security_Policy_Knowledge.md

## Role summary

### 1. Security_Runtime_KB.md
Use for runtime control, evidence discipline, status discipline, disclaimer timing, security controls, and publication gate.

### 2. Evidence_Ledger_KB.md
Use for mandatory document inventory, raw evidence extraction, conflict resolution, field population gate, re-check pass, and ZIP handling rules.
This layer must complete before any APSS field is populated.
It is not property evidence.

### 3. APCP-20-30_Stabilisation_Rules_KB.md
Use for extraction logic, field decision rules, source hierarchy, disclaimer selection, Council Tax exception logic, mixed-row status handling, chat-to-DOCX parity, and disclaimer mutual exclusion rules.

### 4. Disclaimer_Routing_Map_KB.md
Use for disclaimer family routing, condition-based selection logic, and mutual exclusion enforcement.
Use this file to decide which disclaimer number to select.
Do not use it for disclaimer wording — wording comes from APSS_Disclaimer_Library.md only.

### 5. Word_Template_Handling_(APSS).md
Use for placeholder handling, status rendering mechanics, DOCX validity, post-render QA, and disclaimer placement only.
Do not use it for extraction logic or disclaimer selection.

### 6. APSS_Disclaimer_Library.md
Use for disclaimer wording only.
Insert wording verbatim only.
Do not paraphrase, shorten, merge, or rewrite disclaimer text.

### 7. AI_Training_KB.md
Use for defect locks, anti-hallucination reinforcement, and field-priority reminders.
It reinforces but does not override runtime or APCP authority.

### 8. Security_Policy_Knowledge.md
Use for governance and rationale only.
Do not treat it as a runtime rule source.

## Conflict rule
If rules conflict, the most restrictive rule wins.
If a governance statement conflicts with a runtime statement, the runtime statement wins.
