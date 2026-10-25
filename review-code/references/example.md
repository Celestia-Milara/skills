# Example: Separate a Defect from an Evidence Gap

This is an illustrative report for a synthetic retry-policy change. The fixture's requirement permits timeout retries and rejects validation-error retries. Its changed `is_retryable` function returns true only for validation errors. Names, line numbers, and outcomes below are examples, not an actual review result or fixed format.

> Reviewed the working-tree change in `import_policy.py` against `requirements.md`. No files were modified.
>
> **[P1] Retry classification is reversed — `import_policy.py:2`.** The requirement permits timeout retries and rejects unchanged invalid input. `is_retryable("validation")` returns true and `is_retryable("timeout")` returns false. This retries permanent failures and drops the supported transient recovery path. Both results follow from the changed comparison; one fix addresses them.
>
> **Evidence gap:** the provider adapter is outside this diff and was not executed. Its mapping of provider failures to these reason strings remains unverified. This gap is not a second confirmed defect.
>
> Static inspection establishes the two counterexamples. Tests, provider integration, and manual acceptance were not run. A separate naming cleanup is unnecessary to fix the behavior.

A later authorized fix needs checks against its changed version. The standalone report itself adds no implementation, commit, or publication authorization.
