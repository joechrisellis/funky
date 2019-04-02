"""Sets logger verbosity."""

import logging

QUIET           =  -1
DEFAULT         =  0
VERBOSE         =  1
DOUBLE_VERBOSE  =  2
TRIPLE_VERBOSE  =  3

verbosity_2_loglevel = {
    QUIET           :  logging.CRITICAL,  #  <-  -q
    DEFAULT         :  logging.ERROR,     #  <-  default
    VERBOSE         :  logging.WARNING,   #  <-  -v
    DOUBLE_VERBOSE  :  logging.INFO,      #  <-  -vv
    TRIPLE_VERBOSE  :  logging.DEBUG,     #  <-  -vvv
}
quietest  =  min(verbosity_2_loglevel)
loudest   =  max(verbosity_2_loglevel)

def set_verbosity(verbosity):
    """Sets the loglevel of the logger based on a verbosity number. I.e.
    verbosity=3 corresponds to -vvv on the command line, etc. If the supplied
    verbosity is out of range, we use the loudest or quitest extreme depending
    on whether the range overflows or underflows.

    :param verbosity: the verbosity.
    """
    try:
        desired_loglevel = verbosity_2_loglevel[verbosity]
    except KeyError:
        verbosity = max(quietest, min(verbosity, loudest))
        desired_loglevel = verbosity_2_loglevel[verbosity]
    logging.getLogger().setLevel(desired_loglevel)
