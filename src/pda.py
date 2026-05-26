"""
Pushdown Automaton simulator for nested mathematical expressions.

Project Code 93:
  - Domain (mod 10 = 3): Mathematical Expressions
  - Constraint ((code // 10) mod 5 = 4): Mixed terminal symbols with nested structures
  - Feature (mod 7 = 2): Support escaped symbols

The PDA recognizes strings whose delimiter nesting is well-formed, where
delimiters are (), [], and {} that may be mixed and nested. A backslash
escapes the next character so it is treated as a literal, not a delimiter.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Callable, Iterable, Optional


class Decision(Enum):
    ACCEPT = auto()
    REJECT = auto()
    CONTINUE = auto()


OPEN_TO_CLOSE = {"(": ")", "[": "]", "{": "}"}
CLOSE_TO_OPEN = {v: k for k, v in OPEN_TO_CLOSE.items()}
DELIMITERS = set(OPEN_TO_CLOSE) | set(CLOSE_TO_OPEN)
MATH_SYMBOLS = set("+-*/.^")
DIGITS = set("0123456789")
LETTERS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_")


class PDAState(Enum):
    Q0 = "q0"  # main scan
    Q_ESC = "q_esc"  # consumed '\', next symbol is literal
    Q_ACCEPT = "q_accept"
    Q_REJECT = "q_reject"


@dataclass
class TraceStep:
    step: int
    state: str
    remaining_input: str
    stack: list[str]
    action: str


@dataclass
class PDAResult:
    input_string: str
    decision: Decision
    trace: list[TraceStep] = field(default_factory=list)
    failure_reason: Optional[str] = None


def _is_math_char(ch: str) -> bool:
    return ch in DIGITS or ch in LETTERS or ch in MATH_SYMBOLS or ch.isspace()


@dataclass
class MathNestedPDA:
    """
    Deterministic PDA with stack alphabet {$, (, [, {}.

    Transition summary (on input from state q0):
      - opening delimiter d: push d
      - closing delimiter d: pop matching opener if stack top matches
      - '\\': enter q_esc (no stack change)
      - math / other allowed literal: no stack change
      - end of input in q0: accept iff stack == ['$']
    """

    initial_stack: str = "$"

    def reset(self) -> tuple[PDAState, list[str]]:
        return PDAState.Q0, [self.initial_stack]

    def run(self, input_string: str, trace: bool = True) -> PDAResult:
        state, stack = self.reset()
        index = 0
        steps: list[TraceStep] = []
        step_num = 0
        failure_reason: Optional[str] = None

        def record(action: str) -> None:
            nonlocal step_num
            if not trace:
                return
            steps.append(
                TraceStep(
                    step=step_num,
                    state=state.value,
                    remaining_input=input_string[index:],
                    stack=list(stack),
                    action=action,
                )
            )
            step_num += 1

        record("Start")

        while True:
            if state == PDAState.Q_ACCEPT:
                return PDAResult(input_string, Decision.ACCEPT, steps, failure_reason)
            if state == PDAState.Q_REJECT:
                return PDAResult(input_string, Decision.REJECT, steps, failure_reason)

            if state == PDAState.Q_ESC:
                if index >= len(input_string):
                    failure_reason = "Escape at end of input with no following symbol"
                    state = PDAState.Q_REJECT
                    record(failure_reason)
                    continue
                ch = input_string[index]
                index += 1
                state = PDAState.Q0
                record(f"Escape consumed; literal '{ch}' (no stack change)")
                continue

            # state == Q0
            if index >= len(input_string):
                if len(stack) == 1 and stack[0] == self.initial_stack:
                    state = PDAState.Q_ACCEPT
                    record("Input exhausted; stack empty → Accept")
                else:
                    failure_reason = (
                        f"Input exhausted with unmatched delimiters on stack: {stack[1:]}"
                    )
                    state = PDAState.Q_REJECT
                    record(failure_reason)
                continue

            ch = input_string[index]

            if ch == "\\":
                index += 1
                state = PDAState.Q_ESC
                record("Read '\\' → enter escape state")
                continue

            if ch in OPEN_TO_CLOSE:
                stack.append(ch)
                index += 1
                record(f"Read '{ch}' → push '{ch}'")
                continue

            if ch in CLOSE_TO_OPEN:
                expected_open = CLOSE_TO_OPEN[ch]
                if len(stack) < 2:
                    failure_reason = f"Closing '{ch}' with empty delimiter stack"
                    state = PDAState.Q_REJECT
                    record(failure_reason)
                    continue
                top = stack[-1]
                if top != expected_open:
                    failure_reason = (
                        f"Mismatched delimiter: expected '{OPEN_TO_CLOSE.get(top, top)}' "
                        f"but read '{ch}'"
                    )
                    state = PDAState.Q_REJECT
                    record(failure_reason)
                    continue
                stack.pop()
                index += 1
                record(f"Read '{ch}' → pop '{top}'")
                continue

            if _is_math_char(ch):
                index += 1
                record(f"Read math/literal '{ch}' → no stack change")
                continue

            failure_reason = f"Illegal symbol '{ch}' for this language"
            state = PDAState.Q_REJECT
            record(failure_reason)

    def accepts(self, input_string: str) -> bool:
        return self.run(input_string, trace=False).decision == Decision.ACCEPT


def format_trace(result: PDAResult) -> str:
    lines = [f'Input: "{result.input_string}"', ""]
    lines.append(f"{'Step':<6}{'State':<10}{'Remaining':<22}{'Stack':<20}Action")
    lines.append("-" * 80)
    for row in result.trace:
        stack_display = "".join(reversed(row.stack)) if row.stack else "ε"
        lines.append(
            f"{row.step:<6}{row.state:<10}{row.remaining_input!r:<22}"
            f"{stack_display:<20}{row.action}"
        )
    verdict = "ACCEPT" if result.decision == Decision.ACCEPT else "REJECT"
    lines.append("")
    lines.append(f"Final decision: {verdict}")
    if result.failure_reason:
        lines.append(f"Reason: {result.failure_reason}")
    return "\n".join(lines)
