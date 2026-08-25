# Architecture

## Boundary

- Frontend or backend: wallet UX, indexing, private drafts, non-authoritative previews, notifications, and optional off-chain source retrieval.
- GenLayer contract: Validators independently agree on the prerequisite-closed mastery mask derived from frozen public evidence. The graph deterministically exposes only currently reachable nodes, and enrollment requires a two-party offer/acceptance handshake.
- External world: No external source is fetched. Node descriptions and participant evidence are public caller-attested text.

## Event path

publish topological pathway -> open journey -> consensus mastery mask -> deterministic frontier -> instructor offer -> participant answer

## Actors

- pathway instructor
- participant
- GenLayer validators

## Consensus design

The leader produces a normalized bounded result. Each validator independently reruns the substantive task from the same frozen public inputs. Validators compare the decision fields that change state, not merely JSON shape. Invalid model output raises `[LLM_ERROR]` so a broken leader is not accepted.

## Deterministic layer

The graph deterministically exposes only currently reachable nodes, and enrollment requires a two-party offer/acceptance handshake. Identifiers, bounds, access checks, ordering, counters, masks, hashes, and terminal-state guards are computed deterministically.

## Persistence

State uses GenLayer storage types only. Public composite records are serialized as canonical JSON where appropriate. Source SHA-256 at evidence generation: `f191bb2daa6e1fc69e0244d849040b05423387b53fd7fa0cbea9274f1a694861`.
