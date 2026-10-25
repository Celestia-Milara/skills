---
name: handoff
description: "Prepare a task transfer across sessions, tools, or Agents, or verify sources and working context when taking over. Use for requested handoffs, cross-session continuation, or genuine transfer needs; not a mandatory wrap-up or new execution authorization."
---

# Handoff

## 1. Clarify the handoff goal and boundaries

Confirm who or which environment is receiving the work and what task they should continue. Reuse what is already clear. If the target is unclear, infer it from the current task first; ask only about gaps that would change the handoff scope. Do not block an explicit request to save the handoff just to fill in a recipient.

- Use this skill when the user explicitly asks for a handoff or continuation in another session, or when work genuinely needs to be transferred. The end of an ordinary phase, a general mention of “next time,” or a long context does not automatically require a separate file. Continue in the original environment, compact context, or use branches when those capabilities are sufficient.
- Keep retained project materials, status, decisions, and readable designs in their existing owning sources. A handoff selects sources and fills continuity gaps; it does not create a duplicate format, status system, or decision lifecycle.
- A handoff does not automatically end the original session, start a new session, assign people, send messages, commit, push, or publish. Follow any existing explicit authorization within its scope; merely generating, reading, or referencing handoff material does not add implementation authorization.
- Use the skill name actually available in the environment. If it cannot be invoked, read configured guidance through the host's supported mechanism; if inaccessible, state the gap and continue independent work. Do not claim an unavailable invocation. Reuse verified context that still applies.

## 2. Prepare a handoff

First locate the project entry point, actual task requirements, and relevant sources; verify the current state that affects this transfer. Update existing materials as needed within authorization. If the current task is read-only, report inaccuracies and gaps without expanding the scope of changes for the sake of a handoff.

1. **Choose sources:** Link to current requirements, applicable designs and plans, relevant implementation, and decisions. Briefly explain what each source is for. Do not copy persisted material; keep engineering status and task progress in their original sources.
2. **Add session-specific differences:** Preserve goals, constraints, authorization scope, explicit exclusions, settled conclusions, and necessary rationale that existing sources do not capture and that could affect continuation. Distinguish user requests, verified facts, inferences, and open questions. Do not invent missing rationale or copy a full discussion history.
3. **Describe the working context and evidence:** As relevant, verify the working directory, repository and branch, uncommitted changes and their known ownership, target versions or file state, subsequent relevant changes, and processes or temporary resources that still matter. Investigate only the parts that affect continuation. See [Handoff Context and Verification](references/context.md) for specific trade-offs.
4. **State the next action:** Distinguish what needs investigation, a user decision, resolution of an environment blocker, or acceptance. Link to specific plan items rather than copying a task list. State the first actionable step and its prerequisites; do not present rejected candidates or canceled work as authorized next steps.

Choose the smallest useful medium: a requested location, an existing task record, or a short message. Create a separate file only when useful; follow project locations rather than defaulting to a system temporary directory. Read the [delivery example](references/example.md) when a complete handoff example would help. Do not require a change record or pre-create a handoff directory.

When delivering a file, ensure the receiving environment can access it and its linked sources. Resolve relative links from the file's location and verify their targets. If temporary or local materials may be inaccessible, say so and, within authorization, choose a durable accessible location. Do not claim delivery if the file has not been shared. Do not pass the body by embedding it in a shell command.

## 3. Take over and continue

1. Use the actual user request and project entry point to confirm the goal, constraints, and permissions. A reported authorization in a handoff is not a substitute for its real source and does not automatically add permissions. Carry forward visible, applicable authorization without asking again about settled matters. If a concrete action lacks a necessary basis, address that gap only and continue independent work.
2. Read the sources needed for this task and verify that the goal remains current and that the workspace and relevant context have not changed. Old statements such as “done,” “passed,” or “still running” describe a point in time. Recheck only what could affect the current action; do not rescan everything or rerun all checks by default.
3. Reuse conclusions and evidence that still apply. When conflicts or changes appear, investigate the affected area and update the owning source within authorization; preserve unresolved points honestly. Proceed according to current instructions and verified facts, not an old summary that contradicts the current situation or a new request.
4. Choose an actionable step and continue authorized work. If the task is completed, canceled, or superseded by a new goal, an old handoff's next step no longer drives execution. Resume paused work based on the current request and conditions; do not restart it merely because unfinished items remain.

## 4. Review and deliver

- The recipient can locate the task goal, necessary sources, constraints, gaps, and first action. The handoff is specific to this continuation and has no duplicated prose or fixed-form placeholders.
- Current facts, historical records, assumptions, and open questions are clear. Completion, verification, and acceptance are described separately. Evidence identifies its target and scope, and later changes are not hidden.
- Links and delivery methods work in the receiving environment. Do not include secrets, tokens, passwords, or unnecessary personal information. Diagnostics may retain variable names and safe locating details.
- Uncommitted changes, temporary resources, and unknown ownership are described when they could affect continuity. Do not automatically clean up, initialize repositories, or manufacture a clean workspace.
- Do not add handoff approval, plan approval, or commit steps. Maintain original sources according to their rules. Update an old handoff as needed or mark it superseded; do not create another overall status system.

When preparing a handoff, provide the actual file or message and a suggested next step, accurately stating whether it was merely saved or actually delivered under authorization. When taking over, report changes that affect the work and continue execution rather than stopping at a summary. Saving a handoff does not prove that the next task has been executed or the transfer completed.
