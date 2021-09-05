class Arbol():
    def __init__(self, instruccion):
        self.instruccion = instruccion
        self.funciones = []
        self.excepcion = []
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