from Interprete.Abstract.Instruccion import Instruccion
from Interprete.TS.Tipo import Tipo
from Interprete.TS.Exception import Exception
from Interprete.TS.TablaSimbolos import TablaSimbolos
from Interprete.Instrucciones.Break import Break
from Interprete.Instrucciones.Return import Return
from Interprete.Instrucciones.Continue import Continue

class Funcion(Instruccion):
    def __init__(self, nombre, parametros, instrucciones, fila, columna):
        self.nombre = nombre
        self.parametros = parametros
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna
        self.tipo = Tipo.NOTHING
    
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