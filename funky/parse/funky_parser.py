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

    def p_MODULE_DEFINITION(self, p):
        """MODULE_DEFINITION : MODULE IDENTIFIER WITH MODULE_BODY
        """
        module_id, body = p[2], p[4]
        p[0] = Module(module_id, body)

    def p_MODULE_BODY(self, p):
        """MODULE_BODY : OPEN_BRACE IMPORT_STATEMENTS ENDSTATEMENT TOPLEVEL_DECLARATIONS CLOSE_BRACE
                       | OPEN_BRACE TOPLEVEL_DECLARATIONS CLOSE_BRACE
        """
        if len(p) == 6:
            imports, toplevel_declarations = p[2], p[4]
        else:
            imports, toplevel_declarations = [], p[2]

        imports = [i for i in imports if i]
        toplevel_declarations = [t for t in toplevel_declarations if t]
        p[0] = ProgramBody(imports, toplevel_declarations)

    def p_IMPORT_STATEMENTS(self, p):
        """IMPORT_STATEMENTS : IMPORT_STATEMENTS ENDSTATEMENT IMPORT_STATEMENT
                             | IMPORT_STATEMENT
        """
        if len(p) == 4:
            p[0] = p[1] + [p[3]]
        else:
            p[0] = [p[1]]

    def p_IMPORT_STATEMENT(self, p):
        """IMPORT_STATEMENT : IMPORT STRING"""
        p[0] = p[2]

    def p_TOPLEVEL_DECLARATION(self, p):
        """TOPLEVEL_DECLARATIONS : TOPLEVEL_DECLARATIONS ENDSTATEMENT TOP_DECLARATION
                                 | TOP_DECLARATION
        """
        if len(p) == 4:
            p[0] = p[1] + [p[3]]
        else:
            p[0] =[p[1]]

    def p_TOP_DECLARATION(self, p):
        """TOP_DECLARATION : ADT_DECLARATION
                           | DECLARATION
        """
        p[0] = p[1]

    def p_ADT_DECLARATION(self, p):
        """ADT_DECLARATION : NEWTYPE TYPENAME EQUALS CONSTRUCTORS"""
        p[0] = NewTypeStatement(p[2], [], p[4])

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
        """DECLARATION : FUNCTION_DEFINITION
                       | VARIABLE_DEFINITION
                       | FIXITY_DECLARATION
                       |
        """
        if len(p) >= 2:
            p[0] = p[1]

    def p_FUNCTION_DEFINITION(self, p):
        """FUNCTION_DEFINITION : FUNCTION_LHS RHS"""
        p[0] = FunctionDefinition(p[1], p[2])

    def p_VARIABLE_DEFINITION(self, p):
        """VARIABLE_DEFINITION : PARAM RHS"""
        p[0] = VariableDefinition(p[1], p[2])

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
        if len(p) == 4:
            p[0] = FunctionLHS(p[1], [p[2], *p[3]])
        elif len(p) == 6:
            p[0] = p[2]
            p[0].parameters.append(p[4])
            p[0].parameters.extend(p[5])
        else:
            p[0] = p[1]

    def p_INFIX_FUNCTION_DEFINITION(self, p):
        """INFIX_FUNCTION_DEFINITION : LPAT INFIX_FUNCTION LPAT"""
        p[0] = FunctionLHS(p[2], [p[1], p[3]])

    def p_RHS(self, p):
        """RHS : EQUALS EXP
               | EQUALS EXP WITH DECLARATIONS
               | GDRHS
               | GDRHS WITH DECLARATIONS
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
        """EXP : INFIX_EXP"""
        p[0] = p[1]
        p[0] = fixity.resolve_fixity(p[0])

    def p_INFIX_EXP(self, p):
        """INFIX_EXP : LEXP OP INFIX_EXP
                     | MINUS INFIX_EXP
                     | LEXP
        """
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
        """LEXP : LAMBDA_ABSTRACTION
                | LET_EXPR
                | IF_EXPR
                | MATCH_EXPR
                | FUNCTION_EXPR
        """
        p[0] = p[1]

    def p_LAMBDA_ABSTRACTION(self, p):
        """LAMBDA_ABSTRACTION : LAMBDA APAT APATS ARROW EXP"""
        p[0] = Lambda([p[2], *p[3]], p[5])

    def p_LET_EXPR(self, p):
        """LET_EXPR : LET DECLARATIONS IN EXP"""
        p[0] = Let(p[2], p[4])

    def p_IF_EXPR(self, p):
        """IF_EXPR : EXP IF EXP ELSE EXP"""
        p[0] = If(p[3], p[1], p[5])
    
    def p_MATCH_EXPR(self, p):
        """MATCH_EXPR : MATCH EXP ON OPEN_BRACE ALTS CLOSE_BRACE"""
        p[0] = Match(p[2], p[5])

    def p_FUNCTION_EXPR(self, p):
        """FUNCTION_EXPR : FUNCTION_EXPR AEXP
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
                | CONSTRUCTOR_PATTERN
                | NEGATIVE_LITERAL
        """
        p[0] = p[1]

    def p_CONSTRUCTOR_PATTERN(self, p):
        """CONSTRUCTOR_PATTERN : TYPENAME APAT APATS"""
        p[0] = Construction(p[1], [p[2]] + p[3], pattern=True)

    def p_NEGATIVE_LITERAL(self, p):
        """NEGATIVE_LITERAL : MINUS INTEGER
                            | MINUS FLOAT
        """
        p[0] = Literal(-p[2])

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

    def p_OP(self, p):
        """OP : VARSYM
              | INFIX_FUNCTION
        """
        p[0] = p[1]

    def p_INFIX_FUNCTION(self, p):
        """INFIX_FUNCTION : TILDE IDENTIFIER TILDE"""
        if p[2] not in fixity.fixities:
            fixity.set_fixity(p[2], *fixity.DEFAULT_FIXITY)
        p[0] = p[2]

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
                  | FPOW
                  | IPOW
                  | EQUALITY
                  | INEQUALITY
                  | LESS
                  | LEQ
                  | GREATER
                  | GEQ
                  | CONCAT
                  | AND
                  | OR
        """
        p[0] = p[1]

    def p_LITERAL(self, p):
        """LITERAL : FLOAT
                   | INTEGER
                   | BOOL
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

    def build(self, dump_pretty=False, dump_lexed=False, **kwargs):
        """Build the parser."""
        self.lexer = FunkyLexer()
        self.lexer.build()
        self.lexer = IndentationLexer(self.lexer, dump_pretty=dump_pretty,
                                                  dump_lexed=dump_lexed)
        log.debug("Using PLY to build the parser...")
        self.parser = yacc.yacc(module=self,
                                errorlog=yacc.NullLogger(),
                                **kwargs)
        log.debug("Parser built.")

    def do_parse(self, source):
        """Parse the given source code.
        
        :param source str: the source code as a raw string
        :return:           a parse tree representing the source code
        :rtype:            SourceTree
        """
        log.info("Parsing source...")
        ast = self.parser.parse(source, self.lexer)
        log.info("Done parsing source, AST created.")
        return ast
