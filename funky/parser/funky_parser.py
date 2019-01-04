import ply.yacc as yacc

from funky.util import err
from funky.parser.funky_lexer import FunkyLexer, IndentationLexer
from funky.parser import FunkySyntaxError
from funky.parser.fixity import resolve_fixity

from funky.parser.ast import Module, ProgramBody, ImportStatement,             \
                             NewTypeStatement, TypeDeclaration, Type,          \
                             TupleType, ListType, FunctionType,                \
                             FunctionDefinition, FunctionLHS, FunctionRHS,     \
                             GuardedExpression, PatternDefinition,             \
                             ConstructorChain, Pattern, PatternTuple,          \
                             PatternList, Alternative, Lambda, Let, Match,     \
                             FunctionApplication, Tuple, List, Literal,        \
                             Parameter, UsedVar, InfixExpression

class FunkyParser:

    tokens      =  FunkyLexer.tokens
    start       =  "MODULE_DEFINITION"

    def p_MODULE_DEFINITION(self, p):
        """MODULE_DEFINITION : MODULE IDENTIFIER WHERE BODY
        """
        module_id, body = p[2], p[4]
        p[0] = Module(module_id, body)

    def p_BODY(self, p):
        """BODY : OPEN_BRACE IMPORT_DECLARATIONS ENDSTATEMENT TOP_DECLARATIONS CLOSE_BRACE
                | OPEN_BRACE TOP_DECLARATIONS CLOSE_BRACE
        """
        if len(p) == 6:
            imports, top_declarations = p[2], p[4]
        else:
            imports, top_declarations = [], p[2]

        imports = [i for i in imports if i]
        top_declarations = [t for t in top_declarations if t]
        p[0] = ProgramBody(imports, top_declarations)

    def p_IMPORT_DECLARATIONS(self, p):
        """IMPORT_DECLARATIONS : IMPORT_DECLARATIONS ENDSTATEMENT IMPORT_DECLARATION
                               | IMPORT_DECLARATION
        """
        if len(p) == 4:
            p[0] = p[1] + [p[3]]
        else:
            p[0] = [p[1]]

    def p_IMPORT_DECLARATION(self, p):
        """IMPORT_DECLARATION : IMPORT IDENTIFIER
        """
        p[0] = ImportStatement(p[2])

    def p_TOP_DECLARATIONS(self, p):
        """TOP_DECLARATIONS : TOP_DECLARATIONS ENDSTATEMENT TOP_DECLARATION
                            | TOP_DECLARATION
        """
        if len(p) == 4:
            p[0] = p[1] + [p[3]]
        else:
            p[0] =[p[1]]

    def p_TOP_DECLARATION(self, p):
        """TOP_DECLARATION : NEWTYPE TYPENAME EQUALS TYPE
                           | DECLARATION
        """
        if len(p) == 5:
            p[0] = NewTypeStatement(p[2], p[4])
        else:
            p[0] = p[1]

    def p_DECLARATIONS(self, p):
        """DECLARATIONS : OPEN_BRACE DECLARATIONS_LIST CLOSE_BRACE
                        | OPEN_BRACE CLOSE_BRACE
        """
        if len(p) == 4:
            p[0] = p[2]
        else:
            p[0] = []

    def p_DECLARATIONS_LIST(self, p):
        """DECLARATIONS_LIST : DECLARATION ENDSTATEMENT DECLARATIONS_LIST
                             | DECLARATION
        """
        if len(p) == 4:
            p[0] = [p[1]] + p[3]
        else:
            p[0] = [p[1]]

    def p_DECLARATION(self, p):
        """DECLARATION : GEN_DECLARATION
                       | FUNCTION_LHS RHS
                       | PAT RHS
        """
        if len(p) == 2:
            p[0] = p[1]
        elif type(p[1]) == FunctionLHS:
            p[0] = FunctionDefinition(p[1], p[2])
        else:
            p[0] = PatternDefinition(p[1], p[2])

    def p_GEN_DECLARATION(self, p):
        """GEN_DECLARATION : IDENTIFIER TYPESIG TYPE
                           |
        """
        # NOTE: Fixity declarations removed -- may not be needed for this
        #       project.
        if len(p) == 4:
            p[0] = TypeDeclaration(p[1], p[3])

    def p_TYPE(self, p):
        """TYPE : ATYPE
                | ATYPE ARROW TYPE
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = FunctionType(p[1], p[3])

    def p_ATYPE(self, p):
        """ATYPE : TYPENAME
                 | OPEN_PAREN TYPES_LIST CLOSE_PAREN
                 | OPEN_PAREN TYPE CLOSE_PAREN
                 | OPEN_SQUARE TYPE CLOSE_SQUARE
        """
        if len(p) == 2:
            p[0] = Type(p[1])
        elif p[1] == "(":
            if type(p[2]) == list:
                p[0] = TupleType(tuple(p[2]))
            else:
                p[0] = p[2]
        else:
            p[0] = ListType(p[2])

    def p_FUNCTION_LHS(self, p):
        """FUNCTION_LHS : IDENTIFIER APAT APATS
                        | PAT VAROP PAT
                        | OPEN_PAREN FUNCTION_LHS CLOSE_PAREN APAT APATS
        """
        if type(p[1]) in [Pattern, ConstructorChain]:
            p[0] = FunctionLHS(p[2], [p[1], p[3]])
        elif p[1] == "(":
            p[0] = p[2]
            p[0].parameters.append(p[4])
            p[0].parameters.extend(p[5])
        else:
            p[0] = FunctionLHS(p[1], [p[2], *p[3]])

    def p_RHS(self, p):
        """RHS : EQUALS EXP
               | EQUALS EXP WHERE DECLARATIONS
               | GDRHS
               | GDRHS WHERE DECLARATIONS
        """
        if len(p) == 3:
            p[0] = FunctionRHS([p[2]])
        elif len(p) == 5:
            p[0] = FunctionRHS([p[2]],
                               declarations=p[4])
        elif len(p) == 2:
            p[0] = FunctionRHS(p[1])
        else:
            p[0] = FunctionRHS(p[1], declarations=p[3])

    def p_GDRHS(self, p):
        """GDRHS : GUARDS EQUALS EXP
                 | GUARDS EQUALS EXP GDRHS
        """
        if len(p) == 4:
            p[0] = [GuardedExpression(p[1], p[3])]
        else:
            p[0] = [GuardedExpression(p[1], p[3])] + p[4]

    def p_GUARDS(self, p):
        """GUARDS : PIPE GUARD_LIST
        """
        p[0] = p[2]

    def p_GUARD_LIST(self, p):
        """GUARD_LIST : GUARD_LIST COMMA GUARD
                      | GUARD
        """
        if len(p) == 4:
            p[0] = p[1] + [p[3]]
        else:
            p[0] = [p[1]]

    def p_GUARD(self, p):
        """GUARD : INFIX_EXP
        """ # we only allow for BOOLEAN guards.
        p[0] = p[1]
        p[0] = resolve_fixity(p[0])

    def p_EXP(self, p):
        """EXP : INFIX_EXP
        """
        p[0] = p[1]
        p[0] = resolve_fixity(p[0])

    def p_INFIX_EXP(self, p):
        """INFIX_EXP : LEXP OP INFIX_EXP
                     | MINUS INFIX_EXP
                     | LEXP
        """
        # NOTE: we keep infix expressions FLAT for now -- we perform fixity
        # resolution at a later step.
        tokens = []
        if len(p) == 4:
            tokens.append(p[1])
            tokens.append(p[2])
            tokens.extend(p[3].tokens)
        elif len(p) == 3:
            tokens.append("-")
            tokens.extend(p[2].tokens)
        else:
            tokens.append(p[1])

        p[0] = InfixExpression(tokens)

    def p_LEXP(self, p):
        """LEXP : LAMBDA APAT APATS ARROW EXP
                | LET DECLARATIONS IN EXP
                | IF EXP THEN EXP ELSE EXP
                | MATCH EXP OF OPEN_BRACE ALTS CLOSE_BRACE
                | FEXP
        """
        if len(p) == 6:
            p[0] = Lambda([p[2], *p[3]], p[5])
        elif len(p) == 5:
            p[0] = Let(p[2], p[4])
        elif len(p) == 7:
            if p[1] == "if":
                p[0] = If(p[2], p[4], p[6])
            else:
                p[0] = Match(p[2], p[5])
        else:
            p[0] = p[1]

    def p_FEXP(self, p):
        """FEXP : FEXP AEXP
                | AEXP
        """
        if len(p) == 3:
            p[0] = FunctionApplication(p[1], p[2])
        else:
            p[0] = p[1]

    def p_AEXP(self, p):
        """AEXP : USED_VAR
                | GCON
                | LITERAL
                | OPEN_PAREN EXP CLOSE_PAREN
                | OPEN_PAREN EXP COMMA EXP_LIST CLOSE_PAREN
                | OPEN_SQUARE EXP CLOSE_SQUARE
                | OPEN_SQUARE EXP COMMA EXP_LIST CLOSE_SQUARE
        """
        if len(p) == 2:
            if p[1] == ():
                p[0] = PatternTuple(p[1])
            elif p[1] == []:
                p[0] = PatternTuple(p[1])
            else:
                p[0] = p[1]
        elif p[1] == "(":
            if len(p) == 4:
                p[0] = p[2]
            else:
                p[0] = Tuple((p[2], *p[4]))
        else:
            if len(p) == 4:
                p[0] = List([p[2]])
            else:
                p[0] = List([p[2], *p[4]])

    def p_ALTS(self, p):
        """ALTS : ALT ENDSTATEMENT ALTS
                | ALT
        """
        if len(p) == 4:
            p[0] = p[1] + p[3]
        else:
            p[0] = p[1]

    def p_ALT(self, p):
        """ALT : PAT ARROW EXP
               |
        """
        p[0] = [Alternative(p[1], p[3])] if len(p) == 4 else []

    def p_PAT(self, p):
        """PAT : LPAT CONSTRUCTOR PAT
               | LPAT
        """
        if len(p) == 4:
            p[0] = ConstructorChain(p[1], p[3])
        else:
            p[0] = p[1]

    def p_LPAT(self, p):
        """LPAT : APAT
                | MINUS OPEN_PAREN INTEGER CLOSE_PAREN
                | MINUS OPEN_PAREN FLOAT CLOSE_PAREN
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = Pattern(Literal(-p[3]))

    def p_APAT(self, p):
        """APAT : PARAM
                | GCON
                | LITERAL
                | OPEN_PAREN PAT CLOSE_PAREN
                | OPEN_PAREN PAT COMMA PAT_LIST CLOSE_PAREN
                | OPEN_SQUARE PAT_LIST CLOSE_SQUARE
        """
        if len(p) == 2:
            if p[1] == ():
                p[0] = PatternTuple(p[1])
            elif p[1] == []:
                p[0] = PatternList(p[1])
            else:
                p[0] = Pattern(p[1])
        elif len(p) == 4:
            p[0] = p[2]
        else:
            p[0] = PatternTuple((p[2], *p[4].patterns))

    def p_GCON(self, p):
        """GCON : OPEN_PAREN CLOSE_PAREN
                | OPEN_SQUARE CLOSE_SQUARE
        """
        if p[1] == "(":
            p[0] = ()
        else:
            p[0] = []

    def p_VAROP(self, p):
        """VAROP : VARSYM
                 | BACKTICK IDENTIFIER BACKTICK
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[2]

    def p_OP(self, p):
        """OP : VAROP
        """
        p[0] = p[1]

    def p_EXP_LIST(self, p):
        """EXP_LIST : EXP_LIST COMMA EXP
                    | EXP
        """
        if len(p) == 4:
            p[0] = p[1] + [p[3]]
        else:
            p[0] = [p[1]]

    def p_APATS(self, p):
        """APATS : APAT APATS
                 |
        """
        if len(p) == 1:
            p[0] = []
        else:
            p[0] = [p[1]] + p[2]

    def p_PAT_LIST(self, p):
        """PAT_LIST : PAT_LIST COMMA PAT
                    | PAT
        """
        if len(p) == 4:
            p[0] = p[1]
            p[0].patterns.append(p[3])
        else:
            p[0] = PatternList([p[1]])

    def p_VARSYM(self, p):
        """VARSYM : PLUS
                  | MINUS
                  | TIMES
                  | DIVIDE
                  | POW
                  | EQUALITY
                  | LESS
                  | LEQ
                  | GREATER
                  | GEQ
        """
        p[0] = p[1]

    def p_TYPES_LIST(self, p):
        """TYPES_LIST : TYPES_LIST COMMA TYPE
                      | TYPE
        """
        if len(p) == 4:
            p[0] = p[1] + [p[3]]
        else:
            p[0] = [p[1]]

    def p_LITERAL(self, p):
        """LITERAL : FLOAT
                   | INTEGER
                   | BOOL
                   | CHAR
                   | STRING
        """
        p[0] = Literal(p[1])

    def p_USED_VAR(self, p):
        """USED_VAR : IDENTIFIER"""
        p[0] = UsedVar(p[1])

    def p_PARAM(self, p):
        """PARAM : IDENTIFIER"""
        p[0] = Parameter(p[1])
    
    def p_error(self, p):
        raise FunkySyntaxError("Parsing failed at token {}".format(repr(p)))

    def build(self, **kwargs):
        self.lexer = FunkyLexer()
        self.lexer.build()
        self.lexer = IndentationLexer(self.lexer)
        self.parser = yacc.yacc(module=self, **kwargs)

    def do_parse(self, source):
        self.lexer.input(source)
        for tok in self.lexer:
            print(tok.value, end=" ")
        print()

        parsed = self.parser.parse(source, self.lexer)
        print(parsed)
        parsed.sanity_check()
        return parsed
