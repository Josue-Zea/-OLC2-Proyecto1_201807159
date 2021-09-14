from Interprete.Abstract.Instruccion import Instruccion
from Interprete.TS.Exception import Exception
from Interprete.TS.Tipo import Tipo, Operador_Relacional

class Relacional(Instruccion):

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
        der = self.OperacionDer.interpretar(tree, table)
        if isinstance(der, Exception): return der
        
        if self.operador == Operador_Relacional.IGUALDAD:
            # INT64
            if self.OperacionIzq.tipo == Tipo.INT64 and self.OperacionDer.tipo == Tipo.INT64:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) == self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == Tipo.INT64 and self.OperacionDer.tipo == Tipo.FLOAT64:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) == self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == Tipo.INT64 and self.OperacionDer.tipo == Tipo.STRING:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) == self.obtenerVal(self.OperacionDer.tipo, der)
            # FLOAT64
            elif self.OperacionIzq.tipo == Tipo.FLOAT64 and self.OperacionDer.tipo == Tipo.INT64:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) == self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == Tipo.FLOAT64 and self.OperacionDer.tipo == Tipo.FLOAT64:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) == self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == Tipo.FLOAT64 and self.OperacionDer.tipo == Tipo.STRING:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) == self.obtenerVal(self.OperacionDer.tipo, der)
            # BOOLEAN
            elif self.OperacionIzq.tipo == Tipo.BOOLEANO and self.OperacionDer.tipo == Tipo.BOOLEANO:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) == self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == Tipo.BOOLEANO and self.OperacionDer.tipo == Tipo.STRING:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) == self.obtenerVal(self.OperacionDer.tipo, der)
            # CHAR
            elif self.OperacionIzq.tipo == Tipo.CHAR and self.OperacionDer.tipo == Tipo.CHAR:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) == self.obtenerVal(self.OperacionDer.tipo, der)
            # STRING
            elif self.OperacionIzq.tipo == Tipo.STRING and self.OperacionDer.tipo == Tipo.INT64:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) == self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == Tipo.STRING and self.OperacionDer.tipo == Tipo.FLOAT64:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) == self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == Tipo.STRING and self.OperacionDer.tipo == Tipo.BOOLEANO:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) == self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == Tipo.STRING and self.OperacionDer.tipo == Tipo.STRING:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) == self.obtenerVal(self.OperacionDer.tipo, der)
            return Exception("Semantico", "Tipo Erroneo de operacion para ==.", self.fila, self.columna)

        elif self.operador == Operador_Relacional.DIFERENCIA:
            # INT
            if self.OperacionIzq.tipo == Tipo.INT64 and self.OperacionDer.tipo == Tipo.INT64:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) != self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == Tipo.INT64 and self.OperacionDer.tipo == Tipo.FLOAT64:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) != self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == Tipo.INT64 and self.OperacionDer.tipo == Tipo.STRING:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) != self.obtenerVal(self.OperacionDer.tipo, der)
            # DOUBLE
            elif self.OperacionIzq.tipo == Tipo.FLOAT64 and self.OperacionDer.tipo == Tipo.INT64:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) != self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == Tipo.FLOAT64 and self.OperacionDer.tipo == Tipo.FLOAT64:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) != self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == Tipo.FLOAT64 and self.OperacionDer.tipo == Tipo.STRING:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) != self.obtenerVal(self.OperacionDer.tipo, der)
            # BOOLEAN
            elif self.OperacionIzq.tipo == Tipo.BOOLEANO and self.OperacionDer.tipo == Tipo.BOOLEANO:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) != self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == Tipo.BOOLEANO and self.OperacionDer.tipo == Tipo.STRING:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) != self.obtenerVal(self.OperacionDer.tipo, der)
            # CHAR
            elif self.OperacionIzq.tipo == Tipo.CHAR and self.OperacionDer.tipo == Tipo.CHAR:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) != self.obtenerVal(self.OperacionDer.tipo, der)
            # STRING
            elif self.OperacionIzq.tipo == Tipo.STRING and self.OperacionDer.tipo == Tipo.INT64:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) != str(self.obtenerVal(self.OperacionDer.tipo, der))
            elif self.OperacionIzq.tipo == Tipo.STRING and self.OperacionDer.tipo == Tipo.FLOAT64:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) != self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == Tipo.STRING and self.OperacionDer.tipo == Tipo.BOOLEANO:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) != self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == Tipo.STRING and self.OperacionDer.tipo == Tipo.STRING:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) != self.obtenerVal(self.OperacionDer.tipo, der)
            return Exception("Semantico", "Tipo Erroneo de operacion para =!.", self.fila, self.columna)

        elif self.operador == Operador_Relacional.MENQ:
            # INT
            if self.OperacionIzq.tipo == Tipo.INT64 and self.OperacionDer.tipo == Tipo.INT64:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) < self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == Tipo.INT64 and self.OperacionDer.tipo == Tipo.FLOAT64:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) < self.obtenerVal(self.OperacionDer.tipo, der)
            # DOUBLE
            elif self.OperacionIzq.tipo == Tipo.FLOAT64 and self.OperacionDer.tipo == Tipo.INT64:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) < self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == Tipo.FLOAT64 and self.OperacionDer.tipo == Tipo.FLOAT64:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) < self.obtenerVal(self.OperacionDer.tipo, der)
            # BOOLEAN
            elif self.OperacionIzq.tipo == Tipo.BOOLEANO and self.OperacionDer.tipo == Tipo.BOOLEANO:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) < self.obtenerVal(self.OperacionDer.tipo, der)
            return Exception("Semantico", "Tipo Erroneo de operacion para <.", self.fila, self.columna)

        elif self.operador == Operador_Relacional.MAYQ:
            # INT
            if self.OperacionIzq.tipo == Tipo.INT64 and self.OperacionDer.tipo == Tipo.INT64:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) > self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == Tipo.INT64 and self.OperacionDer.tipo == Tipo.FLOAT64:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) > self.obtenerVal(self.OperacionDer.tipo, der)
            # DOUBLE
            elif self.OperacionIzq.tipo == Tipo.FLOAT64 and self.OperacionDer.tipo == Tipo.INT64:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) > self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == Tipo.FLOAT64 and self.OperacionDer.tipo == Tipo.FLOAT64:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) > self.obtenerVal(self.OperacionDer.tipo, der)
            # BOOLEAN
            elif self.OperacionIzq.tipo == Tipo.BOOLEANO and self.OperacionDer.tipo == Tipo.BOOLEANO:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) > self.obtenerVal(self.OperacionDer.tipo, der)
            return Exception("Semantico", "Tipo Erroneo de operacion para >.", self.fila, self.columna)
        
        elif self.operador == Operador_Relacional.MENEQUALS:
            # INT
            if self.OperacionIzq.tipo == Tipo.INT64 and self.OperacionDer.tipo == Tipo.INT64:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) <= self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == Tipo.INT64 and self.OperacionDer.tipo == Tipo.FLOAT64:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) <= self.obtenerVal(self.OperacionDer.tipo, der)
            # DOUBLE
            elif self.OperacionIzq.tipo == Tipo.FLOAT64 and self.OperacionDer.tipo == Tipo.INT64:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) <= self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == Tipo.FLOAT64 and self.OperacionDer.tipo == Tipo.FLOAT64:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) <= self.obtenerVal(self.OperacionDer.tipo, der)
            # BOOLEAN
            elif self.OperacionIzq.tipo == Tipo.BOOLEANO and self.OperacionDer.tipo == Tipo.BOOLEANO:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) <= self.obtenerVal(self.OperacionDer.tipo, der)
            return Exception("Semantico", "Tipo Erroneo de operacion para <=.", self.fila, self.columna)
        
        elif self.operador == Operador_Relacional.MAYEQUALS:
            # INT
            if self.OperacionIzq.tipo == Tipo.INT64 and self.OperacionDer.tipo == Tipo.INT64:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) >= self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == Tipo.INT64 and self.OperacionDer.tipo == Tipo.FLOAT64:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) >= self.obtenerVal(self.OperacionDer.tipo, der)
            # DOUBLE
            elif self.OperacionIzq.tipo == Tipo.FLOAT64 and self.OperacionDer.tipo == Tipo.INT64:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) >= self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == Tipo.FLOAT64 and self.OperacionDer.tipo == Tipo.FLOAT64:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) >= self.obtenerVal(self.OperacionDer.tipo, der)
            # BOOLEAN
            elif self.OperacionIzq.tipo == Tipo.BOOLEANO and self.OperacionDer.tipo == Tipo.BOOLEANO:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) >= self.obtenerVal(self.OperacionDer.tipo, der)
            return Exception("Semantico", "Tipo Erroneo de operacion para >.", self.fila, self.columna)

        return Exception("Semantico", "Tipo de Operacion no Especificado.", self.fila, self.columna)

    def obtenerVal(self, tipo, val):
        if tipo == Tipo.INT64:
            return int(val)
        elif tipo == Tipo.FLOAT64:
            return float(val)
        elif tipo == Tipo.BOOLEANO:
            return bool(val)
        return str(val)