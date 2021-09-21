
from Interprete.TS.Exception import Exception
from Interprete.TS.Tipo import *

class TablaSimbolos:
    def __init__(self, anterior = None):
        self.tabla = {}
        self.anterior = anterior
        self.funciones = []

    def setTabla(self, simbolo):# Para agregar un simbolo a la tabla
        if simbolo.id in self.tabla : # Si el simbolo ya existe retorna una exception
            return Exception("Semantico", "Variable " + simbolo.id + " ya existe", simbolo.fila, simbolo.columna)
        else: # Se agrega un nuevo simbolo
            self.tabla[simbolo.id] = simbolo
            return None

    def getTabla(self, id):# Esta funcion se encarga de buscar el simbolo en el diccionario.
        tablaActual = self # Se posiciona en la cabeza.
        while tablaActual.tabla != None: # revisa si esta vacio y si no... entra al while.
            if id in tablaActual.tabla : # verifica si id se encuentra en la tabla, si lo encuentra retorna el id.
                return tablaActual.tabla[id]
            else:
                tablaActual = tablaActual.anterior #  si no encuentra el id, regresa al entorno anterior.
                if tablaActual is None: # Si se llega al null es el entorno global entonces sale
                    return None
        return None

    def actualizarTabla(self, simbolo): # Esta funcion se encarga de actualizar el valor del simbolo.
        tablaActual = self # Se posiciona en la cabeza.
        while tablaActual != None:
            if simbolo.id in tablaActual.tabla : # Si el simbolo lo encuentra lo va actualizar con sus sets.
                if tablaActual.tabla[simbolo.id].get_tipo() == simbolo.get_tipo(): # aca si son del mismo tiempo lo cambia.
                    tablaActual.tabla[simbolo.id].set_valor(simbolo.get_valor())
                    tablaActual.tabla[simbolo.id].set_tipo(simbolo.get_tipo())
                    return None
                else:
                    tablaActual.tabla[simbolo.id].set_tipo(simbolo.get_tipo())
                    tablaActual.tabla[simbolo.id].set_valor(simbolo.get_valor())
                    tablaActual.tabla[simbolo.id].set_tipo(simbolo.get_tipo())
                    return None
            else:
                tablaActual = tablaActual.anterior #si no encuentra el id, regresa al entorno anterior.
                if tablaActual is None: # Condicion imprtante por si el anterior es null y no truene.
                    return None
        return Exception("Semantico", "Variable No encontrada en Asignacion", simbolo.get_fila(), simbolo.get_columna())
        
        
    