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
