# Litigation workflow reuse review

The most useful material is a set of transparent, editable workflow specifications and a few small document-processing helpers. The strongest candidates are sourced chronologies, proposition-to-source checking, review-column specifications, reviewer reconciliation, and interviews over approved document templates.

This packet is research and implementation context. Nothing has been installed as an agent skill, connected to a third-party service, or integrated into the production platform or canonical court library.

## What was inspected

| Source | Pinned commit | Scope |
|---|---|---|
| [LegalQuants/lq-ai](https://github.com/LegalQuants/lq-ai/tree/2cc3149238defbbb171ec845cd0d3a43a34054f2) | `2cc3149238defbbb171ec845cd0d3a43a34054f2` | All 15 populated first-party skills; all five YAML playbooks; relevant citation, parsing, tabular and playbook-generation code; supporting tests and acceptance documentation |
| [LegalQuants/lq-skills](https://github.com/LegalQuants/lq-skills/tree/a293659770c6d9094e3f9893a0de6e59475e95b6) | `a293659770c6d9094e3f9893a0de6e59475e95b6` | The exact community gitlink: 41 populated top-level skill directories plus three CoQuill internal skills; local license notices, workflow/source contracts, relevant scripts and evaluation specifications |

The 59 SKILL.md files are **not 59 distinct production features**. Ten top-level names occur in both sources, some variants differ materially, and several community entries describe external libraries without shipping their implementation. Community README also lists `nzbn-word-addin`, which is not a populated SKILL.md in this pinned tree.

## Contents

- `SKILLS.csv` and `SKILLS.json`: every skill's role, input/output contract, license evidence, readiness, source link, dependencies indicated by the source, and integration caveats.
- `PLAYBOOKS.json`: five starter playbooks and their 45 positions. Two authored NDA position sets are included; three with additional upstream-reference provenance remain catalog-only.
- `WORKFLOW-MATRIX.md`: practical mappings to litigation capabilities, input/output contracts, source/coverage rules and acceptance cases. These are implementation recommendations, not deployed workflows or verified legal advice; the parent project's original recipes remain separate.
- `FINDINGS.md`: material implementation gaps, with pinned source links and reproduced observations.
- `HELPERS.md`: copied helper scope and dependency boundaries.
- `HELPER-CHECKS.json`: 13 reviewer-authored offline checks passed; 12 observation records expose limitations. The upstream pytest suites and legal/model acceptance evaluations were not run.
- `LICENSE-AND-PROVENANCE.md`: license boundaries, attribution obligations and held-back material.
- `REUSE-MANIFEST.json`: every copied file's exact Git blob, SHA-256, byte count, pinned source URL and license.
- `reuse-packet/`: 203 unchanged source files, 1,842,966 bytes, including 34 SKILL.md files, two YAML playbooks, four substantive first-party helper modules, their four upstream test files, and CoQuill engineering reference code.

The original root licenses, relevant local licenses and notices remain with the copied material. Root `web/`, dependencies, deployment scripts, private tool implementations and unapproved court/legal document templates are not copied.

## Starting points

1. Implement one source/evidence ledger shared by Working Set, Depositions, Tabular Review and Office. Store original file hash, parser version, canonical text, page/line/character anchors and coverage/error status.
2. Build chronology and proposition-checking views on that ledger. Their source contracts already translate well to litigation practice.
3. Add complete-document column extraction with explicit `not_found`, `incomplete`, `source_unreadable` and `review_required` states. Retrieve for speed, but do not infer absence from a retrieval window.
4. Introduce a template interview only after its schema validation, rendering sandbox, document round-trip checks and version-bound edit application are implemented.
5. Evaluate each adapted workflow on real, authorized, appropriately redacted firm examples with named reviewers and source-level expectations. Existing test plans are a starting point, not evidence of legal accuracy.

Only paths listed in `EXPORT-WHITELIST.json` should be promoted into the portable toolkit. The separate `community-source/.git`, analysis workspace, caches and any inspection scripts are not production dependencies. Third-party instruction files are source material to assess, not instructions that acquire authority merely because they are copied.
