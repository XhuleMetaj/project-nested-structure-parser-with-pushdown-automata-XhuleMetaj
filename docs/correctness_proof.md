# Correctness Argument

## Claim

The PDA `M` in `docs/pda_design.md` accepts exactly the language `L` of strings whose mixed delimiters `()`, `[]`, `{}` are properly nested, whose non-delimiter symbols belong to the restricted math alphabet, and whose escape sequences `\x` treat `x` as literal.

## Proof sketch

### Soundness (every accepted string ∈ L)

Induction on the number of steps until acceptance.

**Invariant I:** At any step in `q0`, the stack (above `$`) is a sequence of opening delimiters that appear in the input prefix in order, and each corresponds to an unmatched opener.

- **Base:** Initially stack = `$`; no openers — holds.
- **Push:** Reading `(` `[` `{` appends the matching opener — still a valid unmatched sequence.
- **Pop:** Reading a closer removes the top only if it is the matching opener; otherwise we reject. So we never pop a non-matching symbol.
- **Escape:** In `q_esc`, one character is consumed with no stack change; delimiters in escaped form cannot affect `I`.
- **Literals:** Math characters do not alter the stack.

On acceptance, input is empty and stack = `$`, so every opener was matched — delimiter nesting is well-formed. Illegal symbols cause rejection, so accepted strings use only allowed math terminals.

Therefore every accepted string satisfies the informal semantics of `L`.

### Completeness (every w ∈ L is accepted)

Let `w ∈ L`. Process left to right:

1. Each opener in `w` triggers a push; because `w` is well-nested, when a closer appears the stack top is exactly its partner, so the PDA pops instead of rejecting.
2. Each escaped pair `\x` moves to `q_esc` and consumes `x` without stack change — legal in `L`.
3. Math characters only advance the head.
4. At end, no unmatched openers remain, so stack = `$` and the PDA enters `q_accept`.

Thus `w` is accepted.

### Rejection cases

The PDA rejects exactly when:

- a closer does not match the stack top,
- a closer appears with only `$` on stack,
- input ends with non-empty delimiter stack,
- `\` appears at end of string,
- an illegal symbol appears.

These correspond to malformed nesting, incomplete input, bad escape, or alphabet violation — i.e. strings outside `L`.

## Sample traces

Run the simulator:

```bash
python src/main.py "(1+2)"
python src/main.py "([)]"
python src/main.py --examples
```

See `docs/sample_traces.txt` for captured output of required test cases.

## Limitation (non-CFL extension)

Balanced **two-track** constraints such as `a^n b^n c^n` are not context-free. Requiring, for example, that the **total** number of `(` equals the total number of `[` globally (regardless of nesting order) would go beyond a standard bracket-matching PDA. Our design intentionally recognizes **Dyck-like** mixed nesting only.
