from Interprete.Abstract.Instruccion import Instruccion
from Interprete.TS.Exception import Exception

class Print(Instruccion):

    def __init__(self, expresion, fila, columna):
        self.expresion = expresion
        self.fila = fila
        self.columna = columna
    
    def interpretar(self, tree, tabla):
        value = self.expresion.interpretar(tree, tabla)

        if isinstance(value, Exception):
            return value

        tree.actualizar_consola_sin_salto(value)