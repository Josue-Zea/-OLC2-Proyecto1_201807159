from Interprete.Abstract.Instruccion import Instruccion
from Interprete.TS.Exception import Exception
from Interprete.TS.Tipo import Tipo
from Interprete.TS.TablaSimbolos import TablaSimbolos
from Interprete.TS.Simbolo import Simbolo
from Interprete.Instrucciones.Break import Break
from Interprete.Instrucciones.Return import Return
from Interprete.Instrucciones.Continue import Continue

class For(Instruccion):
    def __init__(self, identificador, izquierdo, derecho, instrucciones,  fila, columna):
        self.identificador = identificador
        self.izquierdo = izquierdo
        self.derecho = derecho
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        nuevo = TablaSimbolos(table)
        condicion1 = self.izquierdo.interpretar(tree, nuevo)
        if isinstance(condicion1, Exception): return condicion1
        if self.derecho != None:
            condicion2 = self.derecho.interpretar(tree, nuevo)
            if isinstance(condicion2, Exception): return condicion2
        if self.izquierdo.tipo == Tipo.INT64 and self.derecho.tipo == Tipo.INT64:
            simbolo = nuevo.getTabla(self.identificador)
            if simbolo == None:
                simbolo = Simbolo(str(self.identificador), self.izquierdo.tipo, self.fila, self.columna, condicion1)
                resultado = nuevo.setTabla(simbolo)
            aux = condicion1;
            while(condicion1<=condicion2):
                nuevo2 = TablaSimbolos(nuevo)
                simbolo = Simbolo(str(self.identificador), self.izquierdo.tipo, self.fila, self.columna, condicion1)
                result = nuevo.actualizarTabla(simbolo)
                for instruccion in self.instrucciones:
                    result = instruccion.interpretar(tree, nuevo2) 
                    if isinstance(result, Exception) :
                        tree.get_excepcion().append(result)
                        tree.update_consola(result.__str__())
                    if isinstance(result, Break): return None
                    if isinstance(result, Return): return result
                    if isinstance(result, Continue): break
                condicion1+=1
                if(condicion1>condicion2): break;
            simbolo = Simbolo(str(self.identificador), self.izquierdo.tipo, self.fila, self.columna, aux)
            result = nuevo.actualizarTabla(simbolo)
        
        elif self.izquierdo.tipo == Tipo.STRING and self.derecho==None:
            simbolo = nuevo.getTabla(self.identificador)
            if simbolo == None:
                simbolo = Simbolo(str(self.identificador), self.izquierdo.tipo, self.fila, self.columna, condicion1)
                resultado = nuevo.setTabla(simbolo)
            aux = condicion1;
            i = 0
            while(i < len(condicion1)):
                nuevo2 = TablaSimbolos(nuevo)
                simbolo = Simbolo(str(self.identificador), self.izquierdo.tipo, self.fila, self.columna, condicion1[i])
                result = nuevo.actualizarTabla(simbolo)
                for instruccion in self.instrucciones:
                    result = instruccion.interpretar(tree, nuevo2) 
                    if isinstance(result, Exception) :
                        tree.get_excepcion().append(result)
                        tree.update_consola(result.__str__())
                    if isinstance(result, Break): return None
                    if isinstance(result, Return): return result
                    if isinstance(result, Continue): break
                i+=1
            simbolo = Simbolo(str(self.identificador), self.izquierdo.tipo, self.fila, self.columna, aux)
            result = nuevo.actualizarTabla(simbolo)
        
        else:
            return Exception("Semantico", "Rangos no validos en bucle for.", self.fila, self.columna)