import dijkstra
import networkx as nx
import heapq
import numpy as np

G = nx.DiGraph()
# definition des noeuds
G.add_node(1,label='A')
G.add_node(2,label='B')
G.add_node(3,label='C')
G.add_node(4,label='D')
G.add_node(5,label='E')
G.add_node(6,label='F')
# definition des aretes
G.add_edge(1,2,weight=[10,4,2,10])
G.add_edge(1,3,weight=[6,1,18,10])
G.add_edge(3,2,weight=[6,2,10,10])
G.add_edge(2,4,weight=[0,10,12,1])
G.add_edge(4,6,weight=[10,1,1,1])
G.add_edge(4,3,weight=[4,0,0,3])
G.add_edge(3,5,weight=[1,4,8,1])
G.add_edge(5,4,weight=[5,1,3,7])
G.add_edge(5,6,weight=[6,0,0,6])

queue = [[0, 0, 0, 0, 1]]
cost = heapq.heappop(queue)
print(cost)

print(np.any(np.array([[1,2,1],[3,2,1]])[:,:-1]>np.array([1,1,2])[:-1], axis=1))

dijkstra = dijkstra.multi_criteria_dijkstra()
print(dijkstra.dijkstra(G,1,6))

test = np.array([[1,3,1],[4,2,2],[8,8,3],[2,3,4]])
print(np.ones(test.shape[0], dtype=bool))
print(dijkstra.pareto_front(test))

print(dijkstra.try_add_new_cost(test, [[1,2,1]]))
print(dijkstra.try_add_new_cost(test, [[2,3,2]]))
print(dijkstra.try_add_new_cost([], [[2,3,2]]))