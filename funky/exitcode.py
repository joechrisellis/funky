"""The variables defined in this module map causes of failure to exit codes."""
import logging

log = logging.getLogger(__name__)

SUCCESS                 =  0
GENERIC_FRONTEND_ERROR  =  1
LEXING_ERROR            =  2
SYNTAX_ERROR            =  3
RENAMING_ERROR          =  4
DESUGAR_ERROR           =  5
GENERIC_PARSING_ERROR   =  6
TYPE_ERROR              =  7

def err_and_exit(msg, exception, exit_code):
    log.error(msg)
    log.error("Exception message: \"{}\"".format(exception.args[0]))
    exit(exit_code)
