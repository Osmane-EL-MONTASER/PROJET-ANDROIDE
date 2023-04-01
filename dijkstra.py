import networkx as nx
import heapq
import numpy as np

class multi_criteria_dijkstra:
    """
    Classe pour gérer les opérations de dijsktra multi-objectifs
    """
    def __init__(self, G = None, nb_criteria = 4):
        self.G = G
        self.nb_criteria = nb_criteria


    def try_add_new_cost(self, lst:np.array, newcost:list):
        """
        Fonction qui pour une liste de vecteurs coût donné, essaye d'ajouter un nouveau vecteur coût à cette liste
        
        Le nouveau vecteur coût est rajouté si il est pas strictement dominé par un autre vecteur, en enlevant les possibles vecteurs qui sont dominés par le nouveau vecteur.

        Parameters
        ----------
        self
        lst:np.array
            Liste de vecteur coût à modifier
        newcost:list
            Nouveau vecteur coût que l'on tente de rajouter

        Returns
        -------
        lst
            Liste de vecteur coût après tentative d'ajout du vecteur
        is_updated
            True si le vecteur coût a été rajouté, False sinon
        """
        if np.array(lst).shape[0] == 0:
            lst = np.array(newcost)
        else:
            lst = np.append(lst, newcost, axis = 0)
        front = self.pareto_front(lst)
        is_updated = front[-1]
        lst = lst[front]
        return lst, is_updated

    def pareto_front(self, lst:np.array):
        """
        Fonction qui pour une liste de vecteurs coût donné, retourne le front de pareto
        
        Retourne un np.array qui a chaque index indique True si le vecteur à cette indice est dominant, False sinon.

        Parameters
        ----------
        self
        lst:np.array
            Liste de vecteur coût

        Returns
        -------
        front:np.array
            np.array de taille de la lst, avec pour chaque valeur à l'index donné qui indique si le vecteur est dominant ou non
        """
        costs = np.array(lst)
        front = np.ones(costs.shape[0], dtype = bool)
        for i, c in enumerate(costs):
            if front[i]:
                front[front] = np.any(costs[front][:,:-1]<c[:-1], axis=1)  # Keep any point with a lower cost
                front[i] = True  # And keep self
        return front
       
    def dijkstra(self, G: nx.Graph, start, end):
        """
        Fonction pour faire le dijkstra multi-objectifs.
        
        Pour un graphe donné, un départ et un arrivé, la fonction donne la liste des coûts pour chaque noeud visité

        Parameters
        ----------
        self
        G:nx.Graph
            Liste de vecteur coût
        start
            Etiquette du noeud de départ
        end
            Etiquette du noeud d'arrivé

        Returns
        -------
        costs:dict
            Dictionnaire contenant les différents vecteurs de coût pour ce noeud
        """
        costs = {}

        queue = [0 for i in range(self.nb_criteria)]
        costs[start] = queue
        queue.append(start)
        queue = [queue]

        while queue:
            #Pop the current node and its vector cost
            cost = heapq.heappop(queue)
            u = cost[-1]
            
            if end in costs.keys():
                if np.all(np.any(costs[end][:,:-1]<cost[:-1], axis=1)):
                    pass

            #Visit each neighbor of the current node
            for _, v, data in G.edges(u, data = True):
                #edge attribute returned in 3-tuple (u, v, ddict[data])
                nextcost = []
                
                for i in range(len(cost)-1):
                    nextcost.append(cost[i] + data['weight'][i])
                nextqueue = nextcost.copy()

                nextcost.append(u)
                nextqueue.append(v)
                if v not in costs:
                    costs[v] = []

                costs[v], updated = self.try_add_new_cost(costs[v], [nextcost])

                if updated:
                    heapq.heappush(queue, nextqueue)

        return costs