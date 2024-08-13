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

def bfs(v, visitados, vertices):                            # Função BFS padronizada, também pode aceitar um callback, caso necessário
    fila = [v]  
    visitados[v] = True
    
    while fila:
        atual = fila.pop(0)
        
        for vizinho in vertices[atual]:
            if not visitados[vizinho]:
                visitados[vizinho] = True
                fila.append(vizinho)

def dfs_cycle(v, visitados, vertices, pai):
    #o vertice é marcado como visitado                            
    visitados[v] = True                                    
    for vizinho in vertices[v]:
        #para cada vizinho roda o dfs                             
        if not visitados[vizinho]:
            if dfs_cycle(vizinho, visitados, vertices, v):
                return True
        #se o vizinho já visitado for o pai, não tem problema
        elif vizinho != pai:
            return True
    return False

def verify_cycle(vertices):
    visitados = [False] * (quantidade_vertices + 1)         

    for v in range(1, quantidade_vertices + 1):           
        if not visitados[v]:
            if dfs_cycle(v, visitados, vertices, -1): #inicial nao tem pai
                return True
        return False
    
def is_euleriano(vertices):

    if(not verify_conexo(quantidade_vertices,vertices)):
        return False

    for i in range(len(vertices)):
        if(len(vertices[i]) % 2 != 0):
            return False
    
    return True

def detecta_pontes(vertices):
    #Remove uma aresta
    #Verifica se continua conexo
    #Retorna aresta pro grafo
    
    #Uma dfs para cada componente
    def componente_conexa(v, visitados, componente):
        visitados[v] = True
        componente.append(v)
        for vizinho in vertices[v]:
            if not visitados[vizinho]:
                componente_conexa(vizinho, visitados, componente)

    pontes = []

    
    visitados = [False] * (quantidade_vertices + 1)
    
    #Para cada componente do grafo, verifica as arestas dentro dela
    for v in range(1, quantidade_vertices):
        #Se o vértice não foi visitado, cria uma nova componente e visita os vértices dela
        if not visitados[v] and len(vertices[v]) > 0:
            componente = []
            componente_conexa(v, visitados, componente)

            for aresta in arestas:
                id_aresta, ligacao_v1, ligacao_v2, peso = aresta.split()
                
                ligacao_v1 = int(ligacao_v1)
                ligacao_v2 = int(ligacao_v2)
                #Verifica se os vértices pertencem à componente que está sendo analisada
                #Se pertencem, remove as arestas, verifica se a componente continua conexa e retorna as arestas
                if ligacao_v1 in componente and ligacao_v2 in componente:
                    vertices[ligacao_v1].remove(ligacao_v2)
                    vertices[ligacao_v2].remove(ligacao_v1)

                    visitados_comp = [False] * (quantidade_vertices + 1)
                    dfs(componente[0], visitados_comp, vertices)

                    #Se algum vértice nao foi encontrado, a aresta removida é uma ponte
                    if any(not visitados_comp[u] for u in componente):
                        pontes.append(id_aresta)    
                    
                    vertices[ligacao_v1].append(ligacao_v2)
                    vertices[ligacao_v2].append(ligacao_v1)

    return pontes

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


def trilha_euleriana(vertices):
    trilha = []
    pilha = []
    
    # adiciona os vertices que possuem arestas numa pilha
    for i in range(len(vertices)):
        if len(vertices[i]["lista_adjacencia"]) > 0:
            pilha.append(i)
            break
    
    while pilha:
        # pega o último elemento da pilha
        v = pilha[-1]
        
        if vertices[v]["lista_adjacencia"]:
            # ordena para ficar na ordem lexográfica
            vertices[v]["lista_adjacencia"].sort()
            # remove o vértice adjacente de menor valor e o adiciona na pilha
            u = vertices[v]["lista_adjacencia"].pop(0)
            vertices[u]["lista_adjacencia"].remove(v)
            pilha.append(u)
        else:
            # se não possui mais arestas não percorridas, adiciona na trilha
            trilha.append(pilha.pop())

    # retorna na ordem
    return trilha[::-1]


# Testing thiz shit
#print(f"Conexo: {verify_conexo(quantidade_vertices, vertices)}") 
print(f"Possui ciclo: {verify_cycle(vertices)}")
#print(f"Bipartido: {verify_bipartido(quantidade_vertices, vertices)}")
print(f"Euleriano: {is_euleriano(vertices)}")
print(f"Pontes: {detecta_pontes(vertices)}")
#print(f"Vértices de articulação: {list_articula(vertices)}")
