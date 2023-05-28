import lex
import syntax

texto_input = '''constante entero a = 5;
entero b = 10;
decimal c = 3.14;

nulo principal() {
  si (a > b) hacer {
    imprime("a es mayor que b");
  } sino {
    imprime("a es menor o igual que b");
  }
}'''

tokens = lex.lexer(texto_input)

for tok in tokens:
    print(tok)