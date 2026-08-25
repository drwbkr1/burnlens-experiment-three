# Milestone 4 Devlog: Frozen Training

Milestone 4 moved Experiment Three from a frozen executable protocol to a real
neural training lifecycle without opening the known test.

The data gate first decoded only the admitted train and validation roles. All
32 arrays and 888,832 bytes matched the frozen manifest, schema, masks, class
counts, and normalization rules. The loader has no Milestone 4 path for test.

The first training attempt exposed a genuine replay-process defect: the child
process had not applied the required one-thread runtime configuration, so its
probability hash differed even though the checkpoint tensor matched. That
partial attempt remains retained as `FAIL`. A bounded repair produced a second
three-seed run and exact replay, but a completion audit caught a different
contract defect: the checkpoint file was called `state_dict.pt`, while the
prospectively frozen artifact list required `weights.pt`. That complete attempt
remains retained as `INVALID`.

The checkpoint filename and manifest were repaired without changing training
semantics, and all three seeds were rerun from fresh initialization. A later
artifact audit caught that attempt 003 still used `fresh-process-reload.json`
and `run-receipt.json` rather than the frozen required `replay-receipt.json`
and `exact-replay-receipt.json`. Attempt 003 remains `INVALID`. Those receipt
names were repaired without changing scientific semantics, and attempt 004
again reran all seeds from initialization.

A full execution audit then found that attempt 004 still trained its three
seeds sequentially inside one parent process, violating the frozen requirement
for a fresh training process per seed. Attempt 004 remains `INVALID`. The
runner was repaired to spawn one isolated `-I` training child per seed, with
deterministic runtime identity and null-exception metadata, and all seeds were
rerun again as attempt 005.

Attempt 005 selected epochs 105, 147, and 146; every seed had finite nonzero
gradients and changed weights. Tensor-only checkpoints reconstructed exactly in
fresh isolated processes. The shared validation-only threshold is `0.5`, and
independent verification found the primary and replay roots byte-identical: 20
files and 270,793 bytes each. Test values were never opened.

This candidate later passed reviewed publication. PR #9 merged the exact tree
to live `main` at `53983c09a03d7f8f9453e6f492b05e58b795b876`; merge-triggered
CI `32875755932` and direct identity verification passed. Milestone 4 is an
accepted scientific-training checkpoint, not a comparative result or release.
Milestone 5 activated separately with the test still sealed.
