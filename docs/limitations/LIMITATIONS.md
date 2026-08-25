# BurnLens Experiment Three Limitations

## Scientific limits

- The benchmark is retrospective and its Experiment One test outcomes were
  known before Experiment Three. It is a compatibility replay, not blind
  confirmation.
- There are only two events in each split role. Events, not pixels, are the
  relevant independent units; significance and population-generalization
  claims are unsupported.
- Labels score sparse selected prototype cores. Dense model output is not dense
  ground truth and cannot establish full-scene segmentation quality.
- The inherited RBR baseline is structurally aligned with dNBR-derived
  prototype-core labels. Its reported perfect score is prototype-core agreement,
  not independent accuracy.
- Validation selection does not establish test performance. At the current M4
  candidate, test values remain sealed and comparative status is unknown.

## Model and engineering limits

- The 137-parameter pointwise network cannot use spatial context; this is an
  intentional data-sized hypothesis with a real representational constraint.
- The lifecycle is bound to one approved Windows x64 CPU runtime and exact
  deterministic settings. Portability beyond that surface is not yet proven.
- Checkpoints and probability arrays remain in controlled external custody,
  not Git. Public records bind identities but do not distribute those bytes.
- Exact replay demonstrates reproducibility within the frozen environment; it
  does not validate labels, source imagery, operational utility, or independent
  scientific accuracy.

## Use limits

Do not use Experiment Three for wildfire response, evacuation, incident
management, public safety, property decisions, environmental compliance, or
official mapping. Any future fresh-event study requires separately approved,
independently sampled and reviewed evidence and cannot rescue or tune this
experiment.
