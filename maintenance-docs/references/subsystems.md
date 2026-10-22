# Subsystem Documentation

## Boundaries and level of detail

Organize pages by stable responsibilities and runtime behavior. A page can describe several code modules; a subsystem can span packages or repositories. Page layout does not establish implementation boundaries. Do not create a page for each directory, class, or file.

Split pages when distinct responsibilities need separate maintenance and navigation. Do not combine unrelated mechanisms because they share a broad topic. Cover the current task's scope without first documenting the whole repository. Keep each shared interface or constraint in one source; link to it elsewhere.

When assessing boundaries, identify internal choices that can change independently and the state invariants each module maintains. Check who can change that state and through which entries. Multiple writers need clear coordination rules. Use these questions to investigate the project, not to impose a new architecture.

## Content and depth

Give the page a clear title and scope; a Status field is optional. Help readers locate entries, trace runtime paths, and judge effects on interfaces, state, failures, and compatibility.

Distinguish current contracts, verified implementation facts, and known differences between them. A contract states observable behavior that callers can rely on and the conditions they must meet. Keep future goals and transition arrangements in their design sources; an adopted goal does not remove current obligations.

Describe the following as relevant:

- Responsibilities, supported entries, known callers, related subsystems, and sources of truth.
- Calling conditions: input, authorization, initialization, ordering, concurrency, or transaction requirements.
- Success and failure semantics: completed effects, possible partial completion or unknown results, recovery, and safe retry conditions.
- State ownership and relevant invariants: idempotency scope and duration, ordering, cancellation, data formats, and compatibility.
- Actual dependencies and exceptions: direct storage access, shared state, event timing, configuration assumptions, or common transactions. Link their locations and explain their effects. An undocumented dependency still matters; recording it does not make it a permanent contract.
- Internal structure, main runtime paths, interactions, state changes, and key source links. Use diagrams when relationships need them. Label connections and provide source links in the text; see [Architecture Navigation and Diagrams](organization.md#architecture-navigation-and-diagrams).
- Verification entries, the key promises they check, and important coverage gaps. Link relevant notes for lasting rationale.

Select content by actual risk; these items are not required headings. Do not promise details that callers do not need. Omit irrelevant items rather than listing every function or field. Link existing type, protocol, or contract sources instead of copying them.

Verify current facts before recording them. Distinguish source inspection, existing tests, and actual runtime checks. Explain their scope and unknowns; a test's existence does not prove a successful run. Keep version-specific run results with the task's evidence. A documentation update does not prove implementation correctness.

## Updates and discrepancy checks

Update affected sources alongside verified changes to contracts, responsibilities, runtime paths, state, failure behavior, compatibility, or navigation. Do not wait for project completion. Keep accurate descriptions after unrelated internal refactoring, repair broken links, and create missing pages only as needed.

When contracts, documentation, and implementation disagree, check relevant code, tests, requirements, decisions, and transition status. Determine whether the difference is:

- Stale or inaccurate documentation.
- Implementation that diverges from intended behavior, including a genuine defect.
- An explicit transition arrangement or incomplete implementation.

Correct verified documentation errors and address implementation defects within existing authorization. Keep an effective promise visible when implementation violates it; record the known difference instead of redefining the promise. Do not use old documentation to overrule a new user instruction. Ask about unresolved key behavior or trade-offs while continuing independent work within scope.
