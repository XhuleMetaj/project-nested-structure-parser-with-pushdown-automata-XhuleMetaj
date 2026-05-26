# Nested Structure Parser with Pushdown Automata

**CEN 350 — Theory of Computation**  
**Author:** Xhule Metaj  
**Project Code:** 93

| Parameter | Value |
|-----------|-------|
| Domain (93 mod 10) | Mathematical Expressions |
| Constraint ((93÷10) mod 5) | Mixed terminal symbols with nested structures |
| Feature (93 mod 7) | Support escaped symbols |

## Overview

This repository models a restricted language of **mathematical expressions** whose **mixed delimiters** `()`, `[]`, and `{}` must be properly nested. A backslash `\` escapes the next character so it is treated as a literal (not as a delimiter).

Deliverables include:

- Formal language definition and CFG (`docs/formal_specification.md`)
- PDA design with state diagram and transition table (`docs/pda_design.md`)
- Correctness argument (`docs/correctness_proof.md`)
- **Option B** implementation: Python PDA simulator with step-by-step traces (`src/`)

## Quick start

```bash
# Run built-in acceptance/rejection examples
python3 src/main.py --examples

# Validate one expression with full trace
python3 src/main.py "(1+2)*[a+b]"

# Validate with escaped delimiters
python3 src/main.py 'x+\(y\)'

# Run tests
python3 -m unittest discover -s tests -v
```

## Project structure

```
├── README.md
├── docs/
│   ├── formal_specification.md
│   ├── pda_design.md
│   ├── correctness_proof.md
│   └── sample_traces.txt
├── src/
│   ├── pda.py      # PDA simulator
│   └── main.py     # CLI
└── tests/
    └── test_pda.py
```

## Required test cases (summary)

| Input | Expected |
|-------|----------|
| `(1+2)` | Accept |
| `([{3.14}])` | Accept |
| `a*(b+[c])` | Accept |
| `x+\(y\)` | Accept |
| `` | Accept |
| `(1+2` | Reject |
| `([)]` | Reject |
| `(1+2))` | Reject |

## References

Course project guide: *Nested Structure Parser with Pushdown Automata* (CEN 350).
