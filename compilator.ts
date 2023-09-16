import * as fs from "fs"
import * as readline from 'readline'

//! Global variables
let entrance: string = ''
let ERR: number = -1
let ACP: number = 99
let idx: number = 0
let ERRA: boolean = false
let NOPRINC: boolean = true
let rowg: number = 1
let colm: number = 1
let OPAS: string[] = ['+', '-', '*', '%', '^']
let delu: string[] = ['\n', '\t', ' ', String.fromCharCode(32)]
let keywords: string[] = [
  "constante",
  "entero",
  "decimal",
  "logico",
  "palabra",
  "sintipo",
  "inicio",
  "fin",
  "si",
  "sino",
  "hacer",
  "desde",
  "hasta",
  "incr",
  "decr",
  "regresa",
  "imprime",
  "imprimenl",
  "lee",
  "interrumpe",
  "continua"
]
let OPL: string[] = ["no", "y", "o"]
let CTL: string[] = ["verdadero", "falso"]
let delim: string[] = [".", ",", ";", "(", ")", "[", "]", ""]
let special: string[] = ["!", "$", "@", "#", "?"]

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

//? Column Caracter

function colCar(x: string): number {
  if (x.match(/[a-zA-Z]/) || delu.includes(x)) return 0
  if (x === '_')            return 1
  if (x.match(/\d/))        return 2
  if (OPAS.includes(x))     return 3
  if (x === '/')            return 4
  if (x === '.')            return 5
  if (x === '*')            return 6
  if (delim.includes(x))    return 7
  if (x === ':')            return 8
  if (x === '=')            return 9
  if (['<'].includes(x))    return 10
  if (['"'].includes(x))    return 11
  if (special.includes(x))  return 12

  if (!delu.includes(x)) {
    console.log(x, 'is not a char or illegal symbol')
    return ERR
  }
  
  return ERR
}

//? -------------- Scanner --------------

function scanner(): [string, string] {
  let lexema: string = ''
  let token: string = ''
  let status: number = 0
  let statusA: number = 0
  let col: number = -1

  while (idx < entrance.length && status !== ERR && status !== ACP) {
    while (status === 7 && entrance[idx] !== '\n') {
      idx++
      colm++
    }

    if (status !== 0 && (delu.includes(entrance[idx]) || entrance.charCodeAt(idx) === 32)) {
      statusA = status
      status = 0
    } else {
      while (idx < entrance.length && status === 0 && (delu.includes(entrance[idx]) || entrance.charCodeAt(idx) === 32)) {
        if (entrance[idx] === '\n') {
          idx++
          rowg++
          colm = 1
        } else {
          idx++
          colm++
        }
      }
    }

    if (idx >= entrance.length) break

    if (status !== ACP) {
      const c: string = entrance[idx]

      if (c === '\n') {
        rowg++
        idx++
        colm = 1
      } else {
        idx++
        colm++
      }

      col = colCar(c)
    }

    if (delu.includes(entrance[idx]) && status !== 18) {
      statusA = status
      status = ACP
    }

    if (col >= 0 && col <= 12 && status !== ACP && status !== ERR) {
      statusA = status

      if (delu.includes(entrance[idx]) && status !== 18) status = ACP
      status = matrans[status][col]

      if (status === ACP) break
      if (status !== ERR) lexema += entrance[idx]
    } else status = ERR

    if (status === 7 || status === 8 || status === 9) {
      token = lexema = ''
    }
  }

  if (status === ERR || status === ACP) idx--
  else statusA = status

  if (statusA === 1) {
    token = 'Ide'

    if (keywords.includes(lexema)) token = 'Res'
    else if (OPL.includes(lexema)) token = 'OpL'
    else if (CTL.includes(lexema)) token = 'Ctl'
  } else if (statusA === 2) token = 'Ent'
  else if (statusA === 4) token = 'Dec'
  else if ([5, 6, 10].includes(statusA)) token = 'OpA'
  else if (statusA === 11 || statusA === 12) token = 'Del'
  else if (statusA === 13) token = 'OpS'
  else if (statusA === 19) token = 'CtA'
  
  return [token, lexema]
}
//! -------------- Error zone --------------

function error(tipe: string, desc: string, obj: any): void {
  ERRA = true
  console.log(`Linea: ${rowg} Columna: ${colm}. Error de ${tipe}`, desc, obj)
}

function params(): void {}
function statutes(): void {}
function constvars(): void {}

function block(): void {
  let lex: string = ''
  let tok: string = ''

  if (lex !== 'inicio') {
    error('Error de Sintaxis', 'se esperaba <inicio> y llego', lex)
  }
  [tok, lex] = scanner()

  if (lex !== 'Fin') {
    constvars()
  }

  if (lex !== 'Fin') {
    statutes()
  }

  if (lex !== 'fin') {
    error('Error de Sintaxis', 'se esperaba <fin> y llego', lex)
  }
  [tok, lex] = scanner()
}

function funcParcial(): void {
  let lex: string
  let tok: string
  let idf: string = ''

  if (idf === 'principal') {
    NOPRINC = false
  }
  [tok, lex] = scanner()

  if (lex !== ')') {
    params()
  }

  if (lex !== ')') {
    error('Sintaxis', 'Se esperaba cerrar ) y llegó ', lex)
  }
  [tok, lex] = scanner()
  block()

  if (lex !== ';') {
    error('Sintaxis', 'Se esperaba <;> y llegó ', lex)
  }
  [tok, lex] = scanner()
}

function prgm(): void {
  let lex: string
  let tok: string
  let idf: string
  
  [tok, lex] = scanner()

  while (
    lex === 'constante' ||
    lex === 'entero' ||
    lex === 'decimal' ||
    lex === 'palabra' ||
    lex === 'logico' ||
    (lex === 'sintipo' && idx < entrance.length)
  ) {
    if (lex === 'constante') {
      constvars()
    } else {
      if (
        lex !== 'entero' &&
        lex !== 'decimal' &&
        lex !== 'palabra' &&
        lex !== 'logico' &&
        lex === 'sintipo'
      ) {
        error(
          'Sintaxis',
          'Se esperaba <entero>, <decimal>, <logico>, <palabra> o <sintipo> y llego ',
          lex
        )
      } else {
        [tok, lex] = scanner()
        idf = lex,
        [tok, lex] = scanner()

        if (lex === '(') {
          funcParcial()
        } else {
          constvars()
        }
      }
    }
  }
}

//* -------------- Main Zone --------------

async function main(): Promise<void> {
  let line
  let tok: string
  let lex: string

  // Get the file to compile
  const archE = await input("File to compile (*.icc) [. = Exit]: ");

  // Exit if the user enters "."
  if (archE === ".") {
    process.exit(0);
  }

  // Check if the file exists
  if (!fs.existsSync(archE)) {
    console.log("No existe el archivo: ", archE);
    return;
  }

  // Read the file contents
  const inputF = readFileSync(archE, "r+");

  // Iterate over the lines of the file and add them to the entrance string
  while ((line = inputF.readline()) !== null) {
    entrance += line;
  }

  // Close the file
  inputF.close();

  // Print the entrance string
  console.log("\n\n" + entrance, "\n\n");

  // Scan the entrance string for tokens and lexemes
  while (idx < entrance.length) {
    tok = lex = "";
    [tok, lex] = scanner();
    console.log(tok, lex);
  }

  // Call the prgm() function to compile the program
  prgm();

  // Check if the principal function was not declared
  if (NOPRINC) {
    error("Error de Semantica", "NO declaro la funcion <principal>", "");
  }

  // If there were no errors, print a success message
  if (!ERRA) {
    console.log("Compilado con exito");
  }
}

// Start the main function
main();