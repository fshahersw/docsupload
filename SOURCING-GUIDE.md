# Court-library enrichment and sourcing guide

Assessed September 12, 2026. The strongest next step is a versioned **source library** that joins court forms to governing rules, statutes, docket orders and source evidence. A large downloaded row count alone does not make a dependable legal reference collection.

## Added to the library

- [Additional primary sources](EXTENDED-LAW.html): original New Jersey statutes in RTF/TXT, seven complete selected title spans and 5,856 indexed entries; full GPO Title 21 XML and 233 source entries across eight FDA parts. Dates, duplicate source citations and publisher cutoff discrepancies remain visible.
- [Workflow toolkit](TOOLKIT.html): 59 skill files inventoried across pinned LegalQuants repositories, 34 copied skills, two copied NDA playbooks, reviewed helpers/tests, an 18-module implementation audit and eight original litigation recipes.
- [Primary law](LAW.html): official U.S. Code Titles 9 and 28 and the Title 28 appendix, three original PDFs, three original XML files and 1,077 structured provision/rule records. The official release is PL119-103, September 2, 2026. Includes a bounded offline citation and subsection resolver.
- [Settlement references](SETTLEMENTS.html): nine independently checked case references and four original English PDFs. Dates are typed as claim, exclusion, objection or hearing dates. Eligibility/proof details and material source conflicts remain visible.
- The retained court-form collection remains 11,181 documents. The excluded documents and their recovery UI have been deleted. Original retained documents and 295 court/judge images are unchanged.

## What else we can source, and why it matters

| Material | Best acquisition route | Valuable platform use | State of this delivery |
|---|---|---|---|
| Federal jurisdiction, removal, venue, CAFA and MDL law; arbitration; federal civil/appellate/evidence rules | [OLRC official PDF and USLM XML releases](https://uscode.house.gov/download/download.shtml) | Matter-specific source packs; context for venue/removal/MDL planning; click-through citations; access to amendment notes | Titles 9, 28 and appendix acquired and indexed. No case-specific legal conclusions or deadline engine. |
| State statutes | [NJ daily RTF ZIP](https://pub.njleg.state.nj.us/Statutes/STATUTES-TEXT.zip), [NY Senate law API](https://legislation.nysenate.gov/static/docs/html/laws.html), [CA legislative bulk downloads](https://downloads.leginfo.legislature.ca.gov/) | State-law reference packs and statute-to-form links; structured section context; revision comparisons | New Jersey original RTF/TXT and seven complete selected title spans acquired. The statute/TOC cutoff discrepancy is explicit. NY requires a signup key; CA bulk routes are documented but neither corpus is imported. |
| Regulations, authority citations and regulatory history | [eCFR developer resources](https://www.ecfr.gov/reader-aids/ecfr-developer-resources), [GPO XML bulk collections](https://www.govinfo.gov/developers) | FDA/medical-device and other regulatory source packs; statute-to-regulation authority links; dated comparisons | Full GPO Title 21 XML acquired, with an index of parts 11, 50, 56, 312, 314, 803, 807 and 820. File date and volume amendment markers are separate. Incorporated standards are not reproduced; eCFR is an editorial compilation, not an official legal edition. |
| Local rules, judge practices, model orders, standing orders and jury instructions | Official judiciary/court/judge pages; discover links, fetch originals, parse headings and source dates | A court/judge-specific matter binder; filing checklist inputs; links from a template to its governing practice | Existing 26 rules/reference sources and court/judge assets remain. No claim of complete judge or local-rule coverage. |
| Settlement agreements, preliminary/final approval orders, notices, distribution plans and blank claim forms | Feed for discovery, then official administrator/court links and original PDFs | Comparative settlement structures; procedural event timelines; source-backed class-scope and proof matrices | Nine-case sample and four PDFs added. Documents are case-specific references, not universal filing templates. |
| Opinions, citation relationships, docket metadata and judges | [Free Law Project/CourtListener data and APIs](https://www.courtlistener.com/help/api/), [GovInfo developer resources](https://www.govinfo.gov/developers) | Rule/statute-to-case-law links, judge research, procedural history and source-backed case summaries | Not imported in this pass. CourtListener describes memberships/commercial API access; do not assume every service is free. Public records do not guarantee complete PACER attachments. |
| FDA product labels, recalls, enforcement and adverse-event reports | [openFDA APIs](https://open.fda.gov/apis/) and linked FDA originals | Product/exposure chronologies, recall packets, signals for mass-tort research | Sourcing plan only. An adverse-event report does not by itself establish causation, and FDA notes data-validation limits. |
| Bills, public laws, Statutes at Large and Federal Register documents | [GovInfo bulk XML, link services, sitemaps and feeds](https://www.govinfo.gov/developers) | Changes affecting existing reference packs; act-to-code lineage; distinguish proposals from enactments | Source routes inspected, no background monitoring configured. GovInfo also documents an MCP public preview; API access uses a data.gov key. |

These additions would support a useful matter source pack: **court → judge practices → rule → statute/regulation → relevant order/opinion → applicable document**. Each connection should show the cited source span and date. A hyperlink or extracted reference is not proof of applicability or an exhaustive legal-dependency graph.

## Open US Law: useful parts, verified limits

Repository reviewed at commit [`2f7aeb85a434a54a351ac44e3c188fec318f78ba`](https://github.com/Vaquill-AI/open-us-law/tree/2f7aeb85a434a54a351ac44e3c188fec318f78ba). The [public snapshot manifest](https://oss-data-us.vaquill.ai/index.json) describes `v2026.08`, dated August 14: **229 Parquet files, approximately 4.09 GB**. Its court-rule subset contains **44 files and 43,809 rows**: federal plus 43 state/DC/PR jurisdictions. This is not a completeness guarantee. Court-rule files are absent for AR, CO, KY, MO, NJ, NM, OK, SD and VT; having a scraper in the repository does not prove a published dataset exists.

All 44 court-rule file footers were inspected for actual row counts, and four complete samples matched the publisher hashes. Sampling found concrete defects: reserved California rules marked `in_force`, deleted Minnesota rules marked `in_force`, ambiguous/wrong Minnesota rule-family citations, and repeated long overlapping passages in CA/MN/NY text. The statutory coverage configuration also contains withdrawn GA/NC data. These findings are why this delivery uses government originals rather than importing the Parquet corpus wholesale. They do not establish that every other row is defective or correct.

The repo does contain useful code patterns:

| Code | Good reuse opportunity | Required adaptation |
|---|---|---|
| [`scripts/lib/payload_builder.py`](https://github.com/Vaquill-AI/open-us-law/blob/2f7aeb85a434a54a351ac44e3c188fec318f78ba/scripts/lib/payload_builder.py) and [`payload_schema.py`](https://github.com/Vaquill-AI/open-us-law/blob/2f7aeb85a434a54a351ac44e3c188fec318f78ba/scripts/lib/payload_schema.py) | Common metadata vocabulary and normalization audit | Validate types, required provenance, status values and missing content; key checks alone are insufficient. |
| [`parse_ecfr_streaming.py`](https://github.com/Vaquill-AI/open-us-law/blob/2f7aeb85a434a54a351ac44e3c188fec318f78ba/scripts/federal/parse_ecfr_streaming.py) | Parse large regulation XML while keeping hierarchy and authority | Add fixtures for tables, footnotes, stubs and full section boundaries. Avoid unconditional in-force labels. |
| [`parse_authority_citations.py`](https://github.com/Vaquill-AI/open-us-law/blob/2f7aeb85a434a54a351ac44e3c188fec318f78ba/scripts/federal/parse_authority_citations.py) and [`parse_public_law_cites.py`](https://github.com/Vaquill-AI/open-us-law/blob/2f7aeb85a434a54a351ac44e3c188fec318f78ba/scripts/federal/parse_public_law_cites.py) | Statute/regulation authority crosswalk and amendment references | Retain the exact source span and edition; distinguish parsing from legal validation. |
| [`download_usc_zips.py`](https://github.com/Vaquill-AI/open-us-law/blob/2f7aeb85a434a54a351ac44e3c188fec318f78ba/scripts/federal/download_usc_zips.py) | Bounded parallel government bulk acquisition | Pin release, check ZIP/file signatures and hashes, use complete receipts; a partial title must not count as completed. |
| [`ingest_nj_bulk.py`](https://github.com/Vaquill-AI/open-us-law/blob/2f7aeb85a434a54a351ac44e3c188fec318f78ba/scripts/statutes/ingest_nj_bulk.py), [`ny_bulk/api.py`](https://github.com/Vaquill-AI/open-us-law/blob/2f7aeb85a434a54a351ac44e3c188fec318f78ba/scripts/statutes/ny_bulk/api.py), [`ca_bulk/zip_reader.py`](https://github.com/Vaquill-AI/open-us-law/blob/2f7aeb85a434a54a351ac44e3c188fec318f78ba/scripts/statutes/ca_bulk/zip_reader.py) | Official state bulk/API routes with fewer page requests | Respect access conditions, preserve law versions, bound archives, deduplicate content and verify text. |

The repository's hosted citation resolver, index and embedding service are not provided as an equivalent self-hosted service. The [hosted resolver](https://www.vaquill.ai/docs/api-reference/us-statutes/resolve-a-citation-to-its-section) is a separate authenticated commercial API. [Public pricing](https://api.vaquill.ai/api/v1/api-credits/pricing), checked during this pass, lists citation resolution at $0.02, full body at $0.06 and search at $0.04 before optional body charges. Unresolved citations are charged. No account, key, trial or paid service was created or used.

Scripts have an [Apache-2.0 license](https://github.com/Vaquill-AI/open-us-law/blob/2f7aeb85a434a54a351ac44e3c188fec318f78ba/LICENSE); preserve the license/notices and identify changes if adapted. Compilation/metadata use [CC BY 4.0](https://github.com/Vaquill-AI/open-us-law/blob/2f7aeb85a434a54a351ac44e3c188fec318f78ba/data/LICENSE.md): **Open US Law by Vaquill AI, CC BY 4.0**, with license link and modification notice. Dependencies have separate terms; for example, PyMuPDF is AGPL/commercial. No Vaquill code or dataset was bundled in this pass; the local lookup implementation is original.

## SettleSignal: discovery feed, not a legal calendar

The [public data page](https://settlesignal.com/data/) and feed-specific [RSL notice](https://settlesignal.com/.well-known/rsl.xml) offer attribution-based use, while the [general terms](https://settlesignal.com/terms/) restrict commercial use and bulk republication. This conflict is preserved in the settlement collection's source notes. The 848-record raw feed is not included in the portable library.

Checks of nine cases found practical issues: no-claim automatic-payment processes labeled open for claims; an antitrust case categorized as securities; overly broad proof labels; separate settlement rounds collapsed; and a conflict in an official claim form's own benefit language. The curated records cite the actual notice, order or administrator page and keep unresolved source disagreements visible.

Discovery attribution: [SettleSignal](https://settlesignal.com/data/) — published settlement data with evidence status, CC BY 4.0. The four original PDFs have their own rights and no universal template license is asserted. Court/judge logos and portraits likewise retain their existing source-specific reuse notes.

## Acquisition workflow for the next pass

1. Discover official source directories using known government/administrator pages, repo source maps, sitemaps and bounded crawling.
2. Prefer official bulk XML/RTF/JSON or original PDFs/DOCX over scraping rendered page navigation. Follow ordinary documented access; leave unavailable material as a source link.
3. Keep original bytes, source URL, retrieval time, publication/release/effective dates, language, title evidence, checksum and legal-document family.
4. Extract complete sections with nested exceptions, notes and tables. Match source identifiers and compare representative passages with independently obtained originals.
5. Deduplicate by exact content; keep meaningful format and revision variants. Never merge different rules solely because their numbers match.
6. Publish only the accepted material with a clear coverage report. New documents are reference materials until independently qualified as reusable templates or inputs to a rules engine.

No platform repository was changed or deployed. No scheduled monitoring, automated legal advice, filing submission or email workflow was activated. This is a portable local reference-library enhancement before export.


## LegalQuants reuse findings

The main repository and its exact community gitlink were inspected, including all 59 populated skill files, five playbooks and relevant scripts/tests. The [toolkit](TOOLKIT.html) distinguishes copied source material, source-only modules and original integration specifications. The selection preserves 203 exact upstream Git blobs and their applicable license files/notices. Source licenses are checked per scope; the root Apache label does not cover every web, dependency, or third-party skill obligation.

The strongest practical uses are sourced chronologies, proposition checks, evidence receipts, review-column contracts and controlled document generation. The [architecture review](09-Workflow-Toolkit/ARCHITECTURE-REUSE-REVIEW.md) documents reproduced gaps in citation coverage, page relocation, spreadsheet formula handling and MCP policy. [Skills/script findings](09-Workflow-Toolkit/LegalQuants/FINDINGS.md) record template validation and coverage limitations. Bedrock and substantive in-Word editing are not supplied by this pinned code. No platform merge or runtime installation was performed.

## Lavern specialist agents and normalized skills catalog

The [Agent Skills Library](SKILLS.html) joins the existing LegalQuants inventory with the pinned AnttiHero/Lavern profiles, prompts and workflow context. The selected 100 Lavern source files preserve Apache LICENSE/NOTICE and exact Git bytes. See [source review](10-Agent-Skills-Library/Lavern/REUSE-REVIEW.md), [catalog](10-Agent-Skills-Library/catalog.json), and [source-path resolution](10-Agent-Skills-Library/SOURCE-RESOLUTION.md). Profile scores and advertised capability language are not independent benchmarks; profile-only entries are labeled explicitly. The library is a local catalog and brief generator, not an installed multi-agent system.
