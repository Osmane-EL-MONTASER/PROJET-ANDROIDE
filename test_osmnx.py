
import osmnx as ox
import matplotlib

ox.__version__


# get a network
place = "Paris, France"
G = ox.graph_from_place(place, network_type="bike")

# save/load graph as a graphml file: this is the best way to save your model
# for subsequent work later
filepath = "./data/paris.graphml"
ox.save_graphml(G, filepath)
G = ox.load_graphml(filepath)
ox.plot_graph(G)