from keyword import kwlist
import logging

from funky.corelang.coretree import *
from funky.corelang.builtins import String
from funky.generate.gen import CodeGenerator, CodeSection
from funky.generate.runtime.python_runtime import PythonRuntime
from funky.util import get_registry_function, global_counter

log = logging.getLogger(__name__)

base_runtime = """class ADT:
    \"\"\"Superclass for all ADTs.\"\"\"

    def __init__(self, params):
        self.params = params

class InexhaustivePatternMatchError(Exception):
    pass

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
            return expr"""

class PythonCodeGenerator(CodeGenerator):

    def __init__(self):
        super().__init__("Python", "# {}".format)
        self.runtime = PythonRuntime()

    def make_base_runtime(self):
        runtime_section = CodeSection("base runtime")
        runtime_section.emit(base_runtime)
        runtime_section.newline()
        return runtime_section

    def make_used_runtime(self):
        return self.runtime.get_runtime()

    def make_adts(self, typedefs):
        adts = CodeSection("algebraic data types")
        for typedef in typedefs:
            adt = typedef.typ
            superclass_name = "ADT{}".format(adt.type_name)
            adts.emit(self.comment("ADT superclass."))
            adts.emit("class {}(ADT):".format(superclass_name))
            adts.emit("    pass")
            adts.newline()

            for constructor in adt.constructors:
                constructor_name = "ADT{}".format(constructor.identifier)
                adts.emit("class {}({}):".format(constructor_name,
                                                 superclass_name))
                varnames = ["v{}".format(i)
                            for i, _ in enumerate(constructor.parameters)]

                self.newline()
                if varnames:
                    adts.emit("    def __init__(self, {}):".format(", ".join(varnames)))
                    adts.emit("        super().__init__([{}])".format(", ".join(v for v in varnames)))
                else:
                    adts.emit("    def __init__(self):".format(", ".join(varnames)))
                    adts.emit("        super().__init__([])")

                adts.newline()

                adts.emit("    def __eq__(self, other):")
                adts.emit("        if not isinstance(other, self.__class__):")
                adts.emit("            return False")
                adts.emit("        return all(x == y for x, y in zip(self.params, other.params))")
                adts.newline()

                adts.emit("    def __repr__(self):")
                adts.emit("        name = type(self).__name__[3:]")
                if varnames:
                    adts.emit("        vars = [repr(x) for x in self.params]")
                    adts.emit("        return \"({} {})\".format(name, \" \".join(vars))")
                else:
                    adts.emit("        return name")

                adts.newline()

                s = ""
                for var in varnames:
                    s += "lambda {}: ".format(var)

                if constructor.identifier in kwlist:
                    py_name = "__{}".format(constructor.identifier)
                else:
                    py_name = constructor.identifier
                adts.emit("{} = {}{}({})".format(py_name,
                                                 s,
                                                 constructor_name,
                                                 ", ".join(varnames)))
                adts.newline()

        return adts

    py_compile = get_registry_function(registered_index=1) # 1 to skip self

    @py_compile.register(CoreBind)
    def py_compile_bind(self, node, sect, indent):
        if isinstance(node.bindee, CoreLambda):
            lam = node.bindee
            sect.emit("def {}({}):".format(node.identifier,
                                           self.py_compile(lam.param, indent)),
                      d=indent)
            return_statement = self.py_compile(lam.expr, sect, indent+4)
            sect.emit("return {}".format(return_statement), d=indent+4)
            sect.newline()
        else:
            # if it's not a function bind, it must be a value bind.
            val = node.bindee
            sect.emit("{} = {}".format(node.identifier,
                                       self.py_compile(val, sect, indent)),
                      d=indent)

    @py_compile.register(CoreCons)
    def py_compile_cons(self, node, sect, indent):
        return "ADT{}".format(node.constructor)

    @py_compile.register(CoreVariable)
    def py_compile_variable(self, node, sect, indent):
        try:
            return self.runtime.runtime_method(node.identifier)
        except KeyError:
            if node.identifier in kwlist:
                return "__{}".format(node.identifier)
            return node.identifier

    @py_compile.register(CoreLiteral)
    def py_compile_literal(self, node, sect, indent):
        if node.inferred_type == String:
            return "\"{}\"".format(node.value)
        else:
            return str(node.value)

    @py_compile.register(CoreApplication)
    def py_compile_application(self, node, sect, indent):
        f = self.py_compile(node.expr, sect, indent)
        return "({})({})".format(f, self.py_compile(node.arg, sect, indent))

    @py_compile.register(CoreLambda)
    def py_compile_lambda(self, node, sect, indent):
        param = self.py_compile(node.param, sect, indent)
        differentiator = str(global_counter())
        lam_name = "lam{}".forme(differentiator)
        sect.emit("def {}({}):".format(lam_name, param), d=indent)
        expr = self.py_compile(node.expr, sect, indent + 4)
        sect.emit("return {}".format(expr), d=indent+4)
        return lam_name

    @py_compile.register(CoreLet)
    def py_compile_let(self, node, sect, indent):
        for bind in node.binds:
            self.py_compile(bind, sect, indent)
        return self.py_compile(node.expr, sect, indent)

    @py_compile.register(CoreMatch)
    def py_compile_match(self, node, sect, indent):
        scrutinee = self.py_compile(node.scrutinee, sect, indent)
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
                sect.emit("def {}({}):".format(fname, ", ".join(params)),
                          d=indent)
            else:
                sect.emit("def {}():".format(fname), d=indent)
                if isinstance(alt.altcon, CoreVariable) and \
                   alt.altcon.identifier != "_":
                    sect.emit("{} = {}".format(alt.altcon.identifier, scrutinee),
                              d=indent+4)

            k = self.py_compile(alt.altcon, sect, indent+4)
            v = self.py_compile(alt.expr, sect, indent=indent+4)

            if isinstance(alt.altcon, CoreVariable):
                default = fname
            else:
                d[k] = fname
            sect.emit("return {}".format(v), d=indent+4)

        return "__match({}, {{{}}}, {})".format(
            scrutinee,
            ", ".join("{} : {}".format(k, v) for k, v in d.items()),
            default,
        )

    def emit_main(self, main):
        main_section = CodeSection("main method")

        main_section.emit("def main():")
        main_section.emit("print({})".format(main), d=4)
        main_section.newline()
        main_section.emit("if __name__ == \"__main__\":")
        main_section.emit("    main()")

        return main_section

    def do_generate_code(self, core_tree, typedefs):
        """Generates Python code from the core tree and type definitions.
        
        :param core_tree: the type-checked core tree from the desugarer
        :param typedefs:  the typedefs from the desugarer
        :return:          the generated Python code as a string
        :rtype:           str
        """

        log.info("Generating {} code...".format(self.lang_name))
        self.program.reset()

        header_section = self.code_header()
        base_runtime_section = self.make_base_runtime()

        log.info("Creating user-defined data structres...")
        adts_section = self.make_adts(typedefs)
        log.info("Done.")
        log.info("Compiling core tree...")
        core_section = CodeSection("core code")
        main = self.py_compile(core_tree, core_section,  0)
        log.info("Done.")

        log.info("Creating main method...")
        main_section = self.emit_main(main)
        log.info("Done.")

        used_runtime_section = self.make_used_runtime()

        for i, section in enumerate([header_section, base_runtime_section,
                                     used_runtime_section, adts_section,
                                     core_section, main_section]):
            self.program.add_section(section, i)

        log.info("Done generating {} code.".format(self.lang_name))
        return self.program.get_code()
