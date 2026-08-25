# Milestone 6: reviewer release and closeout

Milestone 6 begins from the accepted Milestone 5 result at live main
`45b32c1cb782edc31ef8a4f49671b6a897c7d7bb`. It cannot improve or rerun the
model. Its job is to make lifecycle `PASS` and comparative `FAIL` inspectable,
replayable under the stated custody conditions, and honestly releasable.

The public package is deliberately narrower than the controlled scientific
package. It may contain repository-authored narrative, metrics, hashes,
manifests, and numerical graphics. Benchmark pixels, labels, checkpoints,
predictions, GeoTIFFs, and the imagery-bearing panel remain external because
their controlled-use gate did not authorize public redistribution.

Reviewer graphics start with the result, show the 137-parameter architecture,
retain all three training histories, and compare every seed and control. The
first comparison layout was retained as a visual failure because long labels
collided with the decision box. A spacing-only revision passed direct
inspection without changing any metric.

The first detached Windows checkout exposed a real portability defect: line
ending conversion changed six hash-bound text surfaces. That attempt remains
retained as `FAIL`. An explicit LF checkout policy corrected the issue, and a
second detached worktree passed repository controls, all 56 approved-runtime
tests, full controlled scientific replay, and an independent package build.

The public evidence ZIP reproduced exactly across three builds at 34,007 bytes
and SHA-256 `ac811cb42511a2ec5c1163a1a9f193dcf4bd3637485a452b526a06435511f8e4`.
Its clean-extraction verifier passed, and the candidate release audit evaluates
`verified`. It remains a candidate until reviewed main and live publication are
separately verified.

PR #13 passed both candidate and pull-request checks and merged as live main
`8de60a3350a7c25942be8223bf9067c9460774d1`. Its tree exactly matches the
audited candidate, and merge-triggered run `32882978238` passed. That receipt
unlocks only the exact `v1.0.0` tag/release action; no publication claim is made
until the live release and downloaded assets verify.

Annotated tag `v1.0.0` now peels exactly to that commit. GitHub release
`376615584` is public, non-draft, and non-prerelease. A separate controlled
intake downloaded the two release assets and both GitHub source archives into
an Active-only root without replacement. The asset hashes and packaged
verifier pass; ZIP, tarball, and tagged worktree share the same 136-file roster;
release notes match; and the public page returns HTTP 200. Terminal records are
accepted through final PR #15, which closes issue #12. Experiment Three ends
with lifecycle `PASS`, comparative `FAIL`, one verified release, and no active
successor work.
