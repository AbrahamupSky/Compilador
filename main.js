"use strict";
var _a;
Object.defineProperty(exports, "__esModule", { value: true });
var fs = require("fs");
var entrance = '';
var ERR = -1;
var ACP = 99;
var idx = 0;
var ERRA = false;
var NOPRINC = true;
var rowg = 1;
var colm = 1;
var OPAS = ['+', '-', '*', '%', '^'];
var delu = ['\n', '\t', ' ', String.fromCharCode(32)];
var keywords = [
    'constante', 'entero', 'decimal', 'logico', 'palabra', 'sintipo',
    'inicio', 'fin', 'si', 'sino', 'hacer', 'desde', 'hasta', 'incr',
    'decr', 'regresa', 'imprime', 'imprimenl', 'lee', 'interrumpe', 'continua'
];
var OPL = ['no', 'y', 'o'];
var CTL = ['verdadero', 'falso'];
var delim = ['.', ',', ';', '(', ')', '[', ']'];
var special = ['!', '$', '#', '@', '?'];
var matrans = [
    // col 0 = 'letra'
    // col 1 = '_'
    // col 2 = 'Digito'
    // col 3 = 'OPAS'
    // col 4 = '/'
    // col 5 = '.'
    // col 6 = '*'
    // col 7 = 'Del'
    // col 8 = ':'
    // col 9 = '='
    // col 10 = '<'
    // col 11 = "
    // col 12 = special
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
function colCar(x) {
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
        console.log(x, 'is not a char or illegal symbol');
        return ERR;
    }
}
function scanner() {
    var entrance;
    var matrans;
    var ERR;
    var ACP;
    var idx;
    var colm;
    var rowg;
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
        if (status !== 0 && (entrance[idx] in delu || entrance.charCodeAt(idx) === 32)) {
            statusA = status;
            status = 0;
        }
        else {
            while (idx < entrance.length && status === 0 && (entrance[idx] in delu || entrance.charCodeAt(idx) === 32)) {
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
            var c = entrance[idx];
            if (c === '\n') {
                rowg += 1;
                idx += 1;
                colm = 1;
            }
            else {
                idx += 1;
                colm += 1;
            }
            col = colCar(c);
        }
        if (c in delu && status !== 18) {
            statusA = status;
            status = ACP;
        }
        if (col >= 0 && col <= 12 && status !== ACP && status !== ERR) {
            statusA = status;
            if (c in delu && status !== 18)
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
    if (status === ERR || status === ACP) {
        idx -= 1;
    }
    else {
        statusA = status;
    }
    if (statusA === 1) {
        token = 'Ide';
    }
    var token;
    if (statusA === 1) {
        token = 'Ide';
        if (keywords.includes(lexema))
            token = 'Res';
        else if (OPL.includes(lexema))
            token = 'OpL';
        else if (CTL.includes(lexema))
            token = 'CtL';
    }
    else if (statusA === 2) {
        token = 'Ent';
    }
    else if (statusA === 4) {
        token = 'Dec';
    }
    else if ([5, 6, 10].includes(statusA)) {
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
function error(tipe, desc, obj) {
    ERRA = true;
    console.log("Linea:[".concat(rowg, "] Columna:[").concat(colm, "] Error de ").concat(tipe), desc, obj);
}
function params() { }
function estatutos() { }
function constvars() { }
function bloque() {
    var _a, _b;
    if (lex !== 'inicio') {
        error('Error de Sintaxis', 'se esperaba <inicio> y llego', lex);
    }
    _a = scanner(), tok = _a[0], lex = _a[1];
    if (lex !== 'Fin') {
        constvars();
    }
    if (lex !== 'Fin') {
        estatutos();
    }
    if (lex !== 'fin') {
        error('Error de Sintaxis', 'se esperaba <fin> y llego', lex);
    }
    _b = scanner(), tok = _b[0], lex = _b[1];
}
function funcParcial() {
    var _a, _b;
    if (idf === 'principal')
        NOPRINC = false[tok, lex] = scanner();
    if (lex !== ')') {
        params();
    }
    if (lex !== ')') {
        error('Sintaxis', 'Se esperaba cerrar ) y llego ', lex);
    }
    _a = scanner(), tok = _a[0], lex = _a[1];
    bloque();
    if (lex !== '') {
        error('Sintaxis', 'Se esperaba <> y llego ', lex);
    }
    _b = scanner(), tok = _b[0], lex = _b[1];
}
function prgm() {
    var _a, _b;
    _a = scanner(), tok = _a[0], lex = _a[1];
    while (['constante', 'entero', 'decimal', 'logico', 'palabra', 'sintipo'].includes(lex) && idx < entrance.length) {
        if (lex === 'constante') {
            constvars();
        }
        else {
            if (!['entero', 'decimal', 'palabra', 'logico', 'sintipo'].includes(lex)) {
                error('Sintaxis', 'Se esperaba <entero>, <decimal>, <logico>, <palabra> o <sintipo> y llego ', lex);
            }
            else {
                _b = scanner(), tok = _b[0], lex = _b[1];
                idf = lex[tok, lex] = scanner();
                if (lex === '(') {
                    funcParcial();
                }
                else {
                    constvars();
                }
            }
        }
    }
    if (NOPRINC) {
        error('Error de Semantica', 'NO declaro la funcion <principal>', '');
    }
    if (!ERRA) {
        console.log('Compilado con exito');
    }
}
var readline = require('readline');
var rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});
function getInputFile() {
    return new Promise(function (resolve, reject) {
        rl.question('File to compile (*.icc) [. = Exit]: ', function (archE) {
            if (archE === '.') {
                reject('Exit');
            }
            else {
                resolve(archE);
            }
        });
    });
}
if (require.main === module) {
    var archE = '';
    console.log(archE.slice(-3));
    while (!archE.endsWith('.icc')) {
        archE = prompt('File to compile (*.icc) [. = Exit]: ');
        if (archE === '.')
            process.exit(0);
        try {
            var inputF = fs.readFileSync(archE, 'r+');
            break;
        }
        catch (error) {
            console.log('No existe el archivo: ', archE);
        }
    }
    if (inputF !== null) {
        var entrance_1 = '';
        while ((line = inputF.readLineSync())) {
            entrance_1 += line;
        }
        inputF.close();
    }
    console.log('\n\n' + entrance + '\n\n');
    var tok = '';
    var lex = '';
    var idx_1 = 0;
    while (idx_1 < entrance.length) {
        _a = scanner(), tok = _a[0], lex = _a[1];
        console.log(tok, lex);
    }
    process.exit(0);
    prgm();
    if (NOPRINC) {
        error('Error de Semantica', 'NO declaro la funcion <principal>', '');
    }
    if (ERRA === false) {
        console.log('Compilado con exito');
    }
}
