import * as fs from "fs";
import * as readline from 'readline';

//! Global variables
let entrance: string = '';
let idx: number = 0;
let ERRA: boolean = false;
let rowg: number = 1;
let colm: number = 1;
let NOPRINC: boolean = true;
let archE: string = '';
let inputF: any = null;
let lex: string = '';
let tok: string = '';
let idf: string = '';

const ERR: number = -1;
const ACP: number = 99;
const OPAS: string[] = ['+', '-', '*', '%', '^'];
const delu: string[] = ['\n', '\t', ' ', String.fromCharCode(32)];
const keywords: string[] = [
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
  "continua",
  "mientras",
  "que"
];
const OPL: string[] = ["no", "y", "o"];
const CTL: string[] = ["verdadero", "falso"];
const delim: string[] = [".", ",", ";", "(", ")", "[", "]", ""];
const special: string[] = ["!", "$", "@", "#", "?"];

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
const matrans: number[][] = [
  [  1 ,  1 ,  2 ,  5 ,  6 ,  11,  10,  11,  12,  14,  15,  18, ERR ], //0
  [  1 ,  1 ,  1 , ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP ], //1
  [ ACP, ACP,  2 , ACP, ACP,  3,  ACP, ACP, ACP, ACP, ACP, ACP, ACP ], //2
  [ ERR, ERR,  4 , ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR ], //3
  [ ACP, ACP,  4 , ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP ], //4
  [ ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP ], //5
  [ ACP, ACP, ACP, ACP,  7 , ACP,  8 , ACP, ACP, ACP, ACP, ACP, ACP ], //6
  [  7 ,  7 ,  7 ,  7 ,  7 ,  7 ,  7 ,  7,   7 ,  7 ,  7 ,  7 ,  7  ], //7
  [  8 ,  8 ,  8 ,  8 ,  8 ,  8 ,  9 ,  8 ,  8 ,  8 ,  8 ,  8 ,  8  ], //8
  [  8 ,  8 ,  8 ,  9 ,  0 ,  8 ,  9 ,  8 ,  8 ,  8 ,  8 ,  8 ,  8  ], //9
  [ ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP ], //10
  [ ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP ], //11
  [ ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP,  13, ACP, ACP, ACP ], //12
  [ ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP ], //13
  [ ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP ], //14
  [ ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP,  16, ACP, ACP, ACP ], //15
  [ ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP ], //16
  [ ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP ], //17
  [  18,  18,  18,  18,  18,  18,  18,  18,  18,  18,  18,  19,  18 ], //18
  [ ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP ], //19
];

//? -------------- Column Caracter ---------------
function colCar(x: string): any {
  if (/^[a-zA-Z]$/.test(x) || delu.includes(x)) {return 0}
  else if (x === '_')           {return 1}
  else if (x.match(/^[0-9]+$/))       {return 2}
  else if (OPAS.includes(x))    {return 3}
  else if (x === '/')           {return 4}
  else if (x === '.')           {return 5}
  else if (x === '*')           {return 6}
  else if (delim.includes(x))   {return 7}
  else if (x === ':')           {return 8}
  else if (x === '=')           {return 9}
  else if (['<'].includes(x))   {return 10}
  else if (['"'].includes(x))   {return 11}
  else if (special.includes(x)) {return 12}

  if (!delu.includes(x)) {
    console.log(x + ' is not a char or illegal symbol')
    return ERR
  }
}

//? -------------- Scanner --------------
export function scanner(): [string, string] {
  let lexema: string = ''
  let token: string = ''
  let status: number = 0
  let statusA: number = 0
  let col: number = -1

  while (idx < entrance.length && status !== ERR && status === ACP) {
    while (status === 7 && entrance[idx] !== '\n') {
      idx += 1
      colm += 1
    }

    if (status !== 0 && (delu.includes(entrance[idx]) || entrance.charCodeAt(idx) === 32)) {
      statusA = status
      status = 0
    } else {
      while (
        idx < entrance.length &&
        status === 0 &&
        (delu.includes(entrance[idx]) || entrance.charCodeAt(idx) === 32)
      ) {
        if (entrance[idx] === '\n') {
          idx += 1
          rowg += 1
          colm = 1
        } else {
          idx += 1
          colm += 1
        }
      }
    }
    
    if (idx >= entrance.length) break

    if (status !== ACP) {
      const c = entrance[idx]

      if (c === '\n') {
        rowg += 1
        idx += 1
        colm = 1
      } else {
        idx += 1
        colm += 1
      }

      col = colCar(c)
    }
    let c: string

    if (delu.includes(entrance[idx]) && status !== 18) {
      statusA = status
      status = ACP
    }

    if (col >= 0 && col <= 12 && status !== ACP && status !== ERR) {
      statusA = status

      c = entrance[idx]
      if (delu.includes(c) && status !== 18) status = ACP
      status = matrans[status][col]

      if (status === ACP) break
      if (status !== ERR) {lexema += c}
    } else {
      status = ERR
    }

    if (status === 7 || status === 8 || status === 9) {
      token = lexema = ''
    }
  }

  if (status === ERR || status === ACP) idx -= 1
  else statusA = status

  if (statusA === 1) {
    token = 'Ide'

    if (keywords.includes(lexema)) {token = 'Res'}
    else if (OPL.includes(lexema)) {token = 'OpL'}
    else if (CTL.includes(lexema)) {token = 'CtL'}
  }
  else if (statusA === 2) {token = 'Ent'}
  else if (statusA === 4) {token = 'Dec'}
  else if (statusA in [5, 6, 10]) {
    token = 'OpA'
  }
  else if (statusA === 11 || statusA === 12) {token = 'Del'}
  else if (statusA === 13) {token = 'OpS'}
  else if (statusA === 19) {token = 'CtA'}

  return [token, lexema]
}

//! -------------- Error zone --------------

function error(tipe: string, desc: string, obj: any): void {
  ERRA = true
  console.log(`Linea: ${rowg}[${colm}]. Error de ${tipe}`, desc, obj)
}

//* -------------- To use --------------

function params(): void {}
function statutes(): void {}
function constvars(): void {}

//* -------------- To use --------------

function block(): void {
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
  [tok, lex] = scanner()

  while (
    lex === 'constante' ||
    lex === 'entero' ||
    lex === 'decimal' ||
    lex === 'palabra' ||
    lex === 'logico' ||
    lex === 'sintipo' ||
    lex === 'principal' && NOPRINC
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

        if (tok === 'Ide') idf = lex
        else {
          error('Sintaxis', 'Se esperaba <Ide> y llegó ', tok)
        }

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

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function main() {

  // Manejador de señal para SIGINT (Ctrl + C)
  process.on('SIGINT', () => {
    console.log("\n¡Detenido por el usuario!");
    rl.close();
    process.exit(1); // Salir del programa con código de error 1
  });

  function readInput() {
    rl.question('File to compile (*.icc) [. = Exit]: ', (input) => {
      if (input === '.') {
        rl.close();
        exit();
        return;
      }

      archE = input.trim();

      try {
        const inputF = fs.readFileSync(archE, 'utf8');
        entrance = inputF.toString();
        processInput();
      } catch (error) {
        console.error(`Error: ${error.message}`);
        readInput();
      }
    });
  }

  function processInput() {
    console.log(`\n\n${entrance}\n\n`);

    let tok: string, lex: string;

    while (idx < entrance.length) {
      [tok, lex] = scanner();
      console.log(tok, lex);
      if (tok === 'OpA') break
    }

    exit();
  }

  function exit() {
    rl.close();
    process.exit(0);
  }

  readInput();
}

main();