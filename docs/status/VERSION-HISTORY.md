# Version History

This record distinguishes working-tree candidates, verified checkpoints, and
published releases. A version string does not by itself prove a release.

| Version | Date | State | Revision | Scope | Scientific result |
| --- | --- | --- | --- | --- | --- |
| `0.0.0-bootstrap` | 2026-08-23 | Accepted checkpoint; not a release | `4543a2dad5c2630249906aab763ae0cbf91097ba` | Governance, documentation, repository controls, and CI bootstrap only | None |
| `0.1.0` | 2026-08-24 | Accepted checkpoint; not a release | `32e5b0dfbd93bdf337fa4f2e9bde29d0bc36a6a4` | Hash-bound rights, source gate, readiness, and external controlled intake | None |
| `0.2.0-m2-runtime-gate` | 2026-08-24 | Working-tree candidate; not accepted or released | Pending candidate commit | Synthetic-preflight controls and exact runtime owner gate | None |

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

## Unreleased Milestone 2 runtime-gate candidate

Issue [#4](https://github.com/drwbkr1/burnlens-experiment-three/issues/4)
tracks synthetic preflight from the exact accepted Milestone 1 base. The
working tree binds one CPython 3.12.10 / uv 0.10.7 / PyTorch 2.13.0+cpu
Windows x64 candidate and its 20-package lock. Its source gate passes for
owner review, but the immutable response remains blank. No runtime artifact has
been downloaded or installed and no synthetic or scientific execution has
begun. This candidate is not yet committed, reviewed, accepted, tagged, or
released.

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
