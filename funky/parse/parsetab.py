
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'MODULE_DEFINITIONAND ARROW BACKTICK BOOL CHAR CLOSE_BRACE CLOSE_PAREN CLOSE_SQUARE DIVIDE ELSE ENDSTATEMENT EQUALITY EQUALS FLOAT GEQ GREATER IDENTIFIER IF IMPORT IN INEQUALITY INTEGER LAMBDA LEFTASSOC LEQ LESS LET MATCH MINUS MODULE MODULO NEWCONS NEWTYPE NONASSOC OF OPEN_BRACE OPEN_PAREN OPEN_SQUARE OR PIPE PLUS POW RIGHTASSOC SETFIX STRING THEN TIMES TYPENAME WHERE WHITESPACEMODULE_DEFINITION : MODULE IDENTIFIER WHERE BODY\n        BODY : OPEN_BRACE IMPORT_DECLARATIONS ENDSTATEMENT TOP_DECLARATIONS CLOSE_BRACE\n                | OPEN_BRACE TOP_DECLARATIONS CLOSE_BRACE\n        IMPORT_DECLARATIONS : IMPORT_DECLARATIONS ENDSTATEMENT IMPORT_DECLARATION\n                               | IMPORT_DECLARATION\n        IMPORT_DECLARATION : IMPORT IDENTIFIER\n        TOP_DECLARATIONS : TOP_DECLARATIONS ENDSTATEMENT TOP_DECLARATION\n                            | TOP_DECLARATION\n        TOP_DECLARATION : NEW_CONS\n                           | DECLARATION\n        NEW_CONS : NEWCONS TYPENAME EQUALS CONSTRUCTORSCONSTRUCTORS : CONSTRUCTORS PIPE CONSTRUCTOR\n                        | CONSTRUCTOR\n        CONSTRUCTOR : TYPENAME ATYPESDECLARATIONS : OPEN_BRACE DECLARATIONS_LIST CLOSE_BRACE\n                        | OPEN_BRACE CLOSE_BRACE\n        DECLARATIONS_LIST : DECLARATION ENDSTATEMENT DECLARATIONS_LIST\n                             | DECLARATION\n        DECLARATION : GEN_DECLARATION\n                       | FUNCTION_LHS RHS\n                       | LPAT RHS\n        GEN_DECLARATION : FIXITY_DECLARATION\n                           |\n        FIXITY_DECLARATION : SETFIX ASSOCIATIVITY INTEGER OPASSOCIATIVITY : LEFTASSOC\n                         | RIGHTASSOC\n                         | NONASSOC\n        TYPE : ATYPE\n                | ATYPE ARROW TYPE\n        ATYPES : ATYPES ATYPE\n                  |\n        ATYPE : TYPENAME\n                 | OPEN_PAREN TYPE CLOSE_PAREN\n        FUNCTION_LHS : IDENTIFIER APAT APATS\n                        | LPAT VAROP LPAT\n                        | OPEN_PAREN FUNCTION_LHS CLOSE_PAREN APAT APATS\n        RHS : EQUALS EXP\n               | EQUALS EXP WHERE DECLARATIONS\n               | GDRHS\n               | GDRHS WHERE DECLARATIONS\n        GDRHS : PIPE EXP EQUALS EXP\n                 | PIPE EXP EQUALS EXP GDRHS\n        EXP : INFIX_EXP\n        INFIX_EXP : LEXP OP INFIX_EXP\n                     | MINUS INFIX_EXP\n                     | LEXP\n        LEXP : LAMBDA APAT APATS ARROW EXP\n                | LET DECLARATIONS IN EXP\n                | IF EXP THEN EXP ELSE EXP\n                | MATCH EXP OF OPEN_BRACE ALTS CLOSE_BRACE\n                | FEXP\n        FEXP : FEXP AEXP\n                | AEXP\n        AEXP : USED_VAR\n                | TYPENAME\n                | LITERAL\n                | OPEN_PAREN EXP CLOSE_PAREN\n        CONSTRUCTION_PARAMS : CONSTRUCTION_PARAMS AEXP\n                               | AEXP\n        ALTS : ALT ENDSTATEMENT ALTS\n                | ALT\n        ALT : LPAT ARROW EXP\n               |\n        LPAT : APAT\n                | MINUS OPEN_PAREN INTEGER CLOSE_PAREN\n                | MINUS OPEN_PAREN FLOAT CLOSE_PAREN\n                | TYPENAME APAT APATS\n        APAT : PARAM\n                | TYPENAME\n                | LITERAL\n                | OPEN_PAREN LPAT CLOSE_PAREN\n        VAROP : VARSYM\n                 | BACKTICK IDENTIFIER BACKTICK\n        OP : VAROP\n        APATS : APAT APATS\n                 |\n        VARSYM : PLUS\n                  | MINUS\n                  | TIMES\n                  | DIVIDE\n                  | MODULO\n                  | POW\n                  | EQUALITY\n                  | INEQUALITY\n                  | LESS\n                  | LEQ\n                  | GREATER\n                  | GEQ\n                  | AND\n                  | OR\n        LITERAL : FLOAT\n                   | INTEGER\n                   | BOOL\n                   | CHAR\n                   | STRING\n        USED_VAR : IDENTIFIERPARAM : IDENTIFIER'
    
_lr_action_items = {'MODULE':([0,],[2,]),'$end':([1,5,33,103,],[0,-1,-3,-2,]),'IDENTIFIER':([2,6,11,12,16,22,24,25,27,28,29,30,31,32,34,36,37,38,39,41,43,45,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,74,82,83,85,86,87,88,89,90,91,92,93,98,99,109,110,112,114,117,120,121,122,131,135,137,144,147,149,155,163,164,],[3,12,35,36,36,12,-92,-91,-68,-70,-93,-94,-95,12,12,-97,36,-69,36,36,93,93,36,-72,97,-77,-78,-79,-80,-81,-82,-83,-84,-85,-86,-87,-88,-89,-90,36,93,36,93,93,93,-53,-54,-55,-56,93,-96,36,-71,93,-74,36,12,-52,93,-73,36,93,93,-57,93,12,36,93,36,93,]),'WHERE':([3,24,25,29,30,31,44,79,80,81,87,88,89,90,91,93,111,117,129,137,138,145,150,153,161,162,],[4,-92,-91,-93,-94,-95,94,108,-43,-46,-51,-53,-54,-55,-56,-96,-45,-52,-44,-57,-41,-48,-42,-47,-49,-50,]),'OPEN_BRACE':([4,84,94,108,136,],[6,114,114,114,149,]),'IMPORT':([6,32,],[11,11,]),'NEWCONS':([6,32,34,],[15,15,15,]),'CLOSE_BRACE':([6,8,10,13,14,17,20,24,25,29,30,31,32,34,42,44,46,48,50,51,52,53,54,55,56,57,58,59,60,61,62,63,71,73,79,80,81,87,88,89,90,91,93,105,106,107,110,111,114,117,119,121,125,126,128,129,132,133,134,137,138,140,141,143,145,146,147,149,150,153,154,156,157,159,161,162,163,166,167,],[-23,33,-8,-9,-10,-19,-22,-92,-91,-93,-94,-95,-23,-23,-20,-39,-21,-72,-77,-78,-79,-80,-81,-82,-83,-84,-85,-86,-87,-88,-89,-90,103,-7,-37,-43,-46,-51,-53,-54,-55,-56,-96,-31,-11,-13,-74,-45,133,-52,-40,-73,-24,-14,-38,-44,146,-16,-18,-57,-41,-32,-30,-12,-48,-15,-23,-63,-42,-47,-17,162,-61,-33,-49,-50,-63,-60,-62,]),'ENDSTATEMENT':([6,7,8,9,10,13,14,17,20,24,25,29,30,31,32,34,35,42,44,46,48,50,51,52,53,54,55,56,57,58,59,60,61,62,63,71,72,73,79,80,81,87,88,89,90,91,93,105,106,107,110,111,114,117,119,121,125,126,128,129,133,134,137,138,140,141,143,145,146,147,149,150,153,157,159,161,162,163,167,],[-23,32,34,-5,-8,-9,-10,-19,-22,-92,-91,-93,-94,-95,-23,-23,-6,-20,-39,-21,-72,-77,-78,-79,-80,-81,-82,-83,-84,-85,-86,-87,-88,-89,-90,34,-4,-7,-37,-43,-46,-51,-53,-54,-55,-56,-96,-31,-11,-13,-74,-45,-23,-52,-40,-73,-24,-14,-38,-44,-16,147,-57,-41,-32,-30,-12,-48,-15,-23,-63,-42,-47,163,-33,-49,-50,-63,-62,]),'OPEN_PAREN':([6,12,16,22,23,24,25,27,28,29,30,31,32,34,36,37,38,39,41,43,45,47,48,50,51,52,53,54,55,56,57,58,59,60,61,62,63,74,82,83,85,86,87,88,89,90,91,92,93,98,99,105,109,110,112,114,117,120,121,122,126,131,135,137,140,141,142,144,147,149,155,159,160,163,164,],[22,39,39,22,66,-92,-91,-68,-70,-93,-94,-95,22,22,-97,39,-69,39,39,92,92,39,-72,-77,-78,-79,-80,-81,-82,-83,-84,-85,-86,-87,-88,-89,-90,39,92,39,92,92,92,-53,-54,-55,-56,92,-96,39,-71,-31,92,-74,39,22,-52,92,-73,39,142,92,92,-57,-32,-30,142,92,22,39,92,-33,142,39,92,]),'MINUS':([6,12,16,19,21,22,24,25,27,28,29,30,31,32,34,36,38,39,41,43,45,47,48,50,51,52,53,54,55,56,57,58,59,60,61,62,63,65,74,78,80,81,82,85,86,87,88,89,90,91,92,93,99,102,104,109,110,111,114,117,120,121,123,124,129,131,135,137,144,145,147,149,153,155,161,162,163,164,],[23,-97,-69,51,-64,23,-92,-91,-68,-70,-93,-94,-95,23,23,-97,-69,23,-76,82,82,23,-72,-77,-78,-79,-80,-81,-82,-83,-84,-85,-86,-87,-88,-89,-90,51,-76,-67,-43,51,82,82,82,-51,-53,-54,-55,-56,82,-96,-71,51,-75,82,-74,-45,23,-52,82,-73,-65,-66,-44,82,82,-57,82,-48,23,23,-47,82,-49,-50,23,82,]),'TYPENAME':([6,12,15,16,22,24,25,27,28,29,30,31,32,34,36,37,38,39,41,43,45,47,48,50,51,52,53,54,55,56,57,58,59,60,61,62,63,74,77,82,83,85,86,87,88,89,90,91,92,93,98,99,105,109,110,112,114,117,120,121,122,126,127,131,135,137,140,141,142,144,147,149,155,159,160,163,164,],[16,38,40,38,16,-92,-91,-68,-70,-93,-94,-95,16,16,-97,38,-69,16,38,90,90,16,-72,-77,-78,-79,-80,-81,-82,-83,-84,-85,-86,-87,-88,-89,-90,38,105,90,38,90,90,90,-53,-54,-55,-56,90,-96,38,-71,-31,90,-74,38,16,-52,90,-73,38,140,105,90,90,-57,-32,-30,140,90,16,16,90,-33,140,16,90,]),'SETFIX':([6,32,34,114,147,],[26,26,26,26,26,]),'FLOAT':([6,12,16,22,24,25,27,28,29,30,31,32,34,36,37,38,39,41,43,45,47,48,50,51,52,53,54,55,56,57,58,59,60,61,62,63,66,74,82,83,85,86,87,88,89,90,91,92,93,98,99,109,110,112,114,117,120,121,122,131,135,137,144,147,149,155,163,164,],[25,25,25,25,-92,-91,-68,-70,-93,-94,-95,25,25,-97,25,-69,25,25,25,25,25,-72,-77,-78,-79,-80,-81,-82,-83,-84,-85,-86,-87,-88,-89,-90,101,25,25,25,25,25,25,-53,-54,-55,-56,25,-96,25,-71,25,-74,25,25,-52,25,-73,25,25,25,-57,25,25,25,25,25,25,]),'INTEGER':([6,12,16,22,24,25,27,28,29,30,31,32,34,36,37,38,39,41,43,45,47,48,50,51,52,53,54,55,56,57,58,59,60,61,62,63,66,67,68,69,70,74,82,83,85,86,87,88,89,90,91,92,93,98,99,109,110,112,114,117,120,121,122,131,135,137,144,147,149,155,163,164,],[24,24,24,24,-92,-91,-68,-70,-93,-94,-95,24,24,-97,24,-69,24,24,24,24,24,-72,-77,-78,-79,-80,-81,-82,-83,-84,-85,-86,-87,-88,-89,-90,100,102,-25,-26,-27,24,24,24,24,24,24,-53,-54,-55,-56,24,-96,24,-71,24,-74,24,24,-52,24,-73,24,24,24,-57,24,24,24,24,24,24,]),'BOOL':([6,12,16,22,24,25,27,28,29,30,31,32,34,36,37,38,39,41,43,45,47,48,50,51,52,53,54,55,56,57,58,59,60,61,62,63,74,82,83,85,86,87,88,89,90,91,92,93,98,99,109,110,112,114,117,120,121,122,131,135,137,144,147,149,155,163,164,],[29,29,29,29,-92,-91,-68,-70,-93,-94,-95,29,29,-97,29,-69,29,29,29,29,29,-72,-77,-78,-79,-80,-81,-82,-83,-84,-85,-86,-87,-88,-89,-90,29,29,29,29,29,29,-53,-54,-55,-56,29,-96,29,-71,29,-74,29,29,-52,29,-73,29,29,29,-57,29,29,29,29,29,29,]),'CHAR':([6,12,16,22,24,25,27,28,29,30,31,32,34,36,37,38,39,41,43,45,47,48,50,51,52,53,54,55,56,57,58,59,60,61,62,63,74,82,83,85,86,87,88,89,90,91,92,93,98,99,109,110,112,114,117,120,121,122,131,135,137,144,147,149,155,163,164,],[30,30,30,30,-92,-91,-68,-70,-93,-94,-95,30,30,-97,30,-69,30,30,30,30,30,-72,-77,-78,-79,-80,-81,-82,-83,-84,-85,-86,-87,-88,-89,-90,30,30,30,30,30,30,-53,-54,-55,-56,30,-96,30,-71,30,-74,30,30,-52,30,-73,30,30,30,-57,30,30,30,30,30,30,]),'STRING':([6,12,16,22,24,25,27,28,29,30,31,32,34,36,37,38,39,41,43,45,47,48,50,51,52,53,54,55,56,57,58,59,60,61,62,63,74,82,83,85,86,87,88,89,90,91,92,93,98,99,109,110,112,114,117,120,121,122,131,135,137,144,147,149,155,163,164,],[31,31,31,31,-92,-91,-68,-70,-93,-94,-95,31,31,-97,31,-69,31,31,31,31,31,-72,-77,-78,-79,-80,-81,-82,-83,-84,-85,-86,-87,-88,-89,-90,31,31,31,31,31,31,-53,-54,-55,-56,31,-96,31,-71,31,-74,31,31,-52,31,-73,31,31,31,-57,31,31,31,31,31,31,]),'EQUALS':([12,16,18,19,21,24,25,27,28,29,30,31,36,37,38,40,41,74,75,78,80,81,87,88,89,90,91,93,95,96,99,104,111,117,122,123,124,129,137,139,145,153,161,162,],[-97,-69,43,43,-64,-92,-91,-68,-70,-93,-94,-95,-97,-76,-69,77,-76,-76,-34,-67,-43,-46,-51,-53,-54,-55,-56,-96,120,-35,-71,-75,-45,-52,-76,-65,-66,-44,-57,-36,-48,-47,-49,-50,]),'BACKTICK':([12,16,19,21,24,25,27,28,29,30,31,36,38,41,65,74,78,80,81,87,88,89,90,91,93,97,99,102,104,111,117,123,124,129,137,145,153,161,162,],[-97,-69,49,-64,-92,-91,-68,-70,-93,-94,-95,-97,-69,-76,49,-76,-67,-43,49,-51,-53,-54,-55,-56,-96,121,-71,49,-75,-45,-52,-65,-66,-44,-57,-48,-47,-49,-50,]),'PIPE':([12,16,18,19,21,24,25,27,28,29,30,31,36,37,38,41,74,75,78,80,81,87,88,89,90,91,93,96,99,104,105,106,107,111,117,122,123,124,126,129,137,138,139,140,141,143,145,153,159,161,162,],[-97,-69,45,45,-64,-92,-91,-68,-70,-93,-94,-95,-97,-76,-69,-76,-76,-34,-67,-43,-46,-51,-53,-54,-55,-56,-96,-35,-71,-75,-31,127,-13,-45,-52,-76,-65,-66,-14,-44,-57,45,-36,-32,-30,-12,-48,-47,-33,-49,-50,]),'PLUS':([12,16,19,21,24,25,27,28,29,30,31,36,38,41,65,74,78,80,81,87,88,89,90,91,93,99,102,104,111,117,123,124,129,137,145,153,161,162,],[-97,-69,50,-64,-92,-91,-68,-70,-93,-94,-95,-97,-69,-76,50,-76,-67,-43,50,-51,-53,-54,-55,-56,-96,-71,50,-75,-45,-52,-65,-66,-44,-57,-48,-47,-49,-50,]),'TIMES':([12,16,19,21,24,25,27,28,29,30,31,36,38,41,65,74,78,80,81,87,88,89,90,91,93,99,102,104,111,117,123,124,129,137,145,153,161,162,],[-97,-69,52,-64,-92,-91,-68,-70,-93,-94,-95,-97,-69,-76,52,-76,-67,-43,52,-51,-53,-54,-55,-56,-96,-71,52,-75,-45,-52,-65,-66,-44,-57,-48,-47,-49,-50,]),'DIVIDE':([12,16,19,21,24,25,27,28,29,30,31,36,38,41,65,74,78,80,81,87,88,89,90,91,93,99,102,104,111,117,123,124,129,137,145,153,161,162,],[-97,-69,53,-64,-92,-91,-68,-70,-93,-94,-95,-97,-69,-76,53,-76,-67,-43,53,-51,-53,-54,-55,-56,-96,-71,53,-75,-45,-52,-65,-66,-44,-57,-48,-47,-49,-50,]),'MODULO':([12,16,19,21,24,25,27,28,29,30,31,36,38,41,65,74,78,80,81,87,88,89,90,91,93,99,102,104,111,117,123,124,129,137,145,153,161,162,],[-97,-69,54,-64,-92,-91,-68,-70,-93,-94,-95,-97,-69,-76,54,-76,-67,-43,54,-51,-53,-54,-55,-56,-96,-71,54,-75,-45,-52,-65,-66,-44,-57,-48,-47,-49,-50,]),'POW':([12,16,19,21,24,25,27,28,29,30,31,36,38,41,65,74,78,80,81,87,88,89,90,91,93,99,102,104,111,117,123,124,129,137,145,153,161,162,],[-97,-69,55,-64,-92,-91,-68,-70,-93,-94,-95,-97,-69,-76,55,-76,-67,-43,55,-51,-53,-54,-55,-56,-96,-71,55,-75,-45,-52,-65,-66,-44,-57,-48,-47,-49,-50,]),'EQUALITY':([12,16,19,21,24,25,27,28,29,30,31,36,38,41,65,74,78,80,81,87,88,89,90,91,93,99,102,104,111,117,123,124,129,137,145,153,161,162,],[-97,-69,56,-64,-92,-91,-68,-70,-93,-94,-95,-97,-69,-76,56,-76,-67,-43,56,-51,-53,-54,-55,-56,-96,-71,56,-75,-45,-52,-65,-66,-44,-57,-48,-47,-49,-50,]),'INEQUALITY':([12,16,19,21,24,25,27,28,29,30,31,36,38,41,65,74,78,80,81,87,88,89,90,91,93,99,102,104,111,117,123,124,129,137,145,153,161,162,],[-97,-69,57,-64,-92,-91,-68,-70,-93,-94,-95,-97,-69,-76,57,-76,-67,-43,57,-51,-53,-54,-55,-56,-96,-71,57,-75,-45,-52,-65,-66,-44,-57,-48,-47,-49,-50,]),'LESS':([12,16,19,21,24,25,27,28,29,30,31,36,38,41,65,74,78,80,81,87,88,89,90,91,93,99,102,104,111,117,123,124,129,137,145,153,161,162,],[-97,-69,58,-64,-92,-91,-68,-70,-93,-94,-95,-97,-69,-76,58,-76,-67,-43,58,-51,-53,-54,-55,-56,-96,-71,58,-75,-45,-52,-65,-66,-44,-57,-48,-47,-49,-50,]),'LEQ':([12,16,19,21,24,25,27,28,29,30,31,36,38,41,65,74,78,80,81,87,88,89,90,91,93,99,102,104,111,117,123,124,129,137,145,153,161,162,],[-97,-69,59,-64,-92,-91,-68,-70,-93,-94,-95,-97,-69,-76,59,-76,-67,-43,59,-51,-53,-54,-55,-56,-96,-71,59,-75,-45,-52,-65,-66,-44,-57,-48,-47,-49,-50,]),'GREATER':([12,16,19,21,24,25,27,28,29,30,31,36,38,41,65,74,78,80,81,87,88,89,90,91,93,99,102,104,111,117,123,124,129,137,145,153,161,162,],[-97,-69,60,-64,-92,-91,-68,-70,-93,-94,-95,-97,-69,-76,60,-76,-67,-43,60,-51,-53,-54,-55,-56,-96,-71,60,-75,-45,-52,-65,-66,-44,-57,-48,-47,-49,-50,]),'GEQ':([12,16,19,21,24,25,27,28,29,30,31,36,38,41,65,74,78,80,81,87,88,89,90,91,93,99,102,104,111,117,123,124,129,137,145,153,161,162,],[-97,-69,61,-64,-92,-91,-68,-70,-93,-94,-95,-97,-69,-76,61,-76,-67,-43,61,-51,-53,-54,-55,-56,-96,-71,61,-75,-45,-52,-65,-66,-44,-57,-48,-47,-49,-50,]),'AND':([12,16,19,21,24,25,27,28,29,30,31,36,38,41,65,74,78,80,81,87,88,89,90,91,93,99,102,104,111,117,123,124,129,137,145,153,161,162,],[-97,-69,62,-64,-92,-91,-68,-70,-93,-94,-95,-97,-69,-76,62,-76,-67,-43,62,-51,-53,-54,-55,-56,-96,-71,62,-75,-45,-52,-65,-66,-44,-57,-48,-47,-49,-50,]),'OR':([12,16,19,21,24,25,27,28,29,30,31,36,38,41,65,74,78,80,81,87,88,89,90,91,93,99,102,104,111,117,123,124,129,137,145,153,161,162,],[-97,-69,63,-64,-92,-91,-68,-70,-93,-94,-95,-97,-69,-76,63,-76,-67,-43,63,-51,-53,-54,-55,-56,-96,-71,63,-75,-45,-52,-65,-66,-44,-57,-48,-47,-49,-50,]),'CLOSE_PAREN':([12,16,21,24,25,27,28,29,30,31,36,37,38,41,64,65,74,75,76,78,80,81,87,88,89,90,91,93,96,99,100,101,104,111,117,118,122,123,124,129,137,139,140,145,151,152,153,159,161,162,165,],[-97,-69,-64,-92,-91,-68,-70,-93,-94,-95,-97,-76,-69,-76,98,99,-76,-34,99,-67,-43,-46,-51,-53,-54,-55,-56,-96,-35,-71,123,124,-75,-45,-52,137,-76,-65,-66,-44,-57,-36,-32,-48,159,-28,-47,-33,-49,-50,-29,]),'ARROW':([16,21,24,25,27,28,29,30,31,36,38,41,74,78,99,104,112,123,124,130,140,152,158,159,],[-69,-64,-92,-91,-68,-70,-93,-94,-95,-97,-69,-76,-76,-67,-71,-75,-76,-65,-66,144,-32,160,164,-33,]),'THEN':([24,25,29,30,31,80,81,87,88,89,90,91,93,111,115,117,129,137,145,153,161,162,],[-92,-91,-93,-94,-95,-43,-46,-51,-53,-54,-55,-56,-96,-45,135,-52,-44,-57,-48,-47,-49,-50,]),'OF':([24,25,29,30,31,80,81,87,88,89,90,91,93,111,116,117,129,137,145,153,161,162,],[-92,-91,-93,-94,-95,-43,-46,-51,-53,-54,-55,-56,-96,-45,136,-52,-44,-57,-48,-47,-49,-50,]),'ELSE':([24,25,29,30,31,80,81,87,88,89,90,91,93,111,117,129,137,145,148,153,161,162,],[-92,-91,-93,-94,-95,-43,-46,-51,-53,-54,-55,-56,-96,-45,-52,-44,-57,-48,155,-47,-49,-50,]),'LEFTASSOC':([26,],[68,]),'RIGHTASSOC':([26,],[69,]),'NONASSOC':([26,],[70,]),'LAMBDA':([43,45,48,50,51,52,53,54,55,56,57,58,59,60,61,62,63,82,85,86,92,109,110,120,121,131,135,144,155,164,],[83,83,-72,-77,-78,-79,-80,-81,-82,-83,-84,-85,-86,-87,-88,-89,-90,83,83,83,83,83,-74,83,-73,83,83,83,83,83,]),'LET':([43,45,48,50,51,52,53,54,55,56,57,58,59,60,61,62,63,82,85,86,92,109,110,120,121,131,135,144,155,164,],[84,84,-72,-77,-78,-79,-80,-81,-82,-83,-84,-85,-86,-87,-88,-89,-90,84,84,84,84,84,-74,84,-73,84,84,84,84,84,]),'IF':([43,45,48,50,51,52,53,54,55,56,57,58,59,60,61,62,63,82,85,86,92,109,110,120,121,131,135,144,155,164,],[85,85,-72,-77,-78,-79,-80,-81,-82,-83,-84,-85,-86,-87,-88,-89,-90,85,85,85,85,85,-74,85,-73,85,85,85,85,85,]),'MATCH':([43,45,48,50,51,52,53,54,55,56,57,58,59,60,61,62,63,82,85,86,92,109,110,120,121,131,135,144,155,164,],[86,86,-72,-77,-78,-79,-80,-81,-82,-83,-84,-85,-86,-87,-88,-89,-90,86,86,86,86,86,-74,86,-73,86,86,86,86,86,]),'IN':([113,133,146,],[131,-16,-15,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'MODULE_DEFINITION':([0,],[1,]),'BODY':([4,],[5,]),'IMPORT_DECLARATIONS':([6,],[7,]),'TOP_DECLARATIONS':([6,32,],[8,71,]),'IMPORT_DECLARATION':([6,32,],[9,72,]),'TOP_DECLARATION':([6,32,34,],[10,10,73,]),'NEW_CONS':([6,32,34,],[13,13,13,]),'DECLARATION':([6,32,34,114,147,],[14,14,14,134,134,]),'GEN_DECLARATION':([6,32,34,114,147,],[17,17,17,17,17,]),'FUNCTION_LHS':([6,22,32,34,114,147,],[18,64,18,18,18,18,]),'LPAT':([6,22,32,34,39,47,114,147,149,163,],[19,65,19,19,76,96,19,19,158,158,]),'FIXITY_DECLARATION':([6,32,34,114,147,],[20,20,20,20,20,]),'APAT':([6,12,16,22,32,34,37,39,41,47,74,83,98,112,114,122,147,149,163,],[21,37,41,21,21,21,74,21,74,21,74,112,122,74,21,74,21,21,21,]),'PARAM':([6,12,16,22,32,34,37,39,41,47,74,83,98,112,114,122,147,149,163,],[27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,]),'LITERAL':([6,12,16,22,32,34,37,39,41,43,45,47,74,82,83,85,86,87,92,98,109,112,114,120,122,131,135,144,147,149,155,163,164,],[28,28,28,28,28,28,28,28,28,91,91,28,28,91,28,91,91,91,91,28,91,28,28,91,28,91,91,91,28,28,91,28,91,]),'RHS':([18,19,],[42,46,]),'GDRHS':([18,19,138,],[44,44,150,]),'VAROP':([19,65,81,102,],[47,47,110,110,]),'VARSYM':([19,65,81,102,],[48,48,48,48,]),'ASSOCIATIVITY':([26,],[67,]),'APATS':([37,41,74,112,122,],[75,78,104,130,139,]),'EXP':([43,45,85,86,92,120,131,135,144,155,164,],[79,95,115,116,118,138,145,148,153,161,167,]),'INFIX_EXP':([43,45,82,85,86,92,109,120,131,135,144,155,164,],[80,80,111,80,80,80,129,80,80,80,80,80,80,]),'LEXP':([43,45,82,85,86,92,109,120,131,135,144,155,164,],[81,81,81,81,81,81,81,81,81,81,81,81,81,]),'FEXP':([43,45,82,85,86,92,109,120,131,135,144,155,164,],[87,87,87,87,87,87,87,87,87,87,87,87,87,]),'AEXP':([43,45,82,85,86,87,92,109,120,131,135,144,155,164,],[88,88,88,88,88,117,88,88,88,88,88,88,88,88,]),'USED_VAR':([43,45,82,85,86,87,92,109,120,131,135,144,155,164,],[89,89,89,89,89,89,89,89,89,89,89,89,89,89,]),'CONSTRUCTORS':([77,],[106,]),'CONSTRUCTOR':([77,127,],[107,143,]),'OP':([81,102,],[109,125,]),'DECLARATIONS':([84,94,108,],[113,119,128,]),'ATYPES':([105,],[126,]),'DECLARATIONS_LIST':([114,147,],[132,154,]),'ATYPE':([126,142,160,],[141,152,152,]),'TYPE':([142,160,],[151,165,]),'ALTS':([149,163,],[156,166,]),'ALT':([149,163,],[157,157,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> MODULE_DEFINITION","S'",1,None,None,None),
  ('MODULE_DEFINITION -> MODULE IDENTIFIER WHERE BODY','MODULE_DEFINITION',4,'p_MODULE_DEFINITION','funky_parser.py',20),
  ('BODY -> OPEN_BRACE IMPORT_DECLARATIONS ENDSTATEMENT TOP_DECLARATIONS CLOSE_BRACE','BODY',5,'p_BODY','funky_parser.py',26),
  ('BODY -> OPEN_BRACE TOP_DECLARATIONS CLOSE_BRACE','BODY',3,'p_BODY','funky_parser.py',27),
  ('IMPORT_DECLARATIONS -> IMPORT_DECLARATIONS ENDSTATEMENT IMPORT_DECLARATION','IMPORT_DECLARATIONS',3,'p_IMPORT_DECLARATIONS','funky_parser.py',39),
  ('IMPORT_DECLARATIONS -> IMPORT_DECLARATION','IMPORT_DECLARATIONS',1,'p_IMPORT_DECLARATIONS','funky_parser.py',40),
  ('IMPORT_DECLARATION -> IMPORT IDENTIFIER','IMPORT_DECLARATION',2,'p_IMPORT_DECLARATION','funky_parser.py',48),
  ('TOP_DECLARATIONS -> TOP_DECLARATIONS ENDSTATEMENT TOP_DECLARATION','TOP_DECLARATIONS',3,'p_TOP_DECLARATIONS','funky_parser.py',53),
  ('TOP_DECLARATIONS -> TOP_DECLARATION','TOP_DECLARATIONS',1,'p_TOP_DECLARATIONS','funky_parser.py',54),
  ('TOP_DECLARATION -> NEW_CONS','TOP_DECLARATION',1,'p_TOP_DECLARATION','funky_parser.py',62),
  ('TOP_DECLARATION -> DECLARATION','TOP_DECLARATION',1,'p_TOP_DECLARATION','funky_parser.py',63),
  ('NEW_CONS -> NEWCONS TYPENAME EQUALS CONSTRUCTORS','NEW_CONS',4,'p_NEW_CONS','funky_parser.py',68),
  ('CONSTRUCTORS -> CONSTRUCTORS PIPE CONSTRUCTOR','CONSTRUCTORS',3,'p_CONSTRUCTORS','funky_parser.py',72),
  ('CONSTRUCTORS -> CONSTRUCTOR','CONSTRUCTORS',1,'p_CONSTRUCTORS','funky_parser.py',73),
  ('CONSTRUCTOR -> TYPENAME ATYPES','CONSTRUCTOR',2,'p_CONSTRUCTOR','funky_parser.py',81),
  ('DECLARATIONS -> OPEN_BRACE DECLARATIONS_LIST CLOSE_BRACE','DECLARATIONS',3,'p_DECLARATIONS','funky_parser.py',85),
  ('DECLARATIONS -> OPEN_BRACE CLOSE_BRACE','DECLARATIONS',2,'p_DECLARATIONS','funky_parser.py',86),
  ('DECLARATIONS_LIST -> DECLARATION ENDSTATEMENT DECLARATIONS_LIST','DECLARATIONS_LIST',3,'p_DECLARATIONS_LIST','funky_parser.py',94),
  ('DECLARATIONS_LIST -> DECLARATION','DECLARATIONS_LIST',1,'p_DECLARATIONS_LIST','funky_parser.py',95),
  ('DECLARATION -> GEN_DECLARATION','DECLARATION',1,'p_DECLARATION','funky_parser.py',103),
  ('DECLARATION -> FUNCTION_LHS RHS','DECLARATION',2,'p_DECLARATION','funky_parser.py',104),
  ('DECLARATION -> LPAT RHS','DECLARATION',2,'p_DECLARATION','funky_parser.py',105),
  ('GEN_DECLARATION -> FIXITY_DECLARATION','GEN_DECLARATION',1,'p_GEN_DECLARATION','funky_parser.py',115),
  ('GEN_DECLARATION -> <empty>','GEN_DECLARATION',0,'p_GEN_DECLARATION','funky_parser.py',116),
  ('FIXITY_DECLARATION -> SETFIX ASSOCIATIVITY INTEGER OP','FIXITY_DECLARATION',4,'p_FIXITY_DECLARATION','funky_parser.py',122),
  ('ASSOCIATIVITY -> LEFTASSOC','ASSOCIATIVITY',1,'p_ASSOCIATIVITY','funky_parser.py',126),
  ('ASSOCIATIVITY -> RIGHTASSOC','ASSOCIATIVITY',1,'p_ASSOCIATIVITY','funky_parser.py',127),
  ('ASSOCIATIVITY -> NONASSOC','ASSOCIATIVITY',1,'p_ASSOCIATIVITY','funky_parser.py',128),
  ('TYPE -> ATYPE','TYPE',1,'p_TYPE','funky_parser.py',133),
  ('TYPE -> ATYPE ARROW TYPE','TYPE',3,'p_TYPE','funky_parser.py',134),
  ('ATYPES -> ATYPES ATYPE','ATYPES',2,'p_ATYPES','funky_parser.py',142),
  ('ATYPES -> <empty>','ATYPES',0,'p_ATYPES','funky_parser.py',143),
  ('ATYPE -> TYPENAME','ATYPE',1,'p_ATYPE','funky_parser.py',151),
  ('ATYPE -> OPEN_PAREN TYPE CLOSE_PAREN','ATYPE',3,'p_ATYPE','funky_parser.py',152),
  ('FUNCTION_LHS -> IDENTIFIER APAT APATS','FUNCTION_LHS',3,'p_FUNCTION_LHS','funky_parser.py',165),
  ('FUNCTION_LHS -> LPAT VAROP LPAT','FUNCTION_LHS',3,'p_FUNCTION_LHS','funky_parser.py',166),
  ('FUNCTION_LHS -> OPEN_PAREN FUNCTION_LHS CLOSE_PAREN APAT APATS','FUNCTION_LHS',5,'p_FUNCTION_LHS','funky_parser.py',167),
  ('RHS -> EQUALS EXP','RHS',2,'p_RHS','funky_parser.py',179),
  ('RHS -> EQUALS EXP WHERE DECLARATIONS','RHS',4,'p_RHS','funky_parser.py',180),
  ('RHS -> GDRHS','RHS',1,'p_RHS','funky_parser.py',181),
  ('RHS -> GDRHS WHERE DECLARATIONS','RHS',3,'p_RHS','funky_parser.py',182),
  ('GDRHS -> PIPE EXP EQUALS EXP','GDRHS',4,'p_GDRHS','funky_parser.py',195),
  ('GDRHS -> PIPE EXP EQUALS EXP GDRHS','GDRHS',5,'p_GDRHS','funky_parser.py',196),
  ('EXP -> INFIX_EXP','EXP',1,'p_EXP','funky_parser.py',204),
  ('INFIX_EXP -> LEXP OP INFIX_EXP','INFIX_EXP',3,'p_INFIX_EXP','funky_parser.py',210),
  ('INFIX_EXP -> MINUS INFIX_EXP','INFIX_EXP',2,'p_INFIX_EXP','funky_parser.py',211),
  ('INFIX_EXP -> LEXP','INFIX_EXP',1,'p_INFIX_EXP','funky_parser.py',212),
  ('LEXP -> LAMBDA APAT APATS ARROW EXP','LEXP',5,'p_LEXP','funky_parser.py',230),
  ('LEXP -> LET DECLARATIONS IN EXP','LEXP',4,'p_LEXP','funky_parser.py',231),
  ('LEXP -> IF EXP THEN EXP ELSE EXP','LEXP',6,'p_LEXP','funky_parser.py',232),
  ('LEXP -> MATCH EXP OF OPEN_BRACE ALTS CLOSE_BRACE','LEXP',6,'p_LEXP','funky_parser.py',233),
  ('LEXP -> FEXP','LEXP',1,'p_LEXP','funky_parser.py',234),
  ('FEXP -> FEXP AEXP','FEXP',2,'p_FEXP','funky_parser.py',249),
  ('FEXP -> AEXP','FEXP',1,'p_FEXP','funky_parser.py',250),
  ('AEXP -> USED_VAR','AEXP',1,'p_AEXP','funky_parser.py',258),
  ('AEXP -> TYPENAME','AEXP',1,'p_AEXP','funky_parser.py',259),
  ('AEXP -> LITERAL','AEXP',1,'p_AEXP','funky_parser.py',260),
  ('AEXP -> OPEN_PAREN EXP CLOSE_PAREN','AEXP',3,'p_AEXP','funky_parser.py',261),
  ('CONSTRUCTION_PARAMS -> CONSTRUCTION_PARAMS AEXP','CONSTRUCTION_PARAMS',2,'p_CONSTRUCTION_PARAMS','funky_parser.py',272),
  ('CONSTRUCTION_PARAMS -> AEXP','CONSTRUCTION_PARAMS',1,'p_CONSTRUCTION_PARAMS','funky_parser.py',273),
  ('ALTS -> ALT ENDSTATEMENT ALTS','ALTS',3,'p_ALTS','funky_parser.py',281),
  ('ALTS -> ALT','ALTS',1,'p_ALTS','funky_parser.py',282),
  ('ALT -> LPAT ARROW EXP','ALT',3,'p_ALT','funky_parser.py',290),
  ('ALT -> <empty>','ALT',0,'p_ALT','funky_parser.py',291),
  ('LPAT -> APAT','LPAT',1,'p_LPAT','funky_parser.py',296),
  ('LPAT -> MINUS OPEN_PAREN INTEGER CLOSE_PAREN','LPAT',4,'p_LPAT','funky_parser.py',297),
  ('LPAT -> MINUS OPEN_PAREN FLOAT CLOSE_PAREN','LPAT',4,'p_LPAT','funky_parser.py',298),
  ('LPAT -> TYPENAME APAT APATS','LPAT',3,'p_LPAT','funky_parser.py',299),
  ('APAT -> PARAM','APAT',1,'p_APAT','funky_parser.py',309),
  ('APAT -> TYPENAME','APAT',1,'p_APAT','funky_parser.py',310),
  ('APAT -> LITERAL','APAT',1,'p_APAT','funky_parser.py',311),
  ('APAT -> OPEN_PAREN LPAT CLOSE_PAREN','APAT',3,'p_APAT','funky_parser.py',312),
  ('VAROP -> VARSYM','VAROP',1,'p_VAROP','funky_parser.py',323),
  ('VAROP -> BACKTICK IDENTIFIER BACKTICK','VAROP',3,'p_VAROP','funky_parser.py',324),
  ('OP -> VAROP','OP',1,'p_OP','funky_parser.py',334),
  ('APATS -> APAT APATS','APATS',2,'p_APATS','funky_parser.py',339),
  ('APATS -> <empty>','APATS',0,'p_APATS','funky_parser.py',340),
  ('VARSYM -> PLUS','VARSYM',1,'p_VARSYM','funky_parser.py',348),
  ('VARSYM -> MINUS','VARSYM',1,'p_VARSYM','funky_parser.py',349),
  ('VARSYM -> TIMES','VARSYM',1,'p_VARSYM','funky_parser.py',350),
  ('VARSYM -> DIVIDE','VARSYM',1,'p_VARSYM','funky_parser.py',351),
  ('VARSYM -> MODULO','VARSYM',1,'p_VARSYM','funky_parser.py',352),
  ('VARSYM -> POW','VARSYM',1,'p_VARSYM','funky_parser.py',353),
  ('VARSYM -> EQUALITY','VARSYM',1,'p_VARSYM','funky_parser.py',354),
  ('VARSYM -> INEQUALITY','VARSYM',1,'p_VARSYM','funky_parser.py',355),
  ('VARSYM -> LESS','VARSYM',1,'p_VARSYM','funky_parser.py',356),
  ('VARSYM -> LEQ','VARSYM',1,'p_VARSYM','funky_parser.py',357),
  ('VARSYM -> GREATER','VARSYM',1,'p_VARSYM','funky_parser.py',358),
  ('VARSYM -> GEQ','VARSYM',1,'p_VARSYM','funky_parser.py',359),
  ('VARSYM -> AND','VARSYM',1,'p_VARSYM','funky_parser.py',360),
  ('VARSYM -> OR','VARSYM',1,'p_VARSYM','funky_parser.py',361),
  ('LITERAL -> FLOAT','LITERAL',1,'p_LITERAL','funky_parser.py',366),
  ('LITERAL -> INTEGER','LITERAL',1,'p_LITERAL','funky_parser.py',367),
  ('LITERAL -> BOOL','LITERAL',1,'p_LITERAL','funky_parser.py',368),
  ('LITERAL -> CHAR','LITERAL',1,'p_LITERAL','funky_parser.py',369),
  ('LITERAL -> STRING','LITERAL',1,'p_LITERAL','funky_parser.py',370),
  ('USED_VAR -> IDENTIFIER','USED_VAR',1,'p_USED_VAR','funky_parser.py',375),
  ('PARAM -> IDENTIFIER','PARAM',1,'p_PARAM','funky_parser.py',379),
]
