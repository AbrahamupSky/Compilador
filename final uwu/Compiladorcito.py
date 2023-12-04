"""
Josue Israel Reyes Díaz - 220331747
Abraham Urrutia - 220331658
"""

entrada = ''
ERR = -1
ACP = 99
idx = 0
ERRA = False
NOPRINC = True
reng = 1
colm = 1
prgma = []
conCod = 1

# ? -------------- Matriz --------------

matran= [
# ?  0    1    2     3     4     5     6    7     8     9     10    11    12    13    14   
# ?let    _   dig   Opa     /    .     *     =     <     >     :   Delim   "    \n ,  esp
  [  1,   1,    2,    5,    6,  ERR,   10,   11,   12,   14,   17,   19,   20,    0,  ERR] , #0
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
esp = ['!', '$', '@', '#', '?','¿','¡','&','|','°','¬']
opas = ['+', '-', '^', '%']
delu = ['\t', chr(32)]
keyword = ['constante', 'entero', 'decimal', 'logico', 'palabra', 'sintipo', \
            'inicio', 'fin', 'si', 'sino', 'hacer', 'desde', 'hasta', 'incr', \
            'decr', 'regresa', 'imprime', 'imprimenl', 'lee', \
            'interrumpe', 'continua']
tipos =['constante', 'entero', 'decimal', 'logico', 'palabra', 'sintipo']
keywordMap = {
  "sintipo": 'S',
  "entero" : "E",
  "decimal" :"D",
  "logico" : "L",
  "palabra": "P"
}

opl = ['no', 'y', 'o']
ctl = ['verdadero', 'falso']
delim = ['.', ';', '(', ')', '[', ']',',']
pilaTipos=[]
tabSim = {}

# ? -------------- Fin Lexico --------------

class codigo():
  def __init__(self, lin, mnmo, d1, d2):
    self.linea = lin
    self.mnemo = mnmo
    self.dir1 = d1
    self.dir2 = d2

tabTipos = {"P:=P":'',"E:=E":'',"D:=E":'',"D:=D":'',"L:=L":'',
            "E+E":'E',"D+E":'D',"E+D":'D',"D+D":'D',"P+P":'P',
            "E-E":'E',"D-E":'D',"E-D":'D',"D-D":'D',
            "E*E":'E',"D*E":'D',"E*D":'D',"D*D":'D',
            "E/E":'D',"D/E":'D',"E/D":'D',"D/D":'D',f"E{'%'}E":'E',
            "E^E":'D',"D^E:":'D',"E^D":'D',"D^D":'D',
            "-E":'E',"-D":'D',
            "E<E":'L',"D<E:":'L',"E<D":'L',"P<P":'L',
            "E<=E":'L',"D<=E:":'L',"E<=D":'L',"P<=P":'L',
            "E>E":'L',"D>E:":'L',"E>D":'L',"P>P":'L',
            "E>=E":'L',"D>=E:":'L',"E>=D":'L',"P>=P":'L',
            "E<>E":'L',"D<>E:":'L',"E<>D":'L',"P<>P":'L',
            "E=E":'L',"D=E:":'L',"E=D":'L',"P=P":'L',
            "noL":'L',"LyL":'L',"LoL":'L'
  }

nombre, clase, tipo, dimension, exprSol, valor, scope = "","","","","",'',''
hasMain = False
functName = ""

# ! -------------- Error Zone --------------

def error(tipe, desc, obj):
  global reng, colm, ERRA
  ERRA = True
  print('['+ str(reng) +'][' + str(colm)+ '] Error de '+ tipe, desc, obj)

# ! -------------- End Error Zone --------------

def colCar(x):
  if x.isalpha() or x in delu: return 0
  if x == '_'        : return 1
  if x.isdigit()     : return 2
  if x in opas       : return 3
  if x == '/'        : return 4
  if x == '.'        : return 5
  if x == '*'        : return 6
  if x == '='        : return 7
  if x == '<'        : return 8
  if x == '>'        : return 9
  if x == ':'        : return 10
  if x in delim      : return 11
  if x == '"'        : return 12
  if x == '\n'       : return 13
  if x in esp        : return 14
  else:
    print(ord(x), 'Simbolo NO valido en el Lenguaje')
    return ERR

# ? -------------- Scanner --------------

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
    while estado == 8 and entrada[idx] != "*":
      idx += 1
      colm += 1
    while estado == 9 and entrada[idx] !='/':
      idx +=1
      colm +=1
    if estado != 0 and (entrada[idx] in delu \
        or ord(entrada[idx]) == 32):
        if (estado == 21 or estado ==20 ) and ord(entrada[idx]) == 32: 
          idx+=1
          lexema += ' '
        else:
          estA = estado
          estado == ACP
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
    
    if c in delu and estado != 21: 
      estA = estado
      estado = ACP
    
    if col >= 0 and col <= 14 and estado != ACP and estado != ERR:
      estA = estado
      if c in delu and estado != 21: estado = ACP
      estado = matran[estado][col]
      if estado == ACP: break
      if estado != ERR and c != '\n':
        lexema += c
      if estA == 9:
        lexema = ""
    else: estado = ERR

    if estado == 7 or estado == 8 or estado == 9: token = lexema= ''
  
  if estado == ERR or estado == ACP: idx -= 1
  else: estA = estado

  if estA == 1: 
    if lexema in keyword: token = 'Res'
    elif lexema in opl  : token = 'OpL'
    elif lexema in ctl  : token = 'CtL'  
    else : token = 'Ide' 
  if estA == 2: token = 'Ent'
  if estA == 4: token = 'Dec'
  if estA in [5, 6, 10]: token = 'OpA'
  if estA in [11, 12, 13, 14, 15, 16]: token = 'OpR'
  if estA in [17, 19]: token = 'Del'
  if estA == 18: token = 'OpS'
  if estA == 20: token = 'Del'
  if estA == 22: token = 'CtP'


  return token, lexema

# ? -------------- Fin Scanner --------------

# ? -------------- Insertar a la Tabla de Simbolos --------------

def insTabSim():
  global tabSim, clase, tipo, dimension, valor, functName, scope
  functName = "insTabSim"
  tabSim[nombre + scope] = [clase, tipo, dimension, valor] 

# ? -------------- Fin Insertar a la Tabla de Simbolos --------------

def despilar():
  global pilaTipos, tabSim, functName
  functName = "despilar"
  while len(pilaTipos) > 0:
    print(pilaTipos)
    if len(pilaTipos) <= 1 and pilaTipos[0] in ['L','E','D','P','']:
      break
    elif len(pilaTipos) <= 1:
      error('Error de Semantica','Valor Indefinido:',pilaTipos[0])
    
    td = pilaTipos.pop()
    opr = pilaTipos[-1]
    if opr == '(':  break
    pilaTipos.pop()
    ti = pilaTipos.pop()
    vtipo = ti + opr + td
    try:
      tr = tabTipos[vtipo]
      pilaTipos.append(tr)
    except:
      error('Error de Semantica','Error de Operaciones, operacion invalid:',vtipo)

def vaciarTabSim():
  global clase, tipo, dimension, valor
  clase, tipo, dimension, valor = '', '', '0', ''

def avanzar():
  global tok ,lex, functName,scope
  tok, lex = scanner()
  print(f">>{functName}   :{scope}:  tok -- {tok}      lex -- {lex}     pilaTipos -- {pilaTipos}")

# ? -------------- Constantes que entran al codigo - Expresion --------------

def termino():
  global tok, lex, op, dimension, pilaTipos, tabSim, nombre, functName,conCod
  functName = "termino"
  if lex == '(':
    pilaTipos.append(lex)
    expr()
    
    if lex != ')':
      error('Error de sintaxis', 'se esperaba cerrar <)> y llego', lex)
      
  elif tok in ['CtP','CtL','Dec','Ent'] : 
    if tok == 'CtP': 
      pilaTipos.append('P')
      x = codigo(str(conCod), 'LIT', lex, '0')
      conCod += 1
      prgma.append(x)
    elif tok == 'CtL': 
      if lex == 'verdadero':
        pilaTipos.append('L')
        x = codigo(str(conCod), 'LIT', 'V', '0')
        conCod += 1
        prgma.append(x)
      if lex == 'falso':
        pilaTipos.append('L')
        x = codigo(str(conCod), 'LIT', 'F', '0')
        conCod += 1
        prgma.append(x)
    elif tok == 'Dec': 
      pilaTipos.append('D')
      x = codigo(str(conCod), 'LIT', lex, '0')
      conCod += 1
      prgma.append(x)
    elif tok == 'Ent': 
      pilaTipos.append('E')
      x = codigo(str(conCod), 'LIT', lex, '0')
      conCod += 1
      prgma.append(x)
    avanzar()
  elif tok == 'Ide':
    try:
      pilaTipos.append(tabSim[lex+scope][1])
    except KeyError:
      try:
        pilaTipos.append(tabSim[lex][1])
      except:
        error('Semantico', 'Variable No Inicializada', lex)
    nombre = lex
    avanzar()

    if lex == '[':
      pilaTipos.append('(')
      avanzar()
      expr()
      
      if lex != ']':
        error('Error de sintaxis', 'se esperaba cerrar <)> y llego', lex)
      avanzar()
    elif lex == '(': 
      funct()

# ? -------------- Fin Expresion e Inicio menos unitario --------------

def signo():
  global tok, lex, op, pilaTipos, functName,conCod
  functName = "signo"
  op = ''
  if lex == '-':
    op == '-'
    avanzar()
  termino()
  if op == '-':
    x = codigo(str(conCod), 'OPR', '0', '8')
    conCod += 1
    prgma.append(x)

# ? -------------- Fin menos unitario --------------

# ! -------------- Inicio de los operadores aritmeticos/logicos --------------
    
def expo():
  global tok, lex, op, functName, conCod
  functName = "expo"
  op = '^'
  while op == '^':
    signo()
    op = lex
    if op == "^":
      x = codigo(str(conCod), 'OPR', '0', '7')
      conCod += 1
      prgma.append(x)
    
def multi():
  global tok, lex, op, tr, functName, conCod
  functName = "multi"
  op = '*'
  while op == '*' or op == '/' or op == '%':
    if lex == '*' or lex == '/' or lex == '%':
      pilaTipos.append(lex)
      avanzar()
    expo()
    op = lex
      
    if op == '*' or op == '/' or op == '%':
      op = lex
      if lex == "*": x = codigo(str(conCod), 'OPR', '0', '4')
      if lex == "/": x = codigo(str(conCod), 'OPR', '0', '5')
      if lex == "%": x = codigo(str(conCod), 'OPR', '0', '6')
      
      conCod += 1
      prgma.append(x)

def suma():
  global tok, lex, op, functName, conCod
  functName = "suma"
  op = '+'
  while op == '+' or op == '-':
    if lex == '+' or lex == '-':
      pilaTipos.append(lex)
      avanzar()
      
    multi()
    
    if op == '+' or op == '-':
      op = lex
      if lex == "+": x = codigo(str(conCod), 'OPR', '0', '2')
      if lex == "-": x = codigo(str(conCod), 'OPR', '0', '3')
      conCod += 1
      prgma.append(x)
      
    
def opRel():
  global tok, lex, op, functName, conCod
  functName = "opRel"
  op = '<'
  while op == '<' or op == '>' or op == '=' or op == '<=' or op == '>=' or op == '<>':
    if lex == op:
      avanzar()
    suma()
    op = lex
    if op == '<' or op == '>' or op == '=' or op == '<=' or op == '>=' or op == '<>':
      print(pilaTipos)
      if lex == "<": x = codigo(str(conCod), 'OPR', '0', '9')
      if lex == ">": x = codigo(str(conCod), 'OPR', '0', '10')
      if lex == "<=": x = codigo(str(conCod), 'OPR', '0', '11')
      if lex == ">=": x = codigo(str(conCod), 'OPR', '0', '12')
      if lex == "<>": x = codigo(str(conCod), 'OPR', '0', '13')
      if lex == "=": x = codigo(str(conCod), 'OPR', '0', '14')
      conCod += 1
      prgma.append(x)
      
      pilaTipos.append(op)
    
def opNo():
  global tok, lex, op, functName
  functName = "opNo"
  if lex == 'no':
    op = 'no'
    avanzar()
  opRel()
    
def opY():
  global tok, lex, op, functName, conCod
  functName = "opY"
  op = 'y'
  while op == 'y':
    opNo()
    op = lex
    if op == "y": 
      x = codigo(str(conCod), 'OPR', '0', '16')
      conCod += 1
      prgma.append(x)
    
def expr():
  global tok, lex, op, dimension, pilaTipos, functName, exprSol, conCod
  functName = "expr"
  op = 'o'
  while op == 'o':
    if lex == 'o':
      avanzar()
    opY()
    op = lex
    if op in opl:
      if op == "o":
        x = codigo(str(conCod), 'OPR', '0', '15')
        conCod += 1
        prgma.append(x)
      despilar()
      pilaTipos.append(op)
  despilar()
  exprSol = pilaTipos.pop()

# ! -------------- Inicio de los operadores aritmeticos/logicos --------------
  
def dime():
  global tok, lex, nombre, dimension, valor, tabSim, functName
  functName = "dime"
  
  dimension = '1'
  if lex == '[':
    avanzar()
    temp = nombre
    expr()
    nombre = temp
    if exprSol != 'E':
      error('Error de Semantica','Dimension Invalido',exprSol)

    if lex == ']':
      valor = "['0']"
      avanzar()
    else:
      error('Error de Sintaxis', 'se esperaba <cerrar corchete ] > y llego', lex)

# ! -------------- Bloque interno y externo --------------

def miniBlock():
  global nombre, keyword, functName
  functName = "miniBlock"
  if tok =="Ide":
    nombre=lex
    asigna()
  elif lex in keyword:
    estatuto()
  else:
    error("error de sintaxis", "NO le sabes ",lex)

# ! -------------- Fin Bloque interno inicio 'bloque' --------------
    
def bloque():
  global tipos, tok, lex, clase, keywordMap, tipo, nombre, scope, functName
  functName = "bloque"
  avanzar()
  while lex != 'fin':
    if lex == 'constante':
      avanzar()
      if lex not in tipos: error("Error de Semantica","Tipo Invalido",lex)
      else:
        clase = 'C'
        tipo = keywordMap[lex]
        avanzar()
        nombre = lex
        avanzar()
        constVar()
    elif lex in tipos:
      tipo = keywordMap[lex]
      avanzar()
      nombre = lex
      constVar()
    elif lex in keyword:
      estatuto()
    else:
      avanzar()
  avanzar()
  nombre = ''
      
# ! -------------- Fin Bloque --------------
    
def asigna():
  global nombre, valor, functName, scope
  functName="asigna"
  
  if tok == "Ide":
    avanzar()
    if lex == '[':
      dime()
  
  if lex != ":=": error("Error de Semantica", "Se Esperaba < := > y llego", lex)
  else:
    avanzar()
    expr()
    try:
      tabSim[nombre+scope][3] = '1'
    except KeyError:
      error("Error de Semantica", "Accesso a Vector Invalido", lex)

def imprime():
  global tok, lex, functName,conCod,prgma
  functName = "imprime"
  if lex == "(":
    expr()
  avanzar()
  while lex != ')':
    avanzar()
    expr()
    if lex == ",":
      x = codigo(str(conCod), 'OPR', '0', '20')
      conCod += 1
      prgma.append(x)
  avanzar()
  if lex != ";": error("Error de Sintaxis", "Se Esperaba < , > y llego", lex)
  else:
    x = codigo(str(conCod), 'OPR', '0', '20')
    conCod += 1
    prgma.append(x)

# TODO: -------------- 'if' en Coronaguaje --------------

def si(): 
  global tok, lex, functName
  functName = "si"
  avanzar()
  expr()
  if lex != "hacer":
    error("Error de Sintaxis", "Se esperaba < hacer > y llego", lex)
  else:
    avanzar()
    if lex == 'inicio': bloque()
    else: estatuto()
  avanzar()
  if lex == "sino":
    bloque()
    avanzar()
  
# TODO: -------------- Fin 'if' --------------

# ? -------------- Asgina en 'desde' --------------

def dobleMiniVar():
  global clase, dimension, tipo, nombre, valor
  clase, dimension, tipo = "V", '0', 'E'
  avanzar()
  if lex != ':=': error("Error de Sintaxis","Estas Mal chavo >:(",lex)
  avanzar()
  expr()
  if exprSol == 'E':
    valor = ''
    insTabSim()
  else: error('Error de Sintaxis','Desde solo Acepta Enteros y llego',exprSol)
  
# TODO: -------------- 'for' en Coronaguaje --------------

def desde():
  global tok, lex, functName, nombre,scope
  functName = "desde"
  avanzar()
  nombre = lex
  dobleMiniVar()
  if lex != "hasta": error("Error de Sintaxis", "Se Esperaba < hasta > y llego", lex)
  else:
    avanzar()
    expr()
    if lex != "incr" and lex != "decr": pass
    else:
      if lex == "incr":avanzar()
      elif lex == "decr" :avanzar()
      expr()
    if lex == "inicio": bloque()
    else: miniBlock()

# TODO: -------------- Fin 'for' y 'return' en Coronaguaje --------------

def regresa():
  global functName
  functName = "regresa"
  avanzar()
  expr()
  avanzar()

# TODO: -------------- Fin 'return' en Coronaguaje --------------

def imprimeL(): 
  global tok, lex, functName,conCod
  functName = "imprimeL"
  if lex == "(":
    expr()
  avanzar()
  while lex != ')':
    avanzar()
    expr()
    if lex == ",": 
      x = codigo(str(conCod), 'OPR', '0', '20')
      conCod += 1
      prgma.append(x)
  avanzar()
  if lex != ";": error("Error de Sintaxis", "Se Esperaba < , > y llego", lex)
  else:
    x = codigo(str(conCod), 'OPR', '0', '21')
    conCod += 1
    prgma.append(x)
    
def interrumpe():
  global functName, conCod
  functName = "interrumpa"
  x = codigo(str(conCod), 'OPR', '0', '1')
  conCod += 1
  prgma.append(x)
  avanzar()
  
def continua(): 
  global functName, conCod
  functName = "continua"
  
  avanzar()
  
def lee(): 
  global functName, conCod, nombre, tabSim, scope
  functName = "lee"
  avanzar()
  
  if tok == "ide":
    try:
      tabSim[nombre + scope]
      x = codigo(str(conCod), 'OPR', '0', '19')
      conCod += 1
      prgma.append(x)
      x = codigo(str(conCod), 'STO', '0', nombre+scope)
      conCod += 1
      prgma.append(x)
    except:
      try:
        tabSim[nombre]
        x = codigo(str(conCod), 'OPR', '0', '19')
        conCod += 1
        prgma.append(x)
        x = codigo(str(conCod), 'STO', '0', nombre)
        conCod += 1
        prgma.append(x)
      except:
        error("Error de Semantica", "Variable Invalida", lex)
      
    avanzar()
    if lex == '[':
      dime()

def lmp():
  global functName,conCod
  functName = "lmp"
  x = codigo(str(conCod), 'OPR', '0', '18')
  conCod += 1
  prgma.append(x)
  avanzar()

mapaComandos = {
  'si': si,  
  'lee': lee,
  'lmp' : lmp,
  'desde': desde, 
  'regresa': regresa, 
  'imprime': imprime, 
  'imprimenl': imprimeL, 
  'continua' : continua,
  'interrumpe': interrumpe, 
}    

def estatuto():
  global functName
  functName = "estatuto"
  try:
    mapaComandos[lex]()
  except KeyError:
    error("Error de Sintaxis", "Comando Invalido", lex)
    avanzar()
    
# ? -------------- Para los parametros de las funciones --------------

def miniVar():
  global tipo, scope, nombre, valor, dimension, clase, functName
  functName = "miniVar"
  valor, dimension = '','0'
  clase = 'P'
  try:
    tipo = keywordMap[lex]
  except:
    error('Error de Sintaxis', 'Se esperaba tipo de data y llego', lex)
  avanzar()
  if tok == 'Ide': nombre = lex
  else: error('Error de Sintaxis', 'Qualificador Invalido', lex) 
  insTabSim()
  vaciarTabSim()
  avanzar()     

# ? -------------- Fin parametros de las funciones - Inicio de los parametros --------------

def params():
  global functName
  functName = "params"
  avanzar()
  while lex != ')':
    miniVar()
    if lex == ',':
      avanzar()
  avanzar()

def paramsExpr():
  global functName
  functName = "paramsExpr"
  avanzar()
  while lex != ')':
    expr()
    if lex == ',':
      avanzar()
  avanzar()

# ? -------------- Fin de los parametros - Inicio 'funcion()' en Coronaguaje --------------
  
def funct():
  global dimension, clase, pilaTipos, valor, tabSim, functName, tipo
  functName = "funct"
  try:
    tabSim[nombre]
    pilaTipos.append('(')
    paramsExpr()
  except:
    dimension, clase, valor = '0','F',''
    tabSim[nombre] = [clase, tipo, dimension, valor]
    params()
    if lex == 'inicio':
      bloque()
    else:
      estatuto()

# ? -------------- Fin de la 'funcion()' --------------
  
def constVar():
  global tok, lex, clase, tipo, valor, dimension,nombre, functName
  functName = "constVar"
  if clase == "C":
    dimension = '0'
    if lex == ":=":                 
      avanzar()
      valor = lex
      insTabSim()
      avanzar()
    else:
      error("Error de Sintaxis", "se esperaba < := > y llego", lex)
    if lex == ',':
      while lex != ';':
        avanzar()
        if tok == "Ide":
          nombre = lex
        else: error("Error de Sintaxis", "Se Esperaba un identificador y llego:", lex)
        avanzar()
        if lex == ":=":                 
          avanzar()
          valor = lex
          insTabSim()
        else:
          error("Error de Sintaxis", "se esperaba < := > y llego", lex)
        avanzar()
    if lex != ";":
      error("Error de Sintaxis", "se esperaba < ; > y llego", lex)
    else: avanzar()
    clase = ''
  # ? variables y funciones
  else:
    clase = "V"
    if tok == "Ide" :
      nombre = lex 
      avanzar()
    if lex == "[": 
      dime()
      insTabSim()
    elif lex == ":=":
      dimension = '0'
      avanzar()
      valor = lex 
      insTabSim()
      avanzar()
    elif lex == ",":
      valor = ""
      insTabSim()
    else:
      valor = ''
      insTabSim()
      
    if lex == ',': 
      avanzar()
      while lex != ';':
        if tok == 'Ide': nombre = lex
        else:error("Error de Sintaxis", "se esperaba <Ide>: ", lex)
        avanzar()
        if lex == "[": dime()
        elif lex == ":=":
          avanzar()
          valor = lex 
          insTabSim()
          avanzar()
        elif lex == ",":
          valor = ""
          insTabSim()
          avanzar()
        elif lex == ';':
          valor = ''
          insTabSim()
        
        if lex == ',': 
          avanzar()
        
    if lex != ';':
      error("Error de Sintaxis", "se esperaba <;>: ", lex)       
    else:
      avanzar()
      vaciarTabSim()

# ? -------------- Ciclo principal del Compilador --------------

def programa():
  global tok, lex, clase, tipo, nombre, scope, functName, hasMain, NOPRINC, conCod
  functName = "programa"
  avanzar()
  while ((lex in tipos) or lex == 'constante') and idx < len(entrada):
    if lex == "constante": 
      clase = "C"
      avanzar()
    try:
      tipo = keywordMap[lex]
    except KeyError:
      error("Error de Sintaxis", "se esperapa <tipo de dato>: ", lex)
    avanzar()
  
    if tok == "Ide": 
      nombre = lex
    else: error("Error de Sintaxis", "Se Esperaba un identificador y llego:", lex)
    avanzar()
    if nombre == 'principal':
      scope = '$_P'
      nombre = "_P"
      NOPRINC = False
      hasMain = True
      funct()  
      x = codigo(str(conCod), "OPR", "0", "0")
      conCod += 1
      prgma.append(x)
    elif lex =="(":
      scope = "$" + nombre + '$' + tipo
      funct() 
    else: 
      constVar()
    scope = ''
      
  if not hasMain:
    error("Error de Sintaxis","No Contiene Funcion Principal", lex)

# ? -------------- Fin Ciclo principal del Compilador --------------

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
  programa()
  if NOPRINC: 
    error('Semantica', 'NO declaro la funcion <principal>', '')
    
  if ERRA == False:
    archS = archE[0:len(archE)-3] + 'eje'
    try:
      print(archS)
      with open(archS, 'w') as aSal:
        for x, y in tabSim.items():
          aSal.write(x + ',')
          aSal.write(y[0]+',')
          aSal.write(y[1]+',')
          aSal.write(y[2]+',')
          aSal.write(y[3]+',')
          aSal.write('#,\n')
        aSal.write('@\n')
        for x in prgma:
          aSal.write(x.linea + ' ')
          aSal.write(x.mnemo + ' ')
          aSal.write(x.dir1  + ', ')
          aSal.write(x.dir2  + '\n')
      aSal.close()

    except FileNotFoundError:
      print(archE, 'No exite volver a intentar')
  
  if not ERRA: print("Exit Success!!")
