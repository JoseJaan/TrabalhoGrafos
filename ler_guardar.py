with open("teste.txt",'r') as arquivo:
    entrada = arquivo.readlines()

quantidade_vertices = int(entrada[0][0])

is_direcionado = bool()
if(entrada[1] == "nao_direcionado"):
    is_direcionado = False
if(entrada[0] == "direcionado"):
    is_direcionado = True


vertices = [[] for _ in range(quantidade_vertices+1)]

arestas = entrada[2:]

for aresta in arestas:
    ligacao_v1 = int(aresta[2])
    ligacao_v2 = int(aresta[4])
    vertices[ligacao_v1].append(ligacao_v2)
    vertices[ligacao_v2].append(ligacao_v1)


matriz_adjacencia = [[] for _ in range(quantidade_vertices+1)]

for linha in matriz_adjacencia:
    for x in range(quantidade_vertices+1):
        linha.append(0)


if(not is_direcionado):
    for aresta in arestas:
        ligacao_v1 = int(aresta[2])
        ligacao_v2 = int(aresta[4])
        peso = int(aresta[6])
        matriz_adjacencia[ligacao_v1][ligacao_v2] = peso
        matriz_adjacencia[ligacao_v2][ligacao_v1] = peso


print(matriz_adjacencia)

def dfs(v, visitados, vertices):                            # Função DFS padrão, poderíamos adicionar uma callback de parâmetro
    visitados[v] = True                                     #  def dfs(v, visitados, vertices, callback = none) já que funções 
    for vizinho in vertices[v]:                             # futuras podem precisar -> acredito eu                                            -> Sim gabriel ela foi feita com GPT <-
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

    for v in range(1, quantidade_vertices + 1):             
        if len(vertices[v]) > 0 and not visitados[v]:       # Garante que não temos nenhum grafo com arestas que não foi verificado
            return False                                    # Double check de cria

    return True                                             # Retorna que o grafo é conexo


