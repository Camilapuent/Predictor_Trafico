import folium
from folium.plugins import AntPath

def mostrar_mapa(G, ruta, locations, archivo_nombre="mapa.html"):
    m = folium.Map(location=[4.336, -74.369], zoom_start=14)

    # Añadir los puntos de interés
    for key, (name, coords) in locations.items():
        folium.Marker(location=coords, popup=name).add_to(m)

    # Dibujar la ruta
    route_coords = [(G.nodes[node]["y"], G.nodes[node]["x"]) for node in ruta]
    AntPath(route_coords, color="blue", weight=5, opacity=0.7).add_to(m)

    m.save(archivo_nombre)
