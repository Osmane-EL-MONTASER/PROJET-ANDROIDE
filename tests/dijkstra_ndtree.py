import networkx as nx
import heapq
import numpy as np
from paretoset import paretoset
import geopy.distance
import matplotlib.pyplot as plt
import utm
import time
from ndtree import ndtree

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
        time.sleep(0.1)

class multi_criteria_dijkstra:
    """
    Classe pour gérer les opérations de dijsktra multi-objectifs
    """
    cost_dtype = np.dtype([('weights', list), ('prevnode', np.int64), ('node', np.int64), ('previd', np.int64), ('id', np.int64)])

    def __init__(self, G = None, nb_criteria = 4):
        self.G = G
        self.nb_criteria = nb_criteria


    def try_add_new_cost(self, lstcost:np.recarray, newcost, pareto_func, nadir=None):
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
        lstcopy[-1] = newcost
        if nadir is None:
            front = pareto_func(lstcopy.weights.tolist())
        else:
            front, nadir = pareto_func(lstcopy.weights.tolist(), nadir)
        has_updated = front[-1]
        lstcopy = lstcopy[front]
        #print(newcost)
        return lstcopy, has_updated, nadir
    
    def try_add_new_cost_ndtree(self, tree, newcost):
        has_updated = tree.update_tree(newcost)
        return has_updated

    def pareto_front(self, lst:np.array, nadir):
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
                front[front] = np.any(costs[front]<c-np.array(nadir)/200, axis=1)  # Keep any point with a lower cost
                nadir = np.maximum(c,nadir)
                front[i] = True  # And keep self
        return front, nadir
    
    
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
        gdraw = nx.Graph()

        start_cost = ([0 for i in range(self.nb_criteria)], -1, start, -1, 0)
        costs[start] = np.recarray((1,), dtype=self.cost_dtype)
        costs[start][0] = start_cost

        queue = []
        heapq.heappush(queue, [start_cost[0], start_cost])
        
        counterid = 0
        while queue:
            updated = False
            #Pop le noeud courant et récupère son cout associé
            cost = heapq.heappop(queue)[1]
            #print("NB NOEUDS DANS QUEUE:{}".format(len(queue)))
            #print(cost)
            if end in costs.keys():  #Si le noeud terminal a été atteint, verifier si le noeud courant est strictement dominé ou pas par les vecteurs couts déjà existants
                #print(costs[end].weights.tolist())
                if np.all(np.any(np.array(costs[end].weights.tolist())<cost[0], axis=1)):
                    continue
            #Visiter tout les voisins du noeud courant
            for _, v, data in G.edges(cost[2], data = True):
                #Données des aretes voisines retourné en 3-tuple (u, v, ddict[data])
                counterid += 1
                nextweight = np.array(cost[0]) + data['weight'] #Cout du prochain noeud à visiter
                nextweight = nextweight.tolist()
                nextcost = (nextweight, cost[2], v, cost[4], counterid)

                if v not in costs:
                    costs[v] = np.recarray(1, dtype=self.cost_dtype)
                    costs[v][0] = nextcost
                    updated = True
                else:
                    costs[v], updated = self.try_add_new_cost(costs[v], nextcost, self.pareto_front)

                if updated:
                    draw_add_graph(gdraw,cost[2], G.nodes[cost[2]],v, G.nodes[v], counterid)
                    heapq.heappush(queue, [nextcost[0], nextcost])

        return costs

    """def a_star(self, G: nx.Graph, start, end):
        # initialisation de la liste open_nodes et du set closed_nodes
        open_nodes = set(start)
        open_etiquettes = [self.heuristique(G, start, end),start,0,([0]*self.nb_criteria)]
        closed_etiquettes = {}
        closed_nodes = set()
        
        # initialisation costs dictionnaire clés:noeuds, valeurs:dictionnaires clés étiquettes valeurs: vecteurs coûts
        costs = {}
        costs[start][0] = [0]*self.nb_criteria
        
        # initialisation du dictionnaire cost_from (pour chaque étiquette d'un noeud indique de quelle étiquette il provient)
        # même structure que costs
        cost_from = {}
        cost_from[start][0] = None
        
        # initialisation liste des solutions
        solutions = []  # éléments de la forme [path, cost]
        solutions_costs = []
        
        '''
        while open_nodes:
            curr_node = heapq.heappop(open_nodes)
            
            for curr_etiq in costs[curr_node].keys():
                curr_cost = costs[curr_node][curr_etiq]
            
                if curr_node == end:
                    path = []
                    while curr_etiq:
                        path.append((curr_node, curr_etiq))
                        curr_node, curr_etiq = cost_from[curr_node], cost_from[curr_node][curr_etiq]
                    path = list(reversed(path))
                    solutions.append([path,curr_cost])
                
                else:
                    #Visit each neighbor of the current node
                    for _, v, data in G.edges(curr_node, data = True):
                        if v in closed_nodes:
                            continue
                        
                        if v not in open_nodes:
                            open_nodes.append(v)
                        
                        for etiq in costs[curr_node]:
                            temp_cost = costs[curr_node][etiq] + data['weight']
                            est_cost = temp_cost + heuristique(self, G, v, end)
                        
                        
                        # trier open_nodes en fonction des étiquettes les plus prometteuses
        '''
        while open_etiquettes:
            _, curr_node, curr_etiq, curr_cost = heapq.heappop(open_etiquettes)
            if closed_etiquettes[curr_node] == None:
                closed_etiquettes[curr_node] = set(curr_etiq)
            else:
                closed_etiquettes[curr_node].add(curr_etiq)
            
            if curr_node == end:
                path = []
                while curr_etiq:
                    path.append((curr_node, curr_etiq))
                    curr_node, curr_etiq = cost_from[curr_node], cost_from[curr_node][curr_etiq]
                path = list(reversed(path))
                solutions.append([path,curr_cost])
                solutions_costs.append(curr_cost)
                
            
            else:
                # Visit each neighbor of the current node
                for _, v, data in G.edges(curr_node, data = True):
                    '''
                    if v in closed_nodes:
                        continue
                    '''
                    new_cost = costs[curr_node][curr_etiq] + data['weight']
                    est_cost = new_cost + self.heuristique(G, v, end)
                    
                    tmp_list = solutions_costs + [est_cost]
                    if est_cost not in self.pareto_front_paretoset(tmp_list):
                        continue
                    
                    if v not in open_nodes:
                        open_nodes.add(v)
                        open_etiquettes.append((est_cost,v,0, new_cost))
                        cost_from[v][0] = curr_etiq
                                            
                    else:
                        costs[v], updated, new_etiq = self.update_pareto_front_dct(new_cost,costs[v])
                        if updated:
                            cost_from[v][new_etiq] = curr_etiq
                            open_etiquettes.append((est_cost, v, new_etiq, new_cost))
                        else:
                            continue
            # trier les étiquettes ouvertes selon les coûts estimés avec l'heuristique (selon le 1er objectif)
            open_etiquettes = sorted(open_etiquettes)
        
        return solutions"""
    def a_star(self, G: nx.Graph, start, end):
        costs = {}
        #gdraw = nx.Graph()
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
            
            #print("NB NOEUDS DANS QUEUE:{}".format(len(queue)))
            #print(queued)
            cost = queued[1] #([c_v1 + heur_v,..., c_vn + heur_v], u, v, prevedgeid, curedgeid)
            #print("CURRENT ESTIMATED DISTANCE: {}".format(get_heuristique(G.nodes[cost[2]], G.nodes[end])))
            if end in costs.keys():  #Si le noeud terminal a été atteint, verifier si le noeud courant est strictement dominé ou pas par les vecteurs couts déjà existants
                #print("NOEUD TERMINAL TROUVE")
                nextheur = get_heuristique(G.nodes[cost[2]], G.nodes[end])
                prevheur = get_heuristique(G.nodes[cost[1]], G.nodes[end])
                heuristic = np.array(cost[0]) + nextheur - prevheur
                if np.all(np.any(np.array(costs[end].weights.tolist())<heuristic, axis=1)):
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
                    costs[v], updated,_ = self.try_add_new_cost(costs[v], nextcost, self.pareto_front_paretoset)

                if updated:
                    if v == end:
                        continue
                    #draw_add_graph(gdraw,cost[2], G.nodes[cost[2]],v, G.nodes[v], counterid)
                    nextheurupdated = get_heuristique(G.nodes[v], G.nodes[end])
                    nextheuristic = nextweight + nextheurupdated#Heuristique du prochain noeud à visiter
                    nextheuristic = nextheuristic.tolist()
                    #heapq.heappush(queue, [nextheuristic, nextcost])
                    queue.add(nextheuristic, nextcost)
        print(costs[end])
        return costs[end]
    
    def a_star_heur(self, G: nx.Graph, start, end):
        costs = {}
        nadirs = {}
        nadirs[start] = np.array([0,0,0,0])
        #gdraw = nx.Graph()
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
            
            #print("NB NOEUDS DANS QUEUE:{}".format(len(queue)))
            #print(queued)
            cost = queued[1] #([c_v1 + heur_v,..., c_vn + heur_v], u, v, prevedgeid, curedgeid)
            #print("CURRENT ESTIMATED DISTANCE: {}".format(get_heuristique(G.nodes[cost[2]], G.nodes[end])))
            if end in costs.keys():  #Si le noeud terminal a été atteint, verifier si le noeud courant est strictement dominé ou pas par les vecteurs couts déjà existants
                #print("NOEUD TERMINAL TROUVE")
                nextheur = get_heuristique(G.nodes[cost[2]], G.nodes[end])
                prevheur = get_heuristique(G.nodes[cost[1]], G.nodes[end])
                heuristic = np.array(cost[0]) + nextheur - prevheur
                if np.all(np.any(np.array(costs[end].weights.tolist())<heuristic, axis=1)):
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
                if v not in costs.keys():
                    costs[v] = np.recarray(1, dtype=self.cost_dtype)
                    costs[v][0] = nextcost
                    nadirs[v] = nextweight
                    updated = True
                else:
                    if nextweight[0] > nadirs[v][0]*1.2:
                        continue
                    costs[v], updated, nadirs[v] = self.try_add_new_cost(costs[v], nextcost, self.pareto_front, nadirs[v])
                if updated:
                    if v == end:
                        continue
                    #draw_add_graph(gdraw,cost[2], G.nodes[cost[2]],v, G.nodes[v], counterid)
                    nextheurupdated = get_heuristique(G.nodes[v], G.nodes[end])
                    nextheuristic = nextweight + nextheurupdated#Heuristique du prochain noeud à visiter
                    nextheuristic = nextheuristic.tolist()
                    #heapq.heappush(queue, [nextheuristic, nextcost])
                    queue.add(nextheuristic, nextcost)
        print(costs[end])
        return costs[end]
    

    def a_star_ndtree(self, G: nx.Graph, start, end):
        trees = {}
        #gdraw = nx.Graph()
        start_heuristic = get_heuristique(G.nodes[start], G.nodes[end])
        start_cost = np.array([0 for _ in range(self.nb_criteria)])
        
        to_add_queue = (start_cost + start_heuristic, -1, start, -1, 0)
        trees[start] = ndtree()
        #start_point = np.recarray((1,), dtype=self.cost_dtype)
        start_point = [start_cost, -1, start, -1, 0]
        trees[start].update_tree(start_point)

        G.add_node(-1, label = "Dummy", heuristique = 0)
        queue = PrioritySet()
        queue.add(to_add_queue[0], to_add_queue)
        #heapq.heappush(queue, [to_add_queue[0], to_add_queue])
        
        counterid = 0
        while queue.heap:
            #Pop le noeud courant et récupère son cout associé
            queued = queue.pop()
            #queued = heapq.heappop(queue)
            
            #print("NB NOEUDS DANS QUEUE:{}".format(len(queue)))
            #print(queued)
            cost = queued[1] #([c_v1 + heur_v,..., c_vn + heur_v], u, v, prevedgeid, curedgeid)
            #print("CURRENT ESTIMATED DISTANCE: {}".format(get_heuristique(G.nodes[cost[2]], G.nodes[end])))
            if end in trees.keys():  #Si le noeud terminal a été atteint, verifier si le noeud courant est strictement dominé ou pas par les vecteurs couts déjà existants
                #print("NOEUD TERMINAL TROUVE")
                nextheur = get_heuristique(G.nodes[cost[2]], G.nodes[end])
                prevheur = get_heuristique(G.nodes[cost[1]], G.nodes[end])
                heuristic = np.array(cost[0]) + nextheur - prevheur
                if np.all(trees[end].root.nadir_point<heuristic):
                    continue
                var_stop = False
                for c in trees[end].root.points_list:
                    if np.all(c[0]<heuristic):
                        var_stop = True
                        break
                if var_stop:
                    continue
                #costs = trees[end].root.points_list
                #print("costs", costs, type(costs), type(costs[0]))
            

            #Visiter tout les voisins du noeud courant
            for _, v, data in G.edges(cost[2], data = True):
                #Données des aretes voisines retourné en 3-tuple (u, v, ddict[data])
                updated = False
                counterid += 1
                prevheurvisited = get_heuristique(G.nodes[cost[2]], G.nodes[end])
                curweight = np.array(queued[0]) - prevheurvisited
                nextweight =  curweight + data['weight']#Cout du prochain noeud à visiter
                nextcost = (nextweight, cost[2], v, cost[4], counterid)
                #print(v,nextweight)
                if v not in trees.keys():
                    trees[v] = ndtree()
                    #point = np.recarray(1, dtype=self.cost_dtype)
                    trees[v].update_tree(nextcost)
                    updated = True
                else: #try_add_new_cost_ndtree(self, tree, newcost)
                    '''
                    if nextweight[0] > trees[v].root.nadir_point[0]*1.2:
                        continue
                    '''
                    updated = self.try_add_new_cost_ndtree(trees[v], nextcost)
                #print(updated)
                if updated:
                    if v == end:
                        #trees[end].show()
                        continue
                    #draw_add_graph(gdraw,cost[2], G.nodes[cost[2]],v, G.nodes[v], counterid)
                    nextheurupdated = get_heuristique(G.nodes[v], G.nodes[end])
                    nextheuristic = nextweight + nextheurupdated#Heuristique du prochain noeud à visiter
                    nextheuristic = nextheuristic.tolist()
                    #heapq.heappush(queue, [nextheuristic, nextcost])
                    queue.add(nextheuristic, nextcost)
        costs = trees[end].root.points_list
        print(costs)
        del trees
        
    
    
