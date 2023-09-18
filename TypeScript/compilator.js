"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.scanner = void 0;
var fs = require("fs");
var readline = require("readline");
//! Global variables
var entrance = '';
var idx = 0;
var ERRA = false;
var rowg = 1;
var colm = 1;
var NOPRINC = true;
var archE = '';
var inputF = null;
var lex = ''; // Added declaration
var tok = ''; // Added declaration
var idf = ''; // Added declaration
var ERR = -1;
var ACP = 99;
var OPAS = ['+', '-', '*', '%', '^'];
var delu = ['\n', '\t', ' ', String.fromCharCode(32)];
var keywords = [
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
];
var OPL = ["no", "y", "o"];
var CTL = ["verdadero", "falso"];
var delim = [".", ",", ";", "(", ")", "[", "]", ""];
var special = ["!", "$", "@", "#", "?"];
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
var matrans = [
    [1, 1, 2, 5, 6, 11, 10, 11, 12, 14, 15, 18, ERR],
    [1, 1, 1, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP],
    [ACP, ACP, 2, ACP, ACP, 3, ACP, ACP, ACP, ACP, ACP, ACP, ACP],
    [ERR, ERR, 4, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR],
    [ACP, ACP, 4, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP],
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP],
    [ACP, ACP, ACP, ACP, 7, ACP, 8, ACP, ACP, ACP, ACP, ACP, ACP],
    [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [8, 8, 8, 8, 8, 8, 9, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 9, 0, 8, 9, 8, 8, 8, 8, 8, 8],
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP],
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP],
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, 13, ACP, ACP, ACP],
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP],
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP],
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, 16, ACP, ACP, ACP],
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP],
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP],
    [18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 19, 18],
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP], //19
];
//? -------------- Column Caracter ---------------
function colCar(x) {
    if (/^[a-zA-Z]$/.test(x) || delu.includes(x)) {
        return 0;
    }
    else if (x === '_') {
        return 1;
    }
    else if (x.match(/^[0-9]+$/)) {
        return 2;
    }
    else if (OPAS.includes(x)) {
        return 3;
    }
    else if (x === '/') {
        return 4;
    }
    else if (x === '.') {
        return 5;
    }
    else if (x === '*') {
        return 6;
    }
    else if (delim.includes(x)) {
        return 7;
    }
    else if (x === ':') {
        return 8;
    }
    else if (x === '=') {
        return 9;
    }
    else if (['<'].includes(x)) {
        return 10;
    }
    else if (['"'].includes(x)) {
        return 11;
    }
    else if (special.includes(x)) {
        return 12;
    }
    if (!delu.includes(x)) {
        console.log(x + ' is not a char or illegal symbol');
        return ERR;
    }
}
//? -------------- Scanner --------------
function scanner() {
    var lexema = '';
    var token = '';
    var status = 0;
    var statusA = 0;
    var col = -1;
    while (idx < entrance.length && status !== ERR && status !== ACP) {
        while (status === 7 && entrance[idx] !== '\n') {
            idx += 1;
            colm += 1;
        }
        if (status !== 0 && (delu.includes(entrance[idx]) || entrance.charCodeAt(idx) === 32)) {
            statusA = status;
            status = 0;
        }
        else {
            while (idx < entrance.length &&
                status === 0 &&
                (delu.includes(entrance[idx]) || entrance.charCodeAt(idx) === 32)) {
                if (entrance[idx] === '\n') {
                    idx += 1;
                    rowg += 1;
                    colm = 1;
                }
                else {
                    idx += 1;
                    colm += 1;
                }
            }
        }
        if (idx >= entrance.length)
            break;
        if (status !== ACP) {
            var c_1 = entrance[idx];
            if (c_1 === '\n') {
                rowg += 1;
                idx += 1;
                colm = 1;
            }
            else {
                idx += 1;
                colm += 1;
            }
            col = colCar(c_1);
        }
        var c = void 0;
        if (delu.includes(entrance[idx]) && status !== 18) {
            statusA = status;
            status = ACP;
        }
        if (col >= 0 && col <= 12 && status !== ACP && status !== ERR) {
            statusA = status;
            c = entrance[idx];
            if (delu.includes(c) && status !== 18)
                status = ACP;
            status = matrans[status][col];
            if (status === ACP)
                break;
            if (status !== ERR) {
                lexema += c;
            }
        }
        else {
            status = ERR;
        }
        if (status === 7 || status === 8 || status === 9) {
            token = lexema = '';
        }
    }
    if (status === ERR || status === ACP)
        idx -= 1;
    else
        statusA = status;
    if (statusA === 1) {
        token = 'Ide';
        if (keywords.includes(lexema)) {
            token = 'Res';
        }
        else if (OPL.includes(lexema)) {
            token = 'OpL';
        }
        else if (CTL.includes(lexema)) {
            token = 'CtL';
        }
    }
    else if (statusA === 2) {
        token = 'Ent';
    }
    else if (statusA === 4) {
        token = 'Dec';
    }
    else if (statusA in [5, 6, 10]) {
        token = 'OpA';
    }
    else if (statusA === 11 || statusA === 12) {
        token = 'Del';
    }
    else if (statusA === 13) {
        token = 'OpS';
    }
    else if (statusA === 19) {
        token = 'CtA';
    }
    return [token, lexema];
}
exports.scanner = scanner;
//! -------------- Error zone --------------
function error(tipe, desc, obj) {
    ERRA = true;
    console.log("Linea: ".concat(rowg, "[").concat(colm, "]. Error de ").concat(tipe), desc, obj);
}
//* -------------- To use --------------
function params() { }
function statutes() { }
function constvars() { }
//* -------------- To use --------------
function block() {
    var _a, _b;
    if (lex !== 'inicio') {
        error('Error de Sintaxis', 'se esperaba <inicio> y llego', lex);
    }
    _a = scanner(), tok = _a[0], lex = _a[1];
    if (lex !== 'Fin') {
        constvars();
    }
    if (lex !== 'Fin') {
        statutes();
    }
    if (lex !== 'fin') {
        error('Error de Sintaxis', 'se esperaba <fin> y llego', lex);
    }
    _b = scanner(), tok = _b[0], lex = _b[1];
}
function funcParcial() {
    var _a, _b, _c;
    if (idf === 'principal') {
        NOPRINC = false;
    }
    _a = scanner(), tok = _a[0], lex = _a[1];
    if (lex !== ')') {
        params();
    }
    if (lex !== ')') {
        error('Sintaxis', 'Se esperaba cerrar ) y llegó ', lex);
    }
    _b = scanner(), tok = _b[0], lex = _b[1];
    block();
    if (lex !== ';') {
        error('Sintaxis', 'Se esperaba <;> y llegó ', lex);
    }
    _c = scanner(), tok = _c[0], lex = _c[1];
}
function prgm() {
    var _a, _b, _c;
    _a = scanner(), tok = _a[0], lex = _a[1];
    while (lex === 'constante' ||
        lex === 'entero' ||
        lex === 'decimal' ||
        lex === 'palabra' ||
        lex === 'logico' ||
        lex === 'sintipo' ||
        lex === 'principal' && NOPRINC) {
        if (lex === 'constante') {
            constvars();
        }
        else {
            if (lex !== 'entero' &&
                lex !== 'decimal' &&
                lex !== 'palabra' &&
                lex !== 'logico' &&
                lex === 'sintipo') {
                error('Sintaxis', 'Se esperaba <entero>, <decimal>, <logico>, <palabra> o <sintipo> y llego ', lex);
            }
            else {
                _b = scanner(), tok = _b[0], lex = _b[1];
                if (tok === 'Ide')
                    idf = lex;
                else {
                    error('Sintaxis', 'Se esperaba <Ide> y llegó ', tok);
                }
                _c = scanner(), tok = _c[0], lex = _c[1];
                if (lex === '(') {
                    funcParcial();
                }
                else {
                    constvars();
                }
            }
        }
    }
}
//* -------------- Main Zone --------------
var rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});
function main() {
    // Manejador de señal para SIGINT (Ctrl + C)
    process.on('SIGINT', function () {
        console.log("\n¡Detenido por el usuario!");
        rl.close();
        process.exit(1); // Salir del programa con código de error 1
    });
    function readInput() {
        rl.question('File to compile (*.icc) [. = Exit]: ', function (input) {
            if (input === '.') {
                rl.close();
                exit();
                return;
            }
            archE = input.trim();
            try {
                var inputF_1 = fs.readFileSync(archE, 'utf8');
                entrance = inputF_1.toString();
                processInput();
            }
            catch (error) {
                console.error("Error: ".concat(error.message));
                readInput();
            }
        });
    }
    function processInput() {
        var _a;
        console.log("\n\n".concat(entrance, "\n\n"));
        var tok, lex;
        while (idx < entrance.length) {
            _a = scanner(), tok = _a[0], lex = _a[1];
            console.log(tok, lex);
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
