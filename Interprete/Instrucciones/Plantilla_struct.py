from Interprete.Abstract.Instruccion import Instruccion
from Interprete.Instrucciones.Struct import Struct
from Interprete.TS.Tipo import Tipo
from Interprete.TS.Exception import Exception

class Plantilla_struct(Instruccion):
    def __init__(self, tipo, nombre, parametros, fila, columna):
        self.tipo = tipo
        self.nombre = nombre
        self.parametros = parametros
        self.fila = fila
        self.columna = columna
    
    def interpretar(self, nombre_struct, params, fila, columna, tree, table):
        if len(self.parametros) != len(params): # Validamos la cantidad de parametros que se envía
            return Exception("Semantico", "La cantidad de parametros no coincide al crear el struct", self.fila, self.columna)
        contador=0
        temp = Struct(self.tipo, str(nombre_struct), fila, columna)
        for expresion in params: # SE OBTIENE EL VALOR DEL PARAMETRO EN LA LLAMADA
            resultExpresion = expresion.interpretar(tree, table)
            if isinstance(resultExpresion, Exception): return resultExpresion
            if self.parametros[contador]["tipoDato"] == any:  # VERIFICACION DE TIPO
                temp.agregarVariable({"tipoDato":any, "identificador":str(self.parametros[contador]['identificador']),"valor":resultExpresion})
            elif self.parametros[contador]["tipoDato"] == expresion.tipo:
                temp.agregarVariable({"tipoDato":expresion.tipo, "identificador":str(self.parametros[contador]['identificador']),"valor":resultExpresion})
            else:
                return Exception("Semantico", "Tipo de dato diferente en Parametros de la llamada.", self.fila, self.columna)
            contador += 1
        return temp