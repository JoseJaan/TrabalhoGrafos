arestas_vertices = input()

quantidade_vertices = int(arestas_vertices[0])
quantidade_arestas = int(arestas_vertices[2])

is_direcionado = input()

if( is_direcionado == "nao_direcionado"):
    is_direcionado = False
if(is_direcionado == "direcionado"):
    is_direcionado = True

vertices = [[] for _ in range(quantidade_vertices)]

arestas = list()

for x in range(quantidade_arestas):
    arestas.append(input())


for aresta in arestas:
    ligacao_v1 = int(aresta[2])
    ligacao_v2 = int(aresta[4])
    vertices[ligacao_v1].append(ligacao_v2)
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
        matriz_adjacencia[ligacao_v2][ligacao_v1] = peso


def dfs(v, visitados, vertices):                            # Função DFS padrão, poderíamos adicionar uma callback de parâmetro
    visitados[v] = True                                     #  def dfs(v, visitados, vertices, callback = none) já que funções 
    for vizinho in vertices[v]:                             # futuras podem precisar -> acredito eu         
        if not visitados[vizinho]:
            dfs(vizinho, visitados, vertices)
            
def bfs(v, visitados, vertices):                            # Função BFS padronizada, também pode aceitar um callback, caso necessário
    fila = [v]  
    visitados[v] = True
    
    while fila:
        atual = fila.pop(0)
        
        for vizinho in vertices[atual]:
            if not visitados[vizinho]:
                visitados[vizinho] = True
                fila.append(vizinho)

def verify_conexo(quantidade_vertices, vertices):
    visitados = [False] * (quantidade_vertices + 1)         # Starta os visitados para usar a DFS

    for v in range(1, quantidade_vertices + 1):             # Achar o primeiro vértice que tenha arestas
        if len(vertices[v]) > 0:
            primeiro_vertice = v
            break
    else:                                                   # Caso não existam arestas o grafo não tem como ser conexo, retornando False
        return False    

    dfs(primeiro_vertice, visitados, vertices)              # Chamada da DFS com os params obtidos acima
    for v in range(0, quantidade_vertices):           
        if len(vertices[v]) >= 0 and not visitados[v]:       # Garante que não temos nenhum grafo com arestas que não foi verificado
            return False                                    # Double check de cria

    return True                                             # Retorna que o grafo é conexo

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

def verify_bipartido(quantidade_vertices, vertices):        # teoria -> grafo bipartido é um conjunto de vértices em que o grupo V não se                   
                                                            # conecta com o grupo U, usando cores para diferenciar os mesmos     cores:   U -> 0  V -> 1
    
    cores = [-1] * (quantidade_vertices + 1)                # -1 é a ausência de cor, deixando os vértices marcados como não coloridos
    
    for i in range(1, quantidade_vertices + 1):             # percorre todo mundo até achar um -1 com arestas
        if cores[i] == -1 and len(vertices[i]) > 0:         
            fila = [i]
            cores[i] = 0                                    # começa a colorir com 0
            
            while fila:                                     # enquanto houver algo na fila mantendo-a 'true'
                u = fila.pop(0)                             # vai tirando um vértice dela com o pop
                
                for v in vertices[u]:
                    if cores[v] == -1:                      # se o vértice não foi colorido
                        cores[v] = 1 - cores[u]             # colore com a cor oposta de U transformando ele em V
                        fila.append(v)
                    elif cores[v] == cores[u]:              # se o vértice adjacente tem a mesma cor o grafo não é bipartido
                        return False
    return True

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

def dfs_articulacao(v, visitados, low, disc, pai, articulacoes, tempo):
    filhos = 0                                                                   # Inicializa o número de filhos do vértice atual
    visitados[v] = True                                                          # Marca o vértice como visitado
    disc[v] = low[v] = tempo[0]                                                  # Define o tempo de descoberta e o valor low para o vértice atual
    tempo[0] += 1                                                                # Incrementa o tempo global

    for vizinho in vertices[v]:                                                  # Percorre todos os vértices adjacentes ao vértice atual
        if not visitados[vizinho]:                                               # Se o vizinho ainda não foi visitado
            filhos += 1                                                          # Incrementa o contador de filhos
            dfs_articulacao(vizinho, visitados, low, disc, v, articulacoes, tempo)  # Realiza a chamada recursiva para o vizinho
            low[v] = min(low[v], low[vizinho])                                   # Atualiza o valor low do vértice atual
            if pai is None and filhos > 1:                                       # Se o vértice atual é a raiz e tem mais de um filho, é uma articulação
                articulacoes.add(v)
            if pai is not None and low[vizinho] >= disc[v]:                      # Se o vértice atual não é a raiz e o valor low do vizinho é maior ou igual ao tempo de descoberta do vértice atual
                articulacoes.add(v)
        elif vizinho != pai:                                                     # Se o vizinho não é o pai do vértice atual
            low[v] = min(low[v], disc[vizinho])                                  # Atualiza o valor low do vértice atual

def list_articula(vertices):
    quantidade_vertices = len(vertices) - 1                                      # Obtém a quantidade de vértices no grafo
    visitados = [False] * (quantidade_vertices + 1)                              # Inicializa a lista de visitados
    disc = [float('inf')] * (quantidade_vertices + 1)                            # Inicializa a lista de tempos de descoberta
    low = [float('inf')] * (quantidade_vertices + 1)                             # Inicializa a lista de valores low
    articulacoes = set()                                                         # Inicializa o conjunto de articulações
    tempo = [0]                                                                  # Inicializa o tempo global
    
    for i in range(1, quantidade_vertices + 1):                                  # Percorre todos os vértices do grafo
        if not visitados[i]:                                                     # Se o vértice ainda não foi visitado
            dfs_articulacao(i, visitados, low, disc, None, articulacoes, tempo)  # Realiza a DFS para encontrar articulações
    
    return sorted(list(articulacoes))    

print(vertices)                                        # Retorna a lista de articulações ordenada

# Testing thiz shit
print(f"Conexo: {verify_conexo(quantidade_vertices, vertices)}") 
print(f"Possui ciclo: {verify_cycle(vertices)}")
print(f"Bipartido: {verify_bipartido(quantidade_vertices, vertices)}")
print(f"Euleriano: {is_euleriano(vertices)}")
print(f"Pontes: {detecta_pontes(vertices)}")
print(f"Vértices de articulação: {list_articula(vertices)}")
