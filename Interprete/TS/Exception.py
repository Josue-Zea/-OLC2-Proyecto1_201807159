class Exception():
    def __init__(self, tipo, descripcion, fila, columna, tiempo):
        self.tipo = tipo
        self.descripcion = descripcion
        self.fila = fila
        self.columna = columna
        self.tiempo = tiempo

    def __str__(self):
        return f"{self.tipo} - {self.descripcion} - [{self.fila},{self.columna},{self.tiempo}]"