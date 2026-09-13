# Plaintiff record and fact-sheet reconciliation

Reconcile a matter-approved fact-sheet schema with supporting records and identify missing or inconsistent information.

Implementation recipe; requires a host runtime, source adapters and legal evaluation.

Roles: Plaintiff intake team, Case management team, Litigation paralegal.

Read the shared `evidence-contract.json` with this recipe.

## Inputs

1. court-approved or matter-approved fact-sheet schema/version
2. authorized plaintiff records
3. identity aliases with verified mappings
4. known required source list

## Workflow

1. Freeze the specific fact-sheet version and field definitions. Do not substitute a generic MDL form or infer a required field from another litigation.
2. Match source documents to the correct plaintiff using verified identifiers; route uncertain or conflicting matches to review.
3. For each field, record the exact supporting passage, source date and normalized value separately from original wording.
4. Compare exposures, treatment dates, products, prescribers and injuries across sources while preserving uncertainty and contradictory records.
5. Mark blank/unknown/declined/not-applicable distinctly; absence in reviewed records is not proof the event did not occur.
6. Draft a completeness report and targeted follow-up questions. Require counsel review before sharing or populating a court filing.

## Deliverables

1. field-level support matrix
2. identity exceptions
3. missing-record checklist
4. conflict report
5. draft follow-up questions

## Acceptance cases

1. two plaintiffs with similar names
2. date inferred only from filename
3. conflicting treatment dates
4. revised fact-sheet schema
5. record outside authorized matter
6. missing signature cannot be invented

## Source mapping

Paths in the JSON recipe are relative to the library root unless they begin with `Original-Litigation-Recipes/`, which is relative to the toolkit. The host must resolve source IDs and permissions; these paths are not executable tool grants.
