from Interprete.Abstract.Instruccion import Instruccion
from Interprete.Abstract.NodoAst import NodoAst
from Interprete.TS.Exception import Exception
from Interprete.TS.Tipo import Tipo
from Interprete.TS.TablaSimbolos import TablaSimbolos
from Interprete.Instrucciones.Break import Break
from Interprete.Instrucciones.Return import Return
from Interprete.Instrucciones.Continue import Continue
from datetime import datetime

class While(Instruccion):
    def __init__(self, condicion, instrucciones, fila, columna):
        self.condicion = condicion
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        tree.setAmbito("While")
        while True:
            condicion = self.condicion.interpretar(tree, table)
            if isinstance(condicion, Exception):
                tree.removeAmbito()
                return condicion
            
            if self.condicion.tipo == Tipo.BOOLEANO: # Aqui verifica si la condicion es una expresion logica, sino lanza una Exception.
                if bool(condicion) == True:                 
                    nuevaTabla = TablaSimbolos(table)        # Inicia el Nuevo Ambito.
                    for instruccion in self.instrucciones:  # Inicia ejecutando las instrucciones adentro del While.
                        result = instruccion.interpretar(tree, nuevaTabla) 
                        if isinstance(result, Exception):
                            tree.get_excepcion().append(result)
                            tree.update_consola(result.__str__())
                        if isinstance(result, Break):
                            tree.removeAmbito()
                            return None
                        if isinstance(result, Return):
                            tree.removeAmbito()
                            return result
                        if isinstance(result, Continue): break
                else:
                    tree.removeAmbito()
                    break
            else:
                tree.removeAmbito()
                return Exception("Semantico", "Error en while, la expresion no retorna un booleano.", self.fila, self.columna, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def getNodo(self):
        nodo = NodoAst("WHILE")
        nodo.agregarHijoNodo(self.condicion.getNodo())
        instrucciones = NodoAst("INSTRUCCIONES")
        for instr in self.instrucciones:
            instrucciones.agregarHijoNodo(instr.getNodo())
        nodo.agregarHijoNodo(instrucciones)
        return nodo