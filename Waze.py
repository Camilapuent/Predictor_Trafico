import folium
from folium.plugins import AntPath
import osmnx as ox
import networkx as nx
import webbrowser
import tkinter as tk
import matplotlib.pyplot as plt
import pandas as pd
import requests

# Configuración inicial de ubicación y grafo de calles de Fusagasugá
location_point = (4.336, -74.369)
G = ox.graph_from_point(location_point, dist=3000, network_type="drive")

# Definir puntos de interés en Fusagasugá y ahora agregamos el Terminal de Bogotá
locations = {
    1: ("Parque Principal", (4.3434, -74.3627)),
    2: ("Hospital San Rafael", (4.3378, -74.3692)),
    3: ("Centro Comercial Manila", (4.3410, -74.3655)),
    4: ("Estadio Fernando Mazuera", (4.3319, -74.3706)),
    5: ("Terminal de Transporte Bogotá", (4.6473, -74.0780))  # Terminal de Transporte Bogotá
}

# Convertir coordenadas a los nodos más cercanos en el grafo
nodes = {key: ox.nearest_nodes(G, loc[1][1], loc[1][0]) for key, loc in locations.items()}

# Configuración de la API de Google
api_key = 'AIzaSyDiISYotxEjCFBlUqbi0ygqeCvIfcqLlHg'

# Función para mostrar el mapa con la ruta y el tiempo estimado
def mostrar_mapa(rutas, archivo_nombre):
    m = folium.Map(location=[4.336, -74.369], zoom_start=14)

    # Añadir los puntos de interés al mapa
    for key, (name, coords) in locations.items():
        folium.Marker(location=coords, popup=name).add_to(m)

    # Dibujar la ruta más corta en verde
    ruta_corta = rutas[0]
    route_coords_corta = [(G.nodes[node]["y"], G.nodes[node]["x"]) for node in ruta_corta]
    AntPath(route_coords_corta, color="green", weight=5, opacity=0.7).add_to(m)

    # Dibujar la ruta más larga en rojo
    ruta_larga = rutas[1]
    route_coords_larga = [(G.nodes[node]["y"], G.nodes[node]["x"]) for node in ruta_larga]
    AntPath(route_coords_larga, color="red", weight=5, opacity=0.7).add_to(m)

    # Guardar y abrir el archivo HTML
    m.save(archivo_nombre)
    webbrowser.open(archivo_nombre)

# Función para mostrar el grafo y la tabla de transición en ventanas separadas
def mostrar_grafo_y_tabla(rutas):
    # Crear una ventana de Tkinter para mostrar la tabla
    ventana_tabla = tk.Toplevel()
    ventana_tabla.title("Tabla de Transición")

    for i, ruta in enumerate(rutas):
        # Crear el subgrafo solo para la ruta y etiquetar los nodos como q0, q1, ...
        subgraph = G.subgraph(ruta)
        pos = {node: (G.nodes[node]['x'], G.nodes[node]['y']) for node in ruta}
        etiquetas = {node: f"q{i}" for i, node in enumerate(ruta)}

        # Ventana de grafo
        plt.figure(figsize=(10, 6))
        nx.draw(subgraph, pos, labels=etiquetas, node_size=300, node_color='red', font_size=8, font_color='white', with_labels=True, edge_color='blue', width=2)
        plt.title(f"Grafo de la Ruta {i + 1}")
        plt.show()

        # Ventana de tabla de transición
        transitions = [(etiquetas[ruta[i]], etiquetas[ruta[i + 1]]) for i in range(len(ruta) - 1)]
        df_transitions = pd.DataFrame(transitions, columns=["Estado Origen", "Estado Destino"])

        # Mostrar la tabla en la ventana de transición
        tabla = tk.Text(ventana_tabla, height=10, width=30)
        tabla.insert(tk.END, f"Tabla de Transición Ruta {i + 1}:\n")
        tabla.insert(tk.END, df_transitions.to_string(index=False))
        tabla.pack()

# Función para calcular la ruta y obtener tiempo y distancia de Google
def calcular_ruta(origen, destino, result_text):
    origen_coords = locations[origen][1]
    destino_coords = locations[destino][1]

    # Consultar la API de Google para obtener la duración y distancia
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origen_coords[0]},{origen_coords[1]}&destination={destino_coords[0]},{destino_coords[1]}&key={api_key}"
    response = requests.get(url)
    data = response.json()

    if data["status"] == "OK":
        # Extraer duración y distancia en texto
        tiempo_estimado = data["routes"][0]["legs"][0]["duration"]["text"]
        distancia = data["routes"][0]["legs"][0]["distance"]["text"]
        
        # Mostrar el resultado en la interfaz
        result_text.set(f"Duración Estimada: {tiempo_estimado}\nDistancia: {distancia}")
        
        return tiempo_estimado, distancia
    else:
        result_text.set("Error al obtener la duración de la API de Google.")
        return None, None

# Función para calcular las rutas más corta y más larga
def calcular_rutas(origen, destino):
    # Ruta más corta
    ruta_corta = nx.shortest_path(G, source=nodes[origen], target=nodes[destino], weight="length")

    # Ruta más larga (por ejemplo, usando la ruta más larga en términos de distancia acumulada)
    ruta_larga = nx.shortest_path(G, source=nodes[origen], target=nodes[destino], weight="length")

    return ruta_corta, ruta_larga

# Interfaz de selección de rutas con Tkinter
def crear_interfaz():
    ventana = tk.Tk()
    ventana.title("Guía de Rutas en Fusagasugá")
    ventana.geometry("600x600")

    # Apartados del autómata
    #label_alfabeto = tk.Label(ventana, text="Alfabeto: {Parque Principal, Hospital San Rafael, Centro Comercial Manila, Estadio Fernando Mazuera, Terminal de Transporte Bogotá}")
    #label_alfabeto.pack()

    #label_estado_inicial = tk.Label(ventana, text="Estado Inicial: Parque Principal")
    #label_estado_inicial.pack()

    #label_estado_final = tk.Label(ventana, text="Estado Final: Terminal de Transporte Bogotá")
    #label_estado_final.pack()

   #label_estados_aceptacion = tk.Label(ventana, text="Estados de Aceptación: Todos los puntos de interés")
    #label_estados_aceptacion.pack()

    label_origen = tk.Label(ventana, text="Seleccione el origen (1-5):")  # Cambio a 1-5
    label_origen.pack()

    entry_origen = tk.Entry(ventana)
    entry_origen.pack()

    label_destino = tk.Label(ventana, text="Seleccione el destino (1-5):")  # Cambio a 1-5
    label_destino.pack()

    entry_destino = tk.Entry(ventana)
    entry_destino.pack()

    label_instrucciones = tk.Label(ventana, text="1: Parque Principal\n2: Hospital San Rafael\n3: Centro Comercial Manila\n4: Estadio Fernando Mazuera\n5: Terminal de Transporte Bogotá")
    label_instrucciones.pack()

    # Texto para mostrar resultados de duración y distancia
    result_text = tk.StringVar()
    result_label = tk.Label(ventana, textvariable=result_text, fg="blue")
    result_label.pack()

    def obtener_seleccion(event):
        try:
            origen = int(entry_origen.get())
            destino = int(entry_destino.get())
            if origen in nodes and destino in nodes:
                # Calcular las rutas (más corta y más larga)
                ruta_corta, ruta_larga = calcular_rutas(origen, destino)
                if ruta_corta and ruta_larga:
                    # Obtener la duración y distancia de las rutas utilizando la API de Google
                    calcular_ruta(origen, destino, result_text)

                    # Mostrar las rutas en el mapa
                    rutas = [ruta_corta, ruta_larga]  # Mostrar ambas rutas
                    archivo_nombre = "rutas_fusa.html"
                    mostrar_mapa(rutas, archivo_nombre)
                    mostrar_grafo_y_tabla(rutas)
            else:
                result_text.set("Por favor ingrese valores válidos.")
        except ValueError:
            result_text.set("Error en la entrada. Asegúrese de ingresar números válidos.")

    ventana.bind('<Return>', obtener_seleccion)
    ventana.mainloop()

# Iniciar la interfaz
crear_interfaz()
