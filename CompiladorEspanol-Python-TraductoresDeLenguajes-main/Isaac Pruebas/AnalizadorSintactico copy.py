class SyntacticAnalyzer:

    def __init__(self, tokens):
        self.tokens = tokens
        self.posicion_actual = 0
        self.linea_actual = 0

    def programa(self):
        while self.tokens and self.tokens[self.posicion_actual][0] != 'RESERVADA' and self.tokens[self.posicion_actual][1] != 'principal':
            self.declaracion()
            print('hola')

        self.funcion_principal()

    def declaracion(self):
        if self.tokens[self.posicion_actual][0] == 'RESERVADA' and self.tokens[self.posicion_actual][1] == 'constante':
            self.avanzar()
        elif self.tokens[self.posicion_actual][0] == 'RESERVADA' and self.tokens[self.posicion_actual][1] in ['nulo', 'entero', 'decimal', 'palabra', 'logico']:
            self.tipo()
        elif self.tokens[self.posicion_actual][0] == 'IDENTIFICADOR':
            self.declaracion_variable()
        else:
            raise SyntaxError(f"Se esperaba una declaracion en la linea {self.linea_actual}, posicion {self.posicion_actual}")

    def tipo(self):
        if self.tokens[self.posicion_actual][0] == 'RESERVADA' and self.tokens[self.posicion_actual][1] in ['nulo', 'entero', 'decimal', 'palabra', 'logico']:
            self.avanzar()
        else:
            raise SyntaxError(f"Se esperaba un tipo de dato en la linea {self.linea_actual}, posicion {self.posicion_actual}")

    def declaracion_variable(self):
        self.identificador()

        while self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == ',':
            self.avanzar()
            self.identificador()

        if self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == '=':
            self.avanzar()
            self.expresion()

        if self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == ';':
            self.avanzar()
        else:
            raise SyntaxError(f"Se esperaba ';' en la linea {self.linea_actual}, posicion {self.posicion_actual}")

    def identificador(self):
        if self.tokens[self.posicion_actual][0] == 'IDENTIFICADOR':
            self.avanzar()
        else:
            raise SyntaxError(f"Se esperaba un identificador en la linea {self.linea_actual}, posicion {self.posicion_actual}")

    def expresion(self):
        if self.tokens[self.posicion_actual][0] in ['ENTERO', 'DECIMAL', 'CADENA', 'CONST_LOGICA']:
            self.avanzar()
        elif self.tokens[self.posicion_actual][0] == 'IDENTIFICADOR':
            self.avanzar()
        elif self.tokens[self.posicion_actual][0] in ['OP_ARITMETICO', 'OP_LOGICO', 'OP_RELACIONAL']:
            self.avanzar()
            self.expresion()
        else:
            raise SyntaxError(f"Expresión inválida en la linea {self.linea_actual}, posicion {self.posicion_actual}")
        
    def declaracion_funcion(self):
        self.tipo()
        self.identificador()
        if self.tokens[0][0] == 'DELIMITADOR' and self.tokens[0][1] == '(':
            self.avanzar()
            self.lista_parametros()
            if self.tokens[0][0] == 'DELIMITADOR' and self.tokens[0][1] == ')':
                self.avanzar()
                self.sentencia_compuesta()
            else:
                raise SyntaxError(f"Se esperaba ')' en la línea {self.linea_actual}, posición {self.posicion_actual}")
        else:
            raise SyntaxError(f"Se esperaba '(' en la línea {self.linea_actual}, posición {self.posicion_actual}")
        
    def lista_parametros(self):
        if self.tokens[self.posicion_actual][0] == 'RESERVADA' and self.tokens[self.posicion_actual][1] in ['nulo', 'entero', 'decimal', 'palabra', 'logico']:
            self.tipo()
            self.identificador()
            while self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == ',':
                self.avanzar()
                self.tipo()
                self.identificador()

    def sentencia_compuesta(self):
        if self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == '{':
            self.avanzar()
            while self.tokens and self.tokens[self.posicion_actual][0] != 'DELIMITADOR' and self.tokens[self.posicion_actual][1] != '}':
                self.sentencia()
            if self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == '}':
                self.avanzar()
            else:
                raise SyntaxError(f"Se esperaba '}}' en la línea {self.linea_actual}, posición {self.posicion_actual}")
        else:
            raise SyntaxError(f"Se esperaba '{{' en la línea {self.linea_actual}, posición {self.posicion_actual}")

    def sentencia(self):
        if self.tokens[self.posicion_actual][0] == 'RESERVADA' and self.tokens[self.posicion_actual][1] in ['nulo', 'entero', 'decimal', 'palabra', 'logico', 'constante']:
            self.declaracion()
        elif self.tokens[self.posicion_actual][0] == 'RESERVADA' and self.tokens[self.posicion_actual][1] == 'si':
            self.sentencia_seleccion()
        elif self.tokens[self.posicion_actual][0] == 'RESERVADA' and self.tokens[self.posicion_actual][1] in ['desde', 'mientras', 'repite']:
            self.sentencia_iteracion()
        elif self.tokens[self.posicion_actual][0] == 'RESERVADA' and self.tokens[self.posicion_actual][1] in ['imprime', 'imprimenl']:
            self.sentencia_imprimir()
        elif self.tokens[self.posicion_actual][0] == 'RESERVADA' and self.tokens[self.posicion_actual][1] == 'regresa':
            self.sentencia_retorno()
        elif self.tokens[self.posicion_actual][0] == 'IDENTIFICADOR':
            self.sentencia_asignacion()
        else:
            raise SyntaxError(f"Sentencia inválida en la línea {self.linea_actual}, posición {self.posicion_actual}")
        
    def sentencia_seleccion(self):
        if self.tokens[self.posicion_actual][0] == 'RESERVADA' and self.tokens[self.posicion_actual][1] == 'si':
            self.avanzar()
            if self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == '(':
                self.avanzar()
                self.expresion()
                if self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == ')':
                    self.avanzar()
                    self.sentencia_compuesta()
                    if self.tokens[self.posicion_actual][0] == 'RESERVADA' and self.tokens[self.posicion_actual][1] == 'sino':
                        self.avanzar()
                        self.sentencia_compuesta()
                else:
                    raise SyntaxError(f"Se esperaba ')' en la línea {self.linea_actual}, posición {self.posicion_actual}")
            else:
                raise SyntaxError(f"Se esperaba '(' en la línea {self.linea_actual}, posición {self.posicion_actual}")
        else:
            raise SyntaxError(f"Se esperaba 'si' en la línea {self.linea_actual}, posición {self.posicion_actual}")

    def sentencia_iteracion(self):
        if self.tokens[self.posicion_actual][0] == 'RESERVADA' and self.tokens[self.posicion_actual][1] == 'desde':
            self.avanzar()
            self.expresion()
            if self.tokens[self.posicion_actual][0] == 'RESERVADA' and self.tokens[self.posicion_actual][1] == 'hasta':
                self.avanzar()
                self.expresion()
                if self.tokens[self.posicion_actual][0] == 'RESERVADA' and self.tokens[self.posicion_actual][1] == 'incr':
                    self.avanzar()
                    self.expresion()
                self.sentencia_compuesta()
            elif self.tokens[self.posicion_actual][0] == 'RESERVADA' and self.tokens[self.posicion_actual][1] == 'mientras':
                self.avanzar()
                self.expresion()
                self.sentencia_compuesta()
            elif self.tokens[self.posicion_actual][0] == 'RESERVADA' and self.tokens[self.posicion_actual][1] == 'repite':
                self.avanzar()
                while self.tokens and (self.tokens[self.posicion_actual][0] != 'RESERVADA' or self.tokens[self.posicion_actual][1] != 'hasta') :
                    self.sentencia()
                if self.tokens[self.posicion_actual][0] == 'RESERVADA' and self.tokens[self.posicion_actual][1] == 'hasta':
                    self.avanzar()
                    self.expresion()
                else:
                    raise SyntaxError(f"Se esperaba 'hasta' en la línea {self.linea_actual}, posición {self.posicion_actual}")
        else:
            raise SyntaxError(f"Sentencia de iteración inválida en la línea {self.linea_actual}, posición {self.posicion_actual}")

    def sentencia_imprimir(self):
        if self.tokens[self.posicion_actual][0] == 'RESERVADA' and self.tokens[self.posicion_actual][1] in ['imprime', 'imprimenl']:
            self.avanzar()
            if self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == '(':
                self.avanzar()
                self.expresion()
                if self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == ')':
                    self.avanzar()
                    if self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == ';':
                        self.avanzar()
                    else:
                        raise SyntaxError(f"Se esperaba ';' en la línea {self.linea_actual}, posición {self.posicion_actual}")
                else:
                    raise SyntaxError(f"Se esperaba ')' en la línea {self.linea_actual}, posición {self.posicion_actual}")
            else:
                raise SyntaxError(f"Se esperaba '(' en la línea {self.linea_actual}, posición {self.posicion_actual}")
        else:
            raise SyntaxError(f"Se esperaba 'imprime' o 'imprimenl' en la línea {self.linea_actual}, posición {self.posicion_actual}")

    def sentencia_retorno(self):
        if self.tokens[self.posicion_actual][0] == 'RESERVADA' and self.tokens[self.posicion_actual][1] == 'regresa':
            self.avanzar()
            self.expresion()
            if self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == ';':
                self.avanzar()
            else:
                raise SyntaxError(f"Se esperaba ';' en la línea {self.linea_actual}, posición {self.posicion_actual}")
        else:
            raise SyntaxError(f"Se esperaba 'regresa' en la línea {self.linea_actual}, posición {self.posicion_actual}")

    def sentencia_asignacion(self):
        self.identificador()
        if self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == '=':
            self.avanzar()
            self.expresion()
            if self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == ';':
                self.avanzar()
            else:
                raise SyntaxError(f"Se esperaba ';' en la línea {self.linea_actual}, posición {self.posicion_actual}")
        else:
            raise SyntaxError(f"Se esperaba '=' en la línea {self.linea_actual}, posición {self.posicion_actual}")
        
    def funcion_principal(self):
        if self.tokens[self.posicion_actual][0] == 'RESERVADA' and self.tokens[self.posicion_actual][1] == 'nulo':
            self.avanzar()
        if self.tokens[self.posicion_actual][0] == 'RESERVADA' and self.tokens[self.posicion_actual][1] == 'principal':
            if self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == '(':
                self.avanzar()
                if self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == ')':
                    self.avanzar()
                    self.sentencia_compuesta()
                else:
                    raise SyntaxError(f"Se esperaba ')' en la línea {self.linea_actual}, posición {self.posicion_actual}")
            else:
                raise SyntaxError(f"Se esperaba '(' en la línea {self.linea_actual}, posición {self.posicion_actual}")
        else:
            raise SyntaxError(f"Se esperaba 'principal' en la línea {self.linea_actual}, posición {self.posicion_actual}")

        while self.tokens and self.tokens[self.posicion_actual][0] != 'DELIMITADOR' and self.tokens[self.posicion_actual][1] != '}':
            self.sentencia()

        if self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == '}':
            self.avanzar()
        else:
            raise SyntaxError(f"Se esperaba '}}' en la línea {self.linea_actual}, posición {self.posicion_actual}")
        
    def __call__(self, tokens):
        self.tokens = tokens
        self.posicion_actual = 0
        self.linea_actual = 0
        self.programa()

    def avanzar(self):
        self.posicion_actual += 1
        if self.posicion_actual >= len(self.tokens):
            raise SyntaxError(f"Se esperaba un token en la línea {self.linea_actual}, posición {self.posicion_actual}")

    def get_token(self):
        return self.tokens[self.posicion_actual]

    def get_linea(self):
        return self.linea_actual

    def set_linea(self, linea):
        self.linea_actual = linea
