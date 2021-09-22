from Interprete.Abstract.Instruccion import Instruccion
from Interprete.Abstract.NodoAst import NodoAst
from Interprete.TS.Exception import Exception
from Interprete.TS.Tipo import Tipo
from Interprete.TS.TablaSimbolos import TablaSimbolos

class Return(Instruccion):
    def __init__(self, expresion, fila, columna):
        self.expresion = expresion
        self.fila = fila
        self.columna = columna
        self.tipo = None
        self.result = None

    def interpretar(self, tree, table):
        result = self.expresion.interpretar(tree, table)
        if isinstance(result, Exception): return result
        self.tipo = self.expresion.tipo
        self.result = result
        return self

    def getNodo(self):
        nodo = NodoAst("RETURN")
        nodo.agregarHijoNodo(self.expresion.getNodo())
        return nodo