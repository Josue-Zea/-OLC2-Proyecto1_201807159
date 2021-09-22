import graphviz
contador = 1
def generarAST(nodo):
    global contador
    dot = graphviz.Digraph(name="AST",format="svg")
    dot.node("n0",nodo.getValor().replace("\"","\\\""))
    agregarNodos(dot,"n0",nodo)
    return dot

def agregarNodos(dot, anterior, father):
    global contador
    for nodo in father.getHijos():
        idNodo = "n"+str(contador)
        dot.node(idNodo, nodo.getValor().replace("\"","\\\""))
        dot.edge(anterior,idNodo)
        contador+=1
        agregarNodos(dot, idNodo, nodo)