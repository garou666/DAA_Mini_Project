
---

#  DAA: Safe Routing Network Simulator

```markdown
# Safe Routing Network Simulator (Dijkstra's Algorithm)

##  Project Overview
This project is an interactive GUI-based network simulator built in Python. It demonstrates the practical application of **Dijkstra's Algorithm** (Graph Theory) in cybersecurity. 

Instead of finding the shortest path based on distance, this tool calculates the **safest path** based on a "Risk Score," dynamically avoiding nodes that have been marked as "compromised" by a hacker.

##  Technologies Used
*   **Language:** Python 3.x
*   **GUI Library:** Tkinter (Canvas)
*   **Algorithm:** Dijkstra's Shortest Path (using `heapq` Priority Queue)

##  Features
1.  **Dynamic Pathfinding:** Instantly recalculates the safest route when a node is compromised.
2.  **Interactive GUI:** Click nodes to set the Source (Blue), Target (Yellow), or Compromise them (Red).
3.  **Visual Feedback:** The safest path is highlighted in Green, while blocked nodes turn Red.
4.  **Risk Analysis:** Displays the total cumulative risk score of the chosen path.

##  Installation & Usage
1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
