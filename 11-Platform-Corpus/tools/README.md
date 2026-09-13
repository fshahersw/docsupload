# Local corpus utilities

`corpus_tools.py` uses Python 3.10+ and the standard library. It performs no network requests, model calls, uploads or arbitrary script execution. It writes only the explicitly requested output file and refuses to overwrite an input file.

Run from this directory:

```powershell
python -B -m unittest discover -s . -v
python -B corpus_tools.py registry sources.jsonl --output normalized-sources.json
python -B corpus_tools.py plan documents.json --output scan-plan.json
python -B corpus_tools.py coverage scan-plan.json --results attempts.json --output coverage.json
python -B corpus_tools.py verify documents.json --results findings.json --output grounding.json
python -B corpus_tools.py csv findings.json --output findings.csv
```

JSONL is parsed by physical newline, preserving Unicode line separators inside JSON strings. Inputs are UTF-8 or UTF-8 with a BOM. Outputs use UTF-8. The small files in `examples/` are explicitly synthetic engineering fixtures and must be excluded from the legal knowledge base.

## Registry normalization

Provide a JSON array or JSONL records containing `url` or `canonical_url`. Equivalent protocol/host/default-port representations and common tracking parameters are normalized. Source variants remain attached to the canonical record. Meaningful query order and section anchors are retained; URLs with credentials, control characters or non-HTTP schemes are rejected. This does not determine whether two differently named legal documents are substantively identical.

The HTTP classification helper distinguishes authentication, access denial, rate limiting, timeout, TLS errors and service unavailability. A 403 does not prove a WAF and a 200 does not verify source content. TLS verification is never disabled by these tools because they do not issue network requests.

## Complete scan plan

`documents.json` is an array. Each document requires `document_id`, `matter_id`, `access_scope`, `source_version`, original-byte `sha256`, `expected_page_count`, and `pages`. A page has a one-based numeric `page`, `text`, and explicit extraction status: `complete`, `partial`, `unreadable` or `pending`.

The plan includes every expected page and preserves missing/partial/unreadable pages as gaps. Text chunks retain document, scope, version, page, start/end character and content hash. Chunks do not cross pages. Duplicate content is reported as a candidate only within the same matter/access scope; no document is deleted or access merged. Unicode offsets are Python string character offsets, not UTF-8 byte offsets, PDF coordinates or transcript line numbers.

The planner accepts extracted page text; it is not a PDF parser/OCR engine. `complete` is an extraction status supplied by the caller. A host must verify that status against its parser and original-page manifest. A complete processing report cannot prove that the OCR read a page correctly.

## Attempts and retries

Each attempt records `chunk_id`, positive `attempt`, and `status`: `completed`, `failed`, `timeout` or `pending`. Only known chunk IDs are accepted. The report identifies unfinished, retryable, pending and exhausted chunks and extraction gaps. It does not dispatch retries or overwrite partial model results. The host must bind completions to actual durable results, its cancellation policy and its source snapshot; a client-supplied completion marker is not proof of a completed model call.

## Literal grounding

Findings require unique `finding_id`, `support_status` and a `citations` array. Citations identify `document_id`, `matter_id`, `access_scope`, `source_version`, `source_sha256`, one-based `page` and a literal `quote`. The checker catches empty evidence, unknown documents, cross-scope references, wrong versions/pages and nonmatching quotations. Empty ledgers never produce a successful grounding verdict.

The result is deliberately called `literal_grounding_passed`. It does not evaluate the proposition, distinguish holding from dicta, resolve adverse treatment, certify Bluebook formatting, establish admissibility or determine whether law is current. Those need distinct reviewed results. Exact matching may reject OCR or typographic variations; route those for explicit normalization/review instead of silently accepting approximate matches.

## CSV export

Both headers and string cells beginning with formula-triggering characters receive a leading apostrophe. Values remain unchanged in the original JSON. Numeric values remain numeric. This protects the CSV representation; the host still needs its normal controls for generated Office files, macros and active document content.

## Plan version and integrity

Plans use schema **1.1.0**. Regenerate older plans. Each plan includes a document manifest, per-page text hashes, Unicode code-point units, and `plan_sha256`. Save that fingerprint separately with the authorized job and pass `--expected-plan-sha256 <fingerprint>` to coverage reconciliation. A self-contained digest detects drift but is not a signature or a substitute for host authorization.

Attempt ledgers hold one current status per `(chunk_id, attempt)`; replace a pending row when that attempt completes. A higher attempt ordinal supersedes stale pending states, while completed results remain durable. Examples intentionally contain an unreadable page and an unverified finding so their coverage and grounding checks remain false.
