import inspect
import sys

def err(*args, **kwargs):
    return print(*args, **kwargs, file=sys.stderr)

def get_user_attributes(cls):
    boring = dir(type('dummy', (object,), {}))
    return [item
            for item in inspect.getmembers(cls)
            if item[0] not in boring]
