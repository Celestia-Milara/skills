# Sources and Local Adaptation

This directory contains a local adaptation of Matt Pocock's TDD skill, not an unmodified upstream copy.

- Repository: [mattpocock/skills](https://github.com/mattpocock/skills)
- Pinned commit: `c55ee46073ed923f86ce59a5eb3b6d895095d1b7`
- Original directory: [skills/engineering/tdd](https://github.com/mattpocock/skills/tree/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/engineering/tdd)
- References: [SKILL.md](https://github.com/mattpocock/skills/blob/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/engineering/tdd/SKILL.md), [tests.md](https://github.com/mattpocock/skills/blob/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/engineering/tdd/tests.md), [mocking.md](https://github.com/mattpocock/skills/blob/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/engineering/tdd/mocking.md)
- Copyright: Copyright (c) 2026 Matt Pocock. The complete [MIT LICENSE](LICENSE) is retained with this package.

## Methods retained

Verify behavior through public boundaries, use independently grounded expected values, and avoid implementation-coupled or circular assertions. Advance one behavioral test and the smallest implementation step at a time through red → green rather than writing all tests in advance. Prefer test doubles at system boundaries and retain the main teaching value of the upstream positive and negative examples.

## Main changes

- Rewrote the entry point and guidance in English, retained the TypeScript examples, and replaced the metadata with a local description.
- Make TDD optional by task; do not force test-first work for requests limited to integration testing or require tests, plans, or documents for every small change.
- Let the Agent choose ordinary test boundaries within settled behavior and authorization. Removed unconditional prior approval of test boundaries; ask the user only when behavior, scope, or key trade-offs are unclear.
- Locate evidence through actual project entry points, requirements, subsystems, and `decision-notes`. Do not require CONTEXT.md, a new ADR, or `codebase-design`; use `maintenance-docs` for persistence without copying its detailed formats and status rules.
- Allow necessary small refactors while green instead of uniformly deferring them until review; a behavior can have multiple assertions that jointly prove it.
- Add checks that red and green actually ran, that the failure reason is valid, that regression tests are discriminating, that tests added after implementation are labeled honestly, and that other people's changes are not overwritten.
- Make “mock only system boundaries” a default rather than an absolute rule; allow justified exceptions and address storage contracts or call ordering that are themselves behavior.
- Add impact-based verification, distinctions among tests, builds, and real runtime, accurate review scope for the actual workspace, honest reporting of gaps, and the established commit-confirmation boundary. Do not mandate a full test suite, a fixed number of sub-agents, or automatic commits.

The package's runtime guidance is self-contained. It works with other skills using names actually available in the environment and project entry points; it does not hard-code installation paths or depend on design discussions in this skill repository. Public-page reading was used to check the upstream text; upstream code was not run, and model behavior was not evaluated.