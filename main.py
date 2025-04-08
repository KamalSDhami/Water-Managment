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
from collections import deque

from collections import deque
import time

def simulate_water_flow_extended(graph, start_node, max_pressure=100, drop_rate=5, sleep=False):
    visited = set()
    queue = deque([(start_node, 0, max_pressure)])  # (node, time, pressure)
    flow_data = []

    print("🚿 Starting Water Flow Simulation...\n")

    while queue:
        current, time_taken, pressure = queue.popleft()
        if current in visited:
            continue

        visited.add(current)
        flow_data.append((current, time_taken, pressure))

        # Simulate real-time
        if sleep:
            time.sleep(0.5)

        print(f"💧 {current}: Time = {time_taken} units | Pressure = {pressure:.2f}")

        # Pressure Alert
        if pressure < 30:
            print(f"⚠️ ALERT: Low water pressure at {current} ({pressure:.2f})")

        for neighbor, distance in graph.graph[current]:
            if neighbor not in visited:
                next_time = time_taken + distance
                next_pressure = pressure - (distance * drop_rate)
                queue.append((neighbor, next_time, max(next_pressure, 0)))  # Avoid negative pressure

    return flow_data
import matplotlib.pyplot as plt

def visualize_water_pressure(flow_data):
    houses = [node for node, _, _ in flow_data]
    times = [time for _, time, _ in flow_data]
    pressures = [pressure for _, _, pressure in flow_data]

    # Line Graph
    plt.figure(figsize=(10, 5))
    plt.plot(times, pressures, marker='o', linestyle='-', color='blue')
    for i, house in enumerate(houses):
        plt.text(times[i], pressures[i], house, fontsize=9, ha='center', va='bottom')
    
    plt.title("💧 Water Pressure vs Time")
    plt.xlabel("Time (units)")
    plt.ylabel("Pressure")
    plt.grid(True)
    plt.show()
#otpional 
import networkx as nx

def draw_graph(graph_obj):
    G = nx.Graph()
    for node in graph_obj.graph:
        for neighbor, weight in graph_obj.graph[node]:
            G.add_edge(node, neighbor, weight=weight)

    pos = nx.spring_layout(G, seed=42)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=1200, font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title("🏠 Water Pipe Network")
    plt.show()
def detect_anomalies(flow_data, drop_threshold=40):
    anomalies = []
    for i in range(1, len(flow_data)):
        prev_pressure = flow_data[i-1][2]
        current_node, _, curr_pressure = flow_data[i]
        drop_percent = ((prev_pressure - curr_pressure) / prev_pressure) * 100

        if drop_percent > drop_threshold:
            print(f"🚨 Anomaly Detected at {current_node}: Pressure drop of {drop_percent:.2f}%")
            anomalies.append((current_node, drop_percent))

    return anomalies
import csv

def save_flow_to_csv(flow_data, filename="water_flow_log.csv"):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["House", "Time", "Pressure"])
        writer.writerows(flow_data)
    print(f"✅ Data saved to {filename}")
def simulation_summary(flow_data, anomalies):
    print("\n📋 Simulation Summary:")
    print(f"Total Houses Reached: {len(flow_data)}")
    print(f"Anomalies Detected: {len(anomalies)}")
    if anomalies:
        print("Suggested Checks:")
        for node, drop in anomalies:
            print(f"🔧 Check pipes near {node} (drop = {drop:.2f}%)")

def suggest_repairs(anomalies):
    print("\n🛠️ Auto Repair Suggestion:")
    for node, drop in anomalies:
        if drop > 60:
            print(f"🛠️ Critical: Replace pipe at {node}")
        else:
            print(f"🔍 Moderate: Inspect pipe at {node}")

'''
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
'''

g = Graph()
g.add_edge("Source", "House1", 2)
g.add_edge("Source", "House2", 4)
g.add_edge("House1", "House3", 3)
g.add_edge("House2", "House4", 5)
g.add_edge("House3", "House5", 4)
'''
simulate_water_flow_extended(g, "Source", max_pressure=100, drop_rate=6, sleep=True)
flow_result = simulate_water_flow_extended(g, "Source", max_pressure=100, drop_rate=6, sleep=False)
visualize_water_pressure(flow_result)

# optional 
draw_graph(g)

'''
flow_result = simulate_water_flow_extended(g, "Source", max_pressure=100, drop_rate=6, sleep=False)

draw_graph(g)
visualize_water_pressure(flow_result)

anomalies = detect_anomalies(flow_result)
save_flow_to_csv(flow_result)
simulation_summary(flow_result, anomalies)
suggest_repairs(anomalies)

