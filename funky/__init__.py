import logging
logging.basicConfig(level=logging.DEBUG)

class FunkyError(Exception):
    """Base class for all funky errors."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
