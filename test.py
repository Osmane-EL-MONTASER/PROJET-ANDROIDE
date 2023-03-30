import numpy as np

def pareto_front(lst):
    costs = np.array(lst)
    front = np.ones(costs.shape[0], dtype = bool)
    for i, c in enumerate(costs):
        if front[i]:
            front[front] = np.any(costs[front]<c, axis=1)  # Keep any point with a lower cost
            print(front)
            front[i] = True  # And keep self
    return front


#print(np.array([[1,2,1],[3,2,1]])[:,:-1],np.array([1,1,2])[:-1])
#print(np.any((np.array([[3,4,1],[3,2,1],[0,1,0]]))<[0,2,0]))
print(pareto_front(np.array([[1,1,6],[3,2,1],[1,1,0]])))
