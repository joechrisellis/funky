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

# This might look ugly, but the logic of it is simple and it allows us to use a
# trivial interface for tree-walking, so it's well worth using your brain power
# to understand it!
def get_registry_function():
    """Gets a registry function. Read docstring for 'register' below."""
    def f(obj, *args, **kwargs):
        try:
            return f.register.registry[type(obj)](obj, *args, **kwargs)
        except KeyError:
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
