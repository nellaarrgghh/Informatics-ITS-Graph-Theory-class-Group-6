# Boruvka's algorithm for an undirected, weighted graph.

# Represents a graph using an edge list
class Graph:
    def __init__(self, labels):
        self.labels = labels
        self.graph = []

    def add_edge(self, u, v, weight):
        self.graph.append((u, v, weight))

    # Find-set with path compression. Recursively finds the root of a set.
    def find(self, parent, vertex):
        if parent[vertex] != vertex:
            parent[vertex] = self.find(parent, parent[vertex])
        return parent[vertex]

    # Union by rank. Joins two sets together avoiding deep trees.
    def union(self, parent, rank, first, second):
        first = self.find(parent, first)
        second = self.find(parent, second)
        if first == second:
            return False
        if rank[first] < rank[second]:
            first, second = second, first
        parent[second] = first
        if rank[first] == rank[second]:
            rank[first] += 1
        return True

    # Executes Borůvka's Algorithm to find the Minimum Spanning Tree
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
        edges = graph.boruvka_algorithm()
        print("MST Built.")
        total_weight = 0
        for u, v, weight in edges:
            print(f"{u}-{v} {weight:g}")
            total_weight += weight
        print(f"Total Weight: {total_weight:g}")
    except RuntimeError: # Handles Error
        print("Error! Cannot Build MST")
    except (EOFError, TypeError, ValueError): # This too handles error
        print("Error! Please make sure your input is correct.")
