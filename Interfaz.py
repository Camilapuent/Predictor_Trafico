import tkinter as tk
from rutas import generar_grafo, calcular_ruta_mas_corta
from mapa import mostrar_mapa

def interfaz_usuario():
    ventana = tk.Tk()
    ventana.title("Guía de Rutas en Fusagasugá")

    # Elementos de la interfaz (por ejemplo, botones, entradas, etiquetas, etc.)
    label_origen = tk.Label(ventana, text="Seleccione el origen:")
    label_origen.pack()

    # (El código para los botones, entradas y la lógica de cálculo va aquí)

    ventana.mainloop()
