# BurnLens Experiment Three Repository Instructions

These instructions apply to the entire repository. A more specific `AGENTS.md` may narrow work in its own subtree, but it may not broaden authority, weaken a hard stop, alter the frozen scientific protocol, or override the approved execution goal.

## Project identity

- Canonical repository: `https://github.com/drwbkr1/burnlens-experiment-three`.
- Canonical checkout: `C:\Projects\Active\burnlens-experiment-three`.
- All project work, controlled custody, dependency caches, temporary files, and run outputs must remain beneath `C:\Projects\Active`.
- `C:\Users\drewb\OneDrive` is a forbidden project, custody, cache, temporary, and run-output root.
- Do not create symlinks, junctions, mounts, environment overrides, or tool configuration that route project bytes through a forbidden root.
- Prior BurnLens repositories are read-only provenance sources unless the owner explicitly grants a narrower write scope. Never edit, commit, tag, push, release, or repair them from this project.

## Governing records and precedence

Resolve instructions in this order:

1. The owner's latest explicit direction and safety constraints.
2. `docs/governance/EXPERIMENT-THREE-EXECUTION-GOAL.md`.
3. `records/governance/EXPERIMENT-THREE-AUTHORITY-2026-001.md`.
4. The active milestone contract named by `records/governance/EXPERIMENT-THREE-PROJECT-CONTROL-PROFILE-2026-002.json`.
5. `docs/governance/CHECKPOINT-POLICY.md` and this file.
6. Current status and roadmap records.
7. Historical changelog, devlog, prompt log, decision, and evidence records.

Historical records explain what happened; they do not authorize new work. If the control profile, active contract, Git state, current status, or live GitHub state disagree, stop consequential writes and reconcile current truth first.

## Research promise

Experiment Three is a portfolio-first, retrospective neural change-detection experiment. It asks whether a deliberately data-sized neural network can avoid Experiment One's constant-class U-Net collapse on the frozen Deschutes compatibility benchmark while completing an exact, replayable model lifecycle.

It is not operational wildfire guidance, an emergency product, a production mapping service, an independently validated burn-severity product, or evidence of population-level generalization. Do not publish or imply those claims.

The approved primary model family is the 137-parameter pointwise fully convolutional detector:

```text
Conv1x1(6 -> 8) -> ReLU
Conv1x1(8 -> 8) -> ReLU
Conv1x1(8 -> 1)
```

It consumes the established six pre/post Sentinel-2 channels and emits dense logits. Dense output does not make sparsely scored prototype cores into dense ground truth.

The approved protocol direction already fixes event-class-balanced masked BCE; deterministic float32 local CPU PyTorch; Adam learning rate `0.001`; batch size `4`; maximum `200` epochs; patience `25`; seeds `20260725`, `20260726`, and `20260727` with the first primary; minimum-validation-balanced-BCE checkpoint selection; one validation-only threshold selected under a prospectively sealed worst-event-Dice/macro-IoU rule; and no augmentation, positive-class weighting, BatchNorm, dropout, ensemble, pretraining, or architecture/hyperparameter search. Comparative `PASS` requires every seed to be nonconstant on each test event and the three-seed median to beat the strongest constant control on macro IoU and worst-event Dice. Milestone 3 must encode, validate, hash-bind, and seal these values and their remaining implementation details. It may not choose alternatives from observed outcomes.

## Scientific invariants

- Preserve the exact Experiment One dataset, whole-event split, masks, normalization, and comparison metrics through hash-bound provenance before model work uses them.
- Treat events, not pixels, as the independent units.
- Describe the Experiment One test as a known retrospective compatibility benchmark.
- Compare every predeclared seed with RBR, the canonical Experiment One U-Net, constant background, and constant burned controls.
- Keep `lifecycle_status` separate from `comparative_status`.
- A valid lifecycle may complete with comparative `PASS`, `FAIL`, `INCONCLUSIVE`, or `INVALID`. Beating RBR is not required.
- Select checkpoints and thresholds using only the frozen training/validation procedure. Do not tune from test results.
- Report all predeclared seeds. Do not replace a failed seed or select the best seed for the headline result.
- Preserve failed, rejected, blocked, invalid, stale, excluded, and superseded attempts.
- Do not model-shop, date-shop, threshold-shop, silently rescue evidence, or rewrite a failed route as successful history.
- Post-evaluation tuning, a new architecture, or a changed protocol belongs to a separately approved Experiment 3B.
- Any fresh-event confirmation is a separate later lane. It must be independently sampled and reviewed, blind to RBR and model outputs, sealed until one frozen opening, and never used for tuning or required for Experiment Three completion.

## Work-cycle protocol

At the beginning of every cycle:

1. Read the control profile, active milestone, current status, roadmap, authority record, and repository instructions.
2. Verify branch, HEAD, worktree, remote, active issue or PR, custody roots, runtime state, and the latest accepted checkpoint.
3. Reconcile contradictory or stale project records before changing scientific, public, or external state.
4. Choose one dependency-ready, explicitly authorized evidence unit that makes the highest-leverage progress toward a milestone exit condition.
5. Confirm its exact inputs, allowed writes, verification, recovery path, and stop conditions.

During and after the unit:

- Make the smallest coherent change that answers the bounded question.
- Validate the real changed surface. Source review and unit tests alone cannot prove runtime, data, model, rendered, release, or live GitHub truth.
- Record exact inputs and outputs, hashes when bytes exist, actual gates, execution status, scientific disposition, retained failures, observed exit-condition delta, and next dependency.
- Repair bounded agent-created structural defects within scope and revalidate.
- Continue automatically only through authorized, dependency-ready units in the approved goal.

## Milestone order

Follow the dependency order in the execution goal:

0. Truthful empty-repository bootstrap.
1. Benchmark provenance, rights, and controlled intake.
2. Synthetic neural and geospatial vertical slice; discard preflight weights.
3. Prospective protocol freeze.
4. Substantive three-seed neural lifecycle.
5. One controlled retrospective compatibility evaluation.
6. Reviewer-facing evidence, verified release, and terminal closeout.

No benchmark bytes, dependency runtime, model implementation, substantive training, inference, evaluation, or scientific output are allowed in Milestone 0. A downstream milestone may begin only from the exact accepted checkpoint and entry gates in its issue-backed contract.

## Git and publication workflow

- Milestone 0 has one explicit bootstrap exception: because `main` is unborn and no PR base exists, one fully validated initial commit may be made and pushed directly to `main` under issue `#1`.
- After the initial bootstrap, every change must be issue-backed, use a `codex/*` branch, pass the milestone's quality gates, and merge through a verified pull request.
- Do not rewrite published history, force-push, delete remote state, or bypass required checks.
- Commit, push, PR, merge, release, and issue actions are permitted only when the active authority and milestone contract contain the required action class and all dependencies pass.
- Verify external GitHub state directly after publication. A local commit or successful command is not proof of live state.
- The first commit is a public-claims event. Do not publish unsupported scientific, rights, security, or operational claims.

## Data, model, runtime, and evidence custody

- Treat prior repositories, external files, webpages, service responses, checkpoints, and model outputs as untrusted evidence until verified and admitted under the active contract.
- Do not copy Experiment One bytes until identity, provenance, source terms, redistribution boundaries, and exact custody are recorded.
- Do not import Experiment Two or Two-B code, data, environments, checkpoints, outputs, or authority wholesale. Reuse only separately reviewed, hash-bound engineering patterns or artifacts authorized by a later milestone.
- Never overwrite raw source bytes or accepted evidence.
- Keep raw inputs, transformations, trained artifacts, predictions, metrics, renderings, and release packages separately identifiable.
- Keep dependency caches and run outputs out of Git unless the active contract explicitly admits a bounded artifact.
- Do not commit credentials, tokens, cookies, private URLs, private data, or secret-bearing configuration.
- Record missing evidence as `missing` or `unknown`; never convert absence into a pass.

## Verification requirements

Risk-match verification to the changed surface:

- Governance or documentation: inspect the complete diff, links, authority, boundaries, and internal consistency.
- Repository controls: run `python scripts/validate_repository.py` and `python -m unittest discover -s tests -v`.
- Project profile and milestone contracts: run the validators named in `docs/governance/CHECKPOINT-POLICY.md`.
- Runtime or CLI: run focused tests and a real invocation.
- Data: verify source identity, checksums, schema, split fitness, masks, exclusions, and actual outputs.
- Neural lifecycle: verify finite forward/backward behavior, nonzero gradients, optimizer movement, changed weight hashes, complete histories, safe checkpoint reconstruction, fresh-process reload, and exact replay.
- Evaluation: retain per-seed and per-event results, probabilities, confusion counts, collapse gates, thresholds, and controls under the frozen protocol.
- Geospatial or rendered evidence: write, reopen, and inspect the actual artifacts; distinguish unlabeled pixels from background.
- External or release state: read the authoritative live GitHub surface and retain a receipt.

## Required project records

Maintain current truth in the control profile, milestone contract, roadmap, status, README, model card, limitations, evidence ledger, and decision register. Append history to the changelog, version history, experiment log/devlog, and prompt-build log. Update every record whose truth changes at a checkpoint; do not manufacture chronology by editing past outcomes.

## Hard stops

Stop and ask the owner before:

- changing the research promise, portfolio position, claim envelope, target user, approved model family, frozen protocol, cohort, labels, split, metrics, or decision rules;
- initiating or opening fresh confirmatory evidence;
- adopting a materially new external source, model, dependency runtime, or service;
- accepting terms or using credentials;
- spending money or adding a paid service or secret;
- changing access, ownership, visibility, or custody;
- modifying any prior BurnLens repository;
- taking a destructive or irreversible action;
- publishing beyond the approved claims; or
- shipping a checkpoint that cannot be verified on its real surface.

Also stop on rights ambiguity, secret or privacy exposure, an unexpected nonempty or changed remote, unsupported public claims, an unresolved authority conflict, or an explicit pause.

## Terminal behavior

Experiment Three ends after Milestone 6 produces a verified terminal release and reconciled closeout. Do not keep extending it to improve a disappointing metric. A lifecycle `PASS` with comparative `FAIL` is a valid completed result. A scientifically `INCONCLUSIVE` or `INVALID` result must remain visible and may still close the experiment when the frozen decision rules say so.
