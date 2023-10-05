class Simbolo:
  def __init__(self, lexema, token, tipo=0):
    self.Lexema = lexema
    self.Token = token
    self.Tipo = tipo

  def __repr__(self):
    return ("Lexema: " + self.Lexema).ljust(20) + ("Token: " +
  str(self.Token)).rjust(12)

TOKENS = {
  'BOOL': 256,
  'CALL': 257,
  'CHAR': 258,
  'CONST_CHAR': 259,
  'CONST_STRING' : 260,
  'DIF' : 261,
  'DO' : 262,
  'ELSE' : 263,
  'FLOAT' : 264,
  'FOR' : 265,
  'FUNCTION' : 266,
  'ID' : 267,
  'IF' : 268,
  'IGU' : 269,
  'INT' : 270,
  'MAI' : 271,
  'MAIN' : 272,
  'MAY' : 273,
  'MEI' : 274,
  'MEN' : 275,
  'NUM' : 276,
  'NUMF' : 277,
  'READ' : 278,
  'RETURN' : 279,
  'STRING' : 280,
  'THEN' : 281,
  'TO' : 282,
  'VOID' : 283,
  'WHILE' : 284,
  'WRITE' : 285,
  'FALSE' : 286,
  'TRUE' : 287
  }

TIPO_DATO = {
  'na': 0,
  'int': 1,
  'bool': 2,
  'float': 3,
  'char': 4, 
  'string': 5,
  'arr_int': 6,
  'arr_bool': 7,
  'arr_float': 8,
  'arr_char': 9,
  'arr_string': 10,
  'func_int': 11,
  'func_bool': 12,
  'func_float': 13,
  'func_char': 14,
  'func_string': 15,
  'func_void': 16,
}

ZONA_DE_CODIGO = {
  'DEF_VARIABLES_GLOBALES': 0,
  'DEF_VARIABLES_LOCALES': 1,
  'CUERPO_FUNCION_LOCAL': 2,
  'CUERPO_PRINCIPAL': 3
}

CONST_TOKENS = {}
for key,value in TOKENS.items():
  CONST_TOKENS[value]=key
