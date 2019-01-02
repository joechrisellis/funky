import inspect
import sys

def err(*args, **kwargs):
    """Wrapper around Python's print function -- instead of printing to stdout,
    we print to stderr.
    """
    return print(*args, **kwargs, file=sys.stderr)

def get_user_attributes(cls):
    """Returns the user attributes of a class. These are attributes which are
    not functions, and whose identifier's do not begin with '_' (which
    conventionally denotes a private attribute in Python).
    """
    attributes = inspect.getmembers(cls, lambda a: not(inspect.isroutine(a)))
    attributes = [a for a in attributes if a[0][0] != "_"]
    return attributes
