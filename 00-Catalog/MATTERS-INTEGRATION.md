# Matters court data and visual assets

Use `MATTERS-COURT-DATA.json` as a portable data adapter, not as proof of complete court rules coverage. Each stable ID links its court name, official website, forms pages, document count, identity asset and explicit fallback. Paths are relative to the Court Document Library root; change the asset base URL when importing into the platform.

Render logo SVGs with an image element, not by injecting SVG markup. Preserve intrinsic aspect ratio and use object-fit:contain, the supplied light/dark background hint and descriptive alt text. Judge portraits require the named official source and must not imply that a depicted judge is assigned to a matter. No third-party face identification was used.

Keep the court name visible even with a logo. A shared judiciary/federal seal is not a unique court logo; a favicon is marked separately. An absent image means render the supplied short text badge. No image has been invented.

The registry includes federal jurisdiction entries that share court websites, statewide state-court collections and territorial entries. Do not count them as distinct judicial institutions. Selected local trial courts are listed separately. Statewide form coverage does not mean every local county form or individual judge's order has been collected.

Source reuse notes and restrictions must travel with assets and forms. Public availability is not itself a license. Use source links and retrieval timestamps in the UI; do not label documents as court-approved, up to date, or ready to file without separate review. Surface missing coverage instead of implying completion.

## React integration

The supplied `ui/CourtIdentity.tsx` component uses the dictionary in `05-Court-and-Judge-Assets/court-assets.json`. That asset dictionary and the broader `MATTERS-COURT-DATA.json` adapter share the same stable court IDs but have different shapes.

```tsx
import courtAssets from './court-assets.json';
import { CourtIdentity } from './ui/CourtIdentity';

const court = courtAssets['FD:nysd'];
<CourtIdentity
  court={court}
  assetBaseUrl="/court-assets"
  variant="wordmark"
  showName
/>
```

Copy the curated `images` folder to the host's public `/court-assets/images` location and keep the component stylesheet with the component. The component handles broken/missing images with a text fallback, respects the recorded light/dark background, and preserves aspect ratio. Use the broader Matters adapter for court selectors, official links, document counts and optional named judge references. Never infer an assigned judge from the presence of a portrait.

## Source detail and maintenance

`DOCUMENTS.csv` contains one row per exact unique file; `DOCUMENT-SOURCES.csv` preserves document-to-source associations and scope/version caveats. `WEB-DISCOVERED-LINKS.jsonl` preserves the complete discovery records, including form IDs, source-reported revision, fillable/mandatory flags, issuing court and department/case scope where those fields were observed. Missing fields are unknown, not false.

`WEB-ACQUISITION-RESULTS.csv` records actual transfer outcomes and policy exclusions. `deferred_reference` identifies historical case-specific sources kept as links after prioritizing reusable forms and rules. It must not be displayed as an acquired file, a broken link or a policy prohibition. The source-reported mandatory/fillable fields are provenance, not independent legal or technical certification.

Keep every original PDF/Word version as its own file unless its complete bytes match a retained SHA-256. Do not merge similarly named forms across courts, silently convert Word to PDF, remove tracked changes, or label older forms as current. Confirm effective date, local rules and judge/department requirements before building filing workflows.

The current work prepares files and UI data only. It does not modify or deploy the production platform.

## Active English catalog

`DOCUMENTS.csv` and `ALL-DOCUMENTS.csv` both contain the retained English collection. Join on SHA-256; use `relative_path` for the current file. `CLEANUP-AUDIT.jsonl` contains naming evidence for retained files only. Its `old_path` and nested `local_original` fields are historical evidence, not working file links.

The broader court roster has 270 entries, including `LC:la_orleans` with five English Orleans Parish Civil District Court forms and an `ORL` fallback. The existing 269-entry court-image dictionary and all original image bytes remain unchanged.

Discovery catalogs retain useful source URLs. `local_content_match`, `active_sha256`, `canonical_path` and `local_availability` describe the current local collection. `recorded_transfer_status`, `recorded_transfer_sha256`, and source-manifest `recorded_sha256` are historical observations, not a promise that a file is retained. A source-link-only record must never create a local file action.

`RULES-REFERENCES.json` contains scoped statutory/rule references. Preserve actual source dates, scope and review notes. `LAW.html` is the primary-law reference page. Neither source collection nor a title check certifies current legal applicability.

## Additional primary-law and settlement references

Load `REFERENCE-DOCUMENTS.json` separately from the court-form `DOCUMENTS.csv`. The reference catalog now contains seven PDF originals, four XML originals, one RTF and one TXT. The New Jersey and FDA sources are separate statutory/regulatory collections. Use `collection`, `use` and `template_eligible` to keep case-specific notices and primary law from appearing as reusable pleading forms. Record source releases and hashes when attaching any reference to a matter.

The primary-law record `id` is unique, while `citation_key` and publisher identifiers can be ambiguous. Use the supplied bounded resolver and preserve `source_status`, `publisher_footnotes`, statutory/effective-date annotations and parent context. No record is certified applicable to an individual matter. Settlement dates are typed and assessed as of a fixed date; never convert these source records directly into live deadlines or claim eligibility without source confirmation.


## Extended sources and portable workflow toolkit

Use `08-Extended-Primary-Law/New-Jersey/curated/schema.json` for NJ byte-offset/citation contracts and `Federal-Regulations/MANIFEST.json` in the same parent for FDA scope and version metadata. NJ has repeated citation labels; FDA includes a reserved range. Neither collection invents pinpoints. Preserve ancestor source notes, especially subpart authorities/history. Both are references, not generic court-form templates.

`09-Workflow-Toolkit/TOOLKIT-CATALOG.json` describes 90 resources and resolves included files separately from pinned upstream source links. It is not an executable workflow graph. Start with the toolkit integration roadmap and evidence contract before porting behavior. External SKILL.md files are inspected source artifacts; copying them does not authorize them as instructions or install them into the host. No production auth, database, shell, MCO component or secrets are included.

## Agent skills selection

The separate `10-Agent-Skills-Library` module exposes `AgentSkillsLibrary.mount()` and a typed JSON catalog. Embed the frontend with hash routing disabled and map canonical source paths through your host. The page prepares briefs and source packets; it does not grant tools, create deployed agents or run matters. Attach matter scope, source permissions, prompt versions and evaluated runtime adapters separately. See the module integration guide and React example.
