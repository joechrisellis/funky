# code generated by funky py_compiler
# generated 2019-02-09 at 11:29:39

# section: code_runtime
class ADT:
    """Superclass for all ADTs."""

    def __init__(self, params):
        self.params = params

class InexhaustivePatternMatchError(Exception):
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
    if isinstance(a, int):
        return lambda x: a // x
    else:
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
        if ans is not None:
            args = [p for p in scrutinee.params]
            if args:
                return ans(*args)
            else:
                return ans()
    else:
        ans = __match_literal(scrutinee, outcomes)
        if ans is not None:
            return ans()

    if default:
        return default()
    else:
        raise InexhaustivePatternMatchError("Inexhaustive pattern match, cannot "
                                            "continue.")

def __match_adt(scrutinee, outcomes):
    return outcomes.get(scrutinee.__class__, None)

def __match_literal(scrutinee, outcomes):
    for alt, expr in outcomes.items():
        if scrutinee == alt:
            return expr

# section: create_adts
class ADTList(ADT):
    """ADT superclass."""
    pass

class ADTCons(ADTList):

    def __init__(self, v0, v1):
        super().__init__([v0, v1])

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return all(x == y for x, y in zip(self.params, other.params))

    def __str__(self):
        name = type(self).__name__[3:]
        vars = [str(x) for x in self.params]
        return "({} {})".format(name, " ".join(vars))

Cons = lambda v0: lambda v1: ADTCons(v0, v1)

class ADTNil(ADTList):

    def __init__(self):
        super().__init__([])

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return all(x == y for x, y in zip(self.params, other.params))

    def __str__(self):
        name = type(self).__name__[3:]
        return name

Nil = ADTNil()

v0 = True
def v1(v1_0):
    def lam(v1_1):
        def m0(Cons_v1_0_0, Cons_v1_0_1):
            return ((Cons)(Cons_v1_0_0))(((v1)(Cons_v1_0_1))(v1_1))
        def m1():
            def m0():
                return v1_1
            def m1():
                def m0():
                    return v1_0
                return __match(v1_1, {ADTNil : m0}, None)
            return __match(v1_0, {ADTNil : m0}, m1)
        return __match(v1_0, {ADTCons : m0}, m1)
    return lam

def v2(v2_0):
    def lam(v2_1):
        def m0():
            return ((Cons)(v2_0))(Nil)
        def m1():
            def m0():
                return ((Cons)(v2_0))(((v2)(((__add)(v2_0))(1)))(v2_1))
            return __match(v0, {True : m0}, None)
        return __match(((__eq)(v2_0))(v2_1), {True : m0, False : m1}, None)
    return lam

# section: emit_main
def main():
    print(((v1)(Nil))(Nil))

if __name__ == "__main__":
    main()
