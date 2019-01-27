from funky import FunkyError

class FunkyRenamingError(FunkyError):
    """Raised when the compiler fails to rename your code -- i.e. duplicate
    function definitions.
    """
    pass
