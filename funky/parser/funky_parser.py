import ply.yacc as yacc

from funky.util import err
from funky.parser.funky_lexer import FunkyLexer, IndentationLexer
from funky.parser import FunkySyntaxError

from funky.core.intermediate import Module

class FunkyParser:

    tokens      =  FunkyLexer.tokens
    start       =  "MODULE_DEFINITION"
    precedence  =  (
        ("nonassoc", "EQUALITY"),
        ("left", "LESS", "LEQ", "GREATER", "GEQ"),
        ("left", "PLUS", "MINUS"),
        ("left", "TIMES", "DIVIDE"),
        ("right", "POW"),
    )

    def p_MODULE_DEFINITION(self, p):
        """MODULE_DEFINITION : MODULE IDENTIFIER WHERE BODY
        """
        module_id, body = p[2], p[4]
        p[0] = Module(module_id, body)

    def p_BODY(self, p):
        """BODY : OPEN_BRACE IMPORT_DECLARATIONS ENDSTATEMENT TOP_DECLARATIONS CLOSE_BRACE
                | OPEN_BRACE IMPORT_DECLARATIONS CLOSE_BRACE
                | OPEN_BRACE TOP_DECLARATIONS CLOSE_BRACE
        """
        pass

    def p_IMPORT_DECLARATIONS(self, p):
        """IMPORT_DECLARATIONS : IMPORT_DECLARATIONS ENDSTATEMENT IMPORT_DECLARATION
                               | IMPORT_DECLARATION
        """
        pass

    def p_IMPORT_DECLARATION(self, p):
        """IMPORT_DECLARATION : IMPORT IDENTIFIER ENDSTATEMENT
                              | IMPORT IDENTIFIER AS IDENTIFIER ENDSTATEMENT
        """
        # TODO: may have to change IDENTIFIER to a more robust module ID here.
        pass

    def p_TOP_DECLARATIONS(self, p):
        """TOP_DECLARATIONS : TOP_DECLARATIONS ENDSTATEMENT TOP_DECLARATION
                            | TOP_DECLARATION
        """
        pass

    def p_TOP_DECLARATION(self, p):
        """TOP_DECLARATION : NEWTYPE TYPENAME EQUALS TYPENAME ENDSTATEMENT
                           | DECLARATION
        """
        pass

    def p_DECLARATIONS(self, p):
        """DECLARATIONS : OPEN_BRACE DECLARATIONS_LIST CLOSE_BRACE
                        | OPEN_BRACE CLOSE_BRACE
        """
        pass

    def p_DECLARATIONS_LIST(self, p):
        """DECLARATIONS_LIST : DECLARATION ENDSTATEMENT DECLARATIONS_LIST
                             | DECLARATION
        """
        pass

    def p_DECLARATION(self, p):
        """DECLARATION : GEN_DECLARATION
                       | FUNCTION_LHS RHS
                       | PAT RHS
        """
        pass

    def p_GEN_DECLARATION(self, p):
        """GEN_DECLARATION : VARS TYPESIG TYPE
                           | FIXITY INTEGER OPS
                           | FIXITY OPS
                           |
        """
        pass

    def p_OPS(self, p):
        """OPS : OPS COMMA OP
               | OP
        """
        pass

    def p_VARS(self, p):
        """VARS : VARS COMMA IDENTIFIER
                | IDENTIFIER
        """
        pass

    def p_FIXITY(self, p):
        """FIXITY : INFIXL
                  | INFIXR
                  | INFIX
        """
        pass

    def p_TYPE(self, p):
        """TYPE : BTYPE
                | BTYPE ARROW TYPE
        """
        pass

    def p_BTYPE(self, p):
        """BTYPE : ATYPE
                 | BTYPE ATYPE
        """
        pass

    def p_ATYPE(self, p):
        """ATYPE : TYPENAME
                 | OPEN_PAREN TYPES_LIST CLOSE_PAREN
                 | OPEN_PAREN TYPE CLOSE_PAREN
                 | OPEN_SQUARE TYPE CLOSE_SQUARE
        """
        pass

    def p_FUNCTION_LHS(self, p):
        """FUNCTION_LHS : IDENTIFIER APAT APATS
                        | PAT VAROP PAT
                        | OPEN_PAREN FUNCTION_LHS CLOSE_PAREN APAT APATS
        """
        pass

    def p_RHS(self, p):
        """RHS : EQUALS EXP
               | EQUALS EXP WHERE DECLARATIONS
               | GDRHS
               | GDRHS WHERE DECLARATIONS
        """
        pass

    def p_GDRHS(self, p):
        """GDRHS : GUARDS EQUALS EXP
                 | GUARDS EQUALS EXP GDRHS
        """
        pass

    def p_GUARDS(self, p):
        """GUARDS : PIPE GUARD_LIST
        """
        pass

    def p_GUARD_LIST(self, p):
        """GUARD_LIST : GUARD_LIST GUARD
                      | GUARD
        """
        pass

    def p_GUARD(self, p):
        """GUARD : INFIX_EXP
        """ # we only allow for BOOLEAN guards.
        pass

    def p_EXP(self, p):
        """EXP : INFIX_EXP
        """
        pass
    
    def p_INFIX_EXP(self, p):
        """INFIX_EXP : LEXP OP INFIX_EXP
                     | MINUS INFIX_EXP
                     | LEXP
        """ # did use qualified operators before.
        pass

    def p_LEXP(self, p):
        """LEXP : LAMBDA APAT APATS ARROW EXP
                | LET DECLARATIONS IN EXP
                | IF EXP THEN EXP ELSE EXP
                | MATCH EXP OF OPEN_BRACE ALTS CLOSE_BRACE
                | FEXP
        """
        pass

    def p_FEXP(self, p):
        """FEXP : FEXP AEXP
                | AEXP
        """
        pass

    def p_AEXP(self, p):
        """AEXP : IDENTIFIER
                | GCON
                | LITERAL
                | OPEN_PAREN EXP CLOSE_PAREN
                | OPEN_PAREN EXP COMMA EXP_LIST CLOSE_PAREN
                | OPEN_SQUARE EXP CLOSE_SQUARE
                | OPEN_SQUARE EXP COMMA EXP_LIST CLOSE_SQUARE
        """ # few things missing, should be ok tho
        pass

    def p_ALTS(self, p):
        """ALTS : ALTS ALT ENDSTATEMENT
                | ALT
        """
        pass

    def p_ALT(self, p):
        """ALT : PAT ARROW EXP
               |
        """
        pass

    def p_PAT(self, p):
        """PAT : LPAT CONSTRUCTOR PAT
               | LPAT
        """
        pass

    def p_LPAT(self, p):
        """LPAT : APAT
                | MINUS OPEN_PAREN INTEGER CLOSE_PAREN
                | MINUS OPEN_PAREN FLOAT CLOSE_PAREN
        """
        pass

    def p_APAT(self, p):
        """APAT : IDENTIFIER
                | GCON
                | LITERAL
                | WILDCARD
                | OPEN_PAREN PAT CLOSE_PAREN
                | OPEN_PAREN PAT COMMA PAT_LIST CLOSE_PAREN
                | OPEN_SQUARE PAT_LIST CLOSE_SQUARE
        """
        pass

    def p_GCON(self, p):
        """GCON : OPEN_PAREN CLOSE_PAREN
                | OPEN_SQUARE CLOSE_SQUARE
        """
        pass

    def p_VAROP(self, p):
        """VAROP : VARSYM
                 | BACKTICK IDENTIFIER BACKTICK
        """
        pass

    def p_OP(self, p):
        """OP : VAROP
        """
        pass

    def p_EXP_LIST(self, p):
        """EXP_LIST : EXP_LIST COMMA EXP
                    | EXP
        """
        pass

    def p_APATS(self, p):
        """APATS : APAT APATS
                 |
        """
        pass

    def p_PAT_LIST(self, p):
        """PAT_LIST : PAT_LIST COMMA PAT
                    | PAT
        """
        pass

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
        pass

    def p_TYPES_LIST(self, p):
        """TYPES_LIST : TYPES_LIST COMMA TYPE
                      | TYPE
        """
        pass

    def p_LITERAL(self, p):
        """LITERAL : FLOAT
                   | INTEGER
                   | BOOL
                   | CHAR
                   | STRING
        """
        pass

    def p_error(self, p):
        raise FunkySyntaxError("Parsing failed at symbol " \
                               "'{}' on line {}.".format(p.value, p.lineno))

    def build(self, **kwargs):
        self.lexer = FunkyLexer()
        self.lexer.build()
        self.lexer = IndentationLexer(self.lexer)
        self.parser = yacc.yacc(module=self, **kwargs)

    def do_parse(self, source):
        self.lexer.input(source)
        for tok in self.lexer:
            print(tok, end=" ")
        print()
        return self.parser.parse(source, self.lexer)
