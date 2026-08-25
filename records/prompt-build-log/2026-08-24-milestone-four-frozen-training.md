# Prompt Build Log: Milestone 4 Frozen Training

## Authority consumed

The active long-running Experiment Three goal, authority record, profile 005,
Milestone 4 contract, issue #8, repository instructions, accepted Milestone 3
checkpoint, and frozen protocol authorized the bounded train/validation
lifecycle and routine reviewed publication. They did not authorize test access,
evaluation, a protocol change, or a release.

## Work performed

- Reconciled live repository, branch, accepted main, issue, runtime, custody,
  protocol, and test-seal state.
- Verified exact train and validation data identities and decoded only those
  roles.
- Implemented deterministic frozen training, histories, checkpoint packaging,
  validation-only probability output, shared-threshold selection, fresh-process
  reload, and independent replay verification.
- Retained attempt 001 as `FAIL` and attempt 002 as `INVALID` instead of
  rewriting them after bounded implementation repairs.
- Executed attempt 003 from fresh initialization for all three declared seeds;
  retained it as `INVALID` when a completion audit found nonconforming replay
  receipt filenames.
- Applied the receipt-name-only repair, executed attempt 004 from fresh
  initialization for all three seeds, then retained it as `INVALID` when a full
  execution audit found the seeds had trained sequentially in one parent
  process.
- Repaired the runner to spawn one isolated training process per seed, executed
  attempt 005 from fresh initialization, and verified exact primary/replay
  bytes with test sealed.

## Current boundary

The M4 candidate has three training runs, three selected checkpoints, and three
validation-only inference packages. It has zero evaluations, test openings,
tags, or releases. Reviewed merge and live verification remain required before
M4 acceptance; a new M5 contract is required before any test access.
