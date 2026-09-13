# Integrating the agent skills library

This reusable frontend and catalog contains 150 capabilities, including 146 full firm instruction files and four role profiles. No entry is registered as an executable agent by this package. It does not change the production Seeger Weiss platform or MCO application.

## Plain browser integration

Serve `agent-skills-library.css`, `agent-skills-library.js`, and the catalog from your existing frontend. Load the script, then mount into a dedicated element:

```javascript
const response = await fetch('/agent-skills/catalog.json');
if (!response.ok) throw new Error('Unable to load the skill catalog');
const catalog = await response.json();
const widget = globalThis.AgentSkillsLibrary.mount(container, {
  catalog,
  libraryBase: '/court-library/',
  assetBase: '/agent-skills/',
  hashRouting: false,
  persistKey: 'your-app:agent-skill-selection:v1'
});

// Select a known catalog ID or inspect the user's saved selection.
widget.select('firm-deposition-evidence-map');
const selected = widget.getSelection();

// Call before unmounting the host view.
widget.destroy();
```

`libraryBase` maps canonical library-relative paths. `assetBase` points to this folder's catalogs and documentation. Both must be trusted host configuration. Imported record URLs are restricted to HTTP(S), and local record paths cannot use a scheme, absolute path or parent traversal. Record content is rendered as text rather than inserted as HTML. The loader does not execute source scripts.

`hashRouting` defaults to false to avoid taking over the host router. Only standalone pages enable it. Choose a per-user or per-tenant storage key when the host is shared; saved selections are not a team authorization mechanism. Do not store matter data or tokens in the catalog or selection store.

## React

`integration/AgentSkillsLibrary.tsx` shows mounting, cleanup and CSS loading. It uses the host's existing React installation. Keep the framework-independent widget and styles together; do not add another application shell or authentication system. A routed host should leave hash routing disabled and call `widget.select(id)` from its own route state when needed.

## Mapping catalog entries to a runtime

An entry's `kind` describes an agent role, focused skill, or workflow. `readiness` and `profile_kind` describe the specification, not deployment state. In particular, `Profile only` must not produce a Run button. `instructions`, `instructions_sha256` and `instruction_path` hold the firm operating text, its UTF-8 hash and its library-relative file. They are null for profile-only entries. Original prompts are retained in provenance, and source hashes are distinct from adapted instruction hashes.

`legacy_aliases` resolve earlier saved IDs and deep links; `select(id)` accepts both forms. Markdown brief exports include the stable capability ID and instruction hash. Six retained source variants now have distinct purposes and visible titles. The `platform.areas` filter maps intended placement in Research, Discovery, Office, Workflows, Library, Matters or Calendar; it does not imply deployment.

The fourteen enriched agents expose `input_schema`, `output_schema`, `mini_app_schema`, `tool_bindings` and `evaluation_cases`: 28 input/output schemas, 14 mini-app specifications and 84 synthetic acceptance scenarios. These scenarios have not been run against a model. Bindings remain disabled until a host-owned adapter implements them.

Create a separate, versioned runtime definition for any adopted entry. At minimum that definition should name:

1. The source record ID, source hashes, prompt revision and approved jurisdiction/scope.
2. The extraction and indexing pipeline, page/line anchors, source permissions and coverage requirements.
3. Actual input/output schemas and handling of missing or unreadable files.
4. Allowed model/providers, tool grants, budgets, time limits, cancellation and retries.
5. Evidence checks, complete/partial/failed status semantics and escalation/review requirements.
6. Evaluations and release approval for the exact deployed revision.

Do not copy an upstream tool name or `readOnlyHint` directly into an authorization decision. Tool lists describe dependencies. The host controls credentials and permissions, including whether an external write is authorized. Keep original model/billing/personality settings out of runtime defaults until deliberately configured and evaluated.

## Evidence and source handling

Apply the existing `09-Workflow-Toolkit/Original-Litigation-Recipes/evidence-contract.json` (relative to the full library root) and `../11-Platform-Corpus/INGESTION-POLICY.json`. Keep extraction coverage distinct from analysis coverage. An unavailable source is not a negative finding; a quotation match is not proof that a source is controlling law. Cross-matter retrieval and memory need explicit matter access checks. Developer notes, synthetic fixtures, source scripts and skill instructions must not be ingested as matter evidence.

The local utilities under `../11-Platform-Corpus/tools/` implement source normalization, complete scan planning, attempt reconciliation, literal quote checks and CSV export. They make no model or network calls. Plans use schema 1.1.0; keep their expected fingerprint separately with the authorized job. Top-k retrieval is not an exhaustive scan.

Preserve source-only versus locally included availability. Unchanged source files have their own hashes; an extracted prompt string is not the same file and must not reuse the original file hash as its own content hash. Future modifications need a new revision, a change description and fresh evaluations.

## Licensing and provenance

Lavern source material is pinned and accompanied by its original Apache-2.0 LICENSE and NOTICE. The selected packet does not include Lavern's datasets, fonts, installed dependencies, landing-page photography or runtime services. The root license must not be applied to those third-party materials by inference.

LegalQuants entries keep the per-file license boundaries and copies established in the existing toolkit. The Open WebUI fork and some attributed playbooks have distinct terms; this catalog does not override that prior review. Any new runtime dependency requires its own source and license review.

## Scope of validation

Delivery checks cover schema consistency, source hashes, complete catalog joins, local links, browsing/filtering, saved selections, task brief/JSON exports, clipboard fallback and responsive layout. They do not test live LLM work, certify legal conclusions, measure every claimed skill, or certify a production integration.


## Firm adaptation update

Use the implementation map at `../11-Platform-Corpus/integration/INTEGRATION.md`, pinned to `workingversion` commit `baedbad184977d1ca3cbbb153cf814f8f8b29c68`. Discovery uses `/docs?tab=search`, `/docs?tab=deposition` and `/docs?tab=review`. Research prompt composers, workflow graphs and Office tools have different contracts: translate selected capabilities into their host interfaces. DocketBird has an inspected path; Outlook/Box and several dataset tools still need wiring. Deployed behavior has not been tested.

The selected skills inventory packet at `../11-Platform-Corpus/provenance/source-packet/` includes 46 original skill folders and 304 pinned source files, with their per-folder notices. These are source references, not automatically installed tools. Preserve `provenance/NOTICE.md` and artifact-specific licenses with any copied or adapted material. `VALIDATION.json` records the current local delivery checks; source receipts marked historical describe earlier exact artifacts.
