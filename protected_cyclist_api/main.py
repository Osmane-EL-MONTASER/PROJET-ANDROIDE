from flask import Flask, request
import json, math, pickle

from scipy.spatial.distance import cdist
from six.moves.urllib.request import urlopen
import requests

from astar_eps import astar_eps

app = Flask(__name__)

node_pos = pickle.load(open('node_pos.pickle', 'rb'))

def get_pos_from_street(name: str, city:str):
    strForQuery = name.replace(' ', '+')
    url = 'https://nominatim.openstreetmap.org/search?q=' + strForQuery + f'%2C+{city}&format=geojson'
    response = requests.get(url)
    query = json.loads(response.content.decode('utf-8'))
    
    return [query['features'][0]['geometry']['coordinates'][0], query['features'][0]['geometry']['coordinates'][1]]

#Vitesse moyenne d'un vélo 15 km/h = 0.004167 km/s
V = 0.004167

@app.route('/protected_cyclist_api/route')
def get_route():
    file = open("paris_graph_with_weights.pickle", "rb")
    graphParis = pickle.load(file)
    
    #Récupérer les paramètres de la requête
    start_address = str(request.args.get('start_address'))
    end_address = str(request.args.get('end_address'))
    max_distance = float(request.args.get('max_distance'))
    eps = float(request.args.get('eps'))
    print(start_address, end_address)
    #Notre structure de données comportant les routes
    response = dict()
    response['route'] = []
    
    
    #Convertir les adresses en points de notre graphe multi-objectif
    start_pos = get_pos_from_street(start_address, 'Paris')
    end_pos = get_pos_from_street(end_address, 'Paris')

    response['start_pos'] = start_pos
    response['end_pos'] = end_pos

    distances_from_start = cdist(node_pos[['lat', 'lon']], [start_pos])
    distances_from_end = cdist(node_pos[['lat', 'lon']], [end_pos])

    start_node = node_pos.index[distances_from_start.argmin()]
    end_node = node_pos.index[distances_from_end.argmin()]

    #TO-DO Appeler a_star multi-objectif
    print(start_node, end_node)
    algo = astar_eps(graphParis, 4)
    resultastar = algo.a_star(graphParis, start_node, end_node, max_distance, eps)
    routes = algo.get_all_possible_path(resultastar, graphParis, end_node)

    print(routes)

    #Conversion avant envoi
    for route in routes:
        new_route = dict()
        route['waypoints'].reverse()
        new_route['waypoints'] = route['waypoints']

        d = route['distance'] / 1000 #distance mètres to km 
        new_route['distance'] = d

        new_route['time'] = math.ceil(d / V)
        response['route'].append(new_route)

    response = json.dumps(response)
    return response

if __name__ == '__main__':
    app.run(debug=True)