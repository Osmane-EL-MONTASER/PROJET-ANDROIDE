from flask import Flask, render_template

import json

app = Flask(__name__, static_url_path='/static/')

# Définit une route pour la page d'accueil
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_route')
def generate_route():
    #Un chemin que j'ai fait au pif avec les vrais waypoints OSM.
    waypoints = [(48.8461163, 2.3545259), 
                 (48.8472876, 2.3534072), 
                 (48.8547400, 2.3475545)]

    return json.dumps(waypoints)


if __name__ == '__main__':
    app.run(debug=True)


#Je veux une liste qui comporte toutes les routes possibles :
routes = [
    {#<-- fais gaffe c'est un dictionnaire
        'distance': 156, #<-- distance en mètres
        'waypoints': [(49.34534, 2.23542), (48.8472876, 2.3534072)]#<-- liste encore
    },
    {#<-- fais gaffe c'est un dictionnaire
        'distance': 156, #<-- distance en mètres
        'waypoints': [(49.34534, 2.23542), (48.8472876, 2.3534072)]#<-- liste encore
    },
    {#<-- fais gaffe c'est un dictionnaire
        'distance': 156, #<-- distance en mètres
        'waypoints': [(49.34534, 2.23542), (48.8472876, 2.3534072)]#<-- liste encore
    }
]