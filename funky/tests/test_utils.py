from unittest import TestCase

import funky.globals
import funky.util.specialchars as chars
from funky.util.color import *

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
