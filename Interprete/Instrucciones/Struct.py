from Interprete.Abstract.Instruccion import Instruccion
from Interprete.TS.Tipo import Tipo
from Interprete.TS.Exception import Exception

class Struct(Instruccion):
    def __init__(self, tipo, nombre, parametros, fila, columna):
        self.tipo = tipo
        self.nombre = nombre
        self.parametros = parametros
        self.fila = fila
        self.columna = columna
    
    def interpretar(self, tree, table):
        nuevaTabla = TablaSimbolos(table) 
        for instr in self.instrucciones:
            value = instr.interpretar(tree, nuevaTabla)

            if isinstance(value, Exception):
                tree.get_excepcion().append(value)
                tree.update_consola(value.__str__())

            if isinstance(value, Break): 
                err = Exception("Semantico", "Sentencia Break fuera de ciclo", instr.fila, instr.columna)
                tree.get_excepcion().append(err)
                tree.update_consola(err.__str__())
            if isinstance(value, Continue): 
                err = Exception("Semantico", "Sentencia Continue fuera de ciclo", instr.fila, instr.columna)
                tree.get_excepcion().append(err)
                tree.update_consola(err.__str__())
            if isinstance(value, Return):
                self.tipo = value.tipo
                return value.result
        return None