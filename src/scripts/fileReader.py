import re
import os
from src.scripts.verifyGraph import Graph

def read_graph_from_file():
    try:
        directed_input = input("O grafo é direcionado? (sim/não): ").strip().lower()
        directed = directed_input == 'sim'

        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, 'grafo.txt')

        with open(file_path, 'r') as file:
            lines = file.readlines()

        vertices = set()
        edges = []

        for line in lines:
            line = line.strip()
            vertices_match = re.match(r'V\s*=\s*\{([a-zA-Z0-9,]+)\}', line)
            if vertices_match:
                vertices_str = vertices_match.group(1)
                vertices = set(vertices_str.split(','))
            edges_match = re.match(r'A\s*=\s*\{\(([^)]+)\)\}', line)
            if edges_match:
                edges_str = edges_match.group(1)
                edges_list = edges_str.split('),(')
                for edge_str in edges_list:
                    u, v, w = re.split(r',', edge_str)
                    edges.append((u, v, int(w)))

        graph = Graph(directed=directed)
        for vertex in vertices:
            graph.add_vertex(vertex)
        for u, v, w in edges:
            if u not in vertices or v not in vertices:
                raise ValueError(f"Aresta ({u},{v}) refere-se a vértices inexistentes.")
            graph.add_edge(u, v, w)  

        return graph

    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return None