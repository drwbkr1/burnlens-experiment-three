# Version History

This record distinguishes working-tree candidates, verified checkpoints, and
published releases. A version string does not by itself prove a release.

| Version | Date | State | Revision | Scope | Scientific result |
| --- | --- | --- | --- | --- | --- |
| `0.0.0-bootstrap` | 2026-08-23 | Accepted checkpoint; not a release | `4543a2dad5c2630249906aab763ae0cbf91097ba` | Governance, documentation, repository controls, and CI bootstrap only | None |
| `0.1.0-m1-candidate` | 2026-08-24 | Working-tree candidate; not accepted or released | Pending candidate commit | Hash-bound rights, source gate, readiness, and external controlled intake | None |

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
- Next work: Milestone 1 under issue #2, limited at entry to read-only
  provenance and rights reconciliation with no benchmark bytes admitted.

## Unreleased Milestone 1 candidate

Draft pull request
[#3](https://github.com/drwbkr1/burnlens-experiment-three/pull/3) carries the
Milestone 1 control transition. Its published transition commit
`74171043ddd543979e9773d5ffdd06da116bbaa1` passed push CI run `32674532003`
and pull-request CI run `32674546780`. The subsequent metadata-only identity
inventory and controlled-intake records form a locally and independently
validated issue-backed branch candidate. The dataset is admitted to external
custody, but this is not an accepted public version, release, or scientific
result.

The owner-rightsholder decision is now an exact scoped `yes`, the current
source gate is `READY`, readiness is `PASS`, and controlled intake admitted 131
approved artifacts / 3,369,748 bytes to external custody with matching
identities. Repository redistribution remains unauthorized. This candidate
still requires integrated verification, successful PR checks, reviewed merge,
and direct live-main verification before it becomes accepted.

The inventory was published at branch commit
`b17176d07d34f34ab385acbc91cf1876471afe06`, with successful push run
`32676766091` and pull-request run `32676767882`. A hash-bound, blank
owner-rights response was prepared and remains immutable as the review
interface. The completed response is private; its public aggregate decision is
hash-bound. This remains an unmerged branch candidate, not an accepted
checkpoint or release.

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
