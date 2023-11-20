import AnalizadorLexico
import AnalizadorSintactico
#import AnalizadorSemantico
import os

# Nombre del archivo que quieres leer
nombre_archivo = input("Ingrese archivo '.icc' | Ingrese '.' = salir: ")
if nombre_archivo == '.':
    exit()

# Verificar si el archivo existe
if not os.path.exists(nombre_archivo):
    print(f"Error: El archivo {nombre_archivo} no existe.")
else:
    # Verificar la extensión del archivo
    if not nombre_archivo.endswith(".icc"):
        print(f"Error: El archivo {nombre_archivo} no tiene la extensión correcta. Debe ser '.icc'.")
    else:
        # Abrir el archivo y leer su contenido
        with open(nombre_archivo, 'r') as file:
            texto_input = file.read()

        tokens = AnalizadorLexico.lexer(texto_input)
        print('\n')
        print('\n')
        print(texto_input)
        print('\n')
        print('\n')
        try:
           sintactico = AnalizadorSintactico.SyntacticAnalyzer(tokens)
           sintactico.programa()
        except StopIteration:
           pass

        #semantico = AnalizadorSemantico.SemanticAnalyzer(tokens)
        #semantico.programa()
