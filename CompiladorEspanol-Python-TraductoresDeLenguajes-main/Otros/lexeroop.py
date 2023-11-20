class AnalizadorLexico:
    def __init__(self):
        self.RESERVADAS = ['nulo', 'entero', 'decimal', 'palabra', 'logico', 'constante', 'desde', 'si', 'hasta', 'mientras',
                           'regresa', 'hacer', 'sino', 'incr', 'imprime', 'imprimenl', 'lee', 'repite', 'que']
        self.OPERADORES_LOGICOS = ['no', 'y', 'o']
        self.CONSTANTES_LOGICAS = ['verdadero', 'falso']
        self.OPERADORES_ARITMETICOS = ['+', '-', '*', '/', '%', '^']
        self.DELIMITADORES = [';', ',', '(', ')', '{', '}', '[', ']', ':', '=']
        self.DELIMITADORES_UNIVERSALES = [' ', '\t', '\n']
        self.OPERADORES_RELACIONALES = ['<', '>', '<=', '>=', '<>', '==']
        self.pos = -1
        self.texto = ''
        self.char_actual = None
        self.linea_actual = 1
        self.posicion_actual = 0
        self.tokens = []

    def avanzar(self):
        self.pos += 1
        if self.pos < len(self.texto):
            if self.char_actual == '\n':
                self.linea_actual += 1
                self.posicion_actual = 0
            else:
                self.posicion_actual += 1
            self.char_actual = self.texto[self.pos]
        else:
            self.char_actual = None

    def crear_digitos(self):
        str_num = ''
        puntos = 0
        while self.char_actual is not None and (self.char_actual.isdigit() or self.char_actual == '.'):
            if self.char_actual == '.':
                if puntos == 1:
                    break
                puntos += 1
                str_num += '.'
            else:
                str_num += self.char_actual
            self.avanzar()

        if puntos == 0:
            return ('ENTERO', int(str_num))
        else:
            return ('DECIMAL', float(str_num))

    def crear_cadena(self):
        str_cadena = ''
        self.avanzar()  # Avanza sobre la comilla inicial

        while self.char_actual is not None and self.char_actual != '"':
            str_cadena += self.char_actual
            self.avanzar()

        if self.char_actual == '"':
            self.avanzar()  # Avanza sobre la comilla final
            return ('CADENA', str_cadena)
        else:
            raise SyntaxError(f"Cadena de texto no cerrada en la línea {self.linea_actual}, posición {self.posicion_actual}")

    def analizar(self, input_text):
        self.pos = -1
        self.texto = input_text
        self.char_actual = None
        self.linea_actual = 1
        self.posicion_actual = 0
        self.avanzar()
        self.tokens = []
        en_comentario = False

        while self.char_actual is not None:
            # Comentarios de una línea
            if self.char_actual == '/' and self.pos + 1 < len(self.texto) and self.texto[self.pos + 1] == '/':
                # Ignora todo hasta el final de la línea
                while self.char_actual is not None and self.char_actual != '\n':
                    self.avanzar()
                self.avanzar()  # Avanza sobre el último '\n'
            # Comentarios de varias líneas
            elif self.char_actual == '/' and self.pos + 1 < len(self.texto) and self.texto[self.pos + 1] == '*':
                en_comentario = True
                self.avanzar()  # Avanza sobre el '*'
                self.avanzar()  # Avanza sobre el '/'
            elif en_comentario and self.char_actual == '*' and self.pos + 1 < len(self.texto) and self.texto[self.pos + 1] == '/':
                en_comentario = False
                self.avanzar()  # Avanza sobre el '*'
                self.avanzar()  # Avanza sobre el '/'
            elif not en_comentario:
                if self.char_actual in self.DELIMITADORES_UNIVERSALES:
                    self.avanzar()
                elif self.char_actual.isdigit():
                    self.tokens.append(self.crear_digitos())
                elif self.char_actual in self.OPERADORES_ARITMETICOS:
                    self.tokens.append(('OP_ARITMETICO', self.char_actual))
                    self.avanzar()
                elif self.char_actual in self.OPERADORES_RELACIONALES:
                    # Verificamos si el próximo caracter también forma parte del operador relacional
                    if self.pos + 1 < len(self.texto) and self.char_actual + self.texto[self.pos + 1] in self.OPERADORES_RELACIONALES:
                        self.tokens.append(('OP_RELACIONAL', self.char_actual + self.texto[self.pos + 1]))
                        self.avanzar()
                    else:
                        self.tokens.append(('OP_RELACIONAL', self.char_actual))
                    self.avanzar()
                elif self.char_actual.isalpha() or self.char_actual == '_':
                    id = ''
                    while self.char_actual is not None and (self.char_actual.isalnum() or self.char_actual == '_'):
                        id += self.char_actual
                        self.avanzar()
                    if id in self.RESERVADAS:
                        self.tokens.append(('RESERVADA', id))  # Las palabras reservadas son tokens
                    elif id in self.OPERADORES_LOGICOS:
                        self.tokens.append(('OP_LOGICO', id))
                    elif id in self.CONSTANTES_LOGICAS:
                        self.tokens.append(('CONST_LOGICA', id))
                    else:
                        self.tokens.append(('VARIABLE', id))
                elif self.char_actual == '"':
                    self.tokens.append(self.crear_cadena())
                elif self.char_actual in self.DELIMITADORES:
                    self.tokens.append(('DELIMITADOR', self.char_actual))
                    self.avanzar()
                else:
                    raise SyntaxError(f"Caracter inesperado '{self.char_actual}' en la línea {self.linea_actual}, posición {self.posicion_actual}")
            else:
                self.avanzar()

        if en_comentario:
            raise SyntaxError("Comentario de múltiples líneas no cerrado.")

        return self.tokens
    

codigo_fuente = '''
aqui va el programa de prueba
'''
analizador_lexico = AnalizadorLexico()
tokens = analizador_lexico.analizar(codigo_fuente)

print(tokens)

