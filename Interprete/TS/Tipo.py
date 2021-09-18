from enum import Enum

class Operador_Logico(Enum):
    AND = 1
    OR  = 2
    NOT = 3


class Operador_Aritmetico(Enum):
    SUMA            = 1
    RESTA           = 2
    MULTIPLICACION  = 3
    DIVISION        = 4
    POTENCIA        = 5
    MODULO          = 6
    UMENOS          = 7

class Tipo(Enum):
    NOTHING  = 1
    INT64    = 2
    FLOAT64  = 3
    BOOLEANO = 4
    CHAR     = 5
    STRING   = 6
    ARRAY    = 7
    STRUCT   = 8

class Operador_Relacional(Enum):
    MENQ        = 1
    MAYQ        = 2
    MENEQUALS   = 3
    MAYEQUALS   = 4
    IGUALDAD    = 5
    DIFERENCIA  = 6