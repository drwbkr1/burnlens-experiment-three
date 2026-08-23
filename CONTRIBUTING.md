# Contributing to BurnLens Experiment Three

BurnLens Experiment Three is an evidence-bound experiment, not an open-ended
model search. Contributions are welcome when they preserve the frozen question,
custody boundaries, failed evidence, and claim limits.

## Before proposing a change

1. Read [README.md](README.md), [the current status](docs/status/STATUS.md),
   [the roadmap](docs/roadmap/ROADMAP.md), and
   [the decision register](records/decisions/DECISION-REGISTER.md).
2. Confirm that the change belongs to the active milestone and associated
   issue.
3. Work only in `C:\Projects\Active\burnlens-experiment-three` or another
   explicitly project-owned path beneath `C:\Projects\Active`.
4. Do not use OneDrive for source, caches, environments, custody, temporary
   files, or outputs.
5. Treat all prior BurnLens repositories as read-only provenance sources.

## Evidence rules

- Missing evidence is `unknown` or `missing`, never a pass.
- Preserve failed, rejected, blocked, invalid, stale, and superseded attempts.
- Do not modify labels, splits, metrics, thresholds, seeds, architecture,
  training rules, or decision rules after evaluation evidence is visible.
- Do not select or report only the best seed.
- Do not convert sparse scored cores into a dense-segmentation claim.
- Record content hashes, commands, environment identity, inputs, outputs, and
  validation results for material evidence.
- Use synthetic data and disposable weights for preflight. Substantive training
  requires the complete protocol-freeze gate to pass first.

## Data and model artifacts

Do not copy benchmark bytes, imagery, labels, checkpoints, or pretrained model
artifacts into this repository until source, terms, attribution, redistribution,
custody, and integrity checks are documented and approved. The repository's MIT
license covers repository-authored software and documentation; it does not
relicense third-party data or model artifacts.

Never commit credentials, tokens, private data, local absolute-path secrets, or
unreviewed large binaries.

## Change workflow

- Associate each bounded change with an issue.
- Use a `codex/` branch unless the issue specifies another convention.
- Keep commits focused and human-readable.
- Update status, changelog, evidence, decisions, devlog, and version records in
  the same checkpoint when their truth changes.
- Include exact validation commands and results in the pull request.
- Review rendered scientific surfaces as rendered artifacts, not only source
  files or unit tests.
- Do not merge, tag, release, or publish a checkpoint that cannot be verified
  from the exact reviewed revision.

## Human gates

Stop for owner direction before changing the research promise, claim envelope,
model family, frozen protocol, cohort, labels, split, metrics, or decision
rules; initiating or opening fresh confirmation evidence; adopting a materially
new source, model, dependency runtime, or service; accepting terms or using
credentials; spending money; changing access, ownership, visibility, or
custody; modifying another repository; taking an irreversible action; or
publishing beyond approved claims.

Security concerns should be reported privately to the repository owner rather
than demonstrated against public or production systems.
