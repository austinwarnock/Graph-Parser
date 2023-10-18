from typing import List, Union

class Vertex:
    def __init__(self, name: str, color: str = None) -> None:
        """
        Initialize a vertex with a name and an optional color.

        :param name: The name of the vertex.
        :param color: The color of the vertex (optional).
        """
        self.name = name
        self.color = color
        
    def __hash__(self) -> int:
        return hash(self.name)
    
    def __lt__(self, other: "Vertex") -> bool:
        return self.name < other.name
    
    def __gt__(self, other: "Vertex") -> bool:
        return self.name > other.name
    
    def __str__(self) -> str:
        return self.name
    
    def __repr__(self):
        return self.__str__()

    def __eq__(self, other: "Vertex") -> bool:
        if isinstance(other, Vertex):
            return self.name == other.name
        return False

class Edge:
    def __init__(self, source: Vertex, destination: Vertex, weight: int = 1) -> None:
        """
        Initialize an edge with a source vertex, a destination vertex, and an optional weight.

        :param source: The source vertex of the edge.
        :param destination: The destination vertex of the edge.
        :param weight: The weight of the edge (optional).
        """
        self.source = source
        self.destination = destination
        self.weight = weight
    
    def __hash__(self) -> int:
        ordered_edge = tuple(sorted((self.source, self.destination)))
        return hash(ordered_edge)

    def __eq__(self, other: "Edge") -> bool:
        if isinstance(other, Edge):
            return (self.source == other.source and self.destination == other.destination) or (self.source == other.destination and self.destination == other.source) and self.weight == other.weight
        return False
    
    def __str__(self) -> str:
        return f"{self.source} - {self.destination} ({self.weight})"
    def __repr__(self):
        return self.__str__()

class Graph:
    def __init__(self) -> None:
        """
        Initialize an empty graph with sets for vertices and edges.
        """
        self.vertices: set[Vertex] = set()
        self.edges: set[Edge] = set()
        
    def get_vertex_by_name(self, name: str) -> "Vertex":
        """
        Get a vertex by its name.

        :param name: The name of the vertex.
        :return: The vertex with the given name.
        """
        for vertex in self.vertices:
            if vertex.name == name:
                return vertex
        raise ValueError(f"Vertex {name} not found in graph.")
        
    def insert_vertex(self, vertex_name: str) -> None:
        """
        Insert a vertex into the graph.

        :param vertex_name: The name of the vertex to be inserted.
        """
        self.vertices.add(Vertex(vertex_name))
        
    def insert_edge(self, source: str, destination: str, weight: int = 1) -> None:
        """
        Insert an edge into the graph.

        :param source: The name of the source vertex.
        :param destination: The name of the destination vertex.
        :param weight: The weight of the edge (optional).
        """
        if source not in self.vertices:
            self.insert_vertex(source)
        if destination not in self.vertices:
            self.insert_vertex(destination)
            
        source = self.get_vertex_by_name(source)
        destination = self.get_vertex_by_name(destination)
            
        self.edges.add(Edge(source, destination, weight))
        
    def get_neighbors(self, vertex:Vertex) -> List[Vertex]:
        """
        Get the neighbors of a vertex.

        :param vertex_name: The name of the vertex.
        :return: A list of neighbor vertex names.
        """
        neighbors = []
        for edge in self.edges:
            if edge.source == vertex:
                neighbors.append(edge.destination)
            elif edge.destination == vertex:
                neighbors.append(edge.source)
        return neighbors
    
    def get_vertices(self) -> List[str]:
        """
        Get the names of all vertices in the graph.

        :return: A sorted list of vertex names.
        """
        return sorted(self.vertices)
    
    def get_edges(self) -> List[Union[str, str, str]]:
        """
        Get information about all edges in the graph.

        :return: A sorted list of edge information, where each item is a tuple (source, destination, weight).
        """
        return sorted(self.edges, key=lambda x: (x.source, x.destination, x.weight))
    
    def get_min_edge(self, source: Vertex, destination: Vertex) -> Edge:
        """
        Get an edge by its source and destination vertices.

        :param source: The source vertex of the edge.
        :param destination: The destination vertex of the edge.
        :return: The edge with the given source and destination vertices.
        """
        edges = []
        for edge in self.edges:
            if edge.source == source and edge.destination == destination:
                edges.append(edge)
            elif edge.source == destination and edge.destination == source:
                edges.append(edge)
        return min(edges, key=lambda x: x.weight)

    
    def find(self, parent: dict, vertex: str) -> str:
        """
        Find the representative of the set that a vertex belongs to.

        :param parent: A dictionary representing the parent of each vertex in a set.
        :param vertex: The name of the vertex.
        :return: The representative (parent) of the set.
        """
        if parent[vertex] == vertex:
            return vertex
        return self.find(parent, parent[vertex])

    def union(self, parent: dict, rank: dict, x: str, y: str) -> None:
        """
        Perform a union operation on two sets.

        :param parent: A dictionary representing the parent of each vertex in a set.
        :param rank: A dictionary representing the rank of each set.
        :param x: The name of the first vertex.
        :param y: The name of the second vertex.
        """
        x_root = self.find(parent, x)
        y_root = self.find(parent, y)

        if rank[x_root] < rank[y_root]:
            parent[x_root] = y_root
        elif rank[x_root] > rank[y_root]:
            parent[y_root] = x_root
        else:
            parent[y_root] = x_root
            rank[x_root] += 1

    def minimum_spanning_tree(self) -> "Graph":
        """
        Find the minimum spanning tree of the graph using Kruskal's algorithm.

        :return: A new Graph object representing the minimum spanning tree.
        """
        mst = Graph()
        edges = sorted(self.edges, key=lambda e: e.weight)
        parent = {}
        rank = {}

        for vertex in self.vertices:
            parent[vertex.name] = vertex.name
            rank[vertex.name] = 0

        for edge in edges:
            source = edge.source.name
            destination = edge.destination.name

            source_parent = self.find(parent, source)
            destination_parent = self.find(parent, destination)

            if source_parent != destination_parent:
                mst.insert_vertex(source)
                mst.insert_vertex(destination)
                mst.insert_edge(source, destination, edge.weight)
                self.union(parent, rank, source_parent, destination_parent)

        return mst

    def dijkstra(self, source: str) -> dict:
        """
        Find the shortest paths from a source vertex to all other vertices in the graph using Dijkstra's algorithm.

        :param source: The name of the source vertex.
        :return: A dictionary representing the shortest paths from the source vertex to all other vertices.
        """
        distances = {}
        for vertex in self.vertices:
            distances[vertex.name] = float("inf")
        distances[source] = 0

        visited = set()
        unvisited = set(self.vertices)

        while unvisited:
            current = min(unvisited, key=lambda x: distances[x.name])
            unvisited.remove(current)
            visited.add(current)

            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    distances[neighbor.name] = min(distances[neighbor.name], distances[current.name] + self.get_min_edge(current, neighbor).weight)

        return distances
    
    def __str__(self) -> str:
        return f"Vertices: {self.get_vertices()}\nEdges: {self.get_edges()}"