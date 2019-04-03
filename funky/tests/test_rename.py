from unittest import TestCase

from funky.parse.funky_parser import FunkyParser
from funky.rename.rename import do_rename
from funky.rename import FunkyRenamingError

class TestRenamerSanity(TestCase):

    def test_sanity(self):
        sanity_fails = [
            """
module test with

    tau  = 2 * pi
            """,

            """
module test with
    
    f 0 0 = 0
    f x y z = 1
            """,
            
            """
module test with
    
    f x x = 1
            """,

            """
module test with
    
    to_int = 10
            """,

            """
module test with
    
    to_str = 10
            """,

            """
module test with
    
    to_float = 10
            """,

            """
module test with
    newtype Test = P Integer | P Float
            """,

            """
module test with
    newtype Test  = P Integer
    newtype Test2 = P Float
            """,

            """
module test with
    x = 2
    x = 3
            """,
        ]

        parser = FunkyParser()
        parser.build()
        for test in sanity_fails:
            ast = parser.do_parse(test)
            with self.assertRaises(FunkyRenamingError):
                do_rename(ast)
