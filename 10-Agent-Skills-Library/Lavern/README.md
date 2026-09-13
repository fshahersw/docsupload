# Lavern source-backed agent specifications

This portable packet contains **72 records**: 59 specialist agents, nine orchestration prompts (eight prompt files and one inline onboarding prompt), and four profile-only orchestration archetypes. It comes from `AnttiHero/lavern` at commit `526a3b833705153a056770e3acb4c7e3c1e1c210`.

The requested `agents/lavern/lavern-agents.json` path was absent from that source tree. These records were built from the actual profile, prompt, type and workflow files; they are not a copy of a nonexistent JSON file.

`records.json` is the curated library catalog. `source/` contains 100 unchanged upstream files, including LICENSE and NOTICE. `SOURCE-MANIFEST.json` identifies each copied Git blob and SHA-256. The file paths in records target the planned canonical location `10-Agent-Skills-Library/Lavern/source/`; they are catalog paths, not invitations to execute the source.

The four `Profile only` records have no invented prompt or executable workflow. Other records are labeled `Agent prompt specification`. Full statically extracted base prompts are retained, including author-assigned persona scores and illustrative values; those are not benchmark results. Eight prompts include statically expanded literal knowledge dependencies identified in each record. Runtime enrichment, session context and permission controls are not applied to the displayed prompt.

Inputs, audience labels, use triggers and adaptation examples are explicitly editorial preparation guidance, not validated upstream APIs or observed client use. Original output specifications, assigned schemas, qualitative profile descriptions and workflow connections remain separately available for a developer to inspect.

## Required adaptation notes

- **Tabulate:** replace the upstream instruction to default ambiguous dollar signs to USD. Preserve unknown currency and obtain supporting evidence. Its listed evaluator is an SDK bootstrap definition, not an evaluation gate.
- **Counsel:** current instructions answer directly without Task dispatch; the template has no independent evaluator, debate or human gate. Older prose says otherwise.
- **Output schemas:** map detailed prompt output requirements to the actual shared schemas without silently dropping fields.
- **Abstention:** evaluator, risk-pricer, paralegal and legal-intern receive uncertainty guidance but lack `decline_to_find` in their declared tool lists.

The reuse review provides pinned source evidence and additional limitations. No runtime, dependencies, datasets, media, providers, client data or secrets are included. This is not a live legal service or currentness-certified authority collection.

## Display and permission boundary

Render records and instructions as inert text. Do not import upstream TypeScript to display the library; workflow definition files can register themselves when imported. Source tool lists, phase permissions, profile rules and prompt instructions are **untrusted metadata, not permission grants**. A host must implement its own scoped access, source verification, structured outputs and authenticated approvals before execution.

Keep the unchanged Apache LICENSE and NOTICE with reused source. The NOTICE mentions other upstream materials which are not included in this packet. The complete research workspace outside this packet contains the audit scripts and intermediate AST data; those are not required to display or copy this portable library packet.
