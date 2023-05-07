import numpy as np
import heapq
import matplotlib.pyplot as plt
import copy


DEFAULT_SET_SIZE = 2
DEFAULT_NUMBER_OF_CHILDREN = 2

class ndtree:

    class nodes:

        def __init__(self, parent = None, children = set(), points_list = set(), ideal_point = None, nadir_point = None, level = 0):
            self.parent = parent
            self.children = children
            self.points_list = points_list
            self.ideal_point = ideal_point
            self.nadir_point = nadir_point
            self.level = level

    def __init__(self, root = None, set_size = DEFAULT_SET_SIZE, max_children = DEFAULT_NUMBER_OF_CHILDREN):
        self.root = None
        self.set_size = set_size
        self.max_children = max_children

    def update_tree(self, y):
        if self.root is None:
            points_list = [y]
            self.root = self.nodes(points_list = points_list, ideal_point=y, nadir_point=y)
        else:
            n = self.root
            if self.update_node(n, y):
                self.insert(n, y)
        #tree.show()

    def delete_sub_tree(self, n):
        n.points_list = set()
        if n.parent is None:
            return
        self.delete_sub_points(n.parent, n.points_list)
        n.parent.children.remove(n)
    
    def delete_sub_points(self, n, points):
        for point in points:
            self.remove(n.points_list, point)
        self.delete_sub_points(n.parent, n.points_list)

    def update_node(self, n, y):
        if np.all(y>=n.nadir_point):
            return False
        elif np.all(y<=n.ideal_point):
            self.delete_sub_tree(n)
            return True
        elif np.all(y<=n.nadir_point) or np.all(y>=n.ideal_point):
            if len(n.children) == 0:
                temp_copy = n.points_list.copy()
                for z in temp_copy:
                    if np.all(z<=y):
                        return False
                    elif np.all(y<=z) and np.any(y<z):
                        self.remove(n.points_list, z)
            else:
                temp_copy = n.children.copy()
                
                for child in temp_copy:
                    if not self.update_node(child, y):
                        return False
                    else:
                        if len(child.points_list) == 0:
                            n.children.remove(child)
                            child.parent = None
                
                if len(n.children) == 1:
                    child = list(n.children)[-1]
                    temp = n
                    n = child
                    n.parent = temp.parent
                    if temp == self.root:
                        n == self.root
                    del temp
        return True

    def insert(self, n, y):
        n.points_list.append(y)
        if len(n.children) == 0:
            #n.points_list.append(y)
            self.update_ideal_nadir(n,y)
            if len(n.points_list) > self.set_size:
                self.split(n)
                return
        
        else:
            closest = np.inf
            for child in n.children:
                middlePoint = (np.array(child.ideal_point) + np.array(child.nadir_point))/2
                if np.linalg.norm(middlePoint-y) < closest:
                    closest = np.linalg.norm(middlePoint-y)
                    bestchild = child
            self.insert(bestchild, y)
      
    def remove(self, n_list,z):
        for i in range(len(n_list)):
            if np.all(n_list[i] == z):
                del n_list[i]
                return
            
    def split(self,n):
        arr = np.array(n.points_list)
        mean_dist = np.mean(np.linalg.norm(arr[:,None,:] - arr[None,:,:], axis=-1),axis=1) #distance moyenne d'un point à tous les autres points
        z = arr[np.argmax(mean_dist)] # point ayant la plus grande distance moyenne à tous les autres points
        n_list = copy.deepcopy(n.points_list)
        n_prime = self.nodes(parent=n, nadir_point=list(z), ideal_point=list(z), children = set(), level = n.level+1 )
        n.children.add(n_prime)
        n_prime.points_list = [z]
        self.remove(n_list, z)

        while len(n.children) < self.max_children and len(n_list) != 0:
            ''' Find the point z with the highest average euclidean distance
            to all points in all children of n'''
            # on crée le np.array arr contenant tous les points restant dans L(n)
            new_arr = np.array(n_list) 
            mean_dist = np.mean(np.linalg.norm(new_arr[:,None,:] - arr[None,:,:], axis=-1),axis=1)
            z = new_arr[np.argmax(mean_dist)]

            n_2 = self.nodes(parent=n, points_list = [], children = set(), level = n.level+1)
            n.children.add(n_2)
            n_2.points_list.append(z)
            n_2.nadir_point, n_2.ideal_point = z, z
            self.remove(n_list, z)

        while len(n_list) != 0:
            z = n_list[0]
            closest = None
            for child in n.children:
                middlePoint = (np.array(child.ideal_point) + np.array(child.nadir_point))/2
                if closest is None:
                    closest = np.linalg.norm(middlePoint-z)
                    bestchild = child
                else:
                    if np.linalg.norm(middlePoint-z) < closest:
                        closest = np.linalg.norm(middlePoint-z)
                        bestchild = child
            bestchild.points_list.append(z)
            self.update_ideal_nadir(bestchild,z)
            self.remove(n_list, z)
        del n_list
        

    def update_ideal_nadir(self, n, y):
        change = False 
        concat = np.zeros((3,np.shape(y)[0]))
        concat[0,:] = n.ideal_point
        concat[1,:] = n.nadir_point
        concat[2,:] = y
        n.ideal_point = np.amin(concat,axis=0)
        n.nadir_point = np.amax(concat, axis=0)
        if np.any(concat[0,:]!=n.ideal_point) or np.any(concat[1,:]!=n.nadir_point):
            change = True

        if change:
            if n != self.root:
                n_p = n.parent
                self.update_ideal_nadir(n_p, y)

                
    def show(self):
        fig, ax = plt.subplots(figsize=(4, 4))
        self._plot_node(ax,self.root)
        ax.axis('off')
        plt.show()
    
    def _plot_node(self, ax, node, x=0, y=0):
        if node is None:
            return
        
        # Compute the position of the node
        dx = 1 / 2 ** (node.level + 1)
        node_x = x 
        node_y = y 
        
        # Draw the node
        ax.plot(node_x, node_y, 'o', markersize=10, color = "blue")
        
        if len(node.children) == 0:
            txt = []
            for point in node.points_list:
                txt.append(tuple(point))
            ax.text(node_x, node_y, txt, ha='center', va='center')
        
        # Recursively draw the child nodes
        for ind, child in enumerate (node.children):
            child_x = x + dx * (2 * ind + 1 - len(node.children)) / 2
            child_y = y - 1
            ax.plot([node_x, child_x], [node_y, child_y], '-', color='gray')
            self._plot_node(ax, child, child_x, child_y)
    
        
# Test

tree = ndtree()
'''
for y in [np.array([5,9,2]),np.array([5,8,3]),np.array([3,4,5]),np.array([0,6,3]),np.array([8,7,1])]:
    tree.update_tree(y)
'''

tree.update_tree(np.array([0,0]))

for i in range(8):
    tree.update_tree(np.array([2**i,-2**i]))


tree.show()

