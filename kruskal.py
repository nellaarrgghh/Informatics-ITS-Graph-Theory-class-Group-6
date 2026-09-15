# Kruskal's Algorithm

# Represents a graph using an edge list
class Graph:
    # Initializes the graph with vertex labels and an empty edge list
    def __init__(self, labels):
        self.labels = labels
        self.graph = []

    # Adds a weighted edge to the graph
    def add_edge(self, u, v, weight):
        self.graph.append((u, v, weight))

    # Search function with path compression. Recursively finds the root of a set.
    def find(self, parent, vertex):
        if parent[vertex] != vertex:
            parent[vertex] = self.find(parent, parent[vertex])
        return parent[vertex]

    # Union by rank. Joins two sets together avoiding deep trees.
    def union(self, parent, rank, first, second):
        first = self.find(parent, first)
        second = self.find(parent, second)
        if first == second:
            return
        if rank[first] < rank[second]:
            first, second = second, first
        parent[second] = first
        if rank[first] == rank[second]:
            rank[first] += 1

    # Executes Kruskal's Algorithm
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


# Parses user input to build the graph and its edges
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


# Main execution block
if __name__ == "__main__":
    try:
        graph = read_graph_from_input()
        edges = graph.kruskal_algorithm()
        print("MST Built.")
        total_weight = 0
        for u, v, weight in edges:
            print(f"{u}-{v} {weight:g}")
            total_weight += weight
        print(f"Total Weight: {total_weight:g}")
    except RuntimeError: # Error handling when MST cannot be built
        print("Error! Cannot Build MST")
    except (EOFError, TypeError, ValueError): # when input is invalid
        print("Error! Please make sure your input is correct.")
