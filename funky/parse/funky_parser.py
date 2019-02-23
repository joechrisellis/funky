import logging
import ply.yacc as yacc

from funky.parse.funky_lexer import FunkyLexer, IndentationLexer
from funky.parse import FunkySyntaxError
import funky.parse.fixity as fixity

from funky.corelang.sourcetree import *
from funky.corelang.types import TypeVariable, FunctionType, ConstructorType

log = logging.getLogger(__name__)

class FunkyParser:

    tokens  =  FunkyLexer.tokens
    start   =  "MODULE_DEFINITION"

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
        """TOP_DECLARATION : TYPE_DECLARATION
                           | DECLARATION
        """
        p[0] = p[1]

    def p_TYPE_DECLARATION(self, p):
        """TYPE_DECLARATION : NEWTYPE TYPENAME TYVARS EQUALS CONSTRUCTORS"""
        p[0] = NewTypeStatement(p[2], p[3], p[5])

    def p_TYVARS(self, p):
        """TYVARS : TYVARS IDENTIFIER
                  |
        """
        if len(p) == 3:
            p[0] = p[1] + [p[2]]
        else:
            p[0] = []

    def p_CONSTRUCTORS(self, p):
        """CONSTRUCTORS : CONSTRUCTORS PIPE CONSTRUCTOR
                        | CONSTRUCTOR
        """
        if len(p) == 4:
            p[0] = p[1] + [p[3]]
        else:
            p[0] = [p[1]]

    def p_CONSTRUCTOR(self, p):
        """CONSTRUCTOR : TYPENAME ATYPES"""
        p[0] = ConstructorType(p[1], p[2])

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
                       | FUNCTION_DEFINITION
                       | VARIABLE_DEFINITION
        """
        p[0] = p[1]

    def p_FUNCTION_DEFINITION(self, p):
        """FUNCTION_DEFINITION : FUNCTION_LHS RHS"""
        p[0] = FunctionDefinition(p[1], p[2])

    def p_VARIABLE_DEFINITION(self, p):
        """VARIABLE_DEFINITION : PARAM RHS"""
        p[0] = VariableDefinition(p[1], p[2])

    def p_GEN_DECLARATION(self, p):
        """GEN_DECLARATION : FIXITY_DECLARATION
                           |
        """
        pass

    def p_FIXITY_DECLARATION(self, p):
        """FIXITY_DECLARATION : SETFIX ASSOCIATIVITY INTEGER OP"""
        fixity.set_fixity(p[4], p[2], p[3])

    def p_ASSOCIATIVITY(self, p):
        """ASSOCIATIVITY : LEFTASSOC
                         | RIGHTASSOC
                         | NONASSOC
        """
        p[0] = p[1].lower()

    def p_TYPE(self, p):
        """TYPE : ATYPE
                | ATYPE ARROW TYPE
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = FunctionType(p[1], p[3])

    def p_ATYPES(self, p):
        """ATYPES : ATYPES ATYPE
                  |
        """
        if len(p) == 3:
            p[0] = p[1] + [p[2]]
        else:
            p[0] = []

    def p_ATYPE(self, p):
        """ATYPE : TYPENAME
                 | IDENTIFIER
                 | OPEN_PAREN TYPE CLOSE_PAREN
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[2]

    def p_FUNCTION_LHS(self, p):
        """FUNCTION_LHS : IDENTIFIER APAT APATS
                        | OPEN_PAREN FUNCTION_LHS CLOSE_PAREN APAT APATS
                        | INFIX_FUNCTION_DEFINITION
        """
        if len(p) == 6:
            p[0] = p[2]
            p[0].parameters.append(p[4])
            p[0].parameters.extend(p[5])
        elif len(p) == 4:
            p[0] = FunctionLHS(p[1], [p[2], *p[3]])
        else:
            p[0] = p[1]

    def p_INFIX_FUNCTION_DEFINITION(self, p):
        """INFIX_FUNCTION_DEFINITION : LPAT INFIX_FUNCTION LPAT"""
        p[0] = FunctionLHS(p[2], [p[1], p[3]])

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
        """GDRHS : GIVEN EXP EQUALS EXP
                 | GIVEN EXP EQUALS EXP GDRHS
        """
        if len(p) == 5:
            p[0] = [GuardedExpression(p[2], p[4])]
        else:
            p[0] = [GuardedExpression(p[2], p[4])] + p[5]

    def p_EXP(self, p):
        """EXP : INFIX_EXP
        """
        p[0] = p[1]
        p[0] = fixity.resolve_fixity(p[0])

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
                | EXP IF EXP ELSE EXP
                | MATCH EXP OF OPEN_BRACE ALTS CLOSE_BRACE
                | FEXP
        """
        if len(p) == 6:
            if p[1] == "lambda":
                p[0] = Lambda([p[2], *p[3]], p[5])
            else:
                p[0] = If(p[3], p[1], p[5])
        elif len(p) == 5:
            if p[1] == "let":
                p[0] = Let(p[2], p[4])
        elif len(p) == 7:
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
                | USED_TYPENAME
                | LITERAL
                | OPERATOR_FUNC
                | OPEN_PAREN EXP CLOSE_PAREN
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[2]

    def p_OPERATOR_FUNC(self, p):
        """OPERATOR_FUNC : OPEN_PAREN OP CLOSE_PAREN"""
        p[0] = UsedVar(p[2])

    def p_ALTS(self, p):
        """ALTS : ALT ENDSTATEMENT ALTS
                | ALT
        """
        if len(p) == 4:
            p[0] = p[1] + p[3]
        else:
            p[0] = p[1]

    def p_ALT(self, p):
        """ALT : LPAT ARROW EXP
               |
        """
        p[0] = [Alternative(p[1], p[3])] if len(p) == 4 else []

    def p_LPAT(self, p):
        """LPAT : APAT
                | MINUS OPEN_PAREN INTEGER CLOSE_PAREN
                | MINUS OPEN_PAREN FLOAT CLOSE_PAREN
                | TYPENAME APAT APATS
        """
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 4:
            p[0] = Construction(p[1], [p[2]] + p[3], pattern=True)
        else:
            p[0] = Literal(-p[3])

    def p_APAT(self, p):
        """APAT : PARAM
                | TYPENAME
                | LITERAL
                | OPEN_PAREN LPAT CLOSE_PAREN
        """
        if len(p) == 2:
            if type(p[1]) == str:
                p[0] = Construction(p[1], [], pattern=True)
            else:
                p[0] = p[1]
        else:
            p[0] = p[2]

    def p_VAROP(self, p):
        """VAROP : VARSYM
                 | INFIX_FUNCTION
        """
        p[0] = p[1]

    def p_INFIX_FUNCTION(self, p):
        """INFIX_FUNCTION : BACKTICK IDENTIFIER BACKTICK"""
        if p[2] not in fixity.fixities:
            fixity.set_fixity(p[2], *fixity.DEFAULT_FIXITY)
        p[0] = p[2]

    def p_OP(self, p):
        """OP : VAROP
        """
        p[0] = p[1]

    def p_APATS(self, p):
        """APATS : APAT APATS
                 |
        """
        if len(p) == 1:
            p[0] = []
        else:
            p[0] = [p[1]] + p[2]

    def p_VARSYM(self, p):
        """VARSYM : PLUS
                  | MINUS
                  | TIMES
                  | DIVIDE
                  | MODULO
                  | POW
                  | EQUALITY
                  | INEQUALITY
                  | LESS
                  | LEQ
                  | GREATER
                  | GEQ
                  | AND
                  | OR
        """
        p[0] = p[1]

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

    def p_USED_TYPENAME(self, p):
        """USED_TYPENAME : TYPENAME"""
        p[0] = UsedVar(p[1])

    def p_PARAM(self, p):
        """PARAM : IDENTIFIER"""
        p[0] = Parameter(p[1])
    
    def p_error(self, p):
        raise FunkySyntaxError("Parsing failed at token {}".format(repr(p)))

    def build(self, dump_lexed=False, **kwargs):
        """Build the parser."""
        self.lexer = FunkyLexer()
        self.lexer.build()
        self.lexer = IndentationLexer(self.lexer, dump_lexed=dump_lexed)
        log.debug("Using PLY to build the parser...")
        self.parser = yacc.yacc(module=self,
                                **kwargs)
        log.debug("Parser built.")

    def do_parse(self, source, dump_lexed=False):
        """Parse the given source code.
        
        :param source str: the source code as a raw string
        :return:           a parse tree representing the source code
        :rtype:            SourceTree
        """
        log.info("Parsing source...")
        ast = self.parser.parse(source, self.lexer)
        log.info("Done parsing source, AST created.")
        return ast
