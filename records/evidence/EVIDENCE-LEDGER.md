# Evidence Ledger

This ledger distinguishes observations, admitted evidence, read-only reference
material, and missing surfaces. An entry is not a scientific pass merely
because it appears here.

## Status vocabulary

- `OBSERVED`: directly inspected state, not necessarily immutable evidence.
- `ADMITTED`: provenance, integrity, terms, and custody gates passed for the
  stated role.
- `REFERENCE_ONLY`: external or prior-project evidence not admitted as an
  Experiment Three artifact.
- `MISSING`: required or anticipated evidence does not exist.
- `DEFERRED`: intentionally outside the current required lane.
- `SUPERSEDED`: retained historical evidence replaced for a stated role but not
  deleted.

## Bootstrap entries

| Evidence ID | Status | Subject | Source or location | Bounded statement |
| --- | --- | --- | --- | --- |
| `E3-EVID-0001` | `OBSERVED` | Incoming public repository | `https://github.com/drwbkr1/burnlens-experiment-three` inspected 2026-08-23 | Repository existed with no commits, branches, tags, releases, code, data, or build surfaces at inspection time. |
| `E3-EVID-0002` | `OBSERVED` | Canonical local custody root | `C:\Projects\Active\burnlens-experiment-three` | Local checkout exists under the required non-OneDrive root. This does not admit external assets. |
| `E3-EVID-0003` | `OBSERVED` | Bootstrap tracker | `https://github.com/drwbkr1/burnlens-experiment-three/issues/1` | Open issue #1 tracks truthful Milestone 0 bootstrap work. |
| `E3-EVID-0004` | `REFERENCE_ONLY` | Experiment 1 benchmark and controls | `C:\Projects\Active\burnlens-deschutes` | Candidate source for exact dataset, split, RBR, U-Net, constant-control, and rendered-evidence bindings. No bytes are admitted here yet. |
| `E3-EVID-0005` | `REFERENCE_ONLY` | Experiment 2 and 2B history | `C:\Projects\Active\burnlens-experiment-two` | Candidate source for failure history and reusable engineering lessons. It supplies no Experiment Three scientific result and remains read-only. |
| `E3-EVID-0006` | `OBSERVED` | Local Milestone 0 validation | Canonical checkout, 2026-08-23T22:38:59Z | `python scripts/validate_repository.py` passed 25 required files; `python -m unittest discover -s tests -v` passed 9 tests; both project-control schema validators passed with zero warnings/findings; no scientific output was produced. This is local candidate evidence, not live-main or CI acceptance. |

## Missing and deferred surfaces

| Evidence ID | Status | Surface | Required disposition |
| --- | --- | --- | --- |
| `E3-EVID-0101` | `MISSING` | Benchmark admission manifest | Establish provenance, hashes, rights, attribution, custody, and role before use. |
| `E3-EVID-0102` | `MISSING` | Runtime and dependency lock | Create and verify before executable claims. |
| `E3-EVID-0103` | `MISSING` | Neural implementation and parameter audit | Implement and prove in synthetic preflight. |
| `E3-EVID-0104` | `MISSING` | Synthetic lifecycle report | Produce before protocol freeze and substantive training. |
| `E3-EVID-0105` | `MISSING` | Hash-bound executable protocol artifact | Approved values are recorded, but exact bindings and artifact identity are required before substantive training. |
| `E3-EVID-0106` | `MISSING` | Training histories and checkpoints | No Experiment Three training has occurred. |
| `E3-EVID-0107` | `MISSING` | Predictions, metrics, and decision | No Experiment Three evaluation has occurred. |
| `E3-EVID-0108` | `MISSING` | Geospatial and rendered evidence | No result exists to render. |
| `E3-EVID-0109` | `MISSING` | Exact replay and release verification | Required for terminal closeout. |
| `E3-EVID-0110` | `DEFERRED` | Fresh-event confirmation cohort | Separate owner-gated lane; not required for Experiment Three completion. |

## Admission rule

Future evidence entries must identify the producing command or human action,
input and output paths, SHA-256 hashes where applicable, environment identity,
validation result, claim role, and any exclusions or deviations. Failed and
invalid evidence receives an immutable entry rather than deletion or silent
replacement.
