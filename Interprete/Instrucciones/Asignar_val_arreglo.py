from Interprete.Expresiones.Identificador import Identificador
from Interprete.Instrucciones.Arreglo import Arreglo
from Interprete.TS.Exception import Exception
from Interprete.Abstract.Instruccion import Instruccion
from Interprete.TS.Simbolo import Simbolo
from Interprete.TS.Tipo import *

class Asignar_val_arreglo():
    def __init__(self, identificador, posicion, expresion, fila, columna):
        self.identificador = identificador
        self.posicion = posicion
        self.expresion = expresion
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        arreglo = tree.getArreglo(str(self.identificador))
        posiciones =self.arreglarPosiciones(self.posicion, tree, table)
        if arreglo == None:
            return Exception("Semantico", "Arreglo "+str(self.identificador)+" no declarado", self.fila, self.columna)
        if len(posiciones)==1:
            if type(posiciones[0]) != int:
                return Exception("Semantico", "La posicion de un arreglo debe ser un dato INT64.", self.fila, self.columna)
            return arreglo.setVariable(posiciones[0],self.expresion)
        else:
            return self.actualizarVariable(arreglo, posiciones, self.expresion)
    
    def arreglarPosiciones(self, posiciones, tree, table):
        var = []
        if len(posiciones) == 1:
            var.append(posiciones[0].interpretar(tree, table))
        else:
            var.append(posiciones[0].interpretar(tree, table))
            res = self.arreglarPosiciones(posiciones[1],tree, table)
            for d in res:
                var.append(d)
        return var
    
    def actualizarVariable(self, arreglo, posiciones, valor):
        iterador = 0
        while True:
            aux = arreglo.getVariable(posiciones[iterador])
            if isinstance(aux, Arreglo):
                iterador+=1
                arreglo = aux
            else:
                return arreglo.setVariable(posiciones[iterador], valor)
            if iterador > len(posiciones):
                return Exception("Semantico", "La posicion de un arreglo debe ser un dato INT64.", self.fila, self.columna)
        return None