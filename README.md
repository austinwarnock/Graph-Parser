# Graph Parser in Python using LARK

This is a sample project that uses LARK to create a parser for reading in text files of weighted and unweighted graphs in Adjacency list form.

```
A: B(2), C
B: A(2), D(3)
C: A, D(1)
D: B(3), C
```
Once parsed, the graph is then transformed into a custom implementation of a Graph data structure. From this, I implement a couple of popular graph algorithms (Kruskal's and Dijkstra's).

## Utility
I have also included additional utility code files for both randomly generating graph files and then for plotting the resulting graphs visually. 

## Future Plans
I plan on updating the grammar to allow for directed graphs as input. From this, I will then implement some Max-Flow Algorithms like Ford-Fulkerson or Edmonds-Karp