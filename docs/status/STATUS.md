# BurnLens Experiment Three Status

| Field | Current value |
| --- | --- |
| Status date | 2026-08-24 |
| Canonical remote | `https://github.com/drwbkr1/burnlens-experiment-three` |
| Canonical local checkout | `C:\Projects\Active\burnlens-experiment-three` |
| Working version | `0.2.0-m2-runtime-gate` (unreleased) |
| Accepted checkpoint | `32e5b0dfbd93bdf337fa4f2e9bde29d0bc36a6a4` on live `main` |
| Active work | Milestone 2, issue [#4](https://github.com/drwbkr1/burnlens-experiment-three/issues/4) |
| Active review | Exact runtime successor review; blank response has zero decisions |
| Overall state | Candidate 001 was explicitly approved but failed activation; inspected existing-Python surfaces were restored. Candidate 002 is source-ready but requires a fresh exact owner decision before download or execution. |

## Current truth

Milestone 1 is accepted and live-verified. Pull request
[#3](https://github.com/drwbkr1/burnlens-experiment-three/pull/3) merged to
[`32e5b0dfbd93bdf337fa4f2e9bde29d0bc36a6a4`](https://github.com/drwbkr1/burnlens-experiment-three/commit/32e5b0dfbd93bdf337fa4f2e9bde29d0bc36a6a4),
tree `5b2bd2904b9164b8bd3c655998749cb024202148`. Candidate, pull-request,
and merge-triggered checks passed; the live README, execution goal, source
gate, readiness decision, and intake receipt match the accepted candidate.
Issue #2 is closed. There are still zero tags and zero releases.

| Surface | State | Evidence |
| --- | --- | --- |
| Experiment One identity | `PASS` | Clean source commit `a741111d82e69689022d2058118ed8f4b9bf3546`, tree `bc679254030eb57a65f58ac2af10880866fc52be`; exact 48-array dataset and comparator identities retained |
| Owner/rightsholder review | `PASS: yes`, scoped | One exact attested response locked and reconciled; public aggregate decision SHA-256 `ce7efbbf6eb70713211f46228ffdd6b98fdd5d154afab91fdd75fa1cd887e1bf`; raw response remains private |
| Current external-source gate | `READY` | Six sources, 48 required criteria, 15 live observations, zero blockers or warnings; native provider bytes and restricted Tepee BARC material excluded |
| Dataset readiness | `PASS` | Ten required gates and nine count checks pass; 25 focused source tests passed in the locked Experiment One runtime; training authority remains false |
| Controlled benchmark intake | `PASS` | 131 approved artifacts / 3,369,748 bytes promoted without replacement; destination roster SHA-256 `0daf93b2b3a21330d501c9e222d907738c19e4d5b9e00ebbdd169b65aadb89f4` |
| Experiment Three dataset count | `1` | One retrospective benchmark input admitted to external controlled custody; no benchmark byte committed to Git |
| Runtime candidate inventory | `PASS FOR OWNER REVIEW` | Exact CPython 3.12.10 / uv 0.10.7 / PyTorch 2.13.0+cpu Windows x64 candidate; 20 effective packages; private lock SHA-256 `66ef4a354db2a1e51bd6ebeca81844c1f71497c1f8164e27b99816da5ce2e081` |
| Runtime source gate | `READY` | Four sources, 32 required criteria, 12 live observations, zero blockers or warnings; this creates no adoption authority |
| Runtime candidate 001 adoption | `PASS: yes`, scoped | One exact attested owner response was locked and reconciled; public aggregate decision SHA-256 `af559ec1ebeebea5338b5c8e8b0200dbb98026980111de56fbbfd4f364a8b4ee` |
| Runtime candidate 001 activation | `FAIL`, route closed | The signed installer entered same-version maintenance mode on existing Python instead of creating the Active-only runtime. Zero wheels or imports followed; failure record SHA-256 `a6f98a20371a1ee3a6ad36e7d272fc21fa952d41bf6a5fa9c6abdf28ed803512`. |
| Existing-Python recovery | `PASS`, scoped | pip, test, tkinter/Tk, headers, files, launcher, user PATH, and recorded install features were restored and verified; this does not erase the failed transaction. |
| Runtime successor inventory | `PASS FOR OWNER REVIEW` | Official CPython 3.12.10 embeddable ZIP plus unchanged 20-wheel lock; inventory SHA-256 `ae95bc3982766e996c0ec6cb15d4964738f1958f48b1eabe73d2e2d27b3e3967` |
| Runtime successor source gate | `READY` | One materially new source, eight required criteria, six live observations, zero blockers or warnings; three unchanged package sources inherit gate 001 |
| Runtime successor adoption | `PENDING OWNER YES/NO` | Blank exact response contains zero decisions; no successor artifact has been downloaded, extracted, vendored, or executed |
| Model implementation | `MISSING` | Fixed architecture direction only |
| Training runs / checkpoints | `0 / 0` | Training remains unauthorized before later gates |
| Inference runs / evaluations | `0 / 0` | Known test evidence has not been opened by Experiment Three |
| Metrics / rendered result | `MISSING` | No Experiment Three scientific output exists |
| Release | `0` | No tag or GitHub release exists |
| Fresh confirmation | `DEFERRED` | Separate owner-gated lane; not needed for primary completion |

`PASS` is role-bounded. Rights and readiness for controlled local intake do not
authorize repository redistribution, training, evaluation, or broader claims.
`MISSING` is not `PASS`.

## Scientific boundary

The admitted benchmark is the already-observed Experiment One compatibility
benchmark. Events, not pixels, are the relevant independent units. Its sparse
selected prototype cores cannot establish independent accuracy, dense
segmentation quality, population generalization, statistical significance,
model superiority, operational fitness, or wildfire-response utility.

The approved 137-parameter `6 -> 8 -> 8 -> 1` pointwise neural detector and
bounded training choices remain unchanged. No model code may become substantive
training evidence until synthetic preflight passes and the complete executable
protocol is frozen. Any post-evaluation tuning or new architecture belongs to a
separately approved Experiment 3B.

## Custody and retained failures

- Admitted bytes live only beneath
  `C:\Projects\Active\burnlens-experiment-three-custody\benchmark`.
- The canonical Git repository contains manifests and receipts, not benchmark
  assets, private review material, native provider bytes, restricted Tepee
  BARC4/BARC256 material, or credentials.
- The first focused dataset-validation attempt under system Python retained
  three missing-`rasterio` import failures; the same 25 focused tests passed in
  the locked Experiment One environment.
- Intake attempt 001 safely stopped after 48 promotions when a checker treated
  a staged PNG as UTF-8 text. Resume reverified those 48 and promoted the
  remaining 83 with zero collisions, overwrites, or identity mismatches.
- Prior BurnLens repositories remain read-only and unchanged.
- Runtime candidate 001's signed installer was admitted exactly, but Windows
  detected an existing same-version per-user product and performed a
  maintenance `Modify` transaction instead of creating the requested isolated
  runtime. The attempt is retained as `FAIL`. Recovery restored the specifically
  inspected existing-install surfaces; no wheel download, model import,
  synthetic run, or scientific work occurred.

## Immediate next gate

Provide one explicit `yes` or `no` for runtime successor
`CPYTHON-3.12.10-EMBED-UV-0.10.7-TORCH-2.13.0-CPU-WINDOWS-X64-002`, bound to
inventory SHA-256
`ae95bc3982766e996c0ec6cb15d4964738f1958f48b1eabe73d2e2d27b3e3967`.
A `yes` permits exact Active-only ZIP download, verification, application-local
extraction, vendoring of only the unchanged locked wheels, license capture,
and CPU/native-package/synthetic compatibility tests. It does
not permit benchmark access or substantive training. A `no` rejects the exact
successor and leaves Milestone 2 blocked pending a separately approved
alternative. Candidate 001's prior `yes`, silence, or general chat cannot be
carried forward as this decision.
