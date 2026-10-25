# Change Records: Design and Plans

## Responsibilities and Content

A change record retains the context needed to carry out one identifiable change. Design content explains its target, current gap, affected subsystems, and transition arrangements. Plan content explains work units, dependencies, progress, and verification. Subsystem documentation owns current behavior; notes own long-term rationale.

The change entry point, README, plan, and overall Status rules in this file apply to engineering change records that require ongoing maintenance. When creating or maintaining only a human-readable design, do not require an engineering record or add engineering progress status; keep settled, recommended, and unresolved design content distinct from work progress.

If an existing design owns the goals, behavior, and solution, link to it. Add only missing execution, migration, verification, and progress details to the change record. When no separate design exists and a split has no maintenance value, keep necessary design and plan content in one change record. Do not create a second file just to satisfy a document category.

Before authorized implementation, verify the design against current source, constraints, and notes. Carry forward valid conclusions; keep unresolved recommendations distinct from decisions. Reading or saving a design adds no implementation authorization. Revise the owning design when it changes; a change record must not silently override it.

An engineering change entry must have a title, an overall `Status`, and a clear statement of the goal and scope. By default, combine the design and plan in `README.md`; split them only when needed, following [Organization Rules](organization.md) and keeping the entry point and links intact. Maintain status only at the entry point. See [Status and Closeout](lifecycle.md) for status meanings and completion rules.

Choose sections based on actual content; a complete template is not required. Link to specific locations in relevant requirements, acceptance criteria, subsystem documentation, and notes. Do not duplicate complete sources or create empty pages and placeholder fields. Add metadata such as dates, owners, or priority only when useful.

## Design Content

1. Reference requirements and acceptance criteria, current subsystem documentation, and applicable decisions. Briefly state the goal, scope, and gap from the current state.
2. Describe the target design and identify intended changes to behavior, interfaces, state, or data, including cross-subsystem effects. Add migration, compatibility, failure-handling, and recovery arrangements as relevant; these are not required for every change.
3. Distinguish settled conclusions from undecided recommendations, assumptions, and questions to investigate or verify. Keep unresolved comparisons in the design. Record settled rationale with long-term value in its notes source according to `decision-notes`, then summarize and reference it in the design.
4. Define the implementation scope well enough to support task breakdown and verification without requiring a later Agent to guess key behavior or trade-offs. The Agent can handle remaining engineering details autonomously. Do not prewrite every function or file change, or require a fixed number of candidates.

During investigation, retain unresolved items; a fully implementable solution is not required before creating a record. Reference and carry forward conclusions that still apply rather than reconfirming them merely because they are being documented. An adopted goal does not mean it has been implemented, and a new goal does not automatically remove current compatibility obligations.

## Plan Content and Detail

Reference the target design and acceptance sources in the plan. Break work into units with verifiable outcomes instead of mechanically splitting by tool operation, function, or commit.

- For each item, state its expected result, necessary dependencies and ordering, and verification method. Tasks may depend on earlier items and do not each need independent end-to-end acceptance; verification methods do not have to require new tests.
- Describe near-term tasks in enough detail to act on directly. Keep later work directional and refine it as investigation proceeds; do not prewrite every file change and command for the entire effort.
- For investigations and experiments, state the question to resolve and expected output, preserving genuine uncertainty.
- Record actual completion, remaining work, blockers, next steps, concise verification conclusions that support continuation, and necessary evidence. Do not copy complete logs or conversations, or duplicate the design and long-term rationale.
- Distinguish code changes, successful verification, and pending manual acceptance. Do not mark checks complete if they were not run. Tasks default to incomplete/complete checkboxes; describe other states in text as needed. See [Status and Closeout](lifecycle.md) for specific criteria.

For example, a task result could say “implemented checkpoint persistence and verified it can be read after an interruption,” rather than merely “edited the file and added a function.” Record actual results and evidence only after they exist; do not present expected outcomes as verified.

## Updates and Continuation

Promptly update the design when goals, scope, key choices, or premises clearly change; unresolved items remain unresolved. Update the plan when task results, dependencies, blockers, or next steps change in a way that affects execution or continuation. Synchronize important arrangements before executing affected steps; do not log every tool operation.

Handle adjustments within existing authorization autonomously. Documentation updates do not add approval requirements and cannot replace necessary user decisions. Obtain a decision before changing behavior, scope, or key trade-offs beyond existing authorization; do not reconfirm settled matters.

Before delivery, pausing, or handoff, verify that relevant records to be retained let the next Agent identify the current state, gap from the goal, remaining work, and next step. Do not wait until then to create the first record or write a complete duplicate for a new session. Synchronize verified implementation changes to their subsystem sources, maintain long-term decisions according to their rules, and use indexes only for navigation.
