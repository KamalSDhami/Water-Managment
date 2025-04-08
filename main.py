class Graph:
    def __init__(self):
        self.graph = {}  # node: [(neighbor, distance)]

    def add_edge(self, u, v, w):
        if u not in self.graph:
            self.graph[u] = []
        if v not in self.graph:
            self.graph[v] = []
        self.graph[u].append((v, w))
        self.graph[v].append((u, w))  # undirected edge

    def display(self):
        for node in self.graph:
            print(f"{node} -> {self.graph[node]}")
g = Graph()

# Adding edges (pipes with distances)
g.add_edge("Source", "House1", 4)
g.add_edge("Source", "House2", 6)
g.add_edge("House1", "House2", 2)
g.add_edge("House2", "House3", 3)
g.add_edge("House3", "House4", 5)

# Display the graph
g.display()

