RESERVADAS = ['nulo', 'entero', 'decimal', 'palabra', 'logico', 'constante', 'desde', 'si', 'hasta', 'mientras', 'regresa', 'hacer',
'sino', 'incr', 'imprime', 'imprimenl', 'lee', 'repite', 'que']
OPERADORES_LOGICOS = ['no', 'y', 'o']
CONSTANTES_LOGICAS = ['verdadero', 'falso']
OPERADORES_ARITMETICOS = ['+', '-', '*', '/', '%', '^']
DELIMITADORES = [';', ',', '(', ')', '{', '}', '[', ']', ':', '=', '.']
DELIMITADORES_UNIVERSALES = [' ', '\t', '\n']
OPERADORES_RELACIONALES = ['<', '>', '<=', '>=', '<>', '==']

# Analisis Lexico

def avanzar():
    global pos, texto, char_actual, linea_actual, posicion_actual
    pos += 1
    if pos < len(texto):
        if char_actual == '\n':
            linea_actual += 1
            posicion_actual = 0
        else:
            posicion_actual += 1
        char_actual = texto[pos]
    else:
        char_actual = None

def crear_digitos():
    str_num = ''
    puntos = 0
    while char_actual is not None and char_actual.isdigit() or char_actual == '.':
        if char_actual == '.':
            if puntos == 1:
                break
            puntos += 1
            str_num += '.'
        else:
            str_num += char_actual
        avanzar()

    if puntos == 0:
        return ('ENTERO', int(str_num))
    else:
        return ('DECIMAL', float(str_num))

def crear_cadena():
    str_cadena = ''
    avanzar()  # Avanza sobre la comilla inicial

    while char_actual is not None and char_actual != '"':
        str_cadena += char_actual
        avanzar()

    if char_actual == '"':
        avanzar()  # Avanza sobre la comilla final
        return ('CADENA', str_cadena)
    else:
        raise SyntaxError(f"Cadena de texto no cerrada en la línea {linea_actual}, posición {posicion_actual}")

def lexer(input):
    global pos, texto, char_actual, linea_actual, posicion_actual
    pos = -1
    texto = input
    char_actual = None
    linea_actual = 1
    posicion_actual = 0
    avanzar()
    tokens = []
    en_comentario = False

    while char_actual is not None:
        # Comentarios de una línea
        if char_actual == '/' and pos + 1 < len(texto) and texto[pos + 1] == '/':
            # Ignora todo hasta el final de la línea
            while char_actual is not None and char_actual != '\n':
                avanzar()
            avanzar()  # Avanza sobre el último '\n'
        # Comentarios de varias líneas
        elif char_actual == '/' and pos + 1 < len(texto) and texto[pos + 1] == '*':
            en_comentario = True
            avanzar()  # Avanza sobre el '*'
            avanzar()  # Avanza sobre el '/'
        elif en_comentario and char_actual == '*' and pos + 1 < len(texto) and texto[pos + 1] == '/':
            en_comentario = False
            avanzar()  # Avanza sobre el '*'
            avanzar()  # Avanza sobre el '/'
        elif not en_comentario:
            if char_actual in DELIMITADORES_UNIVERSALES:
                avanzar()
            elif char_actual.isdigit():
                tokens.append(crear_digitos())
            elif char_actual in OPERADORES_ARITMETICOS:
                tokens.append(('OP_ARITMETICO', char_actual))
                avanzar()
            elif char_actual in OPERADORES_RELACIONALES:
                # Verificamos si el próximo caracter también forma parte del operador relacional
                if pos+1 < len(texto) and char_actual + texto[pos+1] in OPERADORES_RELACIONALES:
                    tokens.append(('OP_RELACIONAL', char_actual + texto[pos+1]))
                    avanzar()
                else:
                    tokens.append(('OP_RELACIONAL', char_actual))
                avanzar()
            elif char_actual.isalpha() or char_actual == '_':
                id = ''
                while char_actual is not None and (char_actual.isalnum() or char_actual == '_'):
                    id += char_actual
                    avanzar()
                if id in RESERVADAS:
                    tokens.append(('RESERVADA', id))  # Las palabras reservadas son tokens
                elif id in OPERADORES_LOGICOS:
                    tokens.append(('OP_LOGICO', id))
                elif id in CONSTANTES_LOGICAS:
                    tokens.append(('CONST_LOGICA', id))
                else:
                    tokens.append(('VARIABLE', id))
            elif char_actual == '"':
                tokens.append(crear_cadena())
            elif char_actual in DELIMITADORES:
                tokens.append(('DELIMITADOR', char_actual))
                avanzar()
            else:
                raise SyntaxError(f"Caracter inesperado '{char_actual}' en la línea {linea_actual}, posición {posicion_actual}")
        else:
            avanzar()

    if en_comentario:
        raise SyntaxError("Comentario de múltiples líneas no cerrado.")

    return tokens

# Analisis Sintactico

# Ejecucion
def main():
    while True:
        try:
            # Lectura de la entrada
            input_text = input('icc > ')
        except EOFError:
            break
        if input_text:
            try:
                tokens = lexer(input_text)
                for token in tokens:
                    print(token)
            except SyntaxError as e:
                print(f'Error en la entrada | {str(e)}')

if __name__ == '__main__':
    main()
