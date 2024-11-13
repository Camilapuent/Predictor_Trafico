import osmnx as ox
import networkx as nx

def generar_grafo(ciudad, distancia_km):
    location_point = ciudad
    G = ox.graph_from_point(location_point, dist=distancia_km * 1000, network_type="drive")
    return G

def calcular_ruta_mas_corta(G, origen, destino):
    ruta = nx.shortest_path(G, source=origen, target=destino, weight="length")
    return ruta
