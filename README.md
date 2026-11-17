# Proyecto 3: Ruta musical (Streamlit)

Interfaz web interactiva para calcular la ruta más barata entre notas
musicales con el algoritmo de Dijkstra. Es la capa visual sobre el motor
de grafos (Proyecto 1) y la persistencia en CSV (Proyecto 2).

## Archivos

| Archivo         | Función                                          |
|-----------------|--------------------------------------------------|
| `app.py`        | Interfaz visual en Streamlit                     |
| `main.py`       | Ejecución por consola (Proyecto 2)               |
| `grafo.py`      | Clases `Nodo` y `Grafo` con Dijkstra (Proyecto 1)|
| `io_handler.py` | Lectura y escritura de `nodos.csv`               |
| `nodos.csv`     | Base de datos de tramos (origen, destino, peso)  |

## Cómo ejecutarlo

```
pip install -r requirements.txt
streamlit run app.py
```

Versión de consola: `python main.py`

## Calidad de código

```
flake8 .
```

Autor: Roberto Gael Torres Cervantes
