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
    if not is_direcionado:
        return _kruskal_minTree_neg(quantidade_vertices, adj_list)
    else:
        return _bellman_ford_minTree(quantidade_vertices, adj_list, 0)  # Raiz assumida como o vértice 0

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

    min_tree = []
    for weight, u, v in edges:
        if find(u) != find(v):
            union(u, v)
            min_tree.append((u, v, weight))

    return min_tree

# Função interna para Bellman-Ford (grafos direcionados com pesos negativos)
def _bellman_ford_minTree(quantidade_vertices, adj_list, root):
    distances = [float('inf')] * quantidade_vertices
    pred = [-1] * quantidade_vertices
    distances[root] = 0

    for _ in range(quantidade_vertices - 1):
        for u in range(quantidade_vertices):
            for v, weight in adj_list[u]:
                if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
                    pred[v] = u

    for u in range(quantidade_vertices):
        for v, weight in adj_list[u]:
            if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                raise ValueError("Grafo contém ciclo negativo.")

    min_tree = []
    for v in range(quantidade_vertices):
        if v != root and pred[v] != -1:
            min_tree.append((pred[v], v, distances[v] - distances[pred[v]]))

    return min_tree

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
    
    return list(articulation_points)                    # Retornar a lista de pontos de articulação encontrados

# Leitura inicial do grafo
arestas_vertices = input().split()                      # Leitura do número de vértices e arestas
quantidade_vertices = int(arestas_vertices[0])
quantidade_arestas = int(arestas_vertices[1])

# Leitura do tipo de grafo
is_direcionado = input().strip()

if is_direcionado == "nao_direcionado":
    is_direcionado = False
elif is_direcionado == "direcionado":
    is_direcionado = True
else:
    raise ValueError("Tipo de grafo inválido")

vertices = [[] for _ in range(quantidade_vertices)]                # Inicialização da lista de adjacências original
vertices_with_weights = [[] for _ in range(quantidade_vertices)]   # Lista de adjacências com pesos para minTree

# Leitura das arestas
for _ in range(quantidade_arestas):
    aresta = input().strip().split()
    id_aresta = int(aresta[0])                          # ID da aresta (não utilizado no momento)
    ligacao_v1 = int(aresta[1])
    ligacao_v2 = int(aresta[2])
    peso = int(aresta[3])                               # Peso da aresta
    
    # Adicionar a aresta ao grafo no formato original (apenas vértices)
    vertices[ligacao_v1].append(ligacao_v2)
    if not is_direcionado:
        vertices[ligacao_v2].append(ligacao_v1)
    
    # Adicionar a aresta ao grafo no formato com pesos (vértice, peso)
    vertices_with_weights[ligacao_v1].append((ligacao_v2, peso))
    if not is_direcionado:
        vertices_with_weights[ligacao_v2].append((ligacao_v1, peso))

# Verificar se o grafo é conexo
if verify_conexo(vertices, quantidade_vertices):
    print("O grafo é conexo.")
else:
    print("O grafo não é conexo.")

# Verificar se o grafo é bipartido
if verify_bipartido(quantidade_vertices, vertices):
    print("O grafo é bipartido.")
else:
    print("O grafo não é bipartido.")

# Encontrar e imprimir os vértices de articulação
articulations = list_joints(vertices, quantidade_vertices)
print("Vértices de articulação:", articulations)

# Gerar e imprimir a árvore mínima usando a nova estrutura com pesos
min_tree = minTree(quantidade_vertices, vertices_with_weights, is_direcionado)
print("Árvore mínima:", min_tree)