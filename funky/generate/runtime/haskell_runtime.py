from funky.generate.runtime import Runtime

class HaskellRuntime(Runtime):

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
        }
    
    def runtime_eq(self):
        return "=="

    def runtime_neq(self):
        return "/="

    def runtime_less(self):
        return "<"

    def runtime_leq(self):
        return "<="

    def runtime_greater(self):
        return ">"

    def runtime_geq(self):
        return ">="

    def runtime_pow(self):
        return "**"

    def runtime_add(self):
        return "+"

    def runtime_concat(self):
        return "++"

    def runtime_sub(self):
        return "-"

    def runtime_negate(self):
        return "negate"

    def runtime_mul(self):
        return "*"

    def runtime_div(self):
        return "/"

    def runtime_mod(self):
        return "mod"

    def runtime_logical_and(self):
        return "&&"

    def runtime_logical_or(self):
        return "||"
