# Tarea Programada 2: Técnicas de búsqueda para problemas de optimización

**Curso:** CI-0116 Análisis de Algoritmos y Estructuras de Datos  
**Universidad de Costa Rica**  
**Autores:** Marina Castro Peralta (C31886), Emanuel González Chaves (C03361)

## Descripción

Este proyecto implementa y compara tres técnicas de búsqueda para encontrar la
solución óptima de cuatro problemas clásicos de optimización: búsqueda Greedy,
búsqueda Exhaustiva Pura y búsqueda Exhaustiva con Ramificación y Acotamiento.

Desde un menú interactivo el usuario elige el problema, la técnica de búsqueda y
los datos de entrada (digitados a mano o generados aleatoriamente). El programa
despliega la solución encontrada, el tiempo que tardó en encontrarla y, en el
caso de las dos búsquedas exhaustivas, la cantidad de soluciones que fue
necesario evaluar. Las tres técnicas exploran únicamente soluciones factibles.

## Problemas

| Problema | Archivo |
|---|---|
| a) Asignación 1 a 1 | `asign1a1.py` |
| b) Distribución de un recurso | `recursos.py` |
| c) Mochila 0/1 | `mochila.py` |
| d) Vendedor (TSP) | `vendedor.py` |

Cada problema se implementa como una clase `ProblemaX` con los tres métodos de
búsqueda (`busqueda_greedy`, `busqueda_exhaustiva_pura` y
`busqueda_exhaustiva_ra`) y su propia clase de solución `SolucionX`.

## Técnicas de búsqueda

- **Greedy:** construye la solución tomando la mejor opción local en cada paso.
  Es rápida, pero no garantiza el óptimo.
- **Exhaustiva Pura:** explora todo el espacio de soluciones factibles mediante
  backtracking y garantiza el óptimo, a costa de un crecimiento factorial o
  exponencial.
- **Ramificación y Acotamiento:** recorre el mismo árbol de soluciones, pero poda
  las ramas cuya cota optimista no puede mejorar la mejor solución conocida.
  Alcanza el óptimo evaluando una fracción mucho menor de soluciones. En el
  problema de asignación se incluyen dos variantes del árbol: n-aria (un nivel
  por fila) y binaria, al estilo de Aho, Hopcroft y Ullman (incluir o excluir
  una pareja a la vez).

## Requisitos

- Python 3
- Dependencias listadas en `requirements.txt` (rich y matplotlib)

## Instalación

```bash
git clone https://github.com/MarinaCasCode/Tarea2-C31886-C03361.git
cd Tarea2-C31886-C03361
pip install -r requirements.txt
```

## Uso

Lanzar el menú interactivo para resolver cualquier problema con cualquier técnica:

```bash
python prueba.py
```

Generar las tablas comparativas de las tres técnicas en tamaños pequeño, mediano
y grande:

```bash
python experimentos.py
```

Generar los gráficos de tiempo y de soluciones evaluadas (se guardan en la
carpeta `graficos/`):

```bash
python graficos.py
```

Correr las pruebas de validación de cada problema:

```bash
python tests/test_assignment.py
python tests/test_mochila.py
python tests/test_vendedor.py
python tests/test_recursos.py
```

## Análisis empírico

El programa `experimentos.py` genera instancias aleatorias de tamaño pequeño,
mediano y grande para cada problema, y mide el valor de la solución, las
soluciones evaluadas y el tiempo de cada técnica. La búsqueda exhaustiva pura se
omite de forma automática cuando la cantidad estimada de soluciones deja de ser
viable.

El programa `graficos.py` produce dos figuras que muestran, en escala
logarítmica, cómo crecen el tiempo de ejecución y la cantidad de soluciones
evaluadas conforme aumenta el tamaño del problema. Ambos programas usan una
semilla fija (2026), por lo que los resultados son reproducibles.

El informe completo, con el análisis de complejidad teórico (Big-O), las tablas
empíricas y los gráficos, se entrega como documento aparte.

## Estructura del repositorio

```
prueba.py            menú principal (interfaz de consola)
tiempo.py            cronómetro de cada búsqueda
asign1a1.py          Problema a) Asignación 1 a 1
recursos.py          Problema b) Distribución de un recurso
mochila.py           Problema c) Mochila 0/1
vendedor.py          Problema d) Vendedor (TSP)
experimentos.py      tablas comparativas de las tres técnicas
graficos.py          generador de los gráficos de resultados
graficos/            figuras PNG producidas por graficos.py
tests/               pruebas de validación por problema
requirements.txt     dependencias del proyecto
```

## Notas de diseño

- Mochila: variante 0/1 (cada objeto tiene peso y beneficio); el greedy ordena
  los objetos por razón beneficio/peso.
- Vendedor (TSP): el recorrido es un ciclo que regresa a la ciudad de origen y
  la matriz de distancias es simétrica; un valor de -1 indica que no existe
  camino entre dos ciudades.
- Entrada de datos: por el menú, digitada a mano o generada aleatoriamente.
