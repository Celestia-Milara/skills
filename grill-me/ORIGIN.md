# Source and Local Adaptation

- Repository: [mattpocock/skills](https://github.com/mattpocock/skills).
- Pinned commit: `c55ee46073ed923f86ce59a5eb3b6d895095d1b7`.
- Original directory: [skills/productivity/grill-me](https://github.com/mattpocock/skills/tree/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/productivity/grill-me).
- Original entry: [SKILL.md](https://github.com/mattpocock/skills/blob/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/productivity/grill-me/SKILL.md).
- Copyright (c) 2026 Matt Pocock. The complete [MIT LICENSE](LICENSE), including the copyright and permission notices, is retained with this package.

The local entry replaces the upstream instruction to call the `Skill` tool with a host-compatible loading rule for the installed `grilling` dependency: use `Skill` when available; otherwise locate and read `grilling/SKILL.md`. A sibling path is only a candidate when it exists. Missing or inaccessible dependencies must be reported before stopping. The frontmatter is unchanged, and the interview instructions remain in `grilling` rather than being copied into this entry. The Chinese backup translates this loading rule and these adaptation notes while retaining the original frontmatter and complete MIT license.

The initial adaptation was checked against the pinned public Git tree, source text, local metadata, and static paths. It did not include installation or execution. Later discovery and invocation smoke checks are described in the repository's [dated verification record](https://github.com/Celestia-Milara/skills/blob/261837205cf3a5afcefebae2f8468758283ed1f3/README.md#verified-host-behavior). Those checks do not establish complete writing workflows or general effectiveness.
