# Prim's algorithm for an undirected, weighted graph.

# Represents a graph
class Graph:
    # Initializes the graph properties and adjacency matrix
    def __init__(self, labels):
        self.labels = labels
        self.size = len(labels)
        self.adj_matrix = [[0] * self.size for _ in labels]

    # Adds an undirected weighted edge between two vertices
    def add_edge(self, u, v, weight):
        self.adj_matrix[u][v] = weight
        self.adj_matrix[v][u] = weight

    # Computes the Minimum Spanning Tree
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


# Reads graph definition and edges
def read_graph_from_input():
    labels = input("Enter Nodes: ").split()
    if len(labels) < 2 or len(set(labels)) != len(labels):
        raise ValueError

    indexes = {label: index for index, label in enumerate(labels)}
    graph = Graph(labels)
    edge_count = int(input("Enter Edges: "))
    if edge_count < len(labels) - 1:
        raise ValueError

    for _ in range(edge_count):
        parts = input().split()
        if len(parts) != 3:
            raise ValueError
        u_label, v_label, cost = parts
        if u_label not in indexes or v_label not in indexes or u_label == v_label:
            raise ValueError
        weight = float(cost)
        if weight <= 0:
            raise ValueError
        graph.add_edge(indexes[u_label], indexes[v_label], weight)
    return graph


# Main execution block for reading input, running the algorithm, and error handling
if __name__ == "__main__":
    try:
        graph = read_graph_from_input()
        edges = graph.prims_algorithm()
        print("MST Built.")
        total_weight = 0
        for u, v, weight in edges:
            print(f"{u}-{v} {weight:g}")
            total_weight += weight
        print(f"Total Weight: {total_weight:g}")
    except RuntimeError:
        print("Error! Cannot Build MST")
    except (EOFError, TypeError, ValueError):
        print("Error! Please make sure your input is correct.")
