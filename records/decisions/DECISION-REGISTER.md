# Decision Register

This register records scientific and project decisions separately from their
supporting evidence. Decisions remain reviewable; changing a frozen decision
requires the applicable human gate and a new decision record rather than an
overwrite.

## Active decisions

### E3-DEC-0001 - Separate lifecycle completion from comparative outcome

- **Date:** 2026-08-23
- **State:** Active
- **Decision:** Track `lifecycle_status` independently from
  `comparative_status`. A verified lifecycle may complete with comparative
  `FAIL`, `INCONCLUSIVE`, or `INVALID`.
- **Reason:** The experiment's required neural demonstration is the complete,
  replayable process. Favorable performance cannot be guaranteed and is not a
  valid release condition.

### E3-DEC-0002 - Use a 137-parameter pointwise neural detector

- **Date:** 2026-08-23
- **State:** Active and owner-approved; executable protocol freeze pending
- **Decision:** Use biased `1x1` convolutions `6 -> 8 -> 8 -> 1`, with ReLU
  after the first two layers, for exactly 137 trainable parameters.
- **Reason:** This is a real fully convolutional neural model sized to extremely
  limited independent supervision. It avoids adding unjustified spatial
  capacity merely to make the demonstration look more complex.
- **Gate:** A model-family or parameter-count change requires owner approval.
  Approved training and evaluation values must be hash-bound with the remaining
  implementation details before use.

### E3-DEC-0003 - Treat Experiment 1 as retrospective compatibility evidence

- **Date:** 2026-08-23
- **State:** Active
- **Decision:** Bind the exact Experiment 1 benchmark and controls, but describe
  the evaluation as retrospective because its test role and results are known.
- **Reason:** Reusing exposed evidence cannot create fresh held-out
  confirmation.
- **Claim limit:** No independent-accuracy, dense-segmentation,
  generalization, significance, superiority, or operational claim.

### E3-DEC-0004 - Keep prior BurnLens repositories read-only

- **Date:** 2026-08-23
- **State:** Active
- **Decision:** Treat `burnlens-deschutes` and `burnlens-experiment-two` as
  read-only provenance sources. Do not rewrite their decisions or import
  unverified work.
- **Reason:** Experiment Three requires isolated custody and must preserve prior
  failed and accepted evidence exactly as history.

### E3-DEC-0005 - Keep all project state outside OneDrive

- **Date:** 2026-08-23
- **State:** Active
- **Decision:** Keep the canonical checkout, custody roots, caches,
  environments, temporary files, and run outputs under `C:\Projects\Active`.
  Do not use OneDrive.
- **Reason:** A single explicit custody boundary improves reproducibility and
  avoids synchronization interference.

### E3-DEC-0006 - Keep fresh confirmation separate and deferred

- **Date:** 2026-08-23
- **State:** Active
- **Decision:** A new independently reviewed event cohort is not required for
  Experiment Three and cannot rescue or extend its retrospective result.
- **Gate:** Cohort creation, labeling, or opening requires separate owner
  approval and a frozen prospective protocol.

### E3-DEC-0007 - Preserve all declared runs and terminal outcomes

- **Date:** 2026-08-23
- **State:** Active
- **Decision:** Retain valid, failed, interrupted, rejected, inconclusive,
  invalid, stale, and superseded attempts. Report every predeclared seed; never
  silently replace or best-seed-select.
- **Reason:** Failure retention is necessary to make the neural demonstration
  and comparison auditable.

### E3-DEC-0008 - Separate software licensing from asset rights

- **Date:** 2026-08-23
- **State:** Active
- **Decision:** License repository-authored software and documentation under
  MIT, while requiring separate source, terms, attribution, redistribution,
  custody, and integrity decisions for data, model artifacts, and third-party
  materials.
- **Reason:** A repository software license cannot relicense external assets.

### E3-DEC-0009 - Bind the approved bounded neural protocol

- **Date:** 2026-08-23
- **State:** Active and owner-approved; executable protocol artifact pending
- **Decision:** Use event-class-balanced masked BCE; deterministic float32
  local CPU PyTorch; Adam with learning rate `0.001`; batch size `4`; maximum
  `200` epochs with patience `25`; seeds `20260725`, `20260726`, and `20260727`
  with the first primary; and no augmentation, positive-class weighting,
  BatchNorm, dropout, ensemble, pretraining, or search. Select the minimum
  validation balanced-BCE checkpoint. Select one threshold from validation
  only using a prospectively sealed worst-event-Dice/macro-IoU rule.
- **Comparative rule:** `PASS` requires every seed to be nonconstant on each
  test event and the three-seed median to beat the strongest constant control
  on macro IoU and worst-event Dice. Otherwise assign `FAIL`, `INCONCLUSIVE`,
  or `INVALID` under the sealed rules; never tune from the test.
- **Gate:** Milestone 3 must hash-bind exact input order, normalization,
  initialization, deterministic settings, tie-breaks, metric/collapse
  implementations, tolerances, artifact schemas, and exception/terminal rules
  before substantive training. It may not replace the approved values above.

### E3-DEC-0010 - Separate byte identity from permission and admission

- **Date:** 2026-08-23
- **State:** Active
- **Decision:** Accept the exact Experiment One inventory as a metadata
  identity `PASS` while keeping controlled copy and scientific use `DEFER` and
  repository/raw-provider redistribution `BLOCK`.
- **Reason:** Matching hashes establish which bytes exist and whether they
  drifted. They do not establish ownership, license, current upstream terms,
  attribution sufficiency, or permission to copy, use, or redistribute.
- **Gate:** Require an explicit owner/rightsholder yes/no response for the
  exact project-authored derivative artifacts, followed by a separate current
  upstream-source gate and readiness audit before any admission. Ambiguity or
  silence is not permission.

### E3-DEC-0011 - Admit the exact retrospective benchmark to external custody

- **Date:** 2026-08-24
- **State:** Active and accepted at Milestone 1 checkpoint
- **Decision:** Accept the locked owner/rightsholder `yes`, current six-source
  `READY` gate, and dataset-readiness `PASS` for the bounded controlled-intake
  role. Admit exactly 131 approved artifacts / 3,369,748 bytes without
  replacement to external Experiment Three custody.
- **Limits:** Commit no benchmark byte or raw review response to Git. Exclude
  native provider bytes, restricted Tepee BARC4/BARC256 material, unsafe or
  nonselected checkpoints, and current U-Net source that is not the historical
  reference. This decision creates no training, evaluation, redistribution, or
  scientific-claim authority.

### E3-DEC-0012 - Exact runtime candidate 001 adoption

- **Date prepared:** 2026-08-24
- **State:** `APPROVED: yes`; one exact attested decision locked and reconciled
- **Decision:** Adopt candidate
  `CPYTHON-3.12.10-UV-0.10.7-TORCH-2.13.0-CPU-WINDOWS-X64-001`, bound to
  runtime inventory SHA-256
  `68f34338b61da111e0fc20a9a2a02cca7e02ff97262fd5f9d0185d351fc69f05`.
- **Boundary:** The `yes` authorized only exact Active-only download,
  verification, isolated installation, license capture, and CPU/synthetic
  compatibility checks; no benchmark or substantive scientific work.
- **Outcome:** Activation `FAIL`. The installer entered same-version maintenance
  mode on existing Python and did not create the requested isolated runtime.
  Recovery passed for inspected existing-install surfaces. The candidate is
  closed on this host; approval is preserved and cannot be reassigned.

## Decisions still pending evidence or binding

### E3-DEC-PENDING-0013 - Exact runtime successor adoption

- **Date prepared:** 2026-08-24
- **State:** `PENDING`; zero human decisions recorded
- **Question:** Approve or reject candidate
  `CPYTHON-3.12.10-EMBED-UV-0.10.7-TORCH-2.13.0-CPU-WINDOWS-X64-002`, bound to
  runtime inventory SHA-256
  `ae95bc3982766e996c0ec6cb15d4964738f1958f48b1eabe73d2e2d27b3e3967`.
- **Boundary:** A `yes` would authorize only exact Active-only application-local
  extraction, vendoring of the unchanged locked wheels, license capture, and
  CPU/native-package/synthetic compatibility checks. A `no` rejects it.
- **Non-inference rule:** Candidate 001's `yes`, successful recovery, the
  unchanged wheel lock, silence, or general chat cannot substitute for this
  exact response.

Exact implementation bindings, the executable protocol artifact, and every
scientific outcome remain pending their gated milestones. Their absence does
not reopen the approved model or training choices for routine optimization.
