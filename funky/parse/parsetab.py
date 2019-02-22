
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'MODULE_DEFINITIONAND ARROW BACKTICK BOOL CHAR CLOSE_BRACE CLOSE_PAREN DIVIDE ELSE ENDSTATEMENT EQUALITY EQUALS FLOAT GEQ GIVEN GREATER IDENTIFIER IF IMPORT IN INEQUALITY INTEGER LAMBDA LEFTASSOC LEQ LESS LET MATCH MINUS MODULE MODULO NEWTYPE NONASSOC OF OPEN_BRACE OPEN_PAREN OR PIPE PLUS POW RIGHTASSOC SETFIX STRING TIMES TYPENAME WHERE WHITESPACEMODULE_DEFINITION : MODULE IDENTIFIER WHERE BODY\n        BODY : OPEN_BRACE IMPORT_DECLARATIONS ENDSTATEMENT TOP_DECLARATIONS CLOSE_BRACE\n                | OPEN_BRACE TOP_DECLARATIONS CLOSE_BRACE\n        IMPORT_DECLARATIONS : IMPORT_DECLARATIONS ENDSTATEMENT IMPORT_DECLARATION\n                               | IMPORT_DECLARATION\n        IMPORT_DECLARATION : IMPORT IDENTIFIER\n        TOP_DECLARATIONS : TOP_DECLARATIONS ENDSTATEMENT TOP_DECLARATION\n                            | TOP_DECLARATION\n        TOP_DECLARATION : TYPE_DECLARATION\n                           | DECLARATION\n        TYPE_DECLARATION : NEWTYPE TYPENAME TYVARS EQUALS CONSTRUCTORSTYVARS : TYVARS IDENTIFIER\n                  |\n        CONSTRUCTORS : CONSTRUCTORS PIPE CONSTRUCTOR\n                        | CONSTRUCTOR\n        CONSTRUCTOR : TYPENAME ATYPESDECLARATIONS : OPEN_BRACE DECLARATIONS_LIST CLOSE_BRACE\n                        | OPEN_BRACE CLOSE_BRACE\n        DECLARATIONS_LIST : DECLARATION ENDSTATEMENT DECLARATIONS_LIST\n                             | DECLARATION\n        DECLARATION : GEN_DECLARATION\n                       | FUNCTION_LHS RHS\n                       | LPAT RHS\n        GEN_DECLARATION : FIXITY_DECLARATION\n                           |\n        FIXITY_DECLARATION : SETFIX ASSOCIATIVITY INTEGER OPASSOCIATIVITY : LEFTASSOC\n                         | RIGHTASSOC\n                         | NONASSOC\n        TYPE : ATYPE\n                | ATYPE ARROW TYPE\n        ATYPES : ATYPES ATYPE\n                  |\n        ATYPE : TYPENAME\n                 | IDENTIFIER\n                 | OPEN_PAREN TYPE CLOSE_PAREN\n        FUNCTION_LHS : IDENTIFIER APAT APATS\n                        | LPAT VAROP LPAT\n                        | OPEN_PAREN FUNCTION_LHS CLOSE_PAREN APAT APATS\n        RHS : EQUALS EXP\n               | EQUALS EXP WHERE DECLARATIONS\n               | GDRHS\n               | GDRHS WHERE DECLARATIONS\n        GDRHS : GIVEN EXP EQUALS EXP\n                 | GIVEN EXP EQUALS EXP GDRHS\n        EXP : INFIX_EXP\n        INFIX_EXP : LEXP OP INFIX_EXP\n                     | MINUS INFIX_EXP\n                     | LEXP\n        LEXP : LAMBDA APAT APATS ARROW EXP\n                | LET DECLARATIONS IN EXP\n                | EXP IF EXP ELSE EXP\n                | MATCH EXP OF OPEN_BRACE ALTS CLOSE_BRACE\n                | FEXP\n        FEXP : FEXP AEXP\n                | AEXP\n        AEXP : USED_VAR\n                | USED_TYPENAME\n                | LITERAL\n                | OPERATOR_FUNC\n                | OPEN_PAREN EXP CLOSE_PAREN\n        OPERATOR_FUNC : OPEN_PAREN OP CLOSE_PARENCONSTRUCTION_PARAMS : CONSTRUCTION_PARAMS AEXP\n                               | AEXP\n        ALTS : ALT ENDSTATEMENT ALTS\n                | ALT\n        ALT : LPAT ARROW EXP\n               |\n        LPAT : APAT\n                | MINUS OPEN_PAREN INTEGER CLOSE_PAREN\n                | MINUS OPEN_PAREN FLOAT CLOSE_PAREN\n                | TYPENAME APAT APATS\n        APAT : PARAM\n                | TYPENAME\n                | LITERAL\n                | OPEN_PAREN LPAT CLOSE_PAREN\n        VAROP : VARSYM\n                 | BACKTICK IDENTIFIER BACKTICK\n        OP : VAROP\n        APATS : APAT APATS\n                 |\n        VARSYM : PLUS\n                  | MINUS\n                  | TIMES\n                  | DIVIDE\n                  | MODULO\n                  | POW\n                  | EQUALITY\n                  | INEQUALITY\n                  | LESS\n                  | LEQ\n                  | GREATER\n                  | GEQ\n                  | AND\n                  | OR\n        LITERAL : FLOAT\n                   | INTEGER\n                   | BOOL\n                   | CHAR\n                   | STRING\n        USED_VAR : IDENTIFIERUSED_TYPENAME : TYPENAMEPARAM : IDENTIFIER'
    
_lr_action_items = {'MODULE':([0,],[2,]),'$end':([1,5,33,104,],[0,-1,-3,-2,]),'IDENTIFIER':([2,6,11,12,16,22,24,25,27,28,29,30,31,32,34,36,37,38,39,40,41,43,45,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,74,77,82,83,85,86,87,88,89,90,91,92,93,94,99,100,107,109,110,111,114,116,118,121,123,124,125,129,136,141,142,145,147,148,151,152,154,155,156,157,168,169,170,171,],[3,12,35,36,36,12,-97,-96,-73,-75,-98,-99,-100,12,12,-103,36,-74,36,-13,36,93,93,36,-77,98,-82,-83,-84,-85,-86,-87,-88,-89,-90,-91,-92,-93,-94,-95,36,107,93,36,93,93,-56,-57,-58,-59,-60,93,-101,-102,36,-76,-12,93,93,-79,36,12,-55,93,93,-78,36,-33,93,-61,-62,156,93,93,12,36,-34,-32,-35,156,36,93,-36,156,]),'WHERE':([3,24,25,29,30,31,44,79,80,81,86,87,88,89,90,91,93,94,112,118,134,141,142,143,149,153,159,160,167,],[4,-97,-96,-98,-99,-100,95,108,-46,-49,-54,-56,-57,-58,-59,-60,-101,-102,-48,-55,-47,-61,-62,-44,-51,-45,-52,-50,-53,]),'OPEN_BRACE':([4,84,95,108,140,],[6,116,116,116,152,]),'IMPORT':([6,32,],[11,11,]),'NEWTYPE':([6,32,34,],[15,15,15,]),'CLOSE_BRACE':([6,8,10,13,14,17,20,24,25,29,30,31,32,34,42,44,46,48,50,51,52,53,54,55,56,57,58,59,60,61,62,63,71,73,79,80,81,86,87,88,89,90,91,93,94,111,112,116,118,122,124,128,129,130,131,132,134,137,138,139,141,142,143,145,149,150,151,152,153,154,155,156,158,159,160,161,162,163,167,168,170,172,173,],[-25,33,-8,-9,-10,-21,-24,-97,-96,-98,-99,-100,-25,-25,-22,-42,-23,-77,-82,-83,-84,-85,-86,-87,-88,-89,-90,-91,-92,-93,-94,-95,104,-7,-40,-46,-49,-54,-56,-57,-58,-59,-60,-101,-102,-79,-48,138,-55,-43,-78,-26,-33,-11,-15,-41,-47,150,-18,-20,-61,-62,-44,-16,-51,-17,-25,-68,-45,-34,-32,-35,-14,-52,-50,-19,167,-66,-53,-68,-36,-65,-67,]),'ENDSTATEMENT':([6,7,8,9,10,13,14,17,20,24,25,29,30,31,32,34,35,42,44,46,48,50,51,52,53,54,55,56,57,58,59,60,61,62,63,71,72,73,79,80,81,86,87,88,89,90,91,93,94,111,112,116,118,122,124,128,129,130,131,132,134,138,139,141,142,143,145,149,150,151,152,153,154,155,156,158,159,160,163,167,168,170,173,],[-25,32,34,-5,-8,-9,-10,-21,-24,-97,-96,-98,-99,-100,-25,-25,-6,-22,-42,-23,-77,-82,-83,-84,-85,-86,-87,-88,-89,-90,-91,-92,-93,-94,-95,34,-4,-7,-40,-46,-49,-54,-56,-57,-58,-59,-60,-101,-102,-79,-48,-25,-55,-43,-78,-26,-33,-11,-15,-41,-47,-18,151,-61,-62,-44,-16,-51,-17,-25,-68,-45,-34,-32,-35,-14,-52,-50,168,-53,-68,-36,-67,]),'OPEN_PAREN':([6,12,16,22,23,24,25,27,28,29,30,31,32,34,36,37,38,39,41,43,45,47,48,50,51,52,53,54,55,56,57,58,59,60,61,62,63,74,82,83,85,86,87,88,89,90,91,92,93,94,99,100,109,110,111,114,116,118,121,123,124,125,129,136,141,142,145,147,148,151,152,154,155,156,157,168,169,170,171,],[22,39,39,22,66,-97,-96,-73,-75,-98,-99,-100,22,22,-103,39,-74,39,39,92,92,39,-77,-82,-83,-84,-85,-86,-87,-88,-89,-90,-91,-92,-93,-94,-95,39,92,39,92,92,-56,-57,-58,-59,-60,92,-101,-102,39,-76,92,92,-79,39,22,-55,92,92,-78,39,-33,92,-61,-62,157,92,92,22,39,-34,-32,-35,157,39,92,-36,157,]),'MINUS':([6,12,16,19,21,22,24,25,27,28,29,30,31,32,34,36,38,39,41,43,45,47,48,50,51,52,53,54,55,56,57,58,59,60,61,62,63,65,74,78,80,81,82,85,86,87,88,89,90,91,92,93,94,100,103,105,109,110,111,112,116,118,121,123,124,126,127,134,136,141,142,147,148,149,151,152,159,160,167,168,169,],[23,-103,-74,51,-69,23,-97,-96,-73,-75,-98,-99,-100,23,23,-103,-74,23,-81,82,82,23,-77,-82,-83,-84,-85,-86,-87,-88,-89,-90,-91,-92,-93,-94,-95,51,-81,-72,-46,51,82,82,-54,-56,-57,-58,-59,-60,121,-101,-102,-76,51,-80,82,82,-79,-48,23,-55,82,82,-78,-70,-71,-47,82,-61,-62,82,82,-51,23,23,-52,-50,-53,23,82,]),'TYPENAME':([6,12,15,16,22,24,25,27,28,29,30,31,32,34,36,37,38,39,41,43,45,47,48,50,51,52,53,54,55,56,57,58,59,60,61,62,63,74,82,83,85,86,87,88,89,90,91,92,93,94,99,100,106,109,110,111,114,116,118,121,123,124,125,129,136,141,142,145,146,147,148,151,152,154,155,156,157,168,169,170,171,],[16,38,40,38,16,-97,-96,-73,-75,-98,-99,-100,16,16,-103,38,-74,16,38,94,94,16,-77,-82,-83,-84,-85,-86,-87,-88,-89,-90,-91,-92,-93,-94,-95,38,94,38,94,94,-56,-57,-58,-59,-60,94,-101,-102,38,-76,129,94,94,-79,38,16,-55,94,94,-78,38,-33,94,-61,-62,154,129,94,94,16,16,-34,-32,-35,154,16,94,-36,154,]),'SETFIX':([6,32,34,116,151,],[26,26,26,26,26,]),'FLOAT':([6,12,16,22,24,25,27,28,29,30,31,32,34,36,37,38,39,41,43,45,47,48,50,51,52,53,54,55,56,57,58,59,60,61,62,63,66,74,82,83,85,86,87,88,89,90,91,92,93,94,99,100,109,110,111,114,116,118,121,123,124,125,136,141,142,147,148,151,152,168,169,],[25,25,25,25,-97,-96,-73,-75,-98,-99,-100,25,25,-103,25,-74,25,25,25,25,25,-77,-82,-83,-84,-85,-86,-87,-88,-89,-90,-91,-92,-93,-94,-95,102,25,25,25,25,25,-56,-57,-58,-59,-60,25,-101,-102,25,-76,25,25,-79,25,25,-55,25,25,-78,25,25,-61,-62,25,25,25,25,25,25,]),'INTEGER':([6,12,16,22,24,25,27,28,29,30,31,32,34,36,37,38,39,41,43,45,47,48,50,51,52,53,54,55,56,57,58,59,60,61,62,63,66,67,68,69,70,74,82,83,85,86,87,88,89,90,91,92,93,94,99,100,109,110,111,114,116,118,121,123,124,125,136,141,142,147,148,151,152,168,169,],[24,24,24,24,-97,-96,-73,-75,-98,-99,-100,24,24,-103,24,-74,24,24,24,24,24,-77,-82,-83,-84,-85,-86,-87,-88,-89,-90,-91,-92,-93,-94,-95,101,103,-27,-28,-29,24,24,24,24,24,-56,-57,-58,-59,-60,24,-101,-102,24,-76,24,24,-79,24,24,-55,24,24,-78,24,24,-61,-62,24,24,24,24,24,24,]),'BOOL':([6,12,16,22,24,25,27,28,29,30,31,32,34,36,37,38,39,41,43,45,47,48,50,51,52,53,54,55,56,57,58,59,60,61,62,63,74,82,83,85,86,87,88,89,90,91,92,93,94,99,100,109,110,111,114,116,118,121,123,124,125,136,141,142,147,148,151,152,168,169,],[29,29,29,29,-97,-96,-73,-75,-98,-99,-100,29,29,-103,29,-74,29,29,29,29,29,-77,-82,-83,-84,-85,-86,-87,-88,-89,-90,-91,-92,-93,-94,-95,29,29,29,29,29,-56,-57,-58,-59,-60,29,-101,-102,29,-76,29,29,-79,29,29,-55,29,29,-78,29,29,-61,-62,29,29,29,29,29,29,]),'CHAR':([6,12,16,22,24,25,27,28,29,30,31,32,34,36,37,38,39,41,43,45,47,48,50,51,52,53,54,55,56,57,58,59,60,61,62,63,74,82,83,85,86,87,88,89,90,91,92,93,94,99,100,109,110,111,114,116,118,121,123,124,125,136,141,142,147,148,151,152,168,169,],[30,30,30,30,-97,-96,-73,-75,-98,-99,-100,30,30,-103,30,-74,30,30,30,30,30,-77,-82,-83,-84,-85,-86,-87,-88,-89,-90,-91,-92,-93,-94,-95,30,30,30,30,30,-56,-57,-58,-59,-60,30,-101,-102,30,-76,30,30,-79,30,30,-55,30,30,-78,30,30,-61,-62,30,30,30,30,30,30,]),'STRING':([6,12,16,22,24,25,27,28,29,30,31,32,34,36,37,38,39,41,43,45,47,48,50,51,52,53,54,55,56,57,58,59,60,61,62,63,74,82,83,85,86,87,88,89,90,91,92,93,94,99,100,109,110,111,114,116,118,121,123,124,125,136,141,142,147,148,151,152,168,169,],[31,31,31,31,-97,-96,-73,-75,-98,-99,-100,31,31,-103,31,-74,31,31,31,31,31,-77,-82,-83,-84,-85,-86,-87,-88,-89,-90,-91,-92,-93,-94,-95,31,31,31,31,31,-56,-57,-58,-59,-60,31,-101,-102,31,-76,31,31,-79,31,31,-55,31,31,-78,31,31,-61,-62,31,31,31,31,31,31,]),'EQUALS':([12,16,18,19,21,24,25,27,28,29,30,31,36,37,38,40,41,74,75,77,78,80,81,86,87,88,89,90,91,93,94,96,97,100,105,107,112,118,125,126,127,134,141,142,144,149,159,160,167,],[-103,-74,43,43,-69,-97,-96,-73,-75,-98,-99,-100,-103,-81,-74,-13,-81,-81,-37,106,-72,-46,-49,-54,-56,-57,-58,-59,-60,-101,-102,123,-38,-76,-80,-12,-48,-55,-81,-70,-71,-47,-61,-62,-39,-51,-52,-50,-53,]),'BACKTICK':([12,16,19,21,24,25,27,28,29,30,31,36,38,41,65,74,78,80,81,86,87,88,89,90,91,92,93,94,98,100,103,105,112,118,126,127,134,141,142,149,159,160,167,],[-103,-74,49,-69,-97,-96,-73,-75,-98,-99,-100,-103,-74,-81,49,-81,-72,-46,49,-54,-56,-57,-58,-59,-60,49,-101,-102,124,-76,49,-80,-48,-55,-70,-71,-47,-61,-62,-51,-52,-50,-53,]),'GIVEN':([12,16,18,19,21,24,25,27,28,29,30,31,36,37,38,41,74,75,78,80,81,86,87,88,89,90,91,93,94,97,100,105,112,118,125,126,127,134,141,142,143,144,149,159,160,167,],[-103,-74,45,45,-69,-97,-96,-73,-75,-98,-99,-100,-103,-81,-74,-81,-81,-37,-72,-46,-49,-54,-56,-57,-58,-59,-60,-101,-102,-38,-76,-80,-48,-55,-81,-70,-71,-47,-61,-62,45,-39,-51,-52,-50,-53,]),'PLUS':([12,16,19,21,24,25,27,28,29,30,31,36,38,41,65,74,78,80,81,86,87,88,89,90,91,92,93,94,100,103,105,112,118,126,127,134,141,142,149,159,160,167,],[-103,-74,50,-69,-97,-96,-73,-75,-98,-99,-100,-103,-74,-81,50,-81,-72,-46,50,-54,-56,-57,-58,-59,-60,50,-101,-102,-76,50,-80,-48,-55,-70,-71,-47,-61,-62,-51,-52,-50,-53,]),'TIMES':([12,16,19,21,24,25,27,28,29,30,31,36,38,41,65,74,78,80,81,86,87,88,89,90,91,92,93,94,100,103,105,112,118,126,127,134,141,142,149,159,160,167,],[-103,-74,52,-69,-97,-96,-73,-75,-98,-99,-100,-103,-74,-81,52,-81,-72,-46,52,-54,-56,-57,-58,-59,-60,52,-101,-102,-76,52,-80,-48,-55,-70,-71,-47,-61,-62,-51,-52,-50,-53,]),'DIVIDE':([12,16,19,21,24,25,27,28,29,30,31,36,38,41,65,74,78,80,81,86,87,88,89,90,91,92,93,94,100,103,105,112,118,126,127,134,141,142,149,159,160,167,],[-103,-74,53,-69,-97,-96,-73,-75,-98,-99,-100,-103,-74,-81,53,-81,-72,-46,53,-54,-56,-57,-58,-59,-60,53,-101,-102,-76,53,-80,-48,-55,-70,-71,-47,-61,-62,-51,-52,-50,-53,]),'MODULO':([12,16,19,21,24,25,27,28,29,30,31,36,38,41,65,74,78,80,81,86,87,88,89,90,91,92,93,94,100,103,105,112,118,126,127,134,141,142,149,159,160,167,],[-103,-74,54,-69,-97,-96,-73,-75,-98,-99,-100,-103,-74,-81,54,-81,-72,-46,54,-54,-56,-57,-58,-59,-60,54,-101,-102,-76,54,-80,-48,-55,-70,-71,-47,-61,-62,-51,-52,-50,-53,]),'POW':([12,16,19,21,24,25,27,28,29,30,31,36,38,41,65,74,78,80,81,86,87,88,89,90,91,92,93,94,100,103,105,112,118,126,127,134,141,142,149,159,160,167,],[-103,-74,55,-69,-97,-96,-73,-75,-98,-99,-100,-103,-74,-81,55,-81,-72,-46,55,-54,-56,-57,-58,-59,-60,55,-101,-102,-76,55,-80,-48,-55,-70,-71,-47,-61,-62,-51,-52,-50,-53,]),'EQUALITY':([12,16,19,21,24,25,27,28,29,30,31,36,38,41,65,74,78,80,81,86,87,88,89,90,91,92,93,94,100,103,105,112,118,126,127,134,141,142,149,159,160,167,],[-103,-74,56,-69,-97,-96,-73,-75,-98,-99,-100,-103,-74,-81,56,-81,-72,-46,56,-54,-56,-57,-58,-59,-60,56,-101,-102,-76,56,-80,-48,-55,-70,-71,-47,-61,-62,-51,-52,-50,-53,]),'INEQUALITY':([12,16,19,21,24,25,27,28,29,30,31,36,38,41,65,74,78,80,81,86,87,88,89,90,91,92,93,94,100,103,105,112,118,126,127,134,141,142,149,159,160,167,],[-103,-74,57,-69,-97,-96,-73,-75,-98,-99,-100,-103,-74,-81,57,-81,-72,-46,57,-54,-56,-57,-58,-59,-60,57,-101,-102,-76,57,-80,-48,-55,-70,-71,-47,-61,-62,-51,-52,-50,-53,]),'LESS':([12,16,19,21,24,25,27,28,29,30,31,36,38,41,65,74,78,80,81,86,87,88,89,90,91,92,93,94,100,103,105,112,118,126,127,134,141,142,149,159,160,167,],[-103,-74,58,-69,-97,-96,-73,-75,-98,-99,-100,-103,-74,-81,58,-81,-72,-46,58,-54,-56,-57,-58,-59,-60,58,-101,-102,-76,58,-80,-48,-55,-70,-71,-47,-61,-62,-51,-52,-50,-53,]),'LEQ':([12,16,19,21,24,25,27,28,29,30,31,36,38,41,65,74,78,80,81,86,87,88,89,90,91,92,93,94,100,103,105,112,118,126,127,134,141,142,149,159,160,167,],[-103,-74,59,-69,-97,-96,-73,-75,-98,-99,-100,-103,-74,-81,59,-81,-72,-46,59,-54,-56,-57,-58,-59,-60,59,-101,-102,-76,59,-80,-48,-55,-70,-71,-47,-61,-62,-51,-52,-50,-53,]),'GREATER':([12,16,19,21,24,25,27,28,29,30,31,36,38,41,65,74,78,80,81,86,87,88,89,90,91,92,93,94,100,103,105,112,118,126,127,134,141,142,149,159,160,167,],[-103,-74,60,-69,-97,-96,-73,-75,-98,-99,-100,-103,-74,-81,60,-81,-72,-46,60,-54,-56,-57,-58,-59,-60,60,-101,-102,-76,60,-80,-48,-55,-70,-71,-47,-61,-62,-51,-52,-50,-53,]),'GEQ':([12,16,19,21,24,25,27,28,29,30,31,36,38,41,65,74,78,80,81,86,87,88,89,90,91,92,93,94,100,103,105,112,118,126,127,134,141,142,149,159,160,167,],[-103,-74,61,-69,-97,-96,-73,-75,-98,-99,-100,-103,-74,-81,61,-81,-72,-46,61,-54,-56,-57,-58,-59,-60,61,-101,-102,-76,61,-80,-48,-55,-70,-71,-47,-61,-62,-51,-52,-50,-53,]),'AND':([12,16,19,21,24,25,27,28,29,30,31,36,38,41,65,74,78,80,81,86,87,88,89,90,91,92,93,94,100,103,105,112,118,126,127,134,141,142,149,159,160,167,],[-103,-74,62,-69,-97,-96,-73,-75,-98,-99,-100,-103,-74,-81,62,-81,-72,-46,62,-54,-56,-57,-58,-59,-60,62,-101,-102,-76,62,-80,-48,-55,-70,-71,-47,-61,-62,-51,-52,-50,-53,]),'OR':([12,16,19,21,24,25,27,28,29,30,31,36,38,41,65,74,78,80,81,86,87,88,89,90,91,92,93,94,100,103,105,112,118,126,127,134,141,142,149,159,160,167,],[-103,-74,63,-69,-97,-96,-73,-75,-98,-99,-100,-103,-74,-81,63,-81,-72,-46,63,-54,-56,-57,-58,-59,-60,63,-101,-102,-76,63,-80,-48,-55,-70,-71,-47,-61,-62,-51,-52,-50,-53,]),'CLOSE_PAREN':([12,16,21,24,25,27,28,29,30,31,36,37,38,41,48,50,52,53,54,55,56,57,58,59,60,61,62,63,64,65,74,75,76,78,80,81,86,87,88,89,90,91,93,94,97,100,101,102,105,111,112,118,119,120,121,124,125,126,127,134,141,142,144,149,154,156,159,160,165,166,167,170,174,],[-103,-74,-69,-97,-96,-73,-75,-98,-99,-100,-103,-81,-74,-81,-77,-82,-84,-85,-86,-87,-88,-89,-90,-91,-92,-93,-94,-95,99,100,-81,-37,100,-72,-46,-49,-54,-56,-57,-58,-59,-60,-101,-102,-38,-76,126,127,-80,-79,-48,-55,141,142,-83,-78,-81,-70,-71,-47,-61,-62,-39,-51,-34,-35,-52,-50,170,-30,-53,-36,-31,]),'ARROW':([16,21,24,25,27,28,29,30,31,36,38,41,74,78,100,105,114,126,127,135,154,156,164,166,170,],[-74,-69,-97,-96,-73,-75,-98,-99,-100,-103,-74,-81,-81,-72,-76,-80,-81,-70,-71,148,-34,-35,169,171,-36,]),'IF':([24,25,29,30,31,79,80,81,86,87,88,89,90,91,93,94,96,112,113,117,118,119,133,134,141,142,143,149,159,160,167,173,],[-97,-96,-98,-99,-100,109,-46,-49,-54,-56,-57,-58,-59,-60,-101,-102,109,-46,109,109,-55,109,109,-46,-61,-62,109,109,109,109,-53,109,]),'OF':([24,25,29,30,31,80,81,86,87,88,89,90,91,93,94,112,117,118,134,141,142,149,159,160,167,],[-97,-96,-98,-99,-100,-46,-49,-54,-56,-57,-58,-59,-60,-101,-102,-48,140,-55,-47,-61,-62,-51,-52,-50,-53,]),'ELSE':([24,25,29,30,31,80,81,86,87,88,89,90,91,93,94,112,118,133,134,141,142,149,159,160,167,],[-97,-96,-98,-99,-100,-46,-49,-54,-56,-57,-58,-59,-60,-101,-102,-48,-55,147,-47,-61,-62,-51,-52,-50,-53,]),'LEFTASSOC':([26,],[68,]),'RIGHTASSOC':([26,],[69,]),'NONASSOC':([26,],[70,]),'LAMBDA':([43,45,48,50,51,52,53,54,55,56,57,58,59,60,61,62,63,82,85,92,109,110,111,121,123,124,136,147,148,169,],[83,83,-77,-82,-83,-84,-85,-86,-87,-88,-89,-90,-91,-92,-93,-94,-95,83,83,83,83,83,-79,83,83,-78,83,83,83,83,]),'LET':([43,45,48,50,51,52,53,54,55,56,57,58,59,60,61,62,63,82,85,92,109,110,111,121,123,124,136,147,148,169,],[84,84,-77,-82,-83,-84,-85,-86,-87,-88,-89,-90,-91,-92,-93,-94,-95,84,84,84,84,84,-79,84,84,-78,84,84,84,84,]),'MATCH':([43,45,48,50,51,52,53,54,55,56,57,58,59,60,61,62,63,82,85,92,109,110,111,121,123,124,136,147,148,169,],[85,85,-77,-82,-83,-84,-85,-86,-87,-88,-89,-90,-91,-92,-93,-94,-95,85,85,85,85,85,-79,85,85,-78,85,85,85,85,]),'IN':([115,138,150,],[136,-18,-17,]),'PIPE':([129,130,131,145,154,155,156,158,170,],[-33,146,-15,-16,-34,-32,-35,-14,-36,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'MODULE_DEFINITION':([0,],[1,]),'BODY':([4,],[5,]),'IMPORT_DECLARATIONS':([6,],[7,]),'TOP_DECLARATIONS':([6,32,],[8,71,]),'IMPORT_DECLARATION':([6,32,],[9,72,]),'TOP_DECLARATION':([6,32,34,],[10,10,73,]),'TYPE_DECLARATION':([6,32,34,],[13,13,13,]),'DECLARATION':([6,32,34,116,151,],[14,14,14,139,139,]),'GEN_DECLARATION':([6,32,34,116,151,],[17,17,17,17,17,]),'FUNCTION_LHS':([6,22,32,34,116,151,],[18,64,18,18,18,18,]),'LPAT':([6,22,32,34,39,47,116,151,152,168,],[19,65,19,19,76,97,19,19,164,164,]),'FIXITY_DECLARATION':([6,32,34,116,151,],[20,20,20,20,20,]),'APAT':([6,12,16,22,32,34,37,39,41,47,74,83,99,114,116,125,151,152,168,],[21,37,41,21,21,21,74,21,74,21,74,114,125,74,21,74,21,21,21,]),'PARAM':([6,12,16,22,32,34,37,39,41,47,74,83,99,114,116,125,151,152,168,],[27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,]),'LITERAL':([6,12,16,22,32,34,37,39,41,43,45,47,74,82,83,85,86,92,99,109,110,114,116,121,123,125,136,147,148,151,152,168,169,],[28,28,28,28,28,28,28,28,28,90,90,28,28,90,28,90,90,90,28,90,90,28,28,90,90,28,90,90,90,28,28,28,90,]),'RHS':([18,19,],[42,46,]),'GDRHS':([18,19,143,],[44,44,153,]),'VAROP':([19,65,81,92,103,],[47,47,111,111,111,]),'VARSYM':([19,65,81,92,103,],[48,48,48,48,48,]),'ASSOCIATIVITY':([26,],[67,]),'APATS':([37,41,74,114,125,],[75,78,105,135,144,]),'TYVARS':([40,],[77,]),'EXP':([43,45,82,85,92,109,110,121,123,136,147,148,169,],[79,96,113,117,119,133,113,113,143,149,159,160,173,]),'INFIX_EXP':([43,45,82,85,92,109,110,121,123,136,147,148,169,],[80,80,112,80,80,80,134,112,80,80,80,80,80,]),'LEXP':([43,45,82,85,92,109,110,121,123,136,147,148,169,],[81,81,81,81,81,81,81,81,81,81,81,81,81,]),'FEXP':([43,45,82,85,92,109,110,121,123,136,147,148,169,],[86,86,86,86,86,86,86,86,86,86,86,86,86,]),'AEXP':([43,45,82,85,86,92,109,110,121,123,136,147,148,169,],[87,87,87,87,118,87,87,87,87,87,87,87,87,87,]),'USED_VAR':([43,45,82,85,86,92,109,110,121,123,136,147,148,169,],[88,88,88,88,88,88,88,88,88,88,88,88,88,88,]),'USED_TYPENAME':([43,45,82,85,86,92,109,110,121,123,136,147,148,169,],[89,89,89,89,89,89,89,89,89,89,89,89,89,89,]),'OPERATOR_FUNC':([43,45,82,85,86,92,109,110,121,123,136,147,148,169,],[91,91,91,91,91,91,91,91,91,91,91,91,91,91,]),'OP':([81,92,103,],[110,120,128,]),'DECLARATIONS':([84,95,108,],[115,122,132,]),'CONSTRUCTORS':([106,],[130,]),'CONSTRUCTOR':([106,146,],[131,158,]),'DECLARATIONS_LIST':([116,151,],[137,161,]),'ATYPES':([129,],[145,]),'ATYPE':([145,157,171,],[155,166,166,]),'ALTS':([152,168,],[162,172,]),'ALT':([152,168,],[163,163,]),'TYPE':([157,171,],[165,174,]),}

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
  ('TOP_DECLARATION -> TYPE_DECLARATION','TOP_DECLARATION',1,'p_TOP_DECLARATION','funky_parser.py',62),
  ('TOP_DECLARATION -> DECLARATION','TOP_DECLARATION',1,'p_TOP_DECLARATION','funky_parser.py',63),
  ('TYPE_DECLARATION -> NEWTYPE TYPENAME TYVARS EQUALS CONSTRUCTORS','TYPE_DECLARATION',5,'p_TYPE_DECLARATION','funky_parser.py',68),
  ('TYVARS -> TYVARS IDENTIFIER','TYVARS',2,'p_TYVARS','funky_parser.py',72),
  ('TYVARS -> <empty>','TYVARS',0,'p_TYVARS','funky_parser.py',73),
  ('CONSTRUCTORS -> CONSTRUCTORS PIPE CONSTRUCTOR','CONSTRUCTORS',3,'p_CONSTRUCTORS','funky_parser.py',81),
  ('CONSTRUCTORS -> CONSTRUCTOR','CONSTRUCTORS',1,'p_CONSTRUCTORS','funky_parser.py',82),
  ('CONSTRUCTOR -> TYPENAME ATYPES','CONSTRUCTOR',2,'p_CONSTRUCTOR','funky_parser.py',90),
  ('DECLARATIONS -> OPEN_BRACE DECLARATIONS_LIST CLOSE_BRACE','DECLARATIONS',3,'p_DECLARATIONS','funky_parser.py',94),
  ('DECLARATIONS -> OPEN_BRACE CLOSE_BRACE','DECLARATIONS',2,'p_DECLARATIONS','funky_parser.py',95),
  ('DECLARATIONS_LIST -> DECLARATION ENDSTATEMENT DECLARATIONS_LIST','DECLARATIONS_LIST',3,'p_DECLARATIONS_LIST','funky_parser.py',103),
  ('DECLARATIONS_LIST -> DECLARATION','DECLARATIONS_LIST',1,'p_DECLARATIONS_LIST','funky_parser.py',104),
  ('DECLARATION -> GEN_DECLARATION','DECLARATION',1,'p_DECLARATION','funky_parser.py',112),
  ('DECLARATION -> FUNCTION_LHS RHS','DECLARATION',2,'p_DECLARATION','funky_parser.py',113),
  ('DECLARATION -> LPAT RHS','DECLARATION',2,'p_DECLARATION','funky_parser.py',114),
  ('GEN_DECLARATION -> FIXITY_DECLARATION','GEN_DECLARATION',1,'p_GEN_DECLARATION','funky_parser.py',124),
  ('GEN_DECLARATION -> <empty>','GEN_DECLARATION',0,'p_GEN_DECLARATION','funky_parser.py',125),
  ('FIXITY_DECLARATION -> SETFIX ASSOCIATIVITY INTEGER OP','FIXITY_DECLARATION',4,'p_FIXITY_DECLARATION','funky_parser.py',131),
  ('ASSOCIATIVITY -> LEFTASSOC','ASSOCIATIVITY',1,'p_ASSOCIATIVITY','funky_parser.py',135),
  ('ASSOCIATIVITY -> RIGHTASSOC','ASSOCIATIVITY',1,'p_ASSOCIATIVITY','funky_parser.py',136),
  ('ASSOCIATIVITY -> NONASSOC','ASSOCIATIVITY',1,'p_ASSOCIATIVITY','funky_parser.py',137),
  ('TYPE -> ATYPE','TYPE',1,'p_TYPE','funky_parser.py',142),
  ('TYPE -> ATYPE ARROW TYPE','TYPE',3,'p_TYPE','funky_parser.py',143),
  ('ATYPES -> ATYPES ATYPE','ATYPES',2,'p_ATYPES','funky_parser.py',151),
  ('ATYPES -> <empty>','ATYPES',0,'p_ATYPES','funky_parser.py',152),
  ('ATYPE -> TYPENAME','ATYPE',1,'p_ATYPE','funky_parser.py',160),
  ('ATYPE -> IDENTIFIER','ATYPE',1,'p_ATYPE','funky_parser.py',161),
  ('ATYPE -> OPEN_PAREN TYPE CLOSE_PAREN','ATYPE',3,'p_ATYPE','funky_parser.py',162),
  ('FUNCTION_LHS -> IDENTIFIER APAT APATS','FUNCTION_LHS',3,'p_FUNCTION_LHS','funky_parser.py',170),
  ('FUNCTION_LHS -> LPAT VAROP LPAT','FUNCTION_LHS',3,'p_FUNCTION_LHS','funky_parser.py',171),
  ('FUNCTION_LHS -> OPEN_PAREN FUNCTION_LHS CLOSE_PAREN APAT APATS','FUNCTION_LHS',5,'p_FUNCTION_LHS','funky_parser.py',172),
  ('RHS -> EQUALS EXP','RHS',2,'p_RHS','funky_parser.py',184),
  ('RHS -> EQUALS EXP WHERE DECLARATIONS','RHS',4,'p_RHS','funky_parser.py',185),
  ('RHS -> GDRHS','RHS',1,'p_RHS','funky_parser.py',186),
  ('RHS -> GDRHS WHERE DECLARATIONS','RHS',3,'p_RHS','funky_parser.py',187),
  ('GDRHS -> GIVEN EXP EQUALS EXP','GDRHS',4,'p_GDRHS','funky_parser.py',200),
  ('GDRHS -> GIVEN EXP EQUALS EXP GDRHS','GDRHS',5,'p_GDRHS','funky_parser.py',201),
  ('EXP -> INFIX_EXP','EXP',1,'p_EXP','funky_parser.py',209),
  ('INFIX_EXP -> LEXP OP INFIX_EXP','INFIX_EXP',3,'p_INFIX_EXP','funky_parser.py',215),
  ('INFIX_EXP -> MINUS INFIX_EXP','INFIX_EXP',2,'p_INFIX_EXP','funky_parser.py',216),
  ('INFIX_EXP -> LEXP','INFIX_EXP',1,'p_INFIX_EXP','funky_parser.py',217),
  ('LEXP -> LAMBDA APAT APATS ARROW EXP','LEXP',5,'p_LEXP','funky_parser.py',235),
  ('LEXP -> LET DECLARATIONS IN EXP','LEXP',4,'p_LEXP','funky_parser.py',236),
  ('LEXP -> EXP IF EXP ELSE EXP','LEXP',5,'p_LEXP','funky_parser.py',237),
  ('LEXP -> MATCH EXP OF OPEN_BRACE ALTS CLOSE_BRACE','LEXP',6,'p_LEXP','funky_parser.py',238),
  ('LEXP -> FEXP','LEXP',1,'p_LEXP','funky_parser.py',239),
  ('FEXP -> FEXP AEXP','FEXP',2,'p_FEXP','funky_parser.py',255),
  ('FEXP -> AEXP','FEXP',1,'p_FEXP','funky_parser.py',256),
  ('AEXP -> USED_VAR','AEXP',1,'p_AEXP','funky_parser.py',264),
  ('AEXP -> USED_TYPENAME','AEXP',1,'p_AEXP','funky_parser.py',265),
  ('AEXP -> LITERAL','AEXP',1,'p_AEXP','funky_parser.py',266),
  ('AEXP -> OPERATOR_FUNC','AEXP',1,'p_AEXP','funky_parser.py',267),
  ('AEXP -> OPEN_PAREN EXP CLOSE_PAREN','AEXP',3,'p_AEXP','funky_parser.py',268),
  ('OPERATOR_FUNC -> OPEN_PAREN OP CLOSE_PAREN','OPERATOR_FUNC',3,'p_OPERATOR_FUNC','funky_parser.py',276),
  ('CONSTRUCTION_PARAMS -> CONSTRUCTION_PARAMS AEXP','CONSTRUCTION_PARAMS',2,'p_CONSTRUCTION_PARAMS','funky_parser.py',280),
  ('CONSTRUCTION_PARAMS -> AEXP','CONSTRUCTION_PARAMS',1,'p_CONSTRUCTION_PARAMS','funky_parser.py',281),
  ('ALTS -> ALT ENDSTATEMENT ALTS','ALTS',3,'p_ALTS','funky_parser.py',289),
  ('ALTS -> ALT','ALTS',1,'p_ALTS','funky_parser.py',290),
  ('ALT -> LPAT ARROW EXP','ALT',3,'p_ALT','funky_parser.py',298),
  ('ALT -> <empty>','ALT',0,'p_ALT','funky_parser.py',299),
  ('LPAT -> APAT','LPAT',1,'p_LPAT','funky_parser.py',304),
  ('LPAT -> MINUS OPEN_PAREN INTEGER CLOSE_PAREN','LPAT',4,'p_LPAT','funky_parser.py',305),
  ('LPAT -> MINUS OPEN_PAREN FLOAT CLOSE_PAREN','LPAT',4,'p_LPAT','funky_parser.py',306),
  ('LPAT -> TYPENAME APAT APATS','LPAT',3,'p_LPAT','funky_parser.py',307),
  ('APAT -> PARAM','APAT',1,'p_APAT','funky_parser.py',317),
  ('APAT -> TYPENAME','APAT',1,'p_APAT','funky_parser.py',318),
  ('APAT -> LITERAL','APAT',1,'p_APAT','funky_parser.py',319),
  ('APAT -> OPEN_PAREN LPAT CLOSE_PAREN','APAT',3,'p_APAT','funky_parser.py',320),
  ('VAROP -> VARSYM','VAROP',1,'p_VAROP','funky_parser.py',331),
  ('VAROP -> BACKTICK IDENTIFIER BACKTICK','VAROP',3,'p_VAROP','funky_parser.py',332),
  ('OP -> VAROP','OP',1,'p_OP','funky_parser.py',342),
  ('APATS -> APAT APATS','APATS',2,'p_APATS','funky_parser.py',347),
  ('APATS -> <empty>','APATS',0,'p_APATS','funky_parser.py',348),
  ('VARSYM -> PLUS','VARSYM',1,'p_VARSYM','funky_parser.py',356),
  ('VARSYM -> MINUS','VARSYM',1,'p_VARSYM','funky_parser.py',357),
  ('VARSYM -> TIMES','VARSYM',1,'p_VARSYM','funky_parser.py',358),
  ('VARSYM -> DIVIDE','VARSYM',1,'p_VARSYM','funky_parser.py',359),
  ('VARSYM -> MODULO','VARSYM',1,'p_VARSYM','funky_parser.py',360),
  ('VARSYM -> POW','VARSYM',1,'p_VARSYM','funky_parser.py',361),
  ('VARSYM -> EQUALITY','VARSYM',1,'p_VARSYM','funky_parser.py',362),
  ('VARSYM -> INEQUALITY','VARSYM',1,'p_VARSYM','funky_parser.py',363),
  ('VARSYM -> LESS','VARSYM',1,'p_VARSYM','funky_parser.py',364),
  ('VARSYM -> LEQ','VARSYM',1,'p_VARSYM','funky_parser.py',365),
  ('VARSYM -> GREATER','VARSYM',1,'p_VARSYM','funky_parser.py',366),
  ('VARSYM -> GEQ','VARSYM',1,'p_VARSYM','funky_parser.py',367),
  ('VARSYM -> AND','VARSYM',1,'p_VARSYM','funky_parser.py',368),
  ('VARSYM -> OR','VARSYM',1,'p_VARSYM','funky_parser.py',369),
  ('LITERAL -> FLOAT','LITERAL',1,'p_LITERAL','funky_parser.py',374),
  ('LITERAL -> INTEGER','LITERAL',1,'p_LITERAL','funky_parser.py',375),
  ('LITERAL -> BOOL','LITERAL',1,'p_LITERAL','funky_parser.py',376),
  ('LITERAL -> CHAR','LITERAL',1,'p_LITERAL','funky_parser.py',377),
  ('LITERAL -> STRING','LITERAL',1,'p_LITERAL','funky_parser.py',378),
  ('USED_VAR -> IDENTIFIER','USED_VAR',1,'p_USED_VAR','funky_parser.py',383),
  ('USED_TYPENAME -> TYPENAME','USED_TYPENAME',1,'p_USED_TYPENAME','funky_parser.py',387),
  ('PARAM -> IDENTIFIER','PARAM',1,'p_PARAM','funky_parser.py',391),
]
