class Arbol():
    def __init__(self, instruccion):
        self.instruccion = instruccion
        self.funciones = []
        self.plantillas_structs = []
        #self.structs = []
        self.arreglos = []
        self.excepcion = []
        self.tablaFinal = []
        self.ambitoActual = ["Global"]
        self.consola = ""
        self.tabla_ts_global = None

    def get_instruccion(self):
        return self.instruccion

    def set_instruccion(self, instruccion):
        self.instruccion = instruccion

    def get_excepcion(self):
        return self.excepcion

    def set_excepcion(self, excepcion):
        self.excepcion = excepcion

    def get_consola(self):
        return self.consola
    
    def set_consola(self, consola):
        self.consola = consola

    def actualizar_consola_sin_salto(self, cadena):
        self.consola += str(cadena)
        
    def actualizar_consola_salto(self, cadena):
        self.consola += str(cadena) + '\n'

    def get_tabla_ts_global(self):
        return self.tabla_ts_global

    def set_tabla_ts_global(self, ts_global):
        self.tabla_ts_global = ts_global

    ## Metodos para las funciones
    def addFuncion(self, funcion):
        self.funciones.append(funcion)

    def get_funciones(self):
        return self.funciones

    def getFuncion(self, nombre):
        for funcion in self.funciones:
            if funcion.nombre == nombre:
                return funcion
        return None
    
    def addPlantillaStruct(self, struct):
        self.plantillas_structs.append(struct)

    def get_Plantillas_structs(self):
        return self.plantillas_structs

    def getPlantillaStruct(self, nombre):
        for struct in self.plantillas_structs:
            if struct.nombre == nombre:
                return struct
        return None
    


    def addArreglo(self, arreglo):
        self.agregarVariable([str(arreglo.identificador), str(arreglo.tipo), "Global", str(arreglo.fila),str(arreglo.columna)])
        self.arreglos.append(arreglo)

    def getArreglo(self, identificador):
        for arreglo in self.arreglos:
            if arreglo.identificador == identificador:
                return arreglo
        return None

    def getAmbito(self):
        return self.ambitoActual[len(self.ambitoActual)-1]
    
    def setAmbito(self, ambito):
        self.ambitoActual.append(ambito)
    
    def removeAmbito(self):
        self.ambitoActual.pop()
    
    def agregarVariable(self, variable):
        variable[1]=str(variable[1]).replace("Tipo.","")
        self.tablaFinal.append(variable)

    def getTablaSimbolos(self):
        return self.tablaFinal
    
    """    def addStruct(self, struct):
        self.structs.append(struct)

    def getStruct(self, nombre):
        for struct in self.structs:
            if struct.nombre == nombre:
                return struct
        return None
    
    def get_structs(self):
        return self.structs"""