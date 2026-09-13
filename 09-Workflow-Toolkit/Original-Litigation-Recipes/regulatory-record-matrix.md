# Drug and device regulatory evidence matrix

Connect product, safety and quality records to a specifically selected regulatory reference without making automatic violation findings.

Implementation recipe; requires a host runtime, source adapters and legal evaluation.

Roles: Mass-tort attorney, Expert support team, Document review team.

Read the shared `evidence-contract.json` with this recipe.

## Inputs

1. product/device and relevant time period
2. document corpus
3. selected regulatory provisions
4. issues selected by counsel

## Workflow

1. Identify the product category and relevant factual dates; show uncertainty rather than assume a regulatory pathway.
2. Select applicable candidate provisions by counsel-approved issue. Preserve the exact regulatory snapshot and parent scope/exceptions.
3. Extract statements about reports, events, investigations, controls and responsibilities with actor/date/source distinctions.
4. Construct requirement × evidence × gap rows. Treat missing records, contrary statements and potential noncompliance as separate findings.
5. Flag incorporated external standards as unavailable unless a lawfully provided copy is supplied; do not fill them in from memory.
6. Create source-linked expert/document-request questions and a review packet. Do not infer a private right of action, causation, or a violation from a text match.

## Deliverables

1. regulatory issue matrix
2. chronology of source events
3. incorporated-material gaps
4. expert questions and document-request leads

## Acceptance cases

1. current part 820 applied to earlier events
2. ISO text not supplied
3. reporting date versus event date
4. two formulations with similar product names
5. reserved regulation range
6. manufacturer knowledge not established

## Source mapping

Paths in the JSON recipe are relative to the library root unless they begin with `Original-Litigation-Recipes/`, which is relative to the toolkit. The host must resolve source IDs and permissions; these paths are not executable tool grants.
