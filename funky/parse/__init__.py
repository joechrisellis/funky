from funky import FunkyError

class FunkyParsingError(FunkyError):
    """Generic parsing error -- superclass for more specific parsing errors."""
    pass

class FunkyLexingError(FunkyParsingError):
    """Raised when the lexer fails to lex the source code."""
    pass

class FunkySyntaxError(FunkyParsingError):
    """Raised when the parser fails to parse the lexed source."""
    pass
