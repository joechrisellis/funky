from keyword import kwlist
import logging

from funky.corelang.coretree import *
from funky.generate.gen import CodeGenerator, annotate_section
from funky.util import get_registry_function, global_counter

log = logging.getLogger(__name__)

python_runtime = """class ADT:
    \"\"\"Superclass for all ADTs.\"\"\"

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
    "and"     :  "__logical_and",
    "or"      :  "__logical_or",
}

class PythonCodeGenerator(CodeGenerator):

    docstring = "\"\"\"{}\"\"\"".format
    comment = "# {}".format

    def __init__(self):
        super().__init__("Python")

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

                if constructor.identifier in kwlist:
                    py_name = "__{}".format(constructor.identifier)
                else:
                    py_name = constructor.identifier
                self.emit("{} = {}{}({})".format(py_name,
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
        return "ADT{}".format(node.constructor)

    @py_compile.register(CoreVariable)
    def py_compile_variable(self, node, indent):
        if node.identifier in kwlist:
            return "__{}".format(node.identifier)
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
        differentiator = str(global_counter())
        lam_name = "lam{}".format(differentiator)
        self.emit("def {}({}):".format(lam_name, param), d=indent)
        expr = self.py_compile(node.expr, indent + 4)
        self.emit("return {}".format(expr), d=indent+4)
        return lam_name

    @py_compile.register(CoreLet)
    def py_compile_let(self, node, indent):
        for bind in node.binds:
            self.py_compile(bind, indent)
        return self.py_compile(node.expr, indent)

    @py_compile.register(CoreMatch)
    def py_compile_match(self, node, indent):
        scrutinee = self.py_compile(node.scrutinee, indent)
        d = {}
        default = None
        for i, alt in enumerate(node.alts):
            if not alt.expr: continue
            fname = "m{}".format(i)

            if isinstance(alt.altcon, CoreCons):
                params = []
                for i, v in enumerate(alt.altcon.parameters):
                    name = v.identifier
                    if name == "_":
                        name += str(i)
                    params.append(name)
                self.emit("def {}({}):".format(fname, ", ".join(params)),
                          d=indent)
            else:
                self.emit("def {}():".format(fname), d=indent)

            k = self.py_compile(alt.altcon, indent+4)
            v = self.py_compile(alt.expr, indent=indent+4)

            if isinstance(alt.altcon, CoreVariable):
                default = fname
            else:
                d[k] = fname
            self.emit("return {}".format(v), d=indent+4)

        return "__match({}, {{{}}}, {})".format(
            scrutinee,
            ", ".join("{} : {}".format(k, v) for k, v in d.items()),
            default,
        )

    @annotate_section
    def emit_main(self, main):
        self.emit("def main():")
        self.emit("print({})".format(main), d=4)
        self.newline()
        self.emit("if __name__ == \"__main__\":")
        self.emit("    main()")

    def do_generate_code(self, core_tree, typedefs):
        """Generates Python code from the core tree and type definitions.
        
        :param core_tree: the type-checked core tree from the desugarer
        :param typedefs:  the typedefs from the desugarer
        :return:          the generated Python code as a string
        :rtype:           str
        """

        log.info("Generating {} code...".format(self.lang_name))
        self.program = ""
        self.code_header()
        self.code_runtime()

        log.info("Creating user-defined data structres...")
        self.create_adts(typedefs)
        log.info("Done.")
        log.info("Compiling core tree...")
        main = self.py_compile(core_tree, 0)
        log.info("Done.")

        log.info("Creating main method...")
        self.emit_main(main)
        log.info("Done.")

        log.info("Done generating {} code.".format(self.lang_name))
        return self.program[:]
