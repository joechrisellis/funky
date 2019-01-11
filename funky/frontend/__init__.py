from funky import FunkyError

class FunkyFrontendError(FunkyError):
    pass

class FunkyParsingError(FunkyFrontendError):
    """Generic parsing error -- superclass for more specific parsing errors."""
    pass

class FunkySyntaxError(FunkyParsingError):
    """Raised when the parser fails to parse the lexed source."""
    pass

class FunkyLexingError(FunkyParsingError):
    """Raised when the lexer fails to lex the source code."""
    pass

class FunkyRenamingError(FunkyFrontendError):
    """Raised when the compiler fails to rename your code -- i.e. duplicate
    function definitions.
    """
    pass

class FunkyDesugarError(FunkyFrontendError):
    """Raised when the compiler is unable to desugar your code."""
    pass
