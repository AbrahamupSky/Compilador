from simbolo import Simbolo, TOKENS, ZONA_DE_CODIGO, TIPO_DATO
from error import Error
import json

palabras_reservadas = [
  'bool',
  'call',
  'char',
  'do',
  'else',
  'float',
  'for',
  'function',
  'if',
  'int',
  'main',
  'read',
  'return',
  'string',
  'then',
  'to',
  'void',
  'while',
  'write',
  'false',
  'true']  

#? Lista de Palabras reservadas

class Lexico:
  def __init__(self, codigo):             #Constructor del Analizador Lexico.
    self.codigo = " " + codigo + " "    #codigo fuente a compilar.
    self.tablaSimb = []                 #tabla de Simbolos
    self.index = 0                      #indice del caracter actual
    self.inicioLex = 1                  #inicio del lexema actual
    self.Lexema = ""                    #Ultimo lexema encontrado
    self.num_linea = 1                  #numero de linea del codigo fuente
    self.estado = 0
    self.caracteres_permitidos = "(){}[],;+-*/\\%&|!"     #estado actual en los automatas.
    self.tipo_de_dato_actual = 0  # Registra el tipo de dato de los identificadores.

    self.zona_de_codigo = ZONA_DE_CODIGO['DEF_VARIABLES_GLOBALES']  # Indica la zona del codigo
    # fuente que se esa procesando.

    self.fin_definicion_palabras_reservadas = None  # Indica donde termina la definicion de
    # Palabra Reservadas
    self.fin_definicion_variables_globales = None  # Inidica donde termina la definicion de
    # Variables Globales
    self.inicio_definicion_variables_locales = None  # Indica donde inicia la definicion de
    # Variables Locales en la funcion actual
    self.fin_definicion_variables_locales = None  # Indica donde finaliza la definicion de
    # Variables locales en la funcion actual

    self.error = Error()
    self.cargar_palabras_reservadas()   #Cargar las palabras reservadas en
                      #la tabla de simbolos.


  def insertar_simbolo(self, simbolo):    #inserta un nuevo simbolor en la TS.
    if simbolo:
      self.tablaSimb.append(simbolo)
      return self.tablaSimb[len(self.tablaSimb)-1]
    else:
      raise ValueError("Se esperaba un simbolo")

  def cargar_palabras_reservadas(self):   #Carga las palabras reservadas en TS
    for p in palabras_reservadas:
      self.insertar_simbolo(Simbolo(p, TOKENS[p.upper()]))
    self.fin_definicion_palabras_reservadas = len(self.tablaSimb)

  def mostrar_tabla_simbolos(self):       #muestra el contenido de la TS.
    for s in self.tablaSimb:
      print(s)

  def buscar_lexema(self, lexema):        #busca un lexema en la TS.
    if self.zona_de_codigo == ZONA_DE_CODIGO['DEF_VARIABLES_GLOBALES']:
      for simb in self.tablaSimb:
        if lexema == simb.Lexema:
          return simb
      return None

    elif self.zona_de_codigo == ZONA_DE_CODIGO['DEF_VARIABLES_LOCALES']:
      for simb in self.tablaSimb[self.inicio_definicion_variables_locales:]:
        if lexema == simb.Lexema:
          return simb
      for simb in self.tablaSimb[:self.fin_definicion_palabras_reservadas]:
        if lexema == simb.Lexema:
          return simb
      return None

    elif self.zona_de_codigo == ZONA_DE_CODIGO['CUERPO_FUNCION_LOCAL']:
      for simb in self.tablaSimb[self.inicio_definicion_variables_locales:]:
        if lexema == simb.Lexema:
          return simb
      for simb in self.tablaSimb[:self.fin_definicion_variables_globales]:
        if lexema == simb.Lexema:
          return simb
      return None
      
    elif self.zona_de_codigo == ZONA_DE_CODIGO['CUERPO_PRINCIPAL']:
      for simb in self.tablaSimb[:self.fin_definicion_variables_globales]:
        if lexema == simb.Lexema:
          return simb
      return None

  def tablaSimb2JSON(self):               #regresa el contenido de TS en JSON
    return json.dumps([obj.__dict__ for obj in self.tablaSimb])

  def siguiente_caracter(self):           #regresa el siguiente caracter del
    self.index += 1                     #codigo fuente.
    try:
      return self.codigo[self.index]
    except IndexError:
      return '\0'

  def saltar_caracter(self):              #ignora el caracter actual, por eje-
    self.index += 1                     #mplo: tabs, espacios, enters, etc.
    self.inicioLex = self.index

  def leer_lexema(self):                  #regresa la cadena que se encuentra
    self.Lexema = self.codigo[self.inicioLex:self.index + 1]
    self.estado = 0                     #entre inicioLex y el index.
    self.avanza_inicio_lexema()
    return self.Lexema

  def regresa_caracter(self):             #Representa el (*) en un estado de
    self.index -= 1                     #aceptacion.

  def avanza_inicio_lexema(self):         #mueve el incioLex un caracter hacia
    self.inicioLex = self.index + 1     #adelante

  def deshacer_automata(self):
    self.index = self.inicioLex
    return self.codigo[self.index]

  def siguiente_componente_lexico(self):  #regresa el siguiente simbolo encon-
    while(True):                        #trado en el codigo fuente.
      if self.estado == 0:
        c = self.siguiente_caracter()

        if c ==' ' or c =='\t' or c == '\n':
          self.avanza_inicio_lexema() #Ignorar todo tipo de espacios
          if c == '\n':               #en blanco
            self.num_linea += 1     #incrementar num_line en enter.
        elif c == '\0':
          return None
        elif c == '<':
          self.estado = 1
        elif c == '=':
          self.estado = 5
        elif c == '>':
          self.estado = 6
        else:
          self.estado = self.fallo()  #Probar el siguiente automata.
      elif self.estado == 1:
        c = self.siguiente_caracter()   #Todos los estados intermedios
        if c == '=':                    #deben llamar a siguiente_caracter
          self.estado = 2
        elif c == '>':
          self.estado = 3
        else:
          self.estado = 4
      elif self.estado == 2:
        self.leer_lexema()
        return(Simbolo(self.Lexema,TOKENS['MEI']))
      elif self.estado == 3:
        self.leer_lexema()
        return(Simbolo(self.Lexema,TOKENS['DIF']))
      elif self.estado == 4:
        self.regresa_caracter()
        self.leer_lexema()
        return(Simbolo(self.Lexema,TOKENS['MEN']))
      elif self.estado == 5:
        self.leer_lexema()
        return(Simbolo(self.Lexema,TOKENS['IGU']))
      elif self.estado == 6:
        c = self.siguiente_caracter()
        if c == '=':
          self.estado = 7
        else:
          self.estado = 8
      elif self.estado == 7:
        self.leer_lexema()
        return Simbolo(self.Lexema, TOKENS['MAI'])
      elif self.estado == 8:
        self.regresa_caracter()
        self.leer_lexema()
        return Simbolo(self.Lexema, TOKENS['MAY'])
      elif self.estado == 9:
        if c.isalpha():
          self.estado = 10
        else:
          self.estado = self.fallo()
      elif self.estado == 10:
        c = self.siguiente_caracter()
        if not c.isalnum():
          self.estado = 11
      elif self.estado == 11:
        self.regresa_caracter()
        self.leer_lexema()
        simb = self.buscar_lexema(self.Lexema)
        
        if self.zona_de_codigo == 0 or self.zona_de_codigo == 1:
          if simb and simb.Token != TOKENS['ID']:
            return simb
          elif simb is None:
            return self.insertar_simbolo(Simbolo(self.Lexema, TOKENS['ID'], self.tipo_de_dato_actual))
          elif simb.Token == TOKENS['ID']:
            self.error.reportar_error(self.num_linea, "Semantico", "La variable '{}' ya fue definida en el ambito actual.".format(self.Lexema))
            return simb
        elif self.zona_de_codigo == 2 or self.zona_de_codigo == 3:
          if simb:
            return simb
          else:
            self.error.reportar_error(self.num_linea, "Semantico", "La variable '{}' no fue declarada.".format(self.Lexema))
            return self.insertar_simbolo(Simbolo(self.Lexema, TOKENS['ID'], TIPO_DATO['na']))
      elif self.estado == 12:
        if c.isdigit():
          self.estado = 13
        else:
          self.estado = self.fallo()
      elif self.estado == 13:
        c = self.siguiente_caracter()
        if c == 'E' or c == 'e':
          self.estado = 16
        elif c == '.':
          self.estado = 14
        elif not c.isdigit():
          self.estado = 20
      elif self.estado == 14:
        c = self.siguiente_caracter()
        if c.isdigit():
          self.estado = 15
        else:
          self.estado = self.fallo()
      elif self.estado == 15:
        c = self.siguiente_caracter()
        if c == 'E' or c == 'e':
          self.estado = 16
        elif not c.isdigit():
          self.estado = 21
      elif self.estado == 16:
        c = self.siguiente_caracter()
        if c == '+' or c == '-':
          self.estado = 17
        elif c.isdigit():
          self.estado = 18
        else:
          self.es = self.fallo()
      elif self.estado == 17:
        c = self.siguiente_caracter()
        if c.isdigit():
          self.estado = 18
        else: self.estado = self.fallo()
      elif self.estado == 18:
        c =self.siguiente_caracter()
        if not c.isdigit():
          self.estado = 19
      elif self.estado == 19:
        self.regresa_caracter()
        self.leer_lexema()
        return Simbolo(self.Lexema, TOKENS['NUMF'])
      elif self.estado == 20:
        self.regresa_caracter()
        self.leer_lexema()
        return Simbolo(self.Lexema, TOKENS['NUM'])
      elif self.estado == 21:
        self.regresa_caracter()
        self.leer_lexema()
        return Simbolo(self.Lexema, TOKENS['NUMF'])
      elif self.estado == 22:
        if c == '"':
          self.estado = 23
        else:
          self.estado = self.fallo()
      elif self.estado == 23:
        c = self.siguiente_caracter()
        if c == "\\":
          self.estado = 24
        elif c == '"':
          self.estado = 25
      elif self.estado == 24:
        c = self.siguiente_caracter()
        if c in 'nta"\\r':
          self.estado = 23
        else:
          self.estado = self.fallo()
      elif self.estado == 25:
        self.leer_lexema()
        return Simbolo(self.Lexema, TOKENS['CONST_STRING'])
      elif self.estado == 26:
        if c == "'":
          self.estado = 27
        else:
          self.estado = self.fallo()
      elif self.estado == 27:
        c = self.siguiente_caracter()
        if c == '\\':
          self.estado = 28
        else:
          self.estado = 29
      elif self.estado == 28:
        c = self.siguiente_caracter()
        if c in "nta'\\r":
          self.estado = 29
        else:
          self.estado = self.fallo()
      elif self.estado == 29:
        c = self.siguiente_caracter()
        if c == "'":
          self.estado = 30
        else:
          self.estado = self.fallo()
      elif self.estado == 30:
        self.leer_lexema()
        return Simbolo(self.Lexema, TOKENS['CONST_CHAR'])
      elif self.estado == 31:
        if c == "/":
          self.estado = 32
        else:
          self.estado = self.fallo()
      elif self.estado == 32:
        c = self.siguiente_caracter()
        if c == "/":
          self.estado = 34
        elif c == "*":
          self.estado = 33
        else:
          c = self.deshacer_automata()
          self.estado = self.fallo()
      elif self.estado == 33:
        c = self.siguiente_caracter()
        if c == "*":
          self.estado = 35
      elif self.estado == 34:
        c = self.siguiente_caracter()
        if c == "\n" or c == "\0":
          self.estado = 36
      elif self.estado == 35:
        c = self.siguiente_caracter()
        if c == "/":
          self.estado = 37
        else:
          self.estado = 33
      elif self.estado == 36:
        self.regresa_caracter()
        self.leer_lexema()
      elif self.estado == 37:
        self.leer_lexema()
      elif self.estado == 38:
        if c in self.caracteres_permitidos:
          self.leer_lexema()
          return Simbolo(c,ord(c))
        else:
          self.estado = self.fallo()
      else:
        self.leer_lexema()
        self.error.reportar_error(self.num_linea, "Lexico", "Simbolo no permitido '{}'.".format(self.Lexema))

  def fallo(self):
    if self.estado <= 8:
      return 9
    elif self.estado <= 11:
      return 12
    elif self.estado <= 21:
      return 22
    elif self.estado <= 25:
      return 26
    elif self.estado <= 30:
      return 31
    elif self.estado <= 37:
      return 38
    else:
      return 99
