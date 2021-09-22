import math as ma
from Interprete.Abstract.Instruccion import Instruccion
from Interprete.Abstract.NodoAst import NodoAst
from Interprete.Expresiones.Identificador import Identificador
from Interprete.Expresiones.Primitivos import Primitivos
from Interprete.TS.Exception import Exception
from Interprete.TS.TablaSimbolos import TablaSimbolos
from Interprete.Instrucciones.Break import Break
from Interprete.TS.Simbolo import Simbolo
from Interprete.TS.Tipo import *
from Interprete.Instrucciones.Funcion import Funcion
from datetime import datetime

class Nativas(Instruccion):
    def __init__(self, nombre, parametros, fila, columna):
        self.nombre = nombre
        self.parametros = parametros
        self.fila = fila
        self.columna = columna
        self.tipo = None
    
    def interpretar(self, tree, table):
        if self.nombre == 'log':
            if len(self.parametros) != 2:
                return Exception("Semantico", "Solo se admiten 2 parametros en funcion nativa: log", self.fila, self.columna, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            base = self.parametros[0].interpretar(tree, table)
            valor = self.parametros[1].interpretar(tree, table)
            if type(base) != int:
                return Exception("Semantico", "La base del logaritmo debe ser un entero", self.fila, self.columna, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            if type(valor) != int and type(valor) != float:
                return Exception("Semantico", "El valor del logaritmo debe ser de tipo numerico", self.fila, self.columna, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            result = ma.log(valor, base)
            if type(valor) == int:
                self.tipo = Tipo.INT64
            elif type(valor) == float:
                self.tipo = Tipo.FLOAT64
            return result
        
        elif self.nombre == 'log10':
            if len(self.parametros) != 1:
                return Exception("Semantico", "Solo se admite 1 parametros en funcion nativa: log10", self.fila, self.columna, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            valor = self.parametros[0].interpretar(tree, table)
            if type(valor) != int and type(valor) != float:
                return Exception("Semantico", "El valor del logaritmo debe ser de tipo numerico", self.fila, self.columna, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            result = ma.log(valor,10)
            if type(valor) == int:
                self.tipo = Tipo.INT64
            elif type(valor) == float:
                self.tipo = Tipo.FLOAT64
            return result
                
        elif self.nombre == 'sin' or self.nombre == 'cos' or self.nombre == 'tan'  or self.nombre == 'sqrt' or self.nombre == 'float':
            if len(self.parametros) != 1:
                return Exception("Semantico", "Solo se admite 1 parametros en funcion nativa: "+self.nombre, self.fila, self.columna, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            valor = self.parametros[0].interpretar(tree, table)
            if type(valor) != int and type(valor) != float:
                return Exception("Semantico", "El valor que se necesita en "+ self.nombre+" debe ser de tipo numerico", self.fila, self.columna, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            if self.nombre == 'sin' :
                result = ma.sin(valor)
            elif self.nombre == 'cos' :
                result = ma.cos(valor)
            elif self.nombre == 'tan':
                result = ma.tan(valor)
            elif self.nombre == 'sqrt':
                result = ma.sqrt(valor)
            elif self.nombre == 'float':
                result=float(valor)
            
            if type(result) == int:
                self.tipo = Tipo.INT64
            elif type(result) == float:
                self.tipo = Tipo.FLOAT64
            return result
        
        elif self.nombre == 'parse':
            if len(self.parametros) != 2:
                return Exception("Semantico", "Se esperaban 2 parametros en funcion nativa", self.fila, self.columna, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            tipoFinal = self.parametros[0]
            if not(isinstance(tipoFinal,Tipo)):
                return Exception("Semantico", "Se un tipo de dato en funcion parse", self.fila, self.columna, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            valor = self.parametros[1].interpretar(tree, table)
            if not(type(valor) == str):
                return Exception("Semantico", "Solo se pueden parsear STRING", self.fila, self.columna, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            if tipoFinal == Tipo.INT64:
                try:
                    result =  int(valor)
                except ValueError:
                    return Exception("Semantico", "La cadena enviada no contiene un INT64", self.fila, self.columna, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                self.tipo = Tipo.INT64
            elif tipoFinal == Tipo.FLOAT64:
                try:
                    result =  float(valor)
                except ValueError:
                    return Exception("Semantico", "La cadena enviada no contiene un FLOAT64", self.fila, self.columna, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                self.tipo = Tipo.FLOAT64
            else:
                return Exception("Semantico", "Solo se puede parsear a numeros", self.fila, self.columna, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            return result

        elif self.nombre == 'trunc':
            if len(self.parametros) != 2 and len(self.parametros) != 1:
                return Exception("Semantico", "Cantidad de parametros no valida en trunc", self.fila, self.columna, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            if len(self.parametros) == 2:
                valor = self.parametros[1].interpretar(tree, table)
            else:
                valor = self.parametros[0].interpretar(tree, table)
            if not(type(valor) == float):
                return Exception("Semantico", "Solo se pueden truncar FLOAT64", self.fila, self.columna, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            result =  round(valor)
            self.tipo = Tipo.INT64
            return result

        elif self.nombre == 'string':
            if len(self.parametros) != 1:
                return Exception("Semantico", "Solo se admite 1 parametros en funcion nativa: "+self.nombre, self.fila, self.columna, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            valor = self.parametros[0].interpretar(tree, table)
            result = str(valor)
            self.tipo = Tipo.STRING
            return result
        
        elif self.nombre == 'uppercase' or self.nombre == 'lowercase':
            if len(self.parametros) != 1:
                return Exception("Semantico", "Solo se admite 1 parametros en funcion nativa: "+self.nombre, self.fila, self.columna, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            valor = self.parametros[0].interpretar(tree, table)
            if type(valor) != str:
                return Exception("Semantico", "Solo se permite hacer uppercase/lowercase a STRING", self.fila, self.columna, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            if self.nombre == "uppercase":
                result = valor.upper()
            elif self.nombre == "lowercase":
                result = valor.lower()
            self.tipo = Tipo.STRING
            return result
        
        elif self.nombre == 'typeof':
            if len(self.parametros) != 1:
                return Exception("Semantico", "Solo se admite 1 parametros en funcion nativa: "+self.nombre, self.fila, self.columna, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            valor = self.parametros[0].interpretar(tree, table)
            result = ""
            if type(valor) == int:
                result = "Int64"
                self.tipo = Tipo.INT64
            elif type(valor) == float:
                result = "Float64"
                self.tipo = Tipo.FLOAT64
            elif type(valor) == bool:
                result = "Boolean"
                self.tipo = Tipo.BOOLEANO
            elif type(valor) == str and len(valor) == 1:
                result = "Char"
                self.tipo = Tipo.CHAR
            elif type(valor) == str:
                result = "String"
                self.tipo = Tipo.STRING
            if result == "":
                return Exception("Semantico", "No se encontro referencia al parametro en funcion nativa:  "+self.nombre, self.fila, self.columna, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            return result

        elif self.nombre == 'length':
            if type(self.parametros[0]) != Identificador:
                return Exception("Semantico", "Parametros invalidos en funcion nativa LENGTH, debe enviar un identificador", self.fila, self.columna, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            arreglo = tree.getArreglo(self.parametros[0].identificador)
            if arreglo == None:
                return Exception("Semantico", "No se encontró el arreglo "+self.nombre+" declarado", self.fila, self.columna, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            variables = arreglo.getVariables()
            self.tipo = Tipo.INT64
            return len(variables)
    
    def getNodo(self):
        nodo = NodoAst("FUNCION NATIVA")
        nodo.agregarHijo(str(self.nombre))
        parametros = NodoAst("PARAMETROS")
        for param in self.parametros:
            if isinstance(param, Identificador):
                parametros.agregarHijoNodo(NodoAst(str(param.identificador)))
            elif isinstance(param, Primitivos):
                parametros.agregarHijoNodo(NodoAst(str(param.valor)))
        nodo.agregarHijoNodo(parametros)
        return nodo