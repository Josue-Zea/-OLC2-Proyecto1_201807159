from Interprete.TS.Exception import Exception
from Interprete.Abstract.Instruccion import Instruccion
from datetime import datetime


class Identificador(Instruccion):
    def __init__(self, identificador, fila, columna):
        self.identificador = identificador
        self.fila = fila
        self.columna = columna
        self.tipo = None

    def interpretar(self, tree, table):
        simbolo = table.getTabla(self.identificador)
        if simbolo == None:
            simbolo = tree.getArreglo(self.identificador)
            if simbolo == None:
                return Exception("Semantico", "No se encontro la variable "+self.identificador+" declarada", self.fila, self.columna, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            else:
             self.tipo = simbolo.tipo
             return simbolo.getVariables()
        else:
            self.tipo = simbolo.get_tipo()
            return simbolo.get_valor()