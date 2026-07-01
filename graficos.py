"""
graficos.py — Gráficos comparativos de las 3 técnicas para el informe.

Barre un rango de tamaños por problema, mide el tiempo y las soluciones
evaluadas de Greedy, Exhaustiva Pura y Ramificación y Acotamiento, y guarda dos
figuras PNG en la carpeta graficos/:

  - tiempos.png      : tiempo vs. tamaño (escala log) para los 4 problemas.
  - soluciones.png   : soluciones evaluadas vs. tamaño (escala log).

La exhaustiva pura se detiene en un tamaño tope (crece factorial/exponencial y
dejaría de ser viable). Reutiliza los generadores de instancias de experimentos.py.

Correr desde la raíz del proyecto:   python graficos.py
"""

import os
import time
import random

import matplotlib
matplotlib.use("Agg")  # sin ventana, solo guarda PNG
import matplotlib.pyplot as plt

from experimentos import (generar_asignacion, generar_mochila,
                          generar_vendedor, generar_recursos)

SEMILLA = 2026
CARPETA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "graficos")
os.makedirs(CARPETA, exist_ok=True)

VERDE, ROJO, AZUL = "#2ca02c", "#d62728", "#1f77b4"


def cronometrar(funcion):
    inicio = time.perf_counter()
    solucion = funcion()
    return solucion, time.perf_counter() - inicio


# Para cada problema: generador, tamaños a barrer, tamaños donde SÍ corre la
# exhaustiva (tope), cómo obtener el valor del eje x y su etiqueta.
PROBLEMAS = [
    dict(nombre="Asignación 1 a 1", generar=generar_asignacion,
         tamanos=list(range(2, 12)), tamanos_exh=list(range(2, 10)),
         eje=lambda p: p, xlabel="N (elementos)"),
    dict(nombre="Distribución de un recurso", generar=generar_recursos,
         tamanos=[(10, m) for m in range(2, 10)],
         tamanos_exh=[(10, m) for m in range(2, 8)],
         eje=lambda p: p[1], xlabel="M (ítems), R = 10"),
    dict(nombre="Mochila 0/1", generar=generar_mochila,
         tamanos=list(range(4, 25)), tamanos_exh=list(range(4, 21)),
         eje=lambda p: p, xlabel="N (objetos)"),
    dict(nombre="Vendedor (TSP)", generar=generar_vendedor,
         tamanos=list(range(3, 12)), tamanos_exh=list(range(3, 11)),
         eje=lambda p: p, xlabel="N (ciudades)"),
]


def barrer(pr):
    """Corre las 3 técnicas sobre cada tamaño y junta los datos."""
    d = dict(n=[], tg=[], tb=[], evb=[], ne=[], te=[], eve=[])
    for p in pr["tamanos"]:
        random.seed(SEMILLA)
        problema = pr["generar"](p)
        x = pr["eje"](p)
        d["n"].append(x)

        _, t = cronometrar(problema.busqueda_greedy)
        d["tg"].append(t)

        sol, t = cronometrar(problema.busqueda_exhaustiva_ra)
        d["tb"].append(t)
        d["evb"].append(sol.soluciones_factibles)

        if p in pr["tamanos_exh"]:
            sol, t = cronometrar(problema.busqueda_exhaustiva_pura)
            d["ne"].append(x)
            d["te"].append(t)
            d["eve"].append(sol.soluciones_factibles)
    return d


def eps(valores):
    """Evita ceros para la escala logarítmica."""
    return [max(v, 1e-7) for v in valores]


def main():
    print("Corriendo experimentos para los gráficos (puede tardar ~1 min)...")
    resultados = [(pr, barrer(pr)) for pr in PROBLEMAS]

    # --- Figura 1: tiempos ---
    fig, axs = plt.subplots(2, 2, figsize=(11, 8))
    for ax, (pr, d) in zip(axs.flat, resultados):
        ax.plot(d["n"], eps(d["tg"]), "o-", color=VERDE, label="Greedy")
        if d["ne"]:
            ax.plot(d["ne"], eps(d["te"]), "s-", color=ROJO, label="Exhaustiva pura")
        ax.plot(d["n"], eps(d["tb"]), "^-", color=AZUL, label="Ramif. y Acot.")
        ax.set_yscale("log")
        ax.set_title(pr["nombre"])
        ax.set_xlabel(pr["xlabel"])
        ax.set_ylabel("tiempo (s) — escala log")
        ax.grid(True, which="both", ls=":", alpha=0.5)
        ax.legend(fontsize=8)
    fig.suptitle("Tiempo de ejecución vs. tamaño del problema",
                 fontsize=14, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    ruta1 = os.path.join(CARPETA, "tiempos.png")
    fig.savefig(ruta1, dpi=130)
    plt.close(fig)

    # --- Figura 2: soluciones evaluadas ---
    fig, axs = plt.subplots(2, 2, figsize=(11, 8))
    for ax, (pr, d) in zip(axs.flat, resultados):
        if d["ne"]:
            ax.plot(d["ne"], eps(d["eve"]), "s-", color=ROJO, label="Exhaustiva pura")
        ax.plot(d["n"], eps(d["evb"]), "^-", color=AZUL, label="Ramif. y Acot.")
        ax.set_yscale("log")
        ax.set_title(pr["nombre"])
        ax.set_xlabel(pr["xlabel"])
        ax.set_ylabel("soluciones evaluadas — escala log")
        ax.grid(True, which="both", ls=":", alpha=0.5)
        ax.legend(fontsize=8)
    fig.suptitle("Soluciones evaluadas vs. tamaño del problema",
                 fontsize=14, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    ruta2 = os.path.join(CARPETA, "soluciones.png")
    fig.savefig(ruta2, dpi=130)
    plt.close(fig)

    print("Listo. Figuras guardadas:")
    print("  -", ruta1)
    print("  -", ruta2)


if __name__ == "__main__":
    main()
