def programa(tokens):
    global linea_actual, posicion_actual
    linea_actual = 0
    posicion_actual = 0

    while linea_actual < len(tokens):
        sentencia(tokens)


def sentencia(tokens):
    global linea_actual, posicion_actual

    if tokens[linea_actual][posicion_actual][0] == 'RESERVADA' and tokens[linea_actual][posicion_actual][1] == 'constante':
        definicion_constante(tokens)
    elif tokens[linea_actual][posicion_actual][0] == 'RESERVADA' and tokens[linea_actual][posicion_actual][1] in ['nulo', 'entero', 'decimal', 'palabra', 'logico']:
        definicion_variable(tokens)
    elif tokens[linea_actual][posicion_actual][0] == 'VARIABLE':
        if tokens[linea_actual][posicion_actual + 1][0] == 'DELIMITADOR' and tokens[linea_actual][posicion_actual + 1][1] == '=':
            asignacion_variable(tokens)
        elif tokens[linea_actual][posicion_actual + 1][0] == 'DELIMITADOR' and tokens[linea_actual][posicion_actual + 1][1] == '(':
            llamada_funcion(tokens)
        else:
            raise SyntaxError(f"Error de sintaxis en la línea {linea_actual + 1}, posición {posicion_actual + 1}")
    elif tokens[linea_actual][posicion_actual][0] == 'RESERVADA' and tokens[linea_actual][posicion_actual][1] in ['si', 'desde', 'mientras', 'repite', 'regresa']:
        sentencia_control(tokens)
    elif tokens[linea_actual][posicion_actual][0] == 'RESERVADA' and tokens[linea_actual][posicion_actual][1] == 'imprime':
        imprimir(tokens)
    elif tokens[linea_actual][posicion_actual][0] == 'RESERVADA' and tokens[linea_actual][posicion_actual][1] == 'imprimenl':
        imprimir_nueva_linea(tokens)
    elif tokens[linea_actual][posicion_actual][0] == 'RESERVADA' and tokens[linea_actual][posicion_actual][1] == 'lee':
        leer(tokens)
    else:
        raise SyntaxError(f"Error de sintaxis en la línea {linea_actual + 1}, posición {posicion_actual + 1}")


    
def tipo(tokens):
    if tokens[linea_actual][posicion_actual][0] == 'RESERVADA' and tokens[linea_actual][posicion_actual][1] in ['nulo', 'entero', 'decimal', 'palabra', 'logico']:
        avanzar()
    else:
        raise SyntaxError(f"Error de sintaxis. Se esperaba un tipo de dato en la línea {linea_actual + 1}, posición {posicion_actual + 1}")



def definicion_constante(tokens):
    if tokens[0][0] == 'RESERVADA' and tokens[0][1] == 'constante':
        avanzar()
        tipo(tokens)
        if tokens[0][0] == 'VARIABLE':
            avanzar()
            if tokens[0][0] == 'DELIMITADOR' and tokens[0][1] == '=':
                avanzar()
                expresion(tokens)
                if tokens[0][0] == 'DELIMITADOR' and tokens[0][1] == ';':
                    avanzar()
                else:
                    raise SyntaxError(f"Error de sintaxis. Se esperaba ';' en la línea {linea_actual}, posición {posicion_actual}")
            else:
                raise SyntaxError(f"Error de sintaxis. Se esperaba '=' en la línea {linea_actual}, posición {posicion_actual}")
        else:
            raise SyntaxError(f"Error de sintaxis. Se esperaba un identificador en la línea {linea_actual}, posición {posicion_actual}")
    else:
        raise SyntaxError(f"Error de sintaxis en la línea {linea_actual}, posición {posicion_actual}")

def definicion_variable(tokens):
    tipo(tokens)
    lista_variables(tokens)
    if tokens[0][0] == 'DELIMITADOR' and tokens[0][1] == ';':
        avanzar()
    else:
        raise SyntaxError(f"Error de sintaxis. Se esperaba ';' en la línea {linea_actual}, posición {posicion_actual}")

def lista_variables(tokens):
    if tokens[0][0] == 'VARIABLE':
        avanzar()
        if tokens[0][0] == 'DELIMITADOR' and tokens[0][1] == ',':
            avanzar()
            lista_variables(tokens)
        elif tokens[0][0] == 'DELIMITADOR' and tokens[0][1] == '=':
            avanzar()
            expresion(tokens)
            if tokens[0][0] == 'DELIMITADOR' and tokens[0][1] == '[':
                avanzar()
                expresion(tokens)
                if tokens[0][0] == 'DELIMITADOR' and tokens[0][1] == ']':
                    avanzar()
                else:
                    raise SyntaxError(f"Error de sintaxis. Se esperaba ']' en la línea {linea_actual}, posición {posicion_actual}")
            elif tokens[0][0] == 'DELIMITADOR' and tokens[0][1] == '{':
                avanzar()
                lista_valores(tokens)
                if tokens[0][0] == 'DELIMITADOR' and tokens[0][1] == '}':
                    avanzar()
                else:
                    raise SyntaxError(f"Error de sintaxis. Se esperaba '}}' en la línea {linea_actual}, posición {posicion_actual}")
        elif tokens[0][0] == 'DELIMITADOR' and tokens[0][1] == '[':
            avanzar()
            expresion(tokens)
            if tokens[0][0] == 'DELIMITADOR' and tokens[0][1] == ']':
                avanzar()
            else:
                raise SyntaxError(f"Error de sintaxis. Se esperaba ']' en la línea {linea_actual}, posición {posicion_actual}")
    else:
        raise SyntaxError(f"Error de sintaxis. Se esperaba un identificador en la línea {linea_actual}, posición {posicion_actual}")

def lista_valores(tokens):
    expresion(tokens)
    if tokens[0][0] == 'DELIMITADOR' and tokens[0][1] == ',':
        avanzar()
        lista_valores(tokens)

def asignacion_variable(tokens):
    if tokens[0][0] == 'VARIABLE':
        avanzar()
        if tokens[0][0] == 'DELIMITADOR' and tokens[0][1] == '=':
            avanzar()
            expresion(tokens)
            if tokens[0][0] == 'DELIMITADOR' and tokens[0][1] == ';':
                avanzar()
            else:
                raise SyntaxError(f"Error de sintaxis. Se esperaba ';' en la línea {linea_actual}, posición {posicion_actual}")
        else:
            raise SyntaxError(f"Error de sintaxis. Se esperaba '=' en la línea {linea_actual}, posición {posicion_actual}")
    else:
        raise SyntaxError(f"Error de sintaxis. Se esperaba un identificador en la línea {linea_actual}, posición {posicion_actual}")

def llamada_funcion(tokens):
    if tokens[0][0] == 'VARIABLE':
        avanzar()
        if tokens[0][0] == 'DELIMITADOR' and tokens[0][1] == '(':
            avanzar()
            if tokens[0][0] == 'DELIMITADOR' and tokens[0][1] == ')':
                avanzar()
                if tokens[0][0] == 'DELIMITADOR' and tokens[0][1] == ';':
                    avanzar()
                else:
                    raise SyntaxError(f"Error de sintaxis. Se esperaba ';' en la línea {linea_actual}, posición {posicion_actual}")
            else:
                argumentos_funcion(tokens)
                if tokens[0][0] == 'DELIMITADOR' and tokens[0][1] == ')':
                    avanzar()
                    if tokens[0][0] == 'DELIMITADOR' and tokens[0][1] == ';':
                        avanzar()
                    else:
                        raise SyntaxError(f"Error de sintaxis. Se esperaba ';' en la línea {linea_actual}, posición {posicion_actual}")
                else:
                    raise SyntaxError(f"Error de sintaxis. Se esperaba ')' en la línea {linea_actual}, posición {posicion_actual}")
        else:
            raise SyntaxError(f"Error de sintaxis. Se esperaba '(' en la línea {linea_actual}, posición {posicion_actual}")
    else:
        raise SyntaxError(f"Error de sintaxis. Se esperaba un identificador en la línea {linea_actual}, posición {posicion_actual}")

def argumentos_funcion(tokens):
    expresion(tokens)
    if tokens[0][0] == 'DELIMITADOR' and tokens[0][1] == ',':
        avanzar()
        argumentos_funcion(tokens)

def sentencia_control(tokens):
    if tokens[0][0] == 'RESERVADA' and tokens[0][1] == 'si':
        avanzar()
        if tokens[0][0] == 'DELIMITADOR' and tokens[0][1] == '(':
            avanzar()
            expresion(tokens)
            if tokens[0][0] == 'DELIMITADOR' and tokens[0][1] == ')':
                avanzar()
                if tokens[0][0] == 'RESERVADA' and tokens[0][1] == 'hacer':
                    avanzar()
                    if tokens[0][0] == 'DELIMITADOR' and tokens[0][1] == '{':
                        avanzar()
                        while tokens[0][0] != 'DELIMITADOR' or tokens[0][1] != '}':
                            sentencia(tokens)
                        avanzar()
                        if tokens[0][0] == 'RESERVADA' and tokens[0][1] == 'sino':
                            avanzar()
                            if tokens[0][0] == 'DELIMITADOR' and tokens[0][1] == '{':
                                avanzar()
                                while tokens[0][0] != 'DELIMITADOR' or tokens[0][1] != '}':
                                    sentencia(tokens)
                                avanzar()
                        else:
                            raise SyntaxError(f"Error de sintaxis. Se esperaba 'parentesis_derecho' en la línea {linea_actual}, posición {posicion_actual}")
                    else:
                        raise SyntaxError(f"Error de sintaxis. Se esperaba 'parentesis_izquierdo' en la línea {linea_actual}, posición {posicion_actual}")
                else:
                    raise SyntaxError(f"Error de sintaxis. Se esperaba 'hacer' en la línea {linea_actual}, posición {posicion_actual}")
            else:
                raise SyntaxError(f"Error de sintaxis. Se esperaba ')' en la línea {linea_actual}, posición {posicion_actual}")
        else:
            raise SyntaxError(f"Error de sintaxis. Se esperaba '(' en la línea {linea_actual}, posición {posicion_actual}")
    elif tokens[0][0] == 'RESERVADA' and tokens[0][1] == 'desde':
        avanzar()
        if tokens[0][0] == 'VARIABLE':
            avanzar()
            if tokens[0][0] == 'DELIMITADOR' and tokens[0][1] == '=':
                avanzar()
                expresion(tokens)
                if tokens[0][0] == 'RESERVADA' and tokens[0][1] == 'hasta':
                    avanzar()
                    expresion(tokens)
                    if tokens[0][0] == 'RESERVADA' and tokens[0][1] == 'incr':
                        avanzar()
                        expresion(tokens)
                        if tokens[0][0] == 'DELIMITADOR' and tokens[0][1] == '{':
                            avanzar()
                            while tokens[0][0] != 'DELIMITADOR' or tokens[0][1] != '}':
                                sentencia(tokens)
                            avanzar()
                        else:
                            raise SyntaxError(f"Error de sintaxis. Se esperaba '{{' en la línea {linea_actual}, posición {posicion_actual}")
                    else:
                        raise SyntaxError(f"Error de sintaxis. Se esperaba 'incr' en la línea {linea_actual}, posición {posicion_actual}")
                else:
                    raise SyntaxError(f"Error de sintaxis. Se esperaba 'hasta' en la línea {linea_actual}, posición {posicion_actual}")
            else:
                raise SyntaxError(f"Error de sintaxis. Se esperaba '=' en la línea {linea_actual}, posición {posicion_actual}")
        else:
            raise SyntaxError(f"Error de sintaxis. Se esperaba un identificador en la línea {linea_actual}, posición {posicion_actual}")
    elif tokens[0][0] == 'RESERVADA' and tokens[0][1] == 'mientras':
        avanzar()
        if tokens[0][0] == 'RESERVADA' and tokens[0][1] == 'que':
            avanzar()
            if tokens[0][0] == 'DELIMITADOR' and tokens[0][1] == '{':
                avanzar()
                while tokens[0][0] != 'DELIMITADOR' or tokens[0][1] != '}':
                    sentencia(tokens)
                avanzar()
            else:
                raise SyntaxError(f"Error de sintaxis. Se esperaba '{{' en la línea {linea_actual}, posición {posicion_actual}")
        else:
            raise SyntaxError(f"Error de sintaxis. Se esperaba 'que' en la línea {linea_actual}, posición {posicion_actual}")
    elif tokens[0][0] == 'RESERVADA' and tokens[0][1] == 'repite':
        avanzar()
        if tokens[0][0] == 'DELIMITADOR' and tokens[0][1] == '{':
            avanzar()
            while tokens[0][0] != 'DELIMITADOR' or tokens[0][1] != '}':
                sentencia(tokens)
            avanzar()
            if tokens[0][0] == 'RESERVADA' and tokens[0][1] == 'hasta':
                avanzar()
                if tokens[0][0] == 'RESERVADA' and tokens[0][1] == 'que':
                    avanzar()
                    expresion(tokens)
                else:
                    raise SyntaxError(f"Error de sintaxis. Se esperaba 'que' en la línea {linea_actual}, posición {posicion_actual}")
            else:
                raise SyntaxError(f"Error de sintaxis. Se esperaba 'hasta' en la línea {linea_actual}, posición {posicion_actual}")
        else:
            raise SyntaxError(f"Error de sintaxis. Se esperaba '{{' en la línea {linea_actual}, posición {posicion_actual}")
    elif tokens[0][0] == 'RESERVADA' and tokens[0][1] == 'regresa':
        avanzar()
        expresion(tokens)
        if tokens[0][0] == 'DELIMITADOR' and tokens[0][1] == ';':
            avanzar()
        else:
            raise SyntaxError(f"Error de sintaxis. Se esperaba ';' en la línea {linea_actual}, posición {posicion_actual}")
    else:
        raise SyntaxError(f"Error de sintaxis en la línea {linea_actual}, posición {posicion_actual}")

def imprimir(tokens):
    if tokens[0][0] == 'RESERVADA' and tokens[0][1] == 'imprime':
        avanzar()
        if tokens[0][0] == 'DELIMITADOR' and tokens[0][1] == '(':
            avanzar()
            expresion(tokens)
            if tokens[0][0] == 'DELIMITADOR' and tokens[0][1] == ')':
                avanzar()
                if tokens[0][0] == 'DELIMITADOR' and tokens[0][1] == ';':
                    avanzar()
                else:
                    raise SyntaxError(f"Error de sintaxis. Se esperaba ';' en la línea {linea_actual}, posición {posicion_actual}")
            else:
                raise SyntaxError(f"Error de sintaxis. Se esperaba ')' en la línea {linea_actual}, posición {posicion_actual}")
        else:
            raise SyntaxError(f"Error de sintaxis. Se esperaba '(' en la línea {linea_actual}, posición {posicion_actual}")
    else:
        raise SyntaxError(f"Error de sintaxis en la línea {linea_actual}, posición {posicion_actual}")

def imprimir_nueva_linea(tokens):
    if tokens[0][0] == 'RESERVADA' and tokens[0][1] == 'imprimenl':
        avanzar()
        if tokens[0][0] == 'DELIMITADOR' and tokens[0][1] == '(':
            avanzar()
            expresion(tokens)
            if tokens[0][0] == 'DELIMITADOR' and tokens[0][1] == ')':
                avanzar()
                if tokens[0][0] == 'DELIMITADOR' and tokens[0][1] == ';':
                    avanzar()
                else:
                    raise SyntaxError(f"Error de sintaxis. Se esperaba ';' en la línea {linea_actual}, posición {posicion_actual}")
            else:
                raise SyntaxError(f"Error de sintaxis. Se esperaba ')' en la línea {linea_actual}, posición {posicion_actual}")
        else:
            raise SyntaxError(f"Error de sintaxis. Se esperaba '(' en la línea {linea_actual}, posición {posicion_actual}")
    else:
        raise SyntaxError(f"Error de sintaxis en la línea {linea_actual}, posición {posicion_actual}")

def leer(tokens):
    if tokens[0][0] == 'RESERVADA' and tokens[0][1] == 'lee':
        avanzar()
        if tokens[0][0] == 'DELIMITADOR' and tokens[0][1] == '(':
            avanzar()
            if tokens[0][0] == 'VARIABLE':
                avanzar()
                if tokens[0][0] == 'DELIMITADOR' and tokens[0][1] == ')':
                    avanzar()
                    if tokens[0][0] == 'DELIMITADOR' and tokens[0][1] == ';':
                        avanzar()
                    else:
                        raise SyntaxError(f"Error de sintaxis. Se esperaba ';' en la línea {linea_actual}, posición {posicion_actual}")
                else:
                    raise SyntaxError(f"Error de sintaxis. Se esperaba ')' en la línea {linea_actual}, posición {posicion_actual}")
            else:
                raise SyntaxError(f"Error de sintaxis. Se esperaba un identificador en la línea {linea_actual}, posición {posicion_actual}")
        else:
            raise SyntaxError(f"Error de sintaxis. Se esperaba '(' en la línea {linea_actual}, posición {posicion_actual}")
    else:
        raise SyntaxError(f"Error de sintaxis en la línea {linea_actual}, posición {posicion_actual}")

def expresion(tokens):
    termino(tokens)
    if tokens[0][0] == 'OPERADOR' and tokens[0][1] in ['+', '-']:
        avanzar()
        expresion(tokens)

def termino(tokens):
    factor(tokens)
    if tokens[0][0] == 'OPERADOR' and tokens[0][1] in ['*', '/']:
        avanzar()
        termino(tokens)

def factor(tokens):
    if tokens[0][0] == 'DELIMITADOR' and tokens[0][1] == '(':
        avanzar()
        expresion(tokens)
        if tokens[0][0] == 'DELIMITADOR' and tokens[0][1] == ')':
            avanzar()
        else:
            raise SyntaxError(f"Error de sintaxis. Se esperaba ')' en la línea {linea_actual}, posición {posicion_actual}")
    elif tokens[0][0] == 'ENTERO' or tokens[0][0] == 'DECIMAL' or tokens[0][0] == 'PALABRA' or tokens[0][0] == 'LOGICO':
        avanzar()
    elif tokens[0][0] == 'VARIABLE':
        avanzar()
        if tokens[0][0] == 'DELIMITADOR' and tokens[0][1] == '[':
            avanzar()
            expresion(tokens)
            if tokens[0][0] == 'DELIMITADOR' and tokens[0][1] == ']':
                avanzar()
            else:
                raise SyntaxError(f"Error de sintaxis. Se esperaba ']' en la línea {linea_actual}, posición {posicion_actual}")
        elif tokens[0][0] == 'DELIMITADOR' and tokens[0][1] == '(':
            avanzar()
            if tokens[0][0] == 'DELIMITADOR' and tokens[0][1] == ')':
                avanzar()
            else:
                argumentos_funcion(tokens)
                if tokens[0][0] == 'DELIMITADOR' and tokens[0][1] == ')':
                    avanzar()
                else:
                    raise SyntaxError(f"Error de sintaxis. Se esperaba ')' en la línea {linea_actual}, posición {posicion_actual}")
    else:
        raise SyntaxError(f"Error de sintaxis en la línea {linea_actual}, posición {posicion_actual}")

def avanzar():
    global linea_actual, posicion_actual
    posicion_actual += 1
    if posicion_actual >= len(tokens[linea_actual]):
        posicion_actual = 0
        linea_actual += 1



import AnalizadorLexico
input_programa = '''constante entero TAM=10;
entero i, j, k=10, vec[TAM]={12, -1, 0, 99, 18, 23, 55, 10, 25, 30};
palabra p="Hola";
logico band=falso;
constante decimal PI=3.141592;

nulo ordBurbuja(entero *arr, entero n) {
	entero i, j, tmp;
  desde i=0 hasta n-2 incr 1
     j=i+1;
     mientras que j<=n-1 {
        si arr[i] > arr[j] hacer {
           tmp = arr[i];
           arr[i] = arr[j];
			  arr[j] = tmp;
        }
        j = j + 1;
      }
}
nulo impVec(entero *arr, entero n) {
	entero i=0;
  imprime("vec=[");
  repite {
     imprime(arr[i], ", ");
     i =  i+ 1
  } hasta que i == n;
  imprimenl(arr[n-1], "]");
}

entero facRec(entero num) {
   si num == 0 o num == 1 hacer regresa 1;
   sino regresa num * facRec(num-1);
}

logico compara(decimal a, decimal b) {
    regresa a > b;
}

decimal areaCir(decimal radio) {
    regresa PI*radio^2;
}

palabra concatena(palabra a, palabra b) {
    regresa a + " " + b;
}

nulo principal() {
   imprime("Dame numero: ");
   lee(i);
   imprimenl("Factorial(", i, ")=", facRec(i)); 
}
'''
# Llamada al analizador sintáctico
tokens = AnalizadorLexico.lexer(input_programa)
programa(input_programa)
