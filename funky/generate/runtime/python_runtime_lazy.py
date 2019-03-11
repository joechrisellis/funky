from funky.generate.runtime import Runtime, add_to_runtime

class LazyPythonRuntime(Runtime):

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
    return lambda x: lambda: trampoline(a) == trampoline(x)""".format(fname, fname, fname), fname

    @add_to_runtime
    def runtime_neq(self):
        fname = "__neq"
        return """def {}(a):
    return lambda x: lambda: trampoline(a) != trampoline(x)""".format(fname), fname

    @add_to_runtime
    def runtime_less(self):
        fname = "__less"
        return """def {}(a):
    return lambda x: lambda: trampoline(a) < trampoline(x)""".format(fname), fname

    @add_to_runtime
    def runtime_leq(self):
        fname = "__leq"
        return """def {}(a):
    return lambda x: lambda: trampoline(a) <= trampoline(x)""".format(fname), fname

    @add_to_runtime
    def runtime_greater(self):
        fname = "__greater"
        return """def {}(a):
    return lambda x: lambda: trampoline(a) > trampoline(x)""".format(fname), fname

    @add_to_runtime
    def runtime_geq(self):
        fname = "__geq"
        return """def {}(a):
    return lambda x: lambda: trampoline(a) > trampoline(x)""".format(fname), fname

    @add_to_runtime
    def runtime_pow(self):
        fname = "__pow"
        return """def {}(a):
    return lambda x: lambda: trampoline(a) ** trampoline(x)""".format(fname), fname

    @add_to_runtime
    def runtime_add(self):
        fname = "__add"
        return """def {}(a):
    return lambda x: lambda: trampoline(a) + trampoline(x)""".format(fname), fname

    @add_to_runtime
    def runtime_concat(self):
        fname = "__concat"
        return """def {}(a):
    return lambda x: lambda: trampoline(a) + trampoline(x)""".format(fname), fname

    @add_to_runtime
    def runtime_sub(self):
        fname = "__sub"
        return """def {}(a):
    return lambda x: lambda: trampoline(a) - trampoline(x)""".format(fname), fname

    @add_to_runtime
    def runtime_negate(self):
        fname = "__negate"
        return """def {}(a):
    return lambda: -trampoline(a)""".format(fname), fname

    @add_to_runtime
    def runtime_mul(self):
        fname = "__mul"
        return """def {}(a):
    return lambda x: lambda: trampoline(a) * trampoline(x)""".format(fname), fname

    @add_to_runtime
    def runtime_div(self):
        fname = "__div"
        return """def {}(a):
    if isinstance(a, int):
        return lambda x: lambda: trampoline(a) // trampoline(x)
    else:
        return lambda x: lambda: trampoline(a) / trampoline(x)""".format(fname), fname

    @add_to_runtime
    def runtime_mod(self):
        fname = "__mod"
        return """def {}(a):
    return lambda x: lambda: trampoline(a) % trampoline(x)""".format(fname), fname

    @add_to_runtime
    def runtime_logical_and(self):
        fname = "__logical_and"
        return """def {}(a):
    return lambda x: lambda: trampoline(a) and trampoline(x)""".format(fname), fname

    @add_to_runtime
    def runtime_logical_or(self):
        fname = "__logical_or"
        return """def {}(a):
    return lambda x: lambda: trampoline(a) or trampoline(x)""".format(fname), fname

    @add_to_runtime
    def runtime_to_str(self):
        fname = "__to_str"
        return """def {}(a):
    return lambda: str(trampoline(a))""".format(fname), fname

    @add_to_runtime
    def runtime_to_int(self):
        fname = "__to_int"
        return """def {}(a):
    def inner():
        try:
            return int(trampoline(a))
        except ValueError:
            raise FunkyRuntimeError("Cannot convert '{{}}' to Integer.".format(a))
    return inner""".format(fname), fname

    @add_to_runtime
    def runtime_to_float(self):
        fname = "__to_float"
        return """def {}(a):
    def inner():
        try:
            return float(trampoline(a))
        except ValueError:
            raise FunkyRuntimeError("Cannot convert '{{}}' to Float.".format(a))
    return inner""".format(fname), fname

    @add_to_runtime
    def runtime_slice_from(self):
        fname = "__slice_from"
        return """def {}(a):
    return lambda s: lambda: trampoline(s)[trampoline(a):]""".format(fname), fname

    @add_to_runtime
    def runtime_slice_to(self):
        fname = "__slice_to"
        return """def {}(a):
    return lambda s: lambda: trampoline(s)[:trampoline(a)]""".format(fname), fname

    @add_to_runtime
    def runtime_error(self):
        fname = "__error"
        return """def {}(msg):
    def lam():
        raise FunkyRuntimeError(trampoline(msg))
    return lam""".format(fname), fname

    @add_to_runtime
    def runtime_undefined(self):
        fname = "__undefined"
        return """def {}():
    def lam():
        raise FunkyRuntimeError("undefined")
    return lam""".format(fname), fname + "()"
