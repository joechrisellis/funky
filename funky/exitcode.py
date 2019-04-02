"""The variables defined in this module map causes of failure to exit codes."""
import logging
import funky.globals
from funky.util.color import *

log = logging.getLogger(__name__)

SUCCESS                 =  0
LEXING_ERROR            =  1
SYNTAX_ERROR            =  2
RENAMING_ERROR          =  3
DESUGAR_ERROR           =  4
GENERIC_PARSING_ERROR   =  5
TYPE_ERROR              =  6
CODE_GENERATION_ERROR   =  7

def err_and_exit(msg, exception, exit_code):
    """Exits the program, outputting an error message, and exception message,
    and exiting with the desired error code.
    
    :param msg str:             the error message to display before exiting
    :param exception Exception: the exception that lead to this
    :param exit_code int:       the exit code to quit with
    """
    if funky.globals.SHOW_EXCEPTION_TRACES:
        print(cred("SHOW_EXCEPTION_TRACES is true -- dumping exception trace:\n"))
        raise exception
    else:
        log.error(msg)
        log.error("Exception message: \"{}\"".format(exception.args[0]))
    exit(exit_code)
