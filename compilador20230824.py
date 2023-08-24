entrance = ''
ERR = -1
ACP = 99
OPAS = ['+', '-', '*', '%' , '^']
delu = ['\n', '\t', ' ']
keywords = ['si', 'sino', 'mientras', 'repite', 'hasta', 'que', 'entero',
            'decimal', 'palabra', 'logico']
OPL = ['no', 'y', 'o']
CTL = ['verdadero', 'falso']
idx = 0

matrans = [
  # col 0 = 'letra'
  # col 1 = '_'
  # col 2 = 'Digito'
  # col 3 = 'OPAS'
  # col 4 = '/'
  # col 5 = '.'
  # col 6 = '*'

  [  1,   1,   2,   5,   6,  ERR,  10 ], #0
  [  1,   1,   1,  ACP, ACP, ACP, ACP ], #1
  [ ACP, ACP,  2,  ACP, ACP,  3,  ACP ], #2
  [ ERR, ERR,  4,  ERR, ERR, ERR, ERR ], #3
  [ ACP, ACP,  4,  ACP, ACP, ACP, ACP ], #4
  [ ACP, ACP, ACP, ACP, ACP, ACP, ACP ], #5
  [ ACP, ACP, ACP, ACP,  7,  ACP,   8 ], #6
  [  7,   7,   7,   7,   7,   7,    7 ], #7
  [  8,   8,   8,   8,   8,   8,    9 ], #8
  [  8,   8,   8,   9,   0,   8,    9 ], #9
  [ ACP, ACP, ACP, ACP, ACP, ACP, ACP ], #10
]

def colChar(x):
  if x.isalpha(): return 0
  if x == '_': return 1
  if x.isdigit(): return 2
  if x in OPAS: return 3
  if x == '/': return 4
  if x == '.': return 5
  if x == '*': return 6
  print(x, 'is not a char or illegal symbol')


def scanner():
  global entrance, matrans, ERR, ACP
  lexema = ''
  token = ''
  status = 0

  while idx < len(entrance) and status != ERR and status != ACP:
    while status == 0 and entrance[idx] in delu: idx += 1

    c = entrance[idx]
    idx += 1
    col = colChar(c)

    if col >= 0 and col <= 6:
      status = matrans[status][col]
      lexema += c

    if status == 7 or status == 8 or status == 9: lexema = '' #Estos estados no guardan nada, es un comentario

  if status == ERR or status == ACP: idx -= 1

  if status == 1:
    token = 'Ide'

    if lexema in keywords: token = 'Res'
    elif lexema in OPL: token = 'OpL'
    elif lexema in CTL: token = 'CtL'

  elif status == 2: token = 'Ent'
  elif status == 4: token = 'Dec'
  elif status in [5, 6, 10]: token = 'OpA'

  return token, lexema

if __name__ == '__main__':
  entrance = input('Entrada: ')

  while idx < len(entrance):
    tok, lex = scanner() 
    print(tok, '\t\t\t', lex,)