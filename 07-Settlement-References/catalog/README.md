# Settlement intelligence catalog

Open the library's [Settlement intelligence page](../../SETTLEMENTS.html) or this folder's [portable entry point](index.html). The complete supplied snapshot is now browsable: **848 settlement/refund catalog records**, **663 benefit descriptions**, **614 reported claim dates**, **9 existing dated source reviews**, and **4 saved original PDFs across 3 records**. All original fields remain available; this is not a claim that the records describe 848 distinct legal cases or currently available claims.

## What works locally

- Search full titles, benefit descriptions and the attached reviewed case/court fields.
- Filter category, geographic scope, claim date, reported status, proof requirements, publisher evidence tier, saved PDFs and source reviews.
- Compare date-only deadlines against an explicit as-of date. Use the next 7, 30 or 90 days, passed dates, and missing-date filters.
- Save entries in this browser, compare up to four entries, and export the current filtered set or comparison to spreadsheet-safe CSV.
- Export complete individual records as JSON or download a scoped research brief with the source text, review qualifications, source URLs and required credit.
- Read the nine existing source reviews and follow saved original PDFs or explicit source-only links.

There is no installation, model call, account requirement or background network request. Source links open only when selected. Saved IDs stay in local browser storage; storage failure falls back to the current visit. Saving is not a notification subscription, shared case-team list or live monitoring service.

## Package contents

| File | Purpose |
|---|---|
| `publisher-feed.json` | Byte-for-byte copy of the supplied September 13 snapshot; all dataset metadata retained |
| `catalog.json` | Full source records with stable IDs, exact fingerprints and separately attached reviews |
| `catalog-data.js` | Offline browser data; same catalog payload |
| `catalog.schema.json` | Portable JSON Schema for the current catalog contract |
| `settlement-core.js` | Pure filtering, date, link, comparison export and research-brief utilities; browser and CommonJS |
| `settlement-library.js`, `.css`, `index.html` | Standalone offline frontend |
| `import_catalog.py` | Standard-library importer; no network or supplied-script execution |
| `test_import_catalog.py`, `settlement-core.test.cjs` | Import and deterministic behavior regression tests |
| `IMPORT-RECEIPT.json` | Source hashes and import counts |
| `NOTICE.md` | Supplied feed license and attribution |

The nine reviews remain canonical in `../verified-records.json`. Their original documents are in `../documents/`, with metadata in `../documents.json`. The catalog copies these reviews as dated overlays without modifying the originals. Copy the entire `07-Settlement-References` directory to retain its document links. The portable page expects the other library pages two levels above; a host integration should replace those navigation links.

## Source distinctions

`publisher` contains an unchanged provider row. `review` contains a bounded assessment, if available, with its own sources, scope, dates and limitations. `verification_status`, `accepted_official_evidence` and `last_verified` belong to the publisher; they never become a firm verification badge. This import performed **zero new independent settlement reviews**.

The supplied dataset has 342 records marked `needs_recheck`, 234 missing claim dates, and 301 with unknown proof requirements. Those records are retained and remain filterable. There is one prose claim-link value; it remains text. A URL with a literal path space gets a percent-encoded display link while the original string is retained.

An empty `applicable_states` array means nationwide **according to this feed**, not nationwide court jurisdiction or a complete class definition. The CRST source review records a narrower California class and a no-claim-required process. Its discrepancies remain visible. A missing claim date is neither unlimited time nor proof that no action is required.

`estimated_payout` is deliberately stored as full text. It mixes settlement funds, caps, alternative benefits, pro rata estimates, reimbursement terms and noncash benefits. The UI does not total these values or pretend they are comparable per-person awards. Claim, objection, exclusion, hearing and payment events must remain distinct. Date-only values have no invented cutoff time or timezone conversion.

## Host integration for testing.seegerweiss.com

Use the existing authenticated host shell and matter access model. Mount the catalog as a **settlement source-discovery and comparison collection**, separate from primary-law retrieval. An indexed row should carry `record_id`, provider URL, source snapshot SHA-256, row SHA-256, `source_kind=publisher_settlement_catalog`, reported fields and dated review coverage. It should never masquerade as an official notice, court order or matter fact.

The host may use an exported research brief as input to its selected settlement research agent. Fetch and verify the linked primary documents through the host's authorized tools before deriving eligibility, valuation or calendaring decisions. Citations need the actual document/page or source section. Do not treat catalog text, external websites or uploaded documents as tool/system instructions. `SKILLS.html#skill=sw-settlement-valuation-analyst` is a library reference; this page does not start that agent.

For a React host, load the catalog as data and reuse `settlement-core.js` or port its pure functions with the included tests. Keep rendering scoped to the host component; the standalone CSS styles its own page globally and should be isolated with an iframe or scoped before embedding. Replace file links with authenticated source-document routes, browser storage with the host's user-owned saved-list store, and root navigation with host routes. No guessed backend endpoints, credentials or production migrations are supplied.

## Refresh and validation

Keep the previous snapshot/receipt outside the active serving directory. Import a new snapshot into a separate candidate folder first; the importer overwrites its four generated files in the specified output folder. Do not point a routine refresh at the active catalog before comparing the candidate.

```powershell
python -B import_catalog.py --input C:\path\new-settlesignal.json --references ..\verified-records.json --output C:\path\candidate-catalog
python -B -m unittest discover -s . -p test_import_catalog.py
node --test settlement-core.test.cjs
```

The tests shipped here assert this snapshot's audited counts; update count assertions only after reviewing a new snapshot. Exact repeated rows retain every source position. Conflicting payloads sharing a publisher URL remain separate versions. Shared titles, defendants or official-site URLs are never silently merged. Missing or ambiguous review joins fail the import. Changed publisher fields trigger a review-staleness note rather than rewriting the dated review. A changed provider URL requires an explicit reviewed mapping; no fuzzy case-name join is attempted.

Source SHA-256: `76ffad1e50a3154c1149327ac080f3191129d6d82693b16e088c2e52f59505ba`.

Data: [SettleSignal (settlesignal.com)](https://settlesignal.com/). Used under the attribution statement supplied inside the feed; see [NOTICE.md](NOTICE.md). That statement is not a separate license for every linked notice, claim form or website.
