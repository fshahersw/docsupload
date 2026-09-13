# Primary-law reference collection

Open [Primary law](../LAW.html) for offline search, supported citation lookup, complete provision text, source notes, and links to the original government PDF/XML volumes.

This collection was acquired directly from the [Office of the Law Revision Counsel](https://uscode.house.gov/download/download.shtml). The release point is **Public Law 119-103, September 2, 2026**. The source XML conversion/creation date, release date, section-page currency statement, and acquisition date are separate facts. They must not be collapsed into one “updated” timestamp.

## What is included

- Title 9: Arbitration — 33 section entries.
- Title 28: Judiciary and Judicial Procedure — 806 section entries, including source historical stubs.
- Title 28 appendix — 238 rule entries across Appellate Procedure, Civil Procedure, Evidence, Supplemental Admiralty/Asset Forfeiture, and Supplemental Social Security Review rules.
- Three original PDF volumes and three original USLM XML files, with SHA-256 and source-archive provenance in [MANIFEST.json](MANIFEST.json).

There are **1,077 structured records**, including explicitly labeled historical/status entries. “Text present” describes the source record; it does not independently certify legal effect or applicability. Original complete volumes remain intact, including historical notes and other material outside the indexed units.

## Integration contract

`PRIMARY-LAW.jsonl` is the canonical structured export: UTF-8, one record per physical LF-delimited line. Iterate lines rather than splitting on every Unicode line separator. `primary-law-data.js` contains the same records for the offline browser; treat it as generated UI data, not a separate corpus.

Each record includes:

- `id`: unique record identity; use this as the primary key.
- `citation_key`, `citation`, `family`, `number`: scoped citation identity. A citation need not identify exactly one record.
- `body_text`, `subsections`, `editorial_notes`, `source_credit`: source-derived text and context. Notes are retained separately from provision text.
- `publisher_identifiers`, `xml_element_id`, `xml_path`, `source_xml_sha256`: a path back to the original source unit.
- `source_status`, `legal_effect_determined=false`, `release_point`, and `current_through_public_law_date`: explicit status/version distinctions.

Never key only by a rule number or the publisher URI. The official appendix uses overlapping URIs for Civil Rule 1 and Supplemental Social Security Rule 1. The Code also contains **two different 28 U.S.C. § 1932 provisions**. These are preserved as distinct records; the resolver returns ambiguity instead of silently selecting one.

The five rule families retain their full official names. Footnote markers do not belong in display titles. Abrogated, repealed, reserved, transferred, omitted, and renumbered records stay labeled; do not use them as operative rules in a deadline engine.

## Offline citation lookup

`resolve_citation.py` uses the Python standard library and the adjacent JSONL file. It makes no API calls and needs no credentials:

```powershell
python resolve_citation.py "28 U.S.C. 1332(d)(2)"
python resolve_citation.py "FRCP 26(b)(1)"
python resolve_citation.py "Supplemental Social Security Rule 1"
```

`citation-resolver.js` exposes the same bounded lookup to browser code as `CourtCitation.parse()` and `CourtCitation.resolve()`. Supported rule aliases include FRCP, FRAP, FRE and their standard abbreviated names. Supplemental families must be named explicitly.

Results distinguish `resolved`, `ambiguous`, `not_found`, `subsection_not_found`, `source_structure_uncertain`, and `unsupported`. A missing subsection must not be relabeled as an exact parent-section match. Bare rule numbers, citation ranges, case citations, statutes outside this snapshot and other jurisdictions are not guessed. Source numbering/nesting issues in 28 U.S.C. §§ 530C and 3301 and Supplemental Admiralty Rule G are explicit: even a unique source path in those provisions is not presented as a verified legal pinpoint.

This is a reference resolver, not a complete Bluebook checker, case-law citator, treatment checker, statutory effective-date engine or filing-deadline calculator. A pinpoint opens in the full parent context.

## Extraction and validation

USLM structural section/rule boundaries govern extraction. Historical quoted sections nested in notes are not promoted as standalone current sections. Original statutory text, subdivisions, publisher annotations and amendment notes are retained. Nine useful Title 28 sections were compared with separately fetched official section pages; exact comparison methods/results are recorded in the manifest.

Use the original PDF for layout, tables, images or exact typesetting and the original XML for structural fidelity. The plain-text view is a derived reading/indexing aid. It is not a reconstructed Word form.

The local build acquired government originals; no Vaquill Parquet content or hosted API result was imported. The supplied lookup code is original implementation. No API keys, model integration, paid service, automatic updates or hosted server is bundled. For future sources and code-reuse findings see [SOURCING-GUIDE.md](../SOURCING-GUIDE.md).
