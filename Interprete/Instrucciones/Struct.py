class Struct():
    def __init__(self, tipo, nombre, fila, columna):
        self.tipo = tipo
        self.nombre = nombre
        self.variables = []
        self.fila = fila
        self.columna = columna

    def get_nombre(self):
        return self.nombre

    def get_tipo(self):
        return self.tipo

    def get_fila(self):
        return self.fila

    def get_columna(self):
        return self.columna
    
    ##Defifnir metodos para declarar variables y obtener sus valores
    def agregarVariable(self, var):
        self.variables.append(var)
        
    def getVariable(self, nombre):
        for variable in self.variables:
            if variable["identificador"] == nombre:
                return variable
        return None

    def getVariables(self):
        return self.variables

    def __str__(self):
        return str(self.nombre) + "-" + str(self.tipo) + "-[" + str(self.fila) + "," + str(self.columna) +"]-"