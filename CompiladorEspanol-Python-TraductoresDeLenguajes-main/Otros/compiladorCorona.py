import os
ERR = -1
ACP = 99
idx = 0
cERR = False
tok = ''
lex = ''
bPrinc = False
ren = 1
colu = 0
pTipos = []

cTipo = ["E=E", "P=P", "D=D", "L=L", "D=E",
        "E+E", "E+D", "D+E", "D+D", "P=P",
        "E-E", "E-D", "D-E", "D-D",
        "E*E", "E*D", "D*E", "D*D",
        "E/E", "E/D", "D/E", "D/D",
        "E%E", "-E", "-D",
        "LyL", "LoL", "noL",
        "E>E", "D>E", "E>D", "D>D",
        "E<E", "D<E", "E<D", "D<D",
        "E>=E", "D>=E", "E>=D", "D>=D",
        "E<=E", "D<=E", "E<=D", "D<=D",
        "E<>E", "D<>E", "E<>D", "D<>D", "P<>P",
        "E==E", "D==E", "E==D", "D==D", "P==P"
]

tipoR = ["",  "",  "",  "",  "",
        "E", "D", "D", "D", "P",
        "E", "D", "D", "D",
        "E", "D", "D", "D",
        "D", "D", "D", "D",
        "E", "E", "D",
        "L", "L", "L",
        "L", "L", "L", "L",
        "L", "L", "L", "L",
        "L", "L", "L", "L",
        "L", "L", "L", "L",
        "L", "L", "L", "L", "L",
        "L", "L", "L", "L", "L"
]


def buscaTipo(cadt):
    for i in range(len(cTipo)):
        if cTipo[i]==cadt: return i
    return -1


class objPrgm():
    def _init_(self, nom, cls, tip, dim1, dim2, apv) -> None:
        self.dim2apv = []
        self.apv = ["0" for i in range(1000)]
        self.nombre = nom
        self.clase = cls
        self.tipo = tip
        self.dim1 = dim1
        self.dim2 = dim2
        self.apv[int(dim1)] = apv
        return


class TabSimb():
    arreglo = []
    def inserSimbolo(self, nom, cls, tip, dim1, dim2, apv):
        ox = self.buscaSimbolo(nom)
        if ox != None:
            if ox.clase == 'V': cls = 'Variable'
            elif ox.clase == 'C': cls = 'Constante'
            elif ox.clase == 'F': cls = 'Funcion'
            elif ox.clase == 'I': cls = 'Indefinido'
            elif ox.clase == 'L': cls = 'Variable Local'
            if ox.tipo == 'E': tp = 'Entero'
            elif ox.tipo == 'D': tp = 'Decimal'
            elif ox.tipo == 'P': tp = 'Palabra'
            elif ox.tipo == 'I': tp = 'Nulo o Indefinido'
            elif ox.tipo == 'L': tp = 'Logico'
            erra('Error Semantico ' + nom + ' ya esta declarado como', cls + ' del tipo ' + tp)
            return
        obj = objPrgm(nom, cls, tip, dim1, dim2, apv)
        self.arreglo.append( obj )
        return

    def buscaSimbolo(self, ide):
        for x in self.arreglo:
            if x.nombre == ide: return x
        return None
    
    def grabaTabla(self, archSal):
        with open(archSal, 'w') as aSal:
            for x in self.arreglo:
                aSal.write(x.nombre +',' + x.clase + ',' + x.tipo + ',' + \
                           x.dim1 + ','+ x.dim2 + ',' + x.apv[0] + ',#\n')
            aSal.write('@\n')
            aSal.close()
        return
    
    def impTabSim(self):
        for x in self.arreglo:
            print(x.nombre + ',' + x.clase + ',' + x.tipo + ',' + x.dim1 + ',' + x.dim2 + ',' + x.apv[0]+ ',#')
        print('@')
        return


class codigo():
    def _init_(self, mnem, dir1, dir2):
        self.mnemo = mnem
        self.dir1 = dir1
        self.dir2 = dir2


linCod = 0


class Programa():
    cod = []
    def _init_(self):
        for i in range(10000):
            x = codigo('LIT', '0', '0')
            self.cod.append(x)
        return

    def insCodigo(self, mnemo, dir1, dir2):
        global linCod
        linCod = linCod + 1
        x = codigo(mnemo, dir1, dir2)
        self.cod[linCod] = x
        return
    
    def impCodigo(self):
        global linCod
        for i in range(linCod + 1):
           if i > 0:
              x = self.cod[i]
              print(str(i)+ ' '+x.mnemo + ' ' + x.dir1 + ', ' + x.dir2)
        return

    def grabaCodigo(self, archSal):
        global linCod
        with open(archSal, 'r') as aSal:
            if aSal == None: return 

        if linCod > 0:
            with open(archSal, 'a') as aSal:
                for i in range(linCod + 1):
                    if i > 0:
                        x = self.cod[i]
                        aSal.write(str(i)+ ' ' + x.mnemo + ' ' + x.dir1 + ',' + x.dir2 + '\n')

            aSal.close()
        return


tabSimb = TabSimb()  


prgmCod = Programa()


pilaTipos = []


def erra(terr, desc):
    global ren, colu
    global cERR
    print('['+str(ren)+']'+'['+str(colu)+']', terr, desc)
    cERR = True


matran=[
    #let  dig  del  opa   <    >    =    .    "
    [1,   2,   6,   5,    10,  8,   7,  ERR,  12], #0
    [1,   1,   ACP, ACP, ACP, ACP, ACP, ACP, ACP], #1
    [ACP, 2,   ACP, ACP, ACP, ACP, ACP,  3,  ACP], #2
    [ERR, 4,   ERR, ERR, ERR, ERR, ERR, ERR, ERR], #3
    [ACP, 4,   ACP, ACP, ACP, ACP, ACP, ACP, ACP], #4
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP], #5
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP], #6
    [ACP, ACP, ACP, ACP, ACP, ACP,  9,  ACP, ACP], #7
    [ACP, ACP, ACP, ACP, ACP, ACP,  9,  ACP, ACP], #8
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP], #9
    [ACP, ACP, ACP, ACP, ACP, 11,    9, ACP, ACP], #10
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP], #11
    [12,   12,  12,  12,  12,  12,  12,  12,  13], #12
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP]  #13
]


tipo = ['nulo', 'entero', 'decimal', 'palabra', 'logico']
opl = ['no', 'y', 'o']
ctl= ['verdadero', 'falso']
key= ['constante', 'desde', 'si', 'hasta', 'mientras', 'entero', 'decimal', 'regresa', 'hacer',
      'palabra', 'logico', 'nulo', 'sino', 'incr' 'imprime', 'imprimenl', 'lee', 'repite', 'que']
opar=['+', '-', '*', '/', '%', '^']
deli=[';', ',', '(',')', '{', '}', '[', ']', ':']
delu=[' ', '\t', '\n']
opRl = ['<', '>', '<=', '>=', '<>']
tkCts = ['Ent', 'Dec', 'CtA', 'CtL']
entrada = ''


def colCar(x):
    if x == '_' or x.isalpha(): return 0 
    if x.isdigit(): return 1
    if x in deli: return 2
    if x in opar: return 3
    if x == '<': return 4   
    if x == '>': return 5   
    if x == '=': return 6   
    if x == '.': return 7
    if x == '"': return 8
    if x in delu: return 15
    erra('Error Lexico', x + ' simbolo no valido en Alfabeto')
    return ERR


def scanner():
    global entrada, ERR, ACP, idx, ren, colu
    estado = 0
    lexema = ''
    c = ''
    col = 0
    while idx < len(entrada) and \
          estado != ERR and estado != ACP: 
          c = entrada[idx]
          idx = idx + 1
          if c == '\n':
              colu = 0
              ren = ren + 1

          col = colCar(c)
          if estado == 0 and col == 15: 
            continue;
          if col >= 0 and col <= 8 or col == 15:
            if col == 15 and estado != 12: 
                estado = ACP
            if col >=0 and col <= 8:
                estado = matran[estado][col]
            if estado != ERR and estado != ACP and col != 15 or col == 15 and estado == 12:
                estA = estado
                lexema = lexema + c
            
            if c != '\n': colu = colu + 1

    if estado != ACP and estado != ERR: estA = estado;
    token = 'Ntk'
    if estado == ACP and col != 15: 
        idx = idx - 1
        colu = colu - 1

    if estado != ERR and estado != ACP:
        estA = estado
    
    if lexema in key: token = 'Res'
    elif lexema in opl: token = 'OpL'
    elif lexema in ctl: token = 'CtL'
    else: token = 'Ide'

    if estA == 2: token = 'Ent'
    elif estA == 4: token = 'Dec'
    elif estA == 5: token = 'OpA'
    elif estA == 6: token = 'Del'
    elif estA == 7: token = 'OpS'
    elif estA in [8, 9 , 10 , 11]: token = 'OpR'
    elif estA == 13: token = 'CtA'

    if token == 'Ntk':
        print('estA=', estA, 'estado=', estado)

    return token, lexema


def cte():
    global tok, lex, prgmCod, pilaTipos, tabSimb
    if not(tok in tkCts):
        erra('Error de sintaxis', 'se esperaba Cte y llego '+ lex) 
    else:
        if tok == 'CtA' or tok == 'Ent' or tok == 'Dec':
           if tok == 'Dec': pilaTipos.append('D')
           if tok == 'Ent': pilaTipos.append('E')
           if tok == 'CtA': 
               lex = lex[1:len(lex)-1]
               pilaTipos.append('P')
           prgmCod.insCodigo('LIT', lex, '0')
        if tok == 'CtL':
            pilaTipos.append('L')
            if lex == 'verdadero':
                prgmCod.insCodigo('LIT', 'V', '0')
            elif lex == 'falso':
                prgmCod.insCodigo('LIT', 'F', '0')


def termino():
    global lex, tok, tabSimb, pilaTipos
    if lex != '(' and tok != 'Ide' and tok != 'CtA' and \
        tok != 'CtL' and tok != 'Ent' and tok != 'Dec':
        tok, lex = scanner()
    if lex == '(':
        tok, lex = scanner()
        expr()
        if lex != ')':
            erra('Error de Sintaxis', 'se espera cerrar ) y llego '+ lex)
    elif tok == 'Ide':
        nomIde = lex

        x = tabSimb.buscaSimbolo(nomIde)
        if x != None:
            pilaTipos.append(x.tipo)
        else:
            pilaTipos.append('I')
            erra('Error Semantico', 'Identificador no declarado ' + nomIde)

        tok, lex = scanner()
        if lex == '[': 
            tok, lex = scanner()
            expr()
            if lex != ']':
                erra('Error Sintaxis', 'se esperaba cerrar ] y llego '+lex)
        elif lex == '(': asigLfunc()
        prgmCod.insCodigo('LOD', nomIde, '0')
        oIde = tabSimb.buscaSimbolo(nomIde)
        if oIde != None:
            pilaTipos.append(oIde.tipo)
        else:
            erra("Error de Semantica", 'Identificador no declarado '+ nomIde) 
            pilaTipos.append('I')
    elif tok == 'CtL' or tok == 'CtA' or tok == 'Dec' or tok == 'Ent': 
        cte()
    if lex != ')' and lex != ',': 
        tok, lex = scanner()


def signo():
    global lex, tok
    if lex == '-':
        tok, lex = scanner()
    termino()


def expo():
    global tok, lex
    opr = '^'
    while opr == '^':
        signo()
        opr = lex


def multi():
    global tok, lex
    opr = '*'
    while opr == '*' or opr == '/' or opr == '%':
        opr = ''
        expo()
        if opr == '*' or opr == '/' or opr == '%':
            tipd = pilaTipos.pop()
            ope = pilaTipos.pop()
            tipi = pilaTipos.pop()
            tipr = pilaTipos.pop() + ope + tipd
            i = buscaTipo(tipr)
            if i >= 0:
                pilaTipos.append(tipoR[i])
            else:
                erra('Error Semantico ', 'conflicto en operacion ' + tipi + ' ' + ope + ' ' + tipd)
                pilaTipos.append('I')
        opr = lex
        if opr == '*' or opr == '/' or opr == '%':
            pilaTipos.append(opr)


def suma():
    global tok, lex
    opr = '+'
    while opr == '+' or opr == '-':
        opr = ''
        multi()
        if opr == '+' or opr == '-':
            tipd = pilaTipos.pop()
            ope = pilaTipos.pop()
            tipi = pilaTipos.pop()
            tipr = pilaTipos.pop() + ope + tipd
            i = buscaTipo(tipr)
            if i >= 0:
                pilaTipos.append(tipoR[i])
            else:
                erra('Error Semantico ', 'conflicto en operacion ' + tipi + ' ' + ope + ' ' + tipd)
                pilaTipos.append('I')
        opr = lex
        # se anadio esta parte y lo de opr = '' para todas las operaciones
        if opr == '+' or opr == '-':
            pilaTipos.append(opr)


def oprel():
    global tok, lex
    opr = '<'
    while opr in opRl:
        suma()
        opr = lex


def opno(): 
    global lex, tok
    if lex == 'no':
        tok, lex = scanner()
    oprel()


def opy():
    global tok, lex
    opr = 'y'
    while opr == 'y':
        opno()
        opr = lex


def expr():
    global tok, lex
    opr = 'o'
    while opr == 'o':
        opy()
        opr = lex


def dimen():
    global tok, lex
    tok, lex = scanner()

    if lex == 'IDENTIFICADOR':
        # Procesar el identificador de la variable a dimensionar
        var = lex
        tok, lex = scanner()

        if lex == '[':
            tok, lex = scanner()

            if lex == 'NUMERO':
                # Procesar el número de dimensiones de la variable
                num_dim = int(lex)
                tok, lex = scanner()

                if lex == ']':
                    # Procesar la lógica para dimensionar la variable con el número de dimensiones dado
                    # ...
                    
                    # Continuar con la ejecución del programa
                    tok, lex = scanner()
                else:
                    # Error de sintaxis esperando ']'
                    erra("Se esperaba ']' después del número de dimensiones en la instrucción 'dimen'")
            else:
                # Error de sintaxis esperando un número después del símbolo '['
                erra("Se esperaba un número después del símbolo '[' en la instrucción 'dimen'")
        else:
            # Error de sintaxis esperando '[' después del identificador
            erra("Se esperaba '[' después del identificador en la instrucción 'dimen'")
    else:
        # Error de sintaxis esperando un identificador después de 'dimen'
        erra("Se esperaba un identificador después de 'dimen'")

    if lex != '':
        # Error de sintaxis inesperado después de la instrucción 'dimen'
        erra("Se encontró un token inesperado después de la instrucción 'dimen'")



def constants():
    global tok, lex
    tok, lex = scanner()
    if lex in tipo:
            idTipo = lex
            tok, lex = scanner()
    while tok == 'Ide':
        Iden = lex
        tok, lex = scanner()
        if lex == '[':
            tok, lex = scanner()
            dimen()
        elif lex == '=':
            tok, lex = scanner()
            if idTipo == 'entero': idTipo = 'E'
            elif idTipo == 'decimal': idTipo = 'D'
            elif idTipo == 'logico': idTipo = 'L'
            elif idTipo == 'palabra': idTipo = 'P'
            if idTipo == 'P': lex = lex[1:len(lex)-1]
            tabSimb.inserSimbolo(Iden, 'C', idTipo, '0', '0', lex)
        
        tok, lex = scanner()
        if lex == ',':
            tok, lex = scanner()

    if lex != ';':
         erra('Error de Sintaxis', 'se esperaba <;> y llego '+ lex)
    return


def constVars():
        global idx, tok, lex, bPrinc
        if lex == 'constante': constants()
        else:
            if lex in tipo:
                idTipo = lex
                if idTipo == 'entero': idTipo = 'E'
                elif idTipo == 'decimal': idTipo = 'D'
                elif idTipo  == 'logico': idTipo = 'L'
                elif idTipo == 'palabra': idTipo = 'P'
            else: erra('se esperaba tipo '+ str(tipo), ' y llego '+lex)
            tok, lex = scanner()
            nIde = lex
            if tok != 'Ide': erra('Se esperaba Identificador', 'y llego '+ lex)
            tok, lex = scanner()
            if lex == ',':
                tabSimb.inserSimbolo(nIde, 'V', idTipo, '0', '0', '0')
                tok, lex = scanner()
                while tok == 'Ide':
                    nIde = lex
                    tok, lex = scanner()
                    if lex != ',' and lex  != '=' and lex != ';': erra('Error de Sintaxis se esperaba <, = ;>', 'y llego '+ lex)
                    elif lex == ',':
                        tabSimb.inserSimbolo(nIde, 'V', idTipo, '0', '0', '0')
                        tok, lex = scanner()
                    elif lex == '=':
                        tok, lex = scanner()
                        if tok != 'CtA' and idTipo == 'P': erra("Error Semantico, se esperaba Cte palabra ", "y llego "+ lex)
                        elif tok != 'CtL' and idTipo == 'L': erra("Error Semantico, se esperaba Cte logico ", "y llego "+ lex)
                        elif tok != 'Ent' and idTipo == 'E': erra("Error Semantico, se esperaba Cte entero ", "y llego "+ lex)
                        elif tok != 'Dec' and idTipo == 'D': erra("Error Semantico, se esperaba Cte decimal ", "y llego "+ lex)
                        else:
                            if tok == 'CtA': lex = lex[1:len(lex)-1] 
                            tabSimb.inserSimbolo(nIde, 'V', idTipo, '0', '0', lex)
                        tok, lex = scanner()
                        if lex == ',': tok, lex = scanner()
                if lex == ';': tabSimb.inserSimbolo(nIde, 'V', idTipo, '0', '0', '0')        
            elif lex == '=':
                tok, lex = scanner();
                if tok != 'CtA' and idTipo == 'P': erra("Error Semantico, se esperaba Cte palabra ", "y llego "+ lex)
                elif tok != 'CtL' and idTipo == 'L': erra("Error Semantico, se esperaba Cte logico ", "y llego "+ lex)
                elif tok != 'Ent' and idTipo == 'E': erra("Error Semantico, se esperaba Cte entero ", "y llego "+ lex)
                elif tok != 'Dec' and idTipo == 'D': erra("Error Semantico, se esperaba Cte decimal ", "y llego "+ lex)
                else:
                    if tok == 'CtA': lex = lex[1:len(lex)-1] 
                    tabSimb.inserSimbolo(nIde, 'V', idTipo, '0', '0', lex)
                tok, lex = scanner()
                if lex != ',' and lex != ';': erra('Error de Sintaxis, se esperaba , o ;', 'y llego '+ lex)
                elif lex == ',':
                    tok, lex = scanner()
                    while tok == 'Ide':
                        nIde = lex
                        tok, lex = scanner()
                        if lex != ',' and lex  != '=' and lex != ';': erra('Error de Sintaxis se esperaba , =, ;', 'y llego '+ lex)
                        elif lex == ',':
                            tabSimb.inserSimbolo(nIde, 'V', idTipo, '0', '0', '0')
                            tok, lex = scanner()
                        elif lex == '=':
                            tok, lex = scanner()
                            if tok != 'CtA' and idTipo == 'P': erra("Error Semantico, se esperaba Cte palabra ", "y llego "+ lex)
                            elif tok != 'CtL' and idTipo == 'L': erra("Error Semantico, se esperaba Cte logico ", "y llego "+ lex)
                            elif tok != 'Ent' and idTipo == 'E': erra("Error Semantico, se esperaba Cte entero ", "y llego "+ lex)
                            elif tok != 'Dec' and idTipo == 'D': erra("Error Semantico, se esperaba Cte decimal ", "y llego "+ lex)
                            else:
                                if tok == 'CtA': lex = lex[1:len(lex)-1] 
                                tabSimb.inserSimbolo(nIde, 'V', idTipo, '0', '0', lex)
                                tok, lex = scanner()
                                if lex != ',' and lex != ';': erra("Error de Sintaxis se esperaba ,", 'y llego '+lex)
                                if lex == ',':tok, lex = scanner()
                    if lex != ';': erra('Error de Sintaxis, se esperaba ; ', 'y llego '+lex)  
                    else: tabSimb.inserSimbolo(nIde, 'V', idTipo, '0', '0', '0')   
            elif lex == '(': 
                if bPrinc and nIde == 'principal': erra('Error de Semantica', 'la Funcion Principal ya esta definida') 
                if nIde == 'principal': 
                    bPrinc = True
                    tabSimb.inserSimbolo('_P', 'I', 'I', str(linCod + 1), '0', '0')
                tok, lex = scanner()      
                funcs()
                if nIde == 'principal': 
                    prgmCod.insCodigo('OPR', '0', '0')
                    idTipo = 'I'
            else:
                if lex == ';':
                    tabSimb.inserSimbolo(nIde, 'V', idTipo, '0', '0', '0')
                while lex != ';':
                    if lex == '[': dimen()
                    elif lex == ',':
                        tabSimb.inserSimbolo(nIde, 'V', idTipo, '0', '0', '0')
                        tok, lex = scanner()
                        if tok == 'Ide':
                            nIde = lex
                        if tok != 'Ide': erra('Se esperaba Identificador', 'y llego '+ lex)
                        tok, lex = scanner()
                tok, lex = scanner()
            idClase = 'V'
            if nIde == 'principal': idClase = 'F'
            if tabSimb.buscaSimbolo(nIde) == None:
                tabSimb.inserSimbolo(nIde, idClase, idTipo, '0', '0', '0')
        return


def params(): 
    global entrada, lex, tok
    tok, lex = scanner()
    

def gpoExp():
    global tok, lex, prgmCod
    deli=','
    while deli == ',':
        expr()
        if lex == ',': 
            deli = lex
            prgmCod.insCodigo('OPR', '0', '20')
            tok, lex = scanner()
        elif lex == ')': break


def leer():
    global tok, lex
    tok, lex = scanner()

    if lex == 'IDENTIFICADOR':
        # Procesar la variable a la que se desea asignar el valor leído
        var = lex
        tok, lex = scanner()

        if lex == ';':
            # Leer el valor desde la entrada estándar y asignarlo a la variable
            valor = input("Introduce un valor para {}: ".format(var))
            # Aquí puedes realizar la lógica para convertir el valor al tipo de dato adecuado si es necesario
            # Asignar el valor leído a la variable
            # ...

            # Continuar con la ejecución del programa
            tok, lex = scanner()
        else:
            # Error de sintaxis esperando ';'
            erra("Se esperaba ';' después del identificador en la instrucción 'leer'")
    else:
        # Error de sintaxis esperando un identificador después de 'leer'
        erra("Se esperaba un identificador después de 'leer'")

    if lex != '':
        # Error de sintaxis inesperado después de la instrucción 'leer'
        erra("Se encontró un token inesperado después de la instrucción 'leer'")



def imprime(): 
    global tok, lex, prgmCod
    tok, lex = scanner()
    if lex != '(':
        erra('Error de Sintaxis', 'se esperaba abrir ( y llego '+ lex)
    tok, lex = scanner()
    if lex == ')': prgmCod.insCodigo('LIT', '', '0')
    elif lex != ')': 
        gpoExp()
    if lex != ')':
        erra('Error de Sintaxis', 'se esperaba cerrar ) y llego '+ lex)
    prgmCod.insCodigo('OPR', '0', '20')


def imprimenl(): 
    global tok, lex, prgmCod
    tok, lex = scanner()
    if lex != '(':
        erra('Error de Sintaxis', 'se esperaba abrir ( y llego '+ lex)
    tok, lex = scanner()
    if lex == ')': prgmCod.insCodigo('LIT', '', '0')
    if lex != ')': 
        gpoExp()
    if lex != ')':
        erra('Error de Sintaxis', 'se esperaba cerrar ) y llego '+ lex)
    prgmCod.insCodigo('OPR', '0', '21')


def desde():
    global tok, lex
    tok, lex = scanner()

    if lex == 'id':
        # Procesar el identificador
        # ...

        tok, lex = scanner()

        if lex == 'en':
            expr()

            if lex == 'hasta':
                expr()

                if lex == 'hacer':
                    tok, lex = scanner()

                    if lex == '{':
                        blkcmd()
                    else:
                        # Error de sintaxis esperando un bloque de comandos después de 'hacer'
                        erra("Se esperaba un bloque de comandos después de 'hacer'")
                else:
                    # Error de sintaxis esperando la palabra clave 'hacer'
                    erra("Se esperaba la palabra clave 'hacer' después de 'hasta'")
            else:
                # Error de sintaxis esperando la palabra clave 'hasta'
                erra("Se esperaba la palabra clave 'hasta' después de la expresión")
        else:
            # Error de sintaxis esperando la palabra clave 'en'
            erra("Se esperaba la palabra clave 'en' después del identificador")
    else:
        # Error de sintaxis esperando un identificador después de 'desde'
        erra("Se esperaba un identificador después de 'desde'")

    if lex != '':
        # Error de sintaxis inesperado después del bloque de comandos
        erra("Se encontró un token inesperado después del bloque de comandos")



def mientras():
    global tok, lex
    tok, lex = scanner()

    if lex == 'que':
        expr()
    else:
        # Error de sintaxis esperando la palabra clave 'que' después de 'mientras'
        erra("Se esperaba la palabra clave 'que' después de 'mientras'")

    if lex == '{':
        blkcmd()
    else:
        # Error de sintaxis esperando un bloque de comandos después de la expresión
        erra("Se esperaba un bloque de comandos después de la expresión")

    if lex != '':
        # Error de sintaxis inesperado después del bloque de comandos
        erra("Se encontró un token inesperado después del bloque de comandos")



def si():
    global tok, lex
    tok, lex = scanner()  # Obtener el siguiente token y lexema

    if tok == "(":
        tok, lex = scanner()  # Obtener el siguiente token y lexema

        # Procesar la expresión condicional dentro del if
        expresion_condicional()

        if tok == ")":
            tok, lex = scanner()  # Obtener el siguiente token y lexema

            if tok == "THEN":
                tok, lex = scanner()  # Obtener el siguiente token y lexema

                # Crear un nuevo bloque de comandos para el cuerpo del if
                bloque_if = Bloque()

                # Procesar los comandos dentro del cuerpo del if
                estatutos(bloque_if)

                # Agregar el bloque del if al objeto Programa o al bloque padre actual
                programa.agregar_comando(bloque_if)
                if tok == "END":
                    tok, lex = scanner()  # Obtener el siguiente token y lexema
                    if tok == "IF":
                        tok, lex = scanner()  # Obtener el siguiente token y lexema
                        if tok == ";":
                            tok, lex = scanner()  # Obtener el siguiente token y lexema
                            # Éxito, if compilado correctamente
                            return
                        else:
                            # Error de sintaxis esperando un punto y coma al final del if
                            erra("Se esperaba un punto y coma al final del if")
                    else:
                        # Error de sintaxis esperando la palabra clave IF después de END
                        erra("Se esperaba la palabra clave IF después de END")
                else:
                    # Error de sintaxis esperando la palabra clave END después del cuerpo del if
                    erra("Se esperaba la palabra clave END después del cuerpo del if")
            else:
                # Error de sintaxis esperando la palabra clave THEN después de la expresión condicional
                erra("Se esperaba la palabra clave THEN después de la expresión condicional")
        else:
            # Error de sintaxis esperando un paréntesis de cierre después de la expresión condicional
            erra("Se esperaba un paréntesis de cierre después de la expresión condicional")
    else:
        # Error de sintaxis esperando un paréntesis de apertura antes de la expresión condicional
        erra("Se esperaba un paréntesis de apertura antes de la expresión condicional")



def repite():
    global tok, lex
    tok, lex = scanner()

    if lex == 'num':
        # Procesar el número
        # ...

        tok, lex = scanner()

        if lex == 'veces':
            tok, lex = scanner()

            if lex == '{':
                blkcmd()
            else:
                # Error de sintaxis esperando un bloque de comandos después de 'veces'
                erra("Se esperaba un bloque de comandos después de 'veces'")
        else:
            # Error de sintaxis esperando la palabra clave 'veces'
            erra("Se esperaba la palabra clave 'veces' después del número")
    else:
        # Error de sintaxis esperando un número después de 'repite'
        erra("Se esperaba un número después de 'repite'")

    if lex != '':
        # Error de sintaxis inesperado después del bloque de comandos
        erra("Se encontró un token inesperado después del bloque de comandos")


def lmp():
    prgmCod.insCodigo('OPR', '0', '18')


def regresa():
    global tok, lex
    tok, lex = scanner()

    if lex != '':
        expr()
    else:
        # Error de sintaxis esperando una expresión después de 'regresa'
        erra("Se esperaba una expresión después de 'regresa'")

    if lex != '':
        # Error de sintaxis inesperado después de la expresión
        erra("Se encontró un token inesperado después de la expresión")



def Lfunc():
    global tok, lex
    tok, lex = scanner()

    if lex == 'IDENTIFICADOR':
        # Procesar el identificador de la función
        func_name = lex
        tok, lex = scanner()

        if lex == '(':
            tok, lex = scanner()

            if lex == ')':
                # Procesar la lógica para una función sin parámetros
                # ...
                
                # Continuar con la ejecución del programa
                tok, lex = scanner()
            else:
                # Procesar la lógica para una función con parámetros
                # ...
                
                # Continuar con la ejecución del programa
                tok, lex = scanner()
        else:
            # Error de sintaxis esperando '(' después del identificador de la función
            erra("Se esperaba '(' después del identificador de la función en la instrucción 'Lfunc'")
    else:
        # Error de sintaxis esperando un identificador después de 'Lfunc'
        erra("Se esperaba un identificador después de 'Lfunc'")

    if lex != '':
        # Error de sintaxis inesperado después de la instrucción 'Lfunc'
        erra("Se encontró un token inesperado después de la instrucción 'Lfunc'")



def udim(): pass


def asigna(): 
    global tok, lex, tabSimb, pilaTipos
    nomIde = lex

    tabSimb.impTabSim()
    x = tabSimb.buscaSimbolo(nomIde)
    if x != None:
        pilaTipos.append(x.tipo)
    else:
        erra('Error de semantica', 'Identificador no declarado' + nomIde)
        pilaTipos.append('I')
    tok, lex = scanner()
    if lex == '[': udim()
    if lex == '=': 
        pilaTipos.append('=')
    else:
        erra('Error de sintaxis', 'se esperaba = y llego' + lex)
    tok, lex = scanner()
    expr()
    # Valida tipo en asignacion
    tipd = pilaTipos.pop()
    tips = pilaTipos.pop() + tipd
    tipi = pilaTipos.pop()
    tips = tipi + tips
    i = buscaTipo(tips)
    if i >=0 and tipoR[i] != '':
        pilaTipos.append(tipoR[i])
    elif i < 0:
        erra('Error semantico', ' conflicto en tipos en asignacion de ' + tipi + ' = ' + tipd)


def comando(): 
    global tok, lex
    if tok == 'Ide': asigna()
    if lex == 'lee': leer()
    elif lex == 'imprime': imprime()
    elif lex == 'imprimenl': imprimenl()
    elif lex == 'desde': desde()
    elif lex == 'mientras': mientras()
    elif lex == 'si': si()
    elif lex == 'repite': repite()
    elif lex == 'lmp': lmp()
    elif lex == 'regresa': regresa()
    else: erra('Error de Sintaxis', 'comando no definido '+ lex)
    tok, lex = scanner()


def blkcmd():
    global lex, tok
    tok, lex = scanner()
    if lex != ';' and lex != '{': 
        comando()
        tok, lex = scanner()
        if lex != ';': erra('Error de Sintaxis', 'se esperaba ; y llego '+lex)
    elif lex == '{':
        estatutos()
        if lex != '}': erra('Error de Sintaxis', 'se esperaba cerrar block \"}\" y llego '+ lex)


def estatutos(): 
    global tok, lex
    cbk = '{'
    while cbk != '}':
        if lex != ';': comando()
        if lex != ';': erra('Error de Sintaxis', 'se esperaba ; y llego '+lex)
        tok, lex = scanner()
        cbk = lex


def blkFunc():
    global lex, tok
    if lex != '{': erra('Error de Sintaxis', 'se esperaba abrir \"{\" y llego '+lex)
    tok, lex = scanner()
    if lex != '}': estatutos()
    if lex != '}':erra('Error de Sintaxis', 'se esperaba cerrar \"}\" y llego '+lex)


def funcs():
        global tok, lex, tipo, bPrinc
        if lex != ')': params()
        if lex != ')': erra('Error de Sintaxis', 'se esperaba parentisis cerrado \")\"')
        tok, lex = scanner()
        blkFunc()


def prgm():
    global entrada, idx, tok, lex
    while len(entrada) > 0 and  idx < len(entrada):
        tok, lex = scanner()
        constVars()


def parser():
    prgm()


if __name__ == '__main__':
    arche = input('Archivo (.icc) [.]=salir: ')
    if arche == '.': exit()
    archivo = open(arche, 'r')
    #se carag archivo en entrada
    entrada = ''
    for linea in archivo:
        entrada += linea
        
    print(entrada)
    parser()
    archs = arche[:len(arche)-4]
    archsl = archs + '.eje'
    
    if not(cERR): 
        print('Programa COMPILO con EXITO') 
        tabSimb.grabaTabla(archsl)
        prgmCod.grabaCodigo(archsl)
        os.system('Inter ' + archs)