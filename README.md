# Seeger Weiss document library

A portable, static reference library with searchable court documents, court and judge assets, primary-law lookups, workflow resources, agent specifications and settlement intelligence.

## Open locally

Clone the repository, then open **index.html**. For a local HTTP preview:

```sh
python -m http.server 8090 --bind 127.0.0.1
```

Visit `http://127.0.0.1:8090/index.html`. No npm install, build, account, API key or backend is required. GitHub's file viewer displays source rather than running these pages. The document collection is several gigabytes; a clone preserves the complete linked downloads.

## Pages

| Page | Included functionality |
|---|---|
| [Documents](index.html) | Search and filter 11,181 retained English court documents; open original PDF, DOCX, DOC and RTF files |
| [Court coverage](COVERAGE.html) | Court/jurisdiction coverage and explicit gaps |
| [Court and judge assets](05-Court-and-Judge-Assets/ASSET-INDEX.html) | Court marks and named portraits with source and reuse context |
| [Rules](RULES.html) | Scoped court rules and procedure references |
| [Primary law](LAW.html) | 1,077 indexed provisions from U.S. Code Titles 9 and 28 and the Title 28 appendix |
| [Additional sources](EXTENDED-LAW.html) | 5,856 selected New Jersey entries and 233 FDA regulation entries |
| [Settlements](SETTLEMENTS.html) | 848 source records, search/filters, saves, comparison, exports and research briefs; nine dated reviews and four original PDFs |
| [Workflow toolkit](TOOLKIT.html) | Reviewed source resources and eight litigation recipes |
| [Agent skills](SKILLS.html) | 150 capabilities, 146 full instruction files, contracts and task-brief exports |
| [Platform resources](CORPUS.html) | 20 source references and five deterministic local tools |

## Integration

See [INTEGRATION.md](INTEGRATION.md). Keep the relative directory layout so document, data and asset links resolve. The code is framework-independent; agent execution, production connectors, user authentication and shared persistence are host responsibilities. These static pages use browser storage for saved selections.

This public export includes the files needed by the library and its linked reference downloads. Private platform implementation maps, local acquisition logs, cleanup/recovery queues, source archive inventories, browser screenshots and development backups are omitted. The original local working library remains separate.

## Source scope and reuse

Public availability does not certify current legal applicability. Preserve court/jurisdiction, edition, source dates, legal authority, document hashes and individual rights notes. Agent instructions and synthetic acceptance cases are configuration/evaluation material, not legal evidence or measured model accuracy.

Settlement fields are attributed publisher assertions. They remain separate from the nine bounded source reviews; the full 848 records are not independently verified claims. Data: [SettleSignal (settlesignal.com)](https://settlesignal.com/), under the statement retained in its [notice](07-Settlement-References/catalog/NOTICE.md).

Copied open-source material retains its original licenses and notices. See [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md). No blanket license or third-party endorsement is asserted for all court documents, images and data.
