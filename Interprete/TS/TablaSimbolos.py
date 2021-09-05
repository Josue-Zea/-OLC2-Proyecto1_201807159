
from Interprete.TS.Exception import Exception
from Interprete.TS.Tipo import *

class TablaSimbolos:
    def __init__(self, anterior = None):
        self.tabla = {} # Empty Dictionary 
        self.anterior = anterior
        self.funciones = []

    def setTabla(self, simbolo):# Esta funcion se encarga de agregar un simbolo a la tabla de simbolo.
        if simbolo.id.lower() in self.tabla : # Busca si en la tabla de simbolo existe el nombre, si lo encuentra retorna una Exception.
            return Exception("Semantico", "Variable " + simbolo.id + " ya existe", simbolo.fila, simbolo.columna)
        else:
            self.tabla[simbolo.id.lower()] = simbolo # Si no existe el id, lo agrega al diccionario
            return None

    def getTabla(self, id):# Esta funcion se encarga de buscar el simbolo en la el diccionario.
        tablaActual = self # Se posiciona en la cabeza.
        while tablaActual.tabla != None: # revisa si esta vacio y si no... entra al while.
            if id.lower() in tablaActual.tabla : # verifica si id se encuentra en la tabla, si lo encuentra retorna el id.
                return tablaActual.tabla[id.lower()]
            else:
                tablaActual = tablaActual.anterior #  si no encuentra el id, regresa al entorno anterior.
                if tablaActual is None: # Condicion imprtante por si el anterior es null y no truene.
                    return None
        return None

    def actualizarTabla(self, simbolo): # Esta funcion se encarga de actualizar el valor del simbolo.
        tablaActual = self # Se posiciona en la cabeza.
        
        while tablaActual != None: # revisa si esta vacio y si no... entra el while.
            if simbolo.id in tablaActual.tabla : # Si el simbolo lo encuentra lo va actualizar con sus sets.
                if tablaActual.tabla[simbolo.id.lower()].get_tipo() == simbolo.get_tipo(): # aca si son del mismo tiempo lo cambia.
                    tablaActual.tabla[simbolo.id.lower()].set_valor(simbolo.get_valor())
                    tablaActual.tabla[simbolo.id.lower()].set_tipo(simbolo.get_tipo())
                    return None
                return Exception("Semantico", "Tipo de dato Diferente en Asignacion", simbolo.get_fila(), simbolo.get_columna()) # si no encontro el dato en el diccionario retorna una excepcion.
            else:
                tablaActual = tablaActual.anterior #si no encuentra el id, regresa al entorno anterior.
                if tablaActual is None: # Condicion imprtante por si el anterior es null y no truene.
                    return None
        return Exception("Semantico", "Variable No encontrada en Asignacion", simbolo.get_fila(), simbolo.get_columna())
        
        
    