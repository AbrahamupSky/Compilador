import sys

class SyntacticAnalyzer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.posicion_actual = 0
        self.linea_actual = 0

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

    def declaracion_funcion(self):
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

    def lista_parametros(self):
        if self.tokens[self.posicion_actual][0] == 'RESERVADA' and self.tokens[self.posicion_actual][1] in ['nulo', 'entero', 'decimal', 'palabra', 'logico']:
            self.tipo()
            self.identificador()
            while self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == ',':
                self.avanzar()
                if self.tokens[self.posicion_actual][0] == 'RESERVADA' and self.tokens[self.posicion_actual][1] in ['nulo', 'entero', 'decimal', 'palabra', 'logico']:
                    self.tipo()
                    self.identificador()
                else:
                    print(f"Se esperaba un tipo de dato en la línea {self.tokens[self.posicion_actual][2]}")
                    sys.exit()
        else:
            print(f"Se esperaba un tipo de dato en la línea {self.tokens[self.posicion_actual][2]}")
            sys.exit()

    def sentencia_compuesta(self):
        if self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == '{':
            self.avanzar()

            while self.tokens[self.posicion_actual][0] != 'DELIMITADOR' or self.tokens[self.posicion_actual][1] != '}':
                self.sentencia()

            if self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == '}':
                self.avanzar()
            else:
                print(f"Se esperaba '}}' en la línea {self.tokens[self.posicion_actual][2]}")
                sys.exit()
        else:
        
            print(f"Se esperaba '{{' en la línea {self.tokens[self.posicion_actual][2]}")
            sys.exit()

    def tipo(self):
        if self.tokens[self.posicion_actual][0] == 'RESERVADA' and self.tokens[self.posicion_actual][1] in ['nulo', 'entero', 'decimal', 'palabra', 'logico']:
            self.avanzar()
            if self.tokens[self.posicion_actual][0] == 'IDENTIFICADOR':
                if self.tokens[self.posicion_actual+1][1] == '(':
                    self.declaracion_funcion()
        else:
            print(f"Se esperaba un tipo de dato en la línea {self.tokens[self.posicion_actual][2]}")
            sys.exit()

    def declaracion_variable(self):
        if self.tokens[self.posicion_actual][0] == 'IDENTIFICADOR':
            self.identificador()
        

        if (self.tokens[self.posicion_actual][0] == 'DELIMITADOR'and self.tokens[self.posicion_actual][1] == '['):
            self.avanzar()  # Avance sobre '['
            if (self.tokens[self.posicion_actual][0] == 'ENTERO'or self.tokens[self.posicion_actual][0] == 'IDENTIFICADOR'):
                self.avanzar()  # Avance sobre el tamaño del arreglo
            else:
                print(f"Se esperaba un número entero o identificador en la línea {self.tokens[self.posicion_actual][2]}")
                sys.exit()

            if (self.tokens[self.posicion_actual][0] == 'DELIMITADOR'and self.tokens[self.posicion_actual][1] == ']'):
                self.avanzar()  # Avance sobre ']'
                if self.tokens[self.posicion_actual+1][1] == '{':
                    self.declaracion_arreglo()
            else:
                print(f"Se esperaba ']' en la línea {self.tokens[self.posicion_actual][2]}")

        while self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == ',':
            self.avanzar()
            self.identificador()

        if self.tokens[self.posicion_actual][1] == '=':
            self.avanzar()
            while self.tokens[self.posicion_actual][1] != ';':
                self.expresion()

        if self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == ';':
            self.avanzar()
        else:
            print(f"Se esperaba ';' en la línea {self.tokens[self.posicion_actual][2]}")
            sys.exit()

    def declaracion_arreglo(self):
        if self.tokens[self.posicion_actual][1] == '=':
            self.avanzar()
            if self.tokens[self.posicion_actual][1] == '{':
                self.avanzar()
                if self.tokens[self.posicion_actual][0] == 'IDENTIFICADOR' or self.tokens[self.posicion_actual][0] == 'ENTERO' or self.tokens[self.posicion_actual][0] == 'DECIMAL'or self.tokens[self.posicion_actual][0] == 'CADENA':
                    self.avanzar()
                    while self.tokens[self.posicion_actual][1] == ',': 
                        if self.tokens[self.posicion_actual][1] == ',':
                            self.avanzar()
                        
                        if self.tokens[self.posicion_actual][1] == '-':
                            self.avanzar()
                        if self.tokens[self.posicion_actual][0] == 'IDENTIFICADOR' or self.tokens[self.posicion_actual][0] == 'ENTERO' or self.tokens[self.posicion_actual][0] == 'DECIMAL'or self.tokens[self.posicion_actual][0] == 'CADENA':
                            self.avanzar()
                        else:
                            print(f"Valor incorrecto en en arreglo en la línea {self.tokens[self.posicion_actual][2]}")
                            sys.exit()

                else:
                 
                    print(f"Valor incorrecto en en arreglo en la línea {self.tokens[self.posicion_actual][2]}")
                    sys.exit()
                if self.tokens[self.posicion_actual][1] == '}':
                    self.avanzar()
                else:
                 
                    print(f"Se esperaba '}}' en la línea {self.tokens[self.posicion_actual][2]}")
                    sys.exit()
            else:
                print(f"Se esperaba '{{' en la línea {self.tokens[self.posicion_actual][2]}")
                sys.exit()
        else:
            print(f"Se esperaba '=' en la línea {self.tokens[self.posicion_actual][2]}")
            sys.exit()
        

    def identificador(self):
        if self.tokens[self.posicion_actual][1] == '*':
            self.avanzar()
        if self.tokens[self.posicion_actual][0] == 'IDENTIFICADOR':
        
            self.avanzar()
        else:
            print(f"Se esperaba un identificador en la línea {self.tokens[self.posicion_actual][2]}")
            sys.exit()

    def val_arreglo(self):
        if self.tokens[self.posicion_actual][0] in ['ENTERO', 'IDENTIFICADOR']:
            self.avanzar()
            if self.tokens[self.posicion_actual][0] == 'OP_ARITMETICO':
                self.avanzar()
                self.val_arreglo()
        else:
            print(f"Se esperaba un entero o identificador en la línea {self.tokens[self.posicion_actual][2]}")
            sys.exit()

    def expresion(self):
    
        if self.tokens[self.posicion_actual][0] in ['ENTERO', 'DECIMAL', 'CADENA', 'CONST_LOGICA']:
            self.avanzar()
        elif self.tokens[self.posicion_actual][0] == 'IDENTIFICADOR':
            self.avanzar()
            if self.tokens[self.posicion_actual][1] == '[':
                self.avanzar()
                self.val_arreglo()
            
                if self.tokens[self.posicion_actual][1] == ']':
                    self.avanzar()
                else:
                    print(f"Se esperaba ']' en la línea {self.tokens[self.posicion_actual][2]}")
                    sys.exit()
            if self.tokens[self.posicion_actual][1] == '(':
                self.avanzar()
                while self.tokens[self.posicion_actual][0] != 'DELIMITADOR':
                    self.expresion()
                if self.tokens[self.posicion_actual][1] == ')':
                    self.avanzar()
                else:
                    print(f"Se esperaba ')' en la línea {self.tokens[self.posicion_actual][2]}")
                    sys.exit()
        elif self.tokens[self.posicion_actual][0] in ['OP_ARITMETICO', 'OP_LOGICO', 'OP_RELACIONAL']:
            self.avanzar()
        
            #self.expresion()
        else:
            print(f"Expresión inválida en la línea {self.tokens[self.posicion_actual][2]}")
            sys.exit()

    def funcion_principal(self):
        if self.tokens[self.posicion_actual][0] == 'RESERVADA' and self.tokens[self.posicion_actual][1] == 'principal':
            self.avanzar()
            if self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == '(':
                self.avanzar()
                if self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == ')':
                    self.avanzar()
                    if self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == '{':
                        self.avanzar()
                        while self.posicion_actual < len(self.tokens) and self.tokens[self.posicion_actual][1] != '}':
                            self.sentencia()
                        if self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == '}':
                            self.avanzar()
                        else:
                            print(f"Se esperaba '}}' en la línea {self.tokens[self.posicion_actual][2]}")
                            sys.exit()
                    else:
                        print(f"Se esperaba '{{' en la línea {self.tokens[self.posicion_actual][2]}")
                        sys.exit()
                else:
                    print(f"Se esperaba ')' en la línea {self.tokens[self.posicion_actual][2]}")
                    sys.exit()
            else:
                print(f"Se esperaba '(' en la línea {self.tokens[self.posicion_actual][2]}")
                sys.exit()
        else:
            print(f"Se esperaba la función principal en la línea {self.tokens[self.posicion_actual][2]}")
            sys.exit()

    def sentencia(self):
        if self.tokens[self.posicion_actual][0] == 'RESERVADA' and self.tokens[self.posicion_actual][1] in ['si', 'mientras', 'hacer', 'imprime', 'lee','desde','repite','imprimenl','regresa']:
            if self.tokens[self.posicion_actual][1] == 'si':
                self.sentencia_si()
            elif self.tokens[self.posicion_actual][1] == 'mientras':
                self.sentencia_mientras()
            elif self.tokens[self.posicion_actual][1] == 'hacer':
                self.sentencia_hacer()
            elif self.tokens[self.posicion_actual][1] == 'imprime' or self.tokens[self.posicion_actual][1] == 'imprimenl' :
                self.sentencia_imprime()
            elif self.tokens[self.posicion_actual][1] == 'lee':
                self.sentencia_lee()
            elif self.tokens[self.posicion_actual][1] == 'desde':
                self.sentencia_desde()
            elif self.tokens[self.posicion_actual][1] == 'repite':
                self.sentencia_repite()
            elif self.tokens[self.posicion_actual][1] == 'regresa':
                self.sentencia_regresa()
        else:
            self.declaracion()

    def sentencia_regresa(self):
        self.avanzar()
        while self.tokens[self.posicion_actual][1] != ';':
            self.expresion()
        if self.tokens[self.posicion_actual][1] == ';':
            self.avanzar()
        else:
            print(f"Se esperaba ; en la línea {self.tokens[self.posicion_actual][2]}")
            sys.exit()

    def sentencia_desde(self):
        self.avanzar()
        while self.tokens[self.posicion_actual][1] != 'hasta':
            self.expresion()
        if self.tokens[self.posicion_actual][0] == 'RESERVADA' and self.tokens[self.posicion_actual][1] == 'hasta':
            self.avanzar()
            while self.tokens[self.posicion_actual][1] != 'incr':
                self.expresion()
        
            if self.tokens[self.posicion_actual][1] == 'incr':
                self.avanzar()
                self.expresion()
                #self.sentencia_compuesta()
            else:
                print(f"Se esperaba 'incr' en la línea {self.tokens[self.posicion_actual][2]}")
                sys.exit()
        else:
            print(f"Se esperaba 'hasta' en la línea {self.tokens[self.posicion_actual][2]}")
            sys.exit()
        
    def sentencia_repite(self):
        self.avanzar()
        if self.tokens[self.posicion_actual][1] == '{':
            self.avanzar()
            while self.tokens[self.posicion_actual][1] != '}':
                self.sentencia()
                # + 'debug')
            if self.tokens[self.posicion_actual][1] == '}':
                self.avanzar()
                if self.tokens[self.posicion_actual][1] == 'hasta':
                    self.avanzar()
                    if self.tokens[self.posicion_actual][1] == 'que':
                        self.avanzar()
                        while self.tokens[self.posicion_actual][1] != ';':
                            self.expresion()
                        if self.tokens[self.posicion_actual][1] == ';':
                            self.avanzar()
                        else:
                            print(f"Se esperaba ';' en la línea {self.tokens[self.posicion_actual][2]}")
                    else:
                        print(f"Se esperaba 'que' en la línea {self.tokens[self.posicion_actual][2]}")
                        sys.exit()    
                else:
                    print(f"Se esperaba 'hasta' en la línea {self.tokens[self.posicion_actual][2]}")
                    sys.exit()                    
            else:
                print(f"Se esperaba '}}' en la línea {self.tokens[self.posicion_actual][2]}")
                sys.exit()
        else:
            print(f"Se esperaba '{{' en la línea {self.tokens[self.posicion_actual][2]}")
            sys.exit()

    def sentencia_si(self):
        if self.tokens[self.posicion_actual][0] == 'RESERVADA' and self.tokens[self.posicion_actual][1] == 'si':
            self.avanzar()
            while self.tokens[self.posicion_actual][1] != 'hacer':
                self.expresion()
            
            if self.tokens[self.posicion_actual][1] == 'hacer':
                self.avanzar()
                if self.tokens[self.posicion_actual][1] == 'regresa':
                    self.avanzar()
                    while self.tokens[self.posicion_actual][1] != ';':
                        self.expresion()
                    if self.tokens[self.posicion_actual][1] == ';':
                        self.avanzar()
                        self.sentencia_sino()
                    else:
                        print(f"Se esperaba ';' en la línea {self.tokens[self.posicion_actual][2]}")
                        sys.exit()
                elif self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == '{':
                    self.avanzar()
                    while self.posicion_actual < len(self.tokens) and self.tokens[self.posicion_actual][1] != '}':
                        self.sentencia()
                    if self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == '}':
                        self.avanzar()
                        self.sentencia_sino()
                    else:
                        print(f"Se esperaba '}}' en la línea {self.tokens[self.posicion_actual][2]}")
                        sys.exit()
                else:
                
                    print(f"Se esperaba '{{' o 'regresa' en la línea {self.tokens[self.posicion_actual][2]}")
                    sys.exit()
            else:
                print(f"Se esperaba 'hacer' en la línea {self.tokens[self.posicion_actual][2]}")
                sys.exit()
        else:
            print(f"Se esperaba 'si' en la línea {self.tokens[self.posicion_actual][2]}")
            sys.exit()

    def sentencia_sino(self):
        if self.tokens[self.posicion_actual][0] == 'RESERVADA' and self.tokens[self.posicion_actual][1] == 'sino':
            self.avanzar()
            if self.tokens[self.posicion_actual][1] == 'regresa':
                self.avanzar()
                while self.tokens[self.posicion_actual][1] != ';':
                
                    self.expresion()
                if self.tokens[self.posicion_actual][1] == ';':
                    self.avanzar()
                else:
                    print(f"Se esperaba ';' en la línea {self.tokens[self.posicion_actual][2]}")
                    sys.exit()
            elif self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == '{':
                self.avanzar()
                while self.posicion_actual < len(self.tokens) and self.tokens[self.posicion_actual][1] != '}':
                    self.sentencia()
                if self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == '}':
                    self.avanzar()
                else:
                    print(f"Se esperaba '}}' en la línea {self.tokens[self.posicion_actual][2]}")
                    sys.exit()
            else:
                print(f"Se esperaba '{{' o 'regresa' en la línea {self.tokens[self.posicion_actual][2]}")
                sys.exit()

    def sentencia_mientras(self):
        if self.tokens[self.posicion_actual][0] == 'RESERVADA' and self.tokens[self.posicion_actual][1] == 'mientras':
            self.avanzar()
            if self.tokens[self.posicion_actual][1] == 'que':
                self.avanzar()
                while self.tokens[self.posicion_actual][1] != '{':
                    self.expresion()
                if self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == '{':
                    self.avanzar()
                    while self.posicion_actual < len(self.tokens) and self.tokens[self.posicion_actual][1] != '}':
                        self.sentencia()
                    if self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == '}':
                        self.avanzar()
                    else:
                        print(f"Se esperaba '}}' en la línea {self.tokens[self.posicion_actual][2]}")
                        sys.exit()
                else:
                    print(f"Se esperaba '{{' en la línea {self.tokens[self.posicion_actual][2]}")
                    sys.exit()
            else:
                print(f"Se esperaba 'que' en la línea {self.tokens[self.posicion_actual][2]}")
        else:
            print(f"Se esperaba 'mientras' en la línea {self.tokens[self.posicion_actual][2]}")
            sys.exit()

    def sentencia_hacer(self):
        if self.tokens[self.posicion_actual][0] == 'RESERVADA' and self.tokens[self.posicion_actual][1] == 'hacer':
            self.avanzar()
            if self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == '{':
                self.avanzar()
                while self.posicion_actual < len(self.tokens) and self.tokens[self.posicion_actual][1] != '}':
                    self.sentencia()
                if self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == '}':
                    self.avanzar()
                    if self.tokens[self.posicion_actual][0] == 'RESERVADA' and self.tokens[self.posicion_actual][1] == 'mientras':
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
                        print(f"Se esperaba 'mientras' en la línea {self.tokens[self.posicion_actual][2]}")
                        sys.exit()
                else:
                    print(f"Se esperaba '}}' en la línea {self.tokens[self.posicion_actual][2]}")
                    sys.exit()
            else:
                print(f"Se esperaba '{{' en la línea {self.tokens[self.posicion_actual][2]}")
                sys.exit()
        else:
            print(f"Se esperaba 'hacer' en la línea {self.tokens[self.posicion_actual][2]}")
            sys.exit()

    def sentencia_imprime(self):
        self.avanzar()
        if self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == '(':
            self.avanzar()
            while self.tokens[self.posicion_actual][1] != ')':
                if self.tokens[self.posicion_actual][1] == ',':
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

    def sentencia_lee(self):
        self.avanzar()
        if self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == '(':
            self.avanzar()
        
            self.variable()
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

    def asignacion(self):
        self.variable()
        if self.tokens[self.posicion_actual][1] == '=':
            self.avanzar()
            self.expresion()
            if self.tokens[self.posicion_actual][0] == 'DELIMITADOR' and self.tokens[self.posicion_actual][1] == ';':
                self.avanzar()
            else:
            
                print(f"Se esperaba ';' en la línea {self.tokens[self.posicion_actual][2]}")
                sys.exit()
        else:
            print(f"Se esperaba un operador de asignación en la línea {self.tokens[self.posicion_actual][2]}")
            sys.exit()

    def variable(self):
        if self.tokens[self.posicion_actual][0] == 'IDENTIFICADOR':
            self.avanzar()
        else:
            print(f"Se esperaba un identificador en la línea {self.tokens[self.posicion_actual][2]}")
            sys.exit()

    def avanzar(self):
        self.posicion_actual += 1
        if self.posicion_actual >= len(self.tokens):
            print('compilo con exito')
            raise StopIteration


    def get_token(self):
        return self.tokens[self.posicion_actual]

    def get_linea(self):
        return self.linea_actual

    def set_linea(self, linea):
        self.linea_actual = linea


