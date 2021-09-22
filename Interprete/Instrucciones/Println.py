from Interprete.Abstract.Instruccion import Instruccion
from Interprete.Abstract.NodoAst import NodoAst
from Interprete.TS.Tipo import *
from Interprete.TS.Exception import Exception
from Interprete.Expresiones.Primitivos import Primitivos

class Println(Instruccion):
    def __init__(self, expresion, fila, columna):
        self.expresion = expresion
        self.fila = fila
        self.columna = columna
    
    def interpretar(self, tree, tabla):
        ins = []
        for i in self.expresion:
            value = i.interpretar(tree, tabla)
            if type(value) == list:
                ins.append(self.obtenerString(value))
            else:
                ins.append(value)
        for i in ins:
            if isinstance(i, Exception):
                return i
        for i in  ins:
            tree.actualizar_consola_sin_salto(i)
        tree.actualizar_consola_salto("")
    
    def obtenerString(self, lista):
        var = "["
        for i in lista:
            if isinstance(i, Primitivos):
                var+=str(i.valor)+","
        var = var.rstrip(var[-1])
        var += "]"
        return var
    
    def getNodo(self):
        nodo = NodoAst("IMPRIMIR")
        nodo.agregarHijoNodo(self.expresion.getNodo())
        return nodo