import numpy as np

DEFAULT_SET_SIZE = 10
DEFAULT_NUMBER_OF_CHILDREN = 2

class ndtree:

    class nodes:

        def __init__(self, parent = None, children = set(), points_set = set(), ideal_point = None, nadir_point = None):
            self.parent = parent
            self.children = children
            self.points_set = points_set
            self.ideal_point = ideal_point
            self.nadir_point = nadir_point

    def __init__(self, root = None, set_size = DEFAULT_SET_SIZE, max_children = DEFAULT_NUMBER_OF_CHILDREN):
        self.root = None
        self.set_size = set_size
        self.max_children = max_children
        pass

    def update_tree(self, y):
        if self.root is None:
            self.root = self.nodes(points_set = y)
        else:
            n = self.root
            if self.update_node(n, y):
                self.insert(n, y)

    def delete_sub_tree(self, n):
        self.delete_sub_points(n.parent, n.points_set)
        n.parent.children.remove(n)
    
    def delete_sub_points(self, n, points):
        if n.parent is None:
            return
        for point in points:
            n.points_set.remove(point)
        self.delete_sub_points(n.parent, n.points_set)

    def update_node(self, n, y):
        if np.all(y>=n.nadir_point):
            return False
        elif np.all(y<=n.ideal_point):
            self.delete_sub_tree(n)
        elif np.all(y<=n.nadir_point) or np.all(y>=n.ideal_point):
            if len(n.children) == 0:
                temp_copy = n.points_set.copy()
                for z in temp_copy:
                    if np.all(z<=y):
                        return False
                    elif np.all(y<=z) and np.any(y<z):
                        n.points_set.remove(z)
            else:
                temp_copy = n.children()
                for child in temp_copy:
                    if not self.update_node(child, y):
                        return False
                    else:
                        if len(child.points_set) == 0:
                            n.children.remove(child)
                if len(n.children) == 1:
                    n.parent.children.add(list(n.children)[-1])
                    n.parent.children.remove(n)
        else:
            pass
        return True

    def insert(self, n, y):
        if len(n.children) == 0:
            n.points_set.add(y)
            self.update_ideal_nadir(n,y)
            if len(n.children) > self.set_size:
                self.split(n)
        else:
            closest = None
            for child in n.children:
                middlePoint = (np.array(child.ideal_point) + np.array(child.nadir_point))/2
                if closest is None:
                    closest = np.linalg.norm(middlePoint-y)
                    bestChild = child
                else:
                    if np.linalg.norm(middlePoint-y) < closest:
                        bestchild = child
            self.insert(bestchild, y)



    def split(self,n):
        arr = np.array(list(n.points_set))
        mean_dist = np.mean(np.linalg.norm(arr[:,None,:] - arr[None,:,:], axis=-1))
        z = arr[np.argmax(mean_dist)]
        temp = set()
        n_prime = self.nodes(parent=n, points_set=temp.add(tuple(z.flatten())))
        n.children.add(n_prime)
        self.update_ideal_nadir(n_prime, z)
        n.points_set.remove(z)

        while len(n.children) < self.max_children:
            arr = np.array(list(n.points_set)) 
            mean_dist = np.mean(np.linalg.norm(arr[:,None,:] - arr[None,:,:], axis=-1))
            z = arr[np.argmax(mean_dist)]

            n_prime = self.nodes(parent=n)
            n_prime.points_set.add(z)
            self.update_ideal_nadir(n_prime, z)
            n.points_set.remove(z)

        
        

    def update_ideal_nadir(self, n, y):
        change = False
        for i in range(len(y)):
            if y[i]<n.ideal_point[i]:
                n.ideal_point[i] = y[i]
                change = True
            
            elif y[i]>n.nadir_point[i]:
                n.nadir_point[i] = y[i]
                change = True
        if change:
            if n == self.root:
                np = n.parent
                self.update_ideal_nadir(np, y)