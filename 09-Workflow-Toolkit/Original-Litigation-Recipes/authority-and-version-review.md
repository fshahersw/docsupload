# Authority and version review

Audit a draft proposition and citation against the actual authority text, relevant date and jurisdiction.

Implementation recipe; requires a host runtime, source adapters and legal evaluation.

Roles: Research attorney, Brief writer, Supervising partner.

Read the shared `evidence-contract.json` with this recipe.

## Inputs

1. draft propositions with citations
2. question presented
3. jurisdiction and relevant date
4. source documents or authorized legal-research connectors

## Workflow

1. List each legal proposition separately from the citation strings; retain uncited propositions as unresolved candidates.
2. Resolve citations to exact records. For ambiguous citations such as duplicate source section numbers, present all candidates with headings and source versions.
3. Retrieve the complete provision/opinion context and exceptions needed for the proposition. A search-result snippet is a lead, not the authority.
4. Verify quoted text, then assess proposition support separately. Identify parenthetical omissions, negative predicates and quoted language from a dissent or cited party.
5. Record effective dates, amendments, historical stubs and jurisdictional limits. Describe any treatment result as bounded by the sources and checks actually performed.
6. Deliver an issue list with exact evidence and a proposed correction for attorney review; no automatic good-law or controlling-authority certification.

## Deliverables

1. proposition/quotation audit table
2. authority packet with versions
3. unverified or unsupported propositions
4. research coverage receipt

## Acceptance cases

1. uncited factual assertion
2. zero assertions cannot pass an accuracy gate
3. FRCP versus Supplemental Rules numbering
4. negative-treatment source outside retrieved subset
5. NJ duplicate 34:15C-10
6. unsupported subsection locator

## Source mapping

Paths in the JSON recipe are relative to the library root unless they begin with `Original-Litigation-Recipes/`, which is relative to the toolkit. The host must resolve source IDs and permissions; these paths are not executable tool grants.
