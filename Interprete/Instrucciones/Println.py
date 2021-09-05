from Interprete.Abstract.Instruccion import Instruccion
from Interprete.TS.Tipo import *
from Interprete.TS.Exception import Exception

class Println(Instruccion):
    
    def __init__(self, expresion, fila, columna):
        self.expresion = expresion
        self.fila = fila
        self.columna = columna
    
    def interpretar(self, tree, tabla):
        value = self.expresion.interpretar(tree, tabla)

        if isinstance(value, Exception):
            return value

        tree.actualizar_consola_salto(value)