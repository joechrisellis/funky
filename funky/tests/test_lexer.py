from unittest import TestCase

from ply.lex import LexToken
from funky.parse import FunkyLexingError
from funky.parse.funky_lexer import FunkyLexer, IndentationLexer

class TestFirstPass(TestCase):

    def test_valid_first_pass(self):
        """Does the first pass lexer work?"""
        lexer = FunkyLexer()
        lexer.build()

        tests = {
            """
module valid with
    main = 10 + 10""" : ["module", "valid", "with", 4, "main",
                         "=", 10, "+", 10], # <- basic lex test

            """
module comments with # this is a comment
    # commented line
    main = 10 # comment! ###""" : ["module", "comments", "with", 4, "main",
                                   "=", 10], # <- are comments removed?
            
            """
module whitespace          with
    f x = 10 + x



    main =    f    10""" : ["module", "whitespace", "with", 4, "f", "x", "=",
                            10, "+", "x", 4, "main", "=", "f", 10],
            
            """
module strings with

    main = "string1" ++ "string2" """ : ["module", "strings", "with", 4,
                                         "main", "=", "string1", "++", "string2"]
        }

        # For each test, lex it and extract the values of all of the tokens.
        # It should always equal what we expect.
        for test, expected in tests.items():
            tokens = lexer.do_lex(test)
            values = [t.value for t in tokens]
            self.assertEqual(expected, values)

    def test_invalid_first_pass(self):
        lexer = FunkyLexer()
        lexer.build()
        invalid = ["12.2.2", "10 ^ 2", "True && False", "'a'sd\;"]

        for test in invalid:
            with self.assertRaises(FunkyLexingError):
                lexer.do_lex(test)

    def test_lex_identifiers(self):
        valid = ["ident", "id", "test", "v0", "v1", "n", "under_score", "_"]
        invalid = ["_test", "12x", "test-123"]

        lexer = FunkyLexer()
        lexer.build()
        for test in valid:
            tokens = lexer.do_lex(test)
            self.assertTrue(len(tokens) == 1)

            token = tokens[0]
            self.assertTrue(token.type == "IDENTIFIER")
            self.assertTrue(token.value == test)

        for test in invalid:
            tokens = lexer.do_lex(test)
            self.assertTrue(len(tokens) != 1)

class TestSecondPass(TestCase):

    def test_valid_second_pass(self):
        tests = {
            """
module test with

    x = 10
    main = x""" : ["module", "test", "with", "{", "x", "=", 10, ";", "main",
                   "=", "x", "}"],

            """
module test with

    sqrt n = n ** 0.5

    euler = e ** (i * pi)
                with
                 e = 2.72
                 pi = 3.0
                        + 0.141
                 i = sqrt (-1.0)

    main = euler""" : ["module", "test", "with", "{", "sqrt", "n", "=", "n",
                       "**", 0.5, ";", "euler", "=", "e", "**", "(", "i", "*",
                       "pi", ")", "with", "{", "e", "=", 2.72, ";", "pi", "=",
                       3.0, "+", 0.141, ";", "i", "=", "sqrt", "(", "-", 1.0, ")",
                       "}", ";", "main", "=", "euler", "}"],

            """
module nested with

    x = y with y = 10 + x
                    with x = z
                            with z = 10

    main = x""" : ["module", "nested", "with", "{", "x", "=", "y", "with", "{",
                   "y", "=", 10, "+", "x", "with", "{", "x", "=", "z",
                   "with", "{", "z", "=", 10, "}", "}", "}", ";", "main", "=",
                   "x", "}"]
        }


        lexer = FunkyLexer()
        lexer.build()
        lexer = IndentationLexer(lexer)
        for test, expected in tests.items():
            lexer.input(test)
            values = [t.value for t in lexer]
            self.assertEqual(values, expected)
