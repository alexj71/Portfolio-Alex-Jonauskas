# Minimum Weight Vertex Cover (MWVC)
## Description:
Given a graph (in the discrete math sense), find the minimum weight vertex cover. A graph in the discrete math sense is simply a set of nodes and edges connecting those nodes. A vertex cover is a set of edges that touch every node. A graph can have weighted edges (each edge has some kind of value/cost). Finding a minimum weight vertex cover is an NP-complete problem but we explore some variations that are slightly faster.

## Recursive Solution:
Our first task was to find a recursive solution to the minimum weight vertex cover problem that was o(1.5^n) (when the straightforward recursive solution is o(2^n)). The straight-forward recursive algorithm minWVC(graph):
1. Chooses a random edge and:
    - Acts as though it is in the MWVC and removes the nodes that it is touching and any other edges touching those nodes. Then passes the new graph to minWVC(newgraph) (recursively)
    - Acts as though the same random edge is not in the MWVC as well. Removes the edge and passes the altenate new graph to minWVC(alternateNewGraph) (recursively)
2. Eventually the many calls of minWVC() reach a point where there are no more edges to consider. At this point our recursive calls have generated every possible vertex cover since we considered every edge to be in or out of the vertex cover. We simply have minWVC() return the smaller vertex cover at every level and the one that makes it back to the original call of the function will have been the smallest.\

To make it slightly faster (o(1.5^n) -> o(2^n)) we simply stop making recursive calls if every node is touching at most one edge and simply choose the edges left that have the lower weights.

## Bounded Search Tree Algorithm:
Our next task was to solve the same problem but with the added parameter that the vertex cover could be at most size k. I solved this almost the same way. I simply pass make k smaller by how ever many edges are removed at each step and if k reaches 0 while there are still edges left than I simply return the entire graph. The reason for doing so (and what makes it the _bounded_ search tree algorithm) is that the result of continuing to follow that recursive path is going to be larger than k. Returning the entire graph is okay because it will definitely be larger than the smallest solution. So if there is a vertex cover of size k then it will be returned, if not the entire graph will be and there's no solution.

## Results:
I recieved an A on this project.

__Note that both solutions are in the MVWC file.__
