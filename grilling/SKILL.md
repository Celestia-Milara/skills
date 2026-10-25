---
name: grilling
description: "Stress-test a plan, decision, or idea through focused questions in rounds. Use for requests such as 'grill me on this plan' or '帮我质询这个方案'; explore material risks within the agreed scope."
---

Stress-test the agreed topic until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it. Preserve the depth of the interview without expanding beyond the user's scope. If the user explicitly wants exhaustive questioning, explore every relevant branch; otherwise focus on material decisions and risks.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask a manageable batch of the highest-impact frontier questions: number each question and give your recommended answer. Keep the remaining questions visible as deferred topics, then wait for answers before advancing dependent questions. Do not force the whole frontier into one round.

Format a round like so:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Investigate discoverable _facts_ yourself. Delegate when useful, available, and authorized; otherwise use the host's available tools directly. If a fact cannot be accessed, state the gap and ask only for information the user must supply. A running investigation is an unsettled prerequisite: continue independent questions while dependent ones wait.

Ask the user to settle product behavior, scope, and key trade-offs that remain unclear. Handle routine engineering details within existing authorization and explain relevant assumptions; do not turn every implementation choice into an interview question or reopen settled decisions.

Finish when material questions in the agreed scope are resolved, or when the user stops, defers, or narrows the discussion. Summarize the shared understanding and retain open questions and their consequences. Confirm shared understanding before implementing the resulting design; reuse an explicit confirmation already given. Saving settled conclusions and unresolved items does not need to wait for that confirmation and adds no implementation authorization.
