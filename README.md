# Informatics-ITS-Graph-Theory-class-Group-6
# Group Members
| Name                     | NRP        |
| ------------------------ | ---------- |
| Lina Fatima Azzahra Badr | 5025251168 |
| Naila Sa'ada Cahyani     | 5025251258 |

---
##  A. Prim's Algorithm
Prim’s algorithm is a type of greedy algorithm for finding the minimum spanning tree (MST) of an undirected and weighted graph. A fundamental rule when determining a graph's Minimum Spanning Tree via Prim's algorithm is the prevention of cycles. Consequently, a path connecting A to B and B to C cannot be closed by a subsequent link from C back to A. Additionally, all the vertices must be involved in getting the minimum spanning tree (MST).
### Code Explanation
```python
def prims_algorithm(self):
        in_mst = [False] * self.size
        keys = [float("inf")] * self.size
        parents = [-1] * self.size
        keys[0] = 0

        for _ in range(self.size):
            # Select the vertex with the minimum key value not yet included in the MST
            available = (v for v in range(self.size) if not in_mst[v])
            u = min(available, key=lambda vertex: keys[vertex])
            if keys[u] == float("inf"):
                raise RuntimeError
            in_mst[u] = True
            print(f"Selected node {self.labels[u]} with key {keys[u]:g}")

            # Update the key and parent values of the adjacent vertices
            for v, weight in enumerate(self.adj_matrix[u]):
                if weight > 0 and not in_mst[v]:
                    print(f"  Comparing edge {self.labels[u]}-{self.labels[v]} (weight {weight:g})")
                    if weight < keys[v]:
                        print(f"    Updating node {self.labels[v]} key from {keys[v]:g} to {weight:g} via node {self.labels[u]}")
                        keys[v] = weight
                        parents[v] = u
                    else:
                        print(f"    Skipping edge {self.labels[u]}-{self.labels[v]} - current key {keys[v]:g} is smaller or equal")

        # Build and return the list of edges forming the MST
        return [
            (self.labels[parents[v]], self.labels[v], self.adj_matrix[v][parents[v]])
            for v in range(self.size)
            if parents[v] != -1
        ]
```
1. It creates three trackers: `in_mst` to mark which nodes have been added to the tree, `keys` to store the cheapest edge cost to reach each node (starting at infinity), and `parents` to remember the connections. The starting node's key is set to `0`.
2. A loop runs for every node in the graph. It scans the unvisited nodes and selects the one with the smallest `key`. If the smallest key is still infinity, it raises an error because the graph is disconnected.
3. Once a node is selected and marked as visited, the algorithm checks all its neighbors. If it finds a connecting edge to an unvisited neighbor that is cheaper than the neighbor's current `key`, it updates that `key` with the new lower weight and sets the current node as its `parent`.
4. This cycle repeats until all nodes are selected. Finally, it uses the `parents` array to return the completed list of edges forming the Minimum Spanning Tree.
### Input Format
- **Line 1:** `Node1 Node2 Node3 ...` (unique node names separated with space) 
- **Line 2:** `Total_Edges` (Number of edge lines that will follow) 
- **Line 3 to End:** `NodeX NodeY Cost` (Repeated for every edge, representing an undirected connection between Node X and Node Y with the given weight/cost)
Example:
```
Line 1: A B C D E F G
Line 2: 11
Line 3: A B 7
Line 4: A C 6
Line 5: A G 5
Line 6: B C 5
Line 7: B D 7
Line 8: C E 7
Line 9: C F 9
Line 10: D E 5
Line 11: E F 5
Line 12: F G 6
Line 13: A F 10
```

### Output Format
**1. Process Trace** Prints the algorithm's step-by-step logic:
- `Selected node X with key Y`
- `Comparing edge X-Y (weight Z)`
- `Updating node X key...` or `Skipping edge X-Y...`

**2. Final Result** Prints the final Minimum Spanning Tree:
- **Line 1:** `MST Built.`
- **Middle Lines:** `Node1-Node2 Cost` (One per edge in the MST)
- **Last Line:** `Total Weight: X`

_(If an error occurs, it prints either `Error! Cannot Build MST` or `Error! Please make sure your input is correct.` instead)._

### Result of Sample Run
![Prim's algorithm sample run](./Assets/Pasted%20image%2020260915143532.png)

---
## B. Kruskal's Algorithm
Kruskal’s algorithm is a type of greedy algorithm for finding the minimum spanning tree (MST) of an undirected and weighted graph. Unlike Prim's algorithm, which builds the tree outwards from a single starting vertex, Kruskal's algorithm focuses purely on the edges. It begins by sorting all the edges in the entire graph from the lowest weight to the highest. It then iterates through this sorted list, adding each edge to the MST one by one.

### Code Explanation
```python
def kruskal_algorithm(self):
        parent = list(range(len(self.labels)))
        rank = [0] * len(self.labels)
        result = []

        # Sort all edges 
        for u, v, weight in sorted(self.graph, key=lambda edge: edge[2]):
            print(f"Checking edge {self.labels[u]}-{self.labels[v]} with weight {weight:g}")
            if self.find(parent, u) != self.find(parent, v):
                print(f"  Adding edge {self.labels[u]}-{self.labels[v]} to MST (connects components)")
                self.union(parent, rank, u, v)
                result.append((self.labels[u], self.labels[v], weight))
            else:
                print(f"  Skipping edge {self.labels[u]}-{self.labels[v]} (creates cycle)")

        if len(result) != len(self.labels) - 1:
            raise RuntimeError
        return result
```
- It sets up the `parent` array so every node starts in its own independent cluster (pointing to itself), and sets all cluster heights (`rank`) to 0.
- Then, the algorithm sorts the entire `self.graph` edge list from the lowest weight to the highest. It then loops through this sorted list.
- For each edge, it uses the `find` method to check if the two connected nodes already share the same root.
    - If the roots are different, adding the edge is safe. It uses `union` to merge them and adds the edge to the `result` list.
    - If the roots are the same, it skips the edge because adding it would create a closed loop.
- **Completion:** After checking all edges, it verifies that the MST has exactly $N - 1$ edges (where $N$ is the number of nodes). If it doesn't, the graph was disconnected and it raises a `RuntimeError`. Otherwise, it returns the final list of edges.
### Input Format
- **Line 1:** `Node1 Node2 Node3 ...` (unique node names separated with space) 
- **Line 2:** `Total_Edges` (Number of edge lines that will follow) 
- **Line 3 to End:** `NodeX NodeY Cost` (Repeated for every edge, representing an undirected connection between Node X and Node Y with the given weight/cost)
Example:
```
Line 1: A B C D E F G
Line 2: 11
Line 3: A B 7
Line 4: A C 6
Line 5: A G 5
Line 6: B C 5
Line 7: B D 7
Line 8: C E 7
Line 9: C F 9
Line 10: D E 5
Line 11: E F 5
Line 12: F G 6
Line 13: A F 10
```
### Output Format

**1. Process Trace** Prints the algorithm's step-by-step logic:
- `Checking edge X-Y with weight Z`
- `Adding edge X-Y to MST (connects components)` or `Skipping edge X-Y (creates cycle)`

**2. Final Result** Prints the final Minimum Spanning Tree:
- **Line 1:** `MST Built.`
- **Middle Lines:** `Node1-Node2 Cost` (One per edge in the MST)
- **Last Line:** `Total Weight: X`

_(If an error occurs, it prints either `Error! Cannot Build MST` or `Error! Please make sure your input is correct.` instead)._

### Result of Sample Run
![Kruskal's algorithm sample run](./Assets/Pasted%20image%2020260915143655.png)

---
## C. Borůvka's Algorithm
Borůvka’s algorithm is a type of greedy algorithm for finding the MST of an undirected and weighted graph. Unlike Prim's (which builds outward from one node) or Kruskal's (which sorts all edges individually), Borůvka's algorithm is highly parallel and operates in 'rounds'. It starts by treating every individual node as its own separate cluster/component. In each round, it finds the cheapest outgoing edge for _every_ cluster simultaneously. Then, it adds all these cheapest edges to the MST, merging the connected clusters together into larger components. This process of finding the cheapest edges and merging clusters repeats round by round until all nodes are unified into a fully connected tree.

### Code Explanation
```python
def boruvka_algorithm(self):
        parent = list(range(len(self.labels)))
        rank = [0] * len(self.labels)
        components = len(self.labels)
        result = []

        # Continue until all components are merged into a single tree
        round_num = 1
        while components > 1:
            print(f"\n--- Round {round_num} ({components} components remain) ---")
            cheapest = [None] * len(self.labels)

            # Find the cheapest outgoing edge for every component
            for u, v, weight in self.graph:
                first = self.find(parent, u)
                second = self.find(parent, v)
                if first == second:
                    print(f"Skipping edge {self.labels[u]}-{self.labels[v]} (same component)")
                    continue
                print(f"Comparing edge {self.labels[u]}-{self.labels[v]} with weight {weight:g}")
                if cheapest[first] is None or weight < cheapest[first][2]:
                    print(f"  Updating cheapest edge for component of {self.labels[u]} to {self.labels[u]}-{self.labels[v]}")
                    cheapest[first] = (u, v, weight)
                if cheapest[second] is None or weight < cheapest[second][2]:
                    print(f"  Updating cheapest edge for component of {self.labels[v]} to {self.labels[u]}-{self.labels[v]}")
                    cheapest[second] = (u, v, weight)

            # Merge the components using the chosen cheapest edges
            merged = 0
            for edge in cheapest:
                if edge is None:
                    continue
                u, v, weight = edge
                if self.union(parent, rank, u, v):
                    print(f"Adding edge {self.labels[u]}-{self.labels[v]} to MST (weight {weight:g})")
                    result.append((self.labels[u], self.labels[v], weight))
                    components -= 1
                    merged += 1
            round_num += 1

            if merged == 0:
                raise RuntimeError

        return result
```

- Every node starts in its own individual cluster (`components = len(self.labels)`).
- The algorithm enters a `while` loop that continues as long as there is more than 1 disconnected component remaining.
- In each round, it creates an empty `cheapest` array. It loops through every edge in the entire graph. If an edge connects two different clusters, it checks if that edge is cheaper than the currently known cheapest edge for _both_ clusters. If it is, it updates the `cheapest` array for those specific clusters.
- After scanning all edges, it loops through the `cheapest` array and adds those selected edges to the MST result. It uses `union` to merge the connected clusters together, decreasing the total number of independent `components`.
- If a round finishes and absolutely no components were merged (`merged == 0`), but there is still more than 1 component left, it means the graph is disconnected and it raises a `RuntimeError`. Otherwise, it returns the final list of edges.


### Input Format
- **Line 1:** `Node1 Node2 Node3 ...` (unique node names separated with space) 
- **Line 2:** `Total_Edges` (Number of edge lines that will follow) 
- **Line 3 to End:** `NodeX NodeY Cost` (Repeated for every edge, representing an undirected connection between Node X and Node Y with the given weight/cost)
Example:
```
Line 1: A B C D E F G
Line 2: 11
Line 3: A B 7
Line 4: A C 6
Line 5: A G 5
Line 6: B C 5
Line 7: B D 7
Line 8: C E 7
Line 9: C F 9
Line 10: D E 5
Line 11: E F 5
Line 12: F G 6
Line 13: A F 10
```
### Output Format

**1. Process Trace** Prints the algorithm's step-by-step logic:
- **Round Header:** `--- Round X (Y components remain) ---`
- `Comparing edge X-Y with weight Z`
- `Updating cheapest edge for component of X to X-Y`
- `Skipping edge X-Y (same component)`
- `Adding edge X-Y to MST (weight Z)`

**2. Final Result** Prints the final Minimum Spanning Tree:
- **Line 1:** `MST Built.`
- **Middle Lines:** `Node1-Node2 Cost` (One per edge in the MST)
- **Last Line:** `Total Weight: X`

_(If an error occurs, it prints either `Error! Cannot Build MST` or `Error! Please make sure your input is correct.` instead)._

### Result of Sample Run
![Borůvka's algorithm sample run 1](./Assets/Pasted%20image%2020260915143832.png)
![Borůvka's algorithm sample run 2](./Assets/Pasted%20image%2020260915143857.png)

---
## Prerequisites to Run the Code
1. **Python 3.x**: You must have Python 3 installed on your computer. (Any newer version, like Python 3.6 will work perfectly).
2. **No External Libraries**: You do **not** need to install any third-party packages (like `pip install numpy` or `networkx`). The code uses purely built-in Python features.
3. **An Interactive Terminal/IDE**: You must run it in a terminal, command prompt, or an IDE (online compiler works too!).

**To run a script from the terminal, simply use the command:**

```bash
python <filename>.py
```
or
```bash
python3 <filename>.py
```
---
## Resources
- https://www.freecodecamp.org/news/prims-algorithm-explained-with-pseudocode/#heading-what-is-prims-algorithm
- https://www.programiz.com/dsa/kruskal-algorithm
- https://www.geeksforgeeks.org/dsa/boruvkas-algorithm-greedy-algo-9/
- https://see-algorithms.com/graph/Boruvkas
- AI Prompt History: https://share.gemini.google/eiFIuZWUJISq
---
