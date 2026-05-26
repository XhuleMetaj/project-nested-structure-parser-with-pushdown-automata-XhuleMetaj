"""Tests for the mathematical nested-structure PDA."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pda import Decision, MathNestedPDA  # noqa: E402


class TestMathNestedPDA(unittest.TestCase):
    def setUp(self) -> None:
        self.pda = MathNestedPDA()

    def test_accept_simple_paren(self) -> None:
        self.assertTrue(self.pda.accepts("(1+2)"))

    def test_accept_deep_mixed_nesting(self) -> None:
        self.assertTrue(self.pda.accepts("([{3.14}])"))

    def test_accept_mixed_operators(self) -> None:
        self.assertTrue(self.pda.accepts("a*(b+[c])"))

    def test_accept_escaped_delimiters(self) -> None:
        self.assertTrue(self.pda.accepts(r"x+\(y\)"))

    def test_accept_empty_and_whitespace(self) -> None:
        self.assertTrue(self.pda.accepts(""))
        self.assertTrue(self.pda.accepts("  "))

    def test_reject_incomplete(self) -> None:
        result = self.pda.run("(1+2")
        self.assertEqual(result.decision, Decision.REJECT)
        self.assertIsNotNone(result.failure_reason)

    def test_reject_wrong_nesting_order(self) -> None:
        self.assertFalse(self.pda.accepts("([)]"))

    def test_reject_extra_closing(self) -> None:
        self.assertFalse(self.pda.accepts("(1+2))"))

    def test_reject_illegal_symbol(self) -> None:
        self.assertFalse(self.pda.accepts("(1@2)"))

    def test_trace_records_steps(self) -> None:
        result = self.pda.run("()", trace=True)
        self.assertEqual(result.decision, Decision.ACCEPT)
        self.assertGreaterEqual(len(result.trace), 3)


if __name__ == "__main__":
    unittest.main()
