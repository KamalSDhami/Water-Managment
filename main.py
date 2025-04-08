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
import heapq

def prim_mst(graph, start_node):
    visited = set()
    min_heap = [(0, start_node)]  # (weight, node)
    total_cost = 0
    mst_edges = []

    while min_heap:
        weight, current = heapq.heappop(min_heap)
        if current in visited:
            continue

        visited.add(current)
        total_cost += weight

        if weight != 0:
            mst_edges.append((current, weight))

        for neighbor, w in graph.graph[current]:
            if neighbor not in visited:
                heapq.heappush(min_heap, (w, neighbor))

    return total_cost, mst_edges
g = Graph()
g.add_edge("Source", "House1", 4)
g.add_edge("Source", "House2", 6)
g.add_edge("House1", "House2", 2)
g.add_edge("House2", "House3", 3)
g.add_edge("House3", "House4", 5)

cost, connections = prim_mst(g, "Source")
print("✅ Total Pipe Length:", cost)
print("📡 Connections Used:")
for conn in connections:
    print(f"🔗 {conn[0]} via {conn[1]} units")
g.display()

