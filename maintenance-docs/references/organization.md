# Organization, Naming, and Sources

## Single sources of truth and default reading paths

| Default location | Content | Primary readers |
| --- | --- | --- |
| `README.md`, `docs/` | Project purpose, usage and operation, requirements and acceptance criteria, necessary architecture or design overviews | Users and project stakeholders |
| `docs/designs/<topic>.md` | Complete human-readable design deliverables: goals, scenarios, behavior, solutions, style, and unresolved items; existing projects can retain their original sources | Users and Agents carrying out later implementation |
| `.agents/subsystems/` | Current contracts, verified implementation facts, known differences, actual dependencies, and source and verification links | Development and maintenance Agents |
| `.agents/changes/` | Change records: necessary design content or links, implementation slices, dependencies, progress, open questions, and verification plans | Agents executing or continuing the work |
| `.agents/notes/` | Important settled decisions, long-term rationale, rejected options, and evidence | Agents making later decisions |
| Actual `AGENTS.md`, `CLAUDE.md`, or similar entry points | Brief project constraints, activation guidance, and navigation to real materials | Agents |

Divide materials by purpose, default reading path, and depth; do not restrict who can read them. Agents still need to read relevant requirements and acceptance criteria, and users can inspect detailed designs. Do not create a complete “human version” for every detailed document; summarize and link from necessary overviews of existing sources, and maintain interfaces, task status, and long-term rationale in their respective sources.

Use `to-docs` to create human-readable designs. An existing design can be the complete source; change records link to it and add missing execution details. Without a separate design, one change record may contain both necessary design and plan content. Maintain specific style with the design and shared standards in their owning sources; do not require a new design system.

Project entry points should link to the documentation or indexes actually used. Do not assume that ordinary files are automatically loaded because they are in an `.agents/` directory, or that a singular `AGENT.md` is automatically active. This skill package contains the detailed maintenance rules; do not duplicate the full rules in an entry point. For existing projects, prefer their current materials and actual directories rather than requiring migration. Do not create empty directories, empty pages, or placeholder fields when they are unnecessary.

## Architecture navigation and diagrams

Start from the project entry point when learning the project or locating boundaries. Before behavior changes, read relevant contracts and subsystem sources, then verify affected implementation paths. If documentation is missing, use available requirements, supported entries, and callers. Reuse verified context that still applies. By default, link one architecture source from the entry point. Links do not load their targets automatically. Do not require a new architecture page, fixed directory, or diagram when existing descriptions and navigation suffice.

Put global responsibilities, key components, external boundaries, and main data flows in the existing README or architecture overview; put local calls, state changes, and failure recovery in the relevant subsystem documentation; put proposed structures, migrations, and transitions in the relevant design or change record. Clearly distinguish current, target, and transitional states; do not describe an adopted goal as already implemented.

Diagrams should help identify boundaries, locate sources, and assess effects. Do not diagram every directory or class. When relationships are complex, split them into overview and local diagrams, with no more than 8 core nodes in a single diagram. Label the meaning of connections such as calls, data flows, or dependencies. Provide explanations and implementation links in the body so it can be used independently; do not rely solely on clickable diagram nodes. Map responsibilities to their documentation, key implementation, and tests as needed; a separate mapping table is not mandatory.

Keep a minimal diagram in the entry point only for a small, stable set of global relationships that most tasks need to understand, and link to detailed sources. Avoid maintaining the same detailed content in two places. Update diagrams and their owning documentation when relevant boundaries, main paths, or navigation changes; do not redraw them mechanically for unrelated internal refactoring, and disclose unverified areas accurately.

## File naming and splitting

Default human-readable design path: `docs/designs/<topic>.md`, using a stable English kebab-case topic. Prefer updating an existing source. Use a topic subdirectory only when multiple documents or images are needed. Saving a design does not require creating an engineering change record or adopting the engineering entry point and status requirements below.

- **Subsystems**: Use a stable English kebab-case name for the responsibility, without a date, for example `.agents/subsystems/import.md`. Divide by responsibility and behavior; see [Subsystem Documentation](subsystems.md) for details.
- **Changes**: Use a specific, stable English kebab-case topic directory for the change, for example `.agents/changes/import-resume/`. It must identify a single change; avoid broad names like `import/` or `refactor/` that accumulate unrelated tasks.
- Reuse the original directory when continuing the same change. Give a later independent change a specific name and cross-link as needed; verify scope rather than merging records only because their topics are similar.
- By default, combine the design and plan in `README.md` inside the topic directory. Add `design.md` or `plan.md` only when multiple stages need separate tracking or separate maintenance is necessary. Keep the original entry point with overall Status, a brief overview, and links; do not duplicate the full split-out content. Split based on maintenance needs, not just document length.
- Add phase or topic files only as needed; do not pre-create a full set. Update references when paths change; do not rename directories as progress changes.

```text
.agents/
  subsystems/
    import.md
  changes/
    import-resume/
      README.md
```

Change directories do not require dates. Follow existing project conventions if they use dates or task IDs. When using a date, use the record's initial creation date; do not change it as implementation progresses. A date does not represent progress or version. Add dates to body metadata only when tracking them is useful; do not require a new field. A date cannot prevent every naming collision or replace navigation to current work. Naming rules for notes remain governed by `decision-notes` and are unaffected by this section.

## Navigation and source relationships

When centralized navigation is needed, use `.agents/changes/README.md` for change links and brief topic descriptions, prioritizing work that needs to continue or be addressed. Reuse an existing entry point when it is sufficient. Do not create duplicate overall status, detailed progress, blockers, or next steps in the index; reference each change's entry point and its plan instead. Update the index as navigation needs change; do not infer status from directory names or dates.

Link to specific locations in relevant existing requirements, acceptance criteria, subsystem, and notes sources. Do not create empty links or pages to satisfy a template when no source exists. State unknowns that affect the work and investigate as needed. Designs explain how relevant behavior and constraints will be met; plans explain how they will be verified. Create mappings as needed; a traceability matrix is not mandatory. Do not reproduce full requirements, current system descriptions, or long-term rationale.

Keep a cross-subsystem change's goal and transition arrangements in one source. Each subsystem page maintains or links its current contracts, verified facts, and known differences. Shared interfaces and constraints each have one source of truth.
