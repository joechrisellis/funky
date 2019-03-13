from enum import Enum, auto

class Mode(Enum):
    REPL      =  auto()
    COMPILER  =  auto()

CURRENT_MODE = None

# If True, permit the use of pretty unicode characters in output. Change this
# to false if you want plain ASCII (perhaps for older terminals.
USE_UNICODE = True
