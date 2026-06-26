"""
Prueba del problema del vendedor (TSP) con el ejemplo clásico de 4 ciudades.

Matriz de distancias (simétrica, ciudades a,b,c,d = 1,2,3,4):
        a   b   c   d
    a   0  10  15  20
    b  10   0  35  25
    c  15  35   0  30
    d  20  25  30   0

El recorrido óptimo es a-b-d-c-a con costo 80
(equivalente a su reverso a-c-d-b-a). Hay 3! = 6 recorridos posibles.

Correr desde la raíz del proyecto:   python tests/test_vendedor.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vendedor import ProblemaVendedor

# Matriz 1-indexada (fila/columna 0 sin usar).
matriz = [
    [0, 0, 0, 0, 0],
    [0, 0, 10, 15, 20],
    [0, 10, 0, 35, 25],
    [0, 15, 35, 0, 30],
    [0, 20, 25, 30, 0],
]
tamano = 4
problema = ProblemaVendedor(matriz, tamano)


def ruta_texto(sol):
    return "-".join(sol.camino[i] for i in range(1, tamano + 1)) + "-a"


greedy = problema.busqueda_greedy()
pura = problema.busqueda_exhaustiva_pura()
ra = problema.busqueda_exhaustiva_ra()

print("greedy     -> costo =", greedy.costo, " ruta =", ruta_texto(greedy))
print("exhaustiva -> costo =", pura.costo, " ruta =", ruta_texto(pura),
      " evaluados =", pura.soluciones_factibles)
print("R&A        -> costo =", ra.costo, " ruta =", ruta_texto(ra),
      " evaluados =", ra.soluciones_factibles)

assert pura.costo == 80, "el recorrido óptimo cuesta 80"
assert ra.costo == 80, "R&A debe coincidir con el óptimo"
assert pura.soluciones_factibles == 6, "hay 3! = 6 recorridos posibles"
assert ra.soluciones_factibles <= pura.soluciones_factibles, "R&A no evalúa más que la pura"
assert greedy.costo >= 80, "el greedy nunca puede ser mejor que el óptimo"
assert greedy.camino[1] == "a", "el recorrido siempre arranca en la ciudad a"

print("\nOK: vendedor optimo=80 (exhaustiva y B&B coinciden); greedy =", greedy.costo, ".")
