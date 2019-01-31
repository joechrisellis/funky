from funky.generate.gen import CodeGenerator, annotate_section

class CCodeGenerator(CodeGenerator):
    
    def __init__(self):
        super().__init__()

    @annotate_section
    def includes(self):
        self.emit("#include <stdlib.h>")
        self.emit("#include <stdio.h>")
        self.emit("#include <runtime.h>")

    @annotate_section
    def default_storage(self):
        self.emit("Value __add;")
        self.emit("Value __subtract;")
        self.emit("Value __times;")
        self.emit("Value __divide;")
        self.emit("Value __print;")
        self.emit("Value __numEqual;")

    def code_header(self):
        self.includes()
        self.default_storage()

    def create_environments(self):
        pass

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

    @annotate_section
    def primitive_procedures(self):
        self.emit("""Value __prim_add(Value e, Value a, Value b) {
    return MakeInt(a.z.value + a.z.value);
}""")
        self.newline()
        self.emit("""Value __prim_subtract(Value e, Value a, Value b) {
    return MakeInt(a.z.value - b.z.value);
}""")
        self.newline()
        self.emit("""Value __prim_times(Value e, Value a, Value b) {
    return MakeInt(a.z.value * b.z.value);
}""")
        self.newline()
        self.emit("""Value __prim_divide(Value e, Value a, Value b) {
    return MakeInt(a.z.value / b.z.value);
}""")
        self.newline()
        self.emit("""Value __prim_print(Value e, Value v) {
    printf("%i\\n", v.z.value);
    return v;
}""")
        self.newline()
        self.emit("""Value __prim_numEqual(Value e, Value a, Value b) {
    return MakeBoolean(a.z.value == b.z.value);
}""")

    def comment(self, s):
        self.emit("/* {} */".format(s))

    def do_generate_code(self, core_tree, typedefs):
        self.program = ""
        self.code_header()
        self.create_environments()
        self.create_adts(typedefs)

        # compile core_tree

        self.primitive_procedures()
        return self.program[:]
