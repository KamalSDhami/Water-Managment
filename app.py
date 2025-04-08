import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tools import detect_anomalies, visualize_water_pressure, draw_graph, simulate_water_flow_extended


# ---- Import your water management code here ----
# from water_simulation import Graph, simulate_water_flow_extended, draw_graph, visualize_water_pressure, ...
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

class WaterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("💧 Smart Water Flow Simulator")
        self.root.geometry("800x600")
        self.graph = Graph()
        self.flow_result = []

        self.create_widgets()

    def create_widgets(self):
        # Dropdown for source node
        self.source_label = ttk.Label(self.root, text="Select Source Node:")
        self.source_label.pack(pady=5)

        self.source_var = tk.StringVar()
        self.source_dropdown = ttk.Combobox(self.root, textvariable=self.source_var)
        self.source_dropdown.pack()

        # Button to simulate
        self.sim_button = ttk.Button(self.root, text="🚀 Run Simulation", command=self.run_simulation)
        self.sim_button.pack(pady=10)

        # Output box
        self.output_text = tk.Text(self.root, height=15)
        self.output_text.pack(pady=10, fill=tk.BOTH, expand=True)

        # Visualize Buttons
        self.vis_button = ttk.Button(self.root, text="📊 Show Graphs", command=self.show_graphs)
        self.vis_button.pack()

    def update_source_dropdown(self):
        self.source_dropdown['values'] = list(self.graph.graph.keys())

    def run_simulation(self):
        source = self.source_var.get()
        if source not in self.graph.graph:
            messagebox.showerror("Error", "Please select a valid source node.")
            return

        # Simulate water flow
        self.flow_result = simulate_water_flow_extended(self.graph, source, sleep=False)
        
        # Detect anomalies & show summary
        anomalies = detect_anomalies(self.flow_result)
        summary = f"\n📋 Simulation Complete!\nTotal Houses: {len(self.flow_result)}\nAnomalies: {len(anomalies)}\n"

        self.output_text.delete(1.0, tk.END)
        for node, time, pressure in self.flow_result:
            self.output_text.insert(tk.END, f"{node} - Time: {time}, Pressure: {pressure}\n")
        self.output_text.insert(tk.END, summary)

    def show_graphs(self):
        if not self.flow_result:
            messagebox.showwarning("⚠️", "Run simulation first.")
            return
        
        visualize_water_pressure(self.flow_result)
        draw_graph(self.graph)

# -------- Run it --------
if __name__ == "__main__":
    root = tk.Tk()
    app = WaterApp(root)

    # --- Your sample graph creation here ---
    app.graph.add_edge("Source", "A", 2)
    app.graph.add_edge("A", "B", 3)
    app.graph.add_edge("A", "C", 4)
    app.graph.add_edge("B", "D", 5)
    app.graph.add_edge("C", "D", 1)
    app.graph.add_edge("D", "E", 2)
    app.update_source_dropdown()

    root.mainloop()
