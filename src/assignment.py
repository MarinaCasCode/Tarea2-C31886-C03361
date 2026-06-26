"""
assignment.py

Implementación del problema de Asignación 1 a 1.
(Código base provisto por el profesor Braulio Solano.)
"""

from typing import List, Tuple, Optional
from dataclasses import dataclass, field


@dataclass
class NodoArbolAsigna:
    """Representa un nodo en el árbol de búsqueda de asignación."""
    id: str
    cota_superior: float
    asignaciones: List[Tuple[int, int]]  # Lista de (item, recurso)
    nivel: int
    solucion_completa: bool = False
    ganancia_final: Optional[int] = None
    podado: bool = False
    razon_poda: str = ""
    hijos: List['NodoArbolAsigna'] = field(default_factory=list)


@dataclass
class SolucionAsigna1a1:
    """Solución al problema de asignación 1 a 1."""
    asignado: List[int]
    ganancia: int
    soluciones_factibles: int = 0


class ProblemaAsigna1a1:
    """Problema de Asignación de 1 a 1."""

    def __init__(self, matriz: List[List[int]], tamano: int):
        """
        Inicializa el problema de asignación 1 a 1.

        Args:
            matriz: Matriz de ganancias
            tamano: Número de elementos a asignar
        """
        self.matriz = matriz
        self.tamano = tamano

    def busqueda_greedy(self) -> SolucionAsigna1a1:
        """
        Búsqueda Greedy: Selecciona la mejor opción local en cada paso.

        Returns:
            Solución factible (no necesariamente óptima)
        """
        asignado = [False] * (self.tamano + 1)
        solucion = SolucionAsigna1a1(
            asignado=[0] * (self.tamano + 1),
            ganancia=0
        )

        for i in range(1, self.tamano + 1):
            mejor = 1
            while asignado[mejor] and mejor < self.tamano:
                mejor += 1

            for j in range(1, self.tamano + 1):
                if (self.matriz[i][j] > self.matriz[i][mejor] and
                    not asignado[j]):
                    mejor = j

            solucion.asignado[i] = mejor
            solucion.ganancia += self.matriz[i][mejor]
            asignado[mejor] = True

        return solucion

    def busqueda_exhaustiva_pura(self) -> SolucionAsigna1a1:
        """
        Búsqueda Exhaustiva Pura: Explora todas las soluciones posibles.

        Returns:
            Solución óptima
        """
        asignado = [False] * (self.tamano + 1)
        asignacion = [0] * (self.tamano + 1)
        ganancia = [0]  # Usar lista para modificar en función anidada

        solucion = SolucionAsigna1a1(
            asignado=[0] * (self.tamano + 1),
            ganancia=0,
            soluciones_factibles=0
        )

        def asignacion_exhaustiva(item: int):
            """Función recursiva para explorar todas las asignaciones."""
            for i in range(1, self.tamano + 1):
                if not asignado[i]:
                    asignado[i] = True
                    asignacion[item] = i
                    ganancia[0] += self.matriz[item][i]

                    if item == self.tamano:
                        solucion.soluciones_factibles += 1
                        if ganancia[0] > solucion.ganancia:
                            solucion.ganancia = ganancia[0]
                            solucion.asignado = asignacion[:]
                    else:
                        asignacion_exhaustiva(item + 1)

                    asignado[i] = False
                    ganancia[0] -= self.matriz[item][i]

        asignacion_exhaustiva(1)
        return solucion

    def busqueda_exhaustiva_ra(self) -> SolucionAsigna1a1:
        """
        Búsqueda Exhaustiva con Ramificación y Acotamiento.

        Ordena las ramas por mejor cota.
        Explora primero las ramas más prometedoras.

        Returns:
            La mejor solución encontrada.
        """
        asignado = [False] * (self.tamano + 1)
        asignacion = [0] * (self.tamano + 1)
        ganancia_actual = [0]

        solucion = SolucionAsigna1a1(
            asignado=[0] * (self.tamano + 1),
            ganancia=0,
            soluciones_factibles=0
        )

        def calcular_cota_superior(nivel: int) -> int:
            """
            Calcula una cota superior optimista para la ganancia posible.
            """
            cota = ganancia_actual[0]

            for i in range(nivel, self.tamano + 1):
                mejor_disponible = 0
                for j in range(1, self.tamano + 1):
                    if not asignado[j]:
                        if self.matriz[i][j] > mejor_disponible:
                            mejor_disponible = self.matriz[i][j]
                cota += mejor_disponible

            return cota

        def asignacion_ra(item: int):
            """
            Función recursiva con ramificación y acotamiento.

            Ordena las ramas (opciones de asignación) por su cota superior
            de mayor a menor antes de explorarlas.
            """
            if item > self.tamano:
                # Solución completa encontrada
                solucion.soluciones_factibles += 1
                if ganancia_actual[0] > solucion.ganancia:
                    solucion.ganancia = ganancia_actual[0]
                    solucion.asignado = asignacion.copy()
                return

            # OPTIMIZACIÓN: Calcular cotas para todas las opciones disponibles
            opciones_con_cota = []

            for j in range(1, self.tamano + 1):
                if not asignado[j]:
                    # Hacer asignación tentativa para calcular cota
                    asignado[j] = True
                    asignacion[item] = j
                    ganancia_actual[0] += self.matriz[item][j]

                    # Calcular cota con esta asignación
                    cota = calcular_cota_superior(item + 1)

                    # Guardar opción con su cota
                    opciones_con_cota.append((j, cota))

                    # Deshacer asignación temporal
                    asignado[j] = False
                    ganancia_actual[0] -= self.matriz[item][j]

            # ORDENAR: Explorar primero las ramas con mejor cota (mayor a menor)
            opciones_con_cota.sort(key=lambda x: x[1], reverse=True)

            # Explorar opciones en orden de mejor a peor cota
            for j, cota in opciones_con_cota:
                # PODA TEMPRANA: Si esta cota no puede mejorar, las siguientes tampoco
                if cota <= solucion.ganancia:
                    break  # Las siguientes serán peores, no vale la pena explorarlas

                # Hacer asignación
                asignado[j] = True
                asignacion[item] = j
                ganancia_actual[0] += self.matriz[item][j]

                # Recursión
                asignacion_ra(item + 1)

                # Backtrack
                asignado[j] = False
                ganancia_actual[0] -= self.matriz[item][j]

        asignacion_ra(1)
        return solucion

    def busqueda_exhaustiva_ra_guarda(self, archivo_salida: str = "arbol_asignacion") -> SolucionAsigna1a1:
        """
        Búsqueda Exhaustiva con Ramificación y Acotamiento que guarda
        el árbol de búsqueda en un archivo DOT para visualización con Graphviz.

        Args:
            archivo_salida: Nombre base del archivo de salida (sin extensión)

        Returns:
            La mejor solución encontrada.
        """
        asignado = [False] * (self.tamano + 1)
        asignacion = [0] * (self.tamano + 1)
        ganancia_actual = [0]
        contador_nodos = [0]

        solucion = SolucionAsigna1a1(
            asignado=[0] * (self.tamano + 1),
            ganancia=0,
            soluciones_factibles=0
        )

        raiz = None

        def generar_id_nodo() -> str:
            """Genera un identificador de nodo único."""
            resultado = ""
            n = contador_nodos[0]
            while True:
                resultado = chr(65 + (n % 26)) + resultado
                n = n // 26
                if n == 0:
                    break
                n -= 1
            contador_nodos[0] += 1
            return resultado

        def calcular_cota_superior(nivel: int) -> int:
            """
            Calcula una cota superior optimista para la ganancia posible.
            """
            cota = ganancia_actual[0]

            for i in range(nivel, self.tamano + 1):
                mejor_disponible = 0
                for j in range(1, self.tamano + 1):
                    if not asignado[j]:
                        if self.matriz[i][j] > mejor_disponible:
                            mejor_disponible = self.matriz[i][j]
                cota += mejor_disponible

            return cota

        def asignacion_ra_guarda(item: int, asignaciones_previas: List[Tuple[int, int]]) -> NodoArbolAsigna:
            """
            Función recursiva con ramificación y acotamiento que construye el árbol.
            """
            nodo_id = generar_id_nodo()
            cota = calcular_cota_superior(item)

            nodo = NodoArbolAsigna(
                id=nodo_id,
                cota_superior=cota,
                asignaciones=asignaciones_previas.copy(),
                nivel=item - 1
            )

            if item > self.tamano:
                # Solución completa encontrada
                solucion.soluciones_factibles += 1
                nodo.solucion_completa = True
                nodo.ganancia_final = ganancia_actual[0]

                if ganancia_actual[0] > solucion.ganancia:
                    solucion.ganancia = ganancia_actual[0]
                    solucion.asignado = asignacion.copy()
                return nodo

            # Poda temprana
            if cota <= solucion.ganancia:
                nodo.podado = True
                nodo.razon_poda = f"CS ({cota}) <= mejor ({solucion.ganancia})"
                return nodo

            # Calcular cotas para todas las opciones disponibles
            opciones_con_cota = []

            for j in range(1, self.tamano + 1):
                if not asignado[j]:
                    asignado[j] = True
                    asignacion[item] = j
                    ganancia_actual[0] += self.matriz[item][j]

                    cota_opcion = calcular_cota_superior(item + 1)
                    opciones_con_cota.append((j, cota_opcion))

                    asignado[j] = False
                    ganancia_actual[0] -= self.matriz[item][j]

            # Ordenar por mejor cota (mayor a menor para maximización)
            opciones_con_cota.sort(key=lambda x: x[1], reverse=True)

            # Explorar opciones
            for j, cota_j in opciones_con_cota:
                if cota_j <= solucion.ganancia:
                    # Crear nodo podado
                    nodo_podado = NodoArbolAsigna(
                        id=generar_id_nodo(),
                        cota_superior=cota_j,
                        asignaciones=asignaciones_previas + [(item, j)],
                        nivel=item,
                        podado=True,
                        razon_poda=f"CS ({cota_j}) <= mejor ({solucion.ganancia})"
                    )
                    nodo.hijos.append(nodo_podado)
                    continue

                # Hacer asignación
                asignado[j] = True
                asignacion[item] = j
                ganancia_actual[0] += self.matriz[item][j]

                # Recursión
                hijo = asignacion_ra_guarda(item + 1, asignaciones_previas + [(item, j)])
                nodo.hijos.append(hijo)

                # Backtrack
                asignado[j] = False
                ganancia_actual[0] -= self.matriz[item][j]

            return nodo

        raiz = asignacion_ra_guarda(1, [])

        # Generar archivo DOT
        self._generar_dot(raiz, archivo_salida)

        return solucion

    def _generar_dot(self, raiz: NodoArbolAsigna, archivo_salida: str):
        """Genera archivo DOT para visualizar con Graphviz."""

        def formato_asignaciones(asignaciones: List[Tuple[int, int]]) -> str:
            """Formatea las asignaciones para mostrar."""
            if not asignaciones:
                return "sin asignaciones"
            return ", ".join([f"{i}→{j}" for i, j in asignaciones])

        def nodo_a_dot(nodo: NodoArbolAsigna, lineas: List[str]):
            """Convierte un nodo y sus hijos a formato DOT."""

            # Construir etiqueta del nodo
            if nodo.solucion_completa:
                label = f"<B>{nodo.id}</B><BR/>"
                label += f"CS = {nodo.cota_superior}<BR/>"
                label += f"{formato_asignaciones(nodo.asignaciones)}<BR/>"
                label += f"<B>Ganancia = {nodo.ganancia_final}</B>"
                color = "lightgreen"
            elif nodo.podado:
                label = f"<B>{nodo.id}</B><BR/>"
                label += f"CS = {nodo.cota_superior}<BR/>"
                label += f"{formato_asignaciones(nodo.asignaciones)}<BR/>"
                label += f"<I>podado</I>"
                color = "lightgray"
            else:
                label = f"<B>{nodo.id}</B><BR/>"
                label += f"CS = {nodo.cota_superior}<BR/>"
                label += f"{formato_asignaciones(nodo.asignaciones)}"
                color = "lightyellow"

            lineas.append(f'    {nodo.id} [label=<{label}>, fillcolor="{color}"];')

            # Procesar hijos
            for hijo in nodo.hijos:
                nodo_a_dot(hijo, lineas)
                # Etiqueta de la arista mostrando la asignación nueva
                if hijo.asignaciones and len(hijo.asignaciones) > len(nodo.asignaciones):
                    ultima = hijo.asignaciones[-1]
                    edge_label = f"{ultima[0]}→{ultima[1]}"
                    lineas.append(f'    {nodo.id} -> {hijo.id} [label="{edge_label}"];')
                else:
                    lineas.append(f'    {nodo.id} -> {hijo.id};')

        lineas = [
            'digraph ArbolBusqueda {',
            '    node [shape=box, style="filled,rounded", fontname="Arial"];',
            '    edge [fontname="Arial"];',
            '    rankdir=TB;',
            ''
        ]

        if raiz:
            nodo_a_dot(raiz, lineas)

        lineas.append('}')

        # Guardar archivo
        with open(f"{archivo_salida}.dot", 'w', encoding='utf-8') as f:
            f.write('\n'.join(lineas))
