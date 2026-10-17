# Subsystem Documentation

## Boundaries and level of detail

Divide documentation by relatively stable shared responsibilities and runtime behavior. Aim for one page to clearly describe a related set of responsibilities, contracts, and main runtime paths. Do not map pages one-to-one to code directories, classes, or files. A subsystem can span packages or repositories.

Split out a page when a part has an independent responsibility and maintenance boundary, and a separate description would make it easier to understand or locate the effects of a change. A page is an organizational unit, not a fixed length. Do not create a page for every file, or cram several independent mechanisms into one page just because they share a broad topic. Cover only the scope relevant to the current work; do not require an inventory or full documentation of the repository first. Maintain shared interfaces and constraints in one place, and summarize and link to them from related pages.

## Content and depth

Include a clear title and responsibility scope; a Status field is not required. Content should let a future Agent locate entry points, understand responsibility boundaries, trace main runtime paths, and determine which interfaces, state, failure, and compatibility constraints a change may affect.

Describe the following as relevant:

- Responsibilities, boundaries, related subsystems, key entry points, and sources of truth.
- Main runtime paths, interactions, and state changes. Use a diagram when needed to show relationships or state transitions, label connection meanings, and provide links in the body to the owning documentation and key implementation. See [Architecture Navigation and Diagrams](organization.md#architecture-navigation-and-diagrams) for diagram ownership, detail, and entry-point exceptions.
- Interfaces, data, failure handling, recovery, compatibility, and important constraints that affect behavior decisions.
- Links to key source code, tests, and relevant notes, with a brief explanation of the mechanism, behavior covered, or decision topic.

These are content choices, not a required heading checklist. Omit what does not apply. Do not mechanically list functions, enumerate every field, or repeat code; use source links to locate local details. Reference notes for long-term rationale and keep unimplemented goals in change designs.

Distinguish source-code verification, existing test coverage, and actual runtime verification; state their relevant scope and unknowns. The existence of a test does not mean it has been run successfully, and a documentation change does not prove the implementation is correct. Verify current facts before documenting them; do not describe an approved goal, draft, or plan as implemented behavior.

## Updates and discrepancy checks

Update the owning documentation alongside verified changes to responsibilities, boundaries, main runtime paths, interfaces, state, failure or compatibility behavior, or necessary navigation; do not wait for the project to finish. Do not mechanically rewrite accurate documentation after internal refactoring. Repair broken navigation caused by file moves and similar changes. Create missing pages only as needed; do not document the entire repository just because a task has started.

When documentation and implementation disagree, check relevant source code, tests, requirements, applicable notes, and implementation status. Determine whether the discrepancy is:

- Stale or inaccurate documentation.
- Implementation that diverges from intended behavior, including a genuine defect.
- An explicit transition arrangement or incomplete implementation.

Correct verified documentation errors; address implementation errors within existing authorization. Do not rationalize a defect as a normal contract or use old documentation to overrule a new user instruction. If key behavior or a trade-off remains unclear, explain the specific conflict and ask the user to decide, while continuing work that does not depend on that decision. Handle only the scope relevant to the current task.
