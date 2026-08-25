# Version History

This record distinguishes working-tree candidates, verified checkpoints, and
published releases. A version string does not by itself prove a release.

| Version | Date | State | Revision | Scope | Scientific result |
| --- | --- | --- | --- | --- | --- |
| `0.0.0-bootstrap` | 2026-08-23 | Accepted checkpoint; not a release | `4543a2dad5c2630249906aab763ae0cbf91097ba` | Governance, documentation, repository controls, and CI bootstrap only | None |
| `0.1.0` | 2026-08-24 | Accepted checkpoint; not a release | `32e5b0dfbd93bdf337fa4f2e9bde29d0bc36a6a4` | Hash-bound rights, source gate, readiness, and external controlled intake | None |
| `0.2.0-m2-runtime-gate` | 2026-08-24 | Accepted checkpoint; not a release | `8b0636d6cc117d524256a0f7f2bd699fb64a232b` | Retained runtime failure, exact successor activation, fixed model, and synthetic lifecycle | None |
| `0.3.0-m3-protocol-freeze` | 2026-08-24 | Accepted checkpoint; not a release | `10bc499db09bccd66e3bc9289d655ab561bec857` | Complete hash-bound executable protocol, pure selection/metric implementation, fabricated replay, and controls | None |
| `0.4.0-m4-frozen-training` | 2026-08-25 | Accepted checkpoint; not a release | `53983c09a03d7f8f9453e6f492b05e58b795b876` | Three frozen train/validation runs, selected checkpoints, fresh reload, shared threshold, and exact replay | Training/validation evidence only; test unopened |
| `0.5.0-m5-retrospective-evaluation` | 2026-08-25 | Accepted checkpoint; not a release | `45b32c1cb782edc31ef8a4f49671b6a897c7d7bb` | One controlled known-test evaluation, exact replay, geospatial and rendered evidence | Lifecycle `PASS`; comparative `FAIL` |
| `1.0.0` | 2026-08-25 | Active release candidate; not yet tagged or released | `codex/reviewer-release-closeout-006` from accepted M5 | Reviewer evidence, rights-safe package, verified release, and terminal closeout | Frozen lifecycle `PASS`; comparative `FAIL` |

The accepted `0.3.0` checkpoint binds the protocol at canonical-LF SHA-256
`12a092e90586a819e6014ed181da82721675040ff2678c7d7115b1582b904f1e`.
Exact metadata bindings, seven focused tests, and all 39 approved-runtime tests
pass. PR #7 merged the reviewed tree with main CI `32689530033` passing. No
benchmark array was decoded and no scientific run or result existed at that
checkpoint.

## Incoming state

Before `0.0.0-bootstrap`, the public repository contained no commits, tags, or
releases. There is no earlier Experiment Three software or scientific version.

## Acceptance evidence

- Git tree: `6387e91f071609605f7fcc3a05842782423fbb6d`.
- Public GitHub Actions run: `32671370937`, successful.
- Live README and execution-goal blobs: verified identical to the local
  accepted checkpoint.
- Public repository description: corrected to the bounded retrospective
  framing.
- Milestone 1 acceptance: commit
  `32e5b0dfbd93bdf337fa4f2e9bde29d0bc36a6a4`, tree
  `5b2bd2904b9164b8bd3c655998749cb024202148`; candidate, pull-request, and
  merge-triggered checks passed, including main run `32679791900`.

## Accepted Milestone 1

Pull request [#3](https://github.com/drwbkr1/burnlens-experiment-three/pull/3)
merged the exact verified Milestone 1 tree to live `main` at
`32e5b0dfbd93bdf337fa4f2e9bde29d0bc36a6a4`. Candidate run
`32679733201`, pull-request run `32679735057`, and merge-triggered main run
`32679791900` passed. Direct verification confirmed the live tree and required
blobs match the accepted candidate. This is an accepted data-admission
checkpoint, not a release or scientific result.

The owner-rightsholder decision is now an exact scoped `yes`, the current
source gate is `READY`, readiness is `PASS`, and controlled intake admitted 131
approved artifacts / 3,369,748 bytes to external custody with matching
identities. Repository redistribution remains unauthorized. This candidate
is now accepted for the bounded local retrospective role.

The original blank owner-rights response remains immutable. The completed
response is private; only its hash-bound aggregate decision is public. Issue #2
was closed after live verification.

## Accepted Milestone 2 runtime-gate checkpoint

Issue [#4](https://github.com/drwbkr1/burnlens-experiment-three/issues/4)
tracks synthetic preflight from the exact accepted Milestone 1 base. The
branch first bound candidate 001 and its 20-package lock. One exact owner `yes`
was locked and reconciled, and the exact signed installer entered controlled
intake. Activation then `FAIL`ed: the same-version installer modified an
existing per-user Python product instead of creating the isolated Active-only
runtime. Inspected existing-install surfaces were restored, and no wheel sync,
model import, synthetic execution, or scientific work began.

Candidate 002 replaces only the interpreter artifact and construction route
with Python.org's application-local embeddable ZIP while retaining the exact
wheel lock. One exact separate `yes` was locked and reconciled. The activated
runtime passes 20-package compatibility, native imports, CPU gradients,
serialization, subprocess, and deterministic replay without changing the
existing Python executable.

The fixed 137-parameter model passes six neural tests and two independent full
synthetic executions with byte-identical seven-file rosters. The render was
visually inspected and the GeoTIFF reopened exactly. PR #5 merged the reviewed
tree at `8b0636d6cc117d524256a0f7f2bd699fb64a232b` with main CI
`32687957764` passing. It remains an accepted engineering checkpoint, not a
tag, release, or scientific result.

## Accepted Milestone 3 protocol freeze

Pull request [#7](https://github.com/drwbkr1/burnlens-experiment-three/pull/7)
merged the exact protocol-freeze tree to live `main` at
`10bc499db09bccd66e3bc9289d655ab561bec857`. Merge-triggered run
`32689530033` passed. This accepted the executable protocol before substantive
training; it was not a release or scientific result.

## Accepted Milestone 4 frozen-training checkpoint

Issue [#8](https://github.com/drwbkr1/burnlens-experiment-three/issues/8)
tracks the exact frozen train/validation lifecycle. Attempt 001 is retained as
`FAIL` after a fresh-process runtime-configuration mismatch. Attempt 002 is
retained as `INVALID`: all computations and replay matched, but the checkpoint
payload filename violated the frozen artifact contract. Attempt 003 reran all
three seeds from initialization but is also `INVALID` because its receipt
filenames violated the frozen artifact list. Attempt 004 used the corrected
artifact names but is `INVALID` because its seeds trained sequentially in one
process. Attempt 005 reran every seed in a fresh isolated process and passes
complete histories, finite nonzero gradients, changed weights, strict
checkpoint selection, tensor-only `weights.pt` reconstruction, exact frozen
receipt names, validation threshold `0.5`, and byte-identical
primary/replay roots. Test values remained sealed. PR #9 merged the exact
reviewed tree `51dc4ba7b4e942ad7be884051e0ce8e2fe57c6aa` to live `main` at
`53983c09a03d7f8f9453e6f492b05e58b795b876`; push, PR, and main runs
`32875659950`/`32875705749`/`32875755932` passed. This is an accepted training
checkpoint, not a release or comparative result.

## Accepted Milestone 5 retrospective evaluation

Issue [#10](https://github.com/drwbkr1/burnlens-experiment-three/issues/10)
tracks one frozen retrospective opening. Profile 006, the M5 contract, and
state reconciliation begin from the accepted M4 commit. Metadata-only audit
and fabricated path proof passed before `M5-OPENING-2026-001` consumed the test
exactly once. All frozen seeds and controls ran; primary/replay payloads match
at 53 files / 367,150 bytes / roster `e322a101...`; 36 GeoTIFFs reopen exactly
and the actual render passed direct inspection. Lifecycle is `PASS` and the
frozen comparative outcome is `FAIL`. Reviewed merge and live verification are
complete. PR #11 merged exact tree
`91fb304d4cadc450ed997c0d3f68c995b5538cb4` to live main
`45b32c1cb782edc31ef8a4f49671b6a897c7d7bb`; main CI `32879876813` passed.

## Active Milestone 6 release and closeout

Issue [#12](https://github.com/drwbkr1/burnlens-experiment-three/issues/12)
tracks public-safe reviewer evidence, deterministic package verification,
controlled scientific replay, one `v1.0.0` GitHub release, live verification,
and terminal truth. No tag or release exists at entry.

## Versioning rules

- `VERSION`, `CHANGELOG.md`, this history, status, and release metadata must
  agree at a verified checkpoint.
- A working-tree version is a candidate until its exact revision passes its
  milestone gates.
- Tags and GitHub releases may be created only from the exact verified
  revision.
- Failed, invalid, inconclusive, stale, and superseded scientific attempts
  retain their own immutable evidence identity; they are not overwritten by a
  later version.
- Post-evaluation architecture or protocol changes do not become a patch to
  Experiment Three. They require separately approved Experiment 3B scope.
