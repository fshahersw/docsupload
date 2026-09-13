# Helper code and how far it can be reused

The packet includes small source modules plus their existing test files. They are unchanged engineering inputs, not a complete service. No package was installed, no service was started, no model was called, and no real document was rendered during this review.

| Source | Useful behavior | Dependencies / limits | Packet status |
|---|---|---|---|
| `lq-ai/api/app/pipeline/parsers.py` | Strict UTF-8 text parsing; typed page spans; separate original/canonical-text representation | Text path is stdlib. PDF path needs separately reviewed PyMuPDF/optional Docling dependencies. It does not implement DOCX ingestion. UTF-8 BOM is explicitly dropped. Text page 1 is synthetic, not a physical page citation. | Copied with text-parser test file |
| `lq-ai/api/app/pipeline/chunker.py` | Overlapping chunks with exact canonical-text slices and page ranges | Stdlib plus parser dataclasses. Offsets are Python Unicode character indices; not byte offsets or browser UTF-16 indices. Sliding windows are not complete legal-structure parsing. | Copied with test file |
| `lq-ai/api/app/research/html.py` | Simple opinion-HTML to text, entity decoding, script/style removal | Stdlib. Loses links/source geometry and joins adjacent table cells; use only for simple fallback text, not primary structured extraction. | Copied with test file |
| `lq-ai/api/app/citation/normalization.py` | Whitespace/quote normalization for comparison candidates | Stdlib. OCR substitutions can collapse distinct names/words or numeric text. Preserve originals; never use the normalized string as the evidentiary quotation. | Copied with test file; OCR mode requires stronger safeguards |
| `lq-skills/skills/coquill/analyzer/analyze.py` | Template variables, simple boolean/equality branches and loops; manifest generation | PyYAML plus optional DOCX libraries; limited regex grammar. Multiple-template selection is guarded by prompt only. | Copied as engineering reference requiring hardening |
| `lq-skills/skills/coquill/renderer/render.py` | Concrete DOCX/HTML/Markdown rendering and optional PDF branches | Several optional external libraries/processes. Missing-field, path, sandbox, type and layout validation gaps. | Copied for review, not approved as an exposed tool |
| `lq-skills/skills/coquill/transcriber/transcribe.py` | Formats the document interview log | PyYAML; Windows time formatting and prefill handling defects. It does not process audio. | Copied for review |

The first-party helper subset includes only the harmless package initializers needed by those modules. It does not include the citation package initializer, which pulls in the heavier verifier/gateway stack. Preserve the `api/app` relative layout if testing the selected text helpers; do not graft this partial package over an existing `app` package.

## Other reviewed code patterns

- Citation extraction and verification: the parent app has exact-then-fuzzy passage location, full-document fallback and a model-based support judge. Those modules are coupled to its schemas, gateway, observability and optional RapidFuzz; they are linked in `FINDINGS.md`, not copied as drop-in tools.
- Tabular execution: per-column model tiers, optional ensemble support checks, per-cell provenance and cost accounting are useful. The actual retrieval/dispatch strategy needs a complete-coverage design for discovery use.
- Easy Playbook: per-span extraction, clustering and verbatim representative clauses are useful concepts. Failure accounting, verified offsets, deduplication and reviewer approval are required before calling a generated clause “standard” or “fallback.”
- Privacy navigator scripts: their static applicability/precedent/conflict datasets were treated as unverified domain content. The citation auditor is a pattern-based linter, not a source verifier, and reproduced coverage defects make it unsuitable as the sole gate. These scripts are not copied.
- Root `backfill_normalized_content.py`, `gen_openapi.py`, `stack-smoke.sh` and `release-image-check.sh` are application/operations-specific rather than portable legal tools. They were inventoried and excluded.

## Validation actually performed

`run_helper_checks.py` performed 13 offline checks on text parsing, Unicode fidelity, chunk coverage, physical-page ranges, invalid inputs, simple HTML conversion, normalization and CoQuill's basic variable grammar. All passed. The same run recorded 12 observations of known limitations, including markdown citation-audit gaps and missing-field false passes.

All 203 staged source files passed SHA-256/byte-count validation against `REUSE-MANIFEST.json`. The packet builder reads immutable Git blobs, rather than silently rewriting source line endings.

The four original pytest files are included unchanged but were not executed: pytest was not available and no dependencies were installed. CoQuill does not ship a local automated test suite in this pinned folder. Community `evals.yaml` files are prompt-evaluation specifications, not evidence that a model run passed. The review does not measure recall, legal accuracy, latency, cost or production security.
