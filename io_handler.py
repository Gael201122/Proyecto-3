# Título: Lectura y escritura del archivo nodos.csv
# Autor: Roberto Gael Torres Cervantes
# Fecha: 17/11/2026
# Descripción: Carga el grafo desde CSV y guarda nuevas conexiones en disco
"""Persistencia del Proyecto 3 (reutilizable desde main.py y app.py)."""

import csv
from pathlib import Path

from grafo import Grafo, validar_peso

RUTA_CSV = Path(__file__).with_name("nodos.csv")
ENCABEZADO = ["origen", "destino", "peso"]


def cargar_grafo(ruta=RUTA_CSV):
    """Lee el CSV y devuelve un Grafo.

    Lanza FileNotFoundError si el archivo no existe y ValueError si el
    encabezado o alguna fila no son válidos.
    """
    grafo = Grafo()
    with open(ruta, newline="", encoding="utf-8-sig") as archivo:
        lector = csv.DictReader(archivo)
        if lector.fieldnames is None or not set(ENCABEZADO) <= set(
                lector.fieldnames):
            raise ValueError("El CSV debe tener las columnas "
                             "origen, destino y peso.")
        for numero, fila in enumerate(lector, start=2):
            try:
                grafo.agregar_arista(fila.get("origen") or "",
                                     fila.get("destino") or "",
                                     fila.get("peso") or "")
            except ValueError as error:
                raise ValueError(f"Fila {numero} del CSV: {error}") from error
    return grafo


def guardar_conexion(origen, destino, peso, ruta=RUTA_CSV):
    """Agrega una conexión al final del CSV (crea el archivo si no existe).

    Lanza PermissionError u OSError si no se puede escribir en disco.
    """
    ruta = Path(ruta)
    peso = validar_peso(peso)
    tiene_datos = ruta.exists() and ruta.stat().st_size > 0
    falta_salto = False
    if tiene_datos:
        with open(ruta, "rb") as archivo:
            archivo.seek(-1, 2)
            falta_salto = archivo.read(1) not in (b"\n", b"\r")
    with open(ruta, "a", newline="", encoding="utf-8") as archivo:
        if falta_salto:
            archivo.write("\n")
        escritor = csv.writer(archivo, lineterminator="\n")
        if not tiene_datos:
            escritor.writerow(ENCABEZADO)
        escritor.writerow([origen, destino, peso])
