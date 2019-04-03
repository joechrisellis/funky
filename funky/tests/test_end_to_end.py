from unittest import TestCase

from funky.ffi import funky_prog

class TestEndToEnd(TestCase):
    
    def test_factorial(self):
        prog = """
module factorial with

    factorial 0 = 1
    factorial n = n * factorial (n - 1)

    main = factorial {}
        """

        factorial = lambda n: 1 if n <= 1 else n * factorial(n - 1)
        for i in range(1, 20):
            fprog = funky_prog(prog.format(i))
            self.assertTrue(fprog() == factorial(i))

    def test_math(self):
        prog = """
module math with
    
    area r = pi * r ** 2.0
             with pi = 3.0 +
                            0.141
    
    main = area {0:.2f}
        """

        area = lambda r: 3.141 * r ** 2
        for i in range(1, 20):
            fprog = funky_prog(prog.format(i))
            self.assertTrue(fprog() == area(i))

    def test_patterns(self):
        prog = """
module pattern_matching with

    f  _      False  True   =  1
    f  False  True   _      =  2
    f  _      _      False  =  3
    f  _      _      True   =  4

    main = f {} {} {}
        """

        expected = {
            (False,  False,  False)  :  3,
            (False,  False,  True)   :  1,
            (False,  True,   False)  :  2,
            (False,  True,   True)   :  2,
            (True,   False,  False)  :  3,
            (True,   False,  True)   :  1,
            (True,   True,   False)  :  3,
            (True,   True,   True)   :  4,
        }

        for combination, expected in expected.items():
            fprog = funky_prog(prog.format(*combination))
            self.assertEqual(fprog(), expected)

    def test_xor(self):
        prog = """
module xor with

    xor  True   False  =  True
    xor  False  True   =  True
    xor  _      _      =  False

    main = xor {} {}
        """

        expected = {
            (False,  False)  :  False,
            (False,  True)   :  True,
            (True,   False)  :  True,
            (True,   True)   :  False,
        }

        for combination, expected in expected.items():
            fprog = funky_prog(prog.format(*combination))
            self.assertEqual(fprog(), expected)
    
    def test_quicksort(self):
        prog = """
module quicksort with

    import "stdlib.fky"
    import "intlist.fky"

    quicksort Nil         = Nil
    quicksort (Cons x xs) = (quicksort lesser) ~concatenate~ unit x ~concatenate~ (quicksort greater)
                            with lesser  = filter ((>)  x) xs
                                 greater = filter ((<=) x) xs

    main = pprint (quicksort my_list)
           with my_list = {}
        """

        tests = {
            "Cons 1 (Cons 2 (Cons 9 (Cons 1 (Cons 1 Nil))))" : "[1, 1, 1, 2, 9]",
            "Cons 4 (Cons (-1) (Cons 10 (Cons (-1) (Cons (-2) Nil))))" : "[-2, -1, -1, 4, 10]",
            "Cons 5 (Cons 1 (Cons 7 (Cons 7 (Cons 3 Nil))))" : "[1, 3, 5, 7, 7]",
            "Nil" : "[]",
            "Cons 1 Nil" : "[1]",
        }

        for test, expected in tests.items():
            fprog = funky_prog(prog.format(test))
            self.assertEqual(fprog(), expected)

    def test_treesort(self):
        prog = """
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

    main = pprint (treesort my_list)
           with my_list = {}
        """

        tests = {
            "Cons 1 (Cons 2 (Cons 9 (Cons 1 (Cons 1 Nil))))" : "[1, 1, 1, 2, 9]",
            "Cons 1 Nil" : "[1]",
            "Cons 4 (Cons (-1) (Cons 10 (Cons (-1) (Cons (-2) Nil))))" : "[-2, -1, -1, 4, 10]",
            "Cons 5 (Cons 1 (Cons 7 (Cons 7 (Cons 3 Nil))))" : "[1, 3, 5, 7, 7]",
            "Nil" : "[]",
        }

        for test, expected in tests.items():
            fprog = funky_prog(prog.format(test))
            self.assertEqual(fprog(), expected)

    def test_mutualrecursion(self):
        prog = """
module mutualrecursion with

    even 0 = True
    even n = odd  (n - 1)
    odd  0 = False
    odd  n = even  (n - 1)
    
    main = even {}
    """
    
        even = lambda n: n % 2 == 0
        for i in range(1, 10):
            fprog = funky_prog(prog.format(i))
            self.assertEqual(fprog(), even(i))
    
    def test_fizzbuzz(self):
        prog = """
module fizzbuzz with

    import "stdlib.fky"

    fizzbuzz n = fizzbuzz_ 1 n

    fizzbuzz_ n m given n == m    = aux n
                  given otherwise = aux n ++ "\\n" ++ fizzbuzz_ (n + 1) m
                  with aux x given x % 3 == 0 and x % 5 == 0 = "FizzBuzz"
                             given x % 3 == 0                = "Fizz"
                             given x % 5 == 0                = "Buzz"
                             given otherwise                 = to_str x

    main = fizzbuzz {}
        """

        fizz_buzz = lambda n: "FizzBuzz" if n % 3 == 0 and n % 5 == 0 \
                         else "Fizz" if n % 3 == 0 \
                         else "Buzz" if n % 5 == 0 \
                         else str(n)

        for n in [10, 20, 50, 100]:
            python_fizzbuzz = "\n".join(fizz_buzz(i) for i in range(1, n + 1))
            fprog = funky_prog(prog.format(n))
            funky_fizzbuzz = fprog()

            self.assertEqual(python_fizzbuzz, funky_fizzbuzz)

    def test_listlength(self):
        prog = """
module listlength with

    newtype List = Cons Integer List | Nil

    length Nil         = 0
    length (Cons _ xs) = 1 + length xs

    main = length my_list
           with my_list = {}
        """

        tests = {
            "Cons 1 (Cons 2 (Cons 3 Nil))" : 3,
            "Cons 5 (Cons 1 (Cons 7 (Cons 7 (Cons 3 Nil))))" : 5,
            "Nil" : 0,
        }

        for test, expected in tests.items():
            fprog = funky_prog(prog.format(test))
            self.assertEqual(fprog(), expected)

    def test_listindex(self):
        prog = """
module listindex with

    import "stdlib.fky"

    newtype List = Cons Integer List | Nil
    newtype Maybe = Just Integer | Nothing

    index e Nil = Nothing
    index e (Cons x xs) given e == x    = Just 0
                        given otherwise = match index e xs on
                                            Just x -> Just (x + 1)
                                            x      -> x

    main = index {} my_list
           with my_list = {}
        """

        tests = {
            (7, "Cons 5 (Cons 1 (Cons 7 (Cons 7 (Cons 3 Nil))))") : "Just 2",
            (1, "Cons 5 (Cons 1 (Cons 7 (Cons 7 (Cons 3 Nil))))") : "Just 1",
            (9, "Cons 5 (Cons 1 (Cons 7 (Cons 7 (Cons 3 Nil))))") : "Nothing",
            (9, "Nil") : "Nothing",
            (3, "Cons 1 (Cons 2 (Cons 3 Nil))") : "Just 2",
        }

        for (test_index, test_list), expected in tests.items():
            fprog = funky_prog(prog.format(test_index, test_list))
            self.assertEqual(str(fprog()), expected)

    def test_listsum(self):
        prog = """
module listsum with

    newtype List = Cons Integer List | Nil

    sum Nil         = 0
    sum (Cons x xs) = x + sum xs

    main = sum list
           with list = {}
        """

        tests = {
            "Cons 1 (Cons 2 (Cons 3 (Cons 4 (Cons 5 Nil))))" : 15,
            "Cons 1 (Cons 8 (Cons 5 (Cons 26 (Cons 1 (Cons 5 (Cons 19 Nil))))))" : 65,
            "Cons 5 (Cons 1 (Cons 7 (Cons 7 (Cons 3 Nil))))" : 23,
            "Nil" : 0,
        }

        for test_list, expected in tests.items():
            fprog = funky_prog(prog.format(test_list))
            self.assertEqual(fprog(), expected)

    def test_listmax(self):
        prog = """
module listmax with

    import "stdlib.fky"

    newtype List = Cons Integer List | Nil
    
    max Nil          = fail "No max of empty list!"
    max (Cons x Nil) = x
    max (Cons x xs) given x > n     = x
                    given otherwise = n
                    with n = max xs

    main = max list
           with list = {}
        """

        tests = {
            "Cons 1 (Cons 2 (Cons 3 (Cons 4 (Cons 5 Nil))))" : 5,
            "Cons 1 (Cons 8 (Cons 5 (Cons 26 (Cons 1 (Cons 5 (Cons 19 Nil))))))" : 26,
            "Cons 5 (Cons 1 (Cons 7 (Cons 7 (Cons 3 Nil))))" : 7,
        }

        for test_list, expected in tests.items():
            fprog = funky_prog(prog.format(test_list))
            self.assertEqual(fprog(), expected)
        
        with self.assertRaises(Exception):
            fprog = funky_prog(prog.format("Nil"))
            fprog()

    def test_lazy(self):
        prog = """
module lists with
    
    import "intlist.fky"

    ones  = Cons 1 ones
    nats  = iterate ((+) 1) 1
    negs  = map negate nats

    fibs = Cons 0 (Cons 1 (zipwith (+) fibs (tail fibs)))

    primes = sieve (tail nats)
             with sieve (Cons p xs) = Cons p (sieve (filter (lambda x -> x % p > 0) xs))

    main = pprint (take 5 {})
        """
        
        tests = {
            "ones"    :  "[1, 1, 1, 1, 1]",
            "nats"    :  "[1, 2, 3, 4, 5]",
            "negs"    :  "[-1, -2, -3, -4, -5]",
            "fibs"    :  "[0, 1, 1, 2, 3]",
            "primes"  :  "[2, 3, 5, 7, 11]",
        }

        for test_list, expected in tests.items():
            fprog = funky_prog(prog.format(test_list), lazy=True)
            self.assertEqual(str(fprog()), expected)
    
    def test_lazy_string(self):
        prog = """
module lazy_string with

    dog = "woof " ++ dog

    main = slice_to {} ("dog: " ++ dog)
        """

        sample = "dog: woof woof woof woof woof woof woof woof"
        for i in range(35):
            fprog = funky_prog(prog.format(i), lazy=True)
            self.assertEqual(fprog(), sample[:i])

    def test_slice_consistency(self):
        test_string = "hello world 1234567"
        prog = """
module slice with

    test_string = "{}"

    main = {} {} test_string
        """

        for f in ["slice_from", "slice_to"]:
            for n in range(len(test_string)):
                fprog_strict = funky_prog(prog.format(test_string, f, n))
                fprog_lazy = funky_prog(prog.format(test_string, f, n), lazy=True)
                if f == "slice_from":
                    self.assertEqual(fprog_strict(), test_string[n:])
                    self.assertEqual(fprog_lazy(), test_string[n:])
                else:
                    self.assertEqual(fprog_strict(), test_string[:n])
                    self.assertEqual(fprog_lazy(), test_string[:n])

    def test_matching1(self):
        prog = """
module test with

    newtype List = Cons Integer List | Nil

    test x = match x on
                (Cons x (Cons y Nil)) -> x + y
                (Cons x Nil) -> 999
                l -> 0

    main = test ({})
            """

        tests = {
            "Cons 1 (Cons 2 Nil)" : 1 + 2,
            "Cons 1 Nil" : 999,
            "Cons 1 (Cons 2 (Cons 3 Nil))" : 0,
            "Nil" : 0,
        }

        for test, expected in tests.items():
            fprog = funky_prog(prog.format(test))
            self.assertEqual(fprog(), expected)

    def test_matching2(self):
        prog = """
module test with

    newtype Maybe = Just Integer | Nothing

    increment = lambda n -> match n on
                                Just x -> Just (x + 1)
                                f -> f

    main = increment ({})
        """

        tests = {
            "Just 5" : "Just 6",
            "Just (-100)" : "Just -99",
            "Nothing" : "Nothing",
        }

        for test, expected in tests.items():
            fprog = funky_prog(prog.format(test))
            self.assertEqual(str(fprog()), expected)

    def test_matching3(self):
        prog = """
module test with

    newtype List = Cons Integer List | Nil

    test l = match l on
                Cons 1 (Cons 2 (Cons x xs)) -> x
                Cons 2 (Cons 1 (Cons x (Cons y ys))) -> x + y
                Cons 0 (Cons 0 Nil) -> 999
                _ -> -5

    main = test ({})
        """

        tests = {
            "Cons 1 (Cons 2 (Cons 123 (Cons 4 Nil)))" : 123,
            "Cons 2 (Cons 1 (Cons 123 (Cons 4 (Cons 3 Nil))))" : 123 + 4,
            "Cons 0 (Cons 0 (Cons 0 Nil))" : -5,
            "Cons 0 (Cons 0 Nil)" : 999,
        }

        for test, expected in tests.items():
            fprog = funky_prog(prog.format(test))
            self.assertEqual(fprog(), expected)
