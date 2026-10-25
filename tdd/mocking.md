# When to Mock

Adapted from Matt Pocock's similarly named reference; see [Sources and Changes](ORIGIN.md).

## Prefer System Boundaries

By default, place mocks, fakes, or stubs at system boundaries that are uncontrollable or costly: external APIs, time and randomness, the file system, and some database interactions. For database behavior, use an isolated test database when feasible and useful. Do not claim that a real database or external service has been verified based on substitute results.

Prefer allowing internal modules you control to collaborate for real. Avoid simulating an entire call chain merely to satisfy a test. Do not verify only calls to a substitute while missing the actual observable result.

This is not an absolute ban on mocking internal modules. When legacy coupling, isolation cost, or runtime constraints warrant an exception, explain the boundary, what the substitute replaces, and the verification gap. Add higher-level verification as needed. Test doubles must not hide the real mechanism this task is meant to verify.

## Dependency Injection at Boundaries

```typescript
// Easier to replace the external dependency in a test
function processPayment(order, paymentClient) {
  return paymentClient.charge(order.total);
}

// Harder to control: creates an external client internally
function processPayment(order) {
  const client = new StripeClient(process.env.STRIPE_KEY);
  return client.charge(order.total);
}
```

Reuse an existing suitable interface. Dependency injection is a technique; do not require an interface or wrapper for every function, and do not expand scope just to prepare tests.

## Operation-Specific Interfaces

```typescript
// Operations expose distinct inputs and results
const api = {
  getUser: (id) => fetch(`/users/${id}`),
  getOrders: (userId) => fetch(`/users/${userId}/orders`),
  createOrder: (data) => fetch("/orders", { method: "POST", body: data }),
};

// At a domain boundary, every test may otherwise repeat routing conditions
const genericApi = {
  fetch: (endpoint, options) => fetch(endpoint, options),
};
```

If a generic request entry point forces every test to restate routing and response shapes, consider exposing an operation-specific interface. It can clarify intent, inputs, results, and what the test double covers. This does not prohibit a generic `fetch` at the transport layer or require rewriting an existing SDK.

## Preserve Verification Boundaries

A substitute should express relevant success, failure, or timing conditions without turning unrelated implementation details into contracts. Check whether assertions would still catch an incorrect real result. Passing mocks do not mean product integration, real runtime, or target-platform behavior passed. When such evidence is needed, verify it using the project's actual approach and report limitations honestly.

Before real-service tests, verify the environment, account, data, and permitted side effects. Obtain missing authorization for charges, customer notifications, or production writes; reuse explicit authorization for the same scope.
