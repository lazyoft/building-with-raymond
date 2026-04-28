# Building with Raymond

Demo codebase for the talk **Building with Raymond ...one story at a time**.

A small e-commerce backend organized following Story-Based Architecture (SBA): every business operation lives in a single file that tells the complete story from input to mutation, with three phases — load, validate, execute.

## Layout

```
.
├── place_order.py           # use case: place an order
├── process_refund.py        # use case: refund an order
├── generate_invoice.py      # use case: generate an invoice for an order
├── cancel_order.py          # use case: cancel an order
├── domain/
│   └── vat.py               # shared VAT_RATE constant
├── external/
│   └── db.py                # in-memory data store and persistence
└── .claude/
    └── skills/sba/SKILL.md  # SBA conventions for an AI coding agent
```

## How to read it

Open any use case file at the root. The whole business logic is in one function: load all the data, validate every precondition, then execute. No layers, no repositories, no DTOs.

`.claude/skills/sba/SKILL.md` documents the conventions an AI coding agent should follow when working in this codebase.

## License

MIT — see [LICENSE](./LICENSE).
