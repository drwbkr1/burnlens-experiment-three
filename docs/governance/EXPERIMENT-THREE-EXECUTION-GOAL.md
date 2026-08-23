# BurnLens Experiment Three Execution Goal

- **Goal service ID:** `01a03021-0d66-7553-bcab-26971ec191e6`
- **Status:** Active
- **Owner approval:** 2026-08-23
- **Canonical remote:** `https://github.com/drwbkr1/burnlens-experiment-three`
- **Canonical checkout:** `C:\Projects\Active\burnlens-experiment-three`
- **Initial active issue:** `#1`, Milestone 0: truthful empty-repository bootstrap
- **Authority record:** `records/governance/EXPERIMENT-THREE-AUTHORITY-2026-001.md`

## Objective

Bootstrap, build, evaluate, publish, and truthfully close BurnLens Experiment Three as a deliberately bounded neural-network experiment.

The primary scientific question is:

> Can a deliberately data-sized neural change detector avoid Experiment One's constant-class U-Net collapse on the frozen Deschutes retrospective compatibility benchmark while completing an exact, replayable model lifecycle?

Completion requires a real neural-network lifecycle: implementation, synthetic preflight, substantive training, prospective checkpoint selection, safe reconstruction, fresh-process reload, inference, evaluation, packaging, and exact replay. The experiment does not need to beat the RBR baseline to complete.

Codex serves as Experiment Three's technical, scientific, evaluation, release, and reliability director within this charter. It resumes from the latest verified checkpoint, selects the next bounded dependency-ready evidence unit, maintains current truth and history, and continues through terminal closeout without routine approval while the work stays inside the active authority and no hard stop is open.

## Portfolio promise

Experiment Three is a portfolio-first, inspectable research case study for people evaluating applied machine-learning judgment. Its promise is not that a neural network will win. Its promise is that a small remote-sensing neural model will be designed in proportion to its evidence, trained and evaluated without test-driven rescue, compared with honest controls, replayed exactly, and reported truthfully even when the result is negative.

The strongest intended public experience is a reviewer being able to answer, from preserved evidence:

- what the network saw;
- why the architecture was sized this way;
- whether gradients and learning actually occurred;
- how every predeclared seed behaved;
- how checkpoint and threshold choices were made without the test;
- where predictions were right, wrong, or degenerate;
- how the network compared with RBR, the canonical U-Net, and constant controls;
- which pixels were actually labeled and scored;
- what the evidence does and does not support; and
- whether the released package replays exactly.

This is not operational wildfire guidance, an emergency-response product, a production burn-severity service, or independent proof of real-world mapping accuracy.

## Verified bootstrap state

The verified entry state is the unaccepted checkpoint candidate `EMPTY-UNBORN-BOOTSTRAP-CANDIDATE-2026-08-23`:

- the public GitHub repository exists and is empty;
- local `main` is unborn and has no Git objects;
- no branch, tag, release, PR, workflow, deployment, model, dataset, validator, roadmap, status record, authority record, or rendered surface existed before Milestone 0;
- GitHub issue `#1` records the truthful bootstrap objective and one direct-`main` exception; and
- missing surfaces are `missing`, not passed.

The first commit is therefore both a technical bootstrap and a public-claims event. It may not contain benchmark bytes, model code, training, inference, evaluation, unsupported scientific claims, secrets, credentials, or operational wildfire claims.

## Canonical location and custody boundary

- Keep the canonical checkout at `C:\Projects\Active\burnlens-experiment-three`.
- Keep all work, controlled custody, caches, temporary files, and run outputs beneath `C:\Projects\Active`.
- Never use `C:\Users\drewb\OneDrive` as a project, custody, cache, temporary, or run-output root.
- Do not route work into a forbidden root through a link, mount, environment variable, or tool configuration.
- Treat prior BurnLens repositories as read-only provenance sources unless the owner explicitly expands their write scope.
- Do not silently import prior repositories' environments, dependencies, code, data, checkpoints, outputs, authority, or unresolved worktree state.

## Inherited evidence, not inherited authority

### Experiment One: comparison benchmark

Experiment One is the scientific compatibility source. The inspected canonical checkpoint was clean `main` at commit `a741111d82e69689022d2058118ed8f4b9bf3546`.

The relevant inherited facts are:

- twelve `64 x 64` patches from six fire events;
- six pre/post Sentinel-2 channels: pre B04, B8A, B12 and post B04, B8A, B12;
- whole-event train, validation, and test roles containing two events each;
- 109 accepted training core pixels, 89 validation core pixels, and 89 test core pixels;
- a validation-selected RBR threshold whose event-class macro Dice, event-class macro IoU, and worst-event Dice were all `1.0` on the known test cores; and
- a 117,473-parameter canonical bounded U-Net that predicted all 89 test cores as burned and exactly matched the constant-burned control on the recorded primary metrics.

The authoritative Experiment One artifacts to bind in Milestone 1 include:

- `samples/datasets/burnlens-dataset-v0.1.0/DATASET-MANIFEST.json`;
- `records/phase-two/manifests/WHOLE-EVENT-SPLIT-2026-001.json`;
- `samples/baselines/burnlens-baseline-v0.1.0/BASELINE-EVALUATION-2026-001.json`; and
- `samples/evaluation/phase-three/bounded-unet-test-v0.1.0/BOUNDED-UNET-TEST-EVALUATION-2026-001.json`.

These facts establish a retrospective compatibility benchmark, not independent ground truth, dense segmentation evidence, statistical significance, or geographic generalization. The candidate labels and sparse core masks were owner-approved prototype evidence and may favor spectral separability. The effective independent sample is the number of events, not the pixel count.

### Experiment Two and Two-B: engineering lessons

Experiment Two and Two-B are engineering-provenance sources only.

- Experiment Two's frozen Prithvi EO 1.0 path ended `INVALID` for executability/reproducibility and produced no project predictions or scientific metrics.
- Experiment Two-B demonstrated restrictive checkpoint mapping, exact tensor accounting, bitwise synthetic equivalence, deterministic validation-runtime techniques, content-addressed custody, and retained failure evidence.
- It did not complete project inference, training, or scientific evaluation.
- Its HLS routes failed or remained inconclusive, and its local worktree contains extensive uncommitted and untracked state.

Do not import that worktree wholesale or reinterpret its engineering validation as Experiment Three model evidence. A later milestone may reuse a specific pattern or artifact only after separate inspection, identity binding, license/terms review, and admission under the active contract.

## Source precedence

For this experiment:

1. the owner's current approved direction controls scope and taste;
2. this execution goal, the authority record, the active milestone contract, and repository instructions control work;
3. hash-bound canonical Experiment One artifacts control benchmark identity and historical comparison values;
4. official Copernicus/Sentinel documentation and source metadata control external source meaning and attribution;
5. current project records control Experiment Three state; and
6. historical prompts, logs, and outputs provide provenance but not authority.

Conflicts, missing provenance, or terms ambiguity fail closed. A plausible file, count, webpage, model output, or prior statement is not sufficient evidence by itself.

## Approved neural model

The primary model is the 137-parameter pointwise fully convolutional neural change detector:

```text
input: 6 pre/post spectral channels per pixel
Conv2d(6, 8, kernel_size=1, bias=true)
ReLU
Conv2d(8, 8, kernel_size=1, bias=true)
ReLU
Conv2d(8, 1, kernel_size=1, bias=true)
output: one logit per pixel
```

Parameter count:

- first layer: `(6 * 8) + 8 = 56`;
- second layer: `(8 * 8) + 8 = 72`;
- output layer: `(8 * 1) + 1 = 9`; and
- total: `137` trainable parameters.

This is a genuine neural segmentation model: it learns nonlinear relationships among paired pre/post spectral inputs and produces a spatially aligned dense logit surface for arbitrary compatible image dimensions. It deliberately does not use spatial context. That constraint is a scientific control against giving a much larger spatial model 117,473 parameters for only 109 supervised training-core pixels and four training patches.

The architecture, model family, and following protocol values are already approved and fixed in direction:

- event-class-balanced masked binary cross-entropy;
- deterministic float32 local CPU PyTorch execution;
- Adam with learning rate `0.001`;
- batch size `4`;
- maximum `200` epochs;
- early-stopping patience `25`;
- exact seeds `20260725`, `20260726`, and `20260727`, all reported with no best-seed selection and `20260725` prospectively designated primary;
- minimum validation event-class-balanced masked-BCE checkpoint selection;
- one global validation-only threshold procedure using a prospectively sealed worst-event-Dice/macro-IoU rule;
- explicit all-background and all-burned collapse gates; and
- no augmentation, positive-class weighting, BatchNorm, dropout, ensemble, pretraining, architecture search, hyperparameter search, or post-test rescue.

The approved comparative `PASS` rule requires every seed to be nonconstant on each test event and the three-seed median to beat the strongest constant control on macro IoU and worst-event Dice. Otherwise the frozen rules must assign `FAIL`, `INCONCLUSIVE`, or `INVALID`; they may never tune from the test.

Milestone 3 must encode, validate, hash-bind, and seal those approved values together with the remaining implementation details before substantive training: input order; normalization; mask behavior; initialization; exact deterministic-runtime flags and dependency identities; checkpoint tie handling; threshold candidates and tie handling; metric implementation; numerical collapse definitions; replay tolerances; artifact schemas; and exception/terminal rules. Milestone 3 may clarify an implementation detail only when it does not choose a different scientific route. It is not authorized to select alternative values from training, validation, synthetic, or test outcomes. Changing an approved value or the model family requires an owner gate; changing either after evaluation creates a separately approved Experiment 3B.

## Two independent outcome dimensions

Never collapse engineering completion and scientific comparison into one status.

### `lifecycle_status`

This records whether the required model lifecycle was validly completed. A lifecycle `PASS` requires, at minimum:

- exact source, environment, configuration, and input identities;
- successful forward and backward passes;
- finite losses and gradients;
- nonzero gradients and a verified optimizer update;
- different initial and final parameter hashes;
- complete training and validation histories for every seed;
- prospective checkpoint selection under the frozen rule;
- safe checkpoint reconstruction and fresh-process reload;
- identical or prospectively bounded replay logits;
- inference and evaluation under the frozen procedure;
- packaged machine-readable and reviewer-facing evidence; and
- an exact replay that verifies the released result.

### `comparative_status`

This records the scientific result as `PASS`, `FAIL`, `INCONCLUSIVE`, or `INVALID` under prospectively frozen decision rules.

- `PASS` must mean only what the frozen rule says and cannot imply independent accuracy or operational superiority.
- `FAIL` is a valid result and may accompany lifecycle `PASS`.
- `INCONCLUSIVE` preserves evidence that cannot answer the bounded question.
- `INVALID` identifies a protocol, execution, identity, or evidence defect that prevents the planned comparison.

The experiment completes when its terminal contract is satisfied, not when a desired metric is achieved.

## Claim envelope

### Allowed after evidence exists

The project may accurately report:

- that a 137-parameter pointwise fully convolutional neural model was implemented;
- whether its synthetic preflight, training, reload, inference, evaluation, packaging, and replay gates passed;
- how every predeclared seed performed on the exact frozen retrospective core benchmark;
- how those results compare descriptively with the recorded RBR, canonical U-Net, constant-background, and constant-burned controls under disclosed threshold rules;
- where predictions were degenerate, uncertain, false positive, or false negative on the labeled cores;
- that full-patch predictions outside labeled cores are qualitative and unscored; and
- the exact limitations arising from sparse prototype labels, two events per split, known test exposure, source construction, and absent fresh confirmation.

### Prohibited without separately admitted evidence

Do not claim or imply:

- independent real-world burn-scar accuracy;
- dense segmentation validity from sparse core masks;
- statistical significance or population inference from two test events;
- geographic, temporal, sensor, fire-type, or operational generalization;
- that a neural model is superior merely because it trained or avoided a constant-class prediction;
- that Experiment Three beat the perfect RBR score if the frozen metric gives no room to improve;
- causal architectural improvement unless a genuinely controlled reproduction supports it;
- calibrated probabilities unless prospectively validated;
- production readiness, emergency utility, or suitability for wildfire decisions; or
- fresh confirmatory performance before a separately approved sealed cohort exists and is opened once.

## Comparison set and reporting

Every predeclared neural seed must be shown individually. The comparison set is:

1. RBR with its historically validation-selected threshold and disclosed selection method;
2. the canonical Experiment One U-Net artifact and its recorded fixed-threshold result;
3. constant-background;
4. constant-burned; and
5. each Experiment Three neural seed under the single frozen validation-only selection and threshold procedure.

Use the exact Experiment One primary definitions for apples-to-apples reporting, including event-class macro Dice, event-class macro IoU, and worst-event Dice. Additional descriptive metrics may be included only if they are prospectively defined and cannot replace the primary comparison.

Retain, per seed and event:

- checkpoint identity and selection evidence;
- threshold identity and selection evidence;
- confusion counts;
- per-class and macro Dice/IoU where defined;
- worst-event result;
- predicted-burn prevalence;
- probability summaries and distributions;
- explicit all-background/all-burned degeneracy checks;
- probability, class, and error artifacts; and
- runtime, duration, and bounded resource observations.

Three seeds measure optimization variation. They do not create three independent datasets or justify inferential statistics.

## Fresh confirmation lane

Fresh-event confirmation is not required for Experiment Three completion and is not authorized by this goal alone.

If the owner later authorizes it, it must be a separate lane with its own contract and authority. At minimum it must use:

- new events selected without inspecting Experiment Three outputs;
- independently constructed labels and review evidence;
- challenging negatives such as bare soil, water, cloud or shadow, snow, bright surfaces, and non-fire change where scientifically appropriate;
- no RBR- or model-assisted admission of labels;
- explicit unknown/ambiguous regions rather than forced labels;
- event/scene/geography/time/lineage-aware separation;
- a sealed manifest and one frozen opening; and
- the same frozen systems rerun on the same new holdout.

Fresh data may not be used to rescue, tune, or silently continue Experiment Three.

## Milestone plan

### Milestone 0: truthful public bootstrap

**Objective:** Establish the complete operating control plane and honest public repository surface from the verified empty state.

Required outcomes:

- repository instructions, this unabridged goal, authority record, project control profile, checkpoint policy, and Milestone 0 contract;
- roadmap, status, changelog, version history, evidence ledger, decision register, README, software license and terms boundary, contribution workflow, prompt log, and human-readable devlog;
- repository validator, focused control tests, CI, and skill-schema validation;
- a complete diff free of benchmark bytes, model code, scientific outputs, credentials, secrets, and unsupported claims;
- one locally validated initial commit directly on unborn `main` under issue `#1`;
- a verified push to live `main`; and
- closure of issue `#1` only after live verification, with the next issue-backed milestone opened from the exact public checkpoint.

No dataset intake, dependency installation, model code, training, inference, or evaluation belongs in this milestone.

### Milestone 1: benchmark provenance, rights, and controlled intake

**Objective:** Establish whether the exact Experiment One benchmark and comparison artifacts may be used and redistributed here, then admit only verified artifacts into controlled Experiment Three custody.

Required outcomes:

- hash-bound identities for dataset manifest, all arrays, split, masks, normalization, metrics, RBR result, canonical U-Net configuration/checkpoint/predictions, constant controls, and rendered reference evidence;
- source, license, terms, attribution, and redistribution review for every admitted byte;
- schema, shape, dtype, finite-value, mask, class, event, and split-integrity checks;
- leakage and retrospective-test-exposure declarations;
- a controlled intake manifest separating immutable raw source, admitted benchmark, derived evidence, and rejected artifacts;
- explicit PASS/FAIL/DEFER/BLOCK decisions for the compatibility and fresh-confirmation claim lanes; and
- no modification to prior repositories.

Stop on rights ambiguity, identity mismatch, unexpected source changes, missing artifacts, or a required new terms acceptance.

### Milestone 2: synthetic vertical slice

**Objective:** Prove the complete implementation and artifact path without touching substantive benchmark training or test evaluation.

Required outcomes:

- exact 137-parameter architecture and parameter-accounting tests;
- deterministic finite forward and backward passes;
- nonzero gradients and verified optimizer movement;
- loss decrease on a known synthetic rule;
- initial/final weight hash difference;
- safe checkpoint package without opaque executable payloads;
- fresh-process reconstruction and identical logits;
- metric and collapse-gate truth tables;
- geospatial transform/write/reopen/inspect proof on synthetic fixtures;
- rendered probability, class, mask, and error surfaces with unlabeled pixels visually distinct; and
- discarded preflight weights, clearly barred from substantive use.

This milestone may establish an approved pinned runtime only under its dependency and terms gates. Synthetic success is engineering evidence, not benchmark model evidence.

### Milestone 3: prospective protocol freeze

**Objective:** Freeze one complete, executable scientific route before substantive training or evaluation.

Required outcomes:

- one executable protocol that preserves and hash-binds the already approved event-class-balanced masked BCE, deterministic float32 local CPU PyTorch execution, Adam learning rate `0.001`, batch size `4`, maximum `200` epochs, patience `25`, and seeds `20260725`/`20260726`/`20260727` with the first primary;
- exact input order, normalization, mask behavior, initialization, dependency identities, determinism flags, minimum-validation-balanced-BCE checkpoint tie rule, validation-only worst-event-Dice/macro-IoU threshold candidates and tie rule, metrics, numerical collapse definitions, comparison rules, replay tolerances, output schemas, and exception/terminal rules;
- the approved comparative `PASS` rule requiring every seed to be nonconstant on each test event and the three-seed median to beat the strongest constant control on macro IoU and worst-event Dice;
- dependency lock and environment identity;
- explicit prohibition of best-seed selection, test-driven adjustment, architecture or hyperparameter search, augmentation, positive-class weighting, BatchNorm, dropout, ensemble, pretraining, and post-test rescue;
- one immutable protocol hash referenced by every run; and
- an evaluation-opening control that cannot pass until all three sealed training packages and controls are complete.

Milestone 3 seals implementation, not model-shops. It may use synthetic checks to prove that the fixed route is executable, but it may not use training, validation, or test outcomes to select alternative scientific values. A post-freeze change requires the owner's protocol-change gate before training; a post-evaluation change belongs to Experiment 3B.

### Milestone 4: substantive neural lifecycle

**Objective:** Execute the frozen three-seed training and checkpoint lifecycle without opening the retrospective test evaluation.

Required outcomes for every seed:

- immutable configuration, code, input, environment, and protocol identities;
- complete train/validation histories;
- finite losses, gradients, parameters, and outputs;
- nonzero gradients and optimizer movement;
- selected checkpoint under the frozen rule;
- safe reconstruction from explicit architecture/configuration plus weights;
- fresh-process reload and exact replay proof;
- validation-only threshold selection under the single frozen procedure;
- retained failed or degenerate seeds with no replacement; and
- sealed run manifests sufficient for one controlled evaluation.

If a seed fails, preserve it and apply the frozen decision rule. Do not create a fourth seed or tune the protocol to force three successful runs.

### Milestone 5: one retrospective compatibility evaluation

**Objective:** Open and evaluate the known Experiment One test once under the frozen Experiment Three protocol.

Required outcomes:

- one recorded opening event after all entry gates pass;
- inference for every frozen seed without mutation;
- comparison with RBR, canonical U-Net, constant-background, and constant-burned controls;
- exact per-seed and per-event metrics, confusion counts, thresholds, probability summaries, predicted prevalence, collapse results, and timings;
- actual probability, classification, and error artifacts for all four test patches;
- clear separation of labeled, unlabeled, background, and predicted classes;
- a protocol-derived `comparative_status` that is separate from `lifecycle_status`;
- no tuning, rerun substitution, threshold rescue, model replacement, or fresh-data extension; and
- a retained terminal evaluation package with immutable identities.

The known test makes this retrospective. It cannot become confirmatory through careful execution alone.

### Milestone 6: reviewer-facing evidence, release, and closeout

**Objective:** Package, replay, render, publish, verify, and terminally close the experiment without changing its result.

Required outcomes:

- architecture explanation and verified parameter count;
- training/validation curves for all seeds;
- comparison tables that disclose differing threshold-selection methods;
- input/reference/RBR/U-Net/new-model panels for every test patch;
- probability, class, and error maps with qualitative regions labeled as such;
- model card, data/benchmark card, limitations, reproducibility instructions, machine-readable evidence manifest, and public experiment narrative;
- exact clean-environment replay from released inputs and package;
- version, changelog, status, roadmap, ledgers, decisions, prompt log, and devlog reconciled to terminal truth;
- one GitHub release created only after release audit gates pass;
- direct verification of live branch, tag, release assets, README claims, and rendered/public surfaces; and
- terminal closeout that names lifecycle status, comparative status, retained failures, limitations, and any separately deferred future work.

Do not prolong Experiment Three to improve a disappointing result. Future architecture or protocol work becomes Experiment 3B.

## Cycle direction

Every cycle begins with live reconciliation of:

- repository root, branch, HEAD, worktree, remote, issue, and PR;
- active authority, contract, entry gates, and stop conditions;
- custody roots and forbidden-root checks;
- environment, dependencies, data, models, runs, and scientific outputs actually present;
- current status, roadmap, ledger, decision, changelog, version, and devlog claims; and
- relevant real surfaces, including GitHub, runtime, model, evaluation, rendered evidence, and release state.

Then execute one bounded highest-leverage evidence unit. Prefer depth, correctness, replayability, and reviewer-visible clarity over parallel systems, extra models, more datasets, or checklist growth.

For each unit, retain:

- stable unit and run IDs;
- dependency IDs;
- exact input and output identities;
- allowed and actual writes;
- gates and actual results;
- execution status and evidence disposition;
- failures, exclusions, deferrals, and supersessions;
- expected and observed exit-condition delta;
- decision value; and
- next dependency or terminal handoff.

After two consecutive terminal units with no exit-condition progress, run an objective path-efficiency review. It may consolidate diagnostics, choose an already authorized fallback, or close a dead path. It may not change the research thesis, claim envelope, protocol, or authority.

## Real-surface validation

Validation must reach the surface whose truth changed:

- documentation and policy: complete diff, link/reference checks, authority, boundaries, and internal consistency;
- repository controls: real validator and test invocations;
- runtime: pinned dependency identity plus a real process invocation;
- data: byte identity, deterministic checks, schema/quality gates, and actual array inspection;
- neural model: gradients, weight movement, histories, reconstruction, inference, and replay;
- evaluation: actual predictions, probabilities, controls, masks, per-event/per-seed metrics, and decision rules;
- geospatial output: write, reopen, metadata verification, and visual inspection;
- rendered evidence: inspect actual figures at useful resolution, not only plotting code;
- GitHub/public state: direct live read of commits, branches, PRs, checks, tags, releases, assets, and rendered README; and
- release: clean replay plus live-publication verification.

A passing test, rendered image, local tag, successful push command, or heartbeat is only scoped evidence. It is not proof of an uninspected real surface.

## Records Codex maintains

Codex is responsible for keeping these mutually consistent:

- repository instructions;
- this execution goal;
- authority record and project control profile;
- active milestone contract and issue;
- roadmap and current status;
- README, model card, data/benchmark card, and limitations;
- evidence ledger and decision register;
- changelog, semantic project version, and version history;
- human-readable devlog/experiment log;
- prompt-build log;
- validation and release receipts; and
- GitHub issues, PRs, tags, and releases that the active authority permits.

Current-state records must tell a fresh operator what is true now. Append-only history must preserve what was tried and how it ended. Do not silently edit a past failure into a later success.

## Standing authority

Within this goal and an active dependency-valid milestone contract, Codex may without routine approval:

- perform read-only repository, provenance, runtime, artifact, and external-state inspection;
- create and maintain repository documentation, governance, evidence, decision, status, roadmap, version, and history records;
- create repository validators, tests, CI, model and evaluation code, renderers, packaging, and replay tooling;
- execute deterministic validation, synthetic preflight, frozen training, checkpointing, inference, retrospective evaluation, rendering, packaging, and replay after their entry gates pass;
- create and manage issues and `codex/*` branches;
- commit, push, open and update PRs, merge verified PRs, create versions and tags, and publish verified GitHub releases;
- apply bounded reversible remediation inside the frozen route;
- verify each real surface directly; and
- select and continue to the next dependency-ready evidence unit through terminal closeout.

This authority does not waive protocol order, human gates, rights/terms gates, external-state verification, or stop conditions. The Milestone 0 direct-`main` exception applies once and only because no base commit exists. After it, all changes are issue-backed `codex/*` PR work.

## Mandatory owner gates

Stop and ask the owner before:

- changing the core research question, portfolio promise, target user, or claim envelope;
- changing the approved 137-parameter model family or any frozen protocol element;
- changing the cohort, labels, split, masks, normalization, metrics, controls, threshold method, checkpoint method, collapse gates, or terminal decision rules;
- initiating, selecting, labeling, admitting, unsealing, or opening a fresh confirmatory cohort;
- adopting a materially new external source, model, dependency runtime, or service;
- accepting terms, granting consent, or using credentials;
- spending money, adding a paid service, or adding a secret;
- changing access, ownership, visibility, or custody;
- modifying another BurnLens repository;
- deleting or irreversibly replacing material evidence or external state;
- taking any other irreversible action;
- publishing a claim outside this charter; or
- shipping a checkpoint whose real surface cannot be verified.

Also stop immediately for an explicit pause, secret/privacy exposure, rights ambiguity, unexpected remote or custody state, conflicting authority, ambiguous terminal evidence, or a required human decision. Objective validation failure is not automatically a human gate: retain it and follow a preauthorized remediation or terminal rule when one exists.

## Failure and recovery rules

- Preserve original failed outputs and receipts before remediation.
- Never overwrite immutable inputs, accepted checkpoints, released artifacts, or sealed evaluation packages.
- Distinguish an execution failure from a scientific `FAIL`, `INCONCLUSIVE`, or `INVALID` disposition.
- Use only recovery routes prospectively allowed by the active contract.
- Do not substitute a different seed, checkpoint, threshold, event, model, metric, or date after seeing an unfavorable result.
- If recovery would change the frozen route, stop and request the applicable gate or close Experiment Three and propose Experiment 3B.
- If evidence cannot support a claim, narrow the claim or report `unknown`; do not infer a pass.

## Terminal completion

The long-running goal is complete only when:

1. Milestones 0 through 6 are dispositioned under their contracts;
2. the required neural lifecycle has a terminal, evidence-backed status;
3. the retrospective comparison has a separate terminal status;
4. all predeclared seeds, controls, failures, limitations, and claim boundaries are retained;
5. the released package replays under the stated conditions;
6. the live GitHub release and public repository surfaces are directly verified;
7. current records and append-only history agree with live state; and
8. the next action is terminal closeout, not another attempt to improve the result.

A lifecycle `PASS` with comparative `FAIL` is successful completion of the experimental process. `INCONCLUSIVE` or `INVALID` may also be an honest terminal scientific outcome. No result authorizes operational wildfire use.
