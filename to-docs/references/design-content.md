# Human-Readable Design Content and Expression

## Choosing what to include

Choose from the following based on the discussion. Do not turn the list into a mandatory template:

| Content | What it helps readers assess |
| --- | --- |
| Problem, goal, and scope | Why this work matters, what it addresses, and what it does not promise |
| User or caller scenarios | Who uses it, under what conditions, and what they expect to happen |
| Key behavior and design | How normal, failure, and boundary scenarios work; how important relationships behave |
| Experience and style | How users understand and operate it, and how it aligns with existing standards |
| Constraints and related sources | Applicable compatibility, data, platform, and other limits, and where requirements, acceptance criteria, and long-term decisions live |
| Open questions and verification | What still needs a decision, investigation, or verification, and whether it affects near-term implementation |

Include technical details and diagrams needed to understand the design; do not artificially exclude technical content. Do not substitute code paths, commands, and task progress for an explanation of behavior. Reference an existing source for engineering arrangements.

## Distinguishing the status of conclusions

Clearly distinguish settled decisions, recommendations, assumptions, and open questions in the relevant paragraphs or sections. Do not require fixed labels on every paragraph or status fields across the entire document. A filename, the act of saving a document, or “documentation complete” does not imply approval, a green light to start, or completed implementation.

For example: “Settled: resumable uploads must retain valid progress from before an interruption. Open: how long that progress is retained.” If the retention period was not discussed, do not invent “seven days by default.” Scenarios explored during design can aid discussion, but label them as suggestions or examples.

You can preserve current results and open questions when discussion pauses. In-depth interviews still follow `grilling`'s shared-understanding confirmation, but settled information worth preserving need not wait until every topic is finished.

## Make the experience concrete enough to evaluate

Abstract style words can express direction, but should not be the only requirements. Add interface states, user actions, feedback, error handling, and recovery behavior as needed, and refer to existing components, styles, or sketches.

For example, “make failure messages clear” could be expanded into an open scenario: “When an import fails, show the reason and saved progress, and offer continue or exit actions.” This example does not automatically become user-approved product behavior.

Maintain styles unique to this topic in its design document. Put established cross-feature conventions for buttons, spacing, interactions, and similar concerns in an appropriate shared design source and link to it. Do not create a complete design system just because one topic needs style details.

## Sources and later feedback

The design document is a source that should be maintained, not a read-only duplicate generated from Agent documents. After the user makes changes, later tasks must read the actual file rather than rely only on an old session summary. If the design conflicts with current implementation or an applicable decision, explain the conflict and its impact. Do not automatically reject a new user request or present a recommendation as a decision reversal.

`decision-notes` owns complete rationale and rejected alternatives that need long-term retention; the design keeps a concise explanation and link needed to understand it. If adequate rationale is unavailable, say so rather than inventing history.

When engineering continuity materials are needed, `maintenance-docs` guides adding implementation arrangements to `.agents/changes/` and linking this design. Subsystem documentation owns current behavior. These materials have separate responsibilities; do not require a complete engineering duplicate for every human-readable design.