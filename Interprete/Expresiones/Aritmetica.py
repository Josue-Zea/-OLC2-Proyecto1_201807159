from Interprete.Abstract.Instruccion import Instruccion
from Interprete.TS.Exception import Exception
from Interprete.TS.Tipo import Tipo, Operador_Aritmetico

class Aritmetica(Instruccion):
    def __init__(self, operador, OperacionIzq, OperacionDer, fila, columna):
        self.operador = operador
        self.OperacionIzq = OperacionIzq
        self.OperacionDer = OperacionDer
        self.fila = fila
        self.columna = columna
        self.tipo = None

    def interpretar(self, tree, table):
        izq = self.OperacionIzq.interpretar(tree, table)
        if isinstance(izq, Exception): return izq
        if self.OperacionDer != None:
            der = self.OperacionDer.interpretar(tree, table)
            if isinstance(der, Exception): return der

        if self.operador == Operador_Aritmetico.SUMA: # CUANDO TIENE UN SIGNO POSITIVO (+)
            if self.OperacionIzq.tipo == Tipo.INT64 and self.OperacionDer.tipo == Tipo.INT64:
                self.tipo = Tipo.INT64
                return self.returnVal(self.OperacionIzq.tipo, izq) + self.returnVal(self.OperacionDer.tipo, der) 
            elif self.OperacionIzq.tipo == Tipo.INT64 and self.OperacionDer.tipo == Tipo.FLOAT64:
                self.tipo = Tipo.FLOAT64
                return self.returnVal(self.OperacionIzq.tipo, izq) + self.returnVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == Tipo.FLOAT64 and self.OperacionDer.tipo == Tipo.INT64:
                self.tipo = Tipo.FLOAT64
                return self.returnVal(self.OperacionIzq.tipo, izq) + self.returnVal(self.OperacionDer.tipo, der) 
            elif self.OperacionIzq.tipo == Tipo.FLOAT64 and self.OperacionDer.tipo == Tipo.FLOAT64:
                self.tipo = Tipo.FLOAT64
                return self.returnVal(self.OperacionIzq.tipo, izq) + self.returnVal(self.OperacionDer.tipo, der)

            return Exception("Semantico", "Tipos erroneos en operación suma.", self.fila, self.columna)
        
        elif self.operador == Operador_Aritmetico.RESTA:
            if self.OperacionIzq.tipo == Tipo.INT64 and self.OperacionDer.tipo == Tipo.INT64:
                self.tipo = Tipo.INT64
                return self.returnVal(self.OperacionIzq.tipo, izq) - self.returnVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == Tipo.INT64 and self.OperacionDer.tipo == Tipo.FLOAT64:
                self.tipo = Tipo.FLOAT64
                return self.returnVal(self.OperacionIzq.tipo, izq) - self.returnVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == Tipo.FLOAT64 and self.OperacionDer.tipo == Tipo.INT64:
                self.tipo = Tipo.FLOAT64
                return self.returnVal(self.OperacionIzq.tipo, izq) - self.returnVal(self.OperacionDer.tipo, der) 
            elif self.OperacionIzq.tipo == Tipo.FLOAT64 and self.OperacionDer.tipo == Tipo.FLOAT64:
                self.tipo = Tipo.FLOAT64
                return self.returnVal(self.OperacionIzq.tipo, izq) - self.returnVal(self.OperacionDer.tipo, der) 
            
            return Exception("Semantico", "Tipos erroneos en operación resta.", self.fila, self.columna)

        elif self.operador == Operador_Aritmetico.MULTIPLICACION:
            if self.OperacionIzq.tipo == Tipo.INT64 and self.OperacionDer.tipo == Tipo.INT64:
                self.tipo = Tipo.INT64
                return self.returnVal(self.OperacionIzq.tipo, izq) * self.returnVal(self.OperacionDer.tipo, der) 
            elif self.OperacionIzq.tipo == Tipo.INT64 and self.OperacionDer.tipo == Tipo.FLOAT64:
                self.tipo = Tipo.FLOAT64
                return self.returnVal(self.OperacionIzq.tipo, izq) * self.returnVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == Tipo.FLOAT64 and self.OperacionDer.tipo == Tipo.INT64:
                self.tipo = Tipo.FLOAT64
                return self.returnVal(self.OperacionIzq.tipo, izq) * self.returnVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == Tipo.FLOAT64 and self.OperacionDer.tipo == Tipo.FLOAT64:
                self.tipo = Tipo.FLOAT64
                return self.returnVal(self.OperacionIzq.tipo, izq) * self.returnVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == Tipo.STRING and self.OperacionDer.tipo == Tipo.STRING:
                self.tipo = Tipo.STRING
                var = self.returnVal(self.OperacionIzq.tipo, izq)
                var += self.returnVal(self.OperacionDer.tipo, der)
                return var
            return Exception("Semantico", "Tipos erroneos en operación multiplicación.", self.fila, self.columna)

        elif self.operador == Operador_Aritmetico.DIVISION:
            if self.OperacionIzq.tipo == Tipo.INT64 and self.OperacionDer.tipo == Tipo.INT64:
                self.tipo = Tipo.FLOAT64
                if self.returnVal(self.OperacionDer.tipo, der) == 0:  
                    return Exception("Semantico", "No es posible dividir entre cero", self.fila, self.columna)
                return self.returnVal(self.OperacionIzq.tipo, izq) / self.returnVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == Tipo.INT64 and self.OperacionDer.tipo == Tipo.FLOAT64:
                self.tipo = Tipo.FLOAT64
                if self.returnVal(self.OperacionDer.tipo, der) == 0:  
                    return Exception("Semantico", "No es posible dividir entre cero", self.fila, self.columna)
                return self.returnVal(self.OperacionIzq.tipo, izq) / self.returnVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == Tipo.FLOAT64 and self.OperacionDer.tipo == Tipo.INT64:
                self.tipo = Tipo.FLOAT64
                if self.returnVal(self.OperacionDer.tipo, der) == 0:  
                    return Exception("Semantico", "No es posible dividir entre cero", self.fila, self.columna)
                return self.returnVal(self.OperacionIzq.tipo, izq) / self.returnVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == Tipo.FLOAT64 and self.OperacionDer.tipo == Tipo.FLOAT64:
                self.tipo = Tipo.FLOAT64
                if self.returnVal(self.OperacionDer.tipo, der) == 0:  
                    return Exception("Semantico", "No es posible dividir entre cero", self.fila, self.columna)
                return self.returnVal(self.OperacionIzq.tipo, izq) / self.returnVal(self.OperacionDer.tipo, der)
            
            return Exception("Semantico", "Tipos erroneos en operación división.", self.fila, self.columna)
        
        elif self.operador == Operador_Aritmetico.POTENCIA:
            if self.OperacionIzq.tipo == Tipo.INT64 and self.OperacionDer.tipo == Tipo.INT64:
                self.tipo = Tipo.INT64
                return self.returnVal(self.OperacionIzq.tipo, izq) ** self.returnVal(self.OperacionDer.tipo, der)            
            elif self.OperacionIzq.tipo == Tipo.INT64 and self.OperacionDer.tipo == Tipo.FLOAT64:
                self.tipo = Tipo.FLOAT64
                return self.returnVal(self.OperacionIzq.tipo, izq) ** self.returnVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == Tipo.FLOAT64 and self.OperacionDer.tipo == Tipo.INT64:
                self.tipo = Tipo.FLOAT64
                return self.returnVal(self.OperacionIzq.tipo, izq) ** self.returnVal(self.OperacionDer.tipo, der) 
            elif self.OperacionIzq.tipo == Tipo.FLOAT64 and self.OperacionDer.tipo == Tipo.FLOAT64:
                self.tipo = Tipo.FLOAT64
                return self.returnVal(self.OperacionIzq.tipo, izq) ** self.returnVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == Tipo.STRING and self.OperacionDer.tipo == Tipo.INT64:
                self.tipo = Tipo.STRING
                var = self.returnVal(self.OperacionIzq.tipo, izq)
                res=""
                for i in range(self.returnVal(self.OperacionDer.tipo, der)):
                    res+=var
                return res
            return Exception("Semantico", "Tipos erroneos en operación potencia.", self.fila, self.columna)

        elif self.operador == Operador_Aritmetico.COMA:
            self.tipo = Tipo.STRING
            return str(izq) + str(der)
        
        elif self.operador == Operador_Aritmetico.MODULO:
            if self.OperacionIzq.tipo == Tipo.INT64 and self.OperacionDer.tipo == Tipo.INT64:
                self.tipo = Tipo.FLOAT64
                if self.returnVal(self.OperacionDer.tipo, der) == 0:  
                    return Exception("Semantico", "No es posible mod entre cero", self.fila, self.columna)
                return self.returnVal(self.OperacionIzq.tipo, izq) % self.returnVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == Tipo.INT64 and self.OperacionDer.tipo == Tipo.FLOAT64:
                self.tipo = Tipo.FLOAT64
                if self.returnVal(self.OperacionDer.tipo, der) == 0:  
                    return Exception("Semantico", "No es posible mod entre cero", self.fila, self.columna)
                return self.returnVal(self.OperacionIzq.tipo, izq) % self.returnVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == Tipo.FLOAT64 and self.OperacionDer.tipo == Tipo.INT64:
                self.tipo = Tipo.FLOAT64
                if self.returnVal(self.OperacionDer.tipo, der) == 0:  
                    return Exception("Semantico", "No es posible mod entre cero", self.fila, self.columna)
                return self.returnVal(self.OperacionIzq.tipo, izq) % self.returnVal(self.OperacionDer.tipo, der) 
            elif self.OperacionIzq.tipo == Tipo.FLOAT64 and self.OperacionDer.tipo == Tipo.FLOAT64:
                self.tipo = Tipo.FLOAT64
                if self.returnVal(self.OperacionDer.tipo, der) == 0:  
                    return Exception("Semantico", "No es posible mod entre cero", self.fila, self.columna)
                return self.returnVal(self.OperacionIzq.tipo, izq) % self.returnVal(self.OperacionDer.tipo, der)
            
            return Exception("Semantico", "Tipos erroneos en operación modulo.", self.fila, self.columna)

        elif self.operador == Operador_Aritmetico.UMENOS:
            if self.OperacionIzq.tipo == Tipo.INT64:
                self.tipo = Tipo.INT64
                return - self.returnVal(self.OperacionIzq.tipo, izq)
            elif self.OperacionIzq.tipo == Tipo.FLOAT64:
                self.tipo = Tipo.FLOAT64
                return - self.returnVal(self.OperacionIzq.tipo, izq)
            
            return Exception("Semantico", "Acción erronea en operador unario -.", self.fila, self.columna)
        
        return Exception("Semantico", "Tipo de Operacion no Especificado.", self.fila, self.columna)

    def returnVal(self, tipo, val):
        if tipo == Tipo.INT64:
            return int(val)
        elif tipo == Tipo.FLOAT64:
            return float(val)
        elif tipo == Tipo.BOOLEANO:
            return bool(val)
        return str(val)