import random
import string

def generate_random_graph(num_nodes, max_edges_per_node):
    graph = {}
    for node in range(num_nodes):
        neighbors = random.sample(range(num_nodes), random.randint(1, max_edges_per_node))
        edges = {string.ascii_uppercase[neighbor]: random.randint(1, 10) for neighbor in neighbors}
        graph[string.ascii_uppercase[node]] = edges
    return graph


def save_graph_to_file(graph, filename):
    with open(filename, 'w') as file:
        for node, edges in graph.items():
            edge_strings = [f"{neighbor}({weight})" if weight > 1 else str(neighbor) for neighbor, weight in edges.items()]
            file.write(f"{node}: {', '.join(edge_strings)}\n")


num_nodes = random.randint(4, 10)
max_edges_per_node = random.randint(2, 10)


num_files = 50

for i in range(num_files):
    graph = generate_random_graph(num_nodes, max_edges_per_node)
    filename = f'./example_graphs/graph_{i}.txt'
    save_graph_to_file(graph, filename)

    print(f'Generated {filename}')

