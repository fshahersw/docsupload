# LegalQuants skill descriptions

Detailed records for all **59 existing LegalQuants skill IDs**. Each entry contains a substantive description, suitable tasks, grounded inputs, review steps, outputs, example user instructions, checks, limitations, tool requirements and provenance. Every record is classified **Prompt specification**.

## Availability

- **34 locally included skills:** `source_prompt` contains the complete unchanged canonical SKILL.md. Its UTF-8 bytes match both the original source hash and the pinned Git blob.
- **25 source-only skills:** `source_prompt` and `source.included_path` are null. Only pinned source links are provided; their instructions and supporting files were not added to the local packet.
- Ten same-name first-party/community pairs retain separate IDs, source metadata and related links. The community NDA review remains explicitly unilateral; the first-party review also supports a mutual perspective.
- UK, England and Wales, Singapore, California, privacy-regime and other specialist scope labels remain explicit. Source jurisdiction tags on technical recipes are preserved in original metadata and are not widened into legal applicability claims.

## Files

- `records.json` — portable array for the parent Agent Skills Library.
- `VALIDATION.json` — structural checks, source hashes, local-link hashes and scope limits.
- `EXPORT-VALIDATION.json` — independent JSON round-trip check and byte comparison of all 177 linked local files with pinned Git blobs; passed.
- `profiles.py` — editorial descriptions derived from the reviewed sources.
- `build_records.py` — reproducible read-only-source builder and validator. It writes only this workspace directory.
- `verify_export.py` — independent export validator; run after the builder.

## Pinned sources

- [LegalQuants/lq-ai](https://github.com/LegalQuants/lq-ai/tree/2cc3149238defbbb171ec845cd0d3a43a34054f2): `2cc3149238defbbb171ec845cd0d3a43a34054f2`.
- [LegalQuants/lq-skills](https://github.com/LegalQuants/lq-skills/tree/a293659770c6d9094e3f9893a0de6e59475e95b6): `a293659770c6d9094e3f9893a0de6e59475e95b6`, the parent repository's pinned community gitlink.

Existing catalog inputs: `09-Workflow-Toolkit/LegalQuants/SKILLS.json` and `09-Workflow-Toolkit/TOOLKIT-CATALOG.json`. Per-skill Apache-2.0 or MIT license locations and license SHA-256 values are preserved. A skill's license does not license a separately named external service or library.

## Schema notes

The requested fields are unchanged. Extra fields are `source_prompt`, `availability`, `practice_areas`, `strengths` and `provenance`. `provenance.original_metadata` and `original_description` preserve the reviewed source descriptions in full, including upstream promotional wording or instructions; these are attributed source material, not validated capability claims. Frontmatter input schemas are preserved exactly where present. Other inputs are editorial extractions from the reviewed skill body, with that distinction recorded per entry.

`files[].path` and `source.included_path` are relative to the canonical Court-Document-Library root. `files[].url` is a pinned GitHub blob link. The host should render all prompt and metadata text inertly, never execute it on catalog load, and only use a skill in an explicitly authorized workflow with the indicated host tools and review.

## Validation

All 59 IDs and original skill hashes match the existing catalog and pinned Git objects. All 34 embedded prompts equal the unchanged canonical copies. 177 unique local file links exist; 207 pinned remote file references resolve in the pinned Git trees. Inputs, required fields, categories, related IDs, source-only boundaries and display encoding checks passed. Input catalogs and source-clone status were unchanged.

No model workflow, external service, Office adapter, legal analysis, or underlying helper was run for this metadata task. The existing helper findings are surfaced as integration limitations, not reported as new tests. Examples are suggested instructions, never claimed results. No canonical library files were modified.

Records SHA-256: `26c9e951e0a48f4c50aa87775a8cfb6f97505d7b24f4b247a45ebde256670e11`.
