
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'PROGleftPOWleftPLUSMINUSleftTIMESDIVIDErightUMINUSARROW CLOSE_BRACKET DIVIDE ELSE EQUALS GUARD IDENTIFIER IF IN LET MATCH MINUS NEWLINE NUMBER OPEN_BRACKET PLUS POW STRING TIMES WHEREPROG : FUNC_LISTFUNC_LIST : FUNC NEWLINE FUNC_LIST\n                     | empty\n        FUNC : IDENTIFIER ARG_LIST EQUALS EXPRESSIONARG_LIST : IDENTIFIER ARG_LIST\n                    | NUMBER ARG_LIST\n                    | STRING ARG_LIST\n                    | IDENTIFIER\n                    | NUMBER\n                    | STRING\n        EXPRESSION : OPEN_BRACKET EXPRESSION CLOSE_BRACKETEXPRESSION : EXPRESSION PLUS EXPRESSION\n                      | EXPRESSION MINUS EXPRESSION\n                      | EXPRESSION TIMES EXPRESSION\n                      | EXPRESSION DIVIDE EXPRESSION\n                      | EXPRESSION POW EXPRESSION\n        EXPRESSION : MINUS EXPRESSION %prec UMINUSEXPRESSION : IDENTIFIER ARG_LISTEXPRESSION : LET IDENTIFIER EQUALS EXPRESSION IN EXPRESSIONEXPRESSION : EXPRESSION IF EXPRESSION ELSE EXPRESSIONEXPRESSION : EXPRESSION WHERE IDENTIFIER EQUALS EXPRESSIONEXPRESSION : NUMBEREXPRESSION : IDENTIFIEREXPRESSION : STRINGempty :'
    
_lr_action_items = {'IDENTIFIER':([0,5,6,7,9,10,13,16,18,19,20,24,25,26,27,28,29,30,42,43,44,48,],[5,7,5,7,7,7,16,7,16,16,33,16,16,16,16,16,16,40,16,16,16,16,]),'$end':([0,1,2,4,6,11,],[-25,0,-1,-3,-25,-2,]),'NEWLINE':([3,7,9,10,12,14,15,16,17,21,22,23,32,34,35,36,37,38,41,46,47,49,],[6,-8,-9,-10,-5,-6,-7,-23,-4,-22,-24,-18,-17,-12,-13,-14,-15,-16,-11,-20,-21,-19,]),'NUMBER':([5,7,9,10,13,16,18,19,24,25,26,27,28,29,42,43,44,48,],[9,9,9,9,21,9,21,21,21,21,21,21,21,21,21,21,21,21,]),'STRING':([5,7,9,10,13,16,18,19,24,25,26,27,28,29,42,43,44,48,],[10,10,10,10,22,10,22,22,22,22,22,22,22,22,22,22,22,22,]),'EQUALS':([7,8,9,10,12,14,15,33,40,],[-8,13,-9,-10,-5,-6,-7,42,44,]),'PLUS':([7,9,10,12,14,15,16,17,21,22,23,31,32,34,35,36,37,38,39,41,45,46,47,49,],[-8,-9,-10,-5,-6,-7,-23,24,-22,-24,-18,24,-17,-12,-13,-14,-15,24,24,-11,24,24,24,24,]),'MINUS':([7,9,10,12,13,14,15,16,17,18,19,21,22,23,24,25,26,27,28,29,31,32,34,35,36,37,38,39,41,42,43,44,45,46,47,48,49,],[-8,-9,-10,-5,19,-6,-7,-23,25,19,19,-22,-24,-18,19,19,19,19,19,19,25,-17,-12,-13,-14,-15,25,25,-11,19,19,19,25,25,25,19,25,]),'TIMES':([7,9,10,12,14,15,16,17,21,22,23,31,32,34,35,36,37,38,39,41,45,46,47,49,],[-8,-9,-10,-5,-6,-7,-23,26,-22,-24,-18,26,-17,26,26,-14,-15,26,26,-11,26,26,26,26,]),'DIVIDE':([7,9,10,12,14,15,16,17,21,22,23,31,32,34,35,36,37,38,39,41,45,46,47,49,],[-8,-9,-10,-5,-6,-7,-23,27,-22,-24,-18,27,-17,27,27,-14,-15,27,27,-11,27,27,27,27,]),'POW':([7,9,10,12,14,15,16,17,21,22,23,31,32,34,35,36,37,38,39,41,45,46,47,49,],[-8,-9,-10,-5,-6,-7,-23,28,-22,-24,-18,28,-17,-12,-13,-14,-15,-16,28,-11,28,28,28,28,]),'IF':([7,9,10,12,14,15,16,17,21,22,23,31,32,34,35,36,37,38,39,41,45,46,47,49,],[-8,-9,-10,-5,-6,-7,-23,29,-22,-24,-18,29,-17,-12,-13,-14,-15,-16,29,-11,29,29,29,29,]),'WHERE':([7,9,10,12,14,15,16,17,21,22,23,31,32,34,35,36,37,38,39,41,45,46,47,49,],[-8,-9,-10,-5,-6,-7,-23,30,-22,-24,-18,30,-17,-12,-13,-14,-15,-16,30,-11,30,30,30,30,]),'CLOSE_BRACKET':([7,9,10,12,14,15,16,21,22,23,31,32,34,35,36,37,38,41,46,47,49,],[-8,-9,-10,-5,-6,-7,-23,-22,-24,-18,41,-17,-12,-13,-14,-15,-16,-11,-20,-21,-19,]),'ELSE':([7,9,10,12,14,15,16,21,22,23,32,34,35,36,37,38,39,41,46,47,49,],[-8,-9,-10,-5,-6,-7,-23,-22,-24,-18,-17,-12,-13,-14,-15,-16,43,-11,-20,-21,-19,]),'IN':([7,9,10,12,14,15,16,21,22,23,32,34,35,36,37,38,41,45,46,47,49,],[-8,-9,-10,-5,-6,-7,-23,-22,-24,-18,-17,-12,-13,-14,-15,-16,-11,48,-20,-21,-19,]),'OPEN_BRACKET':([13,18,19,24,25,26,27,28,29,42,43,44,48,],[18,18,18,18,18,18,18,18,18,18,18,18,18,]),'LET':([13,18,19,24,25,26,27,28,29,42,43,44,48,],[20,20,20,20,20,20,20,20,20,20,20,20,20,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'PROG':([0,],[1,]),'FUNC_LIST':([0,6,],[2,11,]),'FUNC':([0,6,],[3,3,]),'empty':([0,6,],[4,4,]),'ARG_LIST':([5,7,9,10,16,],[8,12,14,15,23,]),'EXPRESSION':([13,18,19,24,25,26,27,28,29,42,43,44,48,],[17,31,32,34,35,36,37,38,39,45,46,47,49,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> PROG","S'",1,None,None,None),
  ('PROG -> FUNC_LIST','PROG',1,'p_PROG','funky_parser.py',21),
  ('FUNC_LIST -> FUNC NEWLINE FUNC_LIST','FUNC_LIST',3,'p_FUNC_LIST','funky_parser.py',25),
  ('FUNC_LIST -> empty','FUNC_LIST',1,'p_FUNC_LIST','funky_parser.py',26),
  ('FUNC -> IDENTIFIER ARG_LIST EQUALS EXPRESSION','FUNC',4,'p_FUNC','funky_parser.py',31),
  ('ARG_LIST -> IDENTIFIER ARG_LIST','ARG_LIST',2,'p_ARG_LIST','funky_parser.py',35),
  ('ARG_LIST -> NUMBER ARG_LIST','ARG_LIST',2,'p_ARG_LIST','funky_parser.py',36),
  ('ARG_LIST -> STRING ARG_LIST','ARG_LIST',2,'p_ARG_LIST','funky_parser.py',37),
  ('ARG_LIST -> IDENTIFIER','ARG_LIST',1,'p_ARG_LIST','funky_parser.py',38),
  ('ARG_LIST -> NUMBER','ARG_LIST',1,'p_ARG_LIST','funky_parser.py',39),
  ('ARG_LIST -> STRING','ARG_LIST',1,'p_ARG_LIST','funky_parser.py',40),
  ('EXPRESSION -> OPEN_BRACKET EXPRESSION CLOSE_BRACKET','EXPRESSION',3,'p_EXPRESSION_GROUP','funky_parser.py',45),
  ('EXPRESSION -> EXPRESSION PLUS EXPRESSION','EXPRESSION',3,'p_EXPRESSION_BINOP','funky_parser.py',49),
  ('EXPRESSION -> EXPRESSION MINUS EXPRESSION','EXPRESSION',3,'p_EXPRESSION_BINOP','funky_parser.py',50),
  ('EXPRESSION -> EXPRESSION TIMES EXPRESSION','EXPRESSION',3,'p_EXPRESSION_BINOP','funky_parser.py',51),
  ('EXPRESSION -> EXPRESSION DIVIDE EXPRESSION','EXPRESSION',3,'p_EXPRESSION_BINOP','funky_parser.py',52),
  ('EXPRESSION -> EXPRESSION POW EXPRESSION','EXPRESSION',3,'p_EXPRESSION_BINOP','funky_parser.py',53),
  ('EXPRESSION -> MINUS EXPRESSION','EXPRESSION',2,'p_EXPRESSION_UMINUS','funky_parser.py',58),
  ('EXPRESSION -> IDENTIFIER ARG_LIST','EXPRESSION',2,'p_EXPRESSION_FUNCTION_APP','funky_parser.py',62),
  ('EXPRESSION -> LET IDENTIFIER EQUALS EXPRESSION IN EXPRESSION','EXPRESSION',6,'p_EXPRESSION_LET','funky_parser.py',66),
  ('EXPRESSION -> EXPRESSION IF EXPRESSION ELSE EXPRESSION','EXPRESSION',5,'p_EXPRESSION_IF','funky_parser.py',70),
  ('EXPRESSION -> EXPRESSION WHERE IDENTIFIER EQUALS EXPRESSION','EXPRESSION',5,'p_EXPRESSION_WHERE','funky_parser.py',74),
  ('EXPRESSION -> NUMBER','EXPRESSION',1,'p_EXPRESSION_NUMBER','funky_parser.py',78),
  ('EXPRESSION -> IDENTIFIER','EXPRESSION',1,'p_EXPRESSION_VARIABLE','funky_parser.py',82),
  ('EXPRESSION -> STRING','EXPRESSION',1,'p_EXPRESSION_STRING','funky_parser.py',86),
  ('empty -> <empty>','empty',0,'p_empty','funky_parser.py',90),
]
