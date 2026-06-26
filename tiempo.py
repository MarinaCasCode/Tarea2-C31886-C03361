"""
tiempo.py — Medición del tiempo de ejecución de cada búsqueda.

Uso (igual que en prueba.py):
    timer = MedidorTiempo()
    timer.cargar_tiempo()          # marca el inicio
    ... (correr la búsqueda) ...
    t = timer.intervalo_tiempo()   # dict {horas, minutos, segundos, centesimas}
"""

import time


class MedidorTiempo:
    """Cronómetro simple para medir cuánto tarda una búsqueda."""

    def __init__(self):
        self._inicio = 0.0

    def cargar_tiempo(self):
        """Marca el instante de inicio."""
        self._inicio = time.perf_counter()

    def intervalo_tiempo(self) -> dict:
        """Tiempo transcurrido desde cargar_tiempo(), desglosado."""
        transcurrido = time.perf_counter() - self._inicio
        centesimas_totales = int(transcurrido * 100)
        return {
            "horas": centesimas_totales // 360000,
            "minutos": (centesimas_totales // 6000) % 60,
            "segundos": (centesimas_totales // 100) % 60,
            "centesimas": centesimas_totales % 100,
        }
