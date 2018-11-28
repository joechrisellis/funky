import sys

def err(*args, **kwargs):
    return print(*args, **kwargs, file=sys.stderr)
