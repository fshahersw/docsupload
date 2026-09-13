# Settlement source review - September 12, 2026

The feed is useful for discovery and triage, but it should not be treated as a verified legal calendar or an eligibility engine. This review checks **9 selected records** against official public administrator sources, with **4 English original PDFs, 30 pages, and 989,737 bytes** preserved and SHA-256 hashed. The canonical library was not changed.

## Reuse and attribution

[The data page](https://settlesignal.com/data/) explicitly offers the JSON/CSV under **CC BY 4.0**, and [the RSL file](https://settlesignal.com/.well-known/rsl.xml) specifically names the JSON feed with search/AI use and attribution. However, [general terms](https://settlesignal.com/terms/), dated June 3, 2026, restrict use to personal/non-commercial purposes and prohibit bulk scraping, resale, and republication. Those statements conflict. The snapshot was acquired from the explicit public download for local research; this is **not clearance for bulk commercial republication**.

Credit the discovery source as **[SettleSignal](https://settlesignal.com/data/) - published settlement data with evidence status, CC BY 4.0** and retain this conflict note. Do not promote the 848-record raw feed or publisher payout descriptions to the clean library. The curated records contain independently written factual summaries of official sources, with limited publisher field values retained for comparison. Official documents have their own rights and are case-specific references, not generally licensed templates.

## What the feed actually contains

- 848 records in the `settlements` array; no duplicate canonical URLs detected.
- 373 labeled open, 449 labeled closed, and 26 in other states; no open record had a dated deadline already before September 12 in this snapshot.
- 226 open records have no claim deadline; an absent date is not proof of an open claim process.
- 55 categories are empty, 301 proof fields are unknown, and 234 records lack a claim deadline.
- 810 accepted-evidence flags are publisher assertions; 342 coexist with `needs_recheck`.
- 667 records have workflow-check dates more than 30 days before the assessment. Feed generation and last catalog modification do not refresh every source.
- Full per-field citations, source excerpts, and document hashes are absent from the free feed and advertised through the partner API.

## Curated sample

| Official case reference | State observed | Claim date | Local PDFs |
| --- | --- | --- | ---: |
| Bianculli v City of New York - Senior Care Co-Pay Settlement | Claims open; final approval pending | 2026-10-30 | 1 |
| Pork Antitrust Litigation - Consumer Indirect Purchaser Settlements | Claims open for the 2026 settlement round; final approval pending | 2026-10-29 | 0 |
| Heckathorn v Farmers - TCPA Settlement | Claims open; exclusion and objection dates passed; final approval pending | 2026-09-14 | 0 |
| Generic Pharmaceuticals Antitrust Litigation - End-Payer Settlements | Claims open for specified court-approved settlements | 2026-11-09 | 1 |
| Huckaby v CRST Expedited - California Truck Driver Settlement | Automatic-payment process described; final approval pending | No affirmative claim described | 0 |
| FTC v Amazon - Prime Membership Consumer Refunds | Claim window closed; approved-claim payments being processed | 2026-07-27 | 0 |
| AmTrust Financial Services Securities Litigation - Partial Settlement | Claims open for proposed partial settlement | 2026-10-07 | 0 |
| AB v Google - Children Privacy Settlement | Claims open; exclusion and objection dates passed; final approval pending | 2026-09-14 | 0 |
| Lighthouse Electric - Data Incident Settlement | Claims open; exclusion and objection dates passed; final approval pending | 2026-09-14 | 2 |

Each JSON record carries typed deadlines with original date labels, source URLs, document/page or website locators, and past/future status relative to September 12, 2026. Open claims do not mean exclusion or objection remains open. No claims were filed or individual eligibility determined.

## Material corrections and uncertainties

1. **NYC Senior Care:** The publisher's no-proof label is too broad. [Notice pp.4-7](https://www.seniorcarecopaysettlement.com/wp-content/uploads/2026/08/Bianculli_Notice-of-Class-Action-Lawsuit-and-Proposed-Settlement.pdf) gives distinct documented and undocumented reimbursement tiers, caps undocumented payments, and requires authority/name-change evidence in specified circumstances. Receipt of a notice does not itself establish reimbursement eligibility.
2. **Lighthouse:** [The blank claim form](https://cw.simpluris.com/docs/public/downloads/LGC3/CLAIM_FORM) Section IV bars combining the $60 alternative with monitoring or documented losses, while its introductory language appears broader. The publisher's combined-benefit summary should not drive automatic selections. The original notice and form are both preserved for review.
3. **CRST:** [The official page](https://truckingdriversettlement.com/) describes payments without an affirmative claim, subject to approval, and a California-resident class. Do not represent the feed's open status and empty state array as a nationwide claim opportunity.
4. **Generic drugs:** [The official case](https://www.genericdrugsendpayersettlement.com/) is pharmaceutical antitrust, not securities. Separate consumer and third-party-payer classes and settlement rounds. The Sandoz page itself contains a Sun/Taro reference in its Do Nothing row; the specific court order and settlement documents should control scope.
5. **Pork:** [The current settlement round](https://www.overchargedforpork.com/Home/Home) is open, while earlier JBS/Smithfield claim periods are closed. A single record must not reactivate old claims.
6. **Google:** [The hearing listing](https://www.coppaprivacyclassaction.com/) uses PST for a September hearing. Preserve that text and obtain court-schedule confirmation before timezone conversion.
7. **Amazon:** [The substantive page](https://www.subscriptionmembershipsettlement.com/) explicitly closes claims on July 27, 2026, despite remaining File Claim navigation. The sample does not establish any reopening.

## Originals and limits

The four successfully downloaded originals are the Bianculli class notice, the June 10 generic-drug notice/claims-administration order, and Lighthouse's notice plus blank claim form. Exact bytes are preserved; English captions and substantive text were checked, with clean descriptive filenames and no claimant submissions.

Pork, CRST and Google PDF requests returned HTTP 403. Farmers returned TLS/connection-reset failures. Amazon's administrator order failed TLS and the separately observed FTC original returned 403. These links and failures remain in metadata; no access controls were bypassed. AmTrust's reference-use/AI-training signals are preserved and its full notice was not acquired for AI ingestion. Four successful files out of ten selected targets are reported honestly; no missing file is represented as downloaded.

The strongest next integration is a small settlement-source reference page with typed events, exact class scope, document provenance, and review flags. Keep approval state, payment process, and source freshness separate. This is a dated, bounded sample, not an exhaustive settlement database, claims service, or legal-currentness certification.

## Files

- `verified-records.json` / `.csv`: nine curated records suitable for a reference page.
- `documents.json`: four verified original PDFs and hashes; relative paths under `documents/`.
- `findings.json`: terms conflict, schema, statistics, methods, and integration guidance.
- `document-download-results.json`: all ten selected document outcomes; no invented successes.
- `settlements.original.json`: research-only raw feed; do not bulk export.
- `.firecrawl/`, `access-policy/`, and `evidence/text/`: review evidence, not page assets.
