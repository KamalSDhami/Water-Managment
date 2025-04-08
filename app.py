import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tools import detect_anomalies, visualize_water_pressure, draw_graph, simulate_water_flow_extended
import csv
import datetime
import heapq

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import mplcursors
import numpy as np
import os
from tkinter import filedialog

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
        
        #Csv save button
        self.save_button = ttk.Button(self.root, text="💾 Save Results to CSV", command=self.save_to_csv)
        self.save_button.pack(pady=5)   

        #button for future ml prediction
        self.ml_button = ttk.Button(self.root, text="🤖 Predict Future Pressure (Coming Soon)", state='disabled')
        self.ml_button.pack(pady=5)

        #Add Check Anomalies button
        self.anomaly_button = ttk.Button(self.root, text="⚠️ Check Anomalies", command=self.show_anomalies)
        self.anomaly_button.pack(pady=5)



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
        
    # def show_graphs(self):
    #     if not self.flow_result:
    #         messagebox.showwarning("⚠️", "Run simulation first.")
    #         return
        
    #     visualize_water_pressure(self.flow_result)
    #     draw_graph(self.graph)

    # def show_graphs(self):
    #     if not self.flow_result:
    #         messagebox.showwarning("⚠️", "Run simulation first.")
    #         return

    #     # Get anomaly nodes
    #     anomalies = self.detect_anomalies()
    #     anomaly_nodes = [node for node, _ in anomalies]

    #     # Extract values
    #     nodes = [n for n, _, _ in self.flow_result]
    #     times = [t for _, t, _ in self.flow_result]
    #     pressures = [p for _, _, p in self.flow_result]

    #     # Create Plot
    #     fig, ax = plt.subplots(figsize=(10, 6))
    #     ax.plot(nodes, times, marker='o', label='Time to Reach Node (s)', color='blue')
    #     ax.plot(nodes, pressures, marker='x', label='Water Pressure', color='green')

    #     # 🔴 Mark anomaly points
    #     for node, pressure in anomalies:
    #         ax.plot(node, pressure, 'ro', markersize=10, label='Anomaly' if node == anomaly_nodes[0] else "")

    #     ax.set_title("💧 Water Flow Visualization with Anomalies")
    #     ax.set_xlabel("Node")
    #     ax.set_ylabel("Value")
    #     ax.grid(True)
    #     ax.legend()

    #     plt.tight_layout()
    #     plt.show()

    def show_graphs(self):
        if not self.flow_result:
            messagebox.showwarning("⚠️", "Run simulation first.")
            return

        # Get anomaly nodes
        anomalies = self.detect_anomalies()
        anomaly_nodes = [node for node, _ in anomalies]

        # Extract values
        nodes = [n for n, _, _ in self.flow_result]
        times = [t for _, t, _ in self.flow_result]
        pressures = [p for _, _, p in self.flow_result]

        # Create Plot
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(nodes, times, marker='o', label='Time to Reach Node (s)', color='blue')
        ax.plot(nodes, pressures, marker='x', label='Water Pressure', color='green')

        # 🔴 Mark anomaly points with red star
        for idx, (node, pressure) in enumerate(anomalies):
            ax.plot(node, pressure, 'r*', markersize=12, label='Anomaly' if idx == 0 else "")

        ax.set_title("💧 Water Flow Visualization with Anomalies")
        ax.set_xlabel("Node")
        ax.set_ylabel("Value")
        ax.grid(True)
        ax.legend()

        plt.tight_layout()
        plt.show()

        # ✅ Ask to export
        export = messagebox.askyesno("📤 Export", "Do you want to save this graph?")
        if export:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG File", "*.png"), ("PDF File", "*.pdf")],
                initialfile="water_flow_graph"
            )
            if file_path:
                fig.savefig(file_path)
                messagebox.showinfo("✅ Saved", f"Graph saved to:\n{file_path}")


    def save_to_csv(self):
        if not self.flow_result:
            messagebox.showwarning("⚠️", "Run simulation first.")
            return

        filename = f"flow_result_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        try:
            with open(filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Node", "Time", "Pressure"])
                for row in self.flow_result:
                    writer.writerow(row)
            messagebox.showinfo("✅ Success", f"Results saved to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save CSV: {e}")
    def detect_anomalies(self):
        anomalies = []
        pressures = [p for _, _, p in self.flow_result]
        avg_pressure = sum(pressures) / len(pressures)
        threshold = avg_pressure * 0.4  # 40% drop is considered anomaly

        for node, time, pressure in self.flow_result:
            if pressure < threshold:
                anomalies.append((node, pressure))
        
        return anomalies
    def show_anomalies(self):
        anomalies = self.detect_anomalies()
        if not anomalies:
            messagebox.showinfo("✅ All Good", "No anomalies detected in pressure levels.")
        else:
            alert_msg = "\n".join([f"Node {node}: Pressure = {pressure}" for node, pressure in anomalies])
            messagebox.showwarning("⚠️ Anomalies Detected", alert_msg)




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
