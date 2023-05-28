import AnalizadorLexico
#import AnalizadorSintactico

texto_input = '''
nulo miFuncion() {
    entero x;
    x = 5;
}
miFuncion();'''

tokens = AnalizadorLexico.lexer(texto_input)
print(tokens)

print('\n')





'''# Creación de tokens desde un código de entrada
codigo_fuente = 'constante entero x = 5;'
tokens = lexer(codigo_fuente)

# Uso del analizador
parser = Parser(tokens)
parser.programa()  # Si no hay errores de sintaxis, esto no debería lanzar ninguna excepción
'''
