import sys

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}

    def analyze(self, tokens):
        self.tokens = tokens
        self.posicion_actual = 0
        self.linea_actual = 0
        self.programa()

    def programa(self):
        while self.posicion_actual < len(self.tokens) and self.tokens[self.posicion_actual][1] != 'principal':
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
            print(f"Se esperaba una declaración en la línea {self.tokens[self.posicion_actual][2]}")
            sys.exit()

    def tipo(self):
        if self.tokens[self.posicion_actual][0] == 'RESERVADA' and self.tokens[self.posicion_actual][1] in ['nulo', 'entero', 'decimal', 'palabra', 'logico']:
            self.avanzar()
        else:
            print(f"Se esperaba un tipo de dato en la línea {self.tokens[self.posicion_actual][2]}")
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
            print(f"Se esperaba ';' en la línea {self.tokens[self.posicion_actual][2]}")
            sys.exit()

    def identificador(self):
        if self.tokens[self.posicion_actual][0] == 'IDENTIFICADOR':
            # Add identifier to symbol table
            identifier = self.tokens[self.posicion_actual][1]
            if identifier in self.symbol_table:
                print(f"Error: Identificador '{identifier}' ya ha sido declarado en la línea {self.tokens[self.posicion_actual][2]}")
                sys.exit()
            else:
                self.symbol_table[identifier] = None
            self.avanzar()
        else:
            print(f"Se esperaba un identificador en la línea {self.tokens[self.posicion_actual][2]}")
            sys.exit()

    def expresion(self):
        if self.tokens[self.posicion_actual][0] in ['ENTERO', 'DECIMAL', 'CADENA', 'CONST_LOGICA']:
            self.avanzar()
        elif self.tokens[self.posicion_actual][0] == 'IDENTIFICADOR':
            # Check if identifier has been declared
            identifier = self.tokens[self.posicion_actual][1]
            if identifier not in self.symbol_table:
                print(f"Error: Identificador '{identifier}' no ha sido declarado en la línea {self.tokens[self.posicion_actual][2]}")
                sys.exit()
            self.avanzar()
        elif self.tokens[self.posicion_actual][0] == 'OPERADOR':
            self.avanzar()
            self.expresion()
        else:
            print(f"Expresión inválida en la línea {self.tokens[self.posicion_actual][2]}")
            sys.exit()

    def funcion_principal(self):
        if self.tokens[self.posicion_actual][0] == 'RESERVADA' and self.tokens[self.posicion_actual][1] == 'principal':
            self.avanzar()
        else:
            print(f"Se esperaba la función principal en la línea {self.tokens[self.posicion_actual][2]}")
            sys.exit()

    def avanzar(self):
        self.posicion_actual += 1

