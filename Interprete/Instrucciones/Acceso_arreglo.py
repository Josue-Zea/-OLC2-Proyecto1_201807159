from Interprete.Expresiones.Identificador import Identificador
from Interprete.Expresiones.Logicas import Logica
from Interprete.Expresiones.Relacionales import Relacional
from Interprete.Expresiones.Aritmetica import Aritmetica
from Interprete.Instrucciones.Arreglo import Arreglo
from Interprete.TS.Exception import Exception
from Interprete.Abstract.Instruccion import Instruccion
from Interprete.TS.Simbolo import Simbolo
from Interprete.TS.Tipo import *
from datetime import datetime
from Interprete.Abstract.NodoAst import NodoAst

class Acceso_arreglo():
    def __init__(self, identificador, expresion, fila, columna):
        self.identificador = identificador
        self.expresion = expresion
        self.fila = fila
        self.columna = columna
        self.tipo = None
    
    def interpretar(self, tree, table):
        arreglo = tree.getArreglo(str(self.identificador))
        if arreglo == None:
            return Exception("Semantico", "Arreglo "+str(self.identificador)+" no declarado", self.fila, self.columna, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        posiciones = self.arreglarPosiciones(self.expresion, tree, table)
        if len(posiciones) == 1:
            if type(posiciones[0]) != int:
                return Exception("Semantico", "La posicion de un arreglo debe ser un dato INT64.", self.fila, self.columna, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            valor = arreglo.getVariable(posiciones[0])
        else:
            valor = self.obtenerVariable(arreglo, posiciones)
        if valor == None:
            return Exception("Semantico", "Posicion en el arreglo no valida.", self.fila, self.columna, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        if isinstance(valor, Aritmetica):
            valor = valor.interpretar(tree, table)
            if type(valor) == int:
                self.tipo = Tipo.INT64
            elif type(valor) == float:
                self.tipo = Tipo.FLOAT64
            elif type(valor) == bool:
                self.tipo = Tipo.BOOLEANO
            elif type(valor) == str and len(valor) == 1:
                self.tipo = Tipo.CHAR
            elif type(valor) == str:
                self.tipo = Tipo.STRING
            return valor
        elif isinstance(valor, Logica):
            valor = valor.interpretar(tree, table)
            if type(valor) == int:
                self.tipo = Tipo.INT64
            elif type(valor) == float:
                self.tipo = Tipo.FLOAT64
            elif type(valor) == bool:
                self.tipo = Tipo.BOOLEANO
            elif type(valor) == str and len(valor) == 1:
                self.tipo = Tipo.CHAR
            elif type(valor) == str:
                self.tipo = Tipo.STRING
            return valor
        elif isinstance(valor, Relacional):
            valor = valor.interpretar(tree, table)
            if type(valor) == int:
                self.tipo = Tipo.INT64
            elif type(valor) == float:
                self.tipo = Tipo.FLOAT64
            elif type(valor) == bool:
                self.tipo = Tipo.BOOLEANO
            elif type(valor) == str and len(valor) == 1:
                self.tipo = Tipo.CHAR
            elif type(valor) == str:
                self.tipo = Tipo.STRING
            return valor
        self.tipo = valor.tipo
        return valor.valor

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
    
    def obtenerVariable(self, arreglo, posiciones):
        for posicion in posiciones:
            valor = arreglo.getVariable(posicion)
            if isinstance(valor,Arreglo):
                arreglo = valor
            if valor == None:
                return None
        return valor

    def getNodo(self):
        nodo = NodoAst("ASIGNAR VALOR ARREGLO")
        nodo.agregarHijo(str(self.identificador))
        return nodo