from graph import Graph
from lark import Lark, Transformer
import os    
class GraphTransformer(Transformer):
    def start(self, nodes):
        graph = Graph()
        for node in nodes:
            name = node.children[0].value
            neighbors = node.children[1].children
            graph.insert_vertex(name)
            for neighbor in neighbors:
                neighbor_name = neighbor.children[0].value
                weight = neighbor.children[1].value if len(neighbor.children) > 1 else 1
                graph.insert_edge(name, neighbor_name, weight=int(weight))

        return graph


def parse_adjacency_list(input_file):
    with open(input_file, "r") as f:
        content = f.read()

    parser = Lark.open("./graph_grammar.lark", parser="lalr", transformer=GraphTransformer())
    graph = parser.parse(content)
    return graph

if __name__ == "__main__":

    for file in os.listdir("./example_graphs"):
        input_file = f"./example_graphs/{file}"
        parsed_graph = parse_adjacency_list(input_file)
        
        print(parsed_graph)
        print("MST:", parsed_graph.minimum_spanning_tree().get_edges())
        print("Dijkstra:", parsed_graph.dijkstra("A"))


