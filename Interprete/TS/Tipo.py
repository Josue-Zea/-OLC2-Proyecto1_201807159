from enum import Enum

class Tipo(Enum):
    NULO     = 1
    INT64    = 2
    FLOAT64  = 3
    BOOLEANO = 4
    CHAR     = 5
    STRING   = 6
    ARREGLO  = 7
    STRUCT   = 8

class Operador_Aritmetico(Enum):
    SUMA            = 1
    RESTA           = 2
    MULTIPLICACION  = 3
    DIVISION        = 4
    POTENCIA        = 5
    MODULO          = 6
    UMENOS          = 7