# Version History

This record distinguishes working-tree candidates, verified checkpoints, and
published releases. A version string does not by itself prove a release.

| Version | Date | State | Revision | Scope | Scientific result |
| --- | --- | --- | --- | --- | --- |
| `0.0.0-bootstrap` | 2026-08-23 | Accepted checkpoint; not a release | `4543a2dad5c2630249906aab763ae0cbf91097ba` | Governance, documentation, repository controls, and CI bootstrap only | None |

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
inventory is a locally and independently validated issue-backed branch
candidate; it is not an accepted version, release, dataset admission, or
scientific result.

The inventory reports identity `PASS`, controlled copy/use `DEFER`, and
redistribution `BLOCK`. No version may advance on identity alone; an explicit
rights decision, current source gate, readiness result, and zero-copy or
admission receipt must close Milestone 1 first.

The inventory was published at branch commit
`b17176d07d34f34ab385acbc91cf1876471afe06`, with successful push run
`32676766091` and pull-request run `32676767882`. A hash-bound, blank
owner-rights response is now prepared. This is still an unmerged branch
candidate, not an accepted checkpoint or release.

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
