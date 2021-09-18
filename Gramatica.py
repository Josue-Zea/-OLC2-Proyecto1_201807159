from Interprete.TS.Exception import Exception
import re
import os
errores = []
structs = []
reservadas = {
    'print'     : 'TK_PRINT',
    'println'   : 'TK_PRINTLN',
    'Int64'     : 'TK_INT64',
    'Float64'   : 'TK_FLOAT64',
    'Bool'      : 'TK_BOOL',
    'Char'      : 'TK_CHAR',
    'String'    : 'TK_STRING',
    'if'        : 'TK_IF',
    'elseif'    : 'TK_ELSEIF',
    'else'      : 'TK_ELSE',
    'end'       : 'TK_END',
    'true'      : 'TK_TRUE',
    'false'     : 'TK_FALSE',
    'while'     : 'TK_WHILE',
    'break'     : 'TK_BREAK',
    'continue'  : 'TK_CONTINUE',
    'return'    : 'TK_RETURN',
    'function'  : 'TK_FUNCTION',
    'for'       : 'TK_FOR',
    'in'        : 'TK_IN',
    'struct'    : 'TK_STRUCT',
    'mutable'   : 'TK_MUTABLE',
    'nothing'   : 'TK_NOTHING'
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
    'MAYEQUALS',
    'MENEQUALS',
    'IGUALDAD',
    'DIFERENCIA',
    'MAYQ',
    'MENQ',
    'IGUAL',
    'AND',
    'OR',
    'NOT',
    'DOBLEPUNTO',
    'DOSPTOS',
    'PTO',
    'COROP',
    'CORCLS',
    'COMA',
    'DECIMAL',
    'ENTERO',
    'CADENA',
    'CHAR',
    'ID'
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
t_MAYEQUALS     = r'\>\='
t_MENEQUALS     = r'\<\='
t_IGUALDAD      = r'\=\='
t_DIFERENCIA    = r'\!\='
t_MAYQ          = r'\>'
t_MENQ          = r'\<'
t_IGUAL         = r'\='
t_AND           = r'\&\&'
t_OR            = r'\|\|'
t_NOT           = r'\!'
t_DOBLEPUNTO    = r'\:\:'
t_DOSPTOS       = r'\:'
t_COMA          = r'\,'
t_PTO           = r'\.'
t_COROP         = r'\['
t_CORCLS        = r'\]'

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
     t.type = reservadas.get(t.value,'ID')
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
    r'\#=(.|\n)*?=\#'
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
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
    ('left', 'IGUALDAD', 'DIFERENCIA'),
    ('left', 'MAYQ', 'MENQ', 'MAYEQUALS', 'MENEQUALS'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIV', 'MOD'),
    ('right', 'UMENOS'),
    ('right', 'POT')
)

#Abstract
from Interprete.Instrucciones.Funcion import Funcion
from Interprete.Instrucciones.Llamada import Llamada
from Interprete.Instrucciones.Print import Print
from Interprete.Instrucciones.Println import Println
from Interprete.Instrucciones.Asignacion_declaracion import Asignacion
from Interprete.Instrucciones.If import If
from Interprete.Instrucciones.While import While
from Interprete.Instrucciones.Break import Break
from Interprete.Instrucciones.Return import Return
from Interprete.Instrucciones.Continue import Continue
from Interprete.Instrucciones.Nativas import Nativas
from Interprete.Instrucciones.For import For
from Interprete.Instrucciones.Plantilla_struct import Plantilla_struct
from Interprete.Instrucciones.Struct import Struct
from Interprete.Instrucciones.Arreglo import Arreglo
from Interprete.Instrucciones.Acceso_arreglo import Acceso_arreglo
from Interprete.Instrucciones.Asignar_val_arreglo import Asignar_val_arreglo
from Interprete.Instrucciones.Llamada_struct import Llamada_struct
from Interprete.Instrucciones.Llamada_atributo_struct import Llamada_atributo_struct
from Interprete.Instrucciones.Asignar_valor_var_struct import Asignar_valor_var_struct

from Interprete.Expresiones.Primitivos import Primitivos
from Interprete.Expresiones.Aritmetica import Aritmetica
from Interprete.Expresiones.Relacionales import Relacional
from Interprete.Expresiones.Logicas import Logica
from Interprete.Expresiones.Identificador import Identificador
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
                    | ins_if
                    | ins_break
                    | ins_continue
                    | ins_return
                    | ins_while
                    | ins_asignacion
                    | ins_decla_funcion
                    | ins_llamada_funcion
                    | ins_for
                    | ins_declarate_struct
                    | ins_create_struct
                    | ins_cambio_var_strct
                    | ins_asignacion_arreglo
    '''
    t[0] = t[1]

def p_error(t):
    'instruccion : error PTOCOMA'
    errores.append(Exception("Sintáctico","Error Sintáctico." + str(t.value), t.lineno, find_column(input, t)))
    t = ""

############################################### ASIGNACION ARREGLO ################################################
def p_ins_asignar_arreglo(t):
    'ins_asignacion_arreglo : ID posiciones_arreglo IGUAL expresion PTOCOMA'
    t[0] = Asignar_val_arreglo(t[1], t[2], t[4],  t.lineno(1), find_column(input, t.slice[1]))

def p_posiciones_arreglo(t):
    'posiciones_arreglo : posiciones_arreglo posiciones_arreglo'
    t[1].append(t[2])
    t[0] = t[1]

def p_posiciones_arreglo2(t):
    'posiciones_arreglo : position_arreglo'
    t[0] = [t[1]]

def p_posiciones_arreglo3(t):
    'position_arreglo : COROP expresion CORCLS'
    t[0] = t[2]

######################################### ASIGNAR VALOR A VARIABLE DE STRUCT ######################################

def p_asignar_valor_var_struct(t):
    'ins_cambio_var_strct : ID PTO ID expresion IGUAL expresion PTOCOMA'
    t[0] = Asignar_valor_var_struct(t[1], t[3], t[5],  t.lineno(1), find_column(input, t.slice[1]))

################################################## CREATE STRUCT ##################################################

def p_instr_create_struct(t):
    'ins_create_struct : ID IGUAL ID PAROP params_call PARCLS PTOCOMA'
    t[0] = Llamada_struct(t[1], t[3], t[5] , t.lineno(1), find_column(input, t.slice[1]))

################################################# DECLARATE STRUCT ################################################

def p_instr_declarate_struct(t):
    '''ins_declarate_struct : TK_STRUCT ID params_struct TK_END PTOCOMA
                        | TK_MUTABLE TK_STRUCT ID params_struct TK_END PTOCOMA'''
    if len(t) == 6:
        t[0] = Plantilla_struct(0, t[2], t[3], t.lineno(1), find_column(input, t.slice[1]))
    elif len(t) == 7:
        t[0] = Plantilla_struct(1, t[3], t[4], t.lineno(1), find_column(input, t.slice[1]))

def p_params_struct1(t) :
    'params_struct     : params_struct param_struct'
    t[1].append(t[2])
    t[0] = t[1]
    
def p_params_struct2(t) :
    'params_struct    : param_struct'
    t[0] = [t[1]]

def p_params_struct3(t) :
    '''param_struct     : ID DOBLEPUNTO tipos_ins PTOCOMA
                        | ID PTOCOMA'''
    if len(t) == 5:
        t[0] = {'tipoDato':t[3],'identificador':t[1]}
    elif len(t) == 3:
        t[0] = {'tipoDato':any,'identificador':t[1]}

##################################################### FOR #########################################################

def p_instr_for1(t):
    '''ins_for : TK_FOR ID TK_IN expresion DOSPTOS expresion instrucciones TK_END PTOCOMA
                | TK_FOR ID TK_IN expresion instrucciones TK_END PTOCOMA'''
    if len(t) == 9:
        t[0] = For(t[2], t[4], t[6], t[7],  t.lineno(1), find_column(input, t.slice[1]))
    elif len(t) == 7:
        t[0] = For(t[2], t[4], None, t[5],  t.lineno(1), find_column(input, t.slice[1]))

############################################## LLAMADA DE FUNCIONES ###############################################

def p_llamada_de_funcion(t) :
    'ins_llamada_funcion     : ID PAROP PARCLS PTOCOMA'
    t[0] = Llamada(t[1], [], t.lineno(1), find_column(input, t.slice[1]))

def p_llamada_de_funcion_parametros(t) :
    'ins_llamada_funcion     : ID PAROP params_call PARCLS PTOCOMA'
    if t[1] == 'log' or t[1] =='log10' or t[1] =='sin' or t[1] == 'cos'or t[1] =='tan'or t[1] =='sqrt'or t[1] =='parse'or t[1] =='trunc'or t[1] =='float'or t[1] =='string' or t[1] =='push'or t[1] =='pop'or t[1] =='length' or t[1] =='typeof' or t[1] =='uppercase' or t[1] =='lowercase':
        t[0] = Nativas(t[1], t[3], t.lineno(1), find_column(input, t.slice[1]))
    else:
        t[0] = Llamada(t[1], t[3], t.lineno(1), find_column(input, t.slice[1]))

def p_params_llamada(t) :
    'params_call     : params_call COMA param_call'
    t[1].append(t[3])
    t[0] = t[1]
    
def p_parametros_llamadas_parametro_llamada(t) :
    'params_call    : param_call'
    t[0] = [t[1]]

def p_parametro_llamada(t) :
    '''param_call     : expresion
                    | tipos_ins'''
    t[0] = t[1]

########################################### DECLARACION DE FUNCIONES ##############################################

def p_declara_functions(t):
    'ins_decla_funcion : TK_FUNCTION ID PAROP PARCLS instrucciones TK_END PTOCOMA'
    t[0] = Funcion(t[2], [], t[5], t.lineno(1), find_column(input, t.slice[1]))

def p_declara_functions2(t):
    'ins_decla_funcion : TK_FUNCTION ID PAROP params PARCLS instrucciones TK_END PTOCOMA'
    t[0] = Funcion(t[2], t[4], t[6], t.lineno(1), find_column(input, t.slice[1]))

def p_params_parametros(t) :
    'params     : params COMA param'
    t[1].append(t[3])
    t[0] = t[1]
    
def p_params_parametro(t) :
    'params    : param'
    t[0] = [t[1]]

def p_parametro(t) :
    'param     : ID DOBLEPUNTO tipos_ins'
    t[0] = {'tipoDato':t[3],'identificador':t[1]}

################################################# RETURN #########################################################

def p_return(t):
    'ins_return : TK_RETURN expresion PTOCOMA'    
    t[0] = Return(t[2], t.lineno(1), find_column(input, t.slice[1]))

################################################# CONTINUE #######################################################

def p_continue(t):
    'ins_continue : TK_CONTINUE PTOCOMA'
    t[0] = Continue(t.lineno(1), find_column(input, t.slice[1]));

################################################# BREAK ###########################################################

def p_break(t):
    'ins_break : TK_BREAK PTOCOMA'
    t[0] = Break(t.lineno(1), find_column(input, t.slice[1]));

################################################# WHILE ##########################################################

def p_sentencia_while(t) :
    'ins_while     : TK_WHILE expresion instrucciones TK_END PTOCOMA'
    t[0] = While(t[2], t[3], t.lineno(1), find_column(input, t.slice[1]))

################################################## IF ############################################################
def p_if(t):
    'ins_if     : TK_IF expresion instrucciones TK_END PTOCOMA'
    t[0] = If(t[2], t[3], None, None, t.lineno(1), find_column(input, t.slice[1]))

def p_if_else(t):
    'ins_if     : TK_IF expresion instrucciones TK_ELSE instrucciones TK_END PTOCOMA'
    t[0] = If(t[2], t[3], t[5], None, t.lineno(1), find_column(input, t.slice[1]))

def p_if_elseif(t):
    'ins_if     : TK_IF expresion instrucciones ins_elseif TK_END PTOCOMA'
    t[0] = If(t[2], t[3], None, t[4], t.lineno(1), find_column(input, t.slice[1]))

def p_if_elseif2(t):
    'ins_elseif     : TK_ELSEIF expresion instrucciones'
    t[0] = If(t[2], t[3], None, None, t.lineno(1), find_column(input, t.slice[1]))

def p_if_elseif3(t):
    'ins_elseif     : TK_ELSEIF expresion instrucciones ins_elseif'
    t[0] = If(t[2], t[3], None, t[4], t.lineno(1), find_column(input, t.slice[1]))

def p_if_elseif4(t):
    'ins_elseif     : TK_ELSEIF expresion instrucciones TK_ELSE instrucciones'
    t[0] = If(t[2], t[3], t[5], None, t.lineno(1), find_column(input, t.slice[1]))

########################################## ASIGNACION/DECLARACION ################################################

def p_asignacion_ins(t):
    'ins_asignacion    : ID IGUAL expresion PTOCOMA'
    t[0] = Asignacion(t[1], t[3], None, t.lineno(1), find_column(input, t.slice[1]))

def p_asignacion_ins2(t):
    'ins_asignacion    : ID IGUAL expresion DOBLEPUNTO tipos_ins PTOCOMA'
    t[0] = Asignacion(t[1], t[3], t[5], t.lineno(1), find_column(input, t.slice[1]))

def p_tipos_ins(t):
    """tipos_ins : TK_INT64
                | TK_FLOAT64
                | TK_CHAR
                | TK_STRING
                | TK_BOOL
    """
    if t[1] == 'Int64':
        t[0] = Tipo.INT64
    elif t[1] == 'Float64':
        t[0] = Tipo.FLOAT64
    elif t[1] == 'Bool':
        t[0] = Tipo.BOOLEAN
    elif t[1] == 'String':
        t[0] = Tipo.STRING
    elif t[1] == 'Char':
        t[0] = Tipo.CHAR

################################################ PRINT ################################################

def p_print_produ(t) :
    '''ins_print   : TK_PRINT PAROP params_call PARCLS PTOCOMA'''
    t[0] = Print(t[3], t.lineno(1), find_column(input, t.slice[1]))

def p_println_produ(t) :
    '''ins_println   : TK_PRINTLN PAROP params_call PARCLS PTOCOMA'''
    t[0] = Println(t[3], t.lineno(1), find_column(input, t.slice[1]))

################################################ EXPRESION ################################################

def p_exp_doble(t):
    '''
    expresion : expresion MAS expresion
            | expresion MENOS expresion
            | expresion POR expresion
            | expresion DIV expresion
            | expresion POT expresion
            | expresion MOD expresion
            | expresion MENQ expresion
            | expresion MENEQUALS expresion
            | expresion MAYQ expresion
            | expresion MAYEQUALS expresion
            | expresion IGUALDAD expresion
            | expresion DIFERENCIA expresion
            | expresion AND expresion
            | expresion OR expresion
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
    
    #Relacionales
    elif t[2] == '<':
        t[0] = Relacional(Operador_Relacional.MENQ, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '<=':
        t[0] = Relacional(Operador_Relacional.MENEQUALS, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '>':
        t[0] = Relacional(Operador_Relacional.MAYQ, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '==':
        t[0] = Relacional(Operador_Relacional.IGUALDAD, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '>=':
        t[0] = Relacional(Operador_Relacional.MAYEQUALS, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '!=':
        t[0] = Relacional(Operador_Relacional.DIFERENCIA, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    #Logicas
    elif t[2] == '&&':
        t[0] = Logica(Operador_Logico.AND, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '||':
        t[0] = Logica(Operador_Logico.OR, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))

def p_exp_simple(t):
    '''
    expresion : MENOS expresion %prec UMENOS
            | NOT expresion %prec NOT
    '''
    if t[1] == '-':
        t[0] = Aritmetica(Operador_Aritmetico.UMENOS, t[2],None, t.lineno(1), find_column(input, t.slice[1]))
    elif t[1] == '!':
         t[0] = Logica(Operador_Logico.NOT, t[2],None, t.lineno(1), find_column(input, t.slice[1]))

def p_expr_agrupacion(t):
    ''' expresion :   PAROP expresion PARCLS '''
    t[0] = t[2]

def p_exp_llamada(t):
    '''expresion : ins_llamada_funcion'''
    t[0] = t[1]

def p_exp_int(t):
    '''expresion : ENTERO'''
    t[0] = Primitivos(Tipo.INT64,t[1], t.lineno(1), find_column(input, t.slice[1]))

def p_exp_bool(t):
    '''expresion : TK_TRUE
                | TK_FALSE'''
    if t[1] == 'true':
        t[0] = Primitivos(Tipo.BOOLEANO, True, t.lineno(1), find_column(input, t.slice[1]))
    elif t[1] == 'false':
        t[0] = Primitivos(Tipo.BOOLEANO, False, t.lineno(1), find_column(input, t.slice[1]))

def p_exp_float(t):
    '''expresion : DECIMAL'''
    t[0] = Primitivos(Tipo.FLOAT64, t[1], t.lineno(1), find_column(input, t.slice[1]))

def p_exp_nothing(t):
    '''expresion : TK_NOTHING'''
    t[0] = Primitivos(Tipo.NOTHING, None, t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_identificador(t):
    '''expresion : ID'''
    t[0] = Identificador(t[1], t.lineno(1), find_column(input, t.slice[1]))

def p_primitivo_cadena(t):
    '''expresion : CADENA'''
    t[0] = Primitivos(Tipo.STRING,str(t[1]).replace('\\n', '\n'), t.lineno(1), find_column(input, t.slice[1]))

def p_primitivo_char(t):
    '''expresion : CHAR'''
    t[0] = Primitivos(Tipo.CHAR,str(t[1]).replace('\\n', '\n'), t.lineno(1), find_column(input, t.slice[1]))

################################################# CCREAR ARREGLOS ###################################################

def p_declarar_arreglo(t):
    'expresion : COROP params_call CORCLS'
    t[0] = Arreglo(Tipo.ARRAY, t[2], t.lineno(1), find_column(input, t.slice[1]))

################################################ ACCESO A ARREGLOS ################################################

def p_acceso_arreglo(t):
    '''expresion : ID posiciones_arreglo'''
    t[0] = Acceso_arreglo(t[1], t[2], t.lineno(1), find_column(input, t.slice[1]))

############################################## ACCESO ATRIBUTOS STRUCT ############################################
def p_ins_atrib_struct(t):
    'expresion : ID PTO ID'
    t[0] = Llamada_atributo_struct(t[1],t[3], t.lineno(1), find_column(input, t.slice[1]) )

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
        if isinstance(instr, Funcion):
            ast.addFuncion(instr)
        elif isinstance(instr,Plantilla_struct):
            ast.addPlantillaStruct(instr)
        else:
            valor = instr.interpretar(ast,TSGlobal)
            if isinstance(valor, Exception):
                ast.get_excepcion().append(valor)
                ast.actualizar_consola_salto(valor.__str__())

    return(ast.get_consola())