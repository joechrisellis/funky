from unittest import TestCase

import funky.globals
import funky.util.specialchars as chars
from funky.util.color import *
from funky.util.orderedset import *
from funky.util import *

class TestSpecialCharacters(TestCase):

    def test_unicode_on(self):
        """Do we get unicode strings when we turn unicode on?"""
        prev = funky.globals.USE_UNICODE
        funky.globals.USE_UNICODE = True
        self.assertEqual(chars.C_LAMBDA, chars._lambda_unicode)
        self.assertEqual(chars.C_RIGHTARROW, chars._rightarrow_unicode)
        funky.globals.USE_UNICODE = prev

    def test_unicode_off(self):
        """Do we get non-unicode strings when we turn unicode off?"""
        prev = funky.globals.USE_UNICODE
        funky.globals.USE_UNICODE = False
        self.assertEqual(chars.C_LAMBDA, chars._lambda_plain)
        self.assertEqual(chars.C_RIGHTARROW, chars._rightarrow_plain)
        funky.globals.USE_UNICODE = prev

    def test_unicode_dynamic(self):
        """Can we change the global and have the returned characters change
        dynamically?
        """
        prev = funky.globals.USE_UNICODE

        funky.globals.USE_UNICODE = False
        self.assertEqual(chars.C_LAMBDA, chars._lambda_plain)
        self.assertEqual(chars.C_RIGHTARROW, chars._rightarrow_plain)

        funky.globals.USE_UNICODE = True
        self.assertEqual(chars.C_LAMBDA, chars._lambda_unicode)
        self.assertEqual(chars.C_RIGHTARROW, chars._rightarrow_unicode)

        funky.globals.USE_UNICODE = False
        self.assertEqual(chars.C_LAMBDA, chars._lambda_plain)
        self.assertEqual(chars.C_RIGHTARROW, chars._rightarrow_plain)

        funky.globals.USE_UNICODE = prev

class TestColors(TestCase):

    def test_colors_on(self):
        """Test that we get colorised strings when we turn coloring on."""
        prev = funky.globals.USE_COLORS

        funky.globals.USE_COLORS = True
        self.assertTrue(cgreen("Hello world") == "\33[32mHello world\033[0m")
        self.assertTrue(cyellow("Testing 123") == "\33[33mTesting 123\033[0m")
        self.assertTrue(cblue("I should be blue") == "\33[34mI should be blue\033[0m")

        funky.globals.USE_COLORS = prev

    def test_colors_off(self):
        """Test that colorizing does nothing when USE_COLORS is off."""
        prev = funky.globals.USE_COLORS

        funky.globals.USE_COLORS = False
        for s in ["Hello world", "Testing 123", "I should be color-less!"]:
            self.assertTrue(cgreen(s) == s)
            self.assertTrue(cyellow(s) == s)
            self.assertTrue(cblue(s) == s)

        funky.globals.USE_COLORS = prev

    def test_colors_dynamic(self):
        """Test that we can turn on/off colorizing dynamically."""
        prev = funky.globals.USE_COLORS

        funky.globals.USE_COLORS = False
        for s in ["Hello world", "Testing 123", "I should be color-less!"]:
            self.assertTrue(cgreen(s) == s)
            self.assertTrue(cyellow(s) == s)
            self.assertTrue(cblue(s) == s)

        funky.globals.USE_COLORS = True
        self.assertTrue(cgreen("Hello world") == "\33[32mHello world\033[0m")
        self.assertTrue(cyellow("Testing 123") == "\33[33mTesting 123\033[0m")
        self.assertTrue(cblue("I should be blue") == "\33[34mI should be blue\033[0m")

        funky.globals.USE_COLORS = False
        for s in ["Hello world", "Testing 123", "I should be color-less!"]:
            self.assertTrue(cgreen(s) == s)
            self.assertTrue(cyellow(s) == s)
            self.assertTrue(cblue(s) == s)

        funky.globals.USE_UNICODE = prev

class TestOrderedSet(TestCase):

    def test_order_preserved(self):
        """Checks that our OrderedSet actually preserves the order of insertion
        of the elements.
        """
        import random

        trials = 20
        for _ in range(trials):
            l, s = [], OrderedSet()
            for _ in range(random.randint(20, 50)):
                n = random.randint(0, 100)
                while n in s:
                    n = random.randint(0, 100)
                l.append(n)
                s.add(n)

            for x, y in zip(l, s):
                self.assertEqual(x, y)

class TestGetUserAttributes(TestCase):

    def test_get_user_attributes(self):
        """Tests that get_user_attributes returns the expected attributes for
        an object.
        """

        class TestClass1:
            x = 12
            y = 13
        self.assertEqual(get_user_attributes(TestClass1()), [("x", 12), ("y", 13)])

        class TestClass2:
            x = "test"
            y = "two"
            _ignore = "should not appear"

        self.assertEqual(get_user_attributes(TestClass2()), [("x", "test"), ("y", "two")])

        class TestClass3:
            x = "test"
            y = "two"
            x = 5

        self.assertEqual(get_user_attributes(TestClass3()), [("x", 5), ("y", "two")])

        class TestClass4:
            
            def __init__(self):
                self.x = 12

            def function(self):
                return 5

            def __repr__(self):
                return "test"

        self.assertEqual(get_user_attributes(TestClass4()), [("x", 12)])

class TestFlatten(TestCase):

    def test_nested(self):
        """Test that flatten works as intended on nested lists."""
        self.assertEqual(list(flatten([[1,2,3], [4,5,6]])), [1,2,3,4,5,6])
        self.assertEqual(list(flatten([[1,2,[3,4]], [5,6]])), [1,2,3,4,5,6])
        self.assertEqual(list(flatten([[[[[[1]]]],2,[3,4]], [5,6]])), [1,2,3,4,5,6])
        self.assertEqual(list(flatten([[1],[2],[3]])),[1,2,3])
        self.assertEqual(list(flatten([[1],[2],[3]])),[1,2,3])
        self.assertEqual(list(flatten([[[1,2,3]]])),[1,2,3])

    def test_flat(self):
        """Test that flatten is noop for already flat lists."""
        import random
        trials = 20
        for _ in range(trials):
            length = random.randint(3, 20)
            randlist = [random.randint(-10, 10) for _ in range(length)]
            self.assertEqual(list(flatten(randlist)), randlist)

    def test_empty(self):
        """Test flattening an empty list works as expected."""
        self.assertEqual(list(flatten([])), [])

class TestRegistryFunction(TestCase):
    
    def test_registry(self):
        """Tests if registry functions works as expected."""
        f = get_registry_function()

        @f.register(int)
        def f_int(x):
            return "int", x

        @f.register(str)
        def f_str(x):
            return "str", x

        @f.register(float)
        def f_str(x):
            return "float", x

        self.assertEqual(f(1.2), ("float", 1.2))
        self.assertEqual(f("test"), ("str", "test"))
        self.assertEqual(f(0), ("int", 0))

        with self.assertRaises(RuntimeError):
            f(True) # <- bool not defined for the above

    def test_registry_no_err(self):
        """Tests if registry functions are quiet when they are told not to
        raise errors.
        """
        f = get_registry_function(throw_err=False)

        @f.register(int)
        def f_int(x):
            return "int", x

        @f.register(str)
        def f_str(x):
            return "str", x

        @f.register(float)
        def f_str(x):
            return "float", x

        self.assertIsNone(f(False))
