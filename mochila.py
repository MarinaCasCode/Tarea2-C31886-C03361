"""
mochila.py — Problema c) de la mochila (0/1).

Datos confirmados:
  - cada elemento tiene PESO y BENEFICIO por separado (mochila 0/1),
  - capacidad máxima fija,
  - greedy: ordena por razón beneficio/peso (mayor primero) y mete el elemento
    entero mientras quepa; si no cabe, se salta.

Interfaz que espera prueba.py:
  ProblemaMochila(peso, beneficio, capacidad, tamano)
      peso, beneficio: listas 0-indexadas de longitud 'tamano'.
  SolucionMochila: .mochila[i] (1-indexado, bool), .beneficio, .soluciones_factibles.

Las dos búsquedas exhaustivas solo evalúan soluciones FACTIBLES (nunca meten un
ítem que se pase de la capacidad) y reportan cuántas soluciones completas
evaluaron.
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

    def _razon(self, i: int) -> float:
        """Razón beneficio/peso del ítem i (índice 0-based). Peso 0 -> infinito."""
        if self.peso[i] > 0:
            return self.beneficio[i] / self.peso[i]
        return float("inf")

    # ------------------------------------------------------------------
    # 1. BÚSQUEDA GREEDY
    # ------------------------------------------------------------------
    def busqueda_greedy(self) -> SolucionMochila:
        """
        Greedy: ordena los ítems por razón beneficio/peso (mayor primero) y
        mete cada uno entero mientras quepa en la capacidad restante.

        Rápida, pero no siempre óptima.
        """
        orden = sorted(range(self.tamano), key=self._razon, reverse=True)

        mochila = [False] * (self.tamano + 1)
        beneficio_total = 0
        capacidad_restante = self.capacidad

        for i in orden:
            if self.peso[i] <= capacidad_restante:
                mochila[i + 1] = True
                beneficio_total += self.beneficio[i]
                capacidad_restante -= self.peso[i]

        return SolucionMochila(mochila=mochila, beneficio=beneficio_total)

    # ------------------------------------------------------------------
    # 2. BÚSQUEDA EXHAUSTIVA PURA
    # ------------------------------------------------------------------
    def busqueda_exhaustiva_pura(self) -> SolucionMochila:
        """
        Exhaustiva pura: para cada ítem decide meter / no meter, explorando solo
        las ramas factibles (no mete un ítem si se pasa de la capacidad).

        Devuelve la mejor solución y cuenta las soluciones completas evaluadas.
        """
        seleccion = [False] * (self.tamano + 1)
        peso_actual = [0]
        beneficio_actual = [0]

        solucion = SolucionMochila(
            mochila=[False] * (self.tamano + 1),
            beneficio=0,
            soluciones_factibles=0
        )

        def explorar(item: int):
            if item > self.tamano:
                solucion.soluciones_factibles += 1
                if beneficio_actual[0] > solucion.beneficio:
                    solucion.beneficio = beneficio_actual[0]
                    solucion.mochila = seleccion.copy()
                return

            # Opción A: NO incluir el ítem
            seleccion[item] = False
            explorar(item + 1)

            # Opción B: SÍ incluir el ítem (solo si cabe -> factible)
            if peso_actual[0] + self.peso[item - 1] <= self.capacidad:
                seleccion[item] = True
                peso_actual[0] += self.peso[item - 1]
                beneficio_actual[0] += self.beneficio[item - 1]
                explorar(item + 1)
                peso_actual[0] -= self.peso[item - 1]
                beneficio_actual[0] -= self.beneficio[item - 1]
                seleccion[item] = False

        explorar(1)
        return solucion

    # ------------------------------------------------------------------
    # 3. RAMIFICACIÓN Y ACOTAMIENTO
    # ------------------------------------------------------------------
    def busqueda_exhaustiva_ra(self) -> SolucionMochila:
        """
        Ramificación y Acotamiento.

        Igual que la exhaustiva pura, pero ordena los ítems por razón
        beneficio/peso y poda una rama cuando su COTA SUPERIOR optimista
        (relajación fraccional de la mochila) no supera la mejor solución
        encontrada.

        Devuelve la mejor solución (óptima) y cuenta las soluciones completas
        evaluadas.
        """
        n = self.tamano

        # Trabajamos sobre los índices ordenados por razón (mayor primero).
        orden = sorted(range(n), key=self._razon, reverse=True)
        pesos = [self.peso[i] for i in orden]
        benes = [self.beneficio[i] for i in orden]

        seleccion = [False] * n            # en el espacio 'orden'
        mejor_seleccion = [[False] * n]    # holder para la mejor selección
        peso_actual = [0]
        beneficio_actual = [0]

        solucion = SolucionMochila(
            mochila=[False] * (n + 1),
            beneficio=0,
            soluciones_factibles=0
        )

        def cota_superior(pos: int) -> float:
            """
            Cota optimista: al beneficio ya acumulado se le suma el llenado
            fraccional de la capacidad restante con los ítems pos..n-1 (que ya
            vienen ordenados por razón). Es un sobreestimado del mejor posible.
            """
            cap_restante = self.capacidad - peso_actual[0]
            cota = beneficio_actual[0]
            k = pos
            while k < n and pesos[k] <= cap_restante:
                cap_restante -= pesos[k]
                cota += benes[k]
                k += 1
            if k < n and cap_restante > 0:
                cota += benes[k] * (cap_restante / pesos[k])
            return cota

        def explorar(pos: int):
            if pos == n:
                solucion.soluciones_factibles += 1
                if beneficio_actual[0] > solucion.beneficio:
                    solucion.beneficio = beneficio_actual[0]
                    mejor_seleccion[0] = seleccion.copy()
                return

            # Poda: si ni la cota optimista supera lo mejor, abandonar la rama.
            if cota_superior(pos) <= solucion.beneficio:
                return

            # Incluir el ítem (solo si cabe -> factible)
            if peso_actual[0] + pesos[pos] <= self.capacidad:
                seleccion[pos] = True
                peso_actual[0] += pesos[pos]
                beneficio_actual[0] += benes[pos]
                explorar(pos + 1)
                peso_actual[0] -= pesos[pos]
                beneficio_actual[0] -= benes[pos]
                seleccion[pos] = False

            # Excluir el ítem
            explorar(pos + 1)

        explorar(0)

        # Reconstruir la mochila 1-indexada en el orden ORIGINAL de los ítems.
        for k in range(n):
            if mejor_seleccion[0][k]:
                solucion.mochila[orden[k] + 1] = True

        return solucion
