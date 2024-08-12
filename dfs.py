arestas_vertices = input()

quantidade_vertices = int(arestas_vertices[0])
quantidade_arestas = int(arestas_vertices[2])

is_direcionado = input()

if( is_direcionado == "nao_direcionado"):
    is_direcionado = False
if(is_direcionado == "direcionado"):
    is_direcionado = True


vertices = [[] for _ in range(quantidade_vertices)]


grau_entrada = [0 for _ in range(quantidade_vertices)]
grau_saida = [0 for _ in range(quantidade_vertices)]

arestas = list()

for x in range(quantidade_arestas):
    arestas.append(input())


for aresta in arestas:
    ligacao_v1 = int(aresta[2])
    ligacao_v2 = int(aresta[4])
    vertices[ligacao_v1].append(ligacao_v2)
    grau_saida[ligacao_v1] += 1
    grau_entrada[ligacao_v2] += 1
    if(not is_direcionado):
        vertices[ligacao_v2].append(ligacao_v1)


matriz_adjacencia = [[] for _ in range(quantidade_vertices)]

for linha in matriz_adjacencia:
    for x in range(quantidade_vertices):
        linha.append(0)


if(not is_direcionado):
    for aresta in arestas:
        ligacao_v1 = int(aresta[2])
        ligacao_v2 = int(aresta[4])
        peso = int(aresta[6])
        matriz_adjacencia[ligacao_v1][ligacao_v2] = peso
        if(not is_direcionado):
            matriz_adjacencia[ligacao_v2][ligacao_v1] = peso

lista_adjacencia = vertices

vertices = list()

for i in range(quantidade_vertices):
    vertices.append({"vertice":i,"cor": "branco", "filho": None, "tf":0, "ti":0, "lista_adjacencia": lista_adjacencia[i]})



def dfsVisita(vertice,tempo):
    tempo += 1
    vertice["ti"] = tempo
    vertice["cor"] = "cinza"
    for vizinho in vertice["lista_adjacencia"]:
        if vertices[vizinho]["cor"] == "branco":
            vertice["filho"] = vizinho
            tempo = dfsVisita(vertices[vizinho],tempo);
    vertice["cor"] = "preto"
    tempo += 1
    vertice["tf"] = tempo

    return tempo



def dfs(vertices):
    tempo = 0
    for vertice in vertices:
        if vertice["cor"] == "branco":
            dfsVisita(vertice,tempo)

def dfsOrdTop(vertices):
    if((not is_direcionado) and (not verify_cycle(vertices))):
        return []
    tempo = 0
    for key,vertice in enumerate(vertices):
        if (vertice["cor"] == "branco") and (grau_entrada[key] == 0): #verifica se não tem arestas chegando
            dfsVisita(vertice,tempo)
    ordenacao = sorted(vertices, key=lambda vertice: vertice["tf"],reverse=True)
    return ordenacao


componentes = list()


def dfsConexoVisita(vertice,tempo,componente):
    componente.append(vertice["vertice"])
    tempo += 1
    vertice["ti"] = tempo
    vertice["cor"] = "cinza"
    for vizinho in vertice["lista_adjacencia"]:
        if vertices[vizinho]["cor"] == "branco":
            vertice["filho"] = vizinho
            tempo = dfsConexoVisita(vertices[vizinho],tempo,componente);
    vertice["cor"] = "preto"
    tempo += 1
    vertice["tf"] = tempo

    return tempo


def dfsConexo(vertices):
    tempo = 0
    chave = 0
    for vertice in vertices:
        if vertice["cor"] == "branco":
            componentes.append([])
            print(componentes)
            print(chave)
            dfsConexoVisita(vertice,tempo,componentes[chave])
            chave += 1
    return componentes



teste = dfsConexo(vertices)

print(teste)



    

































