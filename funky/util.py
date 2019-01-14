import inspect
import sys

from itertools import count, product
from string import ascii_lowercase

def string_generator():
    """Generator that yields as many strings as you need. Returns (a, b, ...,
    aa, ab, ...).
    """
    for i in count():
        for t in product(ascii_lowercase, repeat=i+1):
            yield "".join(t)

unique_varname = string_generator()

def get_unique_varname(generator=unique_varname):
    return next(generator)

def get_user_attributes(cls):
    """Returns the user attributes of a class. These are attributes which are
    not functions, and whose identifier's do not begin with '_' (which
    conventionally denotes a private attribute in Python).

    Input:
        cls -- the class.

    Returns:
        a list of the public attributes of the class (those that do not begin
        with an underscore).
    """
    attributes = inspect.getmembers(cls, lambda a: not(inspect.isroutine(a)))
    attributes = [a for a in attributes if a[0][0] != "_"]
    return attributes

def output_attributes(self):
    """Recursively outputs the attributes of an object in the format:
        ObjectName(attribute1=..., attribute2=...)

    This is useful as the __repr__ function for tree-like structures, like the
    parse tree.
    """
    children = ", ".join("{}={}".format(a[0], repr(a[1]))
                         for a in get_user_attributes(self))
    return "{}({})".format(type(self).__name__, children)

# This might look ugly, but the logic of it is simple and it allows us to use a
# trivial interface for tree-walking, so it's well worth using your brain power
# to understand it!
def get_registry_function(throw_err=True):
    """Gets a registry function. Read docstring for 'register' below."""
    def f(obj, *args, **kwargs):
        try:
            return f.register.registry[type(obj)](obj, *args, **kwargs)
        except KeyError:
            if throw_err:
                raise RuntimeError("No function registered for " \
                                   "'{}'.".format(type(obj)))

    def register(typ):
        """Nifty decorator that allows us to map a particular type to a
        particular function in some registry. This is useful for tree-walking
        -- it allows us to define 'visitor' methods for different tree-node
        types. The advantage of using this over basic polymorphism is:

            * We decouple tasks *on* a tree from the data structure itself.  *
            We can keep the tree node classes small, keeping only basic
            functions and data members.  * A method is never added to the
            class, so we don't pollute the namespace.

        Basically this grants us a clean way of keeping the task of
        walking/augmenting a tree separate from the tree structure itself.
        """
        def real_decorator(function):
            register.registry[typ] = function
            return function
        return real_decorator

    f.register = register
    f.register.registry = {}
    return f
