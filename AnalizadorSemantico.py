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

# PRUEBaS
tokens = [
    ('RESERVADA', 'constante', 4),
    ('RESERVADA', 'entero', 4),
    ('IDENTIFICADOR', 'TAM', 4),
    ('DELIMITADOR', '=', 4),
    ('ENTERO', '10', 4),
    ('DELIMITADOR', ';', 4),
    ('RESERVADA', 'palabra', 5),
    ('IDENTIFICADOR', 'p', 5),
    ('DELIMITADOR', '=', 5),
    ('CADENA', 'Hola', 5),
    ('DELIMITADOR', ';', 5),
    ('RESERVADA', 'logico', 6),
    ('IDENTIFICADOR', 'band', 6),
    ('DELIMITADOR', '=', 6),
    ('CONST_LOGICA', 'falso', 6),
    ('DELIMITADOR', ';', 6),
    ('RESERVADA', 'constante', 7),
    ('RESERVADA', 'decimal', 7),
    ('IDENTIFICADOR', 'PI', 7),
    ('DELIMITADOR', '=', 7),
    ('DECIMAL', '3.141592', 7),
    ('DELIMITADOR', ';', 7),
    ('RESERVADA', 'nulo', 9),
    ('IDENTIFICADOR', 'ordBurbuja', 9),
    ('DELIMITADOR', '(', 9),
    ('RESERVADA', 'entero', 9),
    ('DELIMITADOR', '*', 9),
    ('IDENTIFICADOR', 'arr', 9),
    ('DELIMITADOR', ',', 9),
    ('RESERVADA', 'entero', 9),
    ('IDENTIFICADOR', 'n', 9),
    ('DELIMITADOR', ')', 9),
    ('DELIMITADOR', '{', 9),
    ('RESERVADA', 'entero', 10),
    ('IDENTIFICADOR', 'i', 10),
    ('DELIMITADOR', ',', 10),
    ('IDENTIFICADOR', 'j', 10),
    ('DELIMITADOR', ',', 10),
    ('IDENTIFICADOR', 'tmp', 10),
    ('DELIMITADOR', ';', 10),
    ('RESERVADA', 'desde', 11),
    ('IDENTIFICADOR', 'i', 11),
    ('DELIMITADOR', '=', 11),
    ('ENTERO', '0', 11),
    ('RESERVADA', 'hasta', 11),
    ('IDENTIFICADOR', 'n', 11),
    ('DELIMITADOR', '-', 11),
    ('ENTERO', '2', 11),
    ('RESERVADA', 'incr', 11),
    ('ENTERO', '1', 11),
    ('IDENTIFICADOR', 'j', 12),
    ('DELIMITADOR', '=', 12),
    ('IDENTIFICADOR', 'i', 12),
    ('DELIMITADOR', '+', 12),
    ('ENTERO', '1', 12),
    ('DELIMITADOR', ';', 12),
    ('RESERVADA', 'mientras', 13),
    ('RESERVADA', 'que', 13),
    ('IDENTIFICADOR', 'j', 13),
    ('DELIMITADOR', '<=', 13),
    ('IDENTIFICADOR', 'n', 13),
    ('DELIMITADOR', '{', 13),
    ('RESERVADA', 'si', 14),
    ('DELIMITADOR', '(', 14),
    ('IDENTIFICADOR', 'arr', 14),
    ('DELIMITADOR', '[', 14),
    ('IDENTIFICADOR', 'i', 14),
    ('DELIMITADOR', ']', 14),
    ('DELIMITADOR', '>', 14),
    ('IDENTIFICADOR', 'arr', 14),
    ('DELIMITADOR', '[', 14),
    ('IDENTIFICADOR', 'j', 14),
    ('DELIMITADOR', ']', 14),
    ('RESERVADA', 'hacer', 14),
    ('IDENTIFICADOR', 'tmp', 15),
    ('DELIMITADOR', '=', 15),
    ('IDENTIFICADOR', 'arr', 15),
    ('DELIMITADOR', '[', 15),
    ('IDENTIFICADOR', 'i', 15),
    ('DELIMITADOR', ']', 15),
    ('IDENTIFICADOR', 'arr', 16),
    ('DELIMITADOR', '[', 16),
    ('IDENTIFICADOR', 'j', 16),
    ('DELIMITADOR', ']', 16),
    ('IDENTIFICADOR', 'tmp', 16),
    ('DELIMITADOR', ';', 16),
    ('IDENTIFICADOR', 'j', 17),
    ('DELIMITADOR', '=', 17),
    ('IDENTIFICADOR', 'j', 17),
    ('DELIMITADOR', '+', 17),
    ('ENTERO', '1', 17),
    ('DELIMITADOR', ';', 17),
    ('DELIMITADOR', '}', 18),
    ('RESERVADA', 'nulo', 20),
    ('IDENTIFICADOR', 'impVec', 20),
    ('DELIMITADOR', '(', 20),
    ('RESERVADA', 'entero', 20),
    ('DELIMITADOR', '*', 20),
    ('IDENTIFICADOR', 'arr', 20),
    ('DELIMITADOR', ',', 20),
    ('RESERVADA', 'entero', 20),
    ('IDENTIFICADOR', 'n', 20),
    ('DELIMITADOR', ')', 20),
    ('DELIMITADOR', '{', 20),
    ('RESERVADA', 'entero', 21),
    ('IDENTIFICADOR', 'i', 21),
    ('DELIMITADOR', '=', 21),
    ('ENTERO', '0', 21),
    ('DELIMITADOR', ';', 21),
    ('RESERVADA', 'imprime', 22),
    ('CADENA', 'vec=[', 22),
    ('RESERVADA', 'repite', 23),
    ('DELIMITADOR', '{', 23),
    ('RESERVADA', 'imprime', 24),
    ('IDENTIFICADOR', 'arr', 24),
    ('DELIMITADOR', '[', 24),
    ('IDENTIFICADOR', 'i', 24),
    ('DELIMITADOR', ']', 24),
    ('DELIMITADOR', ',', 24),
    ('CADENA', "', '", 24),
    ('IDENTIFICADOR', 'i', 24),
    ('DELIMITADOR', '=', 24),
    ('IDENTIFICADOR', 'i', 24),
    ('DELIMITADOR', '+', 24),
    ('ENTERO', '1', 24),
    ('DELIMITADOR', ';', 24),
    ('RESERVADA', 'hasta', 23),
    ('IDENTIFICADOR', 'i', 23),
    ('DELIMITADOR', '==', 23),
    ('IDENTIFICADOR', 'n', 23),
    ('DELIMITADOR', '}', 23),
    ('RESERVADA', 'imprimenl', 25),
    ('IDENTIFICADOR', 'arr', 25),
    ('DELIMITADOR', '[', 25),
    ('IDENTIFICADOR', 'n', 25),
    ('DELIMITADOR', '-', 25),
    ('ENTERO', '1', 25),
    ('DELIMITADOR', ']', 25),
    ('CADENA', ']', 25),
    ('DELIMITADOR', ')', 25),
    ('DELIMITADOR', ';', 25),
    ('RESERVADA', 'entero', 27),
    ('IDENTIFICADOR', 'facRec', 27),
    ('DELIMITADOR', '(', 27),
    ('RESERVADA', 'entero', 27),
    ('IDENTIFICADOR', 'num', 27),
    ('DELIMITADOR', ')', 27),
    ('DELIMITADOR', '{', 27),
    ('RESERVADA', 'si', 28),
    ('IDENTIFICADOR', 'num', 28),
    ('DELIMITADOR', '==', 28),
    ('ENTERO', '0', 28),
    ('RESERVADA', 'o', 28),
    ('IDENTIFICADOR', 'num', 28),
    ('DELIMITADOR', '==', 28),
    ('ENTERO', '1', 28),
    ('RESERVADA', 'hacer', 28),
    ('RESERVADA', 'regresa', 29),
    ('ENTERO', '1', 29),
    ('DELIMITADOR', ';', 29),
    ('RESERVADA', 'sino', 30),
    ('RESERVADA', 'regresa', 31),
    ('IDENTIFICADOR', 'num', 31),
    ('DELIMITADOR', '*', 31),
    ('IDENTIFICADOR', 'facRec', 31),
    ('DELIMITADOR', '(', 31),
    ('IDENTIFICADOR', 'num', 31),
    ('DELIMITADOR', '-', 31),
    ('ENTERO', '1', 31),
    ('DELIMITADOR', ')', 31),
    ('DELIMITADOR', ';', 31),
    ('RESERVADA', '}', 32),
    ('RESERVADA', 'logico', 34),
    ('IDENTIFICADOR', 'compara', 34),
    ('DELIMITADOR', '(', 34),
    ('RESERVADA', 'decimal', 34),
    ('IDENTIFICADOR', 'a', 34),
    ('DELIMITADOR', ',', 34),
    ('RESERVADA', 'decimal', 34),
    ('IDENTIFICADOR', 'b', 34),
    ('DELIMITADOR', ')', 34),
    ('DELIMITADOR', '{', 34),
    ('RESERVADA', 'regresa', 35),
    ('IDENTIFICADOR', 'a', 35),
    ('DELIMITADOR', '>', 35),
    ('IDENTIFICADOR', 'b', 35),
    ('DELIMITADOR', ';', 35),
    ('RESERVADA', '}', 36),
    ('RESERVADA', 'decimal', 38),
    ('IDENTIFICADOR', 'areaCir', 38),
    ('DELIMITADOR', '(', 38),
    ('RESERVADA', 'decimal', 38),
    ('IDENTIFICADOR', 'radio', 38),
    ('DELIMITADOR', ')', 38),
    ('DELIMITADOR', '{', 38),
    ('RESERVADA', 'regresa', 39),
    ('IDENTIFICADOR', 'PI', 39),
    ('DELIMITADOR', '*', 39),
    ('IDENTIFICADOR', 'radio', 39),
    ('DELIMITADOR', '^', 39),
    ('ENTERO', '2', 39),
    ('DELIMITADOR', ';', 39),
    ('RESERVADA', '}', 40),
    ('RESERVADA', 'palabra', 42),
    ('IDENTIFICADOR', 'concatena', 42),
    ('DELIMITADOR', '(', 42),
    ('RESERVADA', 'palabra', 42),
    ('IDENTIFICADOR', 'a', 42),
    ('DELIMITADOR', ',', 42),
    ('RESERVADA', 'palabra', 42),
    ('IDENTIFICADOR', 'b', 42),
    ('DELIMITADOR', ')', 42),
    ('DELIMITADOR', '{', 42),
    ('RESERVADA', 'regresa', 43),
    ('IDENTIFICADOR', 'a', 43),
    ('DELIMITADOR', '+', 43),
    ('CADENA', "' '", 43),
    ('DELIMITADOR', '+', 43),
    ('IDENTIFICADOR', 'b', 43),
    ('DELIMITADOR', ';', 43),
    ('RESERVADA', '}', 44),
    ('RESERVADA', 'nulo', 46),
    ('IDENTIFICADOR', 'principal', 46),
    ('DELIMITADOR', '(', 46),
    ('DELIMITADOR', ')', 46),
    ('DELIMITADOR', '{', 46),
    ('RESERVADA', 'imprime', 47),
    ('CADENA', "'Dame numero: '", 47),
    ('DELIMITADOR', ';', 47),
    ('RESERVADA', 'lee', 48),
    ('DELIMITADOR', '(', 48),
    ('IDENTIFICADOR', 'i', 48),
    ('DELIMITADOR', ')', 48),
    ('DELIMITADOR', ';', 48),
    ('RESERVADA', 'imprimenl', 49),
    ('CADENA', "'Factorial('", 49),
    ('DELIMITADOR', ',', 49),
    ('IDENTIFICADOR', 'i', 49),
    ('DELIMITADOR', ',', 49),
    ('CADENA', "')='", 49),
    ('DELIMITADOR', ',', 49),
    ('IDENTIFICADOR', 'facRec', 49),
    ('DELIMITADOR', '(', 49),
    ('IDENTIFICADOR', 'i', 49),
    ('DELIMITADOR', ')', 49),
    ('DELIMITADOR', ')', 49),
    ('DELIMITADOR', ';', 49),
    ('RESERVADA', '}', 50),
    ('DELIMITADOR', '}', 51)
]

analizador_semantico(tokens)
