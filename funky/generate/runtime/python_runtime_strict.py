from funky.generate.runtime import Runtime, add_to_runtime

class StrictPythonRuntime(Runtime):

    def __init__(self):
        super().__init__()

        self.builtins = {
            "=="          :  self.runtime_eq,
            "!="          :  self.runtime_neq,
            "<"           :  self.runtime_less,
            "<="          :  self.runtime_leq,
            ">"           :  self.runtime_greater,
            ">="          :  self.runtime_geq,
            "**"          :  self.runtime_pow,
            "+"           :  self.runtime_add,
            "++"          :  self.runtime_concat,
            "-"           :  self.runtime_sub,
            "negate"      :  self.runtime_negate,
            "*"           :  self.runtime_mul,
            "/"           :  self.runtime_div,
            "%"           :  self.runtime_mod,
            "and"         :  self.runtime_logical_and,
            "or"          :  self.runtime_logical_or,
            "to_str"      :  self.runtime_to_str,
            "to_int"      :  self.runtime_to_int,
            "to_float"    :  self.runtime_to_float,
            "slice_from"  :  self.runtime_slice_from,
            "slice_to"    :  self.runtime_slice_to,

            "error"       :  self.runtime_error,
            "undefined"   :  self.runtime_undefined,
        }
    
    @add_to_runtime
    def runtime_eq(self):
        fname = "__eq"
        return """def {}(a):
    return lambda x: a == x""".format(fname), fname

    @add_to_runtime
    def runtime_neq(self):
        fname = "__neq"
        return """def {}(a):
    return lambda x: a != x""".format(fname), fname

    @add_to_runtime
    def runtime_less(self):
        fname = "__less"
        return """def {}(a):
    return lambda x: a < x""".format(fname), fname

    @add_to_runtime
    def runtime_leq(self):
        fname = "__leq"
        return """def {}(a):
    return lambda x: a <= x""".format(fname), fname

    @add_to_runtime
    def runtime_greater(self):
        fname = "__greater"
        return """def {}(a):
    return lambda x: a > x""".format(fname), fname

    @add_to_runtime
    def runtime_geq(self):
        fname = "__geq"
        return """def {}(a):
    return lambda x: a > x""".format(fname), fname

    @add_to_runtime
    def runtime_pow(self):
        fname = "__pow"
        return """def {}(a):
    def lam(x):
        if type(a) == int and type(x) == int:
            return int(a ** x)
        else:
            return a ** x
    return lam""".format(fname), fname

    @add_to_runtime
    def runtime_add(self):
        fname = "__add"
        return """def {}(a):
    return lambda x: a + x""".format(fname), fname

    @add_to_runtime
    def runtime_concat(self):
        fname = "__concat"
        return """def {}(a):
    return lambda x: a + x""".format(fname), fname

    @add_to_runtime
    def runtime_sub(self):
        fname = "__sub"
        return """def {}(a):
    return lambda x: a - x""".format(fname), fname

    @add_to_runtime
    def runtime_negate(self):
        fname = "__negate"
        return """def {}(a):
    return -a""".format(fname), fname

    @add_to_runtime
    def runtime_mul(self):
        fname = "__mul"
        return """def {}(a):
    return lambda x: a * x""".format(fname), fname

    @add_to_runtime
    def runtime_div(self):
        fname = "__div"
        return """def {}(a):
    if isinstance(a, int):
        return lambda x: a // x
    else:
        return lambda x: a / x""".format(fname), fname

    @add_to_runtime
    def runtime_mod(self):
        fname = "__mod"
        return """def {}(a):
    return lambda x: a % x""".format(fname), fname

    @add_to_runtime
    def runtime_logical_and(self):
        fname = "__logical_and"
        return """def {}(a):
    return lambda x: a and x""".format(fname), fname

    @add_to_runtime
    def runtime_logical_or(self):
        fname = "__logical_or"
        return """def {}(a):
    return lambda x: a or x""".format(fname), fname

    @add_to_runtime
    def runtime_to_str(self):
        fname = "__to_str"
        return """def {}(a):
    return str(a)""".format(fname), fname

    @add_to_runtime
    def runtime_to_int(self):
        fname = "__to_int"
        return """def {}(a):
    try:
        return int(a)
    except ValueError:
        raise FunkyRuntimeError("Cannot convert '{{}}' to Integer.".format(a))""".format(fname), fname

    @add_to_runtime
    def runtime_to_float(self):
        fname = "__to_float"
        return """def {}(a):
    try:
        return float(a)
    except ValueError:
        raise FunkyRuntimeError("Cannot convert '{{}}' to Float.".format(a))""".format(fname), fname

    @add_to_runtime
    def runtime_slice_from(self):
        fname = "__slice_from"
        return """def {}(a):
    return lambda s: s[a:]""".format(fname), fname

    @add_to_runtime
    def runtime_slice_to(self):
        fname = "__slice_to"
        return """def {}(a):
    return lambda s: s[:a]""".format(fname), fname

    @add_to_runtime
    def runtime_error(self):
        fname = "__error"
        return """def {}(msg):
    raise FunkyRuntimeError(msg)""".format(fname), fname

    @add_to_runtime
    def runtime_undefined(self):
        fname = "__undefined"
        return """def {}():
    raise FunkyRuntimeError("undefined")""".format(fname), fname + "()"
