import ply.yacc as yacc

from funky.util import err
from funky.parser.funky_lexer import FunkyLexer

def err(*args):
    print("AHHHHH")

class FunkyParser:

    tokens = FunkyLexer.tokens
    start = "PROG"
    precedence = (
        ("left", "POW"),
        ("left", "PLUS", "MINUS"),
        ("left", "TIMES", "DIVIDE"),
        ("right", "UMINUS"),
    )

    def p_PROG(self, p):
        """PROG : FUNC_LIST"""
        pass

    def p_FUNC_LIST(self, p):
        """FUNC_LIST : FUNC NEWLINE FUNC_LIST
                     | empty
        """
        pass

    def p_FUNC(self, p):
        """FUNC : IDENTIFIER ARG_LIST EQUALS EXPRESSION"""
        pass

    def p_ARG_LIST(self, p):
        """ARG_LIST : IDENTIFIER ARG_LIST
                    | NUMBER ARG_LIST
                    | STRING ARG_LIST
                    | IDENTIFIER
                    | NUMBER
                    | STRING
        """
        pass

    def p_EXPRESSION_GROUP(self, p):
        """EXPRESSION : OPEN_BRACKET EXPRESSION CLOSE_BRACKET"""
        pass

    def p_EXPRESSION_BINOP(self, p):
        """EXPRESSION : EXPRESSION PLUS EXPRESSION
                      | EXPRESSION MINUS EXPRESSION
                      | EXPRESSION TIMES EXPRESSION
                      | EXPRESSION DIVIDE EXPRESSION
                      | EXPRESSION POW EXPRESSION
        """
        pass

    def p_EXPRESSION_UMINUS(self, p):
        """EXPRESSION : MINUS EXPRESSION %prec UMINUS"""
        pass

    def p_EXPRESSION_FUNCTION_APP(self, p):
        """EXPRESSION : IDENTIFIER ARG_LIST"""
        pass

    def p_EXPRESSION_LET(self, p):
        """EXPRESSION : LET IDENTIFIER EQUALS EXPRESSION IN EXPRESSION"""
        pass

    def p_EXPRESSION_IF(self, p):
        """EXPRESSION : EXPRESSION IF EXPRESSION ELSE EXPRESSION"""
        pass

    def p_EXPRESSION_WHERE(self, p):
        """EXPRESSION : EXPRESSION WHERE IDENTIFIER EQUALS EXPRESSION"""
        pass

    def p_EXPRESSION_NUMBER(self, p):
        """EXPRESSION : NUMBER"""
        pass
    
    def p_EXPRESSION_VARIABLE(self, p):
        """EXPRESSION : IDENTIFIER"""
        pass

    def p_EXPRESSION_STRING(self, p):
        """EXPRESSION : STRING"""
        pass
     
    def p_empty(self, p):
        """empty :"""
        pass

    def p_error(self, p):
        err("Cannot parse input.") # TODO -- make an exception here.

    def build(self, **kwargs):
        self.lexer = FunkyLexer()
        self.lexer.build()
        self.parser = yacc.yacc(module=self, **kwargs)

    def do_parse(self, source):
        return self.parser.parse(source)
