import tkinter as tk
from tkinter import messagebox
import heapq

class SafeRoutingSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Safe Routing Network Simulator (Dijkstra)")
        self.root.geometry("950x750") # Increased window size

        # --- Network Topology Data ---
        # Adjusted coordinates to fit perfectly in the 900x500 canvas
        self.nodes = {
            'Internet': (100, 250),
            'Firewall': (300, 100),
            'Web Server': (300, 400),
            'DB Server': (500, 250),
            'Admin PC': (700, 100),
            'Target Data': (700, 400)
        }

        # Edges: (Node1, Node2, Weight) -> Weight = Security Risk Score
        self.edges = [
            ('Internet', 'Firewall', 5),
            ('Internet', 'Web Server', 10),
            ('Firewall', 'DB Server', 8),
            ('Web Server', 'DB Server', 3),
            ('DB Server', 'Admin PC', 6),
            ('DB Server', 'Target Data', 2),
            ('Firewall', 'Admin PC', 15)
        ]

        # --- State Variables ---
        self.source_node = None
        self.target_node = None
        self.compromised_nodes = set()
        self.mode = "Set Source"

        # Build Adjacency List
        self.graph = {node: [] for node in self.nodes}
        for u, v, w in self.edges:
            self.graph[u].append((v, w))
            self.graph[v].append((u, w))

        self.setup_ui()
        self.draw_network()

    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg="#2c3e50", pady=12)
        header.pack(fill=tk.X)
        tk.Label(header, text="Safe Routing Network Simulator", 
                 font=("Arial", 18, "bold"), bg="#2c3e50", fg="white").pack()

        # Control Panel
        control_frame = tk.Frame(self.root, pady=10)
        control_frame.pack()

        self.btn_source = tk.Button(control_frame, text="1. Set Source", width=15, font=("Arial", 10, "bold"),
                                    command=lambda: self.set_mode("Set Source"))
        self.btn_source.pack(side=tk.LEFT, padx=5)

        self.btn_target = tk.Button(control_frame, text="2. Set Target", width=15, font=("Arial", 10, "bold"),
                                    command=lambda: self.set_mode("Set Target"))
        self.btn_target.pack(side=tk.LEFT, padx=5)

        self.btn_compromise = tk.Button(control_frame, text="3. Compromise Node", width=18, font=("Arial", 10, "bold"),
                                        bg="#e74c3c", fg="white",
                                        command=lambda: self.set_mode("Compromise"))
        self.btn_compromise.pack(side=tk.LEFT, padx=5)

        self.btn_reset = tk.Button(control_frame, text="Reset Network", width=15, font=("Arial", 10, "bold"),
                                   command=self.reset_network)
        self.btn_reset.pack(side=tk.LEFT, padx=5)

        # Status Label
        self.status_label = tk.Label(self.root, text="Mode: Set Source | Click a node to select.", 
                                     font=("Arial", 11, "italic"), fg="#2980b9")
        self.status_label.pack(pady=5)

        # Canvas for Graph (Increased height to prevent cutting off)
        self.canvas = tk.Canvas(self.root, bg="white", width=900, height=500, highlightthickness=2, highlightbackground="grey")
        self.canvas.pack(pady=10)
        self.canvas.bind("<Button-1>", self.on_node_click)

        # Output Log
        self.output_text = tk.Text(self.root, height=6, font=("Consolas", 11), bg="#f4f4f4", padx=10, pady=10)
        self.output_text.pack(fill=tk.X, padx=40, pady=10)
        self.output_text.insert(tk.END, "System Ready. Please select a Source node.\n")

    def set_mode(self, mode):
        self.mode = mode
        self.status_label.config(text=f"Mode: {mode} | Click a node to apply.", fg="#2980b9")

    def reset_network(self):
        self.compromised_nodes.clear()
        self.source_node = None
        self.target_node = None
        self.set_mode("Set Source")
        self.draw_network()

    def on_node_click(self, event):
        # Find the closest node to the click (30px radius)
        clicked_node = None
        for node, (x, y) in self.nodes.items():
            if (x - event.x)**2 + (y - event.y)**2 <= 35**2: 
                clicked_node = node
                break

        if not clicked_node:
            return

        if self.mode == "Set Source":
            self.source_node = clicked_node
            # If source was compromised, restore it
            if clicked_node in self.compromised_nodes:
                self.compromised_nodes.remove(clicked_node)
        elif self.mode == "Set Target":
            self.target_node = clicked_node
            if clicked_node in self.compromised_nodes:
                self.compromised_nodes.remove(clicked_node)
        elif self.mode == "Compromise":
            if clicked_node == self.source_node or clicked_node == self.target_node:
                messagebox.showwarning("Warning", "Cannot compromise the active Source or Target node!")
                return
            
            if clicked_node in self.compromised_nodes:
                self.compromised_nodes.remove(clicked_node)
            else:
                self.compromised_nodes.add(clicked_node)
        
        self.draw_network()

    def dijkstra(self, start, end):
        """Dijkstra's algorithm to find the path with minimum cumulative risk."""
        pq = [(0, start, [start])]
        visited = set()
        min_risk = {node: float('inf') for node in self.nodes}
        min_risk[start] = 0

        while pq:
            risk, current, path = heapq.heappop(pq)

            if current in visited:
                continue
            visited.add(current)

            if current == end:
                return risk, path

            for neighbor, weight in self.graph[current]:
                if neighbor in self.compromised_nodes or neighbor in visited:
                    continue
                
                new_risk = risk + weight
                if new_risk < min_risk[neighbor]:
                    min_risk[neighbor] = new_risk
                    heapq.heappush(pq, (new_risk, neighbor, path + [neighbor]))

        return float('inf'), []

    def draw_network(self):
        self.canvas.delete("all")
        
        path = []
        risk = float('inf')
        
        # Only calculate path if BOTH source and target are set
        if self.source_node and self.target_node:
            risk, path = self.dijkstra(self.source_node, self.target_node)

        path_edges = set()
        if path:
            for i in range(len(path) - 1):
                path_edges.add((path[i], path[i+1]))
                path_edges.add((path[i+1], path[i]))

        # 1. Draw Edges
        for u, v, w in self.edges:
            x1, y1 = self.nodes[u]
            x2, y2 = self.nodes[v]
            
            is_path = (u, v) in path_edges
            color = "#2ecc71" if is_path else "#bdc3c7" 
            width = 5 if is_path else 2
            
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=width)
            
            # Draw weight label
            mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2
            self.canvas.create_text(mid_x, mid_y - 15, text=str(w), fill="#e67e22", font=("Arial", 11, "bold"))

        # 2. Draw Nodes
        for node, (x, y) in self.nodes.items():
            if node in self.compromised_nodes:
                color = "#e74c3c" # Red
                text_color = "white"
            elif node == self.source_node:
                color = "#3498db" # Blue
                text_color = "white"
            elif node == self.target_node:
                color = "#f1c40f" # Yellow
                text_color = "black"
            elif node in path:
                color = "#2ecc71" # Green (Path)
                text_color = "black"
            else:
                color = "#ecf0f1" # Light Grey (Normal)
                text_color = "black"

            self.canvas.create_oval(x-35, y-35, x+35, y+35, fill=color, outline="#2c3e50", width=2)
            self.canvas.create_text(x, y, text=node, font=("Arial", 9, "bold"), fill=text_color)

        # 3. Update Output Text
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, f"Source: {self.source_node if self.source_node else 'Not Selected'} | ")
        self.output_text.insert(tk.END, f"Target: {self.target_node if self.target_node else 'Not Selected'}\n")
        
        if not self.source_node or not self.target_node:
            self.output_text.insert(tk.END, "⏳ Please select both a Source (Blue) and a Target (Yellow) to find the safe route.\n")
        elif risk == float('inf'):
            self.output_text.insert(tk.END, "❌ NO SAFE PATH FOUND! Network is segmented or target is compromised.\n")
        else:
            self.output_text.insert(tk.END, f"✅ SAFE PATH FOUND! Total Risk Score: {risk}\n")
            self.output_text.insert(tk.END, f"Route: {' -> '.join(path)}\n")
            
        self.output_text.insert(tk.END, f"Compromised Nodes: {list(self.compromised_nodes) if self.compromised_nodes else 'None'}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = SafeRoutingSimulator(root)
    root.mainloop()
