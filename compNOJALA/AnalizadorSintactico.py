class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def eat(self, token_type):
        if self.pos < len(self.tokens) and self.tokens[self.pos][0] == token_type:
            self.pos += 1
        else:
            raise SyntaxError(f'Error de sintaxis: se esperaba {token_type}, pero se encontró {self.tokens[self.pos][0]}')

    def programa(self):
        while self.pos < len(self.tokens):
            self.sentencia()

    def sentencia(self):
        if self.tokens[self.pos][1] == 'constante':
            self.definicion_constante()
        # Aquí se puede agregar lógica adicional para manejar otros tipos de sentencias
        else:
            raise SyntaxError(f'Sentencia desconocida: {self.tokens[self.pos][1]}')

    def definicion_constante(self):
        self.eat('RESERVADA')  # 'constante'
        self.tipo()
        self.eat('VARIABLE')
        self.eat('DELIMITADOR')  # '='
        self.expresion()
        self.eat('DELIMITADOR')  # ';'

    def tipo(self):
        if self.tokens[self.pos][1] in ['nulo', 'entero', 'decimal', 'palabra', 'logico']:
            self.eat('RESERVADA')
        else:
            raise SyntaxError(f'Tipo desconocido: {self.tokens[self.pos][1]}')

    def expresion(self):
        # Aquí se puede agregar lógica para manejar expresiones.
        # Por ahora, simplemente reconoceremos una variable, un número entero o un número decimal como una expresión válida.
        if self.tokens[self.pos][0] == 'VARIABLE':
            self.eat('VARIABLE')
        elif self.tokens[self.pos][0] == 'ENTERO':
            self.eat('ENTERO')
        elif self.tokens[self.pos][0] == 'DECIMAL':
            self.eat('DECIMAL')
        else:
            raise SyntaxError(f'Expresión inválida: {self.tokens[self.pos][1]}')

    def sentencia(self):
        if self.tokens[self.pos][1] == 'constante':
            self.definicion_constante()
        elif self.tokens[self.pos][1] in ['nulo', 'entero', 'decimal', 'palabra', 'logico']:
            self.definicion_variable()
        elif self.tokens[self.pos][0] == 'VARIABLE' and self.tokens[self.pos + 1][1] == '=':
            self.asignacion_variable()
        elif self.tokens[self.pos][1] in ['nulo', 'entero', 'decimal', 'palabra', 'logico'] and self.tokens[self.pos + 1][0] == 'VARIABLE' and self.tokens[self.pos + 2][1] == '(':
            self.declaracion_funcion()
        elif self.tokens[self.pos][0] == 'VARIABLE' and self.tokens[self.pos + 1][1] == '(':
            self.llamada_funcion()
        # Aquí se puede agregar lógica adicional para manejar otros tipos de sentencias
        else:
            raise SyntaxError(f'Sentencia desconocida: {self.tokens[self.pos][1]}')

    def definicion_variable(self):
        self.tipo()
        self.eat('VARIABLE')
        self.eat('DELIMITADOR')  # ';'

    def asignacion_variable(self):
        self.eat('VARIABLE')
        self.eat('DELIMITADOR')  # '='
        self.expresion()
        self.eat('DELIMITADOR')  # ';'

    def declaracion_funcion(self):
        self.tipo()
        self.eat('VARIABLE')
        self.eat('DELIMITADOR')  # '('
        # Asumiendo que los parámetros son opcionales y que solo hay un parámetro
        if self.tokens[self.pos][1] in ['nulo', 'entero', 'decimal', 'palabra', 'logico']:
            self.tipo()
            self.eat('VARIABLE')
        self.eat('DELIMITADOR')  # ')'
        self.eat('DELIMITADOR')  # '{'
        # Aquí debería ir la lógica para manejar múltiples sentencias dentro de la función
        self.eat('DELIMITADOR')  # '}'

    def llamada_funcion(self):
        self.eat('VARIABLE')
        self.eat('DELIMITADOR')  # '('
        # Asumiendo que los argumentos son opcionales y que solo hay un argumento
        if self.tokens[self.pos][0] in ['VARIABLE', 'ENTERO', 'DECIMAL', 'CADENA']:
            self.expresion()
        self.eat('DELIMITADOR')  # ')'
        self.eat('DELIMITADOR')  # ';'

import AnalizadorLexico
codigo_fuente = '''
nulo miFuncion() {
    entero x;
    x = 5;
}
miFuncion();
'''
tokens = AnalizadorLexico.lexer(codigo_fuente)
tokens = list(tokens)

parser = Parser(tokens)
parser.programa()  # Si no hay errores de sintaxis, esto no debería lanzar ninguna excepción
