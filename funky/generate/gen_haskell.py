import logging

from funky.corelang.coretree import *
from funky.corelang.types import *
from funky.corelang.builtins import String
from funky.generate.gen import CodeGenerator, CodeSection
from funky.generate.runtime.haskell_runtime import HaskellRuntime
from funky.util import get_registry_function, global_counter

log = logging.getLogger(__name__)

class HaskellCodeGenerator(CodeGenerator):

    comment = "-- {}".format

    def __init__(self):
        super().__init__("Haskell", "-- {}".format)
        self.runtime = HaskellRuntime()

        # this set contains the names that are known to be constructors so that
        # we do not convert them to lowercase when compiling CoreVariables.
        self.constructor_names = set()

    def funky_type_to_haskell(self, t, adt_names):
        if isinstance(t, FunctionType):
            return "({} -> {})".format(self.funky_type_to_haskell(t.input_type, adt_names),
                                     self.funky_type_to_haskell(t.output_type, adt_names))
        else:
            ident = str(t)
            if ident in adt_names:
                ident = "{}{}".format(self.ADT_PREFIX, ident)
            return ident

    ADT_PREFIX = "ADT"
    def make_adts(self, typedefs):
        adts = CodeSection("algebraic data types")

        adt_names = set()
        for typedef in typedefs:
            adt = typedef.typ
            adt_names.add(adt.type_name)
            
            # If true, this ADT contains a function type somewhere, and
            # therefore cannot derive Show or Eq.
            has_function = False

            ind = 0
            for i, constructor in enumerate(adt.constructors):
                
                params = []
                for p in constructor.parameters:
                    pstring = self.funky_type_to_haskell(p, adt_names)
                    if "->" in pstring: has_function = True
                    params.append(pstring)
                params = " ".join(params)

                if i == 0:
                    definition = "data {}{}".format(self.ADT_PREFIX, adt.type_name)
                    ind = len(definition) + 1
                    line = "{} = {}{} {}".format(definition,
                                               self.ADT_PREFIX,
                                               constructor.identifier,
                                               params)
                    adts.emit(line)
                else:
                    line = "| {}{} {}".format(self.ADT_PREFIX,
                                              constructor.identifier,
                                              params)
                    adts.emit(line, d=ind)
                self.constructor_names.add(constructor.identifier)

            if not has_function:
                adts.emit("deriving (Show, Eq)", d=ind)

            adts.newline()

        return adts

    def make_used_runtime(self):
        return self.runtime.get_runtime()

    hs_compile = get_registry_function(registered_index=1) # 1 to skip self

    @hs_compile.register(CoreBind)
    def hs_compile_bind(self, node):
        return "{} = {}".format(node.identifier,
                                self.hs_compile(node.bindee))

    @hs_compile.register(CoreCons)
    def hs_compile_cons(self, node):
        params = " ".join(self.hs_compile(p) for p in node.parameters)
        return "{}{} {}".format(self.ADT_PREFIX, node.constructor, params)

    @hs_compile.register(CoreVariable)
    def hs_compile_variable(self, node):
        ident = node.identifier
        try:
            return self.runtime.runtime_method(ident)
        except KeyError:
            if node.identifier not in self.constructor_names:
                ident = ident.lower()
            else:
                ident = "{}{}".format(self.ADT_PREFIX, ident)
            return ident

    @hs_compile.register(CoreLiteral)
    def hs_compile_literal(self, node):
        if node.inferred_type == String:
            return "\"{}\"".format(node.value)
        else:
            return str(node.value)

    @hs_compile.register(CoreApplication)
    def hs_compile_application(self, node):
        f = self.hs_compile(node.expr)
        return "({})({})".format(f, self.hs_compile(node.arg))

    @hs_compile.register(CoreLambda)
    def hs_compile_lambda(self, node):
        return "\{} -> {}".format(node.param.identifier,
                                  self.hs_compile(node.expr))

    @hs_compile.register(CoreLet)
    def hs_compile_let(self, node):
        binds = "; ".join(self.hs_compile(bind) for bind in node.binds)
        expr = self.hs_compile(node.expr)
        return "let {{ {} }} in {}".format(binds, expr)

    @hs_compile.register(CoreMatch)
    def hs_compile_match(self, node):
        scrutinee = self.hs_compile(node.scrutinee)

        alts = []
        for alt in node.alts:
            compiled_altcon = self.hs_compile(alt.altcon)
            if not alt.expr:
                alts.append("{} -> undefined".format(compiled_altcon))
                continue
            compiled_expr = self.hs_compile(alt.expr)
            alts.append("{} -> {}".format(compiled_altcon, compiled_expr))

        return "case {} of {{ {} }}".format(scrutinee, "; ".join(alts))

    def make_core_section(self, core_tree):
        core_section = CodeSection("core section")
        for bind in core_tree.binds:
            compiled_bind = self.hs_compile(bind)
            core_section.emit(compiled_bind)
        core_section.newline()
        return core_section

    def make_main_section(self, expr):
        main_section = CodeSection("main")
        main_section.emit("main = do")
        main_section.emit("       print ({})".format(self.hs_compile(expr)))
        return main_section

    def do_generate_code(self, core_tree, typedefs):
        """Generates Haskell code from the core tree and type definitions.
        
        :param core_tree: the type-checked core tree from the desugarer
        :param typedefs:  the typedefs from the desugarer
        :return:          the generated Haskell code as a string
        :rtype:           str
        """

        import funky.globals
        funky.globals.USE_UNICODE = False
        funky.globals.USE_COLORS  = False

        super().do_generate_code(core_tree, typedefs)

        log.info("Generating {} code...".format(self.lang_name))
        self.program.reset()
        self.runtime.reset()

        header_section = self.code_header()

        log.info("Creating user-defined data structres...")
        adts = self.make_adts(typedefs)
        log.info("Done.")

        log.info("Compiling core tree...")
        core_section = self.make_core_section(core_tree)
        log.info("Done.")

        log.info("Creating main method...")
        main_section = self.make_main_section(core_tree.expr)
        log.info("Done.")

        log.info("Creating used runtime section...")
        used_runtime_section = self.make_used_runtime()
        log.info("Done.")

        for i, section in enumerate([header_section, used_runtime_section,
                                     adts, core_section, main_section]):
            self.program.add_section(section, i)

        log.info("Done generating {} code.".format(self.lang_name))
        return self.program.get_code()
