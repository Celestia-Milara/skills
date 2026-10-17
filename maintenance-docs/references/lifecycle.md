# Status, Completion, and Closeout

## Scope

The following statuses, task markers, and engineering change closeout rules apply to work that needs an engineering change record. A human-readable design may be saved by itself; this does not require creating `.agents/changes/`, a README, or an implementation plan. Settled, recommended, and unresolved design content is not engineering progress status, and no mandatory design state machine is introduced. Completing design organization does not mean the entire solution is approved or the feature implemented. A standalone design-organization task that actually exists can be completed according to its agreed deliverables, separately from later implementation.

## Overall Status and Task Markers

Maintain the overall `Status` only at the change entry point; split-out designs and plans reference that entry. A central index does not create a duplicate status record.

| Status | Meaning |
| --- | --- |
| `planned` | Recorded; the agreed work has not started. This does not mean the design is approved. |
| `in-progress` | Investigation, design, implementation, or verification is underway; the agreed work is not yet finished. |
| `paused` | Work has explicitly been paused, with conditions for resuming retained. |
| `completed` | The agreed scope of this work, including necessary verification and acceptance, is complete. |
| `cancelled` | It has been explicitly decided that this change will not continue. |

Update status according to actual progress; not every change needs to pass through every status. Status represents overall work progress, not design approval or decision validity, and does not replace notes status. Investigation can be completed as an independent goal without waiting for later implementation. Record local blockers or pending acceptance in the plan; they do not automatically pause the overall work.

By default, use `- [ ]` / `- [x]` for tasks; add text for states such as in progress, blocked, awaiting verification, or awaiting user acceptance as needed. Check a task only when its agreed deliverables and checks are satisfied. Implementation tasks can finish before overall acceptance, but retain separate verification or acceptance tasks as needed. Checking a task does not decide whether the whole change is complete. Tasks may depend on earlier items and need not be split by tool operation or commit count.

## Criteria for Overall Completion

Check against the agreed scope and acceptance sources:

1. Agreed deliverables meet requirements. For an investigation, judge by its investigation deliverables; later decisions or implementation may remain unresolved.
2. Applicable and necessary verification is complete; changed code does not mean verification passed.
3. Necessary manual acceptance is complete. If it is pending, retain it as an open task and do not claim overall completion. Do not impose extra sign-off when manual acceptance was not required.
4. Related current documentation, design plans, and notes that need maintenance have been synchronized and remain in their proper sources.

Accurately record checks that were not run or failed, environmental limitations, and evidence gaps. Explain how gaps are handled; do not omit them silently. Adopting a new goal does not mean implementation, migration, or compatibility cleanup is finished.

A commit, PR closure, merge, or release does not automatically mean the overall work is complete; a completed status does not authorize these operations. Ask the user to decide on behavior, scope, or key trade-off changes beyond existing authorization. Handle adjustments within authorization autonomously and do not reconfirm settled matters.

## Pause, Cancellation, and Resumption

When pausing or cancelling, record the reason, completed work, unfinished items, and relevant risks. A pause must also state the conditions for resuming or the next step. When those conditions are met and existing authorization still applies, verify the current state and continue in the original directory.

Cancellation does not automatically roll back completed work or revoke long-term decisions or compatibility obligations. Restarting after cancellation requires a clear basis for continuing; unfinished tasks alone do not automatically resume the work. Resuming a change does not mean restoring an old decision. Restore or supersede long-term decisions according to `decision-notes`; do not directly change the validity of an old note.

Create a separate topic for a later independent change and cross-link as needed. If a defect in the original scope is found after completion, link corrective work to the original record, preserve the original completion conclusion and subsequent changes, and do not erase history. Update status based on the actual situation rather than editing history to conceal remaining issues.

## Closeout Records and Organization

By default, keep completed or cancelled documents at their original paths. A closeout should state:

- What was actually delivered and how it differs from historical goals or designs.
- The scope of verification, checks performed and their conclusions, and checks not run or not passed.
- The clear disposition of remaining items and links to necessary evidence.

A complete log is not required; maintain current system behavior in subsystem documentation. Closed work should not take precedence over current active work, but must remain traceable; relevant navigation should point to the right sources.

Cancellation, completion, and archiving are separate decisions. Do not automatically move directories, freeze records, or delete them. If organization is necessary, preserve unique information and update references within the authorized scope; do not turn one closeout into a repository-wide cleanup. Retention and organization of notes remain governed by `decision-notes`.
