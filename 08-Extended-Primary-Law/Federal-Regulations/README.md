# FDA regulatory references

This packet contains the untouched GPO Title 21 XML plus a derived index of **233 source entries across eight complete parts**: 11, 50, 56, 312, 314, 803, 807, and 820. Four entries are reserved, including one reserved range kept as a single source record. The full XML contains 275 part nodes; the searchable selection is narrower and is not represented as a full federal-regulation library.

## Source and dates

- Publisher: Office of the Federal Register / U.S. Government Publishing Office.
- Original: https://www.govinfo.gov/bulkdata/ECFR/title-21/ECFR-title21.xml
- GPO Last-Modified: September 11, 2026. Retrieved September 13 UTC / September 12 Central.
- The source contains separate volume amendment markers. These are retained per section, rather than replacing them with the download date.
- The eCFR is a publisher-maintained editorial compilation, **not an official legal edition of the CFR**. Validate historical applicability and intervening amendments for a specific matter against eCFR point-in-time history, the annual CFR and the Federal Register.

## Data contract

`REGULATIONS.jsonl` has one physical UTF-8 line per source section node, including reserved entries and the reserved range. Each row preserves source identifiers, parent headings, authority/source notes at every ancestor level (including subparts), original-file hash, complete section XML, and display text. Tables retain row/column boundaries. No synthetic subsection numbering is created. Exact section lookup is supported in the browser; it does not resolve or invent pinpoints. The reserved range links to its official part instead of fabricating an individual section URL.

The eight selected parts have no source graphic elements. The preserved full-title XML can contain external graphic references. Incorporated standards (including ISO standards referenced in part 820) are **not reproduced** and their terms do not become free merely because a regulation cites them.

All 233 section bodies were checked against the original XML's ordered text, and the source file hash is in `MANIFEST.json`. This checks extraction fidelity, not legal effectiveness, completeness of incorporated materials, or applicability to a client.

## Litigation uses

- Build document requests and an evidence matrix around labeling, safety reporting, sponsor/investigator responsibilities, and record controls.
- Attach exact regulatory text and its source version to expert questions or an issue outline.
- Keep alleged facts, regulatory requirements, expert opinions, and counsel's conclusions in separate fields.
- A mismatch or missing document is an investigation lead, not an automatic noncompliance finding.

Source documentation: https://www.govinfo.gov/developers and https://www.govinfo.gov/help/cfr
