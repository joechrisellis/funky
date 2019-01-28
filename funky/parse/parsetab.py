
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'MODULE_DEFINITIONAND ARROW AS BACKTICK BOOL CHAR CLOSE_BRACE CLOSE_PAREN CLOSE_SQUARE COMMA DIVIDE ELSE ENDSTATEMENT EQUALITY EQUALS FLOAT GEQ GREATER IDENTIFIER IF IMPORT IN INEQUALITY INTEGER LAMBDA LEFTASSOC LEQ LESS LET LIST_CONSTRUCTOR MATCH MINUS MODULE NEWCONS NEWTYPE NONASSOC OF OPEN_BRACE OPEN_PAREN OPEN_SQUARE OR PIPE PLUS POW RIGHTASSOC SETFIX STRING THEN TIMES TYPENAME TYPESIG WHERE WHITESPACEMODULE_DEFINITION : MODULE IDENTIFIER WHERE BODY\n        BODY : OPEN_BRACE IMPORT_DECLARATIONS ENDSTATEMENT TOP_DECLARATIONS CLOSE_BRACE\n                | OPEN_BRACE TOP_DECLARATIONS CLOSE_BRACE\n        IMPORT_DECLARATIONS : IMPORT_DECLARATIONS ENDSTATEMENT IMPORT_DECLARATION\n                               | IMPORT_DECLARATION\n        IMPORT_DECLARATION : IMPORT IDENTIFIER\n        TOP_DECLARATIONS : TOP_DECLARATIONS ENDSTATEMENT TOP_DECLARATION\n                            | TOP_DECLARATION\n        TOP_DECLARATION : NEWTYPE TYPENAME EQUALS TYPE\n                           | NEWCONS TYPENAME TYPE_PARAMETERS EQUALS CONSTRUCTORS\n                           | DECLARATION\n        TYPE_PARAMETERS : TYPE_PARAMETERS IDENTIFIER\n                           |\n        CONSTRUCTORS : CONSTRUCTORS PIPE CONSTRUCTOR\n                        | CONSTRUCTOR\n        CONSTRUCTOR : TYPENAME ATYPESDECLARATIONS : OPEN_BRACE DECLARATIONS_LIST CLOSE_BRACE\n                        | OPEN_BRACE CLOSE_BRACE\n        DECLARATIONS_LIST : DECLARATION ENDSTATEMENT DECLARATIONS_LIST\n                             | DECLARATION\n        DECLARATION : GEN_DECLARATION\n                       | FUNCTION_LHS RHS\n                       | PAT RHS\n        GEN_DECLARATION : IDENTIFIER TYPESIG TYPE\n                           | SETFIX ASSOCIATIVITY INTEGER OP\n                           |\n        ASSOCIATIVITY : LEFTASSOC\n                         | RIGHTASSOC\n                         | NONASSOC\n        TYPE : ATYPE\n                | ATYPE ARROW TYPE\n        ATYPES : ATYPES ATYPE\n                  |\n        ATYPE : TYPENAME\n                 | IDENTIFIER\n                 | OPEN_PAREN TYPES_LIST CLOSE_PAREN\n                 | OPEN_PAREN TYPE CLOSE_PAREN\n                 | OPEN_SQUARE TYPE CLOSE_SQUARE\n        FUNCTION_LHS : IDENTIFIER APAT APATS\n                        | PAT VAROP PAT\n                        | OPEN_PAREN FUNCTION_LHS CLOSE_PAREN APAT APATS\n        RHS : EQUALS EXP\n               | EQUALS EXP WHERE DECLARATIONS\n               | GDRHS\n               | GDRHS WHERE DECLARATIONS\n        GDRHS : GUARDS EQUALS EXP\n                 | GUARDS EQUALS EXP GDRHS\n        GUARDS : PIPE GUARD\n        GUARD : INFIX_EXP\n        EXP : INFIX_EXP\n        INFIX_EXP : LEXP OP INFIX_EXP\n                     | MINUS INFIX_EXP\n                     | LEXP\n        LEXP : LAMBDA APAT APATS ARROW EXP\n                | LET DECLARATIONS IN EXP\n                | IF EXP THEN EXP ELSE EXP\n                | MATCH EXP OF OPEN_BRACE ALTS CLOSE_BRACE\n                | FEXP\n        FEXP : FEXP AEXP\n                | AEXP\n        AEXP : USED_VAR\n                | GCON\n                | LITERAL\n                | OPEN_PAREN EXP CLOSE_PAREN\n                | OPEN_PAREN EXP COMMA EXP_LIST CLOSE_PAREN\n                | OPEN_SQUARE EXP CLOSE_SQUARE\n                | OPEN_SQUARE EXP COMMA EXP_LIST CLOSE_SQUARE\n        CONSTRUCTION_PARAMS : CONSTRUCTION_PARAMS AEXP\n                               | AEXP\n        ALTS : ALT ENDSTATEMENT ALTS\n                | ALT\n        ALT : PAT ARROW EXP\n               |\n        PAT : LPAT LIST_CONSTRUCTOR PAT\n               | LPAT\n        LPAT : APAT\n                | MINUS OPEN_PAREN INTEGER CLOSE_PAREN\n                | MINUS OPEN_PAREN FLOAT CLOSE_PAREN\n                | GCON APAT APATS\n        APAT : PARAM\n                | GCON\n                | LITERAL\n                | OPEN_PAREN PAT CLOSE_PAREN\n                | OPEN_PAREN PAT COMMA PAT_LIST CLOSE_PAREN\n                | OPEN_SQUARE PAT_LIST CLOSE_SQUARE\n        GCON : OPEN_PAREN CLOSE_PAREN\n                | OPEN_SQUARE CLOSE_SQUARE\n                | TYPENAME\n        VAROP : VARSYM\n                 | BACKTICK IDENTIFIER BACKTICK\n        OP : VAROP\n        EXP_LIST : EXP_LIST COMMA EXP\n                    | EXP\n        APATS : APAT APATS\n                 |\n        PAT_LIST : PAT_LIST COMMA PAT\n                    | PAT\n        VARSYM : PLUS\n                  | MINUS\n                  | TIMES\n                  | DIVIDE\n                  | POW\n                  | EQUALITY\n                  | INEQUALITY\n                  | LESS\n                  | LEQ\n                  | GREATER\n                  | GEQ\n                  | AND\n                  | OR\n                  | LIST_CONSTRUCTOR\n        TYPES_LIST : TYPES_LIST COMMA TYPE\n                      | TYPE\n        LITERAL : FLOAT\n                   | INTEGER\n                   | BOOL\n                   | CHAR\n                   | STRING\n        USED_VAR : IDENTIFIERPARAM : IDENTIFIER'
    
_lr_action_items = {'MODULE':([0,],[2,]),'$end':([1,5,35,128,],[0,-1,-3,-2,]),'IDENTIFIER':([2,6,11,12,14,21,23,26,27,28,29,30,31,32,33,34,36,38,39,40,41,42,44,46,49,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,73,75,76,78,80,85,88,89,90,91,94,95,99,100,102,103,104,105,106,107,108,109,110,111,113,119,120,121,126,127,129,136,138,139,141,143,146,151,153,159,160,161,162,163,169,173,175,176,177,178,181,183,185,188,190,194,198,202,203,204,207,208,],[3,12,37,38,-88,-115,75,-114,38,-80,-82,38,-116,-117,-118,12,12,-120,85,38,-81,38,-13,111,111,38,-89,117,-98,-99,-100,-101,-102,-103,-104,-105,-106,-107,-108,-109,-110,-111,-86,38,38,38,-87,-35,-34,85,85,38,85,136,111,38,111,111,111,-60,-61,-62,-63,111,111,-119,111,38,-83,38,-85,38,85,-12,111,-91,38,12,-59,-90,38,-36,85,-37,-38,-33,111,111,-64,111,-66,111,-84,85,111,12,38,-32,111,111,-65,-67,38,111,]),'WHERE':([3,14,21,26,31,32,33,47,73,80,96,97,98,104,105,106,107,108,111,140,146,150,167,175,177,179,186,196,203,204,205,206,],[4,-88,-115,-114,-116,-117,-118,112,-86,-87,137,-50,-53,-58,-60,-61,-62,-63,-119,-52,-59,-46,-51,-64,-66,-47,-55,-54,-65,-67,-56,-57,]),'OPEN_BRACE':([4,101,112,137,174,],[6,143,143,143,190,]),'IMPORT':([6,34,],[11,11,]),'NEWTYPE':([6,34,36,],[13,13,13,]),'NEWCONS':([6,34,36,],[15,15,15,]),'SETFIX':([6,34,36,143,188,],[20,20,20,20,20,]),'CLOSE_BRACE':([6,8,10,14,16,17,21,26,31,32,33,34,36,45,47,50,52,54,55,56,57,58,59,60,61,62,63,64,65,66,67,73,80,82,84,85,86,87,88,96,97,98,104,105,106,107,108,111,134,139,140,143,146,149,150,151,152,158,159,161,162,163,164,165,166,167,170,171,172,175,177,179,183,186,187,188,190,194,195,196,197,199,200,203,204,205,206,207,210,211,],[-26,35,-8,-88,-11,-21,-115,-114,-116,-117,-118,-26,-26,-22,-44,-23,-89,-98,-99,-100,-101,-102,-103,-104,-105,-106,-107,-108,-109,-110,-111,-86,-87,128,-7,-35,-24,-30,-34,-42,-50,-53,-58,-60,-61,-62,-63,-119,-9,-91,-52,171,-59,-45,-46,-90,-25,-31,-36,-37,-38,-33,-10,-15,-43,-51,187,-18,-20,-64,-66,-47,-16,-55,-17,-26,-73,-32,-14,-54,-19,206,-71,-65,-67,-56,-57,-73,-70,-72,]),'ENDSTATEMENT':([6,7,8,9,10,14,16,17,21,26,31,32,33,34,36,37,45,47,50,52,54,55,56,57,58,59,60,61,62,63,64,65,66,67,73,80,82,83,84,85,86,87,88,96,97,98,104,105,106,107,108,111,134,139,140,143,146,149,150,151,152,158,159,161,162,163,164,165,166,167,171,172,175,177,179,183,186,187,188,190,194,195,196,200,203,204,205,206,207,211,],[-26,34,36,-5,-8,-88,-11,-21,-115,-114,-116,-117,-118,-26,-26,-6,-22,-44,-23,-89,-98,-99,-100,-101,-102,-103,-104,-105,-106,-107,-108,-109,-110,-111,-86,-87,36,-4,-7,-35,-24,-30,-34,-42,-50,-53,-58,-60,-61,-62,-63,-119,-9,-91,-52,-26,-59,-45,-46,-90,-25,-31,-36,-37,-38,-33,-10,-15,-43,-51,-18,188,-64,-66,-47,-16,-55,-17,-26,-73,-32,-14,-54,207,-65,-67,-56,-57,-73,-72,]),'OPEN_PAREN':([6,12,14,21,23,25,26,27,28,29,30,31,32,33,34,36,38,39,40,41,42,46,49,51,52,54,55,56,57,58,59,60,61,62,63,64,65,66,67,73,75,76,78,80,85,88,89,90,91,94,99,100,102,103,104,105,106,107,108,109,110,111,113,119,120,121,126,127,129,138,139,141,143,146,151,153,159,160,161,162,163,169,173,175,176,177,178,181,183,185,188,190,194,198,202,203,204,207,208,],[23,42,-88,-115,23,77,-114,42,-80,-82,42,-116,-117,-118,23,23,-120,89,42,-81,42,109,109,42,-89,-98,-99,-100,-101,-102,-103,-104,-105,-106,-107,-108,-109,-110,-111,-86,42,42,42,-87,-35,-34,89,89,42,89,109,42,109,109,109,-60,-61,-62,-63,109,109,-119,109,42,-83,42,-85,42,89,109,-91,42,23,-59,-90,42,-36,89,-37,-38,-33,109,109,-64,109,-66,109,-84,89,109,23,42,-32,109,109,-65,-67,42,109,]),'MINUS':([6,12,14,19,21,22,23,24,26,27,28,29,30,31,32,33,34,36,38,41,42,46,49,51,52,54,55,56,57,58,59,60,61,62,63,64,65,66,67,73,74,75,76,78,80,91,97,98,99,102,103,104,105,106,107,108,109,110,111,113,118,120,121,122,125,126,127,133,138,139,140,143,146,151,155,156,167,169,173,175,176,177,178,181,185,186,188,190,196,198,202,203,204,205,206,207,208,],[25,-120,-88,55,-115,-76,25,-75,-114,-81,-80,-82,25,-116,-117,-118,25,25,-120,-81,25,99,99,25,-89,-98,-99,-100,-101,-102,-103,-104,-105,-106,-107,-108,-109,-110,-111,-86,55,-120,25,-95,-87,-95,-50,55,99,99,99,-58,-60,-61,-62,-63,99,99,-119,99,55,-83,25,-74,-79,-85,25,-94,99,-91,-52,25,-59,-90,-77,-78,-51,99,99,-64,99,-66,99,-84,99,-55,25,25,-54,99,99,-65,-67,-56,-57,25,99,]),'OPEN_SQUARE':([6,12,14,21,23,26,27,28,29,30,31,32,33,34,36,38,39,40,41,42,46,49,51,52,54,55,56,57,58,59,60,61,62,63,64,65,66,67,73,75,76,78,80,85,88,89,90,91,94,99,100,102,103,104,105,106,107,108,109,110,111,113,119,120,121,126,127,129,138,139,141,143,146,151,153,159,160,161,162,163,169,173,175,176,177,178,181,183,185,188,190,194,198,202,203,204,207,208,],[30,30,-88,-115,30,-114,30,-80,-82,30,-116,-117,-118,30,30,-120,90,30,-81,30,110,110,30,-89,-98,-99,-100,-101,-102,-103,-104,-105,-106,-107,-108,-109,-110,-111,-86,30,30,30,-87,-35,-34,90,90,30,90,110,30,110,110,110,-60,-61,-62,-63,110,110,-119,110,30,-83,30,-85,30,90,110,-91,30,30,-59,-90,30,-36,90,-37,-38,-33,110,110,-64,110,-66,110,-84,90,110,30,30,-32,110,110,-65,-67,30,110,]),'TYPENAME':([6,12,13,14,15,21,23,26,27,28,29,30,31,32,33,34,36,38,39,40,41,42,46,49,51,52,54,55,56,57,58,59,60,61,62,63,64,65,66,67,73,75,76,78,80,85,88,89,90,91,94,99,100,102,103,104,105,106,107,108,109,110,111,113,119,120,121,126,127,129,135,138,139,141,143,146,151,153,159,160,161,162,163,169,173,175,176,177,178,181,183,184,185,188,190,194,198,202,203,204,207,208,],[14,14,43,-88,44,-115,14,-114,14,-80,-82,14,-116,-117,-118,14,14,-120,88,14,-81,14,14,14,14,-89,-98,-99,-100,-101,-102,-103,-104,-105,-106,-107,-108,-109,-110,-111,-86,14,14,14,-87,-35,-34,88,88,14,88,14,14,14,14,14,-60,-61,-62,-63,14,14,-119,14,14,-83,14,-85,14,88,163,14,-91,14,14,-59,-90,14,-36,88,-37,-38,-33,14,14,-64,14,-66,14,-84,88,163,14,14,14,-32,14,14,-65,-67,14,14,]),'FLOAT':([6,12,14,21,23,26,27,28,29,30,31,32,33,34,36,38,40,41,42,46,49,51,52,54,55,56,57,58,59,60,61,62,63,64,65,66,67,73,75,76,77,78,80,91,99,100,102,103,104,105,106,107,108,109,110,111,113,119,120,121,126,127,138,139,141,143,146,151,153,169,173,175,176,177,178,181,185,188,190,198,202,203,204,207,208,],[26,26,-88,-115,26,-114,26,-80,-82,26,-116,-117,-118,26,26,-120,26,-81,26,26,26,26,-89,-98,-99,-100,-101,-102,-103,-104,-105,-106,-107,-108,-109,-110,-111,-86,26,26,124,26,-87,26,26,26,26,26,26,-60,-61,-62,-63,26,26,-119,26,26,-83,26,-85,26,26,-91,26,26,-59,-90,26,26,26,-64,26,-66,26,-84,26,26,26,26,26,-65,-67,26,26,]),'INTEGER':([6,12,14,21,23,26,27,28,29,30,31,32,33,34,36,38,40,41,42,46,49,51,52,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,73,75,76,77,78,80,91,99,100,102,103,104,105,106,107,108,109,110,111,113,119,120,121,126,127,138,139,141,143,146,151,153,169,173,175,176,177,178,181,185,188,190,198,202,203,204,207,208,],[21,21,-88,-115,21,-114,21,-80,-82,21,-116,-117,-118,21,21,-120,21,-81,21,21,21,21,-89,-98,-99,-100,-101,-102,-103,-104,-105,-106,-107,-108,-109,-110,-111,118,-27,-28,-29,-86,21,21,123,21,-87,21,21,21,21,21,21,-60,-61,-62,-63,21,21,-119,21,21,-83,21,-85,21,21,-91,21,21,-59,-90,21,21,21,-64,21,-66,21,-84,21,21,21,21,21,-65,-67,21,21,]),'BOOL':([6,12,14,21,23,26,27,28,29,30,31,32,33,34,36,38,40,41,42,46,49,51,52,54,55,56,57,58,59,60,61,62,63,64,65,66,67,73,75,76,78,80,91,99,100,102,103,104,105,106,107,108,109,110,111,113,119,120,121,126,127,138,139,141,143,146,151,153,169,173,175,176,177,178,181,185,188,190,198,202,203,204,207,208,],[31,31,-88,-115,31,-114,31,-80,-82,31,-116,-117,-118,31,31,-120,31,-81,31,31,31,31,-89,-98,-99,-100,-101,-102,-103,-104,-105,-106,-107,-108,-109,-110,-111,-86,31,31,31,-87,31,31,31,31,31,31,-60,-61,-62,-63,31,31,-119,31,31,-83,31,-85,31,31,-91,31,31,-59,-90,31,31,31,-64,31,-66,31,-84,31,31,31,31,31,-65,-67,31,31,]),'CHAR':([6,12,14,21,23,26,27,28,29,30,31,32,33,34,36,38,40,41,42,46,49,51,52,54,55,56,57,58,59,60,61,62,63,64,65,66,67,73,75,76,78,80,91,99,100,102,103,104,105,106,107,108,109,110,111,113,119,120,121,126,127,138,139,141,143,146,151,153,169,173,175,176,177,178,181,185,188,190,198,202,203,204,207,208,],[32,32,-88,-115,32,-114,32,-80,-82,32,-116,-117,-118,32,32,-120,32,-81,32,32,32,32,-89,-98,-99,-100,-101,-102,-103,-104,-105,-106,-107,-108,-109,-110,-111,-86,32,32,32,-87,32,32,32,32,32,32,-60,-61,-62,-63,32,32,-119,32,32,-83,32,-85,32,32,-91,32,32,-59,-90,32,32,32,-64,32,-66,32,-84,32,32,32,32,32,-65,-67,32,32,]),'STRING':([6,12,14,21,23,26,27,28,29,30,31,32,33,34,36,38,40,41,42,46,49,51,52,54,55,56,57,58,59,60,61,62,63,64,65,66,67,73,75,76,78,80,91,99,100,102,103,104,105,106,107,108,109,110,111,113,119,120,121,126,127,138,139,141,143,146,151,153,169,173,175,176,177,178,181,185,188,190,198,202,203,204,207,208,],[33,33,-88,-115,33,-114,33,-80,-82,33,-116,-117,-118,33,33,-120,33,-81,33,33,33,33,-89,-98,-99,-100,-101,-102,-103,-104,-105,-106,-107,-108,-109,-110,-111,-86,33,33,33,-87,33,33,33,33,33,33,-60,-61,-62,-63,33,33,-119,33,33,-83,33,-85,33,33,-91,33,33,-59,-90,33,33,33,-64,33,-66,33,-84,33,33,33,33,33,-65,-67,33,33,]),'TYPESIG':([12,],[39,]),'LIST_CONSTRUCTOR':([12,14,19,21,22,24,26,27,28,29,31,32,33,38,41,73,74,75,78,80,91,97,98,104,105,106,107,108,111,118,120,122,125,126,133,140,146,155,156,167,175,177,181,186,196,203,204,205,206,],[-120,-88,67,-115,-76,76,-114,-81,-80,-82,-116,-117,-118,-120,-81,-86,67,-120,-95,-87,-95,-50,67,-58,-60,-61,-62,-63,-119,67,-83,-74,-79,-85,-94,-52,-59,-77,-78,-51,-64,-66,-84,-55,-54,-65,-67,-56,-57,]),'EQUALS':([12,14,18,19,21,22,24,26,27,28,29,31,32,33,38,40,41,43,44,48,73,78,80,91,92,95,97,98,104,105,106,107,108,111,114,115,116,120,122,125,126,133,136,140,146,153,155,156,167,175,177,180,181,186,196,203,204,205,206,],[-120,-88,46,46,-115,-76,-75,-114,-81,-80,-82,-116,-117,-118,-120,-95,-81,94,-13,113,-86,-95,-87,-95,-39,135,-50,-53,-58,-60,-61,-62,-63,-119,-48,-49,-40,-83,-74,-79,-85,-94,-12,-52,-59,-95,-77,-78,-51,-64,-66,-41,-84,-55,-54,-65,-67,-56,-57,]),'BACKTICK':([12,14,19,21,22,24,26,27,28,29,31,32,33,38,41,73,74,75,78,80,91,97,98,104,105,106,107,108,111,117,118,120,122,125,126,133,140,146,155,156,167,175,177,181,186,196,203,204,205,206,],[-120,-88,53,-115,-76,-75,-114,-81,-80,-82,-116,-117,-118,-120,-81,-86,53,-120,-95,-87,-95,-50,53,-58,-60,-61,-62,-63,-119,151,53,-83,-74,-79,-85,-94,-52,-59,-77,-78,-51,-64,-66,-84,-55,-54,-65,-67,-56,-57,]),'PLUS':([12,14,19,21,22,24,26,27,28,29,31,32,33,38,41,73,74,75,78,80,91,97,98,104,105,106,107,108,111,118,120,122,125,126,133,140,146,155,156,167,175,177,181,186,196,203,204,205,206,],[-120,-88,54,-115,-76,-75,-114,-81,-80,-82,-116,-117,-118,-120,-81,-86,54,-120,-95,-87,-95,-50,54,-58,-60,-61,-62,-63,-119,54,-83,-74,-79,-85,-94,-52,-59,-77,-78,-51,-64,-66,-84,-55,-54,-65,-67,-56,-57,]),'TIMES':([12,14,19,21,22,24,26,27,28,29,31,32,33,38,41,73,74,75,78,80,91,97,98,104,105,106,107,108,111,118,120,122,125,126,133,140,146,155,156,167,175,177,181,186,196,203,204,205,206,],[-120,-88,56,-115,-76,-75,-114,-81,-80,-82,-116,-117,-118,-120,-81,-86,56,-120,-95,-87,-95,-50,56,-58,-60,-61,-62,-63,-119,56,-83,-74,-79,-85,-94,-52,-59,-77,-78,-51,-64,-66,-84,-55,-54,-65,-67,-56,-57,]),'DIVIDE':([12,14,19,21,22,24,26,27,28,29,31,32,33,38,41,73,74,75,78,80,91,97,98,104,105,106,107,108,111,118,120,122,125,126,133,140,146,155,156,167,175,177,181,186,196,203,204,205,206,],[-120,-88,57,-115,-76,-75,-114,-81,-80,-82,-116,-117,-118,-120,-81,-86,57,-120,-95,-87,-95,-50,57,-58,-60,-61,-62,-63,-119,57,-83,-74,-79,-85,-94,-52,-59,-77,-78,-51,-64,-66,-84,-55,-54,-65,-67,-56,-57,]),'POW':([12,14,19,21,22,24,26,27,28,29,31,32,33,38,41,73,74,75,78,80,91,97,98,104,105,106,107,108,111,118,120,122,125,126,133,140,146,155,156,167,175,177,181,186,196,203,204,205,206,],[-120,-88,58,-115,-76,-75,-114,-81,-80,-82,-116,-117,-118,-120,-81,-86,58,-120,-95,-87,-95,-50,58,-58,-60,-61,-62,-63,-119,58,-83,-74,-79,-85,-94,-52,-59,-77,-78,-51,-64,-66,-84,-55,-54,-65,-67,-56,-57,]),'EQUALITY':([12,14,19,21,22,24,26,27,28,29,31,32,33,38,41,73,74,75,78,80,91,97,98,104,105,106,107,108,111,118,120,122,125,126,133,140,146,155,156,167,175,177,181,186,196,203,204,205,206,],[-120,-88,59,-115,-76,-75,-114,-81,-80,-82,-116,-117,-118,-120,-81,-86,59,-120,-95,-87,-95,-50,59,-58,-60,-61,-62,-63,-119,59,-83,-74,-79,-85,-94,-52,-59,-77,-78,-51,-64,-66,-84,-55,-54,-65,-67,-56,-57,]),'INEQUALITY':([12,14,19,21,22,24,26,27,28,29,31,32,33,38,41,73,74,75,78,80,91,97,98,104,105,106,107,108,111,118,120,122,125,126,133,140,146,155,156,167,175,177,181,186,196,203,204,205,206,],[-120,-88,60,-115,-76,-75,-114,-81,-80,-82,-116,-117,-118,-120,-81,-86,60,-120,-95,-87,-95,-50,60,-58,-60,-61,-62,-63,-119,60,-83,-74,-79,-85,-94,-52,-59,-77,-78,-51,-64,-66,-84,-55,-54,-65,-67,-56,-57,]),'LESS':([12,14,19,21,22,24,26,27,28,29,31,32,33,38,41,73,74,75,78,80,91,97,98,104,105,106,107,108,111,118,120,122,125,126,133,140,146,155,156,167,175,177,181,186,196,203,204,205,206,],[-120,-88,61,-115,-76,-75,-114,-81,-80,-82,-116,-117,-118,-120,-81,-86,61,-120,-95,-87,-95,-50,61,-58,-60,-61,-62,-63,-119,61,-83,-74,-79,-85,-94,-52,-59,-77,-78,-51,-64,-66,-84,-55,-54,-65,-67,-56,-57,]),'LEQ':([12,14,19,21,22,24,26,27,28,29,31,32,33,38,41,73,74,75,78,80,91,97,98,104,105,106,107,108,111,118,120,122,125,126,133,140,146,155,156,167,175,177,181,186,196,203,204,205,206,],[-120,-88,62,-115,-76,-75,-114,-81,-80,-82,-116,-117,-118,-120,-81,-86,62,-120,-95,-87,-95,-50,62,-58,-60,-61,-62,-63,-119,62,-83,-74,-79,-85,-94,-52,-59,-77,-78,-51,-64,-66,-84,-55,-54,-65,-67,-56,-57,]),'GREATER':([12,14,19,21,22,24,26,27,28,29,31,32,33,38,41,73,74,75,78,80,91,97,98,104,105,106,107,108,111,118,120,122,125,126,133,140,146,155,156,167,175,177,181,186,196,203,204,205,206,],[-120,-88,63,-115,-76,-75,-114,-81,-80,-82,-116,-117,-118,-120,-81,-86,63,-120,-95,-87,-95,-50,63,-58,-60,-61,-62,-63,-119,63,-83,-74,-79,-85,-94,-52,-59,-77,-78,-51,-64,-66,-84,-55,-54,-65,-67,-56,-57,]),'GEQ':([12,14,19,21,22,24,26,27,28,29,31,32,33,38,41,73,74,75,78,80,91,97,98,104,105,106,107,108,111,118,120,122,125,126,133,140,146,155,156,167,175,177,181,186,196,203,204,205,206,],[-120,-88,64,-115,-76,-75,-114,-81,-80,-82,-116,-117,-118,-120,-81,-86,64,-120,-95,-87,-95,-50,64,-58,-60,-61,-62,-63,-119,64,-83,-74,-79,-85,-94,-52,-59,-77,-78,-51,-64,-66,-84,-55,-54,-65,-67,-56,-57,]),'AND':([12,14,19,21,22,24,26,27,28,29,31,32,33,38,41,73,74,75,78,80,91,97,98,104,105,106,107,108,111,118,120,122,125,126,133,140,146,155,156,167,175,177,181,186,196,203,204,205,206,],[-120,-88,65,-115,-76,-75,-114,-81,-80,-82,-116,-117,-118,-120,-81,-86,65,-120,-95,-87,-95,-50,65,-58,-60,-61,-62,-63,-119,65,-83,-74,-79,-85,-94,-52,-59,-77,-78,-51,-64,-66,-84,-55,-54,-65,-67,-56,-57,]),'OR':([12,14,19,21,22,24,26,27,28,29,31,32,33,38,41,73,74,75,78,80,91,97,98,104,105,106,107,108,111,118,120,122,125,126,133,140,146,155,156,167,175,177,181,186,196,203,204,205,206,],[-120,-88,66,-115,-76,-75,-114,-81,-80,-82,-116,-117,-118,-120,-81,-86,66,-120,-95,-87,-95,-50,66,-58,-60,-61,-62,-63,-119,66,-83,-74,-79,-85,-94,-52,-59,-77,-78,-51,-64,-66,-84,-55,-54,-65,-67,-56,-57,]),'PIPE':([12,14,18,19,21,22,24,26,27,28,29,31,32,33,38,40,41,73,78,80,85,88,91,92,97,98,104,105,106,107,108,111,116,120,122,125,126,133,140,146,150,153,155,156,159,161,162,163,164,165,167,175,177,180,181,183,186,194,195,196,203,204,205,206,],[-120,-88,49,49,-115,-76,-75,-114,-81,-80,-82,-116,-117,-118,-120,-95,-81,-86,-95,-87,-35,-34,-95,-39,-50,-53,-58,-60,-61,-62,-63,-119,-40,-83,-74,-79,-85,-94,-52,-59,49,-95,-77,-78,-36,-37,-38,-33,184,-15,-51,-64,-66,-41,-84,-16,-55,-32,-14,-54,-65,-67,-56,-57,]),'CLOSE_PAREN':([14,21,22,23,24,26,27,28,29,31,32,33,38,40,41,42,72,73,74,75,78,80,81,85,87,88,91,92,93,97,98,104,105,106,107,108,109,111,116,120,122,123,124,125,126,130,131,133,140,146,147,153,154,155,156,157,158,159,161,162,167,175,177,180,181,182,186,191,192,196,203,204,205,206,209,],[-88,-115,-76,73,-75,-114,-81,-80,-82,-116,-117,-118,-120,-95,-81,73,119,-86,120,-120,-95,-87,-97,-35,-30,-34,-95,-39,120,-50,-53,-58,-60,-61,-62,-63,73,-119,-40,-83,-74,155,156,-79,-85,159,161,-94,-52,-59,175,-95,181,-77,-78,-96,-31,-36,-37,-38,-51,-64,-66,-41,-84,-112,-55,-93,203,-54,-65,-67,-56,-57,-92,]),'COMMA':([14,21,22,24,26,27,28,29,31,32,33,38,41,73,74,75,78,79,80,81,85,87,88,91,93,97,98,104,105,106,107,108,111,120,122,125,126,130,131,133,140,146,147,148,154,155,156,157,158,159,161,162,167,175,177,181,182,186,191,192,193,196,203,204,205,206,209,],[-88,-115,-76,-75,-114,-81,-80,-82,-116,-117,-118,-120,-81,-86,121,-120,-95,127,-87,-97,-35,-30,-34,-95,121,-50,-53,-58,-60,-61,-62,-63,-119,-83,-74,-79,-85,160,-113,-94,-52,-59,176,178,127,-77,-78,-96,-31,-36,-37,-38,-51,-64,-66,-84,-112,-55,-93,202,202,-54,-65,-67,-56,-57,-92,]),'CLOSE_SQUARE':([14,21,22,24,26,27,28,29,30,31,32,33,38,41,73,78,79,80,81,85,87,88,91,97,98,104,105,106,107,108,110,111,120,122,125,126,132,133,140,146,148,155,156,157,158,159,161,162,167,175,177,181,186,191,193,196,203,204,205,206,209,],[-88,-115,-76,-75,-114,-81,-80,-82,80,-116,-117,-118,-120,-81,-86,-95,126,-87,-97,-35,-30,-34,-95,-50,-53,-58,-60,-61,-62,-63,80,-119,-83,-74,-79,-85,162,-94,-52,-59,177,-77,-78,-96,-31,-36,-37,-38,-51,-64,-66,-84,-55,-93,204,-54,-65,-67,-56,-57,-92,]),'ARROW':([14,21,22,24,26,27,28,29,31,32,33,38,41,73,78,80,85,87,88,91,120,122,125,126,133,141,155,156,159,161,162,168,181,201,],[-88,-115,-76,-75,-114,-81,-80,-82,-116,-117,-118,-120,-81,-86,-95,-87,-35,129,-34,-95,-83,-74,-79,-85,-94,-95,-77,-78,-36,-37,-38,185,-84,208,]),'THEN':([14,21,26,31,32,33,73,80,97,98,104,105,106,107,108,111,140,144,146,167,175,177,186,196,203,204,205,206,],[-88,-115,-114,-116,-117,-118,-86,-87,-50,-53,-58,-60,-61,-62,-63,-119,-52,173,-59,-51,-64,-66,-55,-54,-65,-67,-56,-57,]),'OF':([14,21,26,31,32,33,73,80,97,98,104,105,106,107,108,111,140,145,146,167,175,177,186,196,203,204,205,206,],[-88,-115,-114,-116,-117,-118,-86,-87,-50,-53,-58,-60,-61,-62,-63,-119,-52,174,-59,-51,-64,-66,-55,-54,-65,-67,-56,-57,]),'ELSE':([14,21,26,31,32,33,73,80,97,98,104,105,106,107,108,111,140,146,167,175,177,186,189,196,203,204,205,206,],[-88,-115,-114,-116,-117,-118,-86,-87,-50,-53,-58,-60,-61,-62,-63,-119,-52,-59,-51,-64,-66,-55,198,-54,-65,-67,-56,-57,]),'LEFTASSOC':([20,],[69,]),'RIGHTASSOC':([20,],[70,]),'NONASSOC':([20,],[71,]),'LAMBDA':([46,49,52,54,55,56,57,58,59,60,61,62,63,64,65,66,67,99,102,103,109,110,113,138,139,151,169,173,176,178,185,198,202,208,],[100,100,-89,-98,-99,-100,-101,-102,-103,-104,-105,-106,-107,-108,-109,-110,-111,100,100,100,100,100,100,100,-91,-90,100,100,100,100,100,100,100,100,]),'LET':([46,49,52,54,55,56,57,58,59,60,61,62,63,64,65,66,67,99,102,103,109,110,113,138,139,151,169,173,176,178,185,198,202,208,],[101,101,-89,-98,-99,-100,-101,-102,-103,-104,-105,-106,-107,-108,-109,-110,-111,101,101,101,101,101,101,101,-91,-90,101,101,101,101,101,101,101,101,]),'IF':([46,49,52,54,55,56,57,58,59,60,61,62,63,64,65,66,67,99,102,103,109,110,113,138,139,151,169,173,176,178,185,198,202,208,],[102,102,-89,-98,-99,-100,-101,-102,-103,-104,-105,-106,-107,-108,-109,-110,-111,102,102,102,102,102,102,102,-91,-90,102,102,102,102,102,102,102,102,]),'MATCH':([46,49,52,54,55,56,57,58,59,60,61,62,63,64,65,66,67,99,102,103,109,110,113,138,139,151,169,173,176,178,185,198,202,208,],[103,103,-89,-98,-99,-100,-101,-102,-103,-104,-105,-106,-107,-108,-109,-110,-111,103,103,103,103,103,103,103,-91,-90,103,103,103,103,103,103,103,103,]),'IN':([142,171,187,],[169,-18,-17,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'MODULE_DEFINITION':([0,],[1,]),'BODY':([4,],[5,]),'IMPORT_DECLARATIONS':([6,],[7,]),'TOP_DECLARATIONS':([6,34,],[8,82,]),'IMPORT_DECLARATION':([6,34,],[9,83,]),'TOP_DECLARATION':([6,34,36,],[10,10,84,]),'DECLARATION':([6,34,36,143,188,],[16,16,16,172,172,]),'GEN_DECLARATION':([6,34,36,143,188,],[17,17,17,17,17,]),'FUNCTION_LHS':([6,23,34,36,143,188,],[18,72,18,18,18,18,]),'PAT':([6,23,30,34,36,42,51,76,121,127,143,188,190,207,],[19,74,81,19,19,93,116,122,81,157,19,19,201,201,]),'APAT':([6,12,23,27,30,34,36,40,42,51,75,76,78,91,100,119,121,127,141,143,153,188,190,207,],[22,40,22,78,22,22,22,91,22,22,40,22,91,91,141,153,22,22,91,22,91,22,22,22,]),'LPAT':([6,23,30,34,36,42,51,76,121,127,143,188,190,207,],[24,24,24,24,24,24,24,24,24,24,24,24,24,24,]),'GCON':([6,12,23,27,30,34,36,40,42,46,49,51,75,76,78,91,99,100,102,103,104,109,110,113,119,121,127,138,141,143,153,169,173,176,178,185,188,190,198,202,207,208,],[27,41,27,41,27,27,27,41,27,107,107,27,41,27,41,41,107,41,107,107,107,107,107,107,41,27,27,107,41,27,41,107,107,107,107,107,27,27,107,107,27,107,]),'PARAM':([6,12,23,27,30,34,36,40,42,51,75,76,78,91,100,119,121,127,141,143,153,188,190,207,],[28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,]),'LITERAL':([6,12,23,27,30,34,36,40,42,46,49,51,75,76,78,91,99,100,102,103,104,109,110,113,119,121,127,138,141,143,153,169,173,176,178,185,188,190,198,202,207,208,],[29,29,29,29,29,29,29,29,29,108,108,29,29,29,29,29,108,29,108,108,108,108,108,108,29,29,29,108,29,29,29,108,108,108,108,108,29,29,108,108,29,108,]),'RHS':([18,19,],[45,50,]),'GDRHS':([18,19,150,],[47,47,179,]),'GUARDS':([18,19,150,],[48,48,48,]),'VAROP':([19,74,98,118,],[51,51,139,139,]),'VARSYM':([19,74,98,118,],[52,52,52,52,]),'ASSOCIATIVITY':([20,],[68,]),'PAT_LIST':([30,121,],[79,154,]),'TYPE':([39,89,90,94,129,160,],[86,131,132,134,158,182,]),'ATYPE':([39,89,90,94,129,160,183,],[87,87,87,87,87,87,194,]),'APATS':([40,78,91,141,153,],[92,125,133,168,180,]),'TYPE_PARAMETERS':([44,],[95,]),'EXP':([46,102,103,109,110,113,169,173,176,178,185,198,202,208,],[96,144,145,147,148,150,186,189,191,191,196,205,209,211,]),'INFIX_EXP':([46,49,99,102,103,109,110,113,138,169,173,176,178,185,198,202,208,],[97,115,140,97,97,97,97,97,167,97,97,97,97,97,97,97,97,]),'LEXP':([46,49,99,102,103,109,110,113,138,169,173,176,178,185,198,202,208,],[98,98,98,98,98,98,98,98,98,98,98,98,98,98,98,98,98,]),'FEXP':([46,49,99,102,103,109,110,113,138,169,173,176,178,185,198,202,208,],[104,104,104,104,104,104,104,104,104,104,104,104,104,104,104,104,104,]),'AEXP':([46,49,99,102,103,104,109,110,113,138,169,173,176,178,185,198,202,208,],[105,105,105,105,105,146,105,105,105,105,105,105,105,105,105,105,105,105,]),'USED_VAR':([46,49,99,102,103,104,109,110,113,138,169,173,176,178,185,198,202,208,],[106,106,106,106,106,106,106,106,106,106,106,106,106,106,106,106,106,106,]),'GUARD':([49,],[114,]),'TYPES_LIST':([89,],[130,]),'OP':([98,118,],[138,152,]),'DECLARATIONS':([101,112,137,],[142,149,166,]),'CONSTRUCTORS':([135,],[164,]),'CONSTRUCTOR':([135,184,],[165,195,]),'DECLARATIONS_LIST':([143,188,],[170,197,]),'ATYPES':([163,],[183,]),'EXP_LIST':([176,178,],[192,193,]),'ALTS':([190,207,],[199,210,]),'ALT':([190,207,],[200,200,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> MODULE_DEFINITION","S'",1,None,None,None),
  ('MODULE_DEFINITION -> MODULE IDENTIFIER WHERE BODY','MODULE_DEFINITION',4,'p_MODULE_DEFINITION','funky_parser.py',21),
  ('BODY -> OPEN_BRACE IMPORT_DECLARATIONS ENDSTATEMENT TOP_DECLARATIONS CLOSE_BRACE','BODY',5,'p_BODY','funky_parser.py',27),
  ('BODY -> OPEN_BRACE TOP_DECLARATIONS CLOSE_BRACE','BODY',3,'p_BODY','funky_parser.py',28),
  ('IMPORT_DECLARATIONS -> IMPORT_DECLARATIONS ENDSTATEMENT IMPORT_DECLARATION','IMPORT_DECLARATIONS',3,'p_IMPORT_DECLARATIONS','funky_parser.py',40),
  ('IMPORT_DECLARATIONS -> IMPORT_DECLARATION','IMPORT_DECLARATIONS',1,'p_IMPORT_DECLARATIONS','funky_parser.py',41),
  ('IMPORT_DECLARATION -> IMPORT IDENTIFIER','IMPORT_DECLARATION',2,'p_IMPORT_DECLARATION','funky_parser.py',49),
  ('TOP_DECLARATIONS -> TOP_DECLARATIONS ENDSTATEMENT TOP_DECLARATION','TOP_DECLARATIONS',3,'p_TOP_DECLARATIONS','funky_parser.py',54),
  ('TOP_DECLARATIONS -> TOP_DECLARATION','TOP_DECLARATIONS',1,'p_TOP_DECLARATIONS','funky_parser.py',55),
  ('TOP_DECLARATION -> NEWTYPE TYPENAME EQUALS TYPE','TOP_DECLARATION',4,'p_TOP_DECLARATION','funky_parser.py',63),
  ('TOP_DECLARATION -> NEWCONS TYPENAME TYPE_PARAMETERS EQUALS CONSTRUCTORS','TOP_DECLARATION',5,'p_TOP_DECLARATION','funky_parser.py',64),
  ('TOP_DECLARATION -> DECLARATION','TOP_DECLARATION',1,'p_TOP_DECLARATION','funky_parser.py',65),
  ('TYPE_PARAMETERS -> TYPE_PARAMETERS IDENTIFIER','TYPE_PARAMETERS',2,'p_TYPE_PARAMETERS','funky_parser.py',75),
  ('TYPE_PARAMETERS -> <empty>','TYPE_PARAMETERS',0,'p_TYPE_PARAMETERS','funky_parser.py',76),
  ('CONSTRUCTORS -> CONSTRUCTORS PIPE CONSTRUCTOR','CONSTRUCTORS',3,'p_CONSTRUCTORS','funky_parser.py',84),
  ('CONSTRUCTORS -> CONSTRUCTOR','CONSTRUCTORS',1,'p_CONSTRUCTORS','funky_parser.py',85),
  ('CONSTRUCTOR -> TYPENAME ATYPES','CONSTRUCTOR',2,'p_CONSTRUCTOR','funky_parser.py',93),
  ('DECLARATIONS -> OPEN_BRACE DECLARATIONS_LIST CLOSE_BRACE','DECLARATIONS',3,'p_DECLARATIONS','funky_parser.py',97),
  ('DECLARATIONS -> OPEN_BRACE CLOSE_BRACE','DECLARATIONS',2,'p_DECLARATIONS','funky_parser.py',98),
  ('DECLARATIONS_LIST -> DECLARATION ENDSTATEMENT DECLARATIONS_LIST','DECLARATIONS_LIST',3,'p_DECLARATIONS_LIST','funky_parser.py',106),
  ('DECLARATIONS_LIST -> DECLARATION','DECLARATIONS_LIST',1,'p_DECLARATIONS_LIST','funky_parser.py',107),
  ('DECLARATION -> GEN_DECLARATION','DECLARATION',1,'p_DECLARATION','funky_parser.py',115),
  ('DECLARATION -> FUNCTION_LHS RHS','DECLARATION',2,'p_DECLARATION','funky_parser.py',116),
  ('DECLARATION -> PAT RHS','DECLARATION',2,'p_DECLARATION','funky_parser.py',117),
  ('GEN_DECLARATION -> IDENTIFIER TYPESIG TYPE','GEN_DECLARATION',3,'p_GEN_DECLARATION','funky_parser.py',127),
  ('GEN_DECLARATION -> SETFIX ASSOCIATIVITY INTEGER OP','GEN_DECLARATION',4,'p_GEN_DECLARATION','funky_parser.py',128),
  ('GEN_DECLARATION -> <empty>','GEN_DECLARATION',0,'p_GEN_DECLARATION','funky_parser.py',129),
  ('ASSOCIATIVITY -> LEFTASSOC','ASSOCIATIVITY',1,'p_ASSOCIATIVITY','funky_parser.py',137),
  ('ASSOCIATIVITY -> RIGHTASSOC','ASSOCIATIVITY',1,'p_ASSOCIATIVITY','funky_parser.py',138),
  ('ASSOCIATIVITY -> NONASSOC','ASSOCIATIVITY',1,'p_ASSOCIATIVITY','funky_parser.py',139),
  ('TYPE -> ATYPE','TYPE',1,'p_TYPE','funky_parser.py',144),
  ('TYPE -> ATYPE ARROW TYPE','TYPE',3,'p_TYPE','funky_parser.py',145),
  ('ATYPES -> ATYPES ATYPE','ATYPES',2,'p_ATYPES','funky_parser.py',153),
  ('ATYPES -> <empty>','ATYPES',0,'p_ATYPES','funky_parser.py',154),
  ('ATYPE -> TYPENAME','ATYPE',1,'p_ATYPE','funky_parser.py',162),
  ('ATYPE -> IDENTIFIER','ATYPE',1,'p_ATYPE','funky_parser.py',163),
  ('ATYPE -> OPEN_PAREN TYPES_LIST CLOSE_PAREN','ATYPE',3,'p_ATYPE','funky_parser.py',164),
  ('ATYPE -> OPEN_PAREN TYPE CLOSE_PAREN','ATYPE',3,'p_ATYPE','funky_parser.py',165),
  ('ATYPE -> OPEN_SQUARE TYPE CLOSE_SQUARE','ATYPE',3,'p_ATYPE','funky_parser.py',166),
  ('FUNCTION_LHS -> IDENTIFIER APAT APATS','FUNCTION_LHS',3,'p_FUNCTION_LHS','funky_parser.py',179),
  ('FUNCTION_LHS -> PAT VAROP PAT','FUNCTION_LHS',3,'p_FUNCTION_LHS','funky_parser.py',180),
  ('FUNCTION_LHS -> OPEN_PAREN FUNCTION_LHS CLOSE_PAREN APAT APATS','FUNCTION_LHS',5,'p_FUNCTION_LHS','funky_parser.py',181),
  ('RHS -> EQUALS EXP','RHS',2,'p_RHS','funky_parser.py',193),
  ('RHS -> EQUALS EXP WHERE DECLARATIONS','RHS',4,'p_RHS','funky_parser.py',194),
  ('RHS -> GDRHS','RHS',1,'p_RHS','funky_parser.py',195),
  ('RHS -> GDRHS WHERE DECLARATIONS','RHS',3,'p_RHS','funky_parser.py',196),
  ('GDRHS -> GUARDS EQUALS EXP','GDRHS',3,'p_GDRHS','funky_parser.py',209),
  ('GDRHS -> GUARDS EQUALS EXP GDRHS','GDRHS',4,'p_GDRHS','funky_parser.py',210),
  ('GUARDS -> PIPE GUARD','GUARDS',2,'p_GUARDS','funky_parser.py',218),
  ('GUARD -> INFIX_EXP','GUARD',1,'p_GUARD','funky_parser.py',223),
  ('EXP -> INFIX_EXP','EXP',1,'p_EXP','funky_parser.py',229),
  ('INFIX_EXP -> LEXP OP INFIX_EXP','INFIX_EXP',3,'p_INFIX_EXP','funky_parser.py',235),
  ('INFIX_EXP -> MINUS INFIX_EXP','INFIX_EXP',2,'p_INFIX_EXP','funky_parser.py',236),
  ('INFIX_EXP -> LEXP','INFIX_EXP',1,'p_INFIX_EXP','funky_parser.py',237),
  ('LEXP -> LAMBDA APAT APATS ARROW EXP','LEXP',5,'p_LEXP','funky_parser.py',255),
  ('LEXP -> LET DECLARATIONS IN EXP','LEXP',4,'p_LEXP','funky_parser.py',256),
  ('LEXP -> IF EXP THEN EXP ELSE EXP','LEXP',6,'p_LEXP','funky_parser.py',257),
  ('LEXP -> MATCH EXP OF OPEN_BRACE ALTS CLOSE_BRACE','LEXP',6,'p_LEXP','funky_parser.py',258),
  ('LEXP -> FEXP','LEXP',1,'p_LEXP','funky_parser.py',259),
  ('FEXP -> FEXP AEXP','FEXP',2,'p_FEXP','funky_parser.py',274),
  ('FEXP -> AEXP','FEXP',1,'p_FEXP','funky_parser.py',275),
  ('AEXP -> USED_VAR','AEXP',1,'p_AEXP','funky_parser.py',283),
  ('AEXP -> GCON','AEXP',1,'p_AEXP','funky_parser.py',284),
  ('AEXP -> LITERAL','AEXP',1,'p_AEXP','funky_parser.py',285),
  ('AEXP -> OPEN_PAREN EXP CLOSE_PAREN','AEXP',3,'p_AEXP','funky_parser.py',286),
  ('AEXP -> OPEN_PAREN EXP COMMA EXP_LIST CLOSE_PAREN','AEXP',5,'p_AEXP','funky_parser.py',287),
  ('AEXP -> OPEN_SQUARE EXP CLOSE_SQUARE','AEXP',3,'p_AEXP','funky_parser.py',288),
  ('AEXP -> OPEN_SQUARE EXP COMMA EXP_LIST CLOSE_SQUARE','AEXP',5,'p_AEXP','funky_parser.py',289),
  ('CONSTRUCTION_PARAMS -> CONSTRUCTION_PARAMS AEXP','CONSTRUCTION_PARAMS',2,'p_CONSTRUCTION_PARAMS','funky_parser.py',312),
  ('CONSTRUCTION_PARAMS -> AEXP','CONSTRUCTION_PARAMS',1,'p_CONSTRUCTION_PARAMS','funky_parser.py',313),
  ('ALTS -> ALT ENDSTATEMENT ALTS','ALTS',3,'p_ALTS','funky_parser.py',321),
  ('ALTS -> ALT','ALTS',1,'p_ALTS','funky_parser.py',322),
  ('ALT -> PAT ARROW EXP','ALT',3,'p_ALT','funky_parser.py',330),
  ('ALT -> <empty>','ALT',0,'p_ALT','funky_parser.py',331),
  ('PAT -> LPAT LIST_CONSTRUCTOR PAT','PAT',3,'p_PAT','funky_parser.py',336),
  ('PAT -> LPAT','PAT',1,'p_PAT','funky_parser.py',337),
  ('LPAT -> APAT','LPAT',1,'p_LPAT','funky_parser.py',345),
  ('LPAT -> MINUS OPEN_PAREN INTEGER CLOSE_PAREN','LPAT',4,'p_LPAT','funky_parser.py',346),
  ('LPAT -> MINUS OPEN_PAREN FLOAT CLOSE_PAREN','LPAT',4,'p_LPAT','funky_parser.py',347),
  ('LPAT -> GCON APAT APATS','LPAT',3,'p_LPAT','funky_parser.py',348),
  ('APAT -> PARAM','APAT',1,'p_APAT','funky_parser.py',358),
  ('APAT -> GCON','APAT',1,'p_APAT','funky_parser.py',359),
  ('APAT -> LITERAL','APAT',1,'p_APAT','funky_parser.py',360),
  ('APAT -> OPEN_PAREN PAT CLOSE_PAREN','APAT',3,'p_APAT','funky_parser.py',361),
  ('APAT -> OPEN_PAREN PAT COMMA PAT_LIST CLOSE_PAREN','APAT',5,'p_APAT','funky_parser.py',362),
  ('APAT -> OPEN_SQUARE PAT_LIST CLOSE_SQUARE','APAT',3,'p_APAT','funky_parser.py',363),
  ('GCON -> OPEN_PAREN CLOSE_PAREN','GCON',2,'p_GCON','funky_parser.py',380),
  ('GCON -> OPEN_SQUARE CLOSE_SQUARE','GCON',2,'p_GCON','funky_parser.py',381),
  ('GCON -> TYPENAME','GCON',1,'p_GCON','funky_parser.py',382),
  ('VAROP -> VARSYM','VAROP',1,'p_VAROP','funky_parser.py',392),
  ('VAROP -> BACKTICK IDENTIFIER BACKTICK','VAROP',3,'p_VAROP','funky_parser.py',393),
  ('OP -> VAROP','OP',1,'p_OP','funky_parser.py',403),
  ('EXP_LIST -> EXP_LIST COMMA EXP','EXP_LIST',3,'p_EXP_LIST','funky_parser.py',408),
  ('EXP_LIST -> EXP','EXP_LIST',1,'p_EXP_LIST','funky_parser.py',409),
  ('APATS -> APAT APATS','APATS',2,'p_APATS','funky_parser.py',417),
  ('APATS -> <empty>','APATS',0,'p_APATS','funky_parser.py',418),
  ('PAT_LIST -> PAT_LIST COMMA PAT','PAT_LIST',3,'p_PAT_LIST','funky_parser.py',426),
  ('PAT_LIST -> PAT','PAT_LIST',1,'p_PAT_LIST','funky_parser.py',427),
  ('VARSYM -> PLUS','VARSYM',1,'p_VARSYM','funky_parser.py',436),
  ('VARSYM -> MINUS','VARSYM',1,'p_VARSYM','funky_parser.py',437),
  ('VARSYM -> TIMES','VARSYM',1,'p_VARSYM','funky_parser.py',438),
  ('VARSYM -> DIVIDE','VARSYM',1,'p_VARSYM','funky_parser.py',439),
  ('VARSYM -> POW','VARSYM',1,'p_VARSYM','funky_parser.py',440),
  ('VARSYM -> EQUALITY','VARSYM',1,'p_VARSYM','funky_parser.py',441),
  ('VARSYM -> INEQUALITY','VARSYM',1,'p_VARSYM','funky_parser.py',442),
  ('VARSYM -> LESS','VARSYM',1,'p_VARSYM','funky_parser.py',443),
  ('VARSYM -> LEQ','VARSYM',1,'p_VARSYM','funky_parser.py',444),
  ('VARSYM -> GREATER','VARSYM',1,'p_VARSYM','funky_parser.py',445),
  ('VARSYM -> GEQ','VARSYM',1,'p_VARSYM','funky_parser.py',446),
  ('VARSYM -> AND','VARSYM',1,'p_VARSYM','funky_parser.py',447),
  ('VARSYM -> OR','VARSYM',1,'p_VARSYM','funky_parser.py',448),
  ('VARSYM -> LIST_CONSTRUCTOR','VARSYM',1,'p_VARSYM','funky_parser.py',449),
  ('TYPES_LIST -> TYPES_LIST COMMA TYPE','TYPES_LIST',3,'p_TYPES_LIST','funky_parser.py',454),
  ('TYPES_LIST -> TYPE','TYPES_LIST',1,'p_TYPES_LIST','funky_parser.py',455),
  ('LITERAL -> FLOAT','LITERAL',1,'p_LITERAL','funky_parser.py',463),
  ('LITERAL -> INTEGER','LITERAL',1,'p_LITERAL','funky_parser.py',464),
  ('LITERAL -> BOOL','LITERAL',1,'p_LITERAL','funky_parser.py',465),
  ('LITERAL -> CHAR','LITERAL',1,'p_LITERAL','funky_parser.py',466),
  ('LITERAL -> STRING','LITERAL',1,'p_LITERAL','funky_parser.py',467),
  ('USED_VAR -> IDENTIFIER','USED_VAR',1,'p_USED_VAR','funky_parser.py',472),
  ('PARAM -> IDENTIFIER','PARAM',1,'p_PARAM','funky_parser.py',476),
]
