"""
Prueba rápida del código de Asignación 1 a 1 (provisto por el profe).

Verifica con un caso chiquito de respuesta conocida a mano:
  - el óptimo es 17 (asignación 1->2, 2->1, 3->3),
  - el greedy se queda corto (da 11) -> sirve para mostrar que greedy NO
    siempre encuentra el óptimo,
  - la búsqueda exhaustiva pura evalúa 3! = 6 soluciones completas.

Correr desde la raíz del proyecto:   python tests/test_assignment.py
"""

import os
import sys

# Permite importar src/ al correr el archivo directamente.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.assignment import ProblemaAsigna1a1

# Matriz 1-indexada: la posición 0 no se usa (igual que en el código del profe).
# matriz[item][recurso] = ganancia de asignar ese item a ese recurso.
matriz = [
    [0, 0, 0, 0],
    [0, 9, 8, 1],
    [0, 8, 1, 1],
    [0, 1, 1, 1],
]
problema = ProblemaAsigna1a1(matriz, tamano=3)

greedy = problema.busqueda_greedy()
exhaustiva = problema.busqueda_exhaustiva_pura()
ra = problema.busqueda_exhaustiva_ra()

print("greedy     -> ganancia =", greedy.ganancia, "  asignacion =", greedy.asignado[1:])
print("exhaustiva -> ganancia =", exhaustiva.ganancia, "  asignacion =", exhaustiva.asignado[1:],
      "  evaluadas =", exhaustiva.soluciones_factibles)
print("R&A        -> ganancia =", ra.ganancia, "  asignacion =", ra.asignado[1:],
      "  evaluadas =", ra.soluciones_factibles)

assert greedy.ganancia == 11, "el greedy debería dar 11 en este caso"
assert exhaustiva.ganancia == 17, "el óptimo es 17"
assert ra.ganancia == 17, "R&A debe coincidir con el óptimo de la exhaustiva"
assert exhaustiva.soluciones_factibles == 6, "la exhaustiva pura evalúa 3! = 6 soluciones"

print("\nOK: las 3 técnicas corren y dan los valores esperados.")
