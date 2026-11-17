# Título: Ejecución de Dijkstra por consola
# Autor: Roberto Gael Torres Cervantes
# Fecha: 17/11/2026
# Descripción: Versión de consola (Proyecto 2) que usa grafo.py e io_handler
"""Programa de consola: pide origen y destino y muestra la ruta."""

from io_handler import cargar_grafo


def main():
    """Carga el grafo y calcula rutas hasta que el usuario deje vacío."""
    try:
        grafo = cargar_grafo()
    except FileNotFoundError:
        print("No se encontró el archivo nodos.csv.")
        return
    except ValueError as error:
        print(f"El archivo nodos.csv no es válido: {error}")
        return

    print("Nodos disponibles:", ", ".join(grafo.nombres()))
    while True:
        texto_origen = input("Nodo origen (Enter para salir): ")
        if not texto_origen.strip():
            break
        texto_destino = input("Nodo destino: ")
        try:
            origen = grafo.resolver_nodo(texto_origen)
            destino = grafo.resolver_nodo(texto_destino)
        except KeyError as error:
            print(error.args[0])
            continue
        distancia, ruta = grafo.dijkstra(origen, destino)
        if not ruta:
            print(f"No existe camino entre {origen} y {destino}.")
        else:
            print(f"Distancia/costo total: {distancia}")
            print("Ruta: " + " -> ".join(ruta))


if __name__ == "__main__":
    main()
