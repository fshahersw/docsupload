# Lavern agent library: source and reuse review

The staged packet contains **72 distinct library records** from `AnttiHero/lavern` at commit `526a3b833705153a056770e3acb4c7e3c1e1c210`: 59 specialist agents, nine orchestration prompts and four profile-only orchestration archetypes. These are source-backed specifications, not installed agents or tested legal services.

The user-referenced `agents/lavern/lavern-agents.json` does **not** exist in this pinned tree. This catalog was reconstructed transparently from actual TypeScript sources; it is not represented as that missing file. The clone has one available commit and is shallow, so this review makes no history-based maintenance or quality claims.

## Inventory and identity

- `src/agents/definitions.ts` has **59 specialist definitions**. Each maps to a real prompt and profile.
- `src/agents/prompts/` has **67 files**: 59 specialist prompts and eight workflow/orchestrator prompts. `transformation.ts` exports the prompt for the actual role `transformation-specialist`; the catalog uses the role identity rather than inventing a second identity from the filename.
- `src/workflows/templates/pre-engagement.ts` supplies a ninth, **inline** orchestration prompt. Its record is `lavern-pre-engagement`, with its template source and inline-prompt status disclosed.
- `src/agents/profiles.ts` has **63 actual profile keys**, despite its stale comment saying 62. The four extra keys are `orchestrator-conductor`, `orchestrator-closer`, `orchestrator-professor` and `orchestrator-fixer`. They have no standalone specialist definitions or separate prompts. Their records are `Profile only`, with `source_prompt: null` and no invented input/step/output contract.
- Nine workflow templates provide explicit connections between prompts, required agent definitions, orchestration archetypes and gates. A relationship in the catalog does not imply that an agent executes: Tabulate's evaluator is an explicit bootstrap exception.

The 100 unchanged selected source files contain prompts, their seven literal knowledge dependencies, profile/agent definitions, type/schema files, workflow definitions/mapping, LICENSE and NOTICE. No installer, service, dataset, photograph, font, runtime dependency or application bundle is included.

## How the records were made

The review reads exact `git show COMMIT:path` blobs and uses the already-installed TypeScript compiler **only as a parser**. It does not import, evaluate or transpile-and-run any upstream module. Prompt literals and their named literal knowledge constants are resolved from the syntax tree, not by executing JavaScript. The inline onboarding prompt is extracted from its actual template property.

Every populated `source_prompt` preserves the full extracted base prompt. For eight prompts with knowledge imports, it includes those statically expanded literal dependencies, listed with hashes in `source_prompt_dependencies`. No raw prompt is cut by a character limit. The source file remains byte-for-byte unchanged and downloadable. Runtime session context, specialist `enrichPrompt` additions, firm personality and permission enforcement have **not** been applied to these strings.

The catalog separates:

- **Curated overview:** source-grounded role summary, method, intended users and use triggers, with no invented ratings, model rankings or simulated billing.
- **Editorial preparation:** inputs, adaptation examples and abbreviated methods. These are explicitly marked as library guidance rather than validated upstream APIs or measured use cases.
- **Source instructions:** complete base prompts, original output specifications, declared schema fields, qualitative profile descriptions, critical rules, success criteria and tool identifiers. These are author statements and configuration data, not proof that a capability exists or has run.

Original numeric personality axes and illustrative values remain visible inside the source instructions and original files. They are explicitly author-assigned and unbenchmarked. A risk example, confidence value, fee or budget in a source prompt is not an actual estimate for the user's matter.

## Concrete integration findings

### 1. Preserve unknown currency; do not adopt the USD fallback

The Tabulate prompt instructs the agent to assign USD to an ambiguous dollar sign and lower confidence. That creates a substantive value not established by the document. The original is preserved, but the catalog prominently says to **replace this rule before reuse**: retain unknown currency, preserve the raw symbol and source quotation, and resolve it through document context or human input. Test ambiguous USD/AUD/CAD cases and mixed-currency tables. [Pinned source, line 149](https://github.com/AnttiHero/lavern/blob/526a3b833705153a056770e3acb4c7e3c1e1c210/src/agents/prompts/orchestrator-tabulate.ts#L149).

### 2. Counsel and Tabulate have no independent evaluation gate

Current Counsel instructions prohibit Task subagent dispatch and answer directly from supplied document context. Its template excludes Task and explicitly has no evaluator, debate or human gates. Older profile/mapping language and one step description still mention dispatch. The record follows the current prompt and tool list, without promising those omitted controls. [Counsel template, lines 3–9](https://github.com/AnttiHero/lavern/blob/526a3b833705153a056770e3acb4c7e3c1e1c210/src/workflows/templates/counsel.ts#L3), [Task removal, line 40](https://github.com/AnttiHero/lavern/blob/526a3b833705153a056770e3acb4c7e3c1e1c210/src/workflows/templates/counsel.ts#L40).

Tabulate is likewise an orchestrator-only extraction flow. The template lists `evaluator` because the executor needs an agent definition to boot the SDK; this does **not** run an evaluator gate. The catalog calls this a bootstrap relationship. [Tabulate template, lines 18–20](https://github.com/AnttiHero/lavern/blob/526a3b833705153a056770e3acb4c7e3c1e1c210/src/workflows/templates/tabulate.ts#L18), [bootstrap comment, line 70](https://github.com/AnttiHero/lavern/blob/526a3b833705153a056770e3acb4c7e3c1e1c210/src/workflows/templates/tabulate.ts#L70).

### 3. Reconcile detailed prompt outputs with shared schemas

The Litigation Associate prompt asks for `researchMemorandum`, `caseDigest`, `factualChronology`, `motionComponents` and `discoveryStatus`. Its definition assigns the shared `LitigationLawyerOutputSchema`, whose top-level fields instead include `executiveSummary`, `caseAssessment`, `arguments` and `strategyRecommendation`. A host must deliberately map the requested detail or extend the schema; do not silently discard it. The same review is needed for other practice-group schemas and several original schemas with more detailed prompt examples. Each specialist record exposes its actual assigned schema, fields and full prompt output section. [Prompt, line 124](https://github.com/AnttiHero/lavern/blob/526a3b833705153a056770e3acb4c7e3c1e1c210/src/agents/prompts/litigation-associate.ts#L124), [assigned schema declaration, line 539](https://github.com/AnttiHero/lavern/blob/526a3b833705153a056770e3acb4c7e3c1e1c210/src/types/output-schemas.ts#L539).

### 4. Repair the abstention-tool mismatch

`enrichPrompt` adds universal guidance to use `decline_to_find` for insufficient context or uncertainty. The declared tool lists for **evaluator, risk-pricer, paralegal and legal-intern** omit that tool. The catalog flags all four; a host should offer an explicit abstention channel rather than assuming the source instruction is sufficient. No tool call was attempted to test this. [Universal guidance, line 112](https://github.com/AnttiHero/lavern/blob/526a3b833705153a056770e3acb4c7e3c1e1c210/src/agents/definitions.ts#L112).

### 5. Profiles and gates are different mechanisms

The executor constructs an orchestration prefix from the profile's display name, tagline and work style. It then appends the workflow prompt and separately configures allowed tools and dynamic permission handling. A profile's critical rules or promises about evaluator checks are not a standalone enforcement layer. This matters particularly for the Fixer archetype attached to the gate-free Counsel and Tabulate flows. [Executor, lines 351–371](https://github.com/AnttiHero/lavern/blob/526a3b833705153a056770e3acb4c7e3c1e1c210/src/workflows/executor.ts#L351).

### 6. Legal and empirical claims need actual evidence services

The research prompts' instructions to verify citations do not supply a citator. Distinguishing an authority is not the same as overruling it; preserve treatment types, jurisdiction, pinpoints and supporting text. Simulated client/user feedback is not an actual study. Risk-pricer probability and insurability outputs are uncalibrated scenario estimates, not an actuarial result or insurer quote. Accessibility review needs actual rendered artifacts and applicable standards. These domain limitations are included in affected records rather than presenting persona language as demonstrated capability.

## Reuse and licensing

The selected source is distributed under the upstream root **Apache License 2.0**. The packet retains unchanged LICENSE and NOTICE, provenance URLs, commit, Git blob IDs and SHA-256 hashes. The manifest distinguishes the exact copied source from the original editorial catalog.

The original NOTICE also discusses datasets, fonts, photographs and npm dependencies. Those materials are not included here; their appearance in NOTICE does not mean the packet contains them or that this review independently validated every dependency license. A later full-runtime integration must review the dependencies it actually uses. Do not reuse upstream branding to imply a relationship with the author or treat simulated firm identities as actual Seeger Weiss personnel.

## Safe integration boundary

Render these records as inert content. Do not load TypeScript modules to display a card: several workflow files register themselves on import. Do not promote source `availableTools`, `phasePermissions`, model preferences or statements inside prompts into a host permission grant. The source text is research data until an authorized developer deliberately adapts it.

For a Seeger Weiss host implementation, retain the useful role decomposition, evidence requirements, disagreement records and separate review artifacts. Supply the firm's own authentication, matter isolation, source retrieval, historical authority, typed outputs, approval state and tool adapters. Validate extraction coverage, unmapped output fields, adverse authority, uncertain values, cross-matter access and failed/partial runs before enabling execution. This packet contains no deployment or integration into the production platform or the MCO repository.

## Validation evidence

`SELF-CHECK.json` reports the schema and identity counts. `SOURCE-MANIFEST.json` and the portable packet manifest record exact source provenance. `FREEZE-VALIDATION.json` records the final independent Git-blob/hash, source-prompt completeness, reference and clean-clone checks. This review ran no upstream tests, installers, services, model calls or paid APIs; any statement about workflow behavior above is a static source finding, not a runtime benchmark.
