---
name: maintenance-docs
description: "Create, verify, and maintain subsystem documentation, change designs, plans, status, and source relationships. Use when asked to organize them, when engineering context must persist, or when changes make existing materials inaccurate; not a mandatory phase for every task."
---

# Maintenance Docs

## 1. Establish responsibilities and scope

Use engineering judgment to retain useful context, verify descriptions, expose gaps, and maintain ownership and navigation. Investigate actual paths when describing current mechanisms; filling a template does not establish facts. Targeted documentation investigation does not require a separate design process.

The task Agent owns technical choices, implementation, debugging, and verification. Use `to-docs` for readable designs, `grilling` for an in-depth discussion, `decision-notes` for lasting decisions and historical search, and `handoff` when a transfer is needed. Continue settled work without reopening decisions, duplicating original sources, or adding approval gates. Search decision history when its triggers apply, even without a direct link.

Use available skills or read configured guidance through the host's supported mechanism. State inaccessible dependencies, continue independent work, and do not claim an unavailable invocation. Reuse verified context; avoid circular loading, duplicate searches, and rescanning the whole repository after a turn or skill change. Recheck affected areas when scope, premises, sources, or conflicts change.

Ordinary reading, immediate questions, and small changes that do not affect retained materials do not trigger a full maintenance process. A documentation-only request adds no permission to change product behavior, run unrelated checks, or commit; existing engineering authorization remains valid.

## 2. Locate sources and decide what to retain

Start from the actual project Agent entry point and relevant requirements, acceptance criteria, subsystems, change records, and notes. Cover shared interfaces and constraints for cross-subsystem work. Prefer existing sources and locations without mandatory migration.

Read [Organization and Sources](references/organization.md) when choosing locations, names, file splits, diagrams, or navigation. Locate the original record before continuing work; similar topics need not be the same change.

Retain designs, migration arrangements, dependencies, and open questions needed for later implementation, acceptance, or continuation, including during investigation. Small clear changes completed now may be delivered in conversation while still updating affected existing sources. Honor explicit requests to save, and do not wait until handoff to retain important context. Do not create records by line count, file count, turn, or commit, pre-create an empty library, or ask permission for every save.

## 3. Route by information ownership

Read only the references relevant to the material being maintained:

| Work | Reference and owning information |
| --- | --- |
| Choose sources, organize files, or align readable designs with engineering records | [Organization and Sources](references/organization.md): locations, navigation, source relationships, diagrams |
| Describe or correct a current subsystem | [Subsystem Documentation](references/subsystems.md): current contracts, verified implementation facts, known differences, dependencies, and verification links |
| Preserve change goals, implementation arrangements, or continuation | [Change Designs and Plans](references/changes.md): target design, gap from current state, dependencies, tasks, verification plans |
| Update status, complete, pause, cancel, resume, or close a record | [Status and Closeout](references/lifecycle.md): status meanings, task markers, completion, acceptance, remaining work |

Maintain each fact in one place; summarize and link elsewhere. A readable design can be the complete source. Engineering records supplement it only as needed; their entry-point, plan, and overall Status rules do not apply automatically to standalone designs. Notes own long-term rationale. An index provides navigation rather than a second progress record.

Distinguish settled conclusions, recommendations, assumptions, current source-code facts, test coverage, actual runtime checks, and manual acceptance. An existing test is not a successful run; adopting a goal does not implement it or remove transition and compatibility obligations.

When documents and implementation disagree, check relevant code, tests, requirements, decisions, and progress. Determine whether documentation is stale, implementation diverges, or a transition is incomplete. Correct verified documentation errors and implementation errors within authorization. Do not normalize a defect or use old documents to override a new user instruction. Ask about unresolved key behavior or trade-offs while continuing independent work.

## 4. Maintain alongside substantive changes

Update subsystem sources with verified changes to responsibilities, boundaries, runtime paths, interfaces, state, failure and compatibility behavior, or necessary navigation. Do not rewrite accurate descriptions after unrelated internal refactoring; repair broken links.

Update designs when goals, scope, choices, or premises change. Update plans when results, dependencies, blockers, or next steps affect execution; synchronize important arrangements before affected steps. Retain unresolved points and avoid a log of every tool action. Handle ordinary adjustments within authorization; ask only for decisions outside it, without reconfirming settled matters.

Before delivery, pause, or handoff, ensure retained sources expose the current state, gap from the goal, remaining work, and next action. Preserve unique information when reorganizing and keep the effort within this task.

## 5. Check and deliver

Check retention and ownership, accuracy, links, and continuation. If an engineering record exists, verify its single overall Status and task results against actual progress using the lifecycle reference. Keep blockers, evidence, gaps, and next steps locatable.

Run relevant existing checks and inspect results, or review manually if no dedicated tool exists. Do not impose a new toolchain, unrelated checks, or a full suite for documentation alone; reuse still-applicable evidence. Report unavailable, failed, unrun, or manual checks precisely. Completing a documentation task means its agreed information is accurate and usable; it does not prove implementation or acceptance.

Deliver links, substantive changes, remaining gaps, and the next action when needed. Continue feedback in the original sources. Follow project Git rules and current authorization; absent explicit commit authorization, show the checked changes and ask whether this round is ready for a local commit. Do not repeat existing authorization. Saving records or completing this task adds no push, PR, merge, or release permission.
