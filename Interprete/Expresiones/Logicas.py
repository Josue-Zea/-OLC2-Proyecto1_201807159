from Interprete.Abstract.Instruccion import Instruccion
from Interprete.TS.Exception import Exception
from Interprete.TS.Tipo import Tipo, Operador_Logico

class Logica(Instruccion):
    def __init__(self, operador, OperacionIzq, OperacionDer, fila, columna):
        self.operador = operador
        self.OperacionIzq = OperacionIzq
        self.OperacionDer = OperacionDer
        self.fila = fila
        self.columna = columna
        self.tipo = Tipo.BOOLEANO

    def interpretar(self, tree, table):
        izq = self.OperacionIzq.interpretar(tree, table)
        if isinstance(izq, Exception): return izq
        if self.OperacionDer != None:
            der = self.OperacionDer.interpretar(tree, table)
            if isinstance(der, Exception): return der

        if self.operador == Operador_Logico.OR:
            if self.OperacionIzq.tipo == Tipo.BOOLEANO and self.OperacionDer.tipo == Tipo.BOOLEANO:
                return self.returnVal(self.OperacionIzq.tipo, izq) or self.returnVal(self.OperacionDer.tipo, der)
            return Exception("Semantico", "Tipo Erroneo de operacion para ||.", self.fila, self.columna)
        elif self.operador == Operador_Logico.AND:
            if self.OperacionIzq.tipo == Tipo.BOOLEANO and self.OperacionDer.tipo == Tipo.BOOLEANO:
                return self.returnVal(self.OperacionIzq.tipo, izq) and self.returnVal(self.OperacionDer.tipo, der)
            return Exception("Semantico", "Tipo Erroneo de operacion para &&.", self.fila, self.columna)
        elif self.operador == Operador_Logico.NOT:
            if self.OperacionIzq.tipo == Tipo.BOOLEANO:
                return not self.returnVal(self.OperacionIzq.tipo, izq)
            return Exception("Semantico", "Tipo Erroneo de operacion para !.", self.fila, self.columna)
        return Exception("Semantico", "Tipo de Operacion no Especificado.", self.fila, self.columna)

    def returnVal(self, tipo, val):
        if tipo == Tipo.INT64:
            return int(val)
        elif tipo == Tipo.FLOAT64:
            return float(val)
        elif tipo == Tipo.BOOLEANO:
            return bool(val)
        return str(val)