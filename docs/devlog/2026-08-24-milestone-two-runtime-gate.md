# Devlog: Milestone 2 Runtime Gate

Milestone 1 is no longer a candidate. Pull request #3 merged the accepted
benchmark-provenance and intake checkpoint to live `main` at commit
`32e5b0dfbd93bdf337fa4f2e9bde29d0bc36a6a4`; its candidate, pull-request,
and merge-triggered checks passed, and the live evidence surfaces matched.

Milestone 2 begins with a synthetic-only boundary. Its first technical risk is
not the 137-parameter model code; it is whether Experiment Three has one exact,
reproducible, legally reviewable CPU runtime that does not quietly inherit
another project's environment.

The candidate is therefore deliberately fresh and narrow:

- CPython 3.12.10 from the official Windows x64 installer;
- the exact already-observed uv 0.10.7 executable as resolution/install
  tooling;
- a private, hash-bound 20-package Windows lock led by PyTorch 2.13.0+cpu,
  NumPy 2.5.1, Pillow 12.3.0, and Rasterio 1.5.0;
- private download/cache custody and the installed runtime entirely beneath
  `C:\Projects\Active`;
- no copied Experiment One environment, OneDrive state, CUDA, Lightning,
  TorchVision, pretrained model, model hub, credential, service, or spend.

Only registry metadata was resolved. No Python installer or wheel was
downloaded, no package was installed, no candidate import ran, and no model or
benchmark value was touched. The source gate passes for presenting this exact
candidate to the owner, not for adopting it.

The owner supplied one exact `yes`. The installer and Sigstore bundle matched
their approved identities, but the installer detected an existing per-user
CPython 3.12.10 product and entered maintenance `Modify` mode. Exit code 0
therefore described a completed maintenance transaction, not construction of
the requested Active-only runtime. The target had no `python.exe`; the route
failed before wheel download or import. The same signed installer restored the
specifically inspected existing-Python components, PATH/launcher integration,
and registry feature state. The activation remains `FAIL` and closed.

The smallest successor avoids Windows installation entirely: Python.org's
official CPython 3.12.10 embeddable ZIP, application-locally extracted beneath
`C:\Projects\Active`, with only the unchanged hash-locked wheels vendored
alongside it. Its main uncertainty is real: embedded Python is not an ordinary
pip-managed environment, so PyTorch, Rasterio, native DLL/data discovery,
subprocess behavior, and deterministic replay must all pass fresh-process
checks. The owner supplied a separate exact `yes`, locked before reveal. The
ZIP and Sigstore digest matched, the unchanged 20-package lock installed under
enforced hashes, and every runtime gate passed without changing the existing
Python executable.

That runtime now carries a real neural implementation—not a mock. The fixed
model contains exactly 137 trainable parameters across three shared 1x1
convolutions. Six focused tests prove its architecture, arbitrary HxW behavior,
event/class-balanced masked loss, unknown-mask preservation, deterministic
fixture, and safe state-dict reload.

Two independent full synthetic executions then produced identical receipts and
all seven artifact bytes. Loss fell from `0.6965426803` to `0.5614569187`;
gradients were finite and nonzero; weights changed; fresh-process logits and
probabilities matched; the GeoTIFF reopened exactly; and the four-panel render
was visually legible. The diagnostic accuracy is deliberately not promoted as
a scientific result. No benchmark value was accessed and no substantive
training, inference, or evaluation occurred.
