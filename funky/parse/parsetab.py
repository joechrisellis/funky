
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'FIXITY_DECLARATIONAND ARROW BACKTICK BOOL CLOSE_BRACE CLOSE_PAREN CONCAT DIVIDE ELSE ENDSTATEMENT EQUALITY EQUALS FLOAT GEQ GIVEN GREATER IDENTIFIER IF IMPORT IN INEQUALITY INTEGER LAMBDA LEFTASSOC LEQ LESS LET MATCH MINUS MODULE MODULO NEWTYPE NONASSOC OF OPEN_BRACE OPEN_PAREN OR PIPE PLUS POW RIGHTASSOC SETFIX STRING TIMES TYPENAME WHERE WHITESPACEMODULE_DEFINITION : MODULE IDENTIFIER WHERE BODY\n        BODY : OPEN_BRACE IMPORT_DECLARATIONS ENDSTATEMENT TOP_DECLARATIONS CLOSE_BRACE\n                | OPEN_BRACE TOP_DECLARATIONS CLOSE_BRACE\n        IMPORT_DECLARATIONS : IMPORT_DECLARATIONS ENDSTATEMENT IMPORT_DECLARATION\n                               | IMPORT_DECLARATION\n        IMPORT_DECLARATION : IMPORT STRINGTOP_DECLARATIONS : TOP_DECLARATIONS ENDSTATEMENT TOP_DECLARATION\n                            | TOP_DECLARATION\n        TOP_DECLARATION : TYPE_DECLARATION\n                           | DECLARATION\n        TYPE_DECLARATION : NEWTYPE TYPENAME TYVARS EQUALS CONSTRUCTORSTYVARS : TYVARS IDENTIFIER\n                  |\n        CONSTRUCTORS : CONSTRUCTORS PIPE CONSTRUCTOR\n                        | CONSTRUCTOR\n        CONSTRUCTOR : TYPENAME ATYPESDECLARATIONS : OPEN_BRACE DECLARATIONS_LIST CLOSE_BRACE\n                        | OPEN_BRACE CLOSE_BRACE\n        DECLARATIONS_LIST : DECLARATION ENDSTATEMENT DECLARATIONS_LIST\n                             | DECLARATION\n        DECLARATION : FUNCTION_DEFINITION\n                       | VARIABLE_DEFINITION\n                       | FIXITY_DECLARATION\n                       |\n        FUNCTION_DEFINITION : FUNCTION_LHS RHSVARIABLE_DEFINITION : PARAM RHSFIXITY_DECLARATION : SETFIX ASSOCIATIVITY INTEGER OPASSOCIATIVITY : LEFTASSOC\n                         | RIGHTASSOC\n                         | NONASSOC\n        TYPE : ATYPE\n                | ATYPE ARROW TYPE\n        ATYPES : ATYPES ATYPE\n                  |\n        ATYPE : TYPENAME\n                 | IDENTIFIER\n                 | OPEN_PAREN TYPE CLOSE_PAREN\n        FUNCTION_LHS : IDENTIFIER APAT APATS\n                        | OPEN_PAREN FUNCTION_LHS CLOSE_PAREN APAT APATS\n                        | INFIX_FUNCTION_DEFINITION\n        INFIX_FUNCTION_DEFINITION : LPAT INFIX_FUNCTION LPATRHS : EQUALS EXP\n               | EQUALS EXP WHERE DECLARATIONS\n               | GDRHS\n               | GDRHS WHERE DECLARATIONS\n        GDRHS : GIVEN EXP EQUALS EXP\n                 | GIVEN EXP EQUALS EXP GDRHS\n        EXP : INFIX_EXPINFIX_EXP : LEXP OP INFIX_EXP\n                     | MINUS INFIX_EXP\n                     | LEXP\n        LEXP : LAMBDA_ABSTRACTION\n                | LET_EXPR\n                | IF_EXPR\n                | MATCH_EXPR\n                | FUNCTION_EXPR\n        LAMBDA_ABSTRACTION : LAMBDA APAT APATS ARROW EXPLET_EXPR : LET DECLARATIONS IN EXPIF_EXPR : EXP IF EXP ELSE EXPMATCH_EXPR : MATCH EXP OF OPEN_BRACE ALTS CLOSE_BRACEFUNCTION_EXPR : FUNCTION_EXPR AEXP\n                         | AEXP\n        AEXP : USED_VAR\n                | USED_TYPENAME\n                | LITERAL\n                | OPERATOR_FUNC\n                | OPEN_PAREN EXP CLOSE_PAREN\n        OPERATOR_FUNC : OPEN_PAREN OP CLOSE_PARENALTS : ALT ENDSTATEMENT ALTS\n                | ALT\n        ALT : LPAT ARROW EXP\n               |\n        LPAT : APAT\n                | CONSTRUCTOR_PATTERN\n                | NEGATIVE_LITERAL\n        CONSTRUCTOR_PATTERN : TYPENAME APAT APATSNEGATIVE_LITERAL : MINUS INTEGER\n                            | MINUS FLOAT\n        APAT : PARAM\n                | TYPENAME\n                | LITERAL\n                | OPEN_PAREN LPAT CLOSE_PAREN\n        OP : VARSYM\n              | INFIX_FUNCTION\n        INFIX_FUNCTION : BACKTICK IDENTIFIER BACKTICKAPATS : APAT APATS\n                 |\n        VARSYM : PLUS\n                  | MINUS\n                  | TIMES\n                  | DIVIDE\n                  | MODULO\n                  | POW\n                  | EQUALITY\n                  | INEQUALITY\n                  | LESS\n                  | LEQ\n                  | GREATER\n                  | GEQ\n                  | CONCAT\n                  | AND\n                  | OR\n        LITERAL : FLOAT\n                   | INTEGER\n                   | BOOL\n                   | STRING\n        USED_VAR : IDENTIFIERUSED_TYPENAME : TYPENAMEPARAM : IDENTIFIER'
    
_lr_action_items = {'SETFIX':([0,],[2,]),'$end':([1,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,28,],[0,-27,-83,-84,-88,-89,-90,-91,-92,-93,-94,-95,-96,-97,-98,-99,-100,-101,-102,-85,]),'LEFTASSOC':([2,],[4,]),'RIGHTASSOC':([2,],[5,]),'NONASSOC':([2,],[6,]),'INTEGER':([3,4,5,6,],[7,-28,-29,-30,]),'PLUS':([7,],[11,]),'MINUS':([7,],[12,]),'TIMES':([7,],[13,]),'DIVIDE':([7,],[14,]),'MODULO':([7,],[15,]),'POW':([7,],[16,]),'EQUALITY':([7,],[17,]),'INEQUALITY':([7,],[18,]),'LESS':([7,],[19,]),'LEQ':([7,],[20,]),'GREATER':([7,],[21,]),'GEQ':([7,],[22,]),'CONCAT':([7,],[23,]),'AND':([7,],[24,]),'OR':([7,],[25,]),'BACKTICK':([7,27,],[26,28,]),'IDENTIFIER':([26,],[27,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'FIXITY_DECLARATION':([0,],[1,]),'ASSOCIATIVITY':([2,],[3,]),'OP':([7,],[8,]),'VARSYM':([7,],[9,]),'INFIX_FUNCTION':([7,],[10,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> FIXITY_DECLARATION","S'",1,None,None,None),
  ('MODULE_DEFINITION -> MODULE IDENTIFIER WHERE BODY','MODULE_DEFINITION',4,'p_MODULE_DEFINITION','funky_parser.py',18),
  ('BODY -> OPEN_BRACE IMPORT_DECLARATIONS ENDSTATEMENT TOP_DECLARATIONS CLOSE_BRACE','BODY',5,'p_BODY','funky_parser.py',24),
  ('BODY -> OPEN_BRACE TOP_DECLARATIONS CLOSE_BRACE','BODY',3,'p_BODY','funky_parser.py',25),
  ('IMPORT_DECLARATIONS -> IMPORT_DECLARATIONS ENDSTATEMENT IMPORT_DECLARATION','IMPORT_DECLARATIONS',3,'p_IMPORT_DECLARATIONS','funky_parser.py',37),
  ('IMPORT_DECLARATIONS -> IMPORT_DECLARATION','IMPORT_DECLARATIONS',1,'p_IMPORT_DECLARATIONS','funky_parser.py',38),
  ('IMPORT_DECLARATION -> IMPORT STRING','IMPORT_DECLARATION',2,'p_IMPORT_DECLARATION','funky_parser.py',46),
  ('TOP_DECLARATIONS -> TOP_DECLARATIONS ENDSTATEMENT TOP_DECLARATION','TOP_DECLARATIONS',3,'p_TOP_DECLARATIONS','funky_parser.py',50),
  ('TOP_DECLARATIONS -> TOP_DECLARATION','TOP_DECLARATIONS',1,'p_TOP_DECLARATIONS','funky_parser.py',51),
  ('TOP_DECLARATION -> TYPE_DECLARATION','TOP_DECLARATION',1,'p_TOP_DECLARATION','funky_parser.py',59),
  ('TOP_DECLARATION -> DECLARATION','TOP_DECLARATION',1,'p_TOP_DECLARATION','funky_parser.py',60),
  ('TYPE_DECLARATION -> NEWTYPE TYPENAME TYVARS EQUALS CONSTRUCTORS','TYPE_DECLARATION',5,'p_TYPE_DECLARATION','funky_parser.py',65),
  ('TYVARS -> TYVARS IDENTIFIER','TYVARS',2,'p_TYVARS','funky_parser.py',69),
  ('TYVARS -> <empty>','TYVARS',0,'p_TYVARS','funky_parser.py',70),
  ('CONSTRUCTORS -> CONSTRUCTORS PIPE CONSTRUCTOR','CONSTRUCTORS',3,'p_CONSTRUCTORS','funky_parser.py',78),
  ('CONSTRUCTORS -> CONSTRUCTOR','CONSTRUCTORS',1,'p_CONSTRUCTORS','funky_parser.py',79),
  ('CONSTRUCTOR -> TYPENAME ATYPES','CONSTRUCTOR',2,'p_CONSTRUCTOR','funky_parser.py',87),
  ('DECLARATIONS -> OPEN_BRACE DECLARATIONS_LIST CLOSE_BRACE','DECLARATIONS',3,'p_DECLARATIONS','funky_parser.py',91),
  ('DECLARATIONS -> OPEN_BRACE CLOSE_BRACE','DECLARATIONS',2,'p_DECLARATIONS','funky_parser.py',92),
  ('DECLARATIONS_LIST -> DECLARATION ENDSTATEMENT DECLARATIONS_LIST','DECLARATIONS_LIST',3,'p_DECLARATIONS_LIST','funky_parser.py',100),
  ('DECLARATIONS_LIST -> DECLARATION','DECLARATIONS_LIST',1,'p_DECLARATIONS_LIST','funky_parser.py',101),
  ('DECLARATION -> FUNCTION_DEFINITION','DECLARATION',1,'p_DECLARATION','funky_parser.py',109),
  ('DECLARATION -> VARIABLE_DEFINITION','DECLARATION',1,'p_DECLARATION','funky_parser.py',110),
  ('DECLARATION -> FIXITY_DECLARATION','DECLARATION',1,'p_DECLARATION','funky_parser.py',111),
  ('DECLARATION -> <empty>','DECLARATION',0,'p_DECLARATION','funky_parser.py',112),
  ('FUNCTION_DEFINITION -> FUNCTION_LHS RHS','FUNCTION_DEFINITION',2,'p_FUNCTION_DEFINITION','funky_parser.py',118),
  ('VARIABLE_DEFINITION -> PARAM RHS','VARIABLE_DEFINITION',2,'p_VARIABLE_DEFINITION','funky_parser.py',122),
  ('FIXITY_DECLARATION -> SETFIX ASSOCIATIVITY INTEGER OP','FIXITY_DECLARATION',4,'p_FIXITY_DECLARATION','funky_parser.py',126),
  ('ASSOCIATIVITY -> LEFTASSOC','ASSOCIATIVITY',1,'p_ASSOCIATIVITY','funky_parser.py',130),
  ('ASSOCIATIVITY -> RIGHTASSOC','ASSOCIATIVITY',1,'p_ASSOCIATIVITY','funky_parser.py',131),
  ('ASSOCIATIVITY -> NONASSOC','ASSOCIATIVITY',1,'p_ASSOCIATIVITY','funky_parser.py',132),
  ('TYPE -> ATYPE','TYPE',1,'p_TYPE','funky_parser.py',137),
  ('TYPE -> ATYPE ARROW TYPE','TYPE',3,'p_TYPE','funky_parser.py',138),
  ('ATYPES -> ATYPES ATYPE','ATYPES',2,'p_ATYPES','funky_parser.py',146),
  ('ATYPES -> <empty>','ATYPES',0,'p_ATYPES','funky_parser.py',147),
  ('ATYPE -> TYPENAME','ATYPE',1,'p_ATYPE','funky_parser.py',155),
  ('ATYPE -> IDENTIFIER','ATYPE',1,'p_ATYPE','funky_parser.py',156),
  ('ATYPE -> OPEN_PAREN TYPE CLOSE_PAREN','ATYPE',3,'p_ATYPE','funky_parser.py',157),
  ('FUNCTION_LHS -> IDENTIFIER APAT APATS','FUNCTION_LHS',3,'p_FUNCTION_LHS','funky_parser.py',165),
  ('FUNCTION_LHS -> OPEN_PAREN FUNCTION_LHS CLOSE_PAREN APAT APATS','FUNCTION_LHS',5,'p_FUNCTION_LHS','funky_parser.py',166),
  ('FUNCTION_LHS -> INFIX_FUNCTION_DEFINITION','FUNCTION_LHS',1,'p_FUNCTION_LHS','funky_parser.py',167),
  ('INFIX_FUNCTION_DEFINITION -> LPAT INFIX_FUNCTION LPAT','INFIX_FUNCTION_DEFINITION',3,'p_INFIX_FUNCTION_DEFINITION','funky_parser.py',179),
  ('RHS -> EQUALS EXP','RHS',2,'p_RHS','funky_parser.py',183),
  ('RHS -> EQUALS EXP WHERE DECLARATIONS','RHS',4,'p_RHS','funky_parser.py',184),
  ('RHS -> GDRHS','RHS',1,'p_RHS','funky_parser.py',185),
  ('RHS -> GDRHS WHERE DECLARATIONS','RHS',3,'p_RHS','funky_parser.py',186),
  ('GDRHS -> GIVEN EXP EQUALS EXP','GDRHS',4,'p_GDRHS','funky_parser.py',199),
  ('GDRHS -> GIVEN EXP EQUALS EXP GDRHS','GDRHS',5,'p_GDRHS','funky_parser.py',200),
  ('EXP -> INFIX_EXP','EXP',1,'p_EXP','funky_parser.py',208),
  ('INFIX_EXP -> LEXP OP INFIX_EXP','INFIX_EXP',3,'p_INFIX_EXP','funky_parser.py',213),
  ('INFIX_EXP -> MINUS INFIX_EXP','INFIX_EXP',2,'p_INFIX_EXP','funky_parser.py',214),
  ('INFIX_EXP -> LEXP','INFIX_EXP',1,'p_INFIX_EXP','funky_parser.py',215),
  ('LEXP -> LAMBDA_ABSTRACTION','LEXP',1,'p_LEXP','funky_parser.py',233),
  ('LEXP -> LET_EXPR','LEXP',1,'p_LEXP','funky_parser.py',234),
  ('LEXP -> IF_EXPR','LEXP',1,'p_LEXP','funky_parser.py',235),
  ('LEXP -> MATCH_EXPR','LEXP',1,'p_LEXP','funky_parser.py',236),
  ('LEXP -> FUNCTION_EXPR','LEXP',1,'p_LEXP','funky_parser.py',237),
  ('LAMBDA_ABSTRACTION -> LAMBDA APAT APATS ARROW EXP','LAMBDA_ABSTRACTION',5,'p_LAMBDA_ABSTRACTION','funky_parser.py',242),
  ('LET_EXPR -> LET DECLARATIONS IN EXP','LET_EXPR',4,'p_LET_EXPR','funky_parser.py',246),
  ('IF_EXPR -> EXP IF EXP ELSE EXP','IF_EXPR',5,'p_IF_EXPR','funky_parser.py',250),
  ('MATCH_EXPR -> MATCH EXP OF OPEN_BRACE ALTS CLOSE_BRACE','MATCH_EXPR',6,'p_MATCH_EXPR','funky_parser.py',254),
  ('FUNCTION_EXPR -> FUNCTION_EXPR AEXP','FUNCTION_EXPR',2,'p_FUNCTION_EXPR','funky_parser.py',258),
  ('FUNCTION_EXPR -> AEXP','FUNCTION_EXPR',1,'p_FUNCTION_EXPR','funky_parser.py',259),
  ('AEXP -> USED_VAR','AEXP',1,'p_AEXP','funky_parser.py',267),
  ('AEXP -> USED_TYPENAME','AEXP',1,'p_AEXP','funky_parser.py',268),
  ('AEXP -> LITERAL','AEXP',1,'p_AEXP','funky_parser.py',269),
  ('AEXP -> OPERATOR_FUNC','AEXP',1,'p_AEXP','funky_parser.py',270),
  ('AEXP -> OPEN_PAREN EXP CLOSE_PAREN','AEXP',3,'p_AEXP','funky_parser.py',271),
  ('OPERATOR_FUNC -> OPEN_PAREN OP CLOSE_PAREN','OPERATOR_FUNC',3,'p_OPERATOR_FUNC','funky_parser.py',279),
  ('ALTS -> ALT ENDSTATEMENT ALTS','ALTS',3,'p_ALTS','funky_parser.py',283),
  ('ALTS -> ALT','ALTS',1,'p_ALTS','funky_parser.py',284),
  ('ALT -> LPAT ARROW EXP','ALT',3,'p_ALT','funky_parser.py',292),
  ('ALT -> <empty>','ALT',0,'p_ALT','funky_parser.py',293),
  ('LPAT -> APAT','LPAT',1,'p_LPAT','funky_parser.py',298),
  ('LPAT -> CONSTRUCTOR_PATTERN','LPAT',1,'p_LPAT','funky_parser.py',299),
  ('LPAT -> NEGATIVE_LITERAL','LPAT',1,'p_LPAT','funky_parser.py',300),
  ('CONSTRUCTOR_PATTERN -> TYPENAME APAT APATS','CONSTRUCTOR_PATTERN',3,'p_CONSTRUCTOR_PATTERN','funky_parser.py',305),
  ('NEGATIVE_LITERAL -> MINUS INTEGER','NEGATIVE_LITERAL',2,'p_NEGATIVE_LITERAL','funky_parser.py',309),
  ('NEGATIVE_LITERAL -> MINUS FLOAT','NEGATIVE_LITERAL',2,'p_NEGATIVE_LITERAL','funky_parser.py',310),
  ('APAT -> PARAM','APAT',1,'p_APAT','funky_parser.py',315),
  ('APAT -> TYPENAME','APAT',1,'p_APAT','funky_parser.py',316),
  ('APAT -> LITERAL','APAT',1,'p_APAT','funky_parser.py',317),
  ('APAT -> OPEN_PAREN LPAT CLOSE_PAREN','APAT',3,'p_APAT','funky_parser.py',318),
  ('OP -> VARSYM','OP',1,'p_OP','funky_parser.py',329),
  ('OP -> INFIX_FUNCTION','OP',1,'p_OP','funky_parser.py',330),
  ('INFIX_FUNCTION -> BACKTICK IDENTIFIER BACKTICK','INFIX_FUNCTION',3,'p_INFIX_FUNCTION','funky_parser.py',335),
  ('APATS -> APAT APATS','APATS',2,'p_APATS','funky_parser.py',341),
  ('APATS -> <empty>','APATS',0,'p_APATS','funky_parser.py',342),
  ('VARSYM -> PLUS','VARSYM',1,'p_VARSYM','funky_parser.py',350),
  ('VARSYM -> MINUS','VARSYM',1,'p_VARSYM','funky_parser.py',351),
  ('VARSYM -> TIMES','VARSYM',1,'p_VARSYM','funky_parser.py',352),
  ('VARSYM -> DIVIDE','VARSYM',1,'p_VARSYM','funky_parser.py',353),
  ('VARSYM -> MODULO','VARSYM',1,'p_VARSYM','funky_parser.py',354),
  ('VARSYM -> POW','VARSYM',1,'p_VARSYM','funky_parser.py',355),
  ('VARSYM -> EQUALITY','VARSYM',1,'p_VARSYM','funky_parser.py',356),
  ('VARSYM -> INEQUALITY','VARSYM',1,'p_VARSYM','funky_parser.py',357),
  ('VARSYM -> LESS','VARSYM',1,'p_VARSYM','funky_parser.py',358),
  ('VARSYM -> LEQ','VARSYM',1,'p_VARSYM','funky_parser.py',359),
  ('VARSYM -> GREATER','VARSYM',1,'p_VARSYM','funky_parser.py',360),
  ('VARSYM -> GEQ','VARSYM',1,'p_VARSYM','funky_parser.py',361),
  ('VARSYM -> CONCAT','VARSYM',1,'p_VARSYM','funky_parser.py',362),
  ('VARSYM -> AND','VARSYM',1,'p_VARSYM','funky_parser.py',363),
  ('VARSYM -> OR','VARSYM',1,'p_VARSYM','funky_parser.py',364),
  ('LITERAL -> FLOAT','LITERAL',1,'p_LITERAL','funky_parser.py',369),
  ('LITERAL -> INTEGER','LITERAL',1,'p_LITERAL','funky_parser.py',370),
  ('LITERAL -> BOOL','LITERAL',1,'p_LITERAL','funky_parser.py',371),
  ('LITERAL -> STRING','LITERAL',1,'p_LITERAL','funky_parser.py',372),
  ('USED_VAR -> IDENTIFIER','USED_VAR',1,'p_USED_VAR','funky_parser.py',377),
  ('USED_TYPENAME -> TYPENAME','USED_TYPENAME',1,'p_USED_TYPENAME','funky_parser.py',381),
  ('PARAM -> IDENTIFIER','PARAM',1,'p_PARAM','funky_parser.py',385),
]
