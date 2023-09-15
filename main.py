entrance = ''
ERR = -1
ACP = 99
idx = 0
ERRA = False
NOPRINC = True
rowg = 1
colm = 1
OPAS = ['+', '-', '*', '%' , '^']
delu = ['\n', '\t', ' ', chr(32)]
keywords = ['constante', 'entero', 'decimal', 'logico', 'palabra', 'sintipo',
            'inicio', 'fin', 'si', 'sino', 'hacer', 'desde', 'hasta', 'incr',
            'decr', 'regresa', 'imprime', 'imprimenl', 'lee', 'interrumpe', 'continua']

OPL = ['no', 'y', 'o']
CTL = ['verdadero', 'falso']
delim = ['.', ';', ':', '(', ')', '[', ']', '{', '}']
special = ['!', '$', '#', '@', '?']

matrans = [
  #* col 0 = 'letra'
  #* col 1 = '_'
  #* col 2 = 'Digito'
  #* col 3 = 'OPAS'
  #* col 4 = '/'
  #* col 5 = '.'
  #* col 6 = '*'
  #* col 7 = 'Del'
  #* col 8 = ':'
  #* col 9 = '='
  #* col 10 = '<'
  #* col 11 = "
  #* col 12 = special

  [  1 ,  1 ,  2 ,  5 ,  6 ,  11,  10,  11,  12,  14,  15,  18, ERR ], #0
  [  1 ,  1 ,  1 , ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP ], #1
  [ ACP, ACP,  2 , ACP, ACP,  3 , ACP, ACP, ACP, ACP, ACP, ACP, ACP ], #2
  [ ERR, ERR,  4 , ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR ], #3
  [ ACP, ACP,  4 , ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP ], #4
  [ ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP ], #5
  [ ACP, ACP, ACP, ACP,  7 , ACP,  8 , ACP, ACP, ACP, ACP, ACP, ACP ], #6
  [  7 ,  7 ,  7 ,  7 ,  7 ,  7 ,  7 ,  7 ,  7 ,  7 ,  7 ,  7 ,  7  ], #7
  [  8 ,  8 ,  8 ,  8 ,  8 ,  8 ,  9 ,  8 ,  8 ,  8 ,  8 ,  8 ,  8  ], #8
  [  8 ,  8 ,  8 ,  9 ,  0 ,  8 ,  9 ,  8 ,  8 ,  8 ,  8 ,  8 ,  8  ], #9
  [ ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP ], #10
  [ ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP ], #11
  [ ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP,  13, ACP, ACP, ACP ], #12
  [ ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP ], #13
  [ ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP ], #14
  [ ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP,  16, ACP, ACP, ACP ], #15
  [ ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP ], #16
  [ ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP ], #17
  [  18,  18,  18,  18,  18,  18,  18,  18,  18,  18,  18,  19,  18 ], #18
  [ ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP ], #19
]

def colCar(x):
  if x.isalpha() or x in delu: return 0
  if x == '_'   : return 1
  if x.isdigit(): return 2
  if x in OPAS  : return 3
  if x == '/'   : return 4
  if x == '.'   : return 5
  if x == '*'   : return 6
  if x in delim : return 7
  if x == ':'   : return 8
  if x == '='   : return 9
  if x in '<'   : return 10
  if x in '"'   : return 11
  if x in special: return 12

  if not(x in delu):
    print(x, 'is not a char or illegal symbol')
    return ERR


def scanner():
  global entrance, matrans, ERR, ACP, idx, colm, rowg
  lexema = ''
  token = ''
  status = 0
  statusA = 0
  col = -1

  while idx < len(entrance) and status != ERR and status != ACP:
    if entrance[idx] != '\n':
      idx += 1
      colm += 1
      continue

    if status != 0 and (entrance[idx] in delu or ord(entrance[idx]) == 32):
      statusA = status
      status == ACP
    else:
      print('Estado al entrar: ', status)
      while status != 7 and idx < len(entrance) and status == 0 \
      and (entrance[idx] in delu or ord(entrance[idx]) == 32): 
        if entrance[idx] == '\n':
          rowg += 1
          colm = 1
        else:
          idx += 1
          colm += 1

    if idx >= len(entrance): break

    if status != ACP:
      c = entrance[idx]
      print('c =', c)

      if c == '\n':
        rowg += 1
        colm = 1
      else:
        idx += 1
        colm += 1
      col = colCar( c )

    if c in delu and status != 18:
      statusA = status
      status = ACP

    if col >= 0 and col <= 12 and status != ACP and status != ERR:
      statusA = status

      if c in delu and status != 18: status = ACP
      status = matrans[status][col]

      if status == 18: print(18, lexema)
      if status == ACP: break
      if status != ERR:
        lexema += c

    else: status = ERR

    if status == 7 or status == 8 or status == 9: token = lexema = ''

  print('Estado al salir: ', status)
  if status == ERR or status == ACP: idx -= 1
  else: statusA = status
  print('Estado al entrar: ', statusA)

  if status == ERR or status == ACP: idx -= 1
  else: statusA = status

  if statusA == 1: 
    token = 'Ide'

    if lexema in keywords: token = 'Res'
    elif lexema in OPL: token = 'OpL'
    elif lexema in CTL: token = 'CtL'

  elif statusA == 2: token = 'Ent'
  elif statusA == 4: token = 'Dec'
  elif statusA in [5, 6, 10]: token = 'OpA'
  elif statusA == 11 or statusA == 12: token = 'Del'
  elif statusA == 13: token = 'OpS'
  elif statusA == 19: token = 'CtA'

  print(token, '\t\t\t', lexema)
  return token, lexema

#! Error Zone

def error(tipe, desc, obj):
  global rowg, colm
  ERRA = True
  print('Linea:' + '['+ str(rowg) +']' + 'Columna:' + '[' + str(colm)+ '] Error de '+ tipe, desc, obj)

def params(): pass

def estatutos(): pass

def constvars(): pass

def bloque():
  global tok, lex

  if lex != 'inicio':
    error('Error de Sintaxis', 'se esperaba <inicio> y llego', lex)
  tok, lex = scanner()
  if lex != 'Fin':
    constvars()
  if lex != 'Fin':
    estatutos()
  if lex != 'fin':
    error('Error de Sintaxis', 'se esperaba <fin> y llego', lex)
  tok, lex = scanner()

def funcParcial():
  global tok, lex, idf, NOPRINC
  if idf == 'principal': NOPRINC = False
  tok, lex = scanner()

  if lex != ')':
    params()

  if lex != ')':
    error('Sintaxis', 'Se esperaba cerrar ) y llego ', lex)
  tok, lex = scanner()
  bloque()

  if lex != ';':
    error('Sintaxis', 'Se esperaba <;> y llego ', lex)
  tok, lex = scanner()

def prgm():
  global tok, lex, idf, NOPRINC
  tok, lex = scanner();
  while lex == 'constante' or lex == 'entero' or lex =='decimal' or \
        lex == 'palabra' or lex == 'logico' or \
        lex == 'sintipo' and idx < len(entrance):
    
    if lex == 'constante': constvars()
    else:
      if lex != 'entero' and lex != 'decimal' and \
          lex != 'palabra' and lex != 'logico' and \
          lex != 'sintipo':
          error('Sintaxis',\
                'Se esperaba <entero>, <decimal>, <logico>, <palabra> o <sintipo> y llego ',\
              lex)
      else: 
        tok, lex = scanner()
        if tok == 'Ide': idf = lex
        else:
          error('Sintaxis', 'Se esperaba <Ide> y llego ', tok)
        tok, lex = scanner()

        if lex == '(': 
          funcParcial()
        else: 
          constvars()

#** Main Zone
if __name__ == '__main__':
  archE = ''

  print(archE[len(archE)-3:])
  while (archE[len(archE)-3:] != '.icc'):
    archE = input('File to compile (*.icc) [. = Exit]: ') # icc = Ingeniero en Ciencias Computacionales

    if archE == '.':
      exit(0)

    try:
      inputF = open(archE, 'r+')
      break

    except FileNotFoundError:
      print('No existe el archivo: ', archE)

  if inputF != None:
    while line := inputF.readline():
      entrance += line

  else:
    print('No existe el archivo: ', archE)
    exit(1)

  print('\n\n' + entrance, '\n\n')

  tok = lex = ''
  prgm()
  if NOPRINC:
    error('Error de Semantica', 'NO declaro la funcion <principal>', '')

  if ERRA == False:
    print('Compilado con exito')
