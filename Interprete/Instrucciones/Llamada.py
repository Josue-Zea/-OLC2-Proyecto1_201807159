from Interprete.Abstract.Instruccion import Instruccion
from Interprete.Abstract.NodoAst import NodoAst
from Interprete.TS.Exception import Exception
from Interprete.TS.TablaSimbolos import TablaSimbolos
from Interprete.Instrucciones.Break import Break
from Interprete.Instrucciones.Struct import Struct
from Interprete.Instrucciones.Plantilla_struct import Plantilla_struct
from Interprete.TS.Simbolo import Simbolo
from Interprete.TS.Tipo import *
from Interprete.Instrucciones.Funcion import Funcion
from datetime import datetime

class Llamada(Instruccion):
    def __init__(self, nombre, parametros, fila, columna):
        self.nombre = nombre
        self.parametros = parametros
        self.fila = fila
        self.columna = columna
        self.tipo = None
    
    def interpretar(self, tree, table):
        tree.setAmbito(str(self.nombre))
        result = tree.getFuncion(self.nombre)       # Buscamos la funcion entre la pila que contiene el tree
        if result == None:
            result = tree.getPlantillaStruct(self.nombre)
            if result == None:
                tree.removeAmbito()
                return Exception("Semantico", "No existe una funcionn con ese nombre: " + self.nombre, self.fila, self.columna, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        if isinstance(result, Plantilla_struct):
            return self.crearStruct(result, tree, table)
        nuevaTabla = TablaSimbolos(tree.get_tabla_ts_global())
        if len(result.parametros) == len(self.parametros): #LA CANTIDAD DE PARAMETROS ES LA ADECUADA
            contador=0
            for expresion in self.parametros: # SE OBTIENE EL VALOR DEL PARAMETRO EN LA LLAMADA
                resultExpresion = expresion.interpretar(tree, table)
                if isinstance(resultExpresion, Exception): 
                    tree.removeAmbito()
                    return resultExpresion
                if isinstance(resultExpresion, Simbolo):
                    if isinstance(resultExpresion.valor, Struct):
                        simbolo = Simbolo(str(result.parametros[contador]['identificador']), Tipo.STRUCT, self.fila, self.columna, resultExpresion.get_valor(), tree.getAmbito())
                elif result.parametros[contador]["tipoDato"] == expresion.tipo or result.parametros[contador]["tipoDato"] == any:  # VERIFICACION DE TIPO 
                    tipe = ""
                    if type(resultExpresion) == int:
                        tipe = Tipo.INT64
                    elif type(resultExpresion) == float:
                        tipe = Tipo.FLOAT64
                    elif type(resultExpresion) == bool:
                        tipe = Tipo.BOOLEANO
                    elif type(resultExpresion) == str and len(resultExpresion) == 1:
                        tipe = Tipo.CHAR
                    elif type(resultExpresion) == str:
                        tipe = Tipo.STRING
                    simbolo = Simbolo(str(result.parametros[contador]['identificador']), tipe, self.fila, self.columna, resultExpresion, tree.getAmbito())
                    tree.agregarVariable([str(result.parametros[contador]['identificador']), tipe, tree.getAmbito(), str(self.fila),str(self.columna)])
                    resultTabla = nuevaTabla.setTabla(simbolo)
                    if isinstance(resultTabla, Exception):
                        tree.removeAmbito()
                        return resultTabla
                else:
                    tree.removeAmbito()
                    return Exception("Semantico", "Tipo de dato diferente en Parametros de la llamada.", self.fila, self.columna, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                contador += 1
        else: 
            tree.removeAmbito()
            return Exception("Semantico", "El numero de parametros enviado no coincide con los que recibe la funcion.", self.fila, self.columna, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        value = result.interpretar(tree, nuevaTabla)         # INTERPRETAR EL NODO FUNCION
        if isinstance(value, Exception):
            tree.removeAmbito()
            return value
        self.tipo = result.tipo
        tree.removeAmbito()
        return value

    def getNodo(self):
        nodo = NodoAst("LLAMADA A FUNCION")
        nodo.agregarHijo(str(self.nombre))
        parametros = NodoAst("PARAMETROS")
        for param in self.parametros:
            parametros.agregarHijoNodo(param.getNodo())
        nodo.agregarHijoNodo(parametros)
        return nodo
    
    def crearStruct(self, plantilla, tree, table):
        temp = plantilla.interpretar(None, self.parametros, self.fila, self.columna, tree, table)
        if isinstance(temp,Exception): return temp
        #simbolo = Simbolo(temp, Tipo.STRUCT, self.fila, self.columna, temp, tree.getAmbito())
        self.tipo = Tipo.STRUCT
        return temp