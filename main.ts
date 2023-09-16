import { isBoolean } from 'util'

let entrance: string = ''
const ERR: number = -1
const ACP: number = 99
let idx: number = 0
let ERRA: boolean = false
let NOPRINC: boolean = true
let rowg: number = 1
let colm: number = 1
const OPAS: string[] = ['+', '-', '*', '%', '^']
const delu: string[] = ['\n', '\t', ' ', String.fromCharCode(32)]
const keywords: string[] = ['constante', 'entero', 'decimal', 'logico', 'palabra', 'sintipo',
                            'inicio', 'fin', 'si', 'sino', 'hacer', 'desde', 'hasta', 'incr',
                            'decr', 'regresa', 'imprime', 'imprimenl', 'lee', 'interrumpe', 'continua']

const OPL: string[] = ['no', 'y', 'o']
const CTL: string[] = ['verdadero', 'falso']
const delim: string[] = ['.', ',', ';', '(', ')', '[', ']']
const special: string[] = ['!', '$', '@', '#', '?']

const matrans: number[][] = [
  // *col 0 = 'letra'
  // *col 1 = '_'
  // *col 2 = 'Digito'
  // *col 3 = 'OPAS'
  // *col 4 = '/'
  // *col 5 = '.'
  // *col 6 = '*'
  // *col 7 = 'Del'
  // *col 8 = ':'
  // *col 9 = '='
  // *col 10 = '<'
  // *col 11 = "
  // *col 12 = special

  [ 1 ,  1 ,  2 ,  5 ,  6 ,  11,  10,  11,  12,  14,  15,  18, ERR ], //0
  [ 1 ,  1 ,  1 , ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP ], //1
  [ACP, ACP,  2 , ACP, ACP,  3,  ACP, ACP, ACP, ACP, ACP, ACP, ACP ], //2
  [ERR, ERR,  4 , ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR ], //3
  [ACP, ACP,  4 , ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP ], //4
  [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP ], //5
  [ACP, ACP, ACP, ACP,  7 , ACP,  8 , ACP, ACP, ACP, ACP, ACP, ACP ], //6
  [ 7 ,  7 ,  7 ,  7 ,  7 ,  7 ,  7 ,  7,   7 ,  7 ,  7 ,  7 ,  7  ], //7
  [ 8 ,  8 ,  8 ,  8 ,  8 ,  8 ,  9 ,  8 ,  8 ,  8 ,  8 ,  8 ,  8  ], //8
  [ 8 ,  8 ,  8 ,  9 ,  0 ,  8 ,  9 ,  8 ,  8 ,  8 ,  8 ,  8 ,  8  ], //9
  [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP ], //10
  [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP ], //11
  [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP,  13, ACP, ACP, ACP ], //12
  [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP ], //13
  [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP ], //14
  [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP,  16, ACP, ACP, ACP ], //15
  [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP ], //16
  [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP ], //17
  [ 18,  18,  18,  18,  18,  18,  18,  18,  18,  18,  18,  19,  18 ], //18
  [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP ], //19
]

function colCar(x: string): number | undefined {
  if (x.match(/[a-zA-Z]/) || delu.includes(x))
    return 0;
  if (x === '_')
    return 1;
  if (x.match(/\d/))
    return 2;
  if (OPAS.includes(x))
    return 3;
  if (x === '/')
    return 4;
  if (x === '.')
    return 5;
  if (x === '*')
    return 6;
  if (delim.includes(x))
    return 7;
  if (x === ':')
    return 8;
  if (x === '=')
    return 9;
  if (['<'].includes(x))
    return 10;
  if (['"'].includes(x))
    return 11;
  if (special.includes(x))
    return 12;

  if (!delu.includes(x)) {
    console.log(x, 'is not a char or illegal symbol')
    return ERR
  }
}

function scanner() {
  let entrance
  let matrans
  let ERR
  let ACP
  let idx
  let colm
  let rowg

  let lexema
  let token
  let status
  let statusA
  let col

  while (idx < entrance.length && status !== ERR && status !== ACP) {
    let c = entrance[idx]

    while (status === 7 && entrance[idx] !== '\n') {
        idx++;
        colm++;
    }
    if (status !== 0 && (delu.includes(entrance[idx]) || entrance.charCodeAt(idx) === 32)) {
        statusA = status;
        status = 0;
    } else {
        while (idx < entrance.length && status === 0 && (delu.includes(entrance[idx]) || entrance.charCodeAt(idx) === 32)) {
            if (entrance[idx] === '\n') {
                idx++;
                rowg++;
                colm = 1;
            } else {
                idx++;
                colm++;
            }
        }
    }

    if (idx >= entrance.length) {
      break
    }

    if (status != ACP) {
      if (c === '\n') {
        idx++;
        rowg++;
        colm = 1;
      } else {
        idx++;
        colm++;
      }

      let col = colCar(c)

      if (c in delu && status != 18) {
        statusA = status
        status = ACP
      }
    }

    if (col >= 0 && col <= 12 && status != ACP && status != ERR) {
      statusA = status

      if (c in delu && status != 18) {
        status = ACP
      }
      status = matrans[col][status]

      if (status === ACP) {
        break
      } else if (status != ERR) {
        lexema =+ c
      } else {
        status = ERR
      }
    }

    if (status === ERR || status === ACP) {
      idx--
    } else {
      statusA = status
    }

    if (statusA === 1) {
      let token = 'Ide'

      if (lexema in keywords) {
        token = 'Res'
      } else if (lexema in OPL) {
        token = 'OpL'
      } else if (lexema in CTL) {
        token = 'CtL'
      }

    } else if (statusA === 2) {
      token = 'Ent'
    } else if (statusA === 4) {
      token = 'Dec'
    } else if (statusA in [5, 6, 10]) {
      token = 'OpA'
    } else if (statusA === 11 || statusA === 12) {
      token = 'Del'
    } else if (statusA === 13) {
      token = 'Ops'
    } else if (statusA === 19) {
      token = 'CtA'
    }

    return [token, lexema]
  }

  //! Error Zone
  function error(tipe, desc, obj) {
    let rowg
    let colm
    let ERRA

    ERRA = true;
    console.log("Linea:[".concat(rowg, "] Columna:[").concat(colm, "] Error de ").concat(tipe), desc, obj);
  }

  function params() {
    
  }

  function funcParcial() {

  }

  function constvars() {
    
  }

}