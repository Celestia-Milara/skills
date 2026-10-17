# Handoff Context and Verification

Choose the following information based on relevance; this is not a mandatory field list or a checklist to complete in full every time. Link to content available in its owning source. Add only gaps that affect continuation.

| Information | When preparing a handoff | When taking over |
| --- | --- | --- |
| Goal and constraints | The specific current task, a locatable source for necessary user requirements, and session-specific constraints; state when authorization is unclear | Judge the current goal and authorization from actual user instructions; do not treat a summary as new permission or repeat approval indiscriminately |
| Design and progress | Link to applicable design, plan, status, and decisions; say which sources to read first | Read only relevant parts and check whether they have been updated, superseded, or canceled |
| Directory and changes | Actual project location; when Git applies, state repository, branch, relevant ref/SHA, staged, unstaged, and untracked content, and known ownership | Verify the actual directory and relevant changes; do not guess ownership from a path or timestamp, overwrite unknown changes, or automatically stash or create a worktree |
| Verification evidence | Checks actually run, target, scope, result, and any relevant changes made since verification; distinguish failures, not run, limitations, and pending manual checks | Decide whether evidence still applies and recheck affected areas; passing in the working tree does not prove the index version passed |
| Temporary resources | If relevant, record service, background task, temporary file, or session-tool identifier, purpose, owner, and receiving-environment constraints | Verify whether the resource is still running and accessible; old tool IDs and local paths may not work in another session; do not restart or clean up automatically |
| Open questions and action | Distinguish investigation, a decision needed, an environment blocker, and acceptance; state the next action and dependencies | Reassess prerequisites and advance independent work; do not resume canceled scope |
| Follow-up methods | When useful, suggest relevant skill names and why; do not hard-code installation paths | Verify which capabilities are actually available; do not invoke every suggested skill or repeat searches just because it was listed |

## Medium and sources

If an existing plan is sufficient, add only necessary continuity details. When there is no engineering record, a short message or separate file is also suitable; do not create a plan just to prepare a handoff. Prefer a user-specified location and project conventions. Choose a location the receiving environment can access; there is no universal requirement to use a system temporary directory.

Maintain necessary completion results, task status, and long-term rationale in their original sources and link to them from the handoff. Note when a working-state hint was verified or the related version only if that helps assess evidence. Add metadata as needed; do not require fixed date or status fields.

When linking to chat, external resources, or local files, consider whether the recipient can access them. If not, preserve the minimum needed continuation context in an authorized location and identify its source. Explicitly state information that cannot be obtained. Do not copy credentials or a complete environment dump, or upload or send material automatically as part of preparing a handoff.

## Different continuation scenarios

- **Continue the same task in another session:** Preserve the current focus, settled matters that should not be re-asked, necessary working context, and first action; do not accumulate every historical phase.
- **Switch tools or directories:** Verify that paths, resources, and references are reachable from the target environment. Do not assume the original session context or tool identifiers will carry over.
- **Parallel subtask:** State the delegated goal, boundaries, dependencies, and how results return; the original task can continue. Do not assign people or modify a shared workspace without authorization.
- **Stale or conflicting handoff:** Verify the affected sources and current state, make gaps visible, and proceed according to the current task. Do not treat the whole handoff as fact, or redo all investigation because one part is stale.
