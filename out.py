# code generated by funky py_compiler
# generated 2019-02-03 at 23:50:32

from contextlib import contextmanager
from inspect import currentframe, getouterframes
from functools import partial

class ADT:
    """Superclass for all ADTs."""
    pass

def __eq(a):
    return lambda x: a == x

def __neq(a):
    return lambda x: a != x

def __less(a):
    return lambda x: a < x

def __leq(a):
    return lambda x: a <= x

def __greater(a):
    return lambda x: a > x

def __geq(a):
    return lambda x: a >= x

def __pow(a):
    return lambda x: a ** x

def __add(a):
    return lambda x: a + x

def __sub(a):
    return lambda x: a - x

def __negate(a):
    return -a

def __mul(a):
    return lambda x: a * x

def __div(a):
    return lambda x: a / x

def __mod(a):
    return lambda x: a % x

def __logical_and(a):
    return lambda x: a and x

def __logical_or(a):
    return lambda x: a or x

def __match(scrutinee, outcomes, default):
    if isinstance(scrutinee, ADT):
        ans = __match_adt(scrutinee, outcomes)
    else:
        ans = __match_literal(scrutinee, outcomes)

    if ans is not None:
        return __lazy(ans)
    else:
        return __lazy(default)

def __match_adt(scrutinee, outcomes):
    raise NotImplementedError()

def __match_literal(scrutinee, outcomes):
    for alt, expr in outcomes.items():
        if scrutinee == alt:
            return expr

def __lazy(f):
    return f()

@contextmanager
def __let(**bindings):
    # special thanks to Vladimir Iakovlev
    # 2 because first frame in `contextmanager` decorator  
    frame = getouterframes(currentframe(), 2)[-1][0]
    locals_ = frame.f_locals
    original = {var: locals_.get(var) for var in bindings.keys()}
    locals_.update(bindings)
    yield
    locals_.update(original)


class ADTList(ADT):
    """ADT superclass."""
    pass

class ADTCons(ADTList):

    def __init__(self, v0, v1):
        self.v0 = v0
        self.v1 = v1

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.v0 == other.v0 and \
               self.v1 == other.v1

Cons = lambda v0: lambda v1: ADTCons(v0, v1)

class ADTNil(ADTList):

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return True

Nil = ADTNil()


v0 = True
def v1(v1_0):
    def v2(v2_0):
        return __match(v2_0, {0 : lambda: True}, lambda: (v3)(((__sub)(v2_0))(1)))

    def v3(v3_0):
        return __match(v3_0, {0 : lambda: False}, lambda: (v2)(((__sub)(v3_0))(1)))

    return (v2)(v1_0)

def v4(v4_0):
    v5 = 3.14
    return ((__mul)(v5))(((__pow)(v4_0))(2.0))

def v6(v6_0):
    return __match(v6_0, {0 : lambda: 1}, lambda: ((__mul)(v6_0))((v6)(((__sub)(v6_0))(1))))

def v7(v7_0):
    return lambda v7_1: lambda v7_2: __match(v7_1, {False : lambda: __match(v7_2, {True : lambda: 1}, lambda: __match(v7_2, {False : lambda: 3}, lambda: None))}, lambda: __match(v7_1, {True : lambda: __match(v7_0, {False : lambda: 2}, lambda: __match(v7_2, {False : lambda: 3}, lambda: __match(v7_2, {True : lambda: 4}, lambda: None)))}, lambda: __match(v7_2, {False : lambda: 3}, lambda: __match(v7_2, {True : lambda: 4}, lambda: None))))

