from flask import Flask, request
import json, math, pickle

from scipy.spatial.distance import cdist
from six.moves.urllib.request import urlopen
import requests

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
routes = [
    {#<-- fais gaffe c'est un dictionnaire
        'distance': 156, #<-- distance en mètres
        'waypoints': [(48.8971056, 2.3591416), (48.8955245, 2.3593294)]#<-- liste encore
    },
    {#<-- fais gaffe c'est un dictionnaire
        'distance': 25, #<-- distance en mètres
        'waypoints': [(48.8860190, 2.3822270), (48.8706397, 2.3612749)]#<-- liste encore
    },
    {#<-- fais gaffe c'est un dictionnaire
        'distance': 58, #<-- distance en mètres
        'waypoints': [(49.34534, 2.23542), (48.8472876, 2.3534072)]#<-- liste encore
    }
]

@app.route('/protected_cyclist_api/route')
def get_route():
    #Récupérer les paramètres de la requête
    start_address = request.args.get('start_address')
    end_address = request.args.get('end_address')
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
    #routes = dijkstra.a_star(start_node, end_node)

    #Conversion avant envoi
    for route in routes:
        new_route = dict()
        new_route['waypoints'] = route['waypoints']

        d = route['distance'] / 1000 #distance mètres to km 
        new_route['distance'] = d

        new_route['time'] = math.ceil(d / V)
        response['route'].append(new_route)

    response = json.dumps(response)
    return response

if __name__ == '__main__':
    app.run(debug=True)