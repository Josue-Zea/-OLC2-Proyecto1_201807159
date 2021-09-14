from Interprete.Expresiones.Identificador import Identificador
from Interprete.TS.Exception import Exception
from Interprete.Abstract.Instruccion import Instruccion
from Interprete.TS.Simbolo import Simbolo


class Asignacion(Instruccion):
    def __init__(self, identificador, expresion, tipo, fila, columna):
        self.identificador = identificador
        self.expresion = expresion
        self.tipo = tipo
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        valor = self.expresion.interpretar(tree, table) # Ejecutamos la expresion que venga en la asignacion
        if isinstance(valor, Exception): return valor
        
        if self.tipo != None and self.tipo != self.expresion.tipo:
            return Exception("Semantico", "Los tipos de variables no concuerdan: "+str(self.tipo)+"!="+str(self.expresion.tipo))
        self.tipo = self.expresion.tipo
        var = ""
        simb = table.getTabla(self.identificador)
        simbolo = Simbolo(str(self.identificador),self.expresion.tipo, self.fila, self.columna, valor)
        if simb == None:
            var = table.setTabla(simbolo)
        else:
            var = table.actualizarTabla(simbolo)
        
        if isinstance(var, Exception): return var
        return None