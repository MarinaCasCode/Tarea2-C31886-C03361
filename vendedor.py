"""
vendedor.py — Problema d) del vendedor (TSP).

Confirmado por el código prueba.py del profe:
  - el recorrido es un CICLO: empieza en la ciudad 1 ('a'), visita todas las
    ciudades una vez y regresa a la ciudad 1,
  - la matriz de distancias es SIMÉTRICA, con la diagonal en 0,
  - un -1 representa "no hay camino" entre dos ciudades.

Interfaz que espera prueba.py:
  ProblemaVendedor(matriz, tamano)        matriz 1-indexada NxN.
  SolucionVendedor: .camino[i] (1-indexado, letra de la ciudad i-ésima del
                    recorrido), .costo, .soluciones_factibles.

Las dos búsquedas exhaustivas solo evalúan recorridos FACTIBLES (que usan
caminos existentes y cierran el ciclo) y reportan cuántos recorridos completos
evaluaron.
"""

import math
from dataclasses import dataclass
from typing import List

# Valor en la matriz que significa "no existe camino" entre dos ciudades.
NO_CAMINO = -1


@dataclass
class SolucionVendedor:
    """Solución del vendedor. camino[i] (1-indexado) = letra de la ciudad i-ésima."""
    camino: List[str]
    costo: int
    soluciones_factibles: int = 0


class ProblemaVendedor:
    """Problema del vendedor viajero (TSP), recorrido cíclico desde la ciudad 1."""

    def __init__(self, matriz: List[List[int]], tamano: int):
        self.matriz = matriz
        self.tamano = tamano

    def _hay_camino(self, i: int, j: int) -> bool:
        """True si existe camino entre las ciudades i y j."""
        d = self.matriz[i][j]
        return d != NO_CAMINO and d != math.inf

    def _letras(self, ruta: List[int]) -> List[str]:
        """Convierte ruta[1..n] (números de ciudad) a un camino de letras (a,b,c...)."""
        camino = [""] * (self.tamano + 1)
        for k in range(1, self.tamano + 1):
            if ruta[k] > 0:
                camino[k] = chr(ruta[k] + 96)
        return camino

    def _min_salida(self) -> List[float]:
        """Para cada ciudad, la distancia mínima a otra ciudad alcanzable."""
        n = self.tamano
        ms = [math.inf] * (n + 1)
        for i in range(1, n + 1):
            menor = math.inf
            for j in range(1, n + 1):
                if i != j and self._hay_camino(i, j) and self.matriz[i][j] < menor:
                    menor = self.matriz[i][j]
            ms[i] = menor
        return ms

    # ------------------------------------------------------------------
    # 1. BÚSQUEDA GREEDY (vecino más cercano)
    # ------------------------------------------------------------------
    def busqueda_greedy(self) -> SolucionVendedor:
        """
        Greedy del vecino más cercano: desde la ciudad actual, ir siempre a la
        ciudad no visitada más cercana. Al final regresa a la ciudad de origen.

        Rápida, pero no siempre óptima.
        """
        n = self.tamano
        visitado = [False] * (n + 1)
        ruta = [0] * (n + 1)
        ruta[1] = 1
        visitado[1] = True
        costo = 0
        actual = 1

        for paso in range(2, n + 1):
            mejor = -1
            mejor_dist = math.inf
            for c in range(1, n + 1):
                if (not visitado[c] and self._hay_camino(actual, c)
                        and self.matriz[actual][c] < mejor_dist):
                    mejor_dist = self.matriz[actual][c]
                    mejor = c
            if mejor == -1:
                break  # ninguna ciudad alcanzable (grafo incompleto)
            visitado[mejor] = True
            ruta[paso] = mejor
            costo += mejor_dist
            actual = mejor

        # Cerrar el ciclo: regresar a la ciudad de origen.
        if self._hay_camino(actual, 1):
            costo += self.matriz[actual][1]

        return SolucionVendedor(camino=self._letras(ruta), costo=costo)

    # ------------------------------------------------------------------
    # 2. BÚSQUEDA EXHAUSTIVA PURA
    # ------------------------------------------------------------------
    def busqueda_exhaustiva_pura(self) -> SolucionVendedor:
        """
        Exhaustiva pura: prueba todas las permutaciones de ciudades (fijando el
        origen en la ciudad 1), siguiendo solo caminos que existen, y se queda
        con el recorrido de menor costo que cierra el ciclo.

        Devuelve la mejor solución y cuenta los recorridos completos evaluados.
        """
        n = self.tamano
        visitado = [False] * (n + 1)
        ruta = [0] * (n + 1)
        ruta[1] = 1
        visitado[1] = True

        mejor = {"costo": math.inf, "ruta": None}
        contador = [0]

        def explorar(pos: int, costo_actual: int):
            if pos > n:
                # Cerrar el ciclo regresando a la ciudad 1.
                if self._hay_camino(ruta[n], 1):
                    total = costo_actual + self.matriz[ruta[n]][1]
                    contador[0] += 1
                    if total < mejor["costo"]:
                        mejor["costo"] = total
                        mejor["ruta"] = ruta.copy()
                return

            for c in range(2, n + 1):
                if not visitado[c] and self._hay_camino(ruta[pos - 1], c):
                    visitado[c] = True
                    ruta[pos] = c
                    explorar(pos + 1, costo_actual + self.matriz[ruta[pos - 1]][c])
                    visitado[c] = False

        explorar(2, 0)

        if mejor["ruta"] is None:
            return SolucionVendedor(camino=self._letras(ruta), costo=0,
                                    soluciones_factibles=contador[0])
        return SolucionVendedor(camino=self._letras(mejor["ruta"]),
                                costo=mejor["costo"],
                                soluciones_factibles=contador[0])

    # ------------------------------------------------------------------
    # 3. RAMIFICACIÓN Y ACOTAMIENTO
    # ------------------------------------------------------------------
    def busqueda_exhaustiva_ra(self) -> SolucionVendedor:
        """
        Ramificación y Acotamiento.

        Igual que la exhaustiva pura, pero poda una rama cuando su COTA INFERIOR
        optimista ya iguala o supera el mejor costo encontrado. La cota suma, al
        costo recorrido, la "salida más barata" de cada ciudad que todavía debe
        salir (la actual y las no visitadas): nunca sobreestima el costo real.

        Devuelve la mejor solución (óptima) y cuenta los recorridos completos
        evaluados.
        """
        n = self.tamano
        min_salida = self._min_salida()
        visitado = [False] * (n + 1)
        ruta = [0] * (n + 1)
        ruta[1] = 1
        visitado[1] = True

        mejor = {"costo": math.inf, "ruta": None}
        contador = [0]

        def cota_inferior(pos: int, costo_actual: int) -> float:
            cota = costo_actual + min_salida[ruta[pos - 1]]
            for c in range(2, n + 1):
                if not visitado[c]:
                    cota += min_salida[c]
            return cota

        def explorar(pos: int, costo_actual: int):
            if pos > n:
                if self._hay_camino(ruta[n], 1):
                    total = costo_actual + self.matriz[ruta[n]][1]
                    contador[0] += 1
                    if total < mejor["costo"]:
                        mejor["costo"] = total
                        mejor["ruta"] = ruta.copy()
                return

            # Poda: si ni la cota optimista mejora lo mejor, abandonar la rama.
            if cota_inferior(pos, costo_actual) >= mejor["costo"]:
                return

            for c in range(2, n + 1):
                if not visitado[c] and self._hay_camino(ruta[pos - 1], c):
                    visitado[c] = True
                    ruta[pos] = c
                    explorar(pos + 1, costo_actual + self.matriz[ruta[pos - 1]][c])
                    visitado[c] = False

        explorar(2, 0)

        if mejor["ruta"] is None:
            return SolucionVendedor(camino=self._letras(ruta), costo=0,
                                    soluciones_factibles=contador[0])
        return SolucionVendedor(camino=self._letras(mejor["ruta"]),
                                costo=mejor["costo"],
                                soluciones_factibles=contador[0])
