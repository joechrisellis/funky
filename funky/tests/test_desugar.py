from unittest import TestCase

from funky.parse.funky_parser import FunkyParser
from funky.rename.rename import do_rename
from funky.rename import FunkyRenamingError
from funky.parse.fixity import resolve_fixity

class TestDesugar(TestCase):

    def test_sanity(self):
        pass
