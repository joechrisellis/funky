"""A central place for special printable characters used in the compiler."""
from types import ModuleType
import funky.globals

class Characters(ModuleType):

    _lambda_unicode,      _lambda_plain      =  "\u03BB",  "lambda"
    _rightarrow_unicode,  _rightarrow_plain  =  "\u2192",  "->"

    # Using properties here because if the USE_UNICODE flag changes, we want to
    # be able to reflect it. In other words, we can switch USE_UNICODE off and
    # on dynamically and it'll work fine.

    @property
    def C_LAMBDA(self):
        return self._lambda_unicode if funky.globals.USE_UNICODE \
          else self._lambda_plain

    @property
    def C_RIGHTARROW(self):
        return self._rightarrow_unicode if funky.globals.USE_UNICODE \
          else self._rightarrow_plain

    ALL_CHARACTERS = [C_LAMBDA, C_RIGHTARROW]

import sys
sys.modules[__name__] = Characters(__name__)
