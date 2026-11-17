# Título: Grafo y algoritmo de Dijkstra (Proyecto 1 reutilizado)
# Autor: Roberto Gael Torres Cervantes
# Fecha: 17/11/2026
# Descripción: Clases Nodo y Grafo con Dijkstra, lógica base del Proyecto 3
"""Proyecto 1: Algoritmo de Dijkstra
Programación III - 2026B

Encuentra la ruta más corta en un grafo ponderado (red de transporte)
usando Programación Orientada a Objetos. En el Proyecto 3 se reutiliza
como lógica de negocio de la interfaz web.
"""

import heapq
import math


def validar_peso(valor):
    """Convierte el peso a número y lanza ValueError si no es válido."""
    try:
        peso = float(str(valor).strip())
    except ValueError:
        raise ValueError("El peso debe ser un número.") from None
    if not math.isfinite(peso):
        raise ValueError("El peso debe ser un número finito.")
    if peso < 0:
        raise ValueError("Dijkstra no admite pesos negativos")
    return int(peso) if peso.is_integer() else peso


class Nodo:
    """Representa un nodo (estación/ciudad) del grafo."""

    def __init__(self, nombre):
        self.nombre = nombre
        self.vecinos = {}  # {Nodo: peso}

    def agregar_vecino(self, vecino, peso):
        self.vecinos[vecino] = peso

    def __repr__(self):
        return f"Nodo({self.nombre})"


class Grafo:
    """Grafo ponderado no dirigido."""

    def __init__(self):
        self.nodos = {}  # {nombre: Nodo}
        self.pasos = []  # detalle del último Dijkstra (para la interfaz)

    def agregar_nodo(self, nombre):
        if nombre not in self.nodos:
            self.nodos[nombre] = Nodo(nombre)
        return self.nodos[nombre]

    def nombre_canonico(self, texto):
        """Devuelve el nombre ya registrado que coincide sin importar
        mayúsculas, o el texto limpio si el nodo todavía no existe."""
        nombre = (texto or "").strip()
        for existente in self.nodos:
            if existente.lower() == nombre.lower():
                return existente
        return nombre

    def validar_arista(self, origen, destino, peso):
        """Valida una conexión y la devuelve limpia (origen, destino, peso).

        Lanza ValueError si falta un nodo, si son iguales o si el peso
        no es un número válido.
        """
        nombre_origen = self.nombre_canonico(origen)
        nombre_destino = self.nombre_canonico(destino)
        if not nombre_origen or not nombre_destino:
            raise ValueError("Origen y destino no pueden estar vacíos.")
        if nombre_origen.lower() == nombre_destino.lower():
            raise ValueError("Origen y destino deben ser distintos.")
        return nombre_origen, nombre_destino, validar_peso(peso)

    def agregar_arista(self, origen, destino, peso):
        origen, destino, peso = self.validar_arista(origen, destino, peso)
        a = self.agregar_nodo(origen)
        b = self.agregar_nodo(destino)
        a.agregar_vecino(b, peso)
        b.agregar_vecino(a, peso)  # no dirigido

    def resolver_nodo(self, texto):
        """Devuelve el nodo escrito por el usuario o lanza KeyError."""
        nombre = self.nombre_canonico(texto)
        if nombre not in self.nodos:
            raise KeyError(f"El nodo '{(texto or '').strip()}' no existe.")
        return nombre

    def nombres(self):
        """Lista de nombres de nodos en el orden en que se registraron."""
        return list(self.nodos)

    def peso(self, origen, destino):
        """Peso de la conexión directa entre dos nodos."""
        return self.nodos[origen].vecinos[self.nodos[destino]]

    def aristas(self):
        """Lista de conexiones únicas como tuplas (origen, destino, peso)."""
        vistas = set()
        resultado = []
        for nodo in self.nodos.values():
            for vecino, peso in nodo.vecinos.items():
                par = frozenset((nodo.nombre, vecino.nombre))
                if par not in vistas:
                    vistas.add(par)
                    resultado.append((nodo.nombre, vecino.nombre, peso))
        return resultado

    def dijkstra(self, origen, destino):
        """Devuelve (distancia_total, ruta) o (inf, []) si no hay camino."""
        if origen not in self.nodos or destino not in self.nodos:
            raise KeyError("Origen o destino no existe en el grafo")

        self.pasos = []
        inicio = self.nodos[origen]
        fin = self.nodos[destino]

        distancias = {n: float("inf") for n in self.nodos.values()}
        previo = {}
        distancias[inicio] = 0
        # (distancia, nombre) -> evita comparar Nodos
        cola = [(0, inicio.nombre)]
        visitados = set()

        while cola:
            dist_actual, nombre = heapq.heappop(cola)
            actual = self.nodos[nombre]
            if actual in visitados:
                continue
            visitados.add(actual)
            # Se guarda el estado al fijar cada nodo (tabla de la interfaz)
            self.pasos.append({
                "visita": nombre,
                "dist": {n.nombre: d for n, d in distancias.items()},
                "fijos": {n.nombre for n in visitados},
            })
            if actual is fin:
                break
            for vecino, peso in actual.vecinos.items():
                nueva = dist_actual + peso
                if nueva < distancias[vecino]:
                    distancias[vecino] = nueva
                    previo[vecino] = actual
                    heapq.heappush(cola, (nueva, vecino.nombre))

        if distancias[fin] == float("inf"):
            return float("inf"), []

        ruta = []
        nodo = fin
        while nodo is not inicio:
            ruta.append(nodo.nombre)
            nodo = previo[nodo]
        ruta.append(inicio.nombre)
        ruta.reverse()
        return distancias[fin], ruta
