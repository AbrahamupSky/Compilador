import sys

class SemanticAnalyzer:

    def __init__(self, tokens):
        self.tokens = tokens
        self.posicion_actual = 0
        self.linea_actual = 0
        self.current_scope = 'global'  # ambito actual
        self.symbol_table = {}  # Tabla de simbolos

    def programa(self):
        while self.posicion_actual < len(self.tokens) and self.tokens[self.posicion_actual][1] != 'principal':
            self.declaracion()

        self.funcion_principal()

        # Verificar variables no utilizadas
        self.verificar_variables_no_utilizadas()

    def declaracion(self):
        if self.tokens[self.posicion_actual][0] == 'RESERVADA' and self.tokens[self.posicion_actual][1] == 'constante':
            self.avanzar()
            self.tipo()
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
        elif self.tokens[self.posicion_actual][0] == 'RESERVADA' and self.tokens[self.posicion_actual][1] in ['nulo', 'entero', 'decimal', 'palabra', 'logico']:
            self.tipo()
            self.declaracion_variable()
        elif self.tokens[self.posicion_actual][0] == 'IDENTIFICADOR':
            self.declaracion_variable()
        else:
            print(f"Se esperaba una declaración en la línea {self.tokens[self.posicion_actual][2]}")
            sys.exit()

    def tipo(self):
        if self.tokens[self.posicion_actual][0] == 'RESERVADA' and self.tokens[self.posicion_actual][1] in ['nulo', 'entero', 'decimal', 'palabra', 'logico']:
            self.avanzar()
        else:
            print(f"Se esperaba un tipo de dato en la línea {self.tokens[self.posicion_actual][2]}")
            sys.exit()

    def declaracion_variable(self):
        self.tipo()
        self.identificador()

        while self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == ',':
            self.avanzar()
            self.identificador()

        if self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == ';':
            self.avanzar()
        else:
            print(f"Se esperaba ';' en la línea {self.tokens[self.posicion_actual][2]}")
            sys.exit()

    def identificador(self):
        if self.tokens[self.posicion_actual][0] == 'IDENTIFICADOR':
            # Agregar el identificador a la tabla de símbolos
            self.agregar_simbolo(self.tokens[self.posicion_actual][1], 'variable')
            self.avanzar()
        else:
            print(f"Se esperaba un identificador en la línea {self.tokens[self.posicion_actual][2]}")
            sys.exit()

    def expresion(self):
        if self.tokens[self.posicion_actual][0] in ['ENTERO', 'DECIMAL', 'CADENA', 'CONST_LOGICA']:
            self.avanzar()
        elif self.tokens[self.posicion_actual][0] == 'IDENTIFICADOR':
            self.verificar_identificador(self.tokens[self.posicion_actual][1])
            self.avanzar()
        elif self.tokens[self.posicion_actual][0] in ['OP_ARITMETICO', 'OP_LOGICO', 'OP_RELACIONAL']:
            self.avanzar()
            self.expresion()
        else:
            print(f"Expresión inválida en la línea {self.tokens[self.posicion_actual][2]}")
            sys.exit()

    def declaracion_funcion(self):
        if self.tokens[self.posicion_actual][0] == 'RESERVADA' and self.tokens[self.posicion_actual][1] in ['nulo', 'entero', 'decimal', 'palabra', 'logico']:
            self.tipo()
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

            # Crear un nuevo ambito para la función
            self.nuevo_ambito()

            while self.tokens[self.posicion_actual][0] != 'DELIMITADOR' and self.tokens[self.posicion_actual][1] != '}':
                self.sentencia()

            # Salir del ambito de la función
            self.salir_ambito()

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
                self.sentencia_compuesta()
                self.expresion()

            else:
                print(f"Sentencia de iteración inválida en la línea {self.tokens[self.posicion_actual][2]}")
                sys.exit()

        else:
            print(f"Sentencia de iteración inválida en la línea {self.tokens[self.posicion_actual][2]}")
            sys.exit()

    def sentencia_imprimir(self):
        if self.tokens[self.posicion_actual][0] == 'RESERVADA' and self.tokens[self.posicion_actual][1] in ['imprime', 'imprimenl']:
            self.avanzar()

            if self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == '(':
                self.avanzar()
                self.lista_expresiones()

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
            print(f"Sentencia de impresión inválida en la línea {self.tokens[self.posicion_actual][2]}")
            sys.exit()

    def lista_expresiones(self):
        self.expresion()

        while self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == ',':
            self.avanzar()
            self.expresion()

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
            print(f"Sentencia de retorno inválida en la línea {self.tokens[self.posicion_actual][2]}")
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

    def avanzar(self):
        self.posicion_actual += 1

    def agregar_simbolo(self, nombre, tipo):
        if nombre in self.symbol_table:
            print(f"Error: El símbolo {nombre} ya ha sido declarado en el ámbito actual.")
            sys.exit()
        else:
            self.symbol_table[nombre] = {'tipo': tipo, 'ambito': self.current_scope}

    def verificar_identificador(self, nombre):
        if nombre not in self.symbol_table:
            print(f"Error: El identificador {nombre} no ha sido declarado en el ámbito actual.")
            sys.exit()

    def nuevo_ambito(self):
        self.current_scope = f'ambito{self.linea_actual}'

    def salir_ambito(self):
        self.current_scope = 'global'

    def verificar_variables_no_utilizadas(self):
        for simbolo in self.symbol_table:
            if self.symbol_table[simbolo]['ambito'] == 'global':
                print(f"Advertencia: La variable {simbolo} declarada en el ámbito global no se utiliza.")

    def analizar(self):
        self.programa()

def analizador_semantico(tokens):
    analizador = SemanticAnalyzer(tokens)
    analizador.analizar()

