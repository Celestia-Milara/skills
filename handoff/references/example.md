# Example: Continue a Storage Fix

The facts below belong to an illustrative fixture. They are not claims about a real repository or a required handoff format.

> Continue the interrupted-import fix in the existing workspace on branch `fix/import-resume`. The request permits local code and test changes; commit and publication are not authorized.
>
> Read `requirements.md` for row identity and `.agents/changes/import-resume/README.md` for the target and remaining work. That record links the storage decision and source paths.
>
> The working tree contains this task's uncommitted store change. Its unit tests passed against the current file; persistence through a fresh connection has not been checked. No acceptance result is recorded. A separate pre-existing README edit has unknown ownership; preserve it.
>
> First inspect the current diff and the shipped store interface, then verify durable checkpoint visibility using an isolated local database. Retention duration still needs a decision; do not invent one or let it block the independent persistence check.

This message selects sources and states continuity gaps. Detailed progress stays in the change record. Saving the message does not deliver it to another session or authorize sending it.
