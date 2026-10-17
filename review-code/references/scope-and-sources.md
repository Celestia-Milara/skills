# Review Scope and Sources

## Determine the Target

Use the target the user actually requested. Examples include a PR, commit, revision range, selected files, or the current task's implementation. Do not assume that “review this” always means the latest commit or every change in the workspace.

When the user does not specify a target, inspect repository status, branch and base, recent history, staged and unstaged changes, and relevant untracked files. Infer the target from the task context where possible. Separate the current task's changes from unrelated work. If the target still cannot be established and the answer would change what is reviewed, ask a focused question.

Select an appropriate comparison:

| Target | Possible comparison |
| --- | --- |
| Pull request | PR changes against the actual base and head |
| One commit | Its patch and relevant surrounding context |
| Commit range | The specified endpoints |
| Current implementation | The identified set of staged, unstaged, committed, and untracked task changes |
| Specific file or behavior | Focused changes plus enough related code to assess their effect |

A merge-base-to-HEAD diff is only one option. Do not create commits, branches, or clean the workspace solely to simplify the comparison. If the selected target has no changes, report that fact accurately.

## Working-Tree and Index Versions

Identify whether relevant files are staged, unstaged, committed, or untracked. Do not infer ownership from filenames, authorship, or timestamps alone. Include new files when they are part of the requested implementation. Exclude unrelated pre-existing modifications; if attribution is unclear, report the ambiguity rather than silently reviewing them as part of the task.

If the staged content differs from the working-tree content, state which version was reviewed. Checks on one version do not automatically validate another. When relevant content changes during review, re-evaluate affected conclusions.

## Find Applicable Sources

Start from the project's actual Agent entry point. Locate and read relevant requirements and acceptance criteria, change designs or plans, subsystem documentation, coding standards, and effective decision notes. Follow links to source code, tests, and related interfaces needed to understand the target.

Use issue descriptions, commit messages, PR descriptions, and comments as context and search clues. They do not necessarily supersede explicit requirements or new user instructions. When intent sources conflict, identify the conflict and establish which is current before asserting a requirement violation. Existing code alone does not prove that its behavior is intended.

If sources are absent, stale, inaccessible, or incomplete, state the resulting limitation. Continue reviewing questions that can be answered from available requirements, contracts, and implementation evidence. Do not invent a requirement to fill a gap or skip correctness checks just because a complete specification is unavailable.

## Related Paths and Scope Boundaries

Trace only paths relevant to the target's behavior and impact, including affected callers, interfaces, persisted data, and failure handling. Cross-subsystem changes may require checking shared interfaces and constraints. Do not expand to unrelated components or unrelated legacy issues merely because they are nearby.

A finding may be located outside the diff if the target change causes or activates the problem. Explain that relationship. An old issue that the target neither introduces nor worsens is not a current finding; keep it separate if useful.
