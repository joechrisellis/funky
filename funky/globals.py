from enum import Enum, auto

class Mode(Enum):
    REPL      =  auto()
    COMPILER  =  auto()

CURRENT_MODE = None

# If True, permit the use of pretty unicode characters in output. Change this
# to False if you want plain ASCII (perhaps for older terminals.
USE_UNICODE = True

# If True, permit the use of colorised output. Change this to False if you want
# all of your output to be mono and boring. :)
USE_COLORS = True
