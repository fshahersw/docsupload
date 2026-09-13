# Material findings before platform reuse

These findings refer to pinned snapshots, not a deployed Seeger Weiss system. Originals remain unchanged. Reproduced pure-function observations are in `HELPER-CHECKS.json`; other findings are based on source inspection.

## 1. Retrieval coverage is not complete-document coverage

The tabular executor retrieves **four lexical chunks per document/cell**, caps extraction at **500 output tokens**, and documents sequential cell dispatch. It also skips deleted/missing selected documents. Those choices can miss a schedule, definition, exception or adverse passage elsewhere in the file. A blank or `not found` answer cannot prove the term is absent. [Executor source](https://github.com/LegalQuants/lq-ai/blob/2cc3149238defbbb171ec845cd0d3a43a34054f2/api/app/tabular/nodes.py#L98)

For discovery, add a page/span coverage ledger, bounded parallel full-document extraction, retrieval expansion around definitions and cross-references, and explicit unreadable/failed/missing rows. Only an exhausted, successful scan may emit `not_found`; a retrieval answer must show its narrower scope. Preserve the selected-document set even when an input disappears.

## 2. Citation location, quotation accuracy and proposition support need separate states

The tolerant verifier accepts a normalized RapidFuzz ratio of **95 or above** and exposes the score as confidence. A close string score is not a calibrated legal/factual confidence measure and can tolerate a changed number or negation in a long quote. OCR normalization actually collapses `modern` and `modem` in the offline check. Exact quotations should require exact source text, with any typography/OCR repair represented explicitly. [Verifier](https://github.com/LegalQuants/lq-ai/blob/2cc3149238defbbb171ec845cd0d3a43a34054f2/api/app/citation/verification.py#L183), [normalization](https://github.com/LegalQuants/lq-ai/blob/2cc3149238defbbb171ec845cd0d3a43a34054f2/api/app/citation/normalization.py)

Full-document citation fallback improves chunk-boundary recall, but the candidate's page is still assigned from the originally cited chunk. Recompute the page from the matched source offset; keep repeated-quote ambiguity and unmatched citation markers in the audit queue rather than silently dropping them. [Extractor](https://github.com/LegalQuants/lq-ai/blob/2cc3149238defbbb171ec845cd0d3a43a34054f2/api/app/citation/extraction.py#L176)

Offsets in these Python modules are Unicode character positions, despite several “byte-for-byte” descriptions. A browser needs an explicit conversion or anchor map for UTF-16; preserve parser version, file hash, canonical text and source geometry.

## 3. DOCX capability is not supplied by the parent ingestion module

Several review prompts accept Word documents, but the inspected parser supports PDF and strict UTF-8 text/Markdown, with DOCX/RTF marked unsupported. A portable prompt does not fill that implementation gap. Build or adapt a DOCX pipeline covering paragraphs, tables, headers, footnotes/endnotes, fields, comments and revisions, and expose any unparsed structure. [Parser boundary](https://github.com/LegalQuants/lq-ai/blob/2cc3149238defbbb171ec845cd0d3a43a34054f2/api/app/pipeline/parsers.py#L130)

The small HTML fallback also joins adjacent table cells (`Amount` + `500` becomes `Amount500`). It is useful for simple opinion bodies, not for extracting reliable legal tables.

## 4. Easy Playbook can hide incomplete extraction and overstate representative clauses

The extractor catches a failed span and continues; malformed/empty responses become empty lists. Model-provided offsets are rebased but not checked against the actual quoted source text. A returned list therefore does not establish full-span completion or anchor correctness. [Extraction loop](https://github.com/LegalQuants/lq-ai/blob/2cc3149238defbbb171ec845cd0d3a43a34054f2/api/app/playbooks/easy/extractor.py#L232), [offset rebasing](https://github.com/LegalQuants/lq-ai/blob/2cc3149238defbbb171ec845cd0d3a43a34054f2/api/app/playbooks/easy/extractor.py#L434)

Clustering uses a threshold tuned on a synthetic NDA corpus. Its “modal” selection is a semantic representative, or the longest clause when embeddings fail; nearby alternatives are not necessarily approved negotiating fallbacks. Overlapping spans can duplicate clauses and bias aggregation. Preserve unique source spans, extraction failures and actual approval history; separate governing law from venue and require human acceptance of every generated position. [Clustering](https://github.com/LegalQuants/lq-ai/blob/2cc3149238defbbb171ec845cd0d3a43a34054f2/api/app/playbooks/easy/clustering.py#L98)

## 5. Prompt test plans and legal standards need real acceptance work

The repository's acceptance-test mini-PRD explicitly says the real-document acceptance pass is missing. No populated first-party `acceptance/` directories were found. Community prompt evals are manually run specifications, not completed evaluation records. [Acceptance status](https://github.com/LegalQuants/lq-ai/blob/2cc3149238defbbb171ec845cd0d3a43a34054f2/docs/contribute/mini-prds/skill-acceptance-tests.md#L3), [community eval method](https://github.com/LegalQuants/lq-skills/blob/a293659770c6d9094e3f9893a0de6e59475e95b6/evals/README.md)

There are concrete prompt inconsistencies:

- `contract-qa` calls Type C comparison/unusualness and Type D scenario; its test plan calls C calculation and D cross-clause comparison. Align the taxonomy before measuring success. [Skill](https://github.com/LegalQuants/lq-ai/blob/2cc3149238defbbb171ec845cd0d3a43a34054f2/skills/contract-qa/SKILL.md#L101), [test plan](https://github.com/LegalQuants/lq-ai/blob/2cc3149238defbbb171ec845cd0d3a43a34054f2/skills/contract-qa/test-plan.md#L67)
- Snapshot introductions equate failed extraction with `not found`, while NDA/MSA endings distinguish parse errors. Keep one typed status contract. [NDA snapshot](https://github.com/LegalQuants/lq-ai/blob/2cc3149238defbbb171ec845cd0d3a43a34054f2/skills/nda-snapshot/SKILL.md#L64)
- DPA review offers compliance-sounding overall labels while disclaiming final compliance analysis. Use source-backed term coverage and unresolved requirements instead of a compliance certificate. [DPA posture](https://github.com/LegalQuants/lq-ai/blob/2cc3149238defbbb171ec845cd0d3a43a34054f2/skills/dpa-checklist-review/SKILL.md#L113)
- Generic market, severity, privacy, privilege and interpretation assertions are practitioner starting points; this review did not independently validate them against current law. Jurisdiction-specific UK/SG instructions must not be applied to US matters unchanged.

## 6. CoQuill needs strict validation and isolation before becoming a user-facing tool

CoQuill has real scripts, but default Jinja rendering turns a missing variable into an empty string. The subsequent token scan passes because the unresolved token is gone. This was reproduced with its constructor and validator. Use typed required-input validation and `StrictUndefined` before any rendering. Blind boolean coercion also changes a literal answer `No` to `False`. [Renderer](https://github.com/LegalQuants/lq-skills/blob/a293659770c6d9094e3f9893a0de6e59475e95b6/skills/coquill/renderer/render.py#L227)

The script joins a caller-supplied job name to an output path without checking containment. Jinja templates are not sandboxed and HTML output is not autoescaped. Treat templates as approved code; enforce server-side directory boundaries, resource limits and an isolated renderer with controlled file/network access before accepting user-created templates. Existing scripts were not run on untrusted content. [Output paths](https://github.com/LegalQuants/lq-skills/blob/a293659770c6d9094e3f9893a0de6e59475e95b6/skills/coquill/renderer/render.py#L58)

Its analyzer misses filtered variables such as `{{ client_name | upper }}`. Multiple templates are rejected in the prompt but the script itself takes the first matching directory entry. Manifest validity must be enforced by code, using a supported grammar or parser. [Analyzer](https://github.com/LegalQuants/lq-skills/blob/a293659770c6d9094e3f9893a0de6e59475e95b6/skills/coquill/analyzer/analyze.py#L112)

The interview transcript formatter loses display times on this Windows runtime (`%-I`) and omits prefilled values from its confirmed-values section when there are no question/answer groups. Both were reproduced. It is an interview log formatter, not speech recognition. [Transcriber](https://github.com/LegalQuants/lq-skills/blob/a293659770c6d9094e3f9893a0de6e59475e95b6/skills/coquill/transcriber/transcribe.py#L40)

## 7. Privacy citation-audit “clean” is not citation verification

The community linter deliberately skips Markdown bullets, numbered items and table rows. It also accepts a generic `§ 999999` string as a citation-shaped token without retrieving any authority. The offline probe returns a missing-citation error for a plain sentence and no findings for the same sentence as a bullet/table row. Do not expose this as an automatic Bluebook, legal-existence or source-support checker. [Auditor exclusions](https://github.com/LegalQuants/lq-skills/blob/a293659770c6d9094e3f9893a0de6e59475e95b6/skills/us-state-privacy-navigator/scripts/citation_audit.py#L164), [generic token](https://github.com/LegalQuants/lq-skills/blob/a293659770c6d9094e3f9893a0de6e59475e95b6/skills/us-state-privacy-navigator/scripts/citation_audit.py#L120)

Replace it with a claim ledger that covers every output block, uses a real citation resolver and separately reports format, existence, pinpoint, quoted text, proposition support and treatment/currentness. The navigator's static legal references and thresholds are not included as authoritative law in this packet.

## 8. Separate reusable instructions from external tools and licensing

Several community skills describe useful Word-diff, redline, text-provenance or private citation applications; their code is not actually in these skill folders. Dependencies and access must be assessed separately. Two MSA playbooks cite CC BY source templates not fully mapped in root NOTICES. Keep their source attribution and verify versions before copying them into a firm distribution. See `LICENSE-AND-PROVENANCE.md`.

Do not flatten identical skill names across the parent and community trees. Preserve repository, author, version, commit and evaluation lineage, then deliberately adapt one variant into the firm namespace.
