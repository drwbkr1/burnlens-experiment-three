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
| `E3-EVID-0003` | `OBSERVED` | Bootstrap tracker | `https://github.com/drwbkr1/burnlens-experiment-three/issues/1` | Issue #1 tracked truthful Milestone 0 bootstrap work. |
| `E3-EVID-0004` | `REFERENCE_ONLY` | Experiment 1 benchmark and controls | `C:\Projects\Active\burnlens-deschutes` | Candidate source for exact dataset, split, RBR, U-Net, constant-control, and rendered-evidence bindings. No bytes are admitted here yet. |
| `E3-EVID-0005` | `REFERENCE_ONLY` | Experiment 2 and 2B history | `C:\Projects\Active\burnlens-experiment-two` | Candidate source for failure history and reusable engineering lessons. It supplies no Experiment Three scientific result and remains read-only. |
| `E3-EVID-0006` | `OBSERVED` | Local Milestone 0 validation | Canonical checkout, 2026-08-23T22:38:59Z | `python scripts/validate_repository.py` passed 25 required files; `python -m unittest discover -s tests -v` passed 9 tests; both project-control schema validators passed with zero warnings/findings; no scientific output was produced. This is local candidate evidence, not live-main or CI acceptance. |
| `E3-EVID-0007` | `OBSERVED` | Accepted live Milestone 0 revision | Live `main` commit `4543a2dad5c2630249906aab763ae0cbf91097ba`, tree `6387e91f071609605f7fcc3a05842782423fbb6d` | The exact truthful bootstrap revision is present on live `main`; this is a checkpoint, not a release or scientific result. |
| `E3-EVID-0008` | `OBSERVED` | Public bootstrap validation | `https://github.com/drwbkr1/burnlens-experiment-three/actions/runs/32671370937` | GitHub Actions run `32671370937` completed successfully for the accepted bootstrap revision. |
| `E3-EVID-0009` | `OBSERVED` | Live blob identity | Live commit `4543a2dad5c2630249906aab763ae0cbf91097ba` and canonical checkout | The live README and execution-goal blobs matched their verified local counterparts. |
| `E3-EVID-0010` | `OBSERVED` | Public repository description | `https://github.com/drwbkr1/burnlens-experiment-three` | The public description was corrected to the bounded retrospective Experiment Three framing. |
| `E3-EVID-0011` | `OBSERVED` | Milestone 1 tracker and entry boundary | `https://github.com/drwbkr1/burnlens-experiment-three/issues/2` | Issue #2 is open for read-only benchmark-provenance and rights reconciliation. No benchmark byte has been admitted. |
| `E3-EVID-0012` | `OBSERVED` | Rendered public repository surface | Live GitHub repository page inspected in the in-app browser on 2026-08-23 | The rendered page showed public `main`, one commit at `4543a2d`, the expected repository file table and README, the bounded About description, two open issues, zero tags, and zero releases. This visual check complements the API, ref, blob, and CI receipts. |
| `E3-EVID-0013` | `OBSERVED` | Milestone 0 tracker closeout | `https://github.com/drwbkr1/burnlens-experiment-three/issues/1` | Issue #1 closed at `2026-08-23T22:55:18Z` only after live commit, CI, blob, public-description, and rendered-surface verification; issue #2 carries the exact next milestone. |
| `E3-EVID-0014` | `OBSERVED` | Milestone 1 control transition | Draft PR #3; branch commit `74171043ddd543979e9773d5ffdd06da116bbaa1` | Push run `32674532003` and pull-request run `32674546780` passed. The PR remains draft and unmerged. |
| `E3-EVID-0015` | `REFERENCE_ONLY` | Experiment One benchmark identity inventory | `records/provenance/EXPERIMENT-ONE-BENCHMARK-IDENTITY-INVENTORY-2026-001.json`, 90,576 bytes, SHA-256 `187c9d8aac67038e1269548d0477192ef6f3c6b8113190626c1aada2bed89529` | Clean source commit `a741111d82e69689022d2058118ed8f4b9bf3546`, tree `bc679254030eb57a65f58ac2af10880866fc52be`; all 48 dataset arrays and all eight U-Net prediction/probability arrays match their declared identities. Metadata identity is `PASS`; this is not admission. |
| `E3-EVID-0016` | `OBSERVED` | Milestone 1 no-copy boundary | Canonical Experiment Three checkout and identity inventory | Inventory recorded `bytes_copied: 0`; no candidate custody directory, dataset, model, training run, inference run, evaluation, or release exists. |
| `E3-EVID-0017` | `MISSING` | Owner/rightsholder artifact-rights decision | Milestone 1 human gate | Controlled copying and scientific use remain `DEFER`; redistribution remains `BLOCK`. A yes/no decision is required and cannot override third-party rights. |
| `E3-EVID-0018` | `OBSERVED` | Local Milestone 1 identity-candidate validation | Canonical checkout, `2026-08-24T00:18:15Z` | Repository validator PASS; 20/20 tests PASS; active profile and milestone schemas PASS; reconciliation aligned; historical Milestone 0 schemas PASS; JSON, relative links, Python compile, diff, and secret-pattern checks PASS. This is local candidate evidence, not merge or live acceptance. |

## Missing and deferred surfaces

| Evidence ID | Status | Surface | Required disposition |
| --- | --- | --- | --- |
| `E3-EVID-0101` | `MISSING` | Benchmark admission or zero-copy manifest | Establish rights, current upstream-source disposition, readiness, custody, and role before admission; otherwise record a terminal zero-copy outcome. |
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
