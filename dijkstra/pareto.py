import numpy as np



def pareto_test(point, dict_points):
    # teste si point est Pareto dominé par l'un des points de dict_points (pour la minimisation)
    # True si dominé, False sinon
    n = len(point)
    for pt in dict_points.items():
        if (pt[1]-point<0).all():
            return True
    return False


def pareto_front(dict_vect):
    # prend en entrée un dictionnaire des vecteurs de coûts
    # supprime les vecteurs Pareto dominés
    # retourne le nouveau dictionnaire, ne contenant que des vecteurs non dominés pour la relation de Pareto

    # trier le dictionnaire
    dict_sort = dict(sorted(dict_vect.items(), key=lambda item: item[1][0]))

    # créer le nouveau dictionnaire
    S = dict()
    
    for v in dict_vect.items():
        l = len(S)
        if pareto_test(v[1],S) == False:
            S[l+1] = v[1]
    return S





print(pareto_front({2:np.array([1,2]),0:np.array([2,3]),1:np.array([4,5])}))