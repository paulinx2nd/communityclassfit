# Source Provenance

## Collection behavior

No external source is fetched. Node descriptions and participant evidence are public caller-attested text.

The contract performs no live web request, does not scrape a page, and does not silently claim that a label or URL authenticates its publisher. This avoids validator drift from changing pages. If an application needs live retrieval, that retrieval belongs in a separately reviewed mechanism whose validators independently fetch and normalize the same source.

## Integrity bindings

- Contract source SHA-256: `f191bb2daa6e1fc69e0244d849040b05423387b53fd7fa0cbea9274f1a694861`
- ABI SHA-256: `2efc291e6265077e4b2201172bb17b62b74e6039462600a6cdb63661aa84ca5e`
- Frozen text and canonical JSON records are hashed inside the contract where the workflow needs a content binding.
- Human-readable source references, when present, are expressly marked unverified.

## Fixture policy

Tests use synthetic public fixtures written for this repository. They are not copied production records and do not represent real people.
