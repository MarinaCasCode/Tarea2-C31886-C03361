"""
recursos.py — Problema b) de distribución de un recurso.

Interfaz que espera prueba.py:
  DistribucionRecursos(matriz, recursos, itemes)
      matriz: tabla [0..recursos][1..itemes]; matriz[i][j] = ganancia de asignar
      i unidades del recurso al ítem j.
  SolucionDistribucion: .distribucion[i] (1-indexado), .ganancia,
                        .soluciones_factibles.

(pendiente) faltan implementar los 3 métodos de búsqueda.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class SolucionDistribucion:
    """Solución de distribución. distribucion[i] (1-indexado) = recursos al ítem i."""
    distribucion: List[int]
    ganancia: int
    soluciones_factibles: int = 0


class DistribucionRecursos:
    """Problema de distribución de un recurso."""

    def __init__(self, matriz: List[List[int]], recursos: int, itemes: int):
        self.matriz = matriz
        self.recursos = recursos
        self.itemes = itemes

    def busqueda_greedy(self) -> SolucionDistribucion:
        raise NotImplementedError("Recursos greedy: pendiente de implementar")

    def busqueda_exhaustiva_pura(self) -> SolucionDistribucion:
        raise NotImplementedError("Recursos exhaustiva pura: pendiente de implementar")

    def busqueda_exhaustiva_ra(self) -> SolucionDistribucion:
        raise NotImplementedError("Recursos R&A: pendiente de implementar")
