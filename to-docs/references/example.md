# Example: Save a Design with an Open Question

This is an illustrative output, not an approved design or required template. The request is to save a discussion only. Its settled points are resumable CSV imports and no duplicate committed rows; the retention period remains open.

Example saved source: `docs/designs/import-resume.md`.

> # Resume Interrupted Imports
>
> An interrupted CSV import retains valid committed progress. On continuation, it retries unfinished rows without inserting committed rows again.
>
> Proposed mechanism: retain committed row identities in a checkpoint tied to the import identity. This mechanism has not been adopted; an unrelated file must not inherit saved progress.
>
> Open: how long checkpoints remain available. A retention value has not been selected. Suggested acceptance cases: interruption, repeated continuation, and a mismatched import identity.
>
> This document records the target behavior. Implementation and runtime verification have not started.

Example delivery: “Saved the design in `docs/designs/import-resume.md`. Checkpoint retention is still open. No implementation or tests were performed.” A change record is unnecessary for this save-only request. Add execution details later only if authorized work needs them to persist.
