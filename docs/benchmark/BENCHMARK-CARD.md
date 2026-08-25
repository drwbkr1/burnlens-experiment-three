# BurnLens Deschutes compatibility benchmark card

## Intended role

This is the exact admitted Experiment One benchmark reused for one bounded,
retrospective compatibility study. It supports comparison with Experiment One's
RBR and canonical U-Net under the same split, masks, normalization, and metric
semantics. It does not support operational wildfire mapping or fresh scientific
confirmation.

## Composition

| Role | Events | Scored prototype-core pixels | Class counts |
| --- | --- | ---: | --- |
| Train | Green Ridge, Tepee | 109 | 58 background / 51 burned |
| Validation | Grandview, McKay | 89 | 32 background / 57 burned |
| Test | Ward Creek, Windigo | 89 | 50 background / 39 burned |

The repository stores identities and public records only. The admitted 131-file
benchmark package remains in controlled local custody; no benchmark byte is
committed or attached to the release.

## Labels and measurement

Labels are sparse selected prototype cores derived from dNBR-binned Sentinel-2
change evidence. Unlabeled pixels are unknown, not background. Metrics are
computed per event and class, then macro-averaged. Events—not pixels—are the
relevant independent units.

RBR is structurally favored because both its rule and the labels use related
spectral-change evidence. Its test score of `1.0` is prototype-core agreement,
not independent accuracy. Only two events appear in each split role; no
significance or population-generalization claim is supported.

## Provenance, rights, and exclusions

The exact dataset, split, normalization, masks, source and terms records, RBR,
U-Net artifacts, and historical predictions were hash-bound before intake.
Owner-controlled rights and upstream source gates permit the frozen local
experiment. Repository or release redistribution of benchmark bytes was not
authorized. Native provider archives, restricted Tepee BARC4/BARC256 material,
private review material, and fresh-event evidence are excluded.

See the [identity inventory](../../records/provenance/EXPERIMENT-ONE-BENCHMARK-IDENTITY-INVENTORY-2026-001.json),
[source gate](../../records/source-gates/EXPERIMENT-ONE-BENCHMARK-SOURCE-GATE-2026-001.json),
and [intake receipt](../../records/intake/EXPERIMENT-ONE-BENCHMARK-INTAKE-RECEIPT-2026-001.json).
