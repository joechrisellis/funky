"""Sets logger verbosity."""

import logging

verbosity_2_loglevel = {
    -1  :  logging.CRITICAL, # <- -q
    0   :  logging.WARNING,  # <- -v
    1   :  logging.INFO,     # <- -vv
    2   :  logging.DEBUG,    # <- -vvv
}
least_verbose  =  verbosity_2_loglevel[min(verbosity_2_loglevel)]
most_verbose   =  verbosity_2_loglevel[max(verbosity_2_loglevel)]

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
        desired_loglevel = max(least_verbose, min(verbosity, most_verbose))
    logging.getLogger().setLevel(desired_loglevel)
