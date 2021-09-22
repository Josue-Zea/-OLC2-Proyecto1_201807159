from Interprete.Expresiones.Identificador import Identificador
from Interprete.TS.Exception import Exception
from Interprete.Abstract.Instruccion import Instruccion
from Interprete.TS.Simbolo import Simbolo
from Interprete.TS.Tipo import *
from Interprete.Abstract.NodoAst import NodoAst
from datetime import datetime


class Asignar_valor_var_struct(Instruccion):
    def __init__(self, nombre_struct, nombre_atributo, expresion, fila, columna):
        self.nombre_struct = nombre_struct
        self.nombre_atributo = nombre_atributo
        self.expresion = expresion
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        expresion = self.expresion.interpretar(tree, table)
        if isinstance(expresion,Exception): return expresion
        struct = tree.getStruct(str(self.nombre_struct))                        # OBTENER EL STRUCT
        if struct == None:
            return Exception("Semantico", "El struct: "+str(self.nombre_struct)+" no se encuentra declarado", self.fila, self.columna, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        if struct.valor.tipo == 0:
            return Exception("Semantico", "El struct: "+str(self.nombre_struct)+" es inmutable", self.fila, self.columna, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        atributo = struct.valor.getVariable(str(self.nombre_atributo))
        if atributo == None:
            return Exception("Semantico", "El struct: "+str(self.nombre_struct)+" no contiene un atributo: "+str(self.nombre_atributo), self.fila, self.columna, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        if atributo["tipoDato"] == any:
            atributo["valor"] = expresion
        else:
            tipe = ""
            if type(expresion) == int:
                tipe = Tipo.INT64
            elif type(expresion) == float:
                tipe = Tipo.FLOAT64
            elif type(expresion) == bool:
                tipe = Tipo.BOOLEANO
            elif type(expresion) == str and len(expresion) == 1:
                tipe = Tipo.CHAR
            elif type(expresion) == str:
                tipe = Tipo.STRING
            if atributo["tipoDato"] == tipe:
                atributo["valor"] = expresion
            else:
                return Exception("Semantico", "El atributo enviado al struct no es del tipo adecuado", self.fila, self.columna, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return None