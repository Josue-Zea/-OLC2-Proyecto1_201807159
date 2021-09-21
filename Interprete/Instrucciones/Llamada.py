from Interprete.Abstract.Instruccion import Instruccion
from Interprete.TS.Exception import Exception
from Interprete.TS.TablaSimbolos import TablaSimbolos
from Interprete.Instrucciones.Break import Break
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
    
    def interpretar(self, tree, table):
        result = tree.getFuncion(self.nombre)       # Buscamos la funcion entre la pila que contiene el tree
        if result == None:
            return Exception("Semantico", "No existe una funcionn con ese nombre: " + self.nombre, self.fila, self.columna, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        nuevaTabla = TablaSimbolos(tree.get_tabla_ts_global())
        if len(result.parametros) == len(self.parametros): #LA CANTIDAD DE PARAMETROS ES LA ADECUADA
            contador=0
            for expresion in self.parametros: # SE OBTIENE EL VALOR DEL PARAMETRO EN LA LLAMADA
                resultExpresion = expresion.interpretar(tree, table)
                if isinstance(resultExpresion, Exception): return resultExpresion
                
                if result.parametros[contador]["tipoDato"] == expresion.tipo or result.parametros[contador]["tipoDato"] == any:  # VERIFICACION DE TIPO 
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
                    # CREACION DE SIMBOLO E INGRESARLO A LA TABLA DE SIMBOLOS
                    simbolo = Simbolo(str(result.parametros[contador]['identificador']), tipe, self.fila, self.columna, resultExpresion)
                    resultTabla = nuevaTabla.setTabla(simbolo)
                    if isinstance(resultTabla, Exception): return resultTabla
                    
                else:
                    return Exception("Semantico", "Tipo de dato diferente en Parametros de la llamada.", self.fila, self.columna, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                contador += 1
        else: 
            return Exception("Semantico", "El numero de parametros enviado no coincide con los que recibe la funcion.", self.fila, self.columna, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
        value = result.interpretar(tree, nuevaTabla)         # INTERPRETAR EL NODO FUNCION
        if isinstance(value, Exception): return value
        self.tipo = result.tipo
        
        return value