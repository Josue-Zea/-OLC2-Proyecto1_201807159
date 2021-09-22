from Interprete.Expresiones.Identificador import Identificador
from Interprete.Instrucciones.Arreglo import Arreglo
from Interprete.TS.Exception import Exception
from Interprete.Abstract.NodoAst import NodoAst
from Interprete.Abstract.Instruccion import Instruccion
from Interprete.TS.Simbolo import Simbolo
from Interprete.Expresiones.Primitivos import Primitivos
from Interprete.TS.Tipo import *
from datetime import datetime

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
            return Exception("Semantico", "Arreglo "+str(self.identificador)+" no declarado", self.fila, self.columna, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        if len(posiciones)==1:
            if type(posiciones[0]) != int:
                return Exception("Semantico", "La posicion de un arreglo debe ser un dato INT64.", self.fila, self.columna, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            result = self.expresion.interpretar(tree, table)
            tipe = ""
            if type(result) == int:
                tipe = Tipo.INT64
            elif type(result) == float:
                tipe = Tipo.FLOAT64
            elif type(result) == bool:
                tipe = Tipo.BOOLEANO
            elif type(result) == str and len(result) == 1:
                tipe = Tipo.CHAR
            elif type(result) == str:
                tipe = Tipo.STRING
            variable = Primitivos(tipe, result, self.fila, self.columna)
            return arreglo.setVariable(posiciones[0],variable)
        else:
            result = self.expresion.interpretar(tree, table)
            return self.actualizarVariable(arreglo, posiciones, result)
    
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
                tipe = ""
                if type(result) == int:
                    tipe = Tipo.INT64
                elif type(result) == float:
                    tipe = Tipo.FLOAT64
                elif type(result) == bool:
                    tipe = Tipo.BOOLEANO
                elif type(result) == str and len(result) == 1:
                    tipe = Tipo.CHAR
                elif type(result) == str:
                    tipe = Tipo.STRING
                variable = Primitivos(tipe, valor, self.fila, self.columna)
                return arreglo.setVariable(posiciones[iterador], variable)
            if iterador > len(posiciones):
                return Exception("Semantico", "La posicion de un arreglo debe ser un dato INT64.", self.fila, self.columna, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return None