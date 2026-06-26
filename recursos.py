"""
recursos.py — Problema b) de distribución de un recurso.

Se reparten R unidades de un recurso entre M ítems para maximizar la ganancia
total. matriz[i][j] = ganancia de asignar i unidades al ítem j (i de 0 a R).
Un reparto es factible si el total de unidades asignadas no supera R.

Interfaz que espera prueba.py:
  DistribucionRecursos(matriz, recursos, itemes)
      matriz: tabla [0..recursos][1..itemes].
      recursos = R (unidades disponibles), itemes = M (cantidad de ítems).
  SolucionDistribucion: .distribucion[j] (1-indexado, unidades dadas al ítem j),
                        .ganancia, .soluciones_factibles.

Las dos búsquedas exhaustivas solo evalúan repartos FACTIBLES (suma de unidades
<= R) y reportan cuántos repartos completos evaluaron.
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class SolucionDistribucion:
    """Solución de distribución. distribucion[j] (1-indexado) = unidades al ítem j."""
    distribucion: List[int]
    ganancia: int
    soluciones_factibles: int = 0


class DistribucionRecursos:
    """Problema de distribución de un recurso entre varios ítems."""

    def __init__(self, matriz: List[List[int]], recursos: int, itemes: int):
        self.matriz = matriz
        self.recursos = recursos
        self.itemes = itemes

    # ------------------------------------------------------------------
    # 1. BÚSQUEDA GREEDY
    # ------------------------------------------------------------------
    def busqueda_greedy(self) -> SolucionDistribucion:
        """
        Greedy: recorre los ítems en orden y a cada uno le asigna la cantidad de
        unidades que MÁS le conviene a ese ítem con el recurso que queda.

        Rápida, pero no siempre óptima (un ítem puede acaparar unidades y dejar a
        los siguientes sin recurso).
        """
        m = self.itemes
        distribucion = [0] * (m + 1)
        ganancia = 0
        restante = self.recursos

        for j in range(1, m + 1):
            mejor_x = 0
            mejor_g = self.matriz[0][j]
            for x in range(0, restante + 1):
                if self.matriz[x][j] > mejor_g:
                    mejor_g = self.matriz[x][j]
                    mejor_x = x
            distribucion[j] = mejor_x
            ganancia += mejor_g
            restante -= mejor_x

        return SolucionDistribucion(distribucion=distribucion, ganancia=ganancia)

    # ------------------------------------------------------------------
    # 2. BÚSQUEDA EXHAUSTIVA PURA
    # ------------------------------------------------------------------
    def busqueda_exhaustiva_pura(self) -> SolucionDistribucion:
        """
        Exhaustiva pura: prueba todos los repartos posibles (a cada ítem 0..lo
        que quede de recurso) y se queda con el de mayor ganancia.

        Devuelve la mejor solución y cuenta los repartos completos evaluados.
        """
        m = self.itemes
        distribucion = [0] * (m + 1)
        mejor = {"ganancia": float("-inf"), "dist": None}
        contador = [0]

        def explorar(j: int, restante: int, ganancia_actual: int):
            if j > m:
                contador[0] += 1
                if ganancia_actual > mejor["ganancia"]:
                    mejor["ganancia"] = ganancia_actual
                    mejor["dist"] = distribucion.copy()
                return
            for x in range(0, restante + 1):
                distribucion[j] = x
                explorar(j + 1, restante - x, ganancia_actual + self.matriz[x][j])
            distribucion[j] = 0

        explorar(1, self.recursos, 0)
        return SolucionDistribucion(distribucion=mejor["dist"],
                                    ganancia=mejor["ganancia"],
                                    soluciones_factibles=contador[0])

    # ------------------------------------------------------------------
    # 3. RAMIFICACIÓN Y ACOTAMIENTO
    # ------------------------------------------------------------------
    def busqueda_exhaustiva_ra(self) -> SolucionDistribucion:
        """
        Ramificación y Acotamiento.

        Igual que la exhaustiva pura, pero poda una rama cuando su COTA SUPERIOR
        optimista no supera la mejor ganancia encontrada. La cota deja que cada
        ítem que falta tome su mejor ganancia posible con el recurso restante
        (ignorando que comparten presupuesto): nunca subestima el óptimo real.

        Devuelve la mejor solución (óptima) y cuenta los repartos evaluados.
        """
        m = self.itemes
        r = self.recursos

        # max_hasta[k][u] = mejor ganancia de asignar entre 0 y u unidades al ítem k.
        max_hasta = [[0] * (r + 1) for _ in range(m + 1)]
        for k in range(1, m + 1):
            mejor_k = self.matriz[0][k]
            max_hasta[k][0] = mejor_k
            for u in range(1, r + 1):
                if self.matriz[u][k] > mejor_k:
                    mejor_k = self.matriz[u][k]
                max_hasta[k][u] = mejor_k

        distribucion = [0] * (m + 1)
        mejor = {"ganancia": float("-inf"), "dist": None}
        contador = [0]

        def cota_superior(j: int, restante: int, ganancia_actual: int) -> float:
            cota = ganancia_actual
            for k in range(j, m + 1):
                cota += max_hasta[k][restante]
            return cota

        def explorar(j: int, restante: int, ganancia_actual: int):
            if j > m:
                contador[0] += 1
                if ganancia_actual > mejor["ganancia"]:
                    mejor["ganancia"] = ganancia_actual
                    mejor["dist"] = distribucion.copy()
                return

            # Poda: si ni la cota optimista supera lo mejor, abandonar la rama.
            if cota_superior(j, restante, ganancia_actual) <= mejor["ganancia"]:
                return

            for x in range(0, restante + 1):
                distribucion[j] = x
                explorar(j + 1, restante - x, ganancia_actual + self.matriz[x][j])
            distribucion[j] = 0

        explorar(1, r, 0)
        return SolucionDistribucion(distribucion=mejor["dist"],
                                    ganancia=mejor["ganancia"],
                                    soluciones_factibles=contador[0])
