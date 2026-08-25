# Reproducibility and release verification

Experiment Three separates two reproducibility claims that must not be
conflated.

## Public package verification

The GitHub release contains repository-authored documentation, machine-readable
records, numerical SVGs, a manifest, and a standalone verifier. A clean
extraction can verify every included byte without external data or Python
packages beyond the standard library:

```powershell
python verify_release_package.py --package-root . --manifest release-manifest.json
```

This proves package integrity and internal evidence consistency. It does not
re-run the neural model and is not public-download scientific reproduction.

## Full scientific replay

Full replay requires all three separately controlled inputs:

1. the exact released repository revision;
2. the approved application-local CPython/PyTorch CPU runtime beneath
   `C:\Projects\Active\burnlens-experiment-three-runtime`; and
3. the admitted benchmark, accepted checkpoints, and terminal evaluation
   package beneath `C:\Projects\Active\burnlens-experiment-three-custody`.

From a clean checkout of the release commit:

```powershell
C:\Projects\Active\burnlens-experiment-three-runtime\cpython-3.12.10-embed\python.exe -I scripts\verify_retrospective_evaluation.py `
  --root C:\Projects\Active\burnlens-experiment-three-custody\evaluation\m5-2026-001 `
  --custody-root C:\Projects\Active\burnlens-experiment-three-custody `
  --training-root C:\Projects\Active\burnlens-experiment-three-custody\training\m4-2026-005-primary `
  --inspect-geospatial --inspect-rendered
```

Expected terminal facts are lifecycle `PASS`, comparative `FAIL`, three seeds,
one opening, 36 reopened GeoTIFFs, and exact 53-file / 367,150-byte
primary/replay payloads with roster SHA-256
`e322a10135243d06360393b21553602713285a0b2f7aeabbb924930073bd1d68`.

Controlled benchmark and model-output bytes are intentionally not public
release assets. A reviewer without authorized custody can verify the public
package, records, hashes, tests, decision logic, and claim limits, but cannot
independently rerun the scientific computation from public downloads alone.
