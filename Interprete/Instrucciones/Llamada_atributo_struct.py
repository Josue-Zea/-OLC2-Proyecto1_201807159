from Interprete.Expresiones.Identificador import Identificador
from Interprete.Instrucciones.Struct import Struct
from Interprete.Abstract.NodoAst import NodoAst
from Interprete.TS.Exception import Exception
from Interprete.Abstract.Instruccion import Instruccion
from Interprete.TS.Simbolo import Simbolo
from Interprete.TS.Tipo import *
from datetime import datetime

class Llamada_atributo_struct(Instruccion):
    def __init__(self, nombre_struct, atributos, fila, columna):
        self.nombre_struct = nombre_struct
        self.atributos = atributos
        self.fila = fila
        self.columna = columna
        self.tipo = None

    def interpretar(self, tree, table):
        struct = table.getTabla(str(self.nombre_struct))                   # OBTENER EL STRUCT
        struct = struct.get_valor()
        if struct == None:
            return Exception("Semantico", "El struct: "+str(self.nombre_struct)+" no se encuentra declarado", self.fila, self.columna, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        atributo = ""
        for i in self.atributos:
            struct = struct.getVariable(str(i))
            if isinstance(struct["valor"], Struct):
                struct = struct["valor"]
            else:
                atributo = struct
        if atributo == None:
            return Exception("Semantico", "El struct: "+str(self.nombre_struct)+" no contiene un atributo: "+str(i), self.fila, self.columna, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
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
            elif isinstance(valor, Struct):
                self.tipo = Tipo.STRUCT
        else:
            self.tipo = atributo["tipoDato"]
        return valor

    def getNodo(self):
        nodo = NodoAst("LLAMADA ATRIBUTO")
        nodo.agregarHijo(str(self.nombre_struct))
        atributos = NodoAst("ATRIBUTOS")
        for atributo in self.atributos:
            atributos.agregarHijo(str(atributo))
        nodo.agregarHijoNodo(atributos)
        return nodo