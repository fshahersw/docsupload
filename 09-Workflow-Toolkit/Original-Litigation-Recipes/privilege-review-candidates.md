# Privilege and confidentiality review candidates

Prioritize documents for privilege/confidentiality review and prepare a source-linked candidate log.

Implementation recipe; requires a host runtime, source adapters and legal evaluation.

Roles: Review attorney, Discovery counsel, Litigation support.

Read the shared `evidence-contract.json` with this recipe.

## Inputs

1. matter-approved review protocol
2. authorized documents and families
3. participant roles if verified
4. governing jurisdiction and date

## Workflow

1. Preserve document family relationships and identify missing attachments, incomplete email threads and inaccessible content.
2. Extract verified participants, roles, dates and source metadata; leave unknown values unresolved.
3. Identify passages that may warrant review under the provided protocol. Separate legal-advice content from business discussion and from mere attorney presence.
4. Record countervailing facts and sharing/waiver questions without deciding legal privilege automatically.
5. Produce a candidate log with non-substantive descriptions for counsel review; do not expose potentially privileged content in a public export.
6. Require an authorized reviewer to finalize dispositions and descriptions before production or withholding.

## Deliverables

1. review priority queue
2. candidate log
3. family-level exceptions
4. reviewer disposition history

## Acceptance cases

1. attorney copied only for business purpose
2. privilege banner without legal advice
3. missing attachment
4. mixed personal/business/legal discussion
5. unverified participant role

## Source mapping

Paths in the JSON recipe are relative to the library root unless they begin with `Original-Litigation-Recipes/`, which is relative to the toolkit. The host must resolve source IDs and permissions; these paths are not executable tool grants.
