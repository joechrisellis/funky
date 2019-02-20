import logging

from funky.corelang.coretree import *
from funky.generate.gen import CodeGenerator, annotate_section
from funky.util import get_registry_function, global_counter

log = logging.getLogger(__name__)

c_runtime = """struct Integer;
struct Boolean;
struct Closure;
union  Value;

enum Tag { VOID, INTEGER, BOOLEAN, CLOSURE, ENV };

typedef union Value (*Lambda)() ;

struct Integer { enum Tag t; int value;               };
struct Boolean { enum Tag t; unsigned int value;      };
struct Closure { enum Tag t; Lambda lam; void* env;   };
struct Env     { enum Tag t; void* env;               };

union Value {
    enum   Tag     t;
    struct Integer z;
    struct Boolean b;
    struct Closure clo;
    struct Env     env;
};

typedef union Value Value;

static Value MakeClosure(Lambda lam, Value env) {
    Value v;
    v.clo.t    =  CLOSURE;
    v.clo.lam  =  lam;
    v.clo.env  =  env.env.env;
    return v;
}

static Value MakeInteger(int n) {
    Value v;
    v.z.t      =  INTEGER;
    v.z.value  =  n;
    return v;
}

static Value MakeBoolean(unsigned int b) {
    Value v;
    v.b.t      =  BOOLEAN;
    v.b.value  =  b;
    return v;
}

static Value MakePrimitive(Lambda prim) {
    Value v;
    v.clo.t    =  CLOSURE;
    v.clo.lam  =  prim;

Value __prim_add(Value e, Value a, Value b) {
    return MakeInt(a.z.value + a.z.value);
}

Value __prim_subtract(Value e, Value a, Value b) {
    return MakeInt(a.z.value - b.z.value);
}

Value __prim_times(Value e, Value a, Value b) {
    return MakeInt(a.z.value * b.z.value);
}

Value __prim_divide(Value e, Value a, Value b) {
    return MakeInt(a.z.value / b.z.value);
}

Value __prim_print(Value e, Value v) {
    printf("%i\\n", v.z.value);
    return v;
}

Value __prim_numEqual(Value e, Value a, Value b) {
    return MakeBoolean(a.z.value == b.z.value);
}"""

class CCodeGenerator(CodeGenerator):

    comment = "// {}".format
    
    def __init__(self):
        super().__init__("C")

    @annotate_section
    def includes(self):
        self.emit("#include <stdlib.h>")
        self.emit("#include <stdio.h>")

    @annotate_section
    def runtime(self):
        self.emit(c_runtime)

    @annotate_section
    def default_storage(self):
        self.emit("Value __add;")
        self.emit("Value __subtract;")
        self.emit("Value __times;")
        self.emit("Value __divide;")
        self.emit("Value __print;")
        self.emit("Value __numEqual;")

    @annotate_section
    def create_adts(self, typedefs):
        names = [typedef.typ.type_name for typedef in typedefs]
        for typedef in typedefs:
            adt = typedef.typ

            struct_name = adt.type_name
            enum_name  = "{}_TAG".format(struct_name.upper())

            self.emit("enum {} {{".format(enum_name))
            for constructor in adt.constructors:
                self.emit("    {},".format(constructor.identifier.upper()))
            self.emit("};")
            self.emit("")
            
            self.emit("struct {} {{".format(struct_name))
            self.emit("    enum {} tag;".format(enum_name))
            self.emit("    union {")
            for constructor in adt.constructors:
                if not constructor.parameters: continue
                self.emit("        struct {")
                for i, parameter in enumerate(constructor.parameters):
                    varname = "v{}".format(i)
                    if parameter in names:
                        self.emit("            struct {} *{};".format(parameter, varname))
                    else:
                        self.emit("            Value {};".format(varname))
                self.emit("        };")
            self.emit("    };")
            self.emit("}};".format(struct_name))
            self.emit("")

            for constructor in adt.constructors:
                params = ["v{}".format(i) for i, _ in enumerate(constructor.parameters)]
                self.emit("struct *{} __get_{}({}) {{".format(struct_name, constructor.identifier,
                                                         ", ".join("Value {}".format(p) for p in params)))
                self.emit("    struct {} *x = malloc(sizeof(struct {}));".format(struct_name, struct_name))
                self.emit("    x->tag = {};".format(constructor.identifier.upper()))
                self.emit("\n".join("    x->v{} = v{};".format(i, i) for i, _ in enumerate(constructor.parameters)))
                self.emit("    return x;")
                self.emit("}")
                self.emit("")

    def do_generate_code(self, core_tree, typedefs):
        """Generates C code from the core tree and type definitions.
        
        :param core_tree: the type-checked core tree from the desugarer
        :param typedefs:  the typedefs from the desugarer
        :return:          the generated C code as a string
        :rtype:           str
        """

        log.info("Generating {} code...".format(self.lang_name))
        self.program = ""

        self.includes()
        self.newline()
        self.runtime()
        self.newline()
        self.default_storage()
        self.newline()

        log.info("Creating user-defined data structres...")
        self.create_adts(typedefs)
        log.info("Done.")
        log.info("Compiling core tree...")
        log.info("Done.")

        log.info("Done generating {} code.".format(self.lang_name))
        return self.program[:]
