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


class AnalizadorSintactico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def avanzar(self, tipo_token):
        if self.pos < len(self.tokens) and self.tokens[self.pos][0] == tipo_token:
            self.pos += 1
        else:
            raise SyntaxError(f"Se esperaba {tipo_token}, pero se encontró {self.tokens[self.pos][0]}")

    def programa(self):
        while self.pos < len(self.tokens):
            self.declaracion()
        self.funcion_principal()

    def declaracion(self):
        if self.tokens[self.pos][0] == 'CONSTANTE':
            self.calificador_constante()
            self.declaracion_variable()
        else:
            self.declaracion_variable()

    def calificador_constante(self):
        self.avanzar('CONSTANTE')

    def declaracion_variable(self):
        self.tipo()
        self.identificador()
        while self.tokens[self.pos][0] == 'DELIMITADOR' and self.tokens[self.pos][1] == ',':
            self.avanzar('DELIMITADOR')
            self.identificador()
        if self.tokens[self.pos][0] == 'DELIMITADOR' and self.tokens[self.pos][1] == '=':
            self.avanzar('DELIMITADOR')
            self.expresion()
        self.avanzar('DELIMITADOR')

    def tipo(self):
        tipos_validos = ['nulo', 'entero', 'decimal', 'palabra', 'logico']
        if self.tokens[self.pos][0] == 'RESERVADA' and self.tokens[self.pos][1] in tipos_validos:
            self.avanzar('RESERVADA')
        else:
            raise SyntaxError(f"Se esperaba un tipo válido, pero se encontró {self.tokens[self.pos][1]}")

    def identificador(self):
        if self.tokens[self.pos][0] == 'VARIABLE':
            self.avanzar('VARIABLE')
        else:
            raise SyntaxError(f"Se esperaba un identificador, pero se encontró {self.tokens[self.pos][1]}")

    def expresion(self):
        if self.tokens[self.pos][0] == 'ENTERO' or self.tokens[self.pos][0] == 'DECIMAL':
            self.numero()
        elif self.tokens[self.pos][0] == 'CADENA':
            self.cadena()
        elif self.tokens[self.pos][0] == 'RESERVADA' and self.tokens[self.pos][1] in self.tokens[self.pos][1] in self.RESERVADAS:
            self.avanzar('RESERVADA')
        elif self.tokens[self.pos][0] == 'OP_ARITMETICO':
            self.operacion_aritmetica()
        elif self.tokens[self.pos][0] == 'OP_LOGICO':
            self.operacion_logica()
        elif self.tokens[self.pos][0] == 'OP_RELACIONAL':
            self.operacion_relacional()
        elif self.tokens[self.pos][0] == 'VARIABLE':
            self.avanzar('VARIABLE')
        else:
            raise SyntaxError(f"Expresión inválida en la línea {self.tokens[self.pos][1]}, posición {self.tokens[self.pos][2]}")

    def numero(self):
        if self.tokens[self.pos][0] == 'ENTERO' or self.tokens[self.pos][0] == 'DECIMAL':
            self.avanzar(self.tokens[self.pos][0])
        else:
            raise SyntaxError(f"Se esperaba un número, pero se encontró {self.tokens[self.pos][1]}")

    def cadena(self):
        if self.tokens[self.pos][0] == 'CADENA':
            self.avanzar('CADENA')
        else:
            raise SyntaxError(f"Se esperaba una cadena de texto, pero se encontró {self.tokens[self.pos][1]}")

    def logico(self):
        if self.tokens[self.pos][0] == 'RESERVADA' and self.tokens[self.pos][1] in self.CONSTANTES_LOGICAS:
            self.avanzar('RESERVADA')
        else:
            raise SyntaxError(f"Se esperaba un valor lógico, pero se encontró {self.tokens[self.pos][1]}")

    def operacion_aritmetica(self):
        self.expresion()
        self.operador_aritmetico()
        self.expresion()

    def operador_aritmetico(self):
        if self.tokens[self.pos][0] == 'OP_ARITMETICO':
            self.avanzar('OP_ARITMETICO')
        else:
            raise SyntaxError(f"Se esperaba un operador aritmético, pero se encontró {self.tokens[self.pos][1]}")

    def operacion_logica(self):
        self.expresion()
        self.operador_logico()
        self.expresion()

    def operador_logico(self):
        if self.tokens[self.pos][0] == 'OP_LOGICO':
            self.avanzar('OP_LOGICO')
        else:
            raise SyntaxError(f"Se esperaba un operador lógico, pero se encontró {self.tokens[self.pos][1]}")

    def operacion_relacional(self):
        self.expresion()
        self.operador_relacional()
        self.expresion()

    def operador_relacional(self):
        if self.tokens[self.pos][0] == 'OP_RELACIONAL':
            self.avanzar('OP_RELACIONAL')
        else:
            raise SyntaxError(f"Se esperaba un operador relacional, pero se encontró {self.tokens[self.pos][1]}")

    def declaracion_funcion(self):
        self.tipo()
        self.identificador()
        self.avanzar('DELIMITADOR')
        self.lista_parametros()
        self.avanzar('DELIMITADOR')
        self.sentencia_compuesta()

    def lista_parametros(self):
        if self.tokens[self.pos][0] == 'RESERVADA' and self.tokens[self.pos][1] in self.RESERVADAS:
            self.tipo()
            self.identificador()
            while self.tokens[self.pos][0] == 'DELIMITADOR' and self.tokens[self.pos][1] == ',':
                self.avanzar('DELIMITADOR')
                self.tipo()
                self.identificador()

    def sentencia_compuesta(self):
        self.avanzar('DELIMITADOR')
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] != 'DELIMITADOR' and self.tokens[self.pos][1] != '}':
            self.sentencia()
        self.avanzar('DELIMITADOR')

    def sentencia(self):
        if self.tokens[self.pos][0] == 'DELIMITADOR':
            self.sentencia_expresion()
        elif self.tokens[self.pos][0] == 'RESERVADA' and self.tokens[self.pos][1] == 'si':
            self.sentencia_seleccion()
        elif self.tokens[self.pos][0] == 'RESERVADA' and self.tokens[self.pos][1] == 'desde':
            self.sentencia_iteracion()
        elif self.tokens[self.pos][0] == 'RESERVADA' and self.tokens[self.pos][1] == 'imprime':
            self.sentencia_imprimir()
        elif self.tokens[self.pos][0] == 'RESERVADA' and self.tokens[self.pos][1] == 'regresa':
            self.sentencia_retorno()
        elif self.tokens[self.pos][0] == 'VARIABLE':
            self.sentencia_asignacion()
        else:
            raise SyntaxError(f"Sentencia inválida en la línea {self.tokens[self.pos][1]}, posición {self.tokens[self.pos][2]}")

    def sentencia_expresion(self):
        self.expresion()
        self.avanzar('DELIMITADOR')

    def sentencia_seleccion(self):
        self.avanzar('RESERVADA')
        self.avanzar('DELIMITADOR')
        self.expresion()
        self.avanzar('DELIMITADOR')
        self.sentencia_compuesta()
        if self.tokens[self.pos][0] == 'RESERVADA' and self.tokens[self.pos][1] == 'sino':
            self.avanzar('RESERVADA')
            self.sentencia_compuesta()

    def sentencia_iteracion(self):
        if self.tokens[self.pos][0] == 'RESERVADA' and self.tokens[self.pos][1] == 'desde':
            self.avanzar('RESERVADA')
            self.expresion()
            self.avanzar('RESERVADA')
            self.expresion()
            self.avanzar('RESERVADA')
            self.expresion()
        elif self.tokens[self.pos][0] == 'RESERVADA' and self.tokens[self.pos][1] == 'mientras':
            self.avanzar('RESERVADA')
            self.expresion()
        elif self.tokens[self.pos][0] == 'RESERVADA' and self.tokens[self.pos][1] == 'repite':
            self.avanzar('RESERVADA')
            while self.pos < len(self.tokens) and (self.tokens[self.pos][0] != 'RESERVADA' or self.tokens[self.pos][1] != 'hasta'):
                self.sentencia()
            self.avanzar('RESERVADA')
            self.expresion()

        self.sentencia_compuesta()

    def sentencia_imprimir(self):
        self.avanzar('RESERVADA')
        self.avanzar('DELIMITADOR')
        self.expresion()
        self.avanzar('DELIMITADOR')

    def sentencia_retorno(self):
        self.avanzar('RESERVADA')
        self.expresion()
        self.avanzar('DELIMITADOR')

    def sentencia_asignacion(self):
        self.identificador()
        self.avanzar('DELIMITADOR')
        self.expresion()
        self.avanzar('DELIMITADOR')

    def funcion_principal(self):
        self.avanzar('RESERVADA')
        self.avanzar('RESERVADA')
        self.avanzar('DELIMITADOR')
        self.sentencia_compuesta()


# Uso del analizador léxico y sintáctico
codigo_fuente = '''
nulo principal() {
    entero a, b, c;
    a = 5;
    b = 10;
    c = a + b;
    si (c > 15) {
        imprime("El resultado es mayor a 15");
    } sino {
        imprime("El resultado es menor o igual a 15");
    }
    regresa c;
}
'''

analizador_lexico = AnalizadorLexico()
tokens = analizador_lexico.analizar(codigo_fuente)

analizador_sintactico = AnalizadorSintactico(tokens)
analizador_sintactico.programa()
