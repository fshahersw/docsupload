# Court filing readiness packet

Build a source-linked checklist of the specific form, court and judge requirements for a proposed filing.

Implementation recipe; requires a host runtime, source adapters and legal evaluation.

Roles: Managing clerk, Litigation paralegal, Filing attorney.

Read the shared `evidence-contract.json` with this recipe.

## Inputs

1. court and judge identifiers
2. case type and posture
3. proposed filing and attachments
4. intended filing date
5. applicable standing/case-management orders

## Workflow

1. Resolve the court and judge against the library roster; report an unresolved identity instead of substituting a similarly named court.
2. Collect applicable court-wide rules, judge practices, case orders and form instructions; record document date and source version separately.
3. Extract requirements into categories: document/form, format, exhibits, service, sealing, proposed order and filing procedure. Each requirement needs a quote and exact source locator.
4. Compare the draft against measurable requirements only when the source and document structure support a check. Label unavailable formatting/word-count checks explicitly.
5. Expose potentially conflicting instructions with their issuing authority and dates for counsel to resolve. Require live official-source confirmation for a dated library copy.
6. Create a review checklist and selected source packet; never compute deadlines or file automatically.

## Deliverables

1. requirement × source × draft-location matrix
2. missing-source/material list
3. selected original court documents
4. review and disposition log

## Acceptance cases

1. wrong district with similar court name
2. judge practices older than a case order
3. scanned exhibit formatting unavailable
4. settlement notice rejected as generic form

## Source mapping

Paths in the JSON recipe are relative to the library root unless they begin with `Original-Litigation-Recipes/`, which is relative to the toolkit. The host must resolve source IDs and permissions; these paths are not executable tool grants.
