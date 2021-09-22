from Interprete.Expresiones.Identificador import Identificador
from Interprete.Abstract.NodoAst import NodoAst
from Interprete.TS.Exception import Exception
from Interprete.Abstract.Instruccion import Instruccion
from Interprete.TS.Simbolo import Simbolo
from Interprete.TS.Tipo import *
from datetime import datetime


class Llamada_atributo_struct(Instruccion):
    def __init__(self, nombre_struct, nombre_atributo, fila, columna):
        self.nombre_struct = nombre_struct
        self.nombre_atributo = nombre_atributo
        self.fila = fila
        self.columna = columna
        self.tipo = None

    def interpretar(self, tree, table):
        struct = tree.getStruct(str(self.nombre_struct))                   # OBTENER EL STRUCT
        if struct == None:
            return Exception("Semantico", "El struct: "+str(self.nombre_struct)+" no se encuentra declarado", self.fila, self.columna, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        atributo = struct.valor.getVariable(str(self.nombre_atributo))
        if atributo == None:
            return Exception("Semantico", "El struct: "+str(self.nombre_struct)+" no contiene un atributo: "+str(self.nombre_atributo), self.fila, self.columna, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        valor = atributo["valor"]
        if atributo["tipoDato"] == any:
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
        else:
            self.tipo = atributo["tipoDato"]
        return valor