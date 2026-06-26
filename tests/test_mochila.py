"""
Prueba del problema de la mochila (0/1) con el ejemplo de la diapositiva del profe.

Datos (capacidad 15):
  ítem:       1   2   3   4   5   6    7   8   9  10
  peso:      10  12   3   4   1   8   11   4   9   6
  beneficio:  5   4   5   8   3   2    6   7  10   8

Resultados:
  - greedy (beneficio/peso) -> 23, ítems {3,4,5,8}  (lo que muestra la diapositiva)
  - óptimo (exhaustiva / B&B) -> 26, ítems {4,5,8,10}
    (greedy se queda corto: sirve para mostrar que greedy NO siempre es óptimo)

Correr desde la raíz del proyecto:   python tests/test_mochila.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mochila import ProblemaMochila

peso = [10, 12, 3, 4, 1, 8, 11, 4, 9, 6]
beneficio = [5, 4, 5, 8, 3, 2, 6, 7, 10, 8]
capacidad = 15
tamano = 10

problema = ProblemaMochila(peso, beneficio, capacidad, tamano)


def seleccionados(sol):
    return [i for i in range(1, tamano + 1) if sol.mochila[i]]


greedy = problema.busqueda_greedy()
pura = problema.busqueda_exhaustiva_pura()
ra = problema.busqueda_exhaustiva_ra()

print("greedy     -> beneficio =", greedy.beneficio, " items =", seleccionados(greedy))
print("exhaustiva -> beneficio =", pura.beneficio, " items =", seleccionados(pura),
      " evaluadas =", pura.soluciones_factibles)
print("R&A        -> beneficio =", ra.beneficio, " items =", seleccionados(ra),
      " evaluadas =", ra.soluciones_factibles)

assert greedy.beneficio == 23, "el greedy de la diapositiva da 23"
assert seleccionados(greedy) == [3, 4, 5, 8], "ítems del greedy"
assert pura.beneficio == 26, "el óptimo es 26"
assert ra.beneficio == 26, "B&B debe coincidir con el óptimo"
assert seleccionados(pura) == [4, 5, 8, 10], "ítems óptimos"
assert seleccionados(ra) == [4, 5, 8, 10], "ítems óptimos (B&B)"

print("\nOK: mochila greedy=23, optimo=26 (exhaustiva y B&B coinciden).")
