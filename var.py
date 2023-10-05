entrada = ''
ERR = -1
ACP = 99
idx = 0
ERRA = False
NOPRINC = True
reng = 1
colm = 1
bImp = False
esp = ['!', '$', '@', '#', '?']
matran= [
  #let    _   dig Opa /   .       *   Del  :   =   <   "  esp
  [1,     1,  2,  5,  6,  11,     10, 11,  12, 14, 15, 18, ERR], #0
  [1,     1,  1,  ACP,ACP,ACP,    ACP,ACP, ACP,ACP,ACP,ACP,ACP], #1
  [ACP,   ACP,2,  ACP,ACP,3,      ACP,ACP, ACP,ACP,ACP,ACP,ACP], #2
  [ERR,   ERR,4,  ERR,ERR,ERR,    ERR,ERR, ERR,ERR,ERR,ERR,ERR], #3
  [ACP,   ACP,4,  ACP,ACP,ACP,    ACP,ACP, ACP,ACP,ACP,ACP,ACP], #4
  [ACP,   ACP,ACP,ACP,ACP,ACP,    ACP,ACP, ACP,ACP,ACP,ACP,ACP], #5
  [ACP,   ACP,ACP,ACP,7,  ACP,    8,  ACP, ACP,ACP,ACP,ACP,ACP], #6
  [7,     7,  7,  7,  7,  7,      7,  7,   7,  7,  7,  7,  7  ], #7
  [8,     8,  8,  8,  8,  8,      9,  8,   8,  8,  8,  8,  8  ], #8
  [8,     8,  8,  8,  0,  8,      9,  8,   8,  8,  8,  8,  8  ], #9
  [ACP,   ACP,ACP,ACP,ACP,ACP,    ACP,ACP, ACP,ACP,ACP,ACP,ACP], #10
  [ACP,   ACP,ACP,ACP,ACP,ACP,    ACP,ACP, ACP,ACP,ACP,ACP,ACP], #11
  [ACP,   ACP,ACP,ACP,ACP,ACP,    ACP,ACP, ACP,13, ACP,ACP,ACP], #12
  [ACP,   ACP,ACP,ACP,ACP,ACP,    ACP,ACP, ACP,ACP,ACP,ACP,ACP], #13
  [ACP,   ACP,ACP,ACP,ACP,ACP,    ACP,ACP, ACP,ACP,ACP,ACP,ACP], #14
  [ACP,   ACP,ACP,ACP,ACP,ACP,    ACP,ACP, ACP,16, ACP,ACP,ACP], #15
  [ACP,   ACP,ACP,ACP,ACP,ACP,    ACP,ACP, ACP,ACP,ACP,ACP,ACP], #16
  [ACP,   ACP,ACP,ACP,ACP,ACP,    ACP,ACP, ACP,ACP,ACP,ACP,ACP], #17
  [18,    18, 18, 18, 18, 18,     18, 18,  18, 18, 18, 19, 18 ], #18
  [ACP,   ACP,ACP,ACP,ACP,ACP,    ACP,ACP, ACP,ACP,ACP,ACP,ACP] #19
]
opas = ['+', '-', '^', '%']
delu = ['\n', '\t', chr(32)]
keyword = ['constante', 'entero', 'decimal', 'logico', 'palabra', 'sintipo', 
      'inicio', 'fin', 'si', 'sino', 'hacer', 'desde', 'hasta', 'incr', 
      'decr', 'regresa', 'imprime', 'imprimenl', 'lee', 
      'interrumpe', 'continua']
opl = ['no', 'y', 'o']
ctl = ['verdadero', 'falso']
delim = ['.', ',', ';', '(', ')', '[', ']']

def colCar(x):
  if x.isalpha() or x in delu: return 0
  if x == '_'   : return 1
  if x.isdigit(): return 2
  if x in opas  : return 3
  if x == '/'   : return 4
  if x == '.'   : return 5
  if x == '*'   : return 6
  if x in delim : return 7
  if x == ':'   : return 8
  if x == '='   : return 9
  if x == '<'   : return 10
  if x == '"'   : return 11
  if x in esp   : return 12
  if not(x in delu):
    print('Simbolo NO valido en el Lenguaje', x)
    return ERR

def scanner():
  global entrada, matran, ERR, ACP, idx, colm, reng
  lexema = ''
  token  = ''
  estado = 0
  estA = 0
  col = -1
  while idx < len(entrada) and estado != ERR and estado != ACP:
    while estado == 7 and entrada[idx] !='\n':
      idx += 1
      colm += 1
    if estado != 0 and (entrada[idx] in delu 
        or ord(entrada[idx]) == 32):
        estA = estado
        estado == 0
    else:
      while idx < len(entrada) and estado == 0 \
          and (entrada[idx] in delu or ord(entrada[idx]) == 32): 
          if entrada[idx] == '\n':
            idx += 1
            reng += 1
            colm = 1
          else:
            idx += 1
            colm += 1

    if idx >= len(entrada): break
    if estado != ACP:
      c = entrada[idx]
      if c == '\n': 
        reng += 1
        idx +=1
        colm = 1
      else:
        idx += 1
        colm += 1
      col = colCar( c )
    
    if c in delu and estado != 18: 
      estA = estado
      estado = ACP
    
    if col >= 0 and col <= 12 and estado != ACP and estado != ERR:
      estA = estado
      if c in delu and estado != 18: estado = ACP
      estado = matran[estado][col]
      if estado == ACP: break
      if estado != ERR:
        lexema += c
    else: estado = ERR

    if estado == 7 or estado == 8 or estado == 9: token = lexema= ''

  #fin del while
  
  if estado == ERR or estado == ACP: idx -= 1
  else: estA = estado

  if estA == 1: 
    token = 'Ide' 
    if lexema in keyword: token = 'Res'
    elif lexema in opl  : token = 'OpL'
    elif lexema in ctl  : token = 'CtL'  
  elif estA == 2: token = 'Ent'
  elif estA == 4: token = 'Dec'
  elif estA in [5, 6, 10]: token = 'OpA'
  elif estA == 11 or estA == 12: token = 'Del'
  elif estA == 13: token = 'OpS'
  elif estA == 19: token = 'CtA'
  return token, lexema

def error(tipe, desc, obj):
  global reng, colm, ERRA
  ERRA = True
  print('['+ str(reng) +'][' + str(colm)+ '] Error de '+ tipe, desc, obj)

def params(): pass

def constvars(): pass

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

def estatutos(): 
  global tok, lex
  while lex != 'fin':
    if lex != ';':
      comando()
    if lex != ';':
      error('Error de Sintaxis', 'se esperaba <;> y llego', lex)
    tok, lex = scanner()
    

def bloque(): 
  global tok, lex
  if lex != 'inicio':
    error('Error de Sintaxis', 'se esperaba <inicio> y llego ', lex)
  tok, lex = scanner()
  if lex != 'fin':
    constvars()
  if lex != 'fin':
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
  while (lex == 'constante' or lex == 'entero' or lex =='decimal' or \
      lex == 'palabra' or lex == 'logico' or \
      lex == 'sintipo') and idx < len(entrada):

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
        if tok == 'Ide'   : idf = lex
        else:
          error('Sintaxis', 'Se esperaba <Ide> y llego ', tok)
        tok, lex = scanner()
        if lex == '(': 
          funcParcial()
        else: 
          constvars()

#fin de prgm

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
      entrada += linea
    aEnt.close()

  print('\n\n' + entrada + '\n\n')
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