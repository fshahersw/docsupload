# Settlement collection integration

The September 13, 2026 user-supplied feed is now integrated in full: **848 catalog records** in `catalog/catalog.json`, alongside the **nine existing dated source reviews** in `verified-records.json` and **four original PDFs** in `documents/`. Open the library's `SETTLEMENTS.html`. The [catalog guide](catalog/README.md) describes its working filters, saved selections, comparison, exports, refresh procedure and host binding.

This supersedes the earlier decision to keep the full provider feed outside the active library. The supplied snapshot now explicitly contains a custom free-with-attribution statement; it is retained byte-for-byte in `catalog/publisher-feed.json`, with its credit in the UI and exports. It is not relabeled CC BY. That statement does not extend to every linked document. See [NOTICE.md](catalog/NOTICE.md).

## Record layers

1. **Publisher catalog:** all raw fields, empty values, benefits, source URLs, provider flags and dates stay under `publisher`. It is a source-discovery collection, not primary law or independently verified matter evidence.
2. **Dated review:** exact publisher-URL joins attach the original nine reviews under `review`. Keep `assessment_date`, `reviewed_at`, `independent_review.scope`, sources, limitations, discrepancies and typed event dates. This import added no new independent review.
3. **Original document:** only `status=downloaded` with a valid local path is rendered as a saved PDF. The four originals have their existing byte hashes and case-specific rights notes. Other references remain external source links, not fake local downloads.

## Accuracy requirements

Retain CRST's no-affirmative-claim process and California-class correction, Google's hearing-time uncertainty, and Lighthouse's benefit-election qualifications. Keep claims, objections, exclusions, hearings, approval and payment status separate. Never invent a cutoff time or infer current eligibility from a future claim date. The reviewed Amazon process and date remain dated findings; they are not silently refreshed by the display clock.

The provider's `verification_status`, `accepted_official_evidence` and `last_verified` fields are its own assertions. A review covers only its stated fields and sources. An empty state list means nationwide according to the feed, not a complete class definition. Benefit text mixes different units and stages and must not be summed as settlement value or per-person awards.

## Portability

Copy the full `07-Settlement-References` directory plus the root `SETTLEMENTS.html`, or use `catalog/index.html` and rebind its parent-library links. `catalog/CORPUS-REGISTRATION.json` provides the collection's integration descriptor. The standalone CSS should be scoped or isolated when embedded in an existing application shell. No platform code, backend schema, credentials or production settings were changed.
