from Interprete.Abstract.Instruccion import Instruccion
from Interprete.TS.Exception import Exception
from Interprete.TS.Tipo import Tipo
from Interprete.TS.TablaSimbolos import TablaSimbolos
from Interprete.TS.Simbolo import Simbolo
from Interprete.Instrucciones.Arreglo import Arreglo
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
        if type(self.izquierdo)!=list:
            condicion1 = self.izquierdo.interpretar(tree, nuevo)
            if isinstance(condicion1, Exception): return condicion1
        if self.derecho != None:
            condicion2 = self.derecho.interpretar(tree, nuevo)
            if isinstance(condicion2, Exception): return condicion2
        if type(self.izquierdo) == list and self.derecho == None: # Cuando se envia un arreglo de esta forma arr[a:b]
            arr = tree.getArreglo(self.izquierdo[0])
            if arr == None:
                return Exception("Semantico", "No se encuentra declarado  el arreglo.", self.fila, self.columna)
            arr = arr.getVariables()
            simbolo = nuevo.getTabla(self.identificador)
            condicion1 = self.izquierdo[1].interpretar(tree, table)
            condicion2 = self.izquierdo[2].interpretar(tree, table)
            if type(condicion1) != int or type(condicion2) != int:
                return Exception("Semantico", "Rangos no validos en bucle for.", self.fila, self.columna)
            if simbolo == None:
                simbolo = Simbolo(str(self.identificador), arr[condicion1].tipo, self.fila, self.columna, condicion1)
                resultado = nuevo.setTabla(simbolo)
            aux = condicion1;
            while(condicion1<=condicion2):
                nuevo2 = TablaSimbolos(nuevo)
                simbolo = Simbolo(str(self.identificador), arr[condicion1].tipo, self.fila, self.columna, arr[condicion1].valor)
                result = nuevo.actualizarTabla(simbolo)
                for instruccion in self.instrucciones:
                    result = instruccion.interpretar(tree, nuevo2) 
                    if isinstance(result, Exception) :
                        tree.get_excepcion().append(result)
                        tree.actualizar_consola_salto(result.__str__())
                    if isinstance(result, Break): return None
                    if isinstance(result, Return): return result
                    if isinstance(result, Continue): break
                condicion1+=1
                if(condicion1>condicion2): break;
            simbolo = Simbolo(str(self.identificador), arr[condicion1].tipo, self.fila, self.columna, aux)
            result = nuevo.actualizarTabla(simbolo)
            return None
        else:
            if self.izquierdo.tipo == Tipo.INT64 and self.derecho.tipo == Tipo.INT64: # Cuando se espera que sean dos enteros
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
                            tree.actualizar_consola_salto(result.__str__())
                        if isinstance(result, Break): return None
                        if isinstance(result, Return): return result
                        if isinstance(result, Continue): break
                    condicion1+=1
                    if(condicion1>condicion2): break;
                simbolo = Simbolo(str(self.identificador), self.izquierdo.tipo, self.fila, self.columna, aux)
                result = nuevo.actualizarTabla(simbolo)
                return None

            elif self.izquierdo.tipo == Tipo.STRING and self.derecho==None: # Cuando se contiene un string
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
                            tree.actualizar_consola_salto(result.__str__())
                        if isinstance(result, Break): return None
                        if isinstance(result, Return): return result
                        if isinstance(result, Continue): break
                    i+=1
                simbolo = Simbolo(str(self.identificador), self.izquierdo.tipo, self.fila, self.columna, aux)
                result = nuevo.actualizarTabla(simbolo)

            elif isinstance(self.izquierdo, Arreglo) and self.derecho == None: # Cuando se contiene un arreglo
                simbolo = nuevo.getTabla(self.identificador)
                if simbolo == None:
                    simbolo = Simbolo(str(self.identificador), self.izquierdo.tipo, self.fila, self.columna, condicion1)
                    resultado = nuevo.setTabla(simbolo)
                aux = condicion1;
                for var in self.izquierdo.getVariables():    
                    nuevo2 = TablaSimbolos(nuevo)
                    simbolo = Simbolo(str(self.identificador), var.tipo, self.fila, self.columna, var.valor)
                    result = nuevo.actualizarTabla(simbolo)
                    for instruccion in self.instrucciones:
                        result = instruccion.interpretar(tree, nuevo2) 
                        if isinstance(result, Exception) :
                            tree.get_excepcion().append(result)
                            tree.actualizar_consola_salto(result.__str__())
                        if isinstance(result, Break): return None
                        if isinstance(result, Return): return result
                        if isinstance(result, Continue): break
                simbolo = Simbolo(str(self.identificador), var.tipo, self.fila, self.columna, aux)
                result = nuevo.actualizarTabla(simbolo)
                return None

            elif type(condicion1) == list and self.derecho==None:
                print("Condicion1")
                simbolo = nuevo.getTabla(self.identificador)
                if simbolo == None:
                    simbolo = Simbolo(str(self.identificador), var.tipo, self.fila, self.columna, condicion1)
                    resultado = nuevo.setTabla(simbolo)
                aux = condicion1;
                for var in condicion1:
                    nuevo2 = TablaSimbolos(nuevo)
                    simbolo = Simbolo(str(self.identificador), var.tipo, self.fila, self.columna, var.valor)
                    result = nuevo.actualizarTabla(simbolo)
                    for instruccion in self.instrucciones:
                        result = instruccion.interpretar(tree, nuevo2) 
                        if isinstance(result, Exception) :
                            tree.get_excepcion().append(result)
                            tree.actualizar_consola_salto(result.__str__())
                        if isinstance(result, Break): return None
                        if isinstance(result, Return): return result
                        if isinstance(result, Continue): break
                simbolo = Simbolo(str(self.identificador), var.tipo, self.fila, self.columna, aux)
                result = nuevo.actualizarTabla(simbolo)
                return None
            
            else:
                return Exception("Semantico", "Rangos no validos en bucle for.", self.fila, self.columna)