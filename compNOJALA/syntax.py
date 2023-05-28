# Analisis Sintactico

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse_programa(self):
        decls = self.parse_declaraciones()
        main = self.parse_principal()
        return ('programa', decls, main)

    def parse_declaraciones(self):
        decls = []
        while self.pos < len(self.tokens):
            if self.tokens[self.pos][1] in ('constante', 'entero', 'decimal', 'logico', 'palabra'):
                decls.append(self.parse_declaracion())
                if self.tokens[self.pos][1] != ';':
                    raise SyntaxError(f"Se esperaba ';' pero se obtuvo '{self.tokens[self.pos][1]}'")
                self.pos += 1  # Avanzar después de ';'
            else:
                break
        return ('declaraciones', decls)

    def parse_declaracion(self):
        if self.tokens[self.pos][1] == 'constante':
            self.pos += 1  # Avanzar después de 'constante'
            tipo = self.parse_tipo()
            if self.tokens[self.pos][0] != 'VARIABLE':
                raise SyntaxError(f"Se esperaba un identificador pero se obtuvo '{self.tokens[self.pos][1]}'")
            id = self.tokens[self.pos][1]
            self.pos += 1  # Avanzar después del identificador
            if self.tokens[self.pos][1] != '=':
                raise SyntaxError(f"Se esperaba '=' pero se obtuvo '{self.tokens[self.pos][1]}'")
            self.pos += 1  # Avanzar después de '='
            valor = self.parse_valor()  # Implementar esta función según tu gramática
            return ('declaracion_constante', tipo, id, valor)
        else:
            tipo = self.parse_tipo()
            return ('declaracion_tipo', tipo, self.parse_lista_declaracion())  # Implementar parse_lista_declaracion

    def parse_tipo(self):
        if self.tokens[self.pos][1] in ('entero', 'decimal', 'logico', 'palabra'):
            tipo = self.tokens[self.pos][1]
            self.pos += 1  # Avanzar después del tipo
            return ('tipo', tipo)
        else:
            raise SyntaxError(f"Se esperaba un tipo pero se obtuvo '{self.tokens[self.pos][1]}'")


    def parse_lista_declaracion(self):
        if self.tokens[self.pos][1] == '[':
            return self.parse_lista_tipo()
        elif self.tokens[self.pos][0] == 'VARIABLE':
            id = self.tokens[self.pos][1]
            self.pos += 1  # Avanzar después del identificador
            if self.tokens[self.pos][1] == '=':
                self.pos += 1  # Avanzar después de '='
                lista_valores = self.parse_lista_valores()
                return ('lista_declaracion', id, lista_valores)
            else:
                return ('lista_declaracion', id)
        else:
            raise SyntaxError(f"Se esperaba '[' o un identificador pero se obtuvo '{self.tokens[self.pos][1]}'")

    def parse_lista_tipo(self):
        if self.tokens[self.pos][1] == '[':
            self.pos += 1  # Avanzar después de '['
            valor = self.parse_valor()
            if self.tokens[self.pos][1] != ']':
                raise SyntaxError(f"Se esperaba ']' pero se obtuvo '{self.tokens[self.pos][1]}'")
            self.pos += 1  # Avanzar después de ']'
            return ('lista_tipo', valor)
        else:
            raise SyntaxError(f"Se esperaba '[' pero se obtuvo '{self.tokens[self.pos][1]}'")

    def parse_lista_valores(self):
        if self.tokens[self.pos][1] == '{':
            self.pos += 1  # Avanzar después de '{'
            valores = []
            while self.tokens[self.pos][1] != '}':
                valores.append(self.parse_valor())
                if self.tokens[self.pos][1] == ',':
                    self.pos += 1  # Avanzar después de ','
                elif self.tokens[self.pos][1] != '}':
                    raise SyntaxError(f"Se esperaba ',' o 'rparen' pero se obtuvo '{self.tokens[self.pos][1]}'")
            self.pos += 1  # Avanzar después de '}'
            return ('lista_valores', valores)
        else:
            raise SyntaxError(f"Se esperaba 'lparen' pero se obtuvo '{self.tokens[self.pos][1]}'")


    def parse_valores(self):
        valores = []
        while True:
            valores.append(self.parse_valor())
            if self.tokens[self.pos][1] == ',':
                self.pos += 1  # Avanza después de ','
            else:
                break
        return ('valores', valores)

    def parse_valor(self):
        if self.tokens[self.pos][0] == 'VARIABLE':
            id = self.tokens[self.pos][1]
            self.pos += 1  # Avanza después del identificador
            if self.tokens[self.pos][1] in ['[', '.']:
                operador = self.tokens[self.pos][1]
                self.pos += 1  # Avanza después del operador
                if operador == '[':
                    expresion = self.parse_expresion()
                    if self.tokens[self.pos][1] != ']':
                        raise SyntaxError(f"Se esperaba ']' pero se obtuvo '{self.tokens[self.pos][1]}'")
                    self.pos += 1  # Avanza después de ']'
                    return ('valor_con_corchetes', id, expresion)
                else:  # operador == '.'
                    if self.tokens[self.pos][0] != 'VARIABLE':
                        raise SyntaxError(f"Se esperaba un identificador pero se obtuvo '{self.tokens[self.pos][1]}'")
                    id2 = self.tokens[self.pos][1]
                    self.pos += 1  # Avanza después del segundo identificador
                    return ('valor_con_punto', id, id2)
            else:
                return ('valor', id)
        elif self.tokens[self.pos][0] in ['ENTERO', 'DECIMAL', 'CADENA', 'CONST_LOGICA']:
            constante = self.tokens[self.pos][1]
            self.pos += 1  # Avanza después de la constante
            return ('constante', constante)
        elif self.tokens[self.pos][1] == '(':
            self.pos += 1  # Avanza después de '('
            expresion = self.parse_expresion()
            if self.tokens[self.pos][1] != ')':
                raise SyntaxError(f"Se esperaba ')' pero se obtuvo '{self.tokens[self.pos][1]}'")
            self.pos += 1  # Avanza después de ')'
            return ('expresion_en_parentesis', expresion)
        else:
            raise SyntaxError(f"Valor inválido '{self.tokens[self.pos][1]}'")

    def parse_expresion(self):
        if self.tokens[self.pos][1] == '-':
            self.pos += 1  # Avanza después de '-'
            valor = self.parse_valor()
            return ('expresion_negativa', valor)
        elif self.tokens[self.pos][1] == '(':
            self.pos += 1  # Avanza después de '('
            expresion = self.parse_expresion()
            if self.tokens[self.pos][1] != ')':
                raise SyntaxError(f"Se esperaba ')' pero se obtuvo '{self.tokens[self.pos][1]}'")
            self.pos += 1  # Avanza después de ')'
            return ('expresion_en_parentesis', expresion)
        else:
            valor1 = self.parse_valor()
            if self.tokens[self.pos][1] in ['+', '-', '*', '/', '%', '^', '>', '<', '<=', '>=', '<>', '==']:
                operador = self.tokens[self.pos][1]
                self.pos += 1  # Avanza después del operador
                valor2 = self.parse_valor()
                return ('expresion_binaria', operador, valor1, valor2)
            else:
                raise SyntaxError(f"Operador inválido '{self.tokens[self.pos][1]}'")


    def parse_operador(self):
        if self.tokens[self.pos][1] in ['+', '-', '*', '/', '%', '^', '>', '<', '<=', '>=', '<>', '==']:
            operador = self.tokens[self.pos][1]
            self.pos += 1  # Avanza después del operador
            return ('operador', operador)
        else:
            raise SyntaxError(f"Operador inválido '{self.tokens[self.pos][1]}'")

    def parse_principal(self):
        if self.tokens[self.pos][1] != 'nulo':
            raise SyntaxError(f"Se esperaba 'nulo' pero se obtuvo '{self.tokens[self.pos][1]}'")
        self.pos += 1  # Avanza después de 'nulo'
        if self.tokens[self.pos][1] != 'principal':
            raise SyntaxError(f"Se esperaba 'principal' pero se obtuvo '{self.tokens[self.pos][1]}'")
        self.pos += 1  # Avanza después de 'principal'
        if self.tokens[self.pos][1] != '(':
            raise SyntaxError(f"Se esperaba '(' pero se obtuvo '{self.tokens[self.pos][1]}'")
        self.pos += 1  # Avanza después de '('
        if self.tokens[self.pos][1] != ')':
            raise SyntaxError(f"Se esperaba ')' pero se obtuvo '{self.tokens[self.pos][1]}'")
        self.pos += 1  # Avanza después de ')'
        bloque = self.parse_bloque()
        return ('principal', bloque)

    def parse_bloque(self):
        if self.tokens[self.pos][1] != '{':
            raise SyntaxError(f"Se esperaba 'doslparen' pero se obtuvo '{self.tokens[self.pos][1]}'")
        self.pos += 1  # Avanza después de '{'
        declaraciones = []
        while self.tokens[self.pos][1] != '}':
            declaraciones.append(self.parse_declaraciones())
            if self.tokens[self.pos][1] != ';':
                raise SyntaxError(f"Se esperaba ';' pero se obtuvo '{self.tokens[self.pos][1]}'")
            self.pos += 1  # Avanza después de ';'
        if self.tokens[self.pos][1] != '}':
            raise SyntaxError(f"Se esperaba 'dosrparen' pero se obtuvo '{self.tokens[self.pos][1]}'")
        self.pos += 1  # Avanza después de '}'
        return ('bloque', declaraciones)


    def parse_sentencias(self):
        sentencias = []
        while self.pos < len(self.tokens) and self.tokens[self.pos][1] != '}':
            sentencias.append(self.parse_sentencia())
            if self.tokens[self.pos][1] != ';':
                raise SyntaxError(f"Se esperaba ';' pero se obtuvo '{self.tokens[self.pos][1]}'")
            self.pos += 1  # Avanza después de ';'
        return ('sentencias', sentencias)

    def parse_sentencia(self):
        if self.tokens[self.pos][0] == 'RESERVADA' and self.tokens[self.pos][1] in ['si', 'desde', 'repite', 'regresa', 'lee', 'imprime', 'imprimenl']:
            if self.tokens[self.pos][1] == 'si':
                return self.parse_sentencia_condicional()
            # Agregar aquí los demás casos para otras sentencias
        else:
            return self.parse_declaracion()  # Si no es una sentencia especial, es una declaración

    def parse_sentencia_condicional(self):
        self.pos += 1  # Avanza después de 'si'
        if self.tokens[self.pos][1] != '(':
            raise SyntaxError(f"Se esperaba '(' pero se obtuvo '{self.tokens[self.pos][1]}'")
        self.pos += 1  # Avanza después de '('
        expresion = self.parse_expresion()
        if self.tokens[self.pos][1] != ')':
            raise SyntaxError(f"Se esperaba ')' pero se obtuvo '{self.tokens[self.pos][1]}'")
        self.pos += 1  # Avanza después de ')'
        bloque = self.parse_bloque()
        if self.pos < len(self.tokens) and self.tokens[self.pos][1] == 'sino':
            self.pos += 1  # Avanza después de 'sino'
            bloque_sino = self.parse_bloque()
            return ('sentencia_condicional', expresion, bloque, bloque_sino)
        return ('sentencia_condicional', expresion, bloque)


    def parse_sentencia_bucle(self):
        if self.tokens[self.pos][1] == 'desde':
            self.pos += 1  # Avanza después de 'desde'
            inicio = self.parse_expresion()
            if self.tokens[self.pos][1] != 'hasta':
                raise SyntaxError(f"Se esperaba 'hasta' pero se obtuvo '{self.tokens[self.pos][1]}'")
            self.pos += 1  # Avanza después de 'hasta'
            fin = self.parse_expresion()
            if self.tokens[self.pos][1] != 'incr':
                raise SyntaxError(f"Se esperaba 'incr' pero se obtuvo '{self.tokens[self.pos][1]}'")
            self.pos += 1  # Avanza después de 'incr'
            incremento = self.parse_expresion()
            bloque = self.parse_bloque()
            return ('sentencia_bucle_desde', inicio, fin, incremento, bloque)
        elif self.tokens[self.pos][1] == 'repite':
            self.pos += 1  # Avanza después de 'repite'
            bloque = self.parse_bloque()
            if self.tokens[self.pos][1] != 'hasta':
                raise SyntaxError(f"Se esperaba 'hasta' pero se obtuvo '{self.tokens[self.pos][1]}'")
            self.pos += 1  # Avanza después de 'hasta'
            condicion = self.parse_expresion()
            return ('sentencia_bucle_repite', bloque, condicion)

    def parse_llamada_funcion(self):
        nombre_funcion = self.tokens[self.pos][1]
        self.pos += 1  # Avanza después de nombre de función
        if self.tokens[self.pos][1] != '(':
            raise SyntaxError(f"Se esperaba '(' pero se obtuvo '{self.tokens[self.pos][1]}'")
        self.pos += 1  # Avanza después de '('
        parametros = self.parse_parametros()
        if self.tokens[self.pos][1] != ')':
            raise SyntaxError(f"Se esperaba ')' pero se obtuvo '{self.tokens[self.pos][1]}'")
        self.pos += 1  # Avanza después de ')'
        return ('llamada_funcion', nombre_funcion, parametros)

    def parse_parametros(self):
        parametros = []
        while self.pos < len(self.tokens) and self.tokens[self.pos][1] != ')':
            parametros.append(self.parse_expresion())
            if self.pos < len(self.tokens) and self.tokens[self.pos][1] == ',':
                self.pos += 1  # Avanza después de ','
        return ('parametros', parametros)


    def parse_retorno(self):
        self.pos += 1  # Avanza después de 'regresa'
        valor = self.parse_valor()
        return ('retorno', valor)

    def parse_lectura(self):
        self.pos += 1  # Avanza después de 'lee'
        if self.tokens[self.pos][1] != '(':
            raise SyntaxError(f"Se esperaba '(' pero se obtuvo '{self.tokens[self.pos][1]}'")
        self.pos += 1  # Avanza después de '('
        id = self.tokens[self.pos][1]
        if self.tokens[self.pos][0] != 'VARIABLE':
            raise SyntaxError(f"Se esperaba una VARIABLE pero se obtuvo '{self.tokens[self.pos][1]}'")
        self.pos += 1  # Avanza después de VARIABLE
        if self.tokens[self.pos][1] != ')':
            raise SyntaxError(f"Se esperaba ')' pero se obtuvo '{self.tokens[self.pos][1]}'")
        self.pos += 1  # Avanza después de ')'
        return ('lectura', id)

    def parse_escritura(self):
        if self.tokens[self.pos][1] in ['imprime', 'imprimenl']:
            tipo = self.tokens[self.pos][1]
            self.pos += 1  # Avanza después de 'imprime' o 'imprimenl'
            if self.tokens[self.pos][1] != '(':
                raise SyntaxError(f"Se esperaba '(' pero se obtuvo '{self.tokens[self.pos][1]}'")
            self.pos += 1  # Avanza después de '('
            valores = self.parse_valores()
            if self.tokens[self.pos][1] != ')':
                raise SyntaxError(f"Se esperaba ')' pero se obtuvo '{self.tokens[self.pos][1]}'")
            self.pos += 1  # Avanza después de ')'
            return ('escritura', tipo, valores)

    def parse_constante(self):
        self.pos += 1  # Avanza después de 'constante'
        tipo = self.parse_tipo()
        id = self.tokens[self.pos][1]
        if self.tokens[self.pos][0] != 'VARIABLE':
            raise SyntaxError(f"Se esperaba una VARIABLE pero se obtuvo '{self.tokens[self.pos][1]}'")
        self.pos += 1  # Avanza después de VARIABLE
        if self.tokens[self.pos][1] != '=':
            raise SyntaxError(f"Se esperaba '=' pero se obtuvo '{self.tokens[self.pos][1]}'")
        self.pos += 1  # Avanza después de '='
        valor = self.parse_valor()
        return ('constante', tipo, id, valor)


    def parse(self):
        result = self.parse_programa()
        if result is not None and self.pos == len(self.tokens):
            return result
        else:
            raise SyntaxError('Error de sintaxis')