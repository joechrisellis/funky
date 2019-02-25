from enum import Enum, auto

class Mode(Enum):
    REPL      =  auto()
    COMPILER  =  auto()

CURRENT_MODE = None
