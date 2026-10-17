# Good and Bad Tests

Adapted from Matt Pocock's similarly named reference; see [Sources and Changes](ORIGIN.md). Examples illustrate methods. The actual API and test framework depend on the project; these examples are not mandatory and do not require adding tools.

## Good Tests

**Integration-style:** Verify behavior that matters to users or callers through a real interface, without mocking the internal implementation.

```typescript
// GOOD: observes the promised checkout result
test("user can checkout with valid cart", async () => {
  const cart = createCart();
  cart.add(product);
  const result = await checkout(cart, paymentMethod);
  expect(result.status).toBe("confirmed");
});
```

The public boundary may be a module API; not every test needs to start the full application. Each test should focus on a recognizable behavioral result. It may have several assertions that together prove that result; do not split tests mechanically by assertion count.

Test names should describe **WHAT**, not internal **HOW**. When implementation is refactored without changing the contract, tests should remain useful where possible.

## Implementation-Coupled Tests

```typescript
// BAD when the internal call is not itself a contract
test("checkout calls paymentService.process", async () => {
  const mockPayment = jest.spyOn(paymentService, "process");
  await checkout(cart, payment);
  expect(mockPayment).toHaveBeenCalledWith(cart.total);
});
```

This test may prove only that an internal method was called, not that checkout succeeded. Other warning signs include tests of private methods, many mocks of internal collaborators, assertions about non-contract calls or their order, and tests that break when only internal structure changes.

If call counts, event order, or idempotent side effects are themselves promises—for example, “a retry must not charge twice”—verify the actual contract. Do not treat the warning signs above as absolute prohibitions.

## Observe Through the Relevant Boundary

```typescript
// BAD for a user-creation API contract: bypasses its retrieval interface
test("createUser saves to database", async () => {
  await createUser({ name: "Alice" });
  const row = await db.query("SELECT * FROM users WHERE name = ?", ["Alice"]);
  expect(row).toBeDefined();
});

// GOOD: verifies caller-visible behavior
test("createUser makes user retrievable", async () => {
  const user = await createUser({ name: "Alice" });
  const retrieved = await getUser(user.id);
  expect(retrieved.name).toBe("Alice");
});
```

If the test subject is the storage adapter, migration, or persistence-format contract, checking database records may be the right boundary. First identify the obligation being protected: do not omit tests to avoid testing internals, and do not expose a new production interface just to assert something.

## Independent Expected Values

```typescript
// BAD: repeats the implementation's likely algorithm
test("calculateTotal sums line items", () => {
  const items = [{ price: 10 }, { price: 5 }];
  const expected = items.reduce((sum, item) => sum + item.price, 0);
  expect(calculateTotal(items)).toBe(expected);
});

// GOOD: independently known result
test("calculateTotal sums line items", () => {
  expect(calculateTotal([{ price: 10 }, { price: 5 }])).toBe(15);
});
```

Independent evidence can come from a specification, a verified example, a manual calculation, or an independently reliable implementation. A literal value also needs a real basis; copying current output into a constant does not make it independent verification. Check that snapshots and large examples express the intended behavior.

## Fail for the Intended Reason

A valid red must fail because the target behavior is missing or incorrect. First confirm that the test actually ran, that its input reached the target path, and that the assertion can distinguish the failure. Environment errors, empty matches, skips, or assertions that only verify mock setup are not evidence of the target failure.

A regression test should correspond to the original trigger condition and pass after the fix. If you did not verify that the original defect is caught, say so honestly; do not claim regression protection solely because a test exists. Do not change the expected result to something wrong just to produce a red.