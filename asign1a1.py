"""
assignment.py

Implementación del problema de Asignación 1 a 1.
(Código base provisto por el profesor Braulio Solano.)

Métodos de búsqueda disponibles:
  - busqueda_greedy               : heurística voraz (rápida, no óptima)
  - busqueda_exhaustiva_pura      : explora todas las permutaciones (óptima)
  - busqueda_exhaustiva_ra_naria  : ramificación y acotamiento, árbol n-ario
  - busqueda_exhaustiva_ra_binaria: ramificación y acotamiento, árbol binario
                                    (estilo Aho, Hopcroft y Ullman: incluir/excluir)
  - busqueda_exhaustiva_ra_guarda : igual que la n-aria, pero guarda el árbol
                                    de búsqueda en un archivo .dot (Graphviz)

Nota didáctica sobre las dos variantes de Ramificación y Acotamiento:

  * La variante N-ARIA usa un nivel del árbol por cada fila (ítem del dominio).
    En cada nivel ramifica probando todas las columnas (ítems del codominio)
    todavía libres, ordena esas ramas por su cota superior y poda en cuanto
    una cota no supera la mejor ganancia encontrada.

  * La variante BINARIA decide de a una pareja (fila, columna) a la vez:
    en cada nodo se toma una columna candidata para la fila actual y se abren
    dos ramas, INCLUIR (asignar fila -> columna) y EXCLUIR (prohibir esa
    columna para esa fila). Es la forma clásica de Aho, Hopcroft y Ullman de
    representar el árbol de soluciones con restricciones de inclusión/exclusión.

  Ambas son correctas y devuelven el óptimo; difieren en la forma del árbol.
"""

from typing import List, Tuple, Optional
from dataclasses import dataclass, field


@dataclass
class NodoArbolAsigna:
    """Representa un nodo en el árbol de búsqueda de asignación (n-ario)."""
    id: str
    cota_superior: float
    asignaciones: List[Tuple[int, int]]  # Lista de (fila, columna)
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
            matriz: Matriz de ganancias (índices 1..tamano; fila/columna 0 sin usar)
            tamano: Número de elementos a asignar
        """
        self.matriz = matriz
        self.tamano = tamano

    # ------------------------------------------------------------------
    # 1. BÚSQUEDA GREEDY
    # ------------------------------------------------------------------
    def busqueda_greedy(self) -> SolucionAsigna1a1:
        """
        Búsqueda Greedy: para cada fila, escoge la mejor columna disponible.

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

    # ------------------------------------------------------------------
    # 2. BÚSQUEDA EXHAUSTIVA PURA
    # ------------------------------------------------------------------
    def busqueda_exhaustiva_pura(self) -> SolucionAsigna1a1:
        """
        Búsqueda Exhaustiva Pura: explora todas las asignaciones posibles.

        Returns:
            Solución óptima
        """
        asignado = [False] * (self.tamano + 1)
        asignacion = [0] * (self.tamano + 1)
        ganancia = [0]

        solucion = SolucionAsigna1a1(
            asignado=[0] * (self.tamano + 1),
            ganancia=0,
            soluciones_factibles=0
        )

        def asignacion_exhaustiva(item: int):
            """Función recursiva que explora todas las asignaciones."""
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

    # ------------------------------------------------------------------
    # 3. RAMIFICACIÓN Y ACOTAMIENTO — VARIANTE N-ARIA
    # ------------------------------------------------------------------
    def busqueda_exhaustiva_ra_naria(self) -> SolucionAsigna1a1:
        """
        Ramificación y Acotamiento (árbol n-ario).

        Un nivel del árbol por cada fila. En cada nivel se prueban todas las
        columnas libres, se ordenan por cota superior (mayor primero) y se
        podan las ramas cuya cota no supera la mejor ganancia encontrada.

        Returns:
            La mejor solución encontrada (óptima).
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
            """Cota superior optimista para las filas 'nivel'..tamano."""
            cota = ganancia_actual[0]
            for i in range(nivel, self.tamano + 1):
                mejor_disponible = 0
                for j in range(1, self.tamano + 1):
                    if not asignado[j] and self.matriz[i][j] > mejor_disponible:
                        mejor_disponible = self.matriz[i][j]
                cota += mejor_disponible
            return cota

        def asignacion_ra(item: int):
            if item > self.tamano:
                solucion.soluciones_factibles += 1
                if ganancia_actual[0] > solucion.ganancia:
                    solucion.ganancia = ganancia_actual[0]
                    solucion.asignado = asignacion.copy()
                return

            # Calcular cota de cada columna disponible para esta fila
            opciones_con_cota = []
            for j in range(1, self.tamano + 1):
                if not asignado[j]:
                    asignado[j] = True
                    asignacion[item] = j
                    ganancia_actual[0] += self.matriz[item][j]

                    cota = calcular_cota_superior(item + 1)
                    opciones_con_cota.append((j, cota))

                    asignado[j] = False
                    ganancia_actual[0] -= self.matriz[item][j]

            # Explorar primero las ramas con mejor cota
            opciones_con_cota.sort(key=lambda x: x[1], reverse=True)

            for j, cota in opciones_con_cota:
                # Poda: si esta cota no mejora, las siguientes tampoco (van ordenadas)
                if cota <= solucion.ganancia:
                    break

                asignado[j] = True
                asignacion[item] = j
                ganancia_actual[0] += self.matriz[item][j]

                asignacion_ra(item + 1)

                asignado[j] = False
                ganancia_actual[0] -= self.matriz[item][j]

        asignacion_ra(1)
        return solucion

    # Alias para compatibilidad con código existente.
    def busqueda_exhaustiva_ra(self) -> SolucionAsigna1a1:
        """Alias de busqueda_exhaustiva_ra_naria (compatibilidad)."""
        return self.busqueda_exhaustiva_ra_naria()

    # ------------------------------------------------------------------
    # 4. RAMIFICACIÓN Y ACOTAMIENTO — VARIANTE BINARIA (estilo Aho)
    # ------------------------------------------------------------------
    def busqueda_exhaustiva_ra_binaria(self) -> SolucionAsigna1a1:
        """
        Ramificación y Acotamiento (árbol binario), traducción corregida del
        Pascal original ASIGN1A1.PAS.

        Estructura conceptual (igual que el Pascal):
          - dominio[i]   : la fila i ya tiene columna asignada.
          - codominio[j] : la columna j ya está usada.
          - descartar[i] : para la fila i se excluyen las columnas <= descartar[i].
          - En cada nodo se toma la primera columna candidata para la fila
            actual y se abren dos ramas:
              * INCLUIR : asignar fila -> columna.
              * EXCLUIR : prohibir esa columna para la fila (descartar) y
                          reintentar la misma fila con la siguiente columna.
          - Se explora primero la rama de mayor cota superior.
          - Poda: una rama se explora solo si su cota supera la mejor ganancia.

        Correcciones respecto al Pascal original:
          - Los bucles que buscan columna libre ahora tienen tope (no se
            desbordan más allá de 'tamano').
          - El marcado/desmarcado de columnas usa siempre el índice correcto.
          - Las hojas evalúan la GANANCIA REAL, no la cota optimista.
          - La poda usa el criterio limpio "cota <= mejor".

        Returns:
            La mejor solución encontrada (óptima).
        """
        dominio = [False] * (self.tamano + 2)
        codominio = [False] * (self.tamano + 2)
        descartar = [0] * (self.tamano + 2)
        asignacion = [0] * (self.tamano + 2)

        solucion = SolucionAsigna1a1(
            asignado=[0] * (self.tamano + 1),
            ganancia=0,
            soluciones_factibles=0
        )

        def cota_superior() -> int:
            """Cota optimista respetando dominio/codominio/descartar."""
            cota = 0
            for i in range(1, self.tamano + 1):
                if dominio[i]:
                    cota += self.matriz[i][asignacion[i]]
                else:
                    mejor = 0
                    for j in range(1, self.tamano + 1):
                        if (not codominio[j] and j > descartar[i]
                                and self.matriz[i][j] > mejor):
                            mejor = self.matriz[i][j]
                    cota += mejor
            return cota

        def primera_fila_libre() -> int:
            i = 1
            while i <= self.tamano and dominio[i]:
                i += 1
            return i

        def primera_columna_libre(desde: int) -> int:
            j = desde
            while j <= self.tamano and codominio[j]:
                j += 1
            return j

        def registrar_si_mejora():
            ganancia_real = sum(self.matriz[f][asignacion[f]]
                                for f in range(1, self.tamano + 1))
            solucion.soluciones_factibles += 1
            if ganancia_real > solucion.ganancia:
                solucion.ganancia = ganancia_real
                solucion.asignado = [0] + [asignacion[f]
                                           for f in range(1, self.tamano + 1)]

        def explorar():
            item = primera_fila_libre()

            # Caso base: todas las filas asignadas
            if item > self.tamano:
                registrar_si_mejora()
                return

            # Optimización: si solo queda una fila libre, su columna está forzada
            filas_libres = sum(1 for i in range(1, self.tamano + 1) if not dominio[i])
            if filas_libres == 1:
                col = primera_columna_libre(1)
                dominio[item] = True
                codominio[col] = True
                asignacion[item] = col
                registrar_si_mejora()
                dominio[item] = False
                codominio[col] = False
                asignacion[item] = 0
                return

            # Primera columna candidata (libre y no descartada) para esta fila
            col = primera_columna_libre(descartar[item] + 1)
            if col > self.tamano:
                return  # sin columna válida en esta rama

            # Cota de la rama INCLUIR (fila item -> columna col)
            dominio[item] = True
            codominio[col] = True
            asignacion[item] = col
            cota_incluir = cota_superior()
            dominio[item] = False
            codominio[col] = False
            asignacion[item] = 0

            # Cota de la rama EXCLUIR (prohibir col para item)
            descarto_previo = descartar[item]
            descartar[item] = col
            cota_excluir = cota_superior()
            descartar[item] = descarto_previo

            def rama_incluir():
                if cota_incluir > solucion.ganancia:
                    dominio[item] = True
                    codominio[col] = True
                    asignacion[item] = col
                    explorar()
                    dominio[item] = False
                    codominio[col] = False
                    asignacion[item] = 0

            def rama_excluir():
                if cota_excluir > solucion.ganancia:
                    descartar[item] = col
                    explorar()
                    descartar[item] = descarto_previo

            # Explorar primero la rama de mayor cota
            if cota_incluir >= cota_excluir:
                rama_incluir()
                rama_excluir()
            else:
                rama_excluir()
                rama_incluir()

        explorar()
        return solucion

    # ------------------------------------------------------------------
    # 5. RAMIFICACIÓN Y ACOTAMIENTO N-ARIA QUE GUARDA EL ÁRBOL
    # ------------------------------------------------------------------
    def busqueda_exhaustiva_ra_guarda(self,
                                      archivo_salida: str = "arbol_asignacion"
                                      ) -> SolucionAsigna1a1:
        """
        Igual que busqueda_exhaustiva_ra_naria, pero construye y guarda el
        árbol de búsqueda en un archivo .dot para visualizar con Graphviz.

        La cota mostrada en cada nodo es la cota calculada justo después de
        fijar la asignación que conduce a ese nodo, de modo que nodos internos,
        nodos podados y hojas usan todos el mismo criterio (consistencia).

        Args:
            archivo_salida: Nombre base del archivo de salida (sin extensión)

        Returns:
            La mejor solución encontrada (óptima).
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

        def generar_id_nodo() -> str:
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
            """Cota superior optimista para las filas 'nivel'..tamano."""
            cota = ganancia_actual[0]
            for i in range(nivel, self.tamano + 1):
                mejor_disponible = 0
                for j in range(1, self.tamano + 1):
                    if not asignado[j] and self.matriz[i][j] > mejor_disponible:
                        mejor_disponible = self.matriz[i][j]
                cota += mejor_disponible
            return cota

        def asignacion_ra_guarda(item: int,
                                 asignaciones_previas: List[Tuple[int, int]],
                                 cota_entrada: int) -> NodoArbolAsigna:
            """
            Construye el árbol. 'cota_entrada' es la cota calculada por el padre
            justo tras fijar la asignación que lleva a este nodo, de modo que
            todos los nodos reportan la misma medida de cota.
            """
            nodo_id = generar_id_nodo()

            nodo = NodoArbolAsigna(
                id=nodo_id,
                cota_superior=cota_entrada,
                asignaciones=asignaciones_previas.copy(),
                nivel=item - 1
            )

            # Solución completa (hoja)
            if item > self.tamano:
                solucion.soluciones_factibles += 1
                nodo.solucion_completa = True
                nodo.ganancia_final = ganancia_actual[0]
                if ganancia_actual[0] > solucion.ganancia:
                    solucion.ganancia = ganancia_actual[0]
                    solucion.asignado = asignacion.copy()
                return nodo

            # Poda del nodo completo: su cota de entrada no supera la mejor
            if cota_entrada <= solucion.ganancia:
                nodo.podado = True
                nodo.razon_poda = f"CS ({cota_entrada}) <= mejor ({solucion.ganancia})"
                return nodo

            # Calcular la cota de cada columna disponible para esta fila
            opciones_con_cota = []
            for j in range(1, self.tamano + 1):
                if not asignado[j]:
                    asignado[j] = True
                    asignacion[item] = j
                    ganancia_actual[0] += self.matriz[item][j]

                    cota_j = calcular_cota_superior(item + 1)
                    opciones_con_cota.append((j, cota_j))

                    asignado[j] = False
                    ganancia_actual[0] -= self.matriz[item][j]

            # Explorar primero las ramas con mejor cota
            opciones_con_cota.sort(key=lambda x: x[1], reverse=True)

            for j, cota_j in opciones_con_cota:
                if cota_j <= solucion.ganancia:
                    # Nodo podado: se muestra con su misma cota de entrada (cota_j)
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

                asignado[j] = True
                asignacion[item] = j
                ganancia_actual[0] += self.matriz[item][j]

                hijo = asignacion_ra_guarda(item + 1,
                                            asignaciones_previas + [(item, j)],
                                            cota_j)
                nodo.hijos.append(hijo)

                asignado[j] = False
                ganancia_actual[0] -= self.matriz[item][j]

            return nodo

        # La cota de entrada de la raíz es la cota global inicial
        cota_raiz = calcular_cota_superior(1)
        raiz = asignacion_ra_guarda(1, [], cota_raiz)

        self._generar_dot(raiz, archivo_salida)
        return solucion

    # ------------------------------------------------------------------
    # Generación del archivo .dot (Graphviz)
    # ------------------------------------------------------------------
    def _generar_dot(self, raiz: NodoArbolAsigna, archivo_salida: str):
        """Genera archivo DOT para visualizar el árbol n-ario con Graphviz."""

        def formato_asignaciones(asignaciones: List[Tuple[int, int]]) -> str:
            if not asignaciones:
                return "sin asignaciones"
            return ", ".join([f"{i}→{j}" for i, j in asignaciones])

        def nodo_a_dot(nodo: NodoArbolAsigna, lineas: List[str]):
            if nodo.solucion_completa:
                label = f"<B>{nodo.id}</B><BR/>"
                label += f"CS = {int(nodo.cota_superior)}<BR/>"
                label += f"{formato_asignaciones(nodo.asignaciones)}<BR/>"
                label += f"<B>Ganancia = {nodo.ganancia_final}</B>"
                color = "lightgreen"
            elif nodo.podado:
                label = f"<B>{nodo.id}</B><BR/>"
                label += f"CS = {int(nodo.cota_superior)}<BR/>"
                label += f"{formato_asignaciones(nodo.asignaciones)}<BR/>"
                label += f"<I>podado</I>"
                color = "lightgray"
            else:
                label = f"<B>{nodo.id}</B><BR/>"
                label += f"CS = {int(nodo.cota_superior)}<BR/>"
                label += f"{formato_asignaciones(nodo.asignaciones)}"
                color = "lightyellow"

            lineas.append(f'    {nodo.id} [label=<{label}>, fillcolor="{color}"];')

            for hijo in nodo.hijos:
                nodo_a_dot(hijo, lineas)
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

        with open(f"{archivo_salida}.dot", 'w', encoding='utf-8') as f:
            f.write('\n'.join(lineas))
