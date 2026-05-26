#!/usr/bin/env python3
"""CLI for the mathematical nested-structure PDA simulator."""

import argparse
import sys
from pathlib import Path

# Allow running as script from repo root or src/
sys.path.insert(0, str(Path(__file__).resolve().parent))

from pda import MathNestedPDA, format_trace


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Simulate a Pushdown Automaton for nested mathematical expressions "
            "(mixed (), [], {} with escape support)."
        )
    )
    parser.add_argument(
        "input",
        nargs="?",
        help="Input string to validate (reads stdin if omitted)",
    )
    parser.add_argument(
        "--no-trace",
        action="store_true",
        help="Only print ACCEPT/REJECT without step-by-step trace",
    )
    parser.add_argument(
        "--examples",
        action="store_true",
        help="Run built-in acceptance/rejection examples",
    )
    args = parser.parse_args()

    pda = MathNestedPDA()

    if args.examples:
        examples = [
            ("(1+2)", True),
            ("([{3.14}])", True),
            ("a*(b+[c])", True),
            (r"x+\(y\)", True),
            ("  ", True),
            ("(1+2", False),
            ("([)]", False),
            ("(1+2))", False),
        ]
        for expr, expected in examples:
            ok = pda.accepts(expr)
            status = "OK" if ok == expected else "FAIL"
            print(f"[{status}] {expr!r} → {'ACCEPT' if ok else 'REJECT'}")
        return 0

    text = args.input
    if text is None:
        text = sys.stdin.read().strip()

    result = pda.run(text, trace=not args.no_trace)
    if args.no_trace:
        print("ACCEPT" if result.decision.name == "ACCEPT" else "REJECT")
    else:
        print(format_trace(result))
    return 0 if result.decision.name == "ACCEPT" else 1


if __name__ == "__main__":
    raise SystemExit(main())
