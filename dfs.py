import copy # Para copiar Estruturas mutáveis

arestas_vertices = input().split()

quantidade_vertices = int(arestas_vertices[0])
quantidade_arestas = int(arestas_vertices[1])

is_direcionado = input()

if( is_direcionado == "nao_direcionado"):
    is_direcionado = False
if(is_direcionado == "direcionado"):
    is_direcionado = True


lista_adjacencia = [[] for _ in range(quantidade_vertices)] # Colocando todas as listas de adjacência dos vertices como vazia


# Colocando, para cada vértice, graus de entrada e saída como zero

grau_entrada = [0 for _ in range(quantidade_vertices)] 
grau_saida = [0 for _ in range(quantidade_vertices)]

arestas = list()

# Lê todas as arestas dadas no terminal
for x in range(quantidade_arestas):
    arestas.append(input())


#   Criação da lista de adjacência
#   O index de lista_adjacência representa cada vertice
for aresta in arestas:
    aresta = aresta.split()
    ligacao_v1 = int(aresta[1])
    ligacao_v2 = int(aresta[2])
    lista_adjacencia[ligacao_v1].append(ligacao_v2)
    grau_saida[ligacao_v1] += 1
    grau_entrada[ligacao_v2] += 1
    if(not is_direcionado): # se o Grafo for não direcionado quer dizer que a ligação ocorre bidirecionalmente
        lista_adjacencia[ligacao_v2].append(ligacao_v1)


matriz_adjacencia = [[] for _ in range(quantidade_vertices)] # Colocando todas as linhas da matriz como vazias

# Colocando todas linhas da matriz com valor 0
for linha in matriz_adjacencia:
    for x in range(quantidade_vertices): 
        linha.append(0)



# Colocando elementos da matriz de adjacência
for aresta in arestas:
    aresta = aresta.split()
    ligacao_v1 = int(aresta[1])
    ligacao_v2 = int(aresta[2])
    peso = int(aresta[3])
    matriz_adjacencia[ligacao_v1][ligacao_v2] = peso
    if(not is_direcionado): # Mesma lógica da lista de Adjacência
        matriz_adjacencia[ligacao_v2][ligacao_v1] = peso


def is_euleriano(lista_adjacencia):

    #if(not verify_conexo(quantidade_vertices,vertices)):
        #return False

    for i in range(len(lista_adjacencia)):
        if(len(lista_adjacencia[i]) % 2 != 0): # Verifica se o grau do vértice é par
            return False # caso o de um não seja, a função já retorna falso
    
    return True # Caso todos sejam, retorna True



vertices = list()

for i in range(quantidade_vertices):
    vertices.append({"vertice":i,"cor": "branco", "filho": None, "tf":0, "ti":0, "lista_adjacencia": copy.deepcopy(lista_adjacencia[i])})



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
            tempo = dfsVisita(vertice,tempo)

def dfsOrdTop(vertices):
    #if((not is_direcionado) and (not verify_cycle(vertices))):
        #return []
    tempo = 0
    for key,vertice in enumerate(vertices):
        if (vertice["cor"] == "branco") and (grau_entrada[key] == 0): #verifica se não tem arestas chegando
            tempo = dfsVisita(vertice,tempo)
    ordenacao = sorted(vertices, key=lambda vertice: vertice["tf"],reverse=True)
    ordenacao_topologica = [x["vertice"] for x in ordenacao]
    return ordenacao_topologica


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
            componentes.append([]) # Para cada rodada do DFS cria um componente
            dfsConexoVisita(vertice,tempo,componentes[chave])
            chave += 1
    return componentes


componentes = list()

def dfsFortementeConexo(vertices):
    tempo = 0
    dfs(vertices)
    lista_adjacencia_invertida = [[] for _ in range(quantidade_vertices)]
    for aresta in arestas:
        aresta = aresta.split()
        ligacao_v1 = int(aresta[1]) 
        ligacao_v2 = int(aresta[2])
        lista_adjacencia_invertida[ligacao_v2].append(ligacao_v1)
    for i,vertice in enumerate(vertices):
        vertice["cor"] = "branco"
        vertice["lista_adjacencia"] = lista_adjacencia_invertida[i]
    

    vertices = sorted(vertices, key=lambda vertice: vertice["tf"],reverse=True)
    chave = 0
    for vertice in vertices:
        if vertice["cor"] == "branco":
            componentes.append([]) # Para cada rodada do DFS cria um componente
            tempo = dfsConexoVisita(vertice,tempo,componentes[chave])
            chave += 1



componentes = list()

def dfsVisitaFecho(vertice,tempo):
    tempo += 1
    vertice["ti"] = tempo
    vertice["cor"] = "cinza"
    for vizinho in vertice["lista_adjacencia"]:
        if vertices[vizinho]["cor"] == "branco":
            componentes.append(vertices[vizinho]["vertice"])
            vertice["filho"] = vizinho
            tempo = dfsVisitaFecho(vertices[vizinho],tempo);
    vertice["cor"] = "preto"
    tempo += 1
    vertice["tf"] = tempo

    return tempo

def dfsFecho(vertices):
    tempo = 0
    tempo = dfsVisitaFecho(vertices[0],tempo)



dfsFecho(vertices)
    

print(componentes)


























