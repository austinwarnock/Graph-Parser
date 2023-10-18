import networkx as nx
import matplotlib.pyplot as plt
import os

def plot_graph(filepath):
    G = nx.Graph()
    with open(filepath, "r") as file:
        for line in file:
            node, connections = line.strip().split(": ")
            connections = connections.split(", ")
            for connection in connections:
                parts = connection.split("(")
                neighbor = parts[0].strip()
                weight = int(parts[1].strip(")")) if len(parts) > 1 else 1
                G.add_edge(node, neighbor, weight=weight)

    # Plot the graph
    pos = nx.circular_layout(G)
    labels = nx.get_edge_attributes(G, "weight")
    nx.draw(G, pos, with_labels=True, node_color='lightblue', font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.savefig(f"./example_graph_imgs/{filepath.split('/')[-1].split('.')[0]}.png")
    plt.clf()
    
if __name__ == "__main__":
    for file in os.listdir("./example_graphs"):
        input_file = f"./example_graphs/{file}"
        parsed_graph = plot_graph(input_file)
