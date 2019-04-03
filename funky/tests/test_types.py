from unittest import TestCase

import funky.globals

from funky.parse.funky_parser import FunkyParser
from funky.rename.rename import do_rename
from funky.desugar.desugar import do_desugar
from funky.infer.infer import do_type_inference
from funky.infer import FunkyTypeError

parser = FunkyParser()
parser.build()
def get_type_str(source):
    ast = parser.do_parse(source)
    # NOTE: we do not include imports for simplicity :)
    do_rename(ast)
    core_tree, typedefs = do_desugar(ast)
    do_type_inference(core_tree, typedefs)

    return str(core_tree.inferred_type)

class TestBasicInference(TestCase):

    def setUp(self):
        funky.globals.USE_UNICODE  =  False
        funky.globals.USE_COLOR    =  False

    def test_basic_type_inference(self):
        tests = {
            """
module test with

    main = 10
            """ : "Integer",
            
            """
module test with

    main = 10.2
            """ : "Float",

            """
module test with

    f x = x + 1

    main = f 10
            """ : "Integer",

            """
module test with

    f x y = x + y

    main = f
            """ : "Num -> Num -> Num",

            """
module test with

    main = (+)
            """ : "Num -> Num -> Num",

            """
module test with

    main = to_int
            """ : "Intable -> Integer",

            """
module test with

    id x = x

    main = id id id id id id id id id id
            """ : r"(t\d+) -> \1",

        }

        for program, expected in tests.items():
            typ = get_type_str(program)
            self.assertRegex(typ, expected)

    def test_more_complex(self):
        tests = {
            """
module test with

    repeat f 0 x = x
    repeat f n x = f (repeat f (n - 1) x)

    main = repeat
            """ : r"\((t\d+) -> \1\) -> Integer -> \1 -> \1",

            """
module test with

    fix f = f (fix f)

    main = fix
            """ : r"\((t\d+) -> \1\) -> \1",

            """
module test with

    newtype List = Cons Integer List | Nil

    map f Nil = Nil
    map f (Cons x xs) = Cons (f x) (map f xs)

    main = map
            """ : r"\(Integer -> Integer\) -> List -> List",

            """
module test with

    newtype List = Cons Integer List | Nil

    filter p Nil = Nil
    filter p (Cons x xs) given p x   = Cons x rest
                         given False = rest
                         with rest = filter p xs

    main = filter
            """ : r"\(Integer -> Bool\) -> List -> List",

            """
module test with

    newtype List = Cons Integer List | Nil

    foldr f z Nil = z
    foldr f z (Cons x xs) = f x (foldr f z xs)

    main = foldr
            """ : r"\(Integer -> (t\d+) -> \1\) -> \1 -> List -> \1",
        }

        for program, expected in tests.items():
            typ = get_type_str(program)
            self.assertRegex(typ, expected)

    def test_lazy_types(self):
        tests = {
            """
module test with

    newtype List = Cons Integer List | Nil
    
    ones = Cons 1 ones

    main = ones
            """ : "List",

            """
module test with

    newtype List = Cons Integer List | Nil

    map f Nil = Nil
    map f (Cons x xs) = Cons (f x) (map f xs)
    
    nats = Cons 1 (map ((+) 1) nats)

    main = nats
            """ : "List",

            """
module test with

    dog = "woof " ++ dog

    main = dog
            """ : "String"
        }

        for program, expected in tests.items():
            typ = get_type_str(program)
            self.assertRegex(typ, expected)

    def test_invalid_types(self):
        invalid_programs = [
            """
module test with

    main = "test" + 1
            """,

            """
module test with

    True  ~n~  True  =  True
    _     ~n~  _     =  False

    main = n 1 2
            """,

            """
module test with

    newtype List = Cons Integer List | Nil
    main = Cons 1 (Cons 2 (Cons 3))
            """,

            """
module test with

    newtype List = Cons Integer List | Nil

    filter p Nil = Nil
    filter p (Cons x xs) given p x   = Cons x rest
                         given False = rest
                         with rest = filter p xs
    
    main = filter (lambda x -> x + 1) my_list
           with my_list = Cons 1 (Cons 2 (Cons 3 Nil))
            """
        ]

        for program in invalid_programs:
            with self.assertRaises(FunkyTypeError):
                get_type_str(program)

    def test_inference_unreachable_patterns(self):
        tests = {
            """
module test with
    newtype List = Cons Integer List | Nil

    concatenate (Cons x xs) ys = Cons x (xs ~concatenate~ ys)
    concatenate xs Nil = xs
    concatenate Nil ys = ys
    concatenate Nil Nil = "garbage"

    main = concatenate
            """ : "List -> List -> List",

            """
module test with

    f x y = x + y
    f 0 0 = "test"

    main = f
            """ : "Num -> Num -> Num"
        }

        for program, expected in tests.items():
            typ = get_type_str(program)
            self.assertRegex(typ, expected)
