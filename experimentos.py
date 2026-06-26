"""
experimentos.py — Comparación empírica de las 3 técnicas de búsqueda.

Genera instancias aleatorias (con semilla fija, reproducibles) de tamaño
pequeño, mediano y grande para los 4 problemas, corre Greedy, Exhaustiva Pura y
Ramificación y Acotamiento, y arma tablas con la ganancia/costo obtenido, las
soluciones evaluadas y el tiempo.

La fuerza bruta se OMITE cuando la cantidad estimada de soluciones supera
LIMITE_SOLUCIONES (en los tamaños grandes es inviable: crece factorial o
exponencialmente). Eso es justamente parte del análisis del informe.

Correr desde la raíz del proyecto:   python experimentos.py
"""

import math
import random
import time

from rich.console import Console
from rich.table import Table
from rich import box

from asign1a1 import ProblemaAsigna1a1
from mochila import ProblemaMochila
from vendedor import ProblemaVendedor
from recursos import DistribucionRecursos

console = Console()

SEMILLA = 2026
LIMITE_SOLUCIONES = 2_000_000  # arriba de esto se omite la fuerza bruta


# ----------------------------------------------------------------------
# Utilidades
# ----------------------------------------------------------------------
def cronometrar(funcion):
    """Corre 'funcion' y devuelve (resultado, segundos)."""
    inicio = time.perf_counter()
    resultado = funcion()
    return resultado, time.perf_counter() - inicio


def fmt_tiempo(segundos: float) -> str:
    if segundos < 1e-3:
        return f"{segundos * 1e6:.0f} us"
    if segundos < 1:
        return f"{segundos * 1e3:.1f} ms"
    return f"{segundos:.2f} s"


def fmt_estimacion(n: float) -> str:
    return f"~{n:.1e}".replace("e+0", "e").replace("e+", "e")


# ----------------------------------------------------------------------
# Generadores de instancias aleatorias
# ----------------------------------------------------------------------
def generar_asignacion(n):
    m = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            m[i][j] = random.randint(1, 99)
    return ProblemaAsigna1a1(m, n)


def generar_mochila(n):
    pesos = [random.randint(1, 20) for _ in range(n)]
    benes = [random.randint(1, 99) for _ in range(n)]
    capacidad = sum(pesos) // 2
    return ProblemaMochila(pesos, benes, capacidad, n)


def generar_vendedor(n):
    m = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            d = random.randint(1, 99)
            m[i][j] = d
            m[j][i] = d
    return ProblemaVendedor(m, n)


def generar_recursos(params):
    r, m_items = params
    m = [[0] * (m_items + 1) for _ in range(r + 1)]
    for i in range(r + 1):
        for j in range(1, m_items + 1):
            m[i][j] = random.randint(0, 99)
    return DistribucionRecursos(m, r, m_items)


# ----------------------------------------------------------------------
# Configuración de los 4 problemas
# ----------------------------------------------------------------------
CONFIGS = [
    {
        "nombre": "Asignación 1 a 1",
        "valor": "ganancia", "sentido": "Ganancia",
        "construir": generar_asignacion,
        "estimar": lambda p: math.factorial(p),
        "describir": lambda p: f"N={p}",
        "tamanos": [("pequeño", 5), ("mediano", 9), ("grande", 12)],
    },
    {
        "nombre": "Distribución de un recurso",
        "valor": "ganancia", "sentido": "Ganancia",
        "construir": generar_recursos,
        "estimar": lambda p: math.comb(p[0] + p[1], p[1]),
        "describir": lambda p: f"R={p[0]}, M={p[1]}",
        "tamanos": [("pequeño", (5, 3)), ("mediano", (12, 5)), ("grande", (19, 8))],
    },
    {
        "nombre": "Mochila 0/1",
        "valor": "beneficio", "sentido": "Beneficio",
        "construir": generar_mochila,
        "estimar": lambda p: 2 ** p,
        "describir": lambda p: f"N={p}",
        "tamanos": [("pequeño", 12), ("mediano", 18), ("grande", 25)],
    },
    {
        "nombre": "Vendedor (TSP)",
        "valor": "costo", "sentido": "Costo",
        "construir": generar_vendedor,
        "estimar": lambda p: math.factorial(max(p - 1, 0)),
        "describir": lambda p: f"N={p}",
        "tamanos": [("pequeño", 5), ("mediano", 9), ("grande", 11)],
    },
]


# ----------------------------------------------------------------------
# Corrida
# ----------------------------------------------------------------------
def correr():
    random.seed(SEMILLA)

    for cfg in CONFIGS:
        tabla = Table(title=cfg["nombre"], box=box.SIMPLE_HEAVY,
                      header_style="bold", title_style="bold cyan")
        tabla.add_column("Tamaño")
        tabla.add_column("Instancia")
        tabla.add_column("Técnica")
        tabla.add_column(cfg["sentido"], justify="right")
        tabla.add_column("Sol. evaluadas", justify="right")
        tabla.add_column("Tiempo", justify="right")

        for etiqueta, params in cfg["tamanos"]:
            problema = cfg["construir"](params)
            estimacion = cfg["estimar"](params)
            descripcion = cfg["describir"](params)

            # Greedy
            sol, t = cronometrar(problema.busqueda_greedy)
            tabla.add_row(etiqueta, descripcion, "Greedy",
                          str(getattr(sol, cfg["valor"])), "—", fmt_tiempo(t))

            # Exhaustiva pura (solo si es viable)
            if estimacion <= LIMITE_SOLUCIONES:
                sol, t = cronometrar(problema.busqueda_exhaustiva_pura)
                tabla.add_row("", "", "Exhaustiva pura",
                              str(getattr(sol, cfg["valor"])),
                              str(sol.soluciones_factibles), fmt_tiempo(t))
            else:
                tabla.add_row("", "", "Exhaustiva pura", "omitida",
                              fmt_estimacion(estimacion), "no viable")

            # Ramificación y Acotamiento
            sol, t = cronometrar(problema.busqueda_exhaustiva_ra)
            tabla.add_row("", "", "R&A (B&B)",
                          str(getattr(sol, cfg["valor"])),
                          str(sol.soluciones_factibles), fmt_tiempo(t))

            tabla.add_section()

        console.print(tabla)
        console.print()


if __name__ == "__main__":
    correr()
