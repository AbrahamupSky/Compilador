from lexico import Lexico
from simbolo import CONST_TOKENS

codigo = ""
with open('codigo.txt','r') as f:
  codigo = f.read()

print(codigo)

lex = Lexico(codigo)

print("\n")
while True:
  s = lex.siguiente_componente_lexico()
  if s:

    print("Lexema: {}".format(s.Lexema).ljust(60),end="")
    print("Token: {} ".format(s.Token))
  else:
    break
print("\n")
if lex.error.total > 0:
  print("Se encontraron: {} errores.".format(lex.error.total))
  for e in lex.error.errores:
    print(e)
