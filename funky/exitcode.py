"""The variables defined in this module map causes of failure to exit codes."""
import logging

log = logging.getLogger(__name__)

SUCCESS                 =  0
LEXING_ERROR            =  1
SYNTAX_ERROR            =  2
RENAMING_ERROR          =  3
DESUGAR_ERROR           =  4
GENERIC_PARSING_ERROR   =  5
TYPE_ERROR              =  6

def err_and_exit(msg, exception, exit_code):
    log.error(msg)
    log.error("Exception message: \"{}\"".format(exception.args[0]))
    exit(exit_code)
