import networkx as nx
import heapq
import numpy as np
from paretoset import paretoset
import geopy.distance
import matplotlib.pyplot as plt
import utm
import time

class PrioritySet(object):
    def __init__(self):
        self.heap = []
        self.set = set()

    def add(self, heur, rec):
        if not tuple(heur) in self.set:
            heapq.heappush(self.heap, [heur, rec])
            self.set.add(tuple(heur))

    def pop(self):
        heur, rec = heapq.heappop(self.heap)
        self.set.remove(tuple(heur))
        return [heur,rec]
    
def get_heuristique(start, end):
    if start.get('heuristique') is None:
        x1, y1 = start['lon'], start['lat']
        x2, y2 = end['lon'], end['lat']
        start['heuristique'] = get_distance(x1,y1,x2,y2)
    return start['heuristique']
    
def get_distance(lat_start, lon_start, lat_goal, long_goal):
    distance = geopy.distance.geodesic((lat_goal, long_goal), (lat_start, lon_start)).m
    return distance

def draw_add_graph(g, u, udata, v, vdata, counter):
    g.add_node(u)
    g.nodes[u].update(udata)
    xy = utm.from_latlon(float(g.nodes[u]['lat']),float(g.nodes[u]['lon']))
    g.nodes[u]['pos'] = (xy[0],xy[1])
    g.add_node(v)
    g.nodes[v].update(vdata)
    xy = utm.from_latlon(float(g.nodes[v]['lat']),float(g.nodes[v]['lon']))
    g.nodes[v]['pos'] = (xy[0],xy[1])
    g.add_edge(u,v)
    nx.draw_networkx(g, nx.get_node_attributes(g, 'pos'), node_size = 1000/g.number_of_nodes(), with_labels = False, width=10/g.number_of_nodes())
    if(counter % 10) == 0:
        #print(len(g.edges(u)))
        plt.show()

class astar_eps:
    """
    Classe pour gérer les opérations de dijsktra multi-objectifs
    """
    cost_dtype = np.dtype([('weights', list), ('prevnode', np.int64), ('node', np.int64), ('previd', np.int64), ('id', np.int64)])

    def __init__(self, G = None, nb_criteria = 4):
        self.G = G
        self.nb_criteria = nb_criteria


    def try_add_new_cost(self, lstcost:np.recarray, newcost, pareto_func, eps):
        """
        Fonction qui pour une liste de vecteurs coût donné, essaye d'ajouter un nouveau vecteur coût à cette liste
        
        Le nouveau vecteur coût est rajouté s'il n'est pas strictement dominé par un autre vecteur, en enlevant les possibles vecteurs qui sont dominés par le nouveau vecteur.

        Parameters
        ----------
        self
        lstcost
            Liste de vecteur coût à modifier
        newcost
            Nouveau vecteur coût que l'on tente de rajouter

        Returns
        -------
        lstcost
            Liste de vecteur coût après tentative d'ajout du vecteur
        has_updated
            True si le vecteur coût a été rajouté, False sinon
        """
        lstcopy = lstcost.copy()
        lstcopy.resize(lstcost.shape[0] + 1, refcheck=False)
        exponent = np.rint(np.emath.logn(1 + eps, newcost[0]))
        temp = [exponent]
        temp[1:] = newcost[1:]
        lstcopy[-1] = tuple(temp)
        front = pareto_func(lstcopy.weights.tolist())
        has_updated = front[-1]
        lstcopy = lstcopy[front]
        return lstcopy, has_updated

    def pareto_front(self, lst:np.array):
        """
        Fonction qui pour une liste de vecteurs coût donné, retourne le front de pareto
        
        Retourne un np.array qui a chaque index indique True si le vecteur à cette indice est non dominé, False sinon.

        Parameters
        ----------
        self
        lst:np.array
            Liste de vecteur coût

        Returns
        -------
        front:np.array
            np.array de taille de la lst, avec pour chaque valeur à l'index donné qui indique si le vecteur est non dominé ou dominé
        """
        costs = np.array(lst)
        front = np.ones(costs.shape[0], dtype = bool)
        for i, c in enumerate(costs):
            if front[i]:
                front[front] = np.any(costs[front]<c, axis=1)  # Keep any point with a lower cost
                front[i] = True  # And keep self
        return front
    
    def pareto_front_paretoset(self, lst:np.array):
        """
        Fonction qui pour une liste de vecteurs coût donné, retourne le front de pareto en utilisant la librairie paretoset
        
        Retourne un np.array qui a chaque index indique True si le vecteur à cette indice est non dominé, False sinon.

        Parameters
        ----------
        self
        lst:np.array
            Liste de vecteur coût

        Returns
        -------
        front:np.array
            np.array de taille de la lst, avec pour chaque valeur à l'index donné qui indique si le vecteur est non dominé ou dominé
        """
        return paretoset(lst)
    
    def update_pareto_front(self, new_cost, lst):
        """
        Fonction qui pour une liste de vecteurs de coût (non dominés entre eux) et un nouveau vecteur de coût 
        met à jour le front de Pareto (si le nouveau vecteur est dominé, ne l'ajoute pas, sinon, supprime les vecteurs
                                       qu'il domine)
        
        Retourne un np.array contenant les coûts non dominés et une variable booléenne indiquant si le nouveau coût a été retenu

        Parameters
        ----------
        self
        lst:np.array
            Liste de vecteur coût

        Returns
        -------
        front:np.array
            np.array de taille de la lst, avec pour chaque valeur à l'index donné qui indique si le vecteur est non dominé ou dominé
        """
        front = np.ones(len(lst)+1,dtype=bool) #le dernier élément correspond au new_cost
        front[-1] = False
        for i,c in enumerate(lst):
            if np.all(new_cost<c):
                front[i] = False
                front[-1] = True        
        return lst[front], front[-1]
                
    
    def update_pareto_front_dct(self, new_cost, dct):
        front = False
        for k,v in dct.items():
            if np.all(new_cost<v):
                del dct[k]
                front = True 
        if front == True:
            etiq = max(dct.keys()) + 1
            dct[etiq] = new_cost
        else:
            etiq = None
        return dct, front, etiq

    class cost_class:
        def __init__(self, weights, prevnode, node, previd, id):
            self.weights = weights
            self.prevnode = prevnode
            self.node = node
            self.previd = previd
            self.id = id

    def a_star(self, G: nx.Graph, start, end, maxdistance, eps):
        costs = {}
        gdraw = nx.Graph()
        start_heuristic = get_heuristique(G.nodes[start], G.nodes[end])
        start_cost = np.array([0 for _ in range(self.nb_criteria)])
        
        to_add_queue = (start_cost + start_heuristic, -1, start, -1, 0)
        costs[start] = np.recarray((1,), dtype=self.cost_dtype)
        costs[start][0] = (start_cost, -1, start, -1, 0)

        G.add_node(-1, label = "Dummy", heuristique = 0)
        queue = PrioritySet()
        queue.add(to_add_queue[0], to_add_queue)
        #heapq.heappush(queue, [to_add_queue[0], to_add_queue])
        
        counterid = 0
        while queue.heap:
            #Pop le noeud courant et récupère son cout associé
            queued = queue.pop()
            #queued = heapq.heappop(queue)
            
            if (counterid%100) == 0:
                print("{} noeuds explorés, {} noeuds restants dans la file".format(counterid, len(queue.heap)))
            #print("NB NOEUDS DANS QUEUE:{}".format(len(queue)))
            #print(queued)
            cost = queued[1] #([c_v1 + heur_v,..., c_vn + heur_v], u, v, prevedgeid, curedgeid)
            #print("CURRENT ESTIMATED DISTANCE: {}".format(get_heuristique(G.nodes[cost[2]], G.nodes[end])))
            if end in costs.keys():  #Si le noeud terminal a été atteint, verifier si le noeud courant est strictement dominé ou pas par les vecteurs couts déjà existants
                print("NOEUD TERMINAL TROUVE")
                nextheur = get_heuristique(G.nodes[cost[2]], G.nodes[end])
                prevheur = get_heuristique(G.nodes[cost[1]], G.nodes[end])
                heuristic = np.array(cost[0]) + nextheur - prevheur
                if np.all(np.any(np.array(costs[end].weights.tolist())<heuristic + maxdistance, axis=1)):
                    continue

            #Visiter tout les voisins du noeud courant
            for _, v, data in G.edges(cost[2], data = True):
                #Données des aretes voisines retourné en 3-tuple (u, v, ddict[data])
                updated = False
                counterid += 1
                prevheurvisited = get_heuristique(G.nodes[cost[2]], G.nodes[end])
                curweight = np.array(queued[0]) - prevheurvisited
                nextweight =  curweight + data['weight']#Cout du prochain noeud à visiter
                nextcost = (nextweight, cost[2], v, cost[4], counterid)
                if v not in costs:
                    costs[v] = np.recarray(1, dtype=self.cost_dtype)
                    costs[v][0] = nextcost
                    updated = True
                else:
                    costs[v], updated = self.try_add_new_cost(costs[v], nextcost, self.pareto_front_paretoset, eps)

                if updated:
                    if v == end:
                        continue
                    #draw_add_graph(gdraw,cost[2], G.nodes[cost[2]],v, G.nodes[v], counterid)
                    nextheurupdated = get_heuristique(G.nodes[v], G.nodes[end])
                    nextheuristic = nextweight + nextheurupdated#Heuristique du prochain noeud à visiter
                    nextheuristic = nextheuristic.tolist()
                    #heapq.heappush(queue, [nextheuristic, nextcost])
                    queue.add(nextheuristic, nextcost)

        return costs
    
    
