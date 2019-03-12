"""Module for printing with color."""

from functools import partial

colors = {
    "CBLACK"   :  '\33[30m',
    "CRED"     :  '\33[31m',
    "CGREEN"   :  '\33[32m',
    "CYELLOW"  :  '\33[33m',
    "CBLUE"    :  '\33[34m',
    "CVIOLET"  :  '\33[35m',
    "CBEIGE"   :  '\33[36m',
    "CWHITE"   :  '\33[37m',
}
ENDC = '\033[0m'

def colorize(color, string):
    """Produces a string that, when printed, appears in the given color.
    
    :param color:  the color, which must be in the colors dictionary
    :param string: the string you want to colorize"""
    if color not in colors:
        raise ValueError("Undefined color '{}'.".format(color))
    return colors[color] + string + ENDC

# create a nice function to easily colorize a string
for color in colors:
    exec("{} = partial(colorize, \"{}\")".format(color.lower(), color))

# color palette used when pretty printing things in the compiler
COLOR_CONSTANT  =  cred
COLOR_EQUALS    =  cviolet
COLOR_KEYWORD   =  cyellow
COLOR_OPERATOR  =  cviolet
COLOR_TYPENAME  =  cbeige
