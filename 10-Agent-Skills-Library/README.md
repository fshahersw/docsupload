# Seeger Weiss agent skills library

Open `index.html` or `../SKILLS.html`. The library works offline: search, filter by platform page and work type, save selections, read full firm instructions, inspect integration/quality contracts, and export task briefs or JSON. No account or model is required for these local functions.

The catalog has 150 capabilities: 84 agent roles, 58 distinct skills and 8 litigation workflows. Four roles are profile-only; the other 146 have firm instruction files in `instructions/`. Fourteen enriched litigation roles additionally have typed input/output contracts, mini-app interface definitions and 84 synthetic acceptance cases in `Seeger-Weiss-Agents/`.

These are task specifications. The library does not provision agents, execute models, grant source access or connect external services. Read `../11-Platform-Corpus/integration/INTEGRATION.md` before binding a capability to Research, Discovery, Office or Workflows. The catalog's page filter is a fit map, not proof of deployment.

`catalog.json` is the canonical data file. `catalog-data.js` contains the same data for offline file URLs. `agent-skills-library.js` and `.css` are the framework-free widget; `agent-skills-library.d.ts` and `integration/AgentSkillsLibrary.tsx` support embedding in React. No dependency installation or build is needed for this standalone viewer.

`legacy-id-aliases.json` maps older IDs, including exact duplicate instruction variants, to the neutral firm IDs. The viewer resolves old deep links and migrates saved selections in memory. Task-brief contents are never stored in localStorage; only selected capability IDs are stored.

Original source identity, hashes, licensing and required notices remain in `provenance/`, `Lavern/` and the wider toolkit's source packet. `provenance/prior-source-catalog.json` is audit material; do not index it as legal evidence or auto-load its prompts. Foreign-law methods retain their actual jurisdiction.

Keep the wider Court Document Library beside this directory for source and navigation links, or map `libraryBase`/`assetBase` to the host’s source service. Read `INTEGRATION.md` for the mount lifecycle and `../11-Platform-Corpus/README.md` for the corpus layers and local validation tools.
