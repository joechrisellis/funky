
class FunkyError(Exception):
    """Base class for all funky errors."""

    def __init__(self, message):
        super().__init__(message)
