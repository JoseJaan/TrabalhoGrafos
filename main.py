import time
from src.scripts.verifyGraph import Graph as verifyGraph
from src.scripts.measureTime import measure_time
from src.scripts.verifyGraph import Graph as visualizeGraph
from src.scripts.listGraph import Graph as listGraph
from file_reader import read_graph_from_file

def main():
    file_path = input("Digite o caminho do arquivo do grafo: ")
    graph = read_graph_from_file(file_path)
    if graph is None:
        return

    menu = """
    1. Verificar
        a. Quantidade de vértices
        b. Quantidade de arestas
        c. Conexo
        d. Bipartido
        e. Euleriano
        f. Hamiltoniano
        g. Cíclico
        h. Planar
    2. Listar
        a. Vértices
        b. Arestas
        c. Componentes conexas
        d. Um caminho Euleriano
        e. Um caminho Hamiltoniano
        f. Vértices de articulação
        g. Arestas ponte
    3. Gerar
        a. Matriz de adjacência
        b. Lista de adjacência
        c. Árvore de profundidade
        d. Árvore de largura
        e. Árvore geradora mínima
        f. Ordem topológia (Esta função não fica disponível em grafos não direcionado)
        g. Caminho mínimo entre dois vértices (Esta função não fica disponível em grafos não ponderados)
        h. Fluxo máximo (Esta função não fica disponível em grafos não ponderados)
        i. Fechamento transitivo (Esta função não fica disponível em grafos não ponderados)
    """

    while True:
        print(menu)
        choice = input("Escolha uma opção: ")

        if choice == '1a':
            print(f"Quantidade de vértices: {verifyGraph.num_vertices()}")
        elif choice == '1b':
            print(f"Quantidade de arestas: {verifyGraph.num_edges()}")
        elif choice == '1c':
            print(f"Conexo: {verifyGraph.is_connected()}")
        elif choice == '1d':
            print(f"Bipartido: {verifyGraph.is_bipartite()}")
        elif choice == '1e':
            print(f"Euleriano: {verifyGraph.is_eulerian()}")
        elif choice == '1f':
            print(f"Hamiltoniano: {verifyGraph.is_hamiltonian()}")
        elif choice == '1g':
            print(f"Cíclico: {verifyGraph.is_cyclic()}")
        elif choice == '1h':
            print(f"Planar: {verifyGraph.is_planar()}")
        elif choice == '2a':
            print(f"Vértices: {listGraph.list_vertices()}")
        elif choice == '2b':
            print(f"Arestas: {listGraph.list_edges()}")
        elif choice == '2c':
            print(f"Componentes conexos: {listGraph.connected_components()}")
        elif choice == '2d':
            print(f"Caminho Euleriano: {listGraph.find_eulerian_path()}") 
        elif choice == '2e':
            print(f"Caminho Hamiltoniano: {listGraph.find_hamiltonian_path()}")
        elif choice == '2f':
            print(f"Vértices de articulação: {listGraph.articulation_points()}")
        elif choice == '2g':
            print(f"Arestas ponte: {listGraph.bridges()}")
        elif choice == '3a':
            print(f"Matriz de adjacência: {visualizeGraph.adjacency_matrix()}")
        elif choice == '3b':
            print(f"Lista de adjacência: {visualizeGraph.adjacency_list()}")
        elif choice == '3c':
            print(f"Árvore de profundidade: {visualizeGraph.depth_first_tree()}")
        elif choice == '3d':
            print(f"Árvore de largura: {visualizeGraph.breadth_first_tree()}")
        elif choice == '3e':
            print(f"Árvore geradora mínima: {visualizeGraph.minimum_spanning_tree()}")
        elif choice == '3f':
            try:
                print(f"Ordem topológica: {visualizeGraph.topological_sort()}")
            except ValueError as e:
                print(e)
        elif choice == '3g':
            source = input("Digite o vértice de origem: ")
            target = input("Digite o vértice de destino: ")
            print(f"Caminho mínimo: {visualizeGraph.shortest_path(source, target)}")
        elif choice == '3h':
            source = input("Digite o vértice de origem: ")
            target = input("Digite o vértice de destino: ")
            print(f"Fluxo máximo: {visualizeGraph.max_flow(source, target)}")
        elif choice == '3i':
            print(f"Fechamento transitivo: {visualizeGraph.transitive_closure()}")
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
