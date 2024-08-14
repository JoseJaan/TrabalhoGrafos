import copy # Para copiar Estruturas mutáveis

funcoes = input().split()

arestas_vertices = input().split()

quantidade_vertices = int(arestas_vertices[0])
quantidade_arestas = int(arestas_vertices[1])

is_direcionado = input()

if( is_direcionado == "nao_direcionado"):
    is_direcionado = False
if(is_direcionado == "direcionado"):
    is_direcionado = True

lista_adjacencia = [[] for _ in range(quantidade_vertices)] # Colocando todas as listas de adjacência dos vertices como vazia
lista_adjacencia_with_weights = [[] for _ in range(quantidade_vertices)]   # Lista de adjacências com pesos para minTree

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
    peso = int(aresta[3]) 
    lista_adjacencia[ligacao_v1].append(ligacao_v2)
    grau_saida[ligacao_v1] += 1
    grau_entrada[ligacao_v2] += 1
    if(not is_direcionado): # se o Grafo for não direcionado quer dizer que a ligação ocorre bidirecionalmente
        lista_adjacencia[ligacao_v2].append(ligacao_v1)

    lista_adjacencia_with_weights[ligacao_v1].append((ligacao_v2, peso))
    if not is_direcionado:
        lista_adjacencia_with_weights[ligacao_v2].append((ligacao_v1, peso))

# Função que realiza a busca em profundidade para verificar se o grafo é bipartido
def dfs_bipartido(v, cores, adj_list):
    stack = [(v, 0)]                                    # Pilha de vertices com cores. Inicia com o vértice 'v' com cor 0.
    while stack:
        node, cor_atual = stack.pop()                   # Remove um vértice da pilha
        if cores[node] == -1:                           # Se o vértice ainda não foi colorido
            cores[node] = cor_atual                     # Colorir o vértice com a cor atual
        elif cores[node] != cor_atual:                  # Se o vértice já foi colorido com uma cor diferente
            return False                                # O grafo não é bipartido, pois há uma inconsistência

                                                        # Explorar todos os vizinhos do vértice atual
        for neighbor in adj_list[node]:
            if cores[neighbor] == -1:                   # Se o vizinho ainda não foi colorido
                stack.append((neighbor, 1 - cor_atual)) # Adicionar o vizinho à pilha com a cor oposta
            elif cores[neighbor] == cor_atual:          # Se o vizinho tem a mesma cor que o vértice atual
                return False                            # O grafo não é bipartido
    return True                                         # O grafo é bipartido

# Função para verificar se o grafo é bipartido
def verify_bipartido(quantidade_vertices, adj_list):
    cores = [-1] * quantidade_vertices                  # Inicialmente, todos os vértices são não coloridos (representados por -1)
    
    for i in range(quantidade_vertices):
        if cores[i] == -1 and len(adj_list[i]) > 0:      # Se o vértice ainda não foi colorido e tem arestas
            fila = [i]                                   # Iniciar a busca em largura a partir deste vértice
            cores[i] = 0                                 # Colorir o vértice inicial com a cor 0
            
            while fila:                                  # Enquanto houver vértices na fila
                u = fila.pop(0)                          # Remover um vértice da fila
                
                for v in adj_list[u]:                    # Explorar todos os vizinhos de 'u'
                    if cores[v] == -1:                   # Se o vizinho ainda não foi colorido
                        cores[v] = 1 - cores[u]          # Colorir o vizinho com a cor oposta
                        fila.append(v)                   # Adicionar o vizinho à fila
                    elif cores[v] == cores[u]:           # Se o vizinho tem a mesma cor que 'u'
                        return False                     # O grafo não é bipartido
    return True                                          # O grafo é bipartido

# Função DFS para encontrar vértices de articulação
def dfs_conexo(v, visited, adj_list):
    stack = [v]                                          # Pilha para a busca em profundidade, iniciando com o vértice 'v'
    while stack:
        node = stack.pop()                               # Remove um vértice da pilha
        if not visited[node]:                            # Se o vértice ainda não foi visitado
            visited[node] = True                         # Marcar o vértice como visitado
            for neighbor in adj_list[node]:              # Explorar todos os vizinhos do vértice atual
                if not visited[neighbor]:                # Se o vizinho ainda não foi visitado
                    stack.append(neighbor)               # Adicionar o vizinho à pilha

# Função para verificar se o grafo é conexo
def verify_conexo(adj_list, quantidade_vertices):
    visited = [False] * quantidade_vertices              # Inicialmente, todos os vértices são não visitados
                                                         # Iniciar a DFS a partir do vértice 0
    dfs_conexo(0, visited, adj_list)
                                                         # Verificar se todos os vértices foram visitados
    return all(visited)                                  # Retorna True se todos os vértices foram visitados, indicando que o grafo é conexo

# Função para encontrar a árvore mínima
def minTree(quantidade_vertices, adj_list, is_direcionado):
    if is_direcionado:
        return -1  # Retorna -1 para grafos direcionados
    else:
        return _kruskal_minTree_neg(quantidade_vertices, adj_list)

# Função interna para Kruskal modificado (grafos não direcionados com pesos negativos)
def _kruskal_minTree_neg(quantidade_vertices, adj_list):
    parent = list(range(quantidade_vertices))
    rank = [0] * quantidade_vertices

    def find(v):
        if parent[v] != v:
            parent[v] = find(parent[v])
        return parent[v]

    def union(v1, v2):
        root1 = find(v1)
        root2 = find(v2)
        if root1 != root2:
            if rank[root1] > rank[root2]:
                parent[root2] = root1
            elif rank[root1] < rank[root2]:
                parent[root1] = root2
            else:
                parent[root2] = root1
                rank[root1] += 1

    edges = []
    for u in range(quantidade_vertices):
        for v, weight in adj_list[u]:
            edges.append((weight, u, v))

    edges.sort()

    min_tree_weight = 0  # Variável para armazenar a soma dos pesos da árvore mínima
    for weight, u, v in edges:
        if find(u) != find(v):
            union(u, v)
            min_tree_weight += weight

    return min_tree_weight  # Retorna a soma dos pesos da árvore mínima

# Função DFS para encontrar vértices de articulação
def dfs_joints(u, parent, visited, discovery, low, articulation_points, time, adj_list):
    children = 0                                        # Contador para o número de filhos do vértice 'u'
    visited[u] = True                                   # Marcar o vértice 'u' como visitado
    discovery[u] = low[u] = time                        # Definir o tempo de descoberta e o valor baixo para 'u'
    time += 1                                           # Incrementar o tempo
    
                                                        # Explorar todos os vizinhos do vértice 'u'
    for v in adj_list[u]:
        if not visited[v]:                              # Se o vizinho 'v' ainda não foi visitado
            children += 1                               # Incrementar o contador de filhos
            parent[v] = u                               # Definir o pai do vizinho 'v' como 'u'
            dfs_joints(v, parent, visited, discovery, low, articulation_points, time, adj_list)  # Chamar DFS recursiva para o vizinho 'v'
            low[u] = min(low[u], low[v])                # Atualizar o valor baixo de 'u' com base no valor baixo de 'v'
            
            # Verificar se 'u' é um ponto de articulação
            if parent[u] is None and children > 1:
                articulation_points.add(u)              # 'u' é a raiz e tem mais de um filho, é um ponto de articulação
            if parent[u] is not None and low[v] >= discovery[u]:
                articulation_points.add(u)              # 'u' não é a raiz e o valor baixo do vizinho 'v' é maior ou igual ao tempo de descoberta de 'u'
        elif v != parent[u]:                            # Se 'v' foi visitado e não é o pai de 'u'
            low[u] = min(low[u], discovery[v])          # Atualizar o valor baixo de 'u' com base no valor de descoberta de 'v'

# Função principal para listar os vértices de articulação
def list_joints(adj_list, quantidade_vertices):
    visited = [False] * quantidade_vertices             # Inicialmente, todos os vértices são não visitados
    discovery = [-1] * quantidade_vertices              # Inicialmente, todos os tempos de descoberta são -1
    low = [-1] * quantidade_vertices                    # Inicialmente, todos os valores baixos são -1
    parent = [None] * quantidade_vertices               # Inicialmente, todos os pais são None
    articulation_points = set()                         # Conjunto para armazenar os vértices de articulação
    time = 0                                            # Tempo inicial para o DFS
    
    # Para cada vértice, se ainda não foi visitado, executar a DFS
    for i in range(quantidade_vertices):
        if not visited[i]:
            dfs_joints(i, parent, visited, discovery, low, articulation_points, time, adj_list)
    
    return list(articulation_points)   

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
    for x in vertices:
        x["cor"] = "branco"
        x["filho"] = None
        x["ti"] = 0
        x["tf"] = 0
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
    for x in vertices:
        x["cor"] = "branco"
        x["filho"] = None
        x["ti"] = 0
        x["tf"] = 0
    for vertice in vertices:
        if vertice["cor"] == "branco":
            componentes.append([]) # Para cada rodada do DFS cria um componente
            dfsConexoVisita(vertice,tempo,componentes[chave])
            chave += 1
    return componentes


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
    
    for i,vertice in enumerate(vertices):
        vertice["lista_adjacencia"] = lista_adjacencia[i]


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
    for x in vertices:
        x["cor"] = "branco"
        x["filho"] = None
        x["ti"] = 0
        x["tf"] = 0
    tempo = 0
    tempo = dfsVisitaFecho(vertices[0],tempo)

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

    
    visitados = [False] * (quantidade_vertices)
    
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

                    visitados_comp = [False] * (quantidade_vertices)
                    dfs(componente[0], visitados_comp, vertices)

                    #Se algum vértice nao foi encontrado, a aresta removida é uma ponte
                    if any(not visitados_comp[u] for u in componente):
                        pontes.append(id_aresta)    
                    
                    vertices[ligacao_v1].append(ligacao_v2)
                    vertices[ligacao_v2].append(ligacao_v1)

    return pontes

for x in funcoes:
    if(x == "0"):
        print(verify_conexo(lista_adjacencia,quantidade_vertices))
    elif (x == "1"):
        print(verify_bipartido(quantidade_vertices,lista_adjacencia))
    elif (x == "2"):
        print(is_euleriano(lista_adjacencia))
    elif (x == "3"):
        print(verify_cycle(lista_adjacencia))
    elif (x == "4"):
        dfsConexo(vertices)        
        print(componentes)
        componentes.clear()
    elif (x == "5"):
        dfsFortementeConexo(vertices)        
        print(componentes)
        componentes.clear()
    elif(x == "6"):
        print(list_joints(lista_adjacencia, quantidade_vertices))
    elif(x == "7"):
        print("ta dando erro em direcionados")
        #print(detecta_pontes(lista_adjacencia))
    elif(x == "8"):
        print("nao tem")
    elif(x == "9"):
        print("nao tem")
    elif(x == "10"):
        print(minTree(quantidade_vertices, lista_adjacencia_with_weights, is_direcionado))
    elif(x == "11"):
        print(dfsOrdTop(vertices))
        componentes.clear()
    elif(x == "12"):
        print("nao tem")
    elif(x == "13"):
        print("nao tem")
    elif(x == "14"):
        dfsFecho(vertices)
        print(componentes)
        componentes.clear()
        