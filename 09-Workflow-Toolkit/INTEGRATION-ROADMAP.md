# Applying the reviewed toolkit to Seeger Weiss

This is an integration design and acceptance plan. It does not imply that the offline library executes agents, authenticates users, edits Word files, schedules jobs, or connects to Bedrock. The upstream packet preserves code and prompt files for inspection. The original litigation recipes describe work the host must implement and evaluate.

## Highest-impact sequence

### 1. A source receipt for every finding

Start with a common evidence object across research, depositions, working sets, tabular cells and Office outputs. Store matter ID, source file hash/version, exact source identifier, extraction version, page/line or validated character span, quote, finding type, retrieval time, source release date and verification method. Hashes identify bytes, not truth. Keep factual allegations, witness statements, model inferences and legal conclusions distinct.

The UI should distinguish **exact text located**, **paraphrase supported**, **ambiguous location**, **source unavailable**, **not checked**, and **review required**. A citation ledger containing no evidence must never receive a positive accuracy grade. Capture rejected candidates and sources that failed retrieval so an absence is visible.

Acceptance: repeated quote on two pages; quotation crossing a chunk boundary; quote relocated to another page; scanned page with no text; unsupported source index; missing source; zero-claim output; partial extraction; changed source hash; incompatible historical version. Exact quotation matching alone never establishes legal relevance or currentness.

### 2. A coverage matrix for document workflows

For each document × question, record `queued`, `running`, `answered`, `not_found_after_completed_scan`, `needs_review`, `failed`, or `cancelled`. Distinguish an unsuccessful retrieval from a completed negative review. Keep extraction coverage and analysis coverage separate. Use bounded parallelism, idempotent run IDs, checkpointing, per-cell retries for transient failures and a visible residual-work list.

In bulk deposition work, preserve witness/date/proceeding/page-line identities across uploads. In tabular review, snapshot the proposed columns and prompts, let counsel edit them, then freeze that revision for the run. A negative response must name the scope actually searched and missing/unreadable files. Test cancellation, resume, partial batch failure, duplicate uploads, changed columns and budget exhaustion.

### 3. Court and authority research tied to the matter

Join the library's court roster, judge assets, court-form catalogs and source versions using stable court IDs. Select sources by jurisdiction, case type, judge and relevant date. An official-host source is preferred evidence of publication; it is not automatically controlling or current for the matter. Do not silently promote settlement notices, generic examples or historical provisions into reusable filing templates.

The reviewed source-registry pattern is valuable: show configured/reachable sources, explicit coverage, allowed operations and unavailable reasons. Keep the original source URL and version attached when using the U.S. Code, New Jersey compilation or FDA selection. The New Jersey package has a legislative cutoff; GPO's eCFR XML has separate amendment and file dates. Do not flatten either into a generic “current” badge.

### 4. Human-reviewable document outputs

Generate an evidence matrix or outline first, then render into a trusted firm template. Separate substantive changes from formatting changes, provide an edit manifest and preserve the original document. Compare expected and actual edits at document anchors; avoid whole-document replacement for a small requested edit. Keep privileged source material out of logs and public render services.

For CSV, neutralize spreadsheet formula prefixes while retaining an exact raw value in a typed JSON artifact. For XLSX, emit untrusted content as literal strings and verify the workbook XML contains no formulas from source text. Validate DOCX structure, links, tables, footnotes and tracked changes in both parser and actual Word rendering. The upstream Word add-in is a scaffold, not a ready-made accurate editor.

### 5. Governed background work

Adapt the useful plan → act → observe pattern with matter-scoped tool grants, explicit budgets, cancellation, action receipts and durable jobs. All external writes need host policy and the user's authorization. A connector's own `readOnlyHint` is not sufficient authorization. Model/provider routing restrictions must reach the tool invocation, including resumed calls and scheduled runs.

Bedrock, AgentCore, Knowledge Bases, Outlook, Box and DocketBird are host-side integration projects. The pinned LQ.AI repository does not supply a working Bedrock adapter. Map reviewed concepts into our services instead of importing its database, auth or web shell wholesale. Keep secret references server-side; do not embed API keys in skills or exported workflow JSON.

## Source refresh design

Maintain `source_id`, `retrieved_at`, `publisher_release`, `content_hash`, `license_or_terms`, `parser_version` and `validation_status`. For a refresh, acquire to staging, verify content type and schema, compare source identifiers/headings, retain effective-date notes, detect ambiguity and promote only validated records. Changed rules should enter a review queue before altering matter advice or calendar events. No background monitor is installed by this packet.

## Licensing boundaries

Follow the per-file provenance manifest. The root Apache license does not erase the web fork's branding conditions, third-party skill terms, attributed playbook content, or dependency obligations. Community skills may be jurisdiction-specific. Preserve notices and licenses, document modifications, and inspect dependencies before execution. The detailed review records code provenance that needs further checking, including the MCP module described as ported from Open WebUI.
