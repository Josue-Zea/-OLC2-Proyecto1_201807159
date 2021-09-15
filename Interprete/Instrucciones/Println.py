from Interprete.Abstract.Instruccion import Instruccion
from Interprete.TS.Tipo import *
from Interprete.TS.Exception import Exception

class Println(Instruccion):
    def __init__(self, expresion, fila, columna):
        self.expresion = expresion
        self.fila = fila
        self.columna = columna
    
    def interpretar(self, tree, tabla):
        ins = []
        for i in self.expresion:
            value = i.interpretar(tree, tabla)
            ins.append(value)
        for i in ins:
            if isinstance(i, Exception):
                return i
        for i in  ins:
            tree.actualizar_consola_sin_salto(i)
        tree.actualizar_consola_salto("")

        """        for i in self.expresion: Codigo anterior
            value = i.interpretar(tree, tabla)
            if isinstance(value, Exception):
                return value
            tree.actualizar_consola_sin_salto(value)
        tree.actualizar_consola_salto("")"""