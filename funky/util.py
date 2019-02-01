from itertools import count
import collections
import inspect
import sys

_global_counter = count()
global_counter = lambda: next(_global_counter)

def get_user_attributes(cls):
    """Returns the user attributes of a class. These are attributes which are
    not functions, and whose identifier's do not begin with '_' (which
    conventionally denotes a private attribute in Python).

    :param cls class: a class of any kind.
    :return:          a list of the public attributes of the class (those that
                      do not begin with an underscore).
    :rtype:           list
    """
    attributes = inspect.getmembers(cls, lambda a: not(inspect.isroutine(a)))
    attributes = [a for a in attributes if a[0][0] != "_"]
    return attributes

def output_attributes(self):
    """Recursively outputs the attributes of an object in the format
    ObjectName(attribute1=..., attribute2=...).
    """
    children = ", ".join("{}={}".format(a[0], repr(a[1]))
                         for a in get_user_attributes(self))
    return "{}({})".format(type(self).__name__, children)

def flatten(l):
    """Utility function to flatten an irregular list of lists.
    
    :param l list: an irregular list of lists
    :return:       the flatten list, e.g. [[[1, 2, 3], 4], 5] becomes
                   [1, 2, 3, 4, 5]
    :rtype         list
    """
    for item in l:
        if isinstance(item, collections.Iterable) and \
	   not isinstance(item, (str, bytes)):
            yield from flatten(item)
        else:
            yield item

# This might look ugly, but the logic of it is simple and it allows us to use a
# trivial interface for tree-walking, so it's well worth using your brain power
# to understand it!
def get_registry_function(throw_err=True, in_class=False):
    """Gets a registry function. Read docstring for 'register' below.

    :param throw_err bool: whether or not to throw a runtime error if no
                           registered function exists.
    :return:               the registry function.
    """
    def f(*args, **kwargs):
        try:
            obj = args[1] if in_class else args[0]
            return f.register.registry[type(obj)](*args, **kwargs)
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
