from Interprete.TS.Tipo import *
from Interprete.TS.Exception import Exception
from datetime import datetime

class Arreglo():
    def __init__(self, tipo, variables, fila, columna):
        self.tipo = tipo
        self.identificador = None
        self.variables = variables
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        for variable in self.variables:
            variable = variable.interpretar(tree,table)
            if isinstance(variable,Exception): return variable
        result = tree.addArreglo(self)
        return None

    def getVariable(self, posicion):
        if posicion <0 or posicion+1 > len(self.variables):
            return None
        else:
            return self.variables[posicion]
    
    def setVariable(self, posicion, valor):
        if posicion < 0 or posicion+1 > len(self.variables):
            return Exception("Semantico", "Posicion en el areglo fuera de los limites.", self.fila, self.columna, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        else:
            self.variables[posicion] = valor
            return None
    
    def getVariables(self):
        return self.variables

    def setIdentificador(self, identificador):
        self.identificador = identificador

    def getIdentificador(self):
        return self.identificador
    
    def get_fila(self):
        return self.fila

    def get_columna(self):
        return self.columna
    
    def __str__(self):
        cadena = "["
        for i in self.variables:
            cadena+=str(i.valor)+","
        cadena+="]"
        return cadena