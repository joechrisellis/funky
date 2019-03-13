"""A central place for special printable characters used in the compiler."""
from types import ModuleType
import funky.globals

class Characters(ModuleType):

    # Using properties here because if the USE_UNICODE flag changes, we want to
    # be able to reflect it. In other words, we can switch USE_UNICODE off and
    # on dynamically and it'll work fine.

    @property
    def C_LAMBDA(self):
        return "\u03BB" if funky.globals.USE_UNICODE else "lambda"

    @property
    def C_RIGHTARROW(self):
        return u"\u2192" if funky.globals.USE_UNICODE else "->"

import sys
sys.modules[__name__] = Characters(__name__)
