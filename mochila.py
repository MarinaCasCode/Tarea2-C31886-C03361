"""
mochila.py — Problema c) de la mochila (0/1).

Datos confirmados en clase (16 jun):
  - cada elemento tiene PESO y BENEFICIO por separado (mochila 0/1),
  - capacidad máxima fija,
  - greedy: ordena por razón beneficio/peso (mayor primero) y mete el elemento
    entero mientras quepa; si no cabe, se salta.

Interfaz que espera prueba.py:
  ProblemaMochila(peso, beneficio, capacidad, tamano)
      peso, beneficio: listas 0-indexadas de longitud 'tamano'.
  SolucionMochila: .mochila[i] (1-indexado, bool), .beneficio, .soluciones_factibles.

(pendiente) faltan implementar los 3 métodos de búsqueda.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class SolucionMochila:
    """Solución de la mochila. mochila[i] (1-indexado) = True si va el ítem i."""
    mochila: List[bool]
    beneficio: int
    soluciones_factibles: int = 0


class ProblemaMochila:
    """Problema de la mochila 0/1."""

    def __init__(self, peso: List[int], beneficio: List[int],
                 capacidad: int, tamano: int):
        self.peso = peso
        self.beneficio = beneficio
        self.capacidad = capacidad
        self.tamano = tamano

    def busqueda_greedy(self) -> SolucionMochila:
        raise NotImplementedError("Mochila greedy: pendiente de implementar")

    def busqueda_exhaustiva_pura(self) -> SolucionMochila:
        raise NotImplementedError("Mochila exhaustiva pura: pendiente de implementar")

    def busqueda_exhaustiva_ra(self) -> SolucionMochila:
        raise NotImplementedError("Mochila R&A: pendiente de implementar")
