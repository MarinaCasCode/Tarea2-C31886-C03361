"""
vendedor.py — Problema d) del vendedor (TSP).

Confirmado por el código prueba.py del profe:
  - el recorrido es un CICLO (regresa a la ciudad de origen),
  - la matriz de distancias es SIMÉTRICA, con la diagonal en 0,
  - un -1 representa "no hay camino" (según el enunciado).

Interfaz que espera prueba.py:
  ProblemaVendedor(matriz, tamano)        matriz 1-indexada NxN.
  SolucionVendedor: .camino[i] (1-indexado, letra de ciudad), .costo,
                    .soluciones_factibles.

(pendiente) faltan implementar los 3 métodos de búsqueda.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class SolucionVendedor:
    """Solución del vendedor. camino[i] (1-indexado) = letra de la ciudad i-ésima."""
    camino: List[str]
    costo: int
    soluciones_factibles: int = 0


class ProblemaVendedor:
    """Problema del vendedor viajero (TSP)."""

    def __init__(self, matriz: List[List[int]], tamano: int):
        self.matriz = matriz
        self.tamano = tamano

    def busqueda_greedy(self) -> SolucionVendedor:
        raise NotImplementedError("Vendedor greedy: pendiente de implementar")

    def busqueda_exhaustiva_pura(self) -> SolucionVendedor:
        raise NotImplementedError("Vendedor exhaustiva pura: pendiente de implementar")

    def busqueda_exhaustiva_ra(self) -> SolucionVendedor:
        raise NotImplementedError("Vendedor R&A: pendiente de implementar")
