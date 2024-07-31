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
            
            


