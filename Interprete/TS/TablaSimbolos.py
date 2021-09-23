
from Interprete.TS.Exception import Exception
from Interprete.TS.Tipo import *
from datetime import datetime

class TablaSimbolos:
    def __init__(self, anterior = None):
        self.tabla = {}
        self.anterior = anterior
        self.funciones = []

    def setTabla(self, simbolo)
        if simbolo.id in self.tabla :
            return Exception("Semantico", "Variable " + simbolo.id + " ya existe", simbolo.fila, simbolo.columna, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        else:
            self.tabla[simbolo.id] = simbolo
            return None

    def getTabla(self, id):
        tablaActual = self
        while tablaActual.tabla != None:
            if id in tablaActual.tabla :
                return tablaActual.tabla[id]
            else:
                tablaActual = tablaActual.anterior 
                if tablaActual is None: 
                    return None
        return None

    def actualizarTabla(self, simbolo):
        tablaActual = self
        while tablaActual != None:
            if simbolo.id in tablaActual.tabla :
                if tablaActual.tabla[simbolo.id].get_tipo() == simbolo.get_tipo():
                    tablaActual.tabla[simbolo.id].set_valor(simbolo.get_valor())
                    tablaActual.tabla[simbolo.id].set_tipo(simbolo.get_tipo())
                    return None
                else:
                    tablaActual.tabla[simbolo.id].set_tipo(simbolo.get_tipo())
                    tablaActual.tabla[simbolo.id].set_valor(simbolo.get_valor())
                    tablaActual.tabla[simbolo.id].set_tipo(simbolo.get_tipo())
                    return None
            else:
                tablaActual = tablaActual.anterior
                if tablaActual is None:
                    return None
        return Exception("Semantico", "Variable No encontrada en Asignacion", simbolo.get_fila(), simbolo.get_columna(), datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        
    
