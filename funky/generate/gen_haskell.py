import logging

from funky.corelang.coretree import *
from funky.corelang.builtins import String
from funky.generate.gen import CodeGenerator, annotate_section
from funky.util import get_registry_function, global_counter

log = logging.getLogger(__name__)

builtins = {
    "=="      :  "==",
    "!="      :  "/=",
    "<"       :  "<",
    "<="      :  "<=",
    ">"       :  ">",
    ">="      :  ">=",
    "**"      :  "**",
    "+"       :  "+",
    "++"      :  "++",
    "-"       :  "-",
    "negate"  :  "negate",
    "*"       :  "*",
    "/"       :  "/",
    "%"       :  "mod",
    "and"     :  "&&",
    "or"      :  "||",
}

class HaskellCodeGenerator(CodeGenerator):

    comment = "-- {}".format

    def __init__(self):
        super().__init__("Haskell")

        # this set contains the names that are known to be constructors so that
        # we do not convert them to lowercase when compiling CoreVariables.
        self.constructor_names = set()

    @annotate_section
    def create_adts(self, typedefs):
        for typedef in typedefs:
            adt = typedef.typ

            ind = 0
            for i, constructor in enumerate(adt.constructors):
                params = " ".join(constructor.parameters)
                if i == 0:
                    definition = "data {}".format(adt.type_name)
                    ind = len(definition) + 1
                    line = "{} = {} {}".format(definition,
                                               constructor.identifier,
                                               params)
                    self.emit(line)
                else:
                    line = "| {} {}".format(constructor.identifier, params)
                    self.emit(line, d=ind)
                self.constructor_names.add(constructor.identifier)

            self.emit("deriving (Show, Eq)", d=ind)
            self.newline()

    hs_compile = get_registry_function(registered_index=1) # 1 to skip self

    @hs_compile.register(CoreBind)
    def hs_compile_bind(self, node):
        return "{} = {}".format(node.identifier,
                                self.hs_compile(node.bindee))

    @hs_compile.register(CoreCons)
    def hs_compile_cons(self, node):
        params = " ".join(self.hs_compile(p) for p in node.parameters)
        return "{} {}".format(node.constructor, params)

    @hs_compile.register(CoreVariable)
    def hs_compile_variable(self, node):
        ident = node.identifier
        try:
            return builtins[ident]
        except KeyError:
            if node.identifier not in self.constructor_names:
                ident = ident.lower()
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

    @annotate_section
    def emit_main(self, expr):
        self.emit("main = do")
        self.emit("       print ({})".format(self.hs_compile(expr)))

    def do_generate_code(self, core_tree, typedefs):
        """Generates Haskell code from the core tree and type definitions.
        
        :param core_tree: the type-checked core tree from the desugarer
        :param typedefs:  the typedefs from the desugarer
        :return:          the generated Haskell code as a string
        :rtype:           str
        """

        log.info("Generating {} code...".format(self.lang_name))
        self.program = ""
        self.code_header()

        log.info("Creating user-defined data structres...")
        self.create_adts(typedefs)
        log.info("Done.")
        log.info("Compiling core tree...")
        
        for bind in core_tree.binds:
            compiled_bind = self.hs_compile(bind)
            self.emit(compiled_bind)
        self.newline()

        log.info("Done.")

        log.info("Creating main method...")
        self.emit_main(core_tree.expr)
        log.info("Done.")

        log.info("Done generating {} code.".format(self.lang_name))
        return self.program[:]
