# New Jersey statutory reference snapshot

This packet preserves the Legislature's original whole-corpus RTF and TXT and makes seven complete source titles easy to search. It is a statutory reference collection, not a set of court forms or editable legal templates.

## Coverage

- Whole originals: 69 title headings plus Appendix A; the source includes a heading-only Title 8A.
- Complete selected source spans: Titles 2A, 2B, 10, 22A, 34, 56 and 59 (8,588,867 bytes).
- 5,856 headnote records across 5,854 citation labels. Counts: 2A 2,416; 2B 254; 10 122; 22A 75; 34 2,105; 56 764; 59 120.
- RTF is one 94,415,499-byte original. TXT is one 83,882,972-byte original. The seven smaller TXT extracts are exact derived title slices; no standalone publisher Word files were invented.

## Version and legal applicability

The statute header states **UPDATED THROUGH P.L.2025, c.405, and J.R.22**. The archive's HTTP Last-Modified is September 12, 2026. A separately published Legislative Counsel table of contents, fetched from the same official directory, states **UPDATED to P.L.2026, c.30 and JR 1**. This discrepancy remains unresolved. Do not transfer the TOC cutoff to the statute text or label the daily ZIP as current law.

Source inclusion does not establish that a provision is active, effective, unamended or applicable. Historical notes and duplicated versions remain intact. Court rules, emergency enactments outside the selected titles, and subsequent amendments require separate checks.

## Quality controls

The ZIP was checked for traversal paths, encryption, symlinks, excessive ratios and size limits before streaming its two entries. Original entry CRCs and SHA256 hashes were verified. No scripts, executables, Folio software or third-party annotations are included. The RTF scan found no object, objdata, field, filetbl, bin or pict controls; a full Word rendering was not performed.

RTF headnote styles were matched in source order to original TXT headings, including three indented headings. Two real headings used nonstandard RTF formatting and were added after inspection: 34:16-43 and 56:8-215. Three fee-statute body paragraphs that repeat citations were correctly kept within their existing sections. Prefix plus section slices reconstruct every selected title byte-for-byte; all 5,856 record texts and hashes round-trip to the original TXT.

The compilation repeats **34:15C-10** and **34:16-43** under different headnotes. Both occurrences are indexed separately. Do not choose the operative version automatically. Three malformed or empty RTF headnote blocks outside the selected titles were not promoted into parsed sections; whole originals retain them.

Three independent official web pages (2A:14-2, 2A:56-23 and 2A:56-44), fetched with ordinary unauthenticated Windows HTTP requests, match the snapshot's complete heading, body and history after whitespace normalization. This validates only the sampled transcription; it is not a comprehensive current-law review.

## Integration

Read `source-manifest.json` for version/access/provenance, `schema.json` for field semantics, `title-index.json` for source spans and `selected-sections.jsonl` for citation-linked text. `selected-citations.csv` offers a compact index. JSON/Markdown are UTF-8; original and title-extract TXT bytes are Windows-1252 with CRLF. Every byte range is zero-based start-inclusive/end-exclusive in the original STATUTES.TXT, and lines are one-based inclusive.

Use the whole original RTF as the Word-readable reference. Use smaller selected-title files or indexed sections for retrieval. Preserve the source hash, title, citation occurrence, version statement, exact text and offsets with every AI quotation. Render source text as text, never instructions or unsanitized HTML. This index does not invent subsection pinpoints, legal summaries or calculated legal deadlines.

`next-sources.json` records bounded official New York and California expansion routes. New York's documented API requires a free signup key; none was obtained. California exposes a public base/increment dataset, but its documented daily full-session files exclude Code tables. Neither state corpus was mirrored in this packet.

The original ZIP and acquisition logs remain outside the clean-library whitelist. Local audit paths in the metadata refer to that separate review workspace. Only the exact files listed in the parent-level `export-manifest.json` are approved for clean-library promotion.
