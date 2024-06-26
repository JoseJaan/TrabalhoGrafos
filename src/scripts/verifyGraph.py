class Graph:
    def __init__(self, directed=False):
        self.directed = directed
        self.vertices = set()
        self.edges = {}

    def add_edge(self, u, v, weight=1):
        if u not in self.vertices or v not in self.vertices:
            raise ValueError("Vértice inexistente.")
        if u not in self.edges:
            self.edges[u] = []
        self.edges[u].append((v, weight))
        if not self.directed:
            if v not in self.edges:
                self.edges[v] = []
            self.edges[v].append((u, weight))

    def add_vertex(self, vertex):
        self.vertices.add(vertex)
        if vertex not in self.edges:
            self.edges[vertex] = []

    def num_vertices(self):
        return len(self.vertices)

    def num_edges(self):
        return sum(len(v) for v in self.edges.values()) // (1 if self.directed else 2)

    def is_connected(self):
        # Placeholder for actual implementation
        return

    def is_bipartite(self):
        # Placeholder for actual implementation
        return

    def is_eulerian(self):
        # Placeholder for actual implementation
        return

    def is_hamiltonian(self):
        # Placeholder for actual implementation
        return

    def is_cyclic(self):
        # Placeholder for actual implementation
        return

    def is_planar(self):
        # Placeholder for actual implementation
        return
