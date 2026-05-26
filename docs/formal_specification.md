# Formal Language Specification

**Project:** Nested Structure Parser with Pushdown Automata  
**Repository:** `project-nested-structure-parser-with-pushdown-automata-XhuleMetaj`  
**Student:** Xhule Metaj  
**Project Code:** 93

| Derived parameter | Formula | Value |
|-------------------|---------|-------|
| Domain | 93 mod 10 | 3 — Mathematical Expressions |
| Constraint | (93 ÷ 10) mod 5 | 4 — Mixed terminal symbols with nested structures |
| Feature | 93 mod 7 | 2 — Support escaped symbols |

## 1. Topic statement

We model a **restricted subset** of mathematical expression syntax whose **delimiter nesting** is well-formed. The language includes:

- Mixed grouping symbols: parentheses `()`, square brackets `[]`, and curly braces `{}`
- Typical math terminals: digits, identifiers, operators `+ - * / .`, and whitespace
- **Escaped symbols:** a backslash `\` makes the next character literal (it does not open/close nesting)

We deliberately **do not** parse full operator precedence, type checking, or complete real-world math grammars. The focus is **context-free nesting** recognized by a PDA.

## 2. Alphabet Σ

| Category | Symbols |
|----------|---------|
| Open delimiters | `(`, `[`, `{` |
| Close delimiters | `)`, `]`, `}` |
| Escape | `\` |
| Digits | `0`–`9` |
| Letters | `a`–`z`, `A`–`Z`, `_` |
| Operators | `+`, `-`, `*`, `/`, `.`, `^` |
| Whitespace | space, tab (single-space class in implementation) |

Any other character is **rejected**.

## 3. Informal semantics

1. **Delimiter matching:** Each closing delimiter must match the most recent unmatched opening delimiter of the same kind. Mixed nesting such as `([{}])` is allowed when properly matched.
2. **Math content:** Characters that are not delimiters (and not introduced by escape) may appear freely between delimiters.
3. **Escape:** If `\` is read, the **next** symbol is consumed as a literal and does not affect the stack (e.g. `\(`, `\)`, `\[`, `\\`).
4. **Empty input:** The empty string is accepted (no unmatched delimiters).

## 4. Sample strings

### Valid (accept)

| String | Notes |
|--------|-------|
| `(1+2)` | Simple parentheses |
| `([{3.14}])` | Deep mixed nesting |
| `a*(b+[c])` | Mixed delimiters with operators |
| `x+\(y\)` | Escaped parentheses inside expression |
| `` (empty) | Boundary: no delimiters |

### Invalid (reject)

| String | Reason |
|--------|--------|
| `(1+2` | Unclosed `(` |
| `([)]` | Mismatched closing `]` vs `[` |
| `(1+2))` | Extra `)` |
| `(1@2)` | Illegal symbol `@` |

## 5. Context-free grammar (CFG)

Non-terminals: `S` (start), `E` (expression body inside delimiters).

```
S  → ε | T S
T  → ( S ) | [ S ] | { S } | L
L  → M L | ε
M  → digit | letter | op | ws | ESC
ESC → \ ( | \ ) | \ [ | \ ] | \ { | \ } | \ \
```

**Notes:**

- `T S` allows concatenation of delimiter groups and literal math segments.
- `ESC` productions implement **Feature 2** (escaped symbols).
- Parentheses/brackets/braces model **Constraint 4** (mixed nested terminals).

This CFG is context-free; a single-stack PDA suffices for delimiter nesting.

## 6. Non-context-free extension (limitation)

Requiring **equal counts of two delimiter types at the same nesting level** without a stack marker between them (e.g. “same number of `(` and `[` before any close”) across the whole string is not captured by a single CFG/PDA without enriching the model. Our project stays within standard Dyck-style matching extended to three bracket types.
