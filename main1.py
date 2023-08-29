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
  [ ACP, ACP, ACP, ACP,  7,  ACP,  8  ], #6
  [  7,   7,   7,   7,   7,   7,   7  ], #7
  [  8,   8,   8,   8,   8,   8,   9  ], #8
  [  8,   8,   8,   9,   0,   8,   9  ], #9
  [ ACP, ACP, ACP, ACP, ACP, ACP, ACP ], #10
]

def colCar(x):
  if x.isalpha() or x in delu: return 0
  if x == '_'   : return 1
  if x.isdigit(): return 2
  if x in OPAS  : return 3
  if x == '/'   : return 4
  if x == '.'   : return 5
  if x == '*'   : return 6
  if not(x in delu):
    print(x, 'is not a char or illegal symbol')
    return ERR


def scanner():
  global entrance, matrans, ERR, ACP, idx
  lexema = ''
  token = ''
  status = 0
  stateA = 0
  col = -1

  while idx < len(entrance) and status != ERR and status != ACP:
    if status == 7 and entrance[idx] != '\n':
      idx += 1
      continue

    if status != 0 and (entrance[idx] in delu or ord(entrance[idx]) == 32):
      statusA = status
      status == ACP
    else:
      while idx < len(entrance) and status == 0 \
        and (entrance[idx] in delu or ord(entrance[idx]) == 32): 
        idx += 1

    if idx >= len(entrance): break

    if status != ACP:
      c = entrance[idx]
      idx += 1
      col = colCar( c )

    if c in delu:
      statusA = status
      status = ACP

    if col >= 0 and col <= 6 and status != ACP and status != ERR:
      statusA = status

      if c in delu: status = ACP
      status = matrans[status][col]

      if status == ACP: break
      if status != ERR:
        lexema += c

    if status == 7 or status == 8 or status == 9: lexema = ''

  if status == ERR or status == ACP: idx -= 1
  else: statusA = status

  if statusA == 1: 
    token = 'Ide'

    if lexema in keywords: token = 'Res'
    elif lexema in OPL: token = 'OpL'
    elif lexema in CTL: token = 'CtL'

  elif statusA == 2: token = 'Ent'
  elif statusA == 4: token = 'Dec'
  elif statusA in [5, 6, 10]: token = 'OpA'

  return token, lexema

if __name__ == '__main__':
  archE = ''

  while (archE[len(archE)-3:] != '.icc'):
    archE = input('File to compile (*.icc) [. = Exit]: ') # icc = Ingeniero en Ciencias Computacionales

    if archE == '.':
      exit(0)

    try:
      inputF = open(archE, 'r+')
      break

    except FileNotFoundError:
      print('No existe el archivo: ', archE)

  if inputF != None:
    while line := inputF.readline():
      entrance += line

  else:
    print('No existe el archivo: ', archE)
    exit(1)

  print('\n\n' + entrance, '\n\n')
    # inputF.close()

  while idx < len(entrance):
    tok, lex = scanner()
    print(tok, '\t\t\t', lex)
