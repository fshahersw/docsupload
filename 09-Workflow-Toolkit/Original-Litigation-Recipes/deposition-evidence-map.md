# Deposition evidence map and chronology

Turn transcripts into a reviewable chronology, witness/entity map and potential admission list without losing testimony context.

Implementation recipe; requires a host runtime, source adapters and legal evaluation.

Roles: Trial attorney, Litigation paralegal, Case team.

Read the shared `evidence-contract.json` with this recipe.

## Inputs

1. transcript originals with page/line mapping
2. witness and proceeding metadata
3. exhibits if available
4. case issue list

## Workflow

1. Validate witness, date, volume and page-line coverage. Keep printed transcript page numbers distinct from PDF page indices.
2. Extract Q/A exchanges with the adjoining question, answer, objections, corrections and qualifications needed to understand each passage.
3. Identify actors with aliases but preserve separate identities until supporting evidence permits a merge. Do not infer plaintiff status merely because a name appears.
4. Separate event dates from testimony dates; preserve approximate dates, intervals, uncertainty and conflicting accounts.
5. Map assertions, exhibits and people using evidence-backed edges. A contradiction candidate must show the two passages and why they concern the same fact.
6. Label potential admissions and impeachment leads as review candidates; export by selected analysis type with precise page-line citations and a coverage receipt.

## Deliverables

1. chronology
2. witness/entity register
3. issue-to-testimony matrix
4. potential admissions with qualifications
5. graph edge evidence records

## Acceptance cases

1. same surname different people
2. question restates an unaccepted premise
3. objection followed by changed answer
4. errata modifying original testimony
5. ambiguous year
6. missing exhibits
7. two volumes both starting at page 1

## Source mapping

Paths in the JSON recipe are relative to the library root unless they begin with `Original-Litigation-Recipes/`, which is relative to the toolkit. The host must resolve source IDs and permissions; these paths are not executable tool grants.
