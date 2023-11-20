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
delim = ['.', ',', ';', '(', ')', '[', ']']
special = ['!', '$', '@', '#', '?']
bImp = False
pilaTipos = []
tipos = ['sintipo', 'entero', 'decimal', 'logico', 'palabra']
tabSim = {'':[], 'x':['V','E','0',''], 'w':['V','E','0','20'],
      'MAX':['C','E','0','30'], 'vector':['V','E','30','']
}

matrans= [
#*  0     1    2     3      4    5     6     7     8     9     10    11    12   13     14   
#? let    _   dig   Opa     /    .     *     =     <     >     :   Delim   "    \n ,  esp
  [  1,   1,    2,    5,    6,  ERR,   10,   11,   12,   14,   17,   19,   20,    0,  ERR], #0
  [  1,   1,    1,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP], #1
  [ACP, ACP,    2,  ACP,  ACP,    3,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP], #2
  [ERR, ERR,    4,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR], #3
  [ACP, ACP,    4,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP], #4
  [ACP, ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP], #5
  [ACP, ACP,  ACP,  ACP,    7,  ACP,    8,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP], #6
  [  7,   7,    7,    7,    7,    7,    7,    7,    7,    7,    7,    7,    7,    0,    7], #7
  [  8,   8,    8,    8,    8,    8,    9,    8,    8,    8,    8,    8,    8,    8,    8], #8
  [  8,   8,    8,    8,    0,    8,    9,    8,    8,    8,    8,    8,    8,    8,    8], #9
  [ACP, ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP], #10
  [ACP, ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP], #11
  [ACP, ACP,  ACP,  ACP,  ACP,  ACP,  ACP,   13,  ERR,   16,  ACP,  ACP,  ACP,  ACP,  ACP], #12
  [ACP, ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP], #13
  [ACP, ACP,  ACP,  ACP,  ACP,  ACP,  ACP,   15,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP], #14
  [ACP, ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP], #15
  [ACP, ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP], #16
  [ACP, ACP,  ACP,  ACP,  ACP,  ACP,  ACP,   18,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP], #17
  [ACP, ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP], #18
  [ACP, ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP], #19
  [ 21,  21,   21,   21,   21,   21,   21,   21,   21,   21,   21,   21,   22,  ACP,   21], #20
  [ 21,  21,   21,   21,   21,   21,   21,   21,   21,   21,   21,   21,   22,   23,   21], #21
  [ACP, ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP,  ACP], #22
  [ERR, ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ACP]  #23
]

def colCar(x):
  if x.isalpha() or x in delu: return 0
  if x == '_'   : return 1
  if x.isdigit(): return 2
  if x in OPAS  : return 3
  if x == '/'   : return 4
  if x == '.'   : return 5
  if x == '*'   : return 6
  if x == '='   : return 7
  if x in '<'   : return 8
  if x in '>'   : return 9
  if x == ':'   : return 10
  if x in delim : return 11
  if x in '"'   : return 12
  if x in '\n'   : return 13
  if x in special: return 14

  if not(x in delu):
    print(x, 'is not a char or illegal symbol')
    return ERR

def insTabsim(nomb, valores):
  tabSim[nomb] = valores;

def getTabsim(nomb):
  return tabSim[nomb];

tabTipos = {'P:=P':'','E:=E':'','D:=E':'','D:=D':'', 'L:=L':'',
      'E+E':'E', 'D+E':'D','E+D':'D','P+P':'P',
      'E-E':'E', 'D-E':'D','E-D':'D',
      'E*E':'E', 'D*E':'D','E*D':'D',
      'E/E':'D', 'D/E':'D','E/D':'D','E'+"%"+'E':'E',
      'E^E':'D', 'D^E':'D','E^D':'D',
      '-E':'E', '-D':'D',
      'E<E':'L', 'D<E':'L','E<D':'','P<P':'L',
      'E>E':'L', 'D>E':'L','E>D':'','P>P':'L',
      'E<=E':'L', 'D<=E':'L','E<=D':'','P<=P':'L',
      'E>=E':'L', 'D>=E':'L','E>=D':'','P>=P':'L',
      'E<>E':'L', 'D<>E':'L','E<>D':'','P<>P':'L',
      'E=E':'L', 'D=E':'L','E=D':'','P=P':'L',
      'noL':'L', 'LyL':'L','LoL':'L'
}


def scanner():
  global entrance, matrans, ERR, ACP, idx, colm, rowg
  lexema = ''
  token = ''
  status = 0
  statusA = 0
  col = -1

  while idx < len(entrance) and status != ERR and status != ACP:
    while status == 7 and entrance[idx] != '\n':
      idx += 1
      colm += 1
    
    if status != 0 and (entrance[idx] in delu or ord(entrance[idx]) == 32):
      statusA = status
      status == 0
    
    else:
      while idx < len(entrance) and status == 0 and (entrance[idx] in delu or ord(entrance[idx]) == 32):
        if entrance[idx] == '\n':
          idx += 1
          rowg += 1
          colm = 1
        else:
          idx += 1
          colm += 1

    if idx >= len(entrance): break

    if status != ACP:
      c = entrance[idx]

      if c == '\n':
        rowg += 1
        idx += 1
        colm = 1
      else:
        idx += 1
        colm += 1

      col = colCar( c )

    if c in delu and status != 18:
      statusA = status
      status = ACP

    if col >= 0 and col <= 12 and col <= 13 and status != ACP and status != ERR:
      statusA = status

      if c in delu and status != 18: status = ACP
      status = matrans[status][col]

      if status == ACP: break
      if status != ERR:
        lexema += c

    else: status = ERR

    if status == 7 or status == 8 or status == 9: token = lexema = ''

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
  elif statusA == 12 or statusA == 13: token = 'Del'
  elif statusA == 15: token = 'OpS'
  elif statusA == 19: token = 'CtA'
  return token, lexema

#! Error Zone

def error(tipe, desc, obj):
  global rowg, colm, ERRA
  ERRA = True
  print('Linea:' + '['+ str(rowg) +']' + 'Columna:' + '[' + str(colm)+ '] Error de '+ tipe, desc, obj)

def params(): pass

def termino():
  global tok, lex
  if lex == '(':
    tok, lex = scanner()
    expr()
    if lex != ')':
      error('Error de sintaxis', 'se esperaba cerrar <)> y llego', lex)
    tok, lex = scanner()
  elif tok == 'CtA' or tok == 'CtL' or tok == 'Dec' or tok == 'Ent':
    tok, lex = scanner()
  elif tok == 'Ide':
    tok, lex = scanner()
    if lex == '[':
      udimen()
    elif lex == '(':
      callF()

def signo():
  global tok, lex
  op = ''
  if lex == '-':
    op == '-'
    tok, lex = scanner()
  termino()
    
def expo():
  global tok, lex
  op = '^'
  while op == '^':
    signo()
    op = lex
    
def multi():
  global tok, lex
  op = '*'
  while op == '*' or op == '/' or op == '%':
    if lex == '*' or lex == '/' or lex == '%':
      tok, lex = scanner()
    expo()
    op = lex
    
def suma():
  global tok, lex
  op = '+'
  while op == '+' or op == '-':
    if lex == '+' or lex == '-':
      tok, lex = scanner()
    multi()
    op = lex
    
def oprel():
  global tok, lex
  op = '<'
  while op == '<' or op == '>' or op == '=' or op == '<=' or op == '>=' or op == '<>':
    if lex == op:
      tok, lex = scanner()
    suma()
    op = lex
    
    
def opno():
  global tok, lex
  if lex == 'no':
    op = 'no'
    tok, lex = scanner()
  oprel()
    
def opy():
  global tok, lex
  op = 'y'
  while op == 'y':
    opno()
    op = lex

def expr():
  global tok, lex
  op = 'o'
  while op == 'o':
    if lex == 'o':
      tok, lex = scanner()
    opy()
    op = lex

def imprimes():
  global tok, lex, bImp
  tok, lex = scanner()
  if lex != '(':
    error('Error de Sintaxis', 'se esperaba <(> y llego ', lex)
  tok, lex = scanner()
  lx = ','
  while lx == ',':
    if lex == ',':
      tok, lex = scanner()
    expr()
    lx = lex

  if lex != ')':
    error('Error de Sintaxis', 'se esperaba <)> y llego ', lex)

  tok, lex = scanner()

def si():
  global tok, lex
  tok, lex = scanner()
  expr()

  if lex != 'hacer':
    error('Error de Sintaxis', 'se esperaba <hacer> y llego ', lex)

  tok, lex = scanner()
  block()
  if lex == 'sino':
    tok, lex = scanner()
    block()

def comando():
  global lex, tok, bImp
  if lex == 'imprimenl':
    bImp = True
  if lex == 'imprime' or bImp:
    imprimes()
  elif lex == 'si':
        si()
def estatutos():
  global tok, lex
  while lex != 'fin':
    if lex != ';':
      comando()
    if lex != ';':
      error('Error de Sintaxis', 'se esperaba <;> y llego', lex)
    tok, lex = scanner()

def constvars(): pass

def block():
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
  block()

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
                'Se esperaba <entero>, <decimal>, <logico>, <palabra> o <sintipo> y llego ', lex)

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

#* Main Zone
if __name__ == '__main__':
  archE = ''
  print(archE[len(archE)-3:])
  while (archE[len(archE)-3:] != 'icc'):
    archE = input('Archivo a compilar (*.icc) [.]=Salir: ')
    if archE == '.': exit(0)
    aEnt = None
    try:
      aEnt = open(archE, 'r+')
      break
    except FileNotFoundError:
      print(archE, 'No exite volver a intentar')
  
  if aEnt != None:
    while (linea := aEnt.readline()):
      entrance += linea
    aEnt.close()

  print('\n\n' + entrance + '\n\n')
  '''
  tok = lex = ''
  while (idx < len(entrada)):
    tok, lex = scanner()
    print(tok, lex)
    #if lex == ';': break

  exit(0) '''
  prgm();
  if NOPRINC: 
    error('Semantica', 'NO declaro la funcion <principal>', '')
  if ERRA == False:
    print(archE, "Compilo con exito!!!") 