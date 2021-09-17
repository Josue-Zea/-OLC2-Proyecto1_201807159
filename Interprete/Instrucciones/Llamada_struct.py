from Interprete.Abstract.Instruccion import Instruccion
from Interprete.TS.Exception import Exception
from Interprete.TS.TablaSimbolos import TablaSimbolos
from Interprete.TS.Simbolo import Simbolo
from Interprete.TS.Tipo import *
from Interprete.Instrucciones.Funcion import Funcion

class Llamada_struct(Instruccion):
    def __init__(self, identificador, nombre_struct, parametros, fila, columna):
        self.identificador = identificador
        self.nombre_struct = nombre_struct
        self.parametros = parametros
        self.fila = fila
        self.columna = columna
    
    def interpretar(self, tree, table):
        result = tree.getPlantillaStruct(self.nombre_struct)                    # Obtener la plantilla de struct
        if result == None:                                                      # No se encontró la plantilla de struct
            return Exception("Semantico", "No existe un struct declarado con ese nombre: " + self.nombre, self.fila, self.columna)
        temp = result.interpretar(str(self.nombre_struct),self.parametros, self.fila, self.columna, tree, table)
        if isinstance(temp,Exception): return temp
        simbolo = Simbolo(str(self.identificador),Tipo.STRUCT, self.fila, self.columna, temp)
        var = tree.addStruct(simbolo)
        if isinstance(var, Exception): return var
        return None