# Experiment Three Checkpoint Policy

## Purpose

This policy turns the execution goal into bounded, inspectable checkpoints. A checkpoint changes accepted project truth only when its active issue-backed milestone contract reaches its exit conditions and every changed real surface is verified.

Schema validity, a passing test, a local commit, or a successful command is scoped evidence. None is sufficient by itself to declare a checkpoint accepted, public, released, or scientifically valid.

## Required checkpoint classes

| Class | Purpose | Normal publication behavior |
|---|---|---|
| Evidence unit | Answer one bounded, independently verifiable question inside a milestone | Accumulate in the active issue and contract; do not ship alone unless the contract identifies a risk exception |
| Milestone checkpoint | Produce one coherent change in accepted project truth | Issue-backed `codex/*` branch, verified PR, merge, and live-state verification |
| Risk exception | Contain a correctness, rights, security, custody, rollback, or stop risk for which waiting is materially worse | Narrow separately recorded change; never a shortcut for convenience |
| Terminal release | Package and verify the frozen Experiment Three result and close the goal | Audit candidate, tag, release, assets, replay, public surfaces, and terminal records |

Milestone 0 has one nonrepeatable exception: because `main` is unborn and there is no PR base, its fully validated bootstrap may create one initial commit directly on `main` under issue `#1`. After that commit, every change must be issue-backed, use `codex/*`, and merge through a verified PR.

## Checkpoint lifecycle

### 1. Reconcile entry truth

Before each evidence unit or milestone:

- read `AGENTS.md`, the execution goal, authority record, control profile, current status, roadmap, and active contract;
- verify canonical root, branch, HEAD, worktree, remote, issue, PR, custody roots, and latest accepted checkpoint;
- verify the identities of required data, runtime, model, and evidence inputs;
- treat absent evidence as `missing` or `unknown`, never as pass; and
- reconcile contradictions before consequential writes.

### 2. Bind a contract

Every milestone contract must record:

- exact authority reference and active action classes;
- objective, entry conditions, exit conditions, and stop conditions;
- allowed paths and forbidden work;
- dependency-ordered units;
- action class and `human_gate` for every unit;
- expected and observed exit-condition deltas;
- decision value;
- required real-surface checks;
- failure retention and recovery behavior; and
- exact next handoff.

Only one unit may be active unless the contract explicitly proves that parallel units have disjoint inputs, writes, and decisions.

### 3. Execute one bounded unit

Select a dependency-ready unit listed by the validated contract as authorized. Confirm inputs, outputs, writes, checks, recovery, and stops. Execute the smallest coherent action that answers its question.

Use these evidence dispositions independently of execution status:

- `pass`: required evidence supports the unit's bounded conclusion;
- `remediate`: bounded correction is allowed and retains the original failure;
- `exclude`: evidence is ineligible and retained with the reason;
- `defer`: evidence or dependency is not currently decidable; or
- `stop`: a hard stop or terminal rule ends the route.

Scientific comparison uses the separately defined `PASS`, `FAIL`, `INCONCLUSIVE`, or `INVALID` result vocabulary. Never substitute an execution status for a scientific disposition.

### 4. Verify the changed real surface

Minimum evidence by surface:

| Surface | Minimum evidence |
|---|---|
| Governance or documentation | Complete diff, reference/link checks, authority, boundaries, and internal consistency |
| Repository control | Repository validator, focused tests, schema validators, and CI result |
| Runtime or CLI | Focused tests plus a real process invocation under the pinned environment |
| Data | Source and byte identity, deterministic checks, schema/quality/leakage gates, and actual array inspection |
| Neural model | Gradients, parameter movement, histories, checkpoint selection, safe reconstruction, fresh-process inference, and replay |
| Evaluation | Frozen input/config identities, every seed and control, actual predictions/probabilities, metrics, masks, collapse gates, and terminal rule |
| Geospatial output | Write, reopen, metadata checks, mask semantics, and visual inspection |
| Rendered evidence | Source checks plus inspection of the actual rendered artifact at useful resolution |
| GitHub or public state | Direct live read of the authoritative branch, commit, PR, checks, tag, release, assets, and rendered public surface |
| Rights, security, or custody | Fail-closed checks and the explicit owner decision when the execution goal requires it |

### 5. Accept, publish, and hand off

At a milestone boundary:

1. compare the full ledger with every exit condition;
2. choose `ship`, `remediate`, `fallback`, `defer`, or `stop` from evidence;
3. reconcile roadmap, status, changelog, version history, ledgers, decisions, prompt log, devlog, and public claims;
4. inspect the complete diff and rerun risk-matched verification;
5. perform authorized GitHub writes only after local gates pass;
6. verify the actual live GitHub state; and
7. record the exact accepted checkpoint and next eligible unit.

Closing an issue, merging a PR, tagging a version, or publishing a release does not prove itself. Retain the live verification receipt.

## Canonical validation commands

Run from `C:\Projects\Active\burnlens-experiment-three`:

```powershell
python scripts/validate_repository.py
python -m unittest discover -s tests -v
python C:\Users\drewb\.codex\skills\standardize-project-control-plane\scripts\validate_project_control.py records/governance/EXPERIMENT-THREE-PROJECT-CONTROL-PROFILE-2026-007.json --project-root . --verify-paths --milestone-contract records/milestones/EXPERIMENT-THREE-MILESTONE-006-RELEASE-CLOSEOUT-2026-001.json
python C:\Users\drewb\.codex\skills\run-controlled-milestone\scripts\validate_milestone.py records/milestones/EXPERIMENT-THREE-MILESTONE-006-RELEASE-CLOSEOUT-2026-001.json --project-profile records/governance/EXPERIMENT-THREE-PROJECT-CONTROL-PROFILE-2026-007.json
python C:\Users\drewb\.codex\skills\reconcile-project-state\scripts\evaluate_project_state.py records/reconciliations/EXPERIMENT-THREE-STATE-2026-007.json --project-root . --verify-paths
python scripts/validate_frozen_protocol.py --custody-root C:\Projects\Active\burnlens-experiment-three-custody
```

Use the active milestone path in place of the Milestone 0 path after handoff. Tool validation never creates authority or proves scientific success.

## Git requirements

- Preserve published history; do not force-push, rewrite, or delete it.
- After Milestone 0, use one issue-backed `codex/*` branch per coherent milestone or explicitly contracted exception.
- Keep commits reviewable and bind them to the active issue and evidence unit.
- Do not merge when required checks, evidence, authority, rights, or real-surface verification are missing.
- Verify the remote commit and branch after every push or merge.
- Create tags and releases only from an accepted exact commit under a release-authorized contract.
- Never change visibility, access, ownership, protection, or custody without the owner's explicit decision.

## Scientific freeze rules

- Milestones 0 through 2 cannot produce substantive benchmark training or evaluation evidence.
- Milestone 3 must freeze the complete protocol and its hash before substantive training.
- The freeze must preserve the already approved deterministic float32 CPU PyTorch route, event-class-balanced masked BCE, Adam `0.001`, batch `4`, maximum `200` epochs, patience `25`, seeds `20260725`/`20260726`/`20260727` with the first primary, minimum-validation-balanced-BCE checkpoint rule, validation-only worst-event-Dice/macro-IoU threshold rule, and no augmentation, positive-class weighting, BatchNorm, dropout, ensemble, pretraining, or search.
- Comparative `PASS` must require every seed to be nonconstant on each test event and the three-seed median to beat the strongest constant control on macro IoU and worst-event Dice; Milestone 3 binds exact implementations and tie rules but may not choose alternative values.
- Milestone 4 cannot open retrospective test predictions or metrics.
- Milestone 5 permits one controlled retrospective evaluation after every entry gate passes.
- Post-opening changes to architecture, data, split, labels, normalization, loss, optimizer, seeds, checkpoint rule, threshold rule, metrics, collapse gates, controls, or terminal rules are not remediation within Experiment Three. They require a separately approved Experiment 3B.
- A fresh confirmatory lane requires a separate owner-approved contract and is never an Experiment Three completion dependency.

## Failure retention and path efficiency

- Retain original failed inputs, outputs, logs, receipts, and decisions before correction.
- Never overwrite raw sources, accepted checkpoints, sealed runs, evaluation packages, or released artifacts.
- Do not replace failed seeds, unfavorable metrics, or missing evidence with a more convenient attempt.
- After two consecutive terminal evidence units with `no_progress`, perform the objective path-efficiency review defined by the active contract.
- The review may consolidate diagnostics, choose an already authorized fallback, or close a dead route. It may not change the goal, claim envelope, frozen protocol, or authority.

## Hard stops

The owner gates in the execution goal apply to every checkpoint. Stop additionally for:

- an unexpected nonempty or changed remote;
- unresolved disagreement among current control records and live state;
- a project, custody, cache, temporary, or run path outside `C:\Projects\Active`;
- any project route through the forbidden `C:\Users\drewb\OneDrive` root;
- secrets, credentials, private data, rights ambiguity, or terms acceptance;
- benchmark, model, training, inference, evaluation, or release material appearing before its milestone permits it;
- an unverified public claim or release surface; or
- an explicit pause.

## Terminal checkpoint

Experiment Three terminal closeout requires both `lifecycle_status` and `comparative_status`, complete retained evidence, exact replay, verified live release state, reconciled records, and no concealed continuation work. A lifecycle `PASS` with comparative `FAIL` is a completed experiment. Do not create additional attempts merely to improve the result.
