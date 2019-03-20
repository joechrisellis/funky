"""Sets logger verbosity."""

import logging

QUIET           =  -1
VERBOSE         =  0
DOUBLE_VERBOSE  =  1
TRIPLE_VERBOSE  =  2

verbosity_2_loglevel = {
    QUIET           :  logging.CRITICAL,  # <- -q
    VERBOSE         :  logging.WARNING,   # <- -v
    DOUBLE_VERBOSE  :  logging.INFO,      # <- -vv
    TRIPLE_VERBOSE  :  logging.DEBUG,     # <- -vvv
}
least_verbose_key  =  min(verbosity_2_loglevel)
most_verbose_key   =  max(verbosity_2_loglevel)

def get_loglevel():
    """Gets the current loglevel.
    
    :return: the current loglevel
    """
    return logging.getLogger().getEffectiveLevel()

def set_loglevel(verbosity):
    """Sets the loglevel of the logger based on a verbosity number. I.e.
    verbosity=3 corresponds to -vvv on the command line, etc. If the supplied
    verbosity is out of range, we use the loudest or quitest extreme depending
    on whether the range overflows or underflows.

    :param verbosity: the verbosity.
    """
    try:
        desired_loglevel = verbosity_2_loglevel[verbosity]
    except KeyError:
        verbosity = max(least_verbose_key, min(verbosity, most_verbose_key))
        desired_loglevel = verbosity_2_loglevel[verbosity]
    logging.getLogger().setLevel(desired_loglevel)
