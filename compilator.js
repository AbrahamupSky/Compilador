"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (g && (g = 0, op[0] && (_ = 0)), _) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
Object.defineProperty(exports, "__esModule", { value: true });
var fs = require("fs");
//! Global variables
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
var matrans = [
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
//? Column Caracter
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
    return ERR;
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
            idx++;
            colm++;
        }
        if (status !== 0 && (delu.includes(entrance[idx]) || entrance.charCodeAt(idx) === 32)) {
            statusA = status;
            status = 0;
        }
        else {
            while (idx < entrance.length && status === 0 && (delu.includes(entrance[idx]) || entrance.charCodeAt(idx) === 32)) {
                if (entrance[idx] === '\n') {
                    idx++;
                    rowg++;
                    colm = 1;
                }
                else {
                    idx++;
                    colm++;
                }
            }
        }
        if (idx >= entrance.length)
            break;
        if (status !== ACP) {
            var c = entrance[idx];
            if (c === '\n') {
                rowg++;
                idx++;
                colm = 1;
            }
            else {
                idx++;
                colm++;
            }
            col = colCar(c);
        }
        if (delu.includes(entrance[idx]) && status !== 18) {
            statusA = status;
            status = ACP;
        }
        if (col >= 0 && col <= 12 && status !== ACP && status !== ERR) {
            statusA = status;
            if (delu.includes(entrance[idx]) && status !== 18)
                status = ACP;
            status = matrans[status][col];
            if (status === ACP)
                break;
            if (status !== ERR)
                lexema += entrance[idx];
        }
        else
            status = ERR;
        if (status === 7 || status === 8 || status === 9) {
            token = lexema = '';
        }
    }
    if (status === ERR || status === ACP)
        idx--;
    else
        statusA = status;
    if (statusA === 1) {
        token = 'Ide';
        if (keywords.includes(lexema))
            token = 'Res';
        else if (OPL.includes(lexema))
            token = 'OpL';
        else if (CTL.includes(lexema))
            token = 'Ctl';
    }
    else if (statusA === 2)
        token = 'Ent';
    else if (statusA === 4)
        token = 'Dec';
    else if ([5, 6, 10].includes(statusA))
        token = 'OpA';
    else if (statusA === 11 || statusA === 12)
        token = 'Del';
    else if (statusA === 13)
        token = 'OpS';
    else if (statusA === 19)
        token = 'CtA';
    return [token, lexema];
}
//! -------------- Error zone --------------
function error(tipe, desc, obj) {
    ERRA = true;
    console.log("Linea: ".concat(rowg, " Columna: ").concat(colm, ". Error de ").concat(tipe), desc, obj);
}
function params() { }
function statutes() { }
function constvars() { }
function block() {
    var _a, _b;
    var lex = '';
    var tok = '';
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
    var lex;
    var tok;
    var idf = '';
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
    var lex;
    var tok;
    var idf;
    _a = scanner(), tok = _a[0], lex = _a[1];
    while (lex === 'constante' ||
        lex === 'entero' ||
        lex === 'decimal' ||
        lex === 'palabra' ||
        lex === 'logico' ||
        (lex === 'sintipo' && idx < entrance.length)) {
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
                idf = lex, _c = scanner(), tok = _c[0], lex = _c[1];
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
function main() {
    return __awaiter(this, void 0, void 0, function () {
        var line, tok, lex, archE, inputF;
        var _a;
        return __generator(this, function (_b) {
            switch (_b.label) {
                case 0: return [4 /*yield*/, input("File to compile (*.icc) [. = Exit]: ")];
                case 1:
                    archE = _b.sent();
                    // Exit if the user enters "."
                    if (archE === ".") {
                        process.exit(0);
                    }
                    // Check if the file exists
                    if (!fs.existsSync(archE)) {
                        console.log("No existe el archivo: ", archE);
                        return [2 /*return*/];
                    }
                    inputF = readFileSync(archE, "r+");
                    // Iterate over the lines of the file and add them to the entrance string
                    while (function (, line) {
                        if (line === void 0) { line = inputF.readline(); }
                        return ;
                    })
                         !== null;
                    {
                        entrance += line;
                    }
                    // Close the file
                    inputF.close();
                    // Print the entrance string
                    console.log("\n\n" + entrance, "\n\n");
                    // Scan the entrance string for tokens and lexemes
                    while (idx < entrance.length) {
                        tok = lex = "";
                        _a = scanner(), tok = _a[0], lex = _a[1];
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
                    return [2 /*return*/];
            }
        });
    });
}
// Start the main function
main();
