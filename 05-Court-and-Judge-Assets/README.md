# Court and judge identity assets

The portable delivery is an integration-ready court identity pack for a Matters
interface. Its `images/` directory contains **only accepted image files referenced
by `assets.jsonl`**. Original downloaded bytes are retained. No images were generated,
redrawn, cropped, or substituted with third-party portraits. No platform code was changed.

Start with **ASSET-INDEX.html** for the searchable offline preview and **SUMMARY.json**
for final counts. The court map contains **269 explicit court/judiciary entries**:
207 federal jurisdiction/special entries, 56 state, D.C., and territory entries,
and six selected local trial courts.
Some federal jurisdiction entries share a court website. The state entries represent
statewide judiciary sites. Local coverage includes Philadelphia, New York County,
Los Angeles, San Francisco, Alameda, and the City of St. Louis. This is not an
inventory of all individual county, trial, or municipal courts.

## Portable delivery

| File | Purpose |
|---|---|
| `court-assets.json` | Map keyed by stable court ID; primary and compact image paths, background, source, and explicit text fallback |
| `resource-assets.json` | Separate national U.S. Courts resource identity, outside the 269 court/judiciary count |
| `judge-assets.json` | Fourteen explicitly identified original judge photographs and profile evidence |
| `assets.jsonl` | Curated source associations, full SHA-256, size, MIME, dimensions, scope, and reuse notes |
| `images/` | Accepted original image files only, content-addressed by SHA-256 and referenced by `assets.jsonl` |
| `ASSETS.csv` | Spreadsheet version of curated associations |
| `COURT-COVERAGE.csv` | Every court entry, including access failures and gaps |
| `VALIDATION.json` | Fresh file-hash and manifest checks |
| `BROWSER-VALIDATION.json` | Independent Chromium rendering, filtering, and all-image decode results |
| `asset-policy-exclusions.json` | Candidate image associations excluded after published source/redirect policy review |
| `ui/CourtIdentity.tsx` | Small optional React adapter with compact and wordmark layouts |
| `ui/court-identity.css` | Component-scoped styling; safe text fallback and high-contrast backgrounds |

The portable delivery excludes publisher-only branding, rejected image originals,
raw download logs, scraped page/robots evidence, and Python collection scripts.
Neither `publisher-assets.jsonl` nor the research utilities are required to use it.

## Integrating with Matters

1. Copy the **portable delivery's** `images` directory into an internal public asset
   directory, for example `public/court-identities/images`. If working directly from
   the original research workspace, copy only the `local_path` files referenced in
   `assets.jsonl`; do not copy that workspace's entire raw `images` directory.
2. Import `court-assets.json` where court entities are selected. Join by the stable
   IDs such as `FD:nysd`, `FD:njd`, `FB:nysb`, `F:ca2`, `ST:ny_state`, or
   `LC:ny_new_york`; never
   match images by loosely matching display names.
3. Use `compact_asset_path` for 28–48 px list avatars. Use `primary_asset_path` for
   a larger identity area. If the compact field is null, render `fallback_text`.
   Wide mastheads are intentionally not squeezed into tiny circles.
4. Respect `primary_background` / `compact_background`. SDNY's original white
   wordmark needs a dark background. Keep aspect ratio with `object-fit: contain`.
5. Display the court's name alongside every image. Link the source in court details.
   Separate a statewide judiciary brand from a specific local court identity.
6. Keep files on your own controlled asset host. Do not hotlink court servers on each
   user page load. Serve SVG files as `<img>` resources, never by injecting raw markup.

The six local court fallback labels are `MO22`, `PHL`, `NYC`, `LA`, `SF`, and `ALA`.
They fit compact badges; the full court name and stable court ID remain available
alongside them. `MO22` identifies the City of St. Louis's 22nd Judicial Circuit.

Example (the host controls the selected court and asset URL base):

```tsx
import courtAssets from './court-assets.json';
import { CourtIdentity } from './ui/CourtIdentity';

<CourtIdentity
  court={courtAssets['FD:nysd']}
  assetBaseUrl="/court-identities"
  variant="compact"
  showName
/>
```

The component requires the host application's React dependency; this data package
does not install a separate application. It never fetches remote branding or changes
the host's court data.

## Scope, accuracy, and reuse

- A logo was accepted because its actual URL was observed in an official court
  page, linked CSS, or official-page Firecrawl output, and the downloaded bytes
  decoded as an image. The final pass fixed HTML parsing issues and retried transient
  fetch failures; explicit access restrictions remained in place.
- Shared federal marks are tagged `judiciary_logo` and list the other observed court
  associations with the same bytes. A state judiciary seal is not automatically the
  specific seal of every court in that state. `observed_on_single_registry_entry`
  reports only what this inventory observed. It does **not** establish ownership,
  exclusivity, or court-specific uniqueness. The previous exclusivity field was removed.
- `identity_scope` distinguishes state-government marks, statewide judiciary marks,
  shared federal judiciary branding, federal/local court-site identity, shared state
  judiciary branding, icons, and portraits.
  Indiana's state seal is explicitly labeled a state-government mark. Kansas uses
  the verified `kscourts.gov` Judicial Branch identity, not the Judicial Council publisher.
  Idaho Court Assistance Office marks are excluded from the portable delivery.
  Their publisher-only records remain in the original research workspace and are
  not used to represent the entire Idaho court system.
- Pennsylvania's statewide website uses the Supreme Court of Pennsylvania seal.
  SDTX and the Idaho federal sites share marks across district/bankruptcy entries.
  Second Circuit's retained masthead contains the Chief Judge's name and should be
  reviewed when court leadership changes; compact layouts use text if no square
  identity image was obtained.
- New York County uses the shared New York State Unified Court System seal.
  Philadelphia's mark identifies the Philadelphia Courts website, not a separate
  Complex Litigation Center logo. San Francisco and Alameda have shared website
  icons, explicitly labeled as fallbacks. The St. Louis entry identifies the **City's
  22nd Judicial Circuit**, not the County's 21st Circuit. Its downloaded image
  candidates redirect to a host that disallows image crawling, so they were excluded
  from the curated manifest and replaced with a text fallback.
- American Samoa has an explicit text fallback. Its High Court is verified through
  the U.S. DOJ directory, but no official court homepage or identity image was
  verified in this collection pass. The DOJ publisher is not used as its identity.
- Some header branding is commemorative, such as Kentucky's 50-year unified system
  identity. Retrieval date records the snapshot, not a guarantee of future currency.
- Judge portraits are a bounded sample of fourteen Northern District of California
  judges. Each is explicitly identified on the official profile. All fourteen
  images were visually checked as portraits; names come from official page text,
  not face recognition. See `judge-assets.json` for names and exact profile evidence.
  Literal observed profile headings are retained as `observed_role_or_status`;
  these are snapshots, not certification of active/senior status or matter assignment.
- Two bounded passes sampled 36 named official profiles. The additional 20-profile
  pass checked SDNY, EDNY, NJD, PAED, FLSD, and CAND; only the ten CAND profiles in
  that pass provided explicit name-linked portraits. The earlier pass also sampled
  EDLA. EDNY's Brodie page used a decorative gavel, which was rejected. Use names
  or initials when no identified photograph is available.
- The final image-path policy review excluded the CAVC favicon because retrieval
  is disallowed for ChatGPT-User, and the two St. Louis image candidates because
  their redirect destination disallows image crawling. No accepted images came
  from the flagged CASD, Connecticut judiciary, or Congress hosts. Future collection
  checks both agent policies, published crawl delays, and every image redirect.
- Public availability does **not** establish a license. All asset records retain
  `permission_status: not_established` and their source URL. Confirm applicable court
  terms before public distribution or using seals in a way that implies endorsement.
- No judges are rated, profiled by personality, or inferred from photographs.
  No private case information, credentials, or platform content was transmitted.

## Validation

All curated image files were rehashed against their recorded SHA-256. SVG parsing
checks exclude scripts and foreign-object candidates from the accepted set. The
offline index uses DOM `textContent`, escaped JSON, and `<img>` for SVG/raster previews.
It has no remote JavaScript or asset dependencies.

A Node check exercised the actual preview JavaScript with its packaged data:
269 court cards, court-type and coverage filters, search, empty results, switching
to all 14 portraits, and switching back. It verified that image paths are local
and present and that no network request is made. This is a DOM-behavior check,
not a browser layout or visual-rendering certification.

An independent headless Microsoft Edge/Chromium check exercised search, court and
coverage filters, all 14 portrait cards, and tablet layout. All 295 curated images
decoded, with no script errors or remote requests; see `BROWSER-VALIDATION.json`.
This check preceded the final compact-badge text update; the image files and preview
behavior are unchanged, and the Node behavior check was rerun after that update.
Local image inspection also covered all fourteen portraits and representative
federal/state marks. Open `ASSET-INDEX.html` directly in your normal browser or file viewer.

## Original research workspace and future refreshes

The original workspace is
The original local research workspace is omitted from this public export.
It retains rejected originals, `publisher-assets.jsonl`, raw logs, page/robots
evidence, and collection/rebuild scripts for audit purposes. Those research-only
materials are **not part of the portable curated delivery** and must not be promoted
into the Matters interface. Policy-excluded images are not included in `assets.jsonl`.

To refresh the portable pack, have the source maintainer produce a newly validated
curated export from that original workspace after reviewing current source, access,
and reuse policies. Its rebuild utilities use the original raw download log and the
sibling federal, state/territory, and local-court registries; they are not installed
with this delivery. No collection script needs to be run by the integrating app.
The standalone HTML preview and optional React adapter use the delivered local
files directly. Source inputs and previous court-document originals were not modified.
