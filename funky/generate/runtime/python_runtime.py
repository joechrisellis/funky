from funky.generate.runtime import Runtime, add_to_runtime

class PythonRuntime(Runtime):

    def __init__(self):
        super().__init__()

        self.builtins = {
            "=="      :  self.runtime_eq,
            "!="      :  self.runtime_neq,
            "<"       :  self.runtime_less,
            "<="      :  self.runtime_leq,
            ">"       :  self.runtime_greater,
            ">="      :  self.runtime_geq,
            "**"      :  self.runtime_pow,
            "+"       :  self.runtime_add,
            "++"      :  self.runtime_concat,
            "-"       :  self.runtime_sub,
            "negate"  :  self.runtime_negate,
            "*"       :  self.runtime_mul,
            "/"       :  self.runtime_div,
            "%"       :  self.runtime_mod,
            "and"     :  self.runtime_logical_and,
            "or"      :  self.runtime_logical_or,
            "to_str"  :  self.runtime_to_str,
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
    return lambda x: a ** x""".format(fname), fname

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
