---
name: SBA
description: Story-Based Architecture conventions for this codebase. Apply when implementing or refactoring use cases.
---

# Story-Based Architecture

This codebase follows Story-Based Architecture. Every business operation is a self-contained narrative living in a single file. Apply these principles strictly.

## Three-act structure

Every use case follows the same pattern:

```python
def use_case(args):
    # 1. Load: gather all data needed upfront
    ...
    # 2. Validate: check every precondition before any mutation
    ...
    # 3. Execute: perform calculations and mutations
    ...
```

Load everything first, validate everything, then mutate. No interleaving unless there is a performance justification.

## Operational transparency

The behavior of a use case must be visible by reading only that file. Avoid:

- Hidden side effects (signals, hooks, callbacks at distance).
- Methods that hide computation. Simple methods belongs inline. Do not extract them into helper methods.
- Inheritance, decorators, metaclasses, or any indirection that obscures flow.

## Intentional redundancy

Two use cases that look similar might serve different business purposes. Keep them separate. Similar code is not duplication when it can evolve independently.

Sandi Metz: "Duplication is far cheaper than the wrong abstraction."

## Minimal abstraction for DRY-knowledge

DRY applies to knowledge, not to code. Hunt and Thomas: "Every piece of knowledge must have a single, unambiguous, authoritative representation."

When something is genuinely shared across use cases, share only the bare minimum and do not over generalize. Keep the boundaries of what is shared minimal in order to avoid dependencies and abstractions that will make the code harder to read.

## Naming for intent

Files are named after the business operation they perform: `place_order.py`. Not `OrderHandler.py` or `OrderService.py`. Open the file, see the story.

## Implementing a new use case

1. Create a file named after the operation.
2. Write a single function that follows the three-act structure. Do not put comments in there explaining the structure, the code should be self-evident.
3. Import only what you need from the external files and shared constants.
4. Keep everything inline and visible unless there is inherent complexity which might benefit from a private function for readability. Use private functions only for complex calculations, never for simple ones. If you find yourself writing a private function for something simple, keep it inline instead.
5. Do not introduce dataclass requests/responses, helper classes, or private helpers unless the existing codebase already uses them.

## Refactoring duplication

1. Identify whether what is duplicated is knowledge or code.
2. Share only knowledge, in a small module. Put that under the `domain` folder. Use a meaningful filename. It is ok to reuse the same filename if the knowledge falls in the same domain. For example, if you have two use cases that need to share the same business rules for calculating discounts, you can create a `domain/discounts.py` file and put the shared logic there.
