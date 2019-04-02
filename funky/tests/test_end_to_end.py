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
