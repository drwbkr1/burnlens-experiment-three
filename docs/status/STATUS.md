# BurnLens Experiment Three Status

| Field | Current value |
| --- | --- |
| Status date | 2026-08-25 |
| Canonical remote | `https://github.com/drwbkr1/burnlens-experiment-three` |
| Canonical local checkout | `C:\Projects\Active\burnlens-experiment-three` |
| Working version | `1.0.0`, tagged and released |
| Accepted checkpoint | `8de60a3350a7c25942be8223bf9067c9460774d1` on live `main`; tag `v1.0.0` |
| Active work | Terminal record acceptance, issue [#12](https://github.com/drwbkr1/burnlens-experiment-three/issues/12) |
| Active review | None |
| Overall state | Release `v1.0.0` is live and independently verified. Lifecycle `PASS`, comparative `FAIL`, exact replay `PASS`; only terminal-record acceptance and goal closeout remain. |

## Current truth

The reviewed release candidate is accepted on live `main`. Pull request
[#13](https://github.com/drwbkr1/burnlens-experiment-three/pull/13) merged exact
tree `98b8447f7aa1f1668adc14da5e364785c05286a1` at
[`8de60a3350a7c25942be8223bf9067c9460774d1`](https://github.com/drwbkr1/burnlens-experiment-three/commit/8de60a3350a7c25942be8223bf9067c9460774d1).
Candidate, pull-request, and merge-triggered runs
`32882903304`/`32882930436`/`32882978238` passed. Annotated tag `v1.0.0`
peels to that commit, and GitHub release `376615584` is public, non-draft, and
non-prerelease. Opening `M5-OPENING-2026-001` remains terminal and cannot be
reused for tuning.

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
| Runtime successor adoption | `PASS: yes`, scoped | One exact attested response locked and reconciled; public aggregate decision SHA-256 `0bb8daafca4198b995f09952404fd93d185e4dccccb0ed45fc072143d491a29e` |
| Runtime successor activation | `PASS`, synthetic-only | Exact application-local runtime: 18,171 files / 726,368,861 bytes / roster SHA-256 `77a5bce011c81cd24ae080d76566e0bbcf8c500e80dfdb7f88efe19ddc1bf977`; 20 packages compatible; CPU/native/replay checks pass |
| Model implementation | `PASS`, synthetic scope | Exact `6 -> 8 -> 8 -> 1` pointwise network, 137 parameters, arbitrary HxW, mask-preserving balanced loss, strict state-dict package |
| Synthetic lifecycle | `PASS` | Primary and replay each contain 7 files / 20,628 bytes with identical roster `9c008f10...`, receipt `7a3fde99...`, and fingerprint `d13ec92...`; fresh-process reload, GeoTIFF, and render verified |
| Frozen executable protocol | `PASS`, accepted | Canonical-LF SHA-256 `12a092e90586a819e6014ed181da82721675040ff2678c7d7115b1582b904f1e`; accepted through PR #7 and live-main CI `32689530033` |
| Train/validation data gate | `PASS` | Exactly 32 arrays / 888,832 bytes verified; train 109 and validation 89 scored prototype-core pixels; zero test arrays listed or decoded |
| Training runs / checkpoints | `3 / 3`, accepted | Seeds `20260725`/`26`/`27`; selected epochs `105`/`147`/`146`; strict `weights.pt` packages reconstruct exactly; accepted through PR #9 |
| Inference runs / evaluations | `6 / 1` | Three validation-only plus three frozen test inference runs; one single-opening retrospective evaluation |
| Neural lifecycle | `PASS` | Exact build, training, safe reload, inference, evaluation, packaging, and primary/replay verification completed |
| Comparative outcome | `FAIL` | Three-seed median macro IoU `0.2201` and median worst-event macro Dice `0.2919`; did not beat strongest constant-control values `0.2853` / `0.3333`; one seed was constant on one event |
| Per-seed macro IoU | `0.2201 / 0.2009 / 0.5794` | Seeds `20260725` / `20260726` / `20260727`; all reported, no best-seed substitution |
| RBR / canonical U-Net | `1.0000 / 0.2147` macro IoU | RBR's perfect sparse-core agreement is structurally favored; the U-Net equals constant-burned and predicts all 89 scored cores burned |
| Evaluation package | `PASS` | Primary/replay each 53 files / 367,150 bytes / roster `e322a101...`; 36 GeoTIFFs reopen exactly; 5360x2076 render directly inspected |
| Reviewer evidence | `PASS`, released | Public-safe architecture, three-seed curves, and all-seed/control comparison contain numerical evidence only; imagery-bearing panel remains hash-bound in controlled custody |
| Release | `1`, verified | [`v1.0.0`](https://github.com/drwbkr1/burnlens-experiment-three/releases/tag/v1.0.0); two exact assets; both GitHub source archives match the tagged 136-file tree |
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
bounded training choices remained unchanged through synthetic preflight,
protocol freeze, training, and evaluation. Any post-evaluation tuning or new
architecture belongs to a separately approved Experiment 3B.

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
- Frozen-training attempt `m4-2026-001-primary` stopped after seed `20260725`
  because its reload child had not applied the required one-thread runtime
  configuration. The partial six-file root remains retained as `FAIL`.
- Attempt `m4-2026-002` completed all three seeds and exact replay, but its
  checkpoint payload was named `state_dict.pt`, violating the frozen required
  `weights.pt` artifact schema. Both roots remain retained as `INVALID`.
  Attempt `003` reran every seed from initialization but is also retained as
  `INVALID` because its replay receipt filenames did not match the frozen
  artifact list. Attempt `004` used the correct artifacts but is `INVALID`
  because its seeds trained sequentially in one process. Attempt `005` reran
  every seed in a separate fresh process and is the sole accepted scientific
  candidate.

## Immediate next gate

Publish the live-release receipts and reconciled status through a checked PR,
then accept the terminal closeout record on `main`, close issue #12, and mark
the long-running goal complete. Fresh confirmation and Experiment 3B remain
outside this milestone.
