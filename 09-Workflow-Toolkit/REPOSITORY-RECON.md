# LegalQuants repository reconnaissance

Reviewed September 12, 2026 Central. Subject: `LegalQuants/lq-ai`, pinned at `2cc3149238defbbb171ec845cd0d3a43a34054f2`. The full clone and raw evidence are in the separate research workspace. This library contains an explicit selection, not a running LQ.AI installation.

## Repository vitals

- 753 commits from May 7 through September 13, 2026 (commit dates); 6,583 tracked paths.
- One fetched product branch, `main` / `origin/main`.
- 15 author identities in non-merge history. Two names dominate and may be aliases; these counts do not establish the number of independent maintainers.
- Monthly commits: May 557, June 108, July 43, August 37, September 8 through the pinned commit. September is partial, and the initial burst is not a comparable operating baseline.
- No commit subject matched `revert`, `hotfix`, `emergency`, or `rollback` in the inspected history. This does not prove the absence of incidents.

## Architecture actually present

The repository includes a Python API, an inference/tool gateway, a forked Open WebUI frontend, a Word task-pane scaffold, Slack and Teams bridges, deployment material, skill files, playbooks, and tests. The community skills directory is a pinned git submodule and is empty in an ordinary clone until separately initialized.

The API's citation, tabular review, playbook, source registry and autonomous-run modules contain real implementations. Production use still requires identity, database migrations, workers, provider configuration, source access, storage, and deployment integration. A skill's input description accepting DOCX does not prove that the runtime ingests DOCX. The pinned honest-state document explicitly describes ingestion limitations and substantive Word features as deferred.

## Change concentration and integration implications

| File or area | Changes | Bug-fix-subject changes | Implication for adaptation |
|---|---:|---:|---|
| `api/app/api/chats.py` | 41 | 18 | Keep our existing chat contracts; port bounded citation/tool patterns behind adapters. |
| `docs/api/backend-openapi.yaml` | 81 | 29 | Snapshot API contracts and exercise end-to-end request/response fixtures before adopting endpoints. |
| `api/tests/test_endpoints.py` | 54 | 21 | Endpoint tests are a useful source of behavioral cases, not evidence of compatibility with our platform. |
| `api/tests/test_openapi.py` | 45 | 21 | Reuse schema drift checks around our own API surface. |
| `api/app/models/__init__.py` | 32 | 16 | Avoid wholesale database-model or migration import. Map only the records we need. |
| `gateway/app/api/inference.py` | 23 | 9 | Treat routing, tier decisions, streaming and tool dispatch as one integration boundary. |
| `gateway/app/router.py` | — | 9 | Add matter-scoped routing and egress tests before exposing external tools. |
| `docs/PRD.md` | 91 | 52 | Roadmap prose changes frequently; confirm claims in code and tests. |

Counts are `git log --since='1 year ago' --name-only` frequencies. Bug-fix classification is a subject-keyword heuristic, not a defect rate. In the combined chat/gateway/model hotspot paths, the two leading author identities account for 86 of 91 non-merge contributions. Do not infer bus factor from aliases without maintainer confirmation.

Recent non-asset additions include the citation ledger/gate, authority text cache, derived treatment analysis, autonomous evidence registry, source adapters, tool governance, and MCP OAuth endpoints, with associated tests. Asset additions dominated an unfiltered new-file scan; the scoped code scan is the useful product signal.

## Reading order for our platform

1. `docs/HONEST-STATE.md` alongside implementation. It is unusually useful, but the code audit found gaps that the positive labels do not resolve.
2. `api/app/citation/` with its tests: quotation location, verification method, ledger coverage and failure handling.
3. `api/app/tabular/`, the worker and export endpoint: column snapshots, fanout, cell status, retry boundaries and exports.
4. `api/app/playbooks/`, built-in YAML and skill loader: declarative legal positions and explicit input contracts.
5. `api/app/research/` and gateway tool providers: availability-aware source registry and normalized retrieval.
6. `api/app/autonomous/` and `api/app/tools/governance.py`: plan/action traces, budgets, grants, cancellation and receipts.
7. The pinned community skill review: chronological evidence, proposition checking, adversarial review, and document rendering are especially relevant.

## Reuse decision

Retain our production shell, auth and Bedrock architecture. Adopt small reviewed prompt/config/helper units, preserve licenses and provenance, and write tests for the behavior we need. The copied source packet is not a safe full-platform merge. The detailed architecture review records reproducible citation, export and MCP concerns and integration requirements.

Pinned source: https://github.com/LegalQuants/lq-ai/tree/2cc3149238defbbb171ec845cd0d3a43a34054f2
