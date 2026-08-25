# CommunityClassFit

A reusable prerequisite-DAG placement protocol where validators map demonstrated mastery, code derives the reachable frontier, an instructor offers one frontier node, and the participant accepts or declines.

## Why GenLayer

Validators independently agree on the prerequisite-closed mastery mask derived from frozen public evidence. The graph deterministically exposes only currently reachable nodes, and enrollment requires a two-party offer/acceptance handshake.

## Roles

- pathway instructor
- participant
- GenLayer validators

## Lifecycle

publish topological pathway -> open journey -> consensus mastery mask -> deterministic frontier -> instructor offer -> participant answer

## Contract interface

- Constructor: none
- Write methods: answer_offer, cancel_journey, map_mastery, offer_class, open_journey, publish_pathway
- View methods: get_journey, get_journey_count, get_journey_id, get_pathway, get_pathway_count, get_pathway_id
- Runner: `py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6`

## Public-data warning

All contract inputs, evidence, notes, addresses, model results, and state are public. Do not submit secrets, private documents, personal contact information, or confidential identifiers.

## Source model

No external source is fetched. Node descriptions and participant evidence are public caller-attested text.

## Verification

```text
genvm-lint check contracts/community_class_fit.py
genvm-lint typecheck contracts/community_class_fit.py --strict
python -m pytest tests/direct -q
python tests/run_glsim.py --port 4000 --validators 5 --no-browser
python -m pytest tests/integration -q -s
```

The repository contains seven direct tests and one full five-validator GLSim flow. StudioNet evidence is recorded separately under `deployments/` after network execution.

## Limitations

The protocol does not verify certificates or instructor identity. Subjective or incomplete evidence can cause rotation or conservative placement.

Licensed under MIT. See `LICENSE`.
