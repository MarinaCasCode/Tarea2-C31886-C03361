"""
Prueba del problema de distribución de un recurso.

R = 3 unidades, M = 2 ítems. matriz[i][j] = ganancia de dar i unidades al ítem j:

        ítem1  ítem2
  0 u     0      0
  1 u     3      2
  2 u     4      6
  3 u     5      7

Mejor reparto: 1 unidad al ítem1 (gana 3) + 2 unidades al ítem2 (gana 6) = 9.
El greedy se queda corto: el ítem1 acapara las 3 unidades (gana 5) y al ítem2
no le queda nada -> 5. Hay 10 repartos factibles (suma <= 3).

Correr desde la raíz del proyecto:   python tests/test_recursos.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from recursos import DistribucionRecursos

# matriz[i][j]: filas i = 0..3 unidades; columna 0 sin usar.
matriz = [
    [0, 0, 0],
    [0, 3, 2],
    [0, 4, 6],
    [0, 5, 7],
]
recursos = 3
itemes = 2

problema = DistribucionRecursos(matriz, recursos, itemes)

greedy = problema.busqueda_greedy()
pura = problema.busqueda_exhaustiva_pura()
ra = problema.busqueda_exhaustiva_ra()

print("greedy     -> ganancia =", greedy.ganancia, " reparto =", greedy.distribucion[1:])
print("exhaustiva -> ganancia =", pura.ganancia, " reparto =", pura.distribucion[1:],
      " evaluados =", pura.soluciones_factibles)
print("R&A        -> ganancia =", ra.ganancia, " reparto =", ra.distribucion[1:],
      " evaluados =", ra.soluciones_factibles)

assert greedy.ganancia == 5, "el greedy acapara y se queda en 5"
assert pura.ganancia == 9, "el óptimo es 9"
assert ra.ganancia == 9, "R&A debe coincidir con el óptimo"
assert pura.distribucion[1:] == [1, 2], "reparto óptimo: 1 al ítem1, 2 al ítem2"
assert pura.soluciones_factibles == 10, "hay 10 repartos factibles (suma <= 3)"
assert ra.soluciones_factibles <= pura.soluciones_factibles, "R&A no evalúa más que la pura"

print("\nOK: recursos greedy=5, optimo=9 (exhaustiva y B&B coinciden).")
