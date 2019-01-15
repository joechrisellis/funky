from funky import FunkyError

class FunkyIntermediateError(FunkyError):
    pass

class FunkyTypeError(FunkyIntermediateError):
    """Thrown when something goes wrong with type inference."""
    pass
