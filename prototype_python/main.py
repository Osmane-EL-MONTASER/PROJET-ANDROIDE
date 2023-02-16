from flask import Flask, render_template

app = Flask(__name__, static_url_path='/static/')

# Définit une route pour la page d'accueil
@app.route('/')
def index():
    # Définit une variable user
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
