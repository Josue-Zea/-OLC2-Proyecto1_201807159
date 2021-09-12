from Interprete.TS.Exception import Exception
import re
import os
errores = []
reservadas = {
    'print'    : 'TK_PRINT',
    'println'  : 'TK_PRINTLN',
}

tokens = [
    'PAROP',
    'PARCLS',
    'MAS',
    'MENOS',
    'POR',
    'DIV',
    'POT',
    'MOD',
    'PTOCOMA', 
    'DECIMAL',
    'ENTERO',
    'CADENA',
    'CHAR',
    'ID',
    'COMENTARIO_SIMPLE',
    'COMENTARIO_VARIAS_LINEAS',
] + list(reservadas.values())

# Tokens
t_MAS           = r'\+'
t_MENOS         = r'\-'
t_POR           = r'\*'
t_DIV           = r'\/'
t_POT           = r'\^'
t_MOD           = r'\%'
t_PAROP         = r'\('
t_PARCLS        = r'\)'
t_PTOCOMA       = r'\;'

def t_DECIMAL(t): # retorna un Float64.
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t

def t_ENTERO(t): # retornar un Int64
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_ID(t): # sirve para las declaraciones o asignaciones.
     r'[a-zA-Z][a-zA-Z_0-9]*'
     t.type = reservadas.get(t.value.lower(),'ID')
     return t

def t_CADENA(t): # un string.
    r'\"(\\"|.)*?\"'
    t.value = t.value[1:-1]  # remover comillas
    t.value = t.value.replace('\\n', '\n')
    t.value = t.value.replace('\\r', '\r')
    t.value = t.value.replace('\\\\', '\\')
    t.value = t.value.replace('\\"', '\"')
    t.value = t.value.replace('\\t', '\t')
    t.value = t.value.replace("\\'", '\'')
    return t

def t_CHAR(t): # es un caracter.
    r"""\' (\\'| \\\\ | \\n | \\t | \\r | \\" | .)? \'"""
    t.value = t.value[1:-1]  # remover comillas
    t.value = t.value.replace('\\\\', '\\')
    t.value = t.value.replace('\\n', '\n')
    t.value = t.value.replace('\\t', '\t')
    t.value = t.value.replace('\\r', '\r')
    t.value = t.value.replace('\\"', '\"')
    t.value = t.value.replace("\\'", '\'')
    return t

# comentario de varias lineas //...
def t_COMENTARIO_VARIAS_LINEAS(t):
    r'\#\=(.|\n)*?\=\#'
    t.lexer.lineno += t.value.count("\n") 

# Comentario simple //...
def t_COMENTARIO_SIMPLE(t):
    r'\#.*\n'
    t.lexer.lineno += 1

# Caracteres ignorados
t_ignore = " \t\r"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    errores.append(Exception("Lexico","Error lexico." + t.value[0], t.lexer.lineno, find_column(input, t)))
    t.lexer.skip(1)

# Compute column.
#     input is the input text string
#     token is a token instance
def find_column(inp, token):
    line_start = inp.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

# Construyendo el analizador léxico
import Interprete.ply.lex as lex
lexer = lex.lex()

# Asociacion
precedence = (
    #('right','IGUAL'),
    #('left', 'OR'),
    #('left', 'AND'),
    #('left', 'UNOT'),
    #('nonassoc', 'MAYORQUE', 'MENORQUE', 'MAYORIGUAL', 'MENORIGUAL', 'IGUALACION', 'DIFERENCIA'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIV', 'MOD'),
    ('right', 'UMENOS'),
    ('right', 'POT')
)

#Abstract
from Interprete.Instrucciones.Print import Print
from Interprete.Instrucciones.Println import Println
from Interprete.Expresiones.Primitivos import Primitivos
from Interprete.Expresiones.Aritmetica import Aritmetica
from Interprete.TS.Tipo import *

def p_init(t) :
    'init            : instrucciones'
    t[0] = t[1]

def p_instrucciones_instrucciones_instruccion(t) :
    'instrucciones    : instrucciones instruccion'
    if t[2] != "":
        t[1].append(t[2])
    t[0] = t[1]
    
# --------------------------------------------- INSTRUCCIONES ---------------------------------------------

def p_instrucciones_instruccion(t) :
    'instrucciones    : instruccion'
    if t[1] == "":
        t[0] = []
    else:    
        t[0] = [t[1]]

# --------------------------------------------- INSTRUCCION ---------------------------------------------

def p_instruccion(t):
    '''instruccion  : ins_print
                    | ins_println
                    | COMENTARIO_VARIAS_LINEAS
                    | COMENTARIO_SIMPLE
    '''

    t[0] = t[1]
    

def p_instruccion_error(t):
    errores.append(Exception("Sintáctico","Error Sintáctico." + t[1].value , t.lineno(1), find_column(input, t.slice[1])))
    t[0] = ""


################################################ IMPRIMIR ################################################

def p_print_produ(t) :
    '''ins_print   : TK_PRINT PAROP expresion PARCLS PTOCOMA'''
    t[0] = Print(t[3], t.lineno(1), find_column(input, t.slice[1]))

def p_println_produ(t) :
    '''ins_println   : TK_PRINTLN PAROP expresion PARCLS PTOCOMA'''
    t[0] = Println(t[3], t.lineno(1), find_column(input, t.slice[1]))

################################################ EXPRESION ################################################

def p_expresion_binaria(t):
    '''
    expresion : expresion MAS expresion
            | expresion MENOS expresion
            | expresion POR expresion
            | expresion DIV expresion
            | expresion POT expresion
            | expresion MOD expresion
    '''
    if t[2] == '+':
        t[0] = Aritmetica(Operador_Aritmetico.SUMA, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '-':
        t[0] = Aritmetica(Operador_Aritmetico.RESTA, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '*':
        t[0] = Aritmetica(Operador_Aritmetico.MULTIPLICACION, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '/':
        t[0] = Aritmetica(Operador_Aritmetico.DIVISION, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))   
    elif t[2] == '^':
        t[0] = Aritmetica(Operador_Aritmetico.POTENCIA, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '%':
        t[0] = Aritmetica(Operador_Aritmetico.MODULO, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))  

def p_expresion_unaria(t):
    '''
    expresion : MENOS expresion %prec UMENOS 
    '''
    if t[1] == '-':
        t[0] = Aritmetica(Operador_Aritmetico.UMENOS, t[2],None, t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_agrupacion(t):
    ''' expresion :   PAROP expresion PARCLS '''
    t[0] = t[2]

def p_expresion_entero(t):
    '''expresion : ENTERO'''
    t[0] = Primitivos(Tipo.INT64,t[1], t.lineno(1), find_column(input, t.slice[1]))

def p_primitivo_decimal(t):
    '''expresion : DECIMAL'''
    t[0] = Primitivos(Tipo.FLOAT64, t[1], t.lineno(1), find_column(input, t.slice[1]))

def p_primitivo_cadena(t):
    '''expresion : CADENA'''
    t[0] = Primitivos(Tipo.STRING,str(t[1]).replace('\\n', '\n'), t.lineno(1), find_column(input, t.slice[1]))

def p_primitivo_char(t):
    '''expresion : CHAR'''
    t[0] = Primitivos(Tipo.CHAR,str(t[1]).replace('\\n', '\n'), t.lineno(1), find_column(input, t.slice[1]))

import Interprete.ply.yacc as yacc
parser = yacc.yacc()

input = ''

def getErrores():
    return errores

def parse(inp) :
    global errores
    global lexer
    global parser
    errores = []
    lexer = lex.lex()
    parser = yacc.yacc()
    global input
    input = inp
    return parser.parse(inp)


from Interprete.TS.Arbol import Arbol
from Interprete.TS.TablaSimbolos import TablaSimbolos

def executeCode(entrada):
    instrucciones = parse(str(entrada))
    ast = Arbol(instrucciones)
    TSGlobal = TablaSimbolos()
    ast.set_tabla_ts_global(TSGlobal)

    for error in errores:
        ast.get_excepcion().append(error)
        ast.actualizar_consola_salto(error.__str__())

    for instr in ast.get_instruccion():
        valor = instr.interpretar(ast,TSGlobal)
        if isinstance(valor, Exception):
            ast.get_excepcion().append(valor)
            ast.actualizar_consola_salto(valor.__str__())
    
    #print(ast.get_consola())
    return(ast.get_consola())