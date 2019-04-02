from unittest import TestCase

from funky.parse import FunkySyntaxError
from funky.parse.fixity import resolve_fixity
from funky.corelang.sourcetree import FunctionApplication, InfixExpression, \
                                      UsedVar, Literal

class TestFixity(TestCase):

    def test_valid_fixity(self):
        test_fixities = {
            InfixExpression([Literal(10), "+", Literal(10)]) : FunctionApplication(FunctionApplication("+", Literal(10)), Literal(10)),
            InfixExpression([Literal(1), "+", Literal(2), "*", Literal(3)]) : FunctionApplication(FunctionApplication("+", Literal(1)), FunctionApplication(FunctionApplication("*", Literal(2)), Literal(3))),
            InfixExpression(["-", UsedVar("x"), "+", Literal(2)]) : FunctionApplication(FunctionApplication("+", FunctionApplication("negate", UsedVar("x"))), Literal(2)),
            InfixExpression(["-", Literal(5)]) : FunctionApplication("negate", Literal(5)),
            InfixExpression(["-", Literal(5), "+", Literal(5)]) : FunctionApplication(FunctionApplication("+", FunctionApplication("negate", Literal(5))), Literal(5)),
            InfixExpression([Literal(1), "+", Literal(2), "**", Literal(6)]) : FunctionApplication(FunctionApplication("+", Literal(1)), FunctionApplication(FunctionApplication("**", Literal(2)), Literal(6))),
        }

        for test, expected in test_fixities.items():
            app = resolve_fixity(test)
            self.assertEqual(repr(app), repr(expected))

    def test_associativity(self):
        associativity_tests = {
            InfixExpression([Literal(1), "+", Literal(1), "+", Literal(1)]) : FunctionApplication(FunctionApplication("+", FunctionApplication(FunctionApplication("+", Literal(1)), Literal(1))), Literal(1)),
            InfixExpression([Literal(1), "*", Literal(1), "*", Literal(1)]) : FunctionApplication(FunctionApplication("*", FunctionApplication(FunctionApplication("*", Literal(1)), Literal(1))), Literal(1)),
            InfixExpression([Literal(1), "**", Literal(1), "**", Literal(1)]) : FunctionApplication(FunctionApplication("**", Literal(1)), FunctionApplication(FunctionApplication("**", Literal(1)), Literal(1))),
            InfixExpression([Literal("test"), "++", Literal("test"), "++", Literal("test")]) : FunctionApplication(FunctionApplication("++", Literal("test")), FunctionApplication(FunctionApplication("++", Literal("test")), Literal("test")))
        }

        for test, expected in associativity_tests.items():
            app = resolve_fixity(test)
            self.assertEqual(repr(app), repr(expected))

    def test_nonfix(self):
        nonfix_tests = [
            InfixExpression([Literal(1), "<", Literal(1), "<", Literal(1)]),
            InfixExpression([Literal(1), "<=", Literal(1), "<=", Literal(1)]),
            InfixExpression([Literal(1), "==", Literal(1), "==", Literal(1)]),
            InfixExpression([Literal(1), ">", Literal(1), ">", Literal(1)]),
            InfixExpression([Literal(1), ">=", Literal(1), ">=", Literal(1)]),
        ]

        for test in nonfix_tests:
            with self.assertRaises(FunkySyntaxError):
                resolve_fixity(test)

    def test_invalid_negation(self):
        invalid_negations = [
            InfixExpression([UsedVar("x"), "+", "-", Literal(2)]),
            InfixExpression([UsedVar("x"), "-", "-", Literal(4)]),
            InfixExpression(["-", UsedVar("x"), "-", "-", Literal(4)]),
        ]

        for test in invalid_negations:
            with self.assertRaises(FunkySyntaxError):
                resolve_fixity(test)
