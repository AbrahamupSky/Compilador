import sys

class SyntacticAnalyzer:

    def __init__(self, tokens):
        self.tokens = tokens
        self.posicion_actual = 0
        self.linea_actual = 0

    def programa(self):
        while self.posicion_actual < len(self.tokens) and self.tokens[self.posicion_actual][1] != 'principal':
            print(self.tokens[self.posicion_actual])
            self.declaracion()
            
        self.funcion_principal()


    def declaracion(self):
        if self.tokens[self.posicion_actual][0] == 'RESERVADA' and self.tokens[self.posicion_actual][1] == 'constante':
            self.avanzar()
        elif self.tokens[self.posicion_actual][0] == 'RESERVADA' and self.tokens[self.posicion_actual][1] in ['nulo', 'entero', 'decimal', 'palabra', 'logico']:
            self.tipo()
        elif self.tokens[self.posicion_actual][0] == 'IDENTIFICADOR':
            self.declaracion_variable()
        else:
            print(f"Se esperaba una declaracion en la linea {self.tokens[self.posicion_actual][2]}")
            sys.exit()

    def tipo(self):
        if self.tokens[self.posicion_actual][0] == 'RESERVADA' and self.tokens[self.posicion_actual][1] in ['nulo', 'entero', 'decimal', 'palabra', 'logico']:
            if self.tokens[self.posicion_actual+1][0] == 'IDENTIFICADOR':
                if self.tokens[self.posicion_actual+2][1] == '(':
                    print(self.tokens[self.posicion_actual])
                    self.declaracion_funcion()
            self.avanzar()
        else:
            print(f"Se esperaba un tipo de dato en la linea {self.tokens[self.posicion_actual][2]}")
            sys.exit()

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
            print(f"Se esperaba ';' en la linea {self.tokens[self.posicion_actual][2]}")
            sys.exit()

    def identificador(self):
        if self.tokens[self.posicion_actual][0] == 'IDENTIFICADOR':
            print(self.tokens[self.posicion_actual])
            self.avanzar()
        else:
            print(self.tokens[self.posicion_actual])
            print(f"Se esperaba un identificador en la linea {self.tokens[self.posicion_actual][2]}")
            sys.exit()

    def expresion(self):
        if self.tokens[self.posicion_actual][0] in ['ENTERO', 'DECIMAL', 'CADENA', 'CONST_LOGICA']:
            self.avanzar()
        elif self.tokens[self.posicion_actual][0] == 'IDENTIFICADOR':
            self.avanzar()

        elif self.tokens[self.posicion_actual][0] in ['OP_ARITMETICO', 'OP_LOGICO', 'OP_RELACIONAL']:
            self.avanzar()

            self.expresion()
        else:
            print(self.posicion_actual)
            print(f"Expresión inválida en la linea {self.tokens[self.posicion_actual][2]}")
            sys.exit()
        
    def declaracion_funcion(self):
        if self.tokens[self.posicion_actual][0] == 'RESERVADA' and self.tokens[self.posicion_actual][1] in ['nulo', 'entero', 'decimal', 'palabra', 'logico']:
            self.avanzar()
            print(self.tokens[self.posicion_actual])
            self.identificador()
            if self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == '(':
                self.avanzar()
                self.lista_parametros()
                if self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == ')':
                    self.avanzar()
                    self.sentencia_compuesta()
                else:
                    print(f"Se esperaba ')' en la línea {self.tokens[self.posicion_actual][2]}")
                    sys.exit()
            else:
                print(f"Se esperaba '(' en la línea {self.tokens[self.posicion_actual][2]}")
                sys.exit()
        else:
            print(f"Se esperaba un tipo de dato en la línea {self.tokens[self.posicion_actual][2]}")
            sys.exit()
        
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

            while self.tokens[self.posicion_actual][0] != 'DELIMITADOR' and self.tokens[self.posicion_actual][1] != '}':
    
                self.sentencia()
            if self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == '}':
                self.avanzar()
            else:
                print(f"Se esperaba '}}' en la línea {self.tokens[self.posicion_actual][2]}")
                sys.exit()
        else:
            print(f"Se esperaba '{{' en la línea {self.tokens[self.posicion_actual][2]}")
            sys.exit()

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
            print(f"Sentencia inválida en la línea {self.tokens[self.posicion_actual][2]}")
            sys.exit()
        
    def sentencia_seleccion(self):
        if self.tokens[self.posicion_actual][0] == 'RESERVADA' and self.tokens[self.posicion_actual][1] == 'si':
            self.avanzar()

            if self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == '(':
                self.avanzar()

                while self.tokens[self.posicion_actual][1] != ')':
                    self.expresion()
                if self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == ')':
                    self.avanzar()
                    if self.tokens[self.posicion_actual][1] == 'hacer':
                        self.avanzar()
                        self.sentencia_compuesta()
                    if self.tokens[self.posicion_actual][0] == 'RESERVADA' and self.tokens[self.posicion_actual][1] == 'sino':
                        self.avanzar()
                        self.sentencia_compuesta()
                else:
                    print(f"Se esperaba ')' en la línea {self.tokens[self.posicion_actual][2]}")
                    sys.exit()
            else:
                print(f"Se esperaba '(' en la línea {self.tokens[self.posicion_actual][2]}")
                sys.exit()
        else:
            print(f"Se esperaba 'si' en la línea {self.tokens[self.posicion_actual][2]}")
            sys.exit()

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
                    print(f"Se esperaba 'hasta' en la línea {self.tokens[self.posicion_actual][2]}")
                    sys.exit()
        else:
            print(f"Sentencia de iteración inválida en la línea {self.tokens[self.posicion_actual][2]}")
            sys.exit()

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
                        print(f"Se esperaba ';' en la línea {self.tokens[self.posicion_actual][2]}")
                        sys.exit()
                else:
                    print(f"Se esperaba ')' en la línea {self.tokens[self.posicion_actual][2]}")
                    sys.exit()
            else:
                print(f"Se esperaba '(' en la línea {self.tokens[self.posicion_actual][2]}")
                sys.exit()
        else:
            print(f"Se esperaba 'imprime' o 'imprimenl' en la línea {self.tokens[self.posicion_actual][2]}")
            sys.exit()

    def sentencia_retorno(self):
        if self.tokens[self.posicion_actual][0] == 'RESERVADA' and self.tokens[self.posicion_actual][1] == 'regresa':
            self.avanzar()
            self.expresion()
            if self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == ';':
                self.avanzar()
            else:
                print(f"Se esperaba ';' en la línea {self.tokens[self.posicion_actual][2]}")
                sys.exit()
        else:
            print(f"Se esperaba 'regresa' en la línea {self.tokens[self.posicion_actual][2]}")
            sys.exit()

    def sentencia_asignacion(self):
        self.identificador()
        if self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == '=':
            self.avanzar()
            self.expresion()
            if self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == ';':
                self.avanzar()
            else:
                print(f"Se esperaba ';' en la línea {self.tokens[self.posicion_actual][2]}")
                sys.exit()
        else:
            print(f"Se esperaba '=' en la línea {self.tokens[self.posicion_actual][2]}")
            sys.exit()
        
    def funcion_principal(self):
        if self.tokens[self.posicion_actual][0] == 'RESERVADA' and self.tokens[self.posicion_actual][1] == 'nulo':
            self.avanzar()

        if self.tokens[self.posicion_actual][0] == 'RESERVADA' and self.tokens[self.posicion_actual][1] == 'principal':
            if self.tokens[self.posicion_actual + 1][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual + 1][1] == '(':
                self.avanzar()
                self.avanzar()
    
                if self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == ')':
        
                    self.avanzar()
        
                    self.sentencia_compuesta()
                else:
                    print(f"Se esperaba ')' en la línea {self.tokens[self.posicion_actual][2]}")
                    sys.exit()
            else:
                print(f"Se esperaba '(' en la línea {self.tokens[self.posicion_actual][2]}")
                sys.exit()
        else:
            print(f"Se esperaba 'principal' en la línea {self.tokens[self.posicion_actual][2]}")
            sys.exit()

        while self.tokens and self.tokens[self.posicion_actual][0] != 'DELIMITADOR' and self.tokens[self.posicion_actual][1] != '}':
            self.sentencia()

        if self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == '}':
            self.avanzar()
        else:
            print(f"Se esperaba 'Parentesis Derecho' en la línea {self.tokens[self.posicion_actual][2]}")
            sys.exit()
        
    def __call__(self, tokens):
        self.tokens = tokens
        self.posicion_actual = 0
        self.linea_actual = 0
        self.programa()

    def avanzar(self):
        self.posicion_actual += 1
        if self.posicion_actual >= len(self.tokens):
            print("* El archivo '.icc' compilo con exito *")
            raise StopIteration


    def get_token(self):
        return self.tokens[self.posicion_actual]

    def get_linea(self):
        return self.linea_actual

    def set_linea(self, linea):
        self.linea_actual = linea
