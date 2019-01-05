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

def add_method(cls, attr):
    """Useful decorator for setting a function as a method for some class
    without actually defining it inside that class. This is primarily used so
    that we can distribute AST-traversal-related tasks across different
    modules.
    
    For example:

        @add_method(TestClass, "test_function")
        def test_function(self):
            print("Hello world")
    
    Means that we can do:

        t = TestClass()
        t.test_function() # "Hello world"

    Which allows us to define methods for an object externally.
    """
    def real_decorator(f):
        setattr(cls, attr, f)
        return f
    return real_decorator
