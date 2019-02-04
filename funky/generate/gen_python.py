from funky.corelang.coretree import *
from funky.generate.gen import CodeGenerator, annotate_section
from funky.util import get_registry_function
import datetime

python_runtime = """class ADT:
    \"\"\"Superclass for all ADTs.\"\"\"

    def __init__(self, params):
        self.params = params

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
        if ans is not None:
            args = [p for p in scrutinee.params]
            if args:
                return __lazy(ans(*args))
            else:
                return __lazy(ans)
    else:
        ans = __match_literal(scrutinee, outcomes)
        if ans is not None:
            return __lazy(ans)

    return __lazy(default)

def __match_adt(scrutinee, outcomes):
    return outcomes.get(scrutinee.__class__, None)

def __match_literal(scrutinee, outcomes):
    for alt, expr in outcomes.items():
        if scrutinee == alt:
            return expr

def __lazy(f):
    return f()
"""

builtins = {
    "=="      :  "__eq",
    "!="      :  "__neq",
    "<"       :  "__less",
    "<="      :  "__leq",
    ">"       :  "__greater",
    ">="      :  "__geq",
    "**"      :  "__pow",
    "+"       :  "__add",
    "-"       :  "__sub",
    "negate"  :  "__negate",
    "*"       :  "__mul",
    "/"       :  "__div",
    "%"       :  "__mod",
    "&&"      :  "__logical_and",
    "||"      :  "__logical_or",
}

class PythonCodeGenerator(CodeGenerator):

    docstring = "\"\"\"{}\"\"\"".format
    comment = "# {}".format

    def __init__(self):
        super().__init__()

    def code_header(self):
        self.emit(self.comment("code generated by funky py_compiler"))
        self.emit(self.comment("generated {}".format(self.timestamp())))
        self.newline()

    @annotate_section
    def code_runtime(self):
        self.emit(python_runtime)

    @annotate_section
    def create_adts(self, typedefs):
        for typedef in typedefs:
            adt = typedef.typ
            superclass_name = "ADT{}".format(adt.type_name)
            self.emit("class {}(ADT):".format(superclass_name))
            self.emit(self.docstring("ADT superclass."), d=4)
            self.emit("    pass")
            self.newline()

            for constructor in adt.constructors:
                constructor_name = "ADT{}".format(constructor.identifier)
                self.emit("class {}({}):".format(constructor_name,
                                                 superclass_name))
                varnames = ["v{}".format(i)
                            for i, _ in enumerate(constructor.parameters)]

                self.newline()
                if varnames:
                    self.emit("    def __init__(self, {}):".format(", ".join(varnames)))
                    self.emit("        super().__init__([{}])".format(", ".join(v for v in varnames)))
                else:
                    self.emit("    def __init__(self):".format(", ".join(varnames)))
                    self.emit("        super().__init__([])")

                self.newline()

                self.emit("    def __eq__(self, other):")
                self.emit("        if not isinstance(other, self.__class__):")
                self.emit("            return False")
                self.emit("        return all(x == y for x, y in zip(self.params, other.params))")
                self.newline()

                self.emit("    def __str__(self):")
                self.emit("        name = type(self).__name__[3:]")
                if varnames:
                    self.emit("        vars = [str(x) for x in self.params]")
                    self.emit("        return \"({} {})\".format(name, \" \".join(vars))")
                else:
                    self.emit("        return name")

                self.newline()

                s = ""
                for var in varnames:
                    s += "lambda {}: ".format(var)
                self.emit("{} = {}{}({})".format(constructor.identifier,
                                                        s,
                                                        constructor_name,
                                                        ", ".join(varnames)))
                self.newline()

    py_compile = get_registry_function(registered_index=1) # 1 to skip self

    @py_compile.register(CoreBind)
    def py_compile_bind(self, node, indent):
        if isinstance(node.bindee, CoreLambda):
            lam = node.bindee
            self.emit("def {}({}):".format(node.identifier,
                                           self.py_compile(lam.param, indent)),
                      d=indent)
            return_statement = self.py_compile(lam.expr, indent+4)
            self.emit("return {}".format(return_statement), d=indent+4)
            self.newline()
        else:
            # if it's not a function bind, it must be a value bind.
            val = node.bindee
            self.emit("{} = {}".format(node.identifier,
                                       self.py_compile(val, indent)),
                      d=indent)

    @py_compile.register(CoreCons)
    def py_compile_cons(self, node, indent):
        vs = []
        for parameter in node.parameters:
            if isinstance(parameter, CoreVariable):
                vs.append("FreeVariable({})".format(parameter.identifier))
            else:
                pass
        return "ADT{}".format(node.constructor)

    @py_compile.register(CoreVariable)
    def py_compile_variable(self, node, indent):
        return node.identifier

    @py_compile.register(CoreLiteral)
    def py_compile_literal(self, node, indent):
        return str(node.value)

    @py_compile.register(CoreApplication)
    def py_compile_application(self, node, indent):
        if isinstance(node.expr, CoreVariable) and \
           node.expr.identifier in builtins:
            f = builtins[node.expr.identifier]
        else:
            f = self.py_compile(node.expr, indent)
        return "({})({})".format(f, self.py_compile(node.arg, indent))

    @py_compile.register(CoreLambda)
    def py_compile_lambda(self, node, indent):
        param = self.py_compile(node.param, indent)
        expr = self.py_compile(node.expr, indent)
        return "lambda {}: {}".format(param, expr)

    @py_compile.register(CoreLet)
    def py_compile_let(self, node, indent):
        for bind in node.binds:
            self.py_compile(bind, indent)
        return self.py_compile(node.expr, indent)

    @py_compile.register(CoreMatch)
    def py_compile_match(self, node, indent):
        scrutinee = self.py_compile(node.scrutinee, indent)
        d = {}
        for alt in node.alts:
            if not alt.expr: continue
            k = self.py_compile(alt.altcon, indent)
            v = self.py_compile(alt.expr, indent)
            if isinstance(alt.altcon, CoreCons) and alt.altcon.parameters:
                v = "lambda {}: lambda: {}".format(
                    ", ".join(self.py_compile(x, indent) for x in alt.altcon.parameters),
                    v,
                )
            else:
                v = "lambda: {}".format(v)
            d[k] = v

        wildcard = None
        if "_" in d:
            wildcard = d["_"]
            del d["_"]

        match = "__match({}, {{{}}}, {})".format(scrutinee,
                                                         ", ".join(
            "{} : {}".format(k, v) for k, v in d.items()),
            wildcard
        )
        return match

    @annotate_section
    def emit_main(self, main):
        self.emit("def main():")
        self.emit("print({})".format(main), d=4)
        self.newline()
        self.emit("if __name__ == \"__main__\":")
        self.emit("    main()")

    def do_generate_code(self, core_tree, typedefs):
        self.program = ""
        self.code_header()
        self.code_runtime()
        self.create_adts(typedefs)
        main = self.py_compile(core_tree, 0)

        self.emit_main(main)
        return self.program[:]
