from unittest import TestCase

from funky.parse import FunkySyntaxError
from funky.parse.funky_parser import FunkyParser
from funky.corelang.sourcetree import ASTNode

class TestParser(TestCase):

    def test_valid_parse(self):
        valid_programs = ["""
module test with

    main = 10 + 10
        """,

        """
module test with

    factorial 0 = 1
    factorial n = n * factorial (n - 1)
    main = factorial 5""",
    
    """
module test with

    area r = pi * r ** 2.0
             with pi = 3.141
    """,
    
    """
# Treesort algorithm for integer in Funky.
module treesort with

    import "stdlib.fky"
    import "intlist.fky"

    newtype Tree = Branch Tree Integer Tree | Empty

    insert e Empty                          = Branch Empty e Empty
    insert e (Branch l v r) given e <= v    = Branch (insert e l) v r
                            given otherwise = Branch l v (insert e r)
    
    inorder Empty = Nil
    inorder (Branch l v r) = inorder l ~concatenate~
                             unit v    ~concatenate~
                             inorder r

    treesort list = inorder (foldr insert Empty list)

    main = treesort my_list
           with my_list = Cons 5 (Cons 1 (Cons 7 (Cons 7 (Cons 3 Nil))))
    """,
    
    """
# Representing and evaluating expression trees in Funky.
module expressiontree with

    newtype Expression = Const Float
                       | BinOp Expression
                               (Expression -> Expression -> Float)
                               Expression
                       | UnOp  (Expression -> Float)
                               Expression

    evaluate (Const x)     = x
    evaluate (BinOp a f b) = f a b
    evaluate (UnOp f x)    = f x

    add  exp1  exp2  =  (evaluate  exp1)  +  (evaluate  exp2)
    sub  exp1  exp2  =  (evaluate  exp1)  -  (evaluate  exp2)
    mul  exp1  exp2  =  (evaluate  exp1)  *  (evaluate  exp2)
    div  exp1  exp2  =  (evaluate  exp1)  /  (evaluate  exp2)

    test_exp = (BinOp (Const 5.0) add (BinOp (Const 3.0) div (Const 2.0)))

    main = evaluate test_exp
    """,
    
    """
# Demonstrating the use of Funky's random library to generate a random float.
module randomfloat with

    import "random.fky"

    seed = 51780

    main = randfloat seed
    """]

        parser = FunkyParser()
        parser.build()
        for valid_program in valid_programs:
            ast = parser.do_parse(valid_program)
            self.assertTrue(isinstance(ast, ASTNode))

    def test_invalid_parse(self):
        invalid_programs = [
            """
module invalid with

    main = f x + + 2
            """,

            """
module invalid some rubbish with 
    nothing
            """,

            """
module invalid with

    n = * 5 2 # '*' needs to be '(*)' for this to be valid!
            """,

            """
module invalid with
    10 + 10"""
            ]

        parser = FunkyParser()
        parser.build()
        for invalid_program in invalid_programs:
            with self.assertRaises(FunkySyntaxError):
                parser.do_parse(invalid_program)
