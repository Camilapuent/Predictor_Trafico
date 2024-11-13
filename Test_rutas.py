import unittest
from rutas import generar_grafo, calcular_ruta_mas_corta

class TestRutas(unittest.TestCase):

    def test_generar_grafo(self):
        ciudad = (4.336, -74.369)
        G = generar_grafo(ciudad, 3)
        self.assertIsNotNone(G)

    def test_calcular_ruta(self):
        G = generar_grafo((4.336, -74.369), 3)
        origen = 1  # Nodo de origen
        destino = 2  # Nodo de destino
        ruta = calcular_ruta_mas_corta(G, origen, destino)
        self.assertIsInstance(ruta, list)
        self.assertGreater(len(ruta), 0)
