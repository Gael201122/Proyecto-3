# Título: Ruta musical - Interfaz web con Streamlit
# Autor: Roberto Gael Torres Cervantes
# Fecha: 17/11/2026
# Descripción: Frontend de Dijkstra con CSV persistente y session_state
"""Interfaz Streamlit del Proyecto 3 (sobre grafo.py e io_handler.py)."""

import base64
import html
import io
import math
import random
import struct
import wave

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from io_handler import cargar_grafo, guardar_conexion

# Paleta: negro y dorado, club de jazz
NEGRO = "#0A0A0A"
PANEL = "#16130D"
LINEA = "#3B3220"
MARFIL = "#E9E4D8"
APAGADO = "#8A7F63"
ORO = "#E3B948"
DISPLAY = "Big Shoulders Display, Impact, sans-serif"

ESTILOS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Big+Shoulders+\
Display:wght@500;700;900&family=Instrument+Sans:wght@400;500;600&\
display=swap');

.stApp {
  background: radial-gradient(ellipse at 85% -10%,
                              #231B08 0%, #0A0A0A 55%);
  font-family: 'Instrument Sans', sans-serif;
}
header[data-testid="stHeader"] { background: transparent; }
div[data-testid="stToolbar"], #MainMenu, footer { display: none; }
.block-container {
  max-width: 1500px; padding-top: 2.4rem; padding-bottom: 3rem;
}
.stApp p, .stApp label, .stApp input, .stApp button {
  font-family: 'Instrument Sans', sans-serif;
}

.titulo {
  font-family: 'Big Shoulders Display', Impact, sans-serif;
  font-weight: 900; text-transform: uppercase;
  font-size: clamp(72px, 9vw, 150px); line-height: .84;
  letter-spacing: -.01em; color: #E9E4D8; margin: 0;
}
.barra { width: 96px; height: 14px; background: #E3B948;
         margin: 22px 0 16px 0; }
.bajada { color: #8A7F63; font-size: 17px; line-height: 1.5;
          max-width: 30ch; margin: 0 0 28px 0; }
.seccion {
  font-family: 'Big Shoulders Display', Impact, sans-serif;
  font-weight: 700; font-size: 34px; color: #E9E4D8;
  margin: 4px 0 10px 0;
}

[data-testid="stWidgetLabel"] p { color: #8A7F63; font-size: 15px; }
div[data-baseweb="input"], div[data-baseweb="base-input"] {
  border-radius: 0 !important;
}
button[kind^="primary"], button[kind^="primary"] p {
  color: #0A0A0A !important; font-weight: 600; border-radius: 0;
}

.resultado { display: flex; justify-content: space-between;
             align-items: flex-end; gap: 16px; }
.sax { height: 210px; width: auto; margin-right: 8px;
       filter: drop-shadow(0 0 18px rgba(227,185,72,.30)); }
.costo {
  font-family: 'Big Shoulders Display', Impact, sans-serif;
  font-weight: 900; font-size: 150px; line-height: .85;
  color: #E3B948; margin-top: 30px;
  text-shadow: 0 0 42px rgba(227,185,72,.35);
}
.leyenda { color: #8A7F63; font-size: 15px; margin: 6px 0 22px 0;
           font-family: 'Instrument Sans', sans-serif; }
.tramo {
  display: flex; justify-content: space-between; align-items: baseline;
  border-top: 1px solid #3B3220; padding: 9px 0; color: #E9E4D8;
  font-size: 18px; font-family: 'Instrument Sans', sans-serif;
}
.tramo b {
  font-family: 'Big Shoulders Display', Impact, sans-serif;
  font-size: 26px; color: #E3B948;
}
.vacio { border-top: 1px solid #3B3220; padding-top: 14px;
         color: #8A7F63; font-size: 16px; margin-top: 30px;
         font-family: 'Instrument Sans', sans-serif; }
audio { width: 100%; color-scheme: dark; margin-top: 8px; }

.tabla { width: 100%; border-collapse: collapse; margin-top: 8px; }
div[data-testid="stMarkdownContainer"] .tabla th,
div[data-testid="stMarkdownContainer"] .tabla td {
  border-left: 0; border-right: 0; border-top: 0;
}
.tabla th {
  font-family: 'Big Shoulders Display', Impact, sans-serif;
  font-weight: 700; font-size: 20px; color: #8A7F63;
  text-align: center; padding: 8px 6px; border-bottom: 1px solid #3B3220;
}
.tabla td { text-align: center; padding: 8px 6px; color: #8A7F63;
            font-size: 17px; border-bottom: 1px solid #1F1A10; }
.tabla td.visita { color: #E9E4D8; font-weight: 600; }
.tabla td.fijo { color: #0A0A0A; background: #E3B948; font-weight: 600; }
.nota-tabla { color: #8A7F63; font-size: 15px; margin: 12px 0 4px 0; }
</style>
"""

# Saxofón dibujado en SVG (se incrusta como imagen)
SAX_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 270">
<g fill="none" stroke="#E3B948" stroke-linecap="round"
   stroke-linejoin="round">
<path d="M 26 20 L 44 28" stroke-width="9"/>
<path d="M 44 28 C 62 24, 80 34, 84 58 L 102 200
         C 106 248, 152 256, 157 216 L 161 152" stroke-width="17"/>
</g>
<path d="M 152 164 C 150 148, 138 140, 133 124 L 189 124
         C 184 140, 171 148, 169 164 Z" fill="#E3B948"/>
<ellipse cx="161" cy="124" rx="28" ry="7" fill="#0A0A0A"
         stroke="#E3B948" stroke-width="3"/>
<g fill="#0A0A0A">
<circle cx="86.5" cy="84" r="4.5"/><circle cx="89.5" cy="108" r="4.5"/>
<circle cx="92.5" cy="132" r="4.5"/><circle cx="95.5" cy="156" r="4.5"/>
<circle cx="98.5" cy="180" r="4.5"/>
</g>
<g fill="#E3B948" stroke="#0A0A0A" stroke-width="1.5">
<circle cx="106" cy="96" r="3.5"/><circle cx="110" cy="124" r="3.5"/>
<circle cx="113" cy="152" r="3.5"/>
</g>
</svg>"""
SAX_B64 = base64.b64encode(SAX_SVG.encode("utf-8")).decode("ascii")
SAX_IMG = (f'<img class="sax" alt="Saxofón" '
           f'src="data:image/svg+xml;base64,{SAX_B64}">')

# Posiciones a mano: la altura de cada nota cambia como en un solo de jazz
POS_BASE = {
    "Do": (0.0, 0.0), "Re": (1.2, 1.4), "Mi": (2.4, -0.8),
    "Fa": (3.2, 1.6), "Sol": (4.6, 0.2), "La": (5.6, 2.0),
    "Si": (6.8, -0.6), "Do2": (7.8, 1.4),
}

# Frecuencias reales (Hz) de la escala de Do mayor
FRECUENCIA = {
    "Do": 261.63, "Re": 293.66, "Mi": 329.63, "Fa": 349.23,
    "Sol": 392.00, "La": 440.00, "Si": 493.88, "Do2": 523.25,
}


def configurar_pagina():
    """Configura la página e inyecta los estilos."""
    st.set_page_config(page_title="Ruta musical", layout="wide")
    st.markdown(ESTILOS, unsafe_allow_html=True)


def obtener_grafo():
    """Lee el CSV una sola vez y lo conserva en st.session_state."""
    if "grafo" not in st.session_state:
        try:
            st.session_state["grafo"] = cargar_grafo()
        except FileNotFoundError:
            st.error("No se encontró el archivo nodos.csv junto a app.py.")
            st.stop()
        except PermissionError:
            st.error("No hay permiso para leer el archivo nodos.csv.")
            st.stop()
        except ValueError as error:
            st.error(f"El archivo nodos.csv no es válido. {error}")
            st.stop()
    return st.session_state["grafo"]


def avisar(tipo, texto):
    """Guarda un mensaje para mostrarlo en la siguiente ejecución."""
    st.session_state["aviso"] = (tipo, texto)


def mostrar_aviso():
    """Muestra (y borra) el mensaje pendiente con st.success o st.error."""
    aviso = st.session_state.pop("aviso", None)
    if aviso:
        tipo, texto = aviso
        getattr(st, tipo)(texto)


def registrar_conexion():
    """Valida, guarda en nodos.csv y actualiza el grafo en memoria."""
    grafo = st.session_state["grafo"]
    try:
        origen, destino, peso = grafo.validar_arista(
            st.session_state["reg_origen"],
            st.session_state["reg_destino"],
            st.session_state["reg_peso"],
        )
        guardar_conexion(origen, destino, peso)
    except ValueError as error:
        avisar("error", str(error))
    except PermissionError:
        avisar("error", "No hay permiso para escribir en nodos.csv.")
    except OSError:
        avisar("error", "No se pudo escribir en nodos.csv.")
    else:
        grafo.agregar_arista(origen, destino, peso)
        avisar("success", f"Conexión {origen} - {destino} guardada.")
        for clave in ("reg_origen", "reg_destino", "reg_peso"):
            st.session_state[clave] = ""


def barra_lateral():
    """Formulario lateral para registrar nuevas conexiones."""
    with st.sidebar:
        st.markdown('<div class="seccion">Registrar conexión</div>',
                    unsafe_allow_html=True)
        st.caption("Si un nodo no existe, se crea junto con la conexión.")
        with st.form("form_registro"):
            st.text_input("Origen", key="reg_origen")
            st.text_input("Destino", key="reg_destino")
            st.text_input("Peso", key="reg_peso")
            st.form_submit_button("Guardar conexión", type="primary",
                                  on_click=registrar_conexion)
        mostrar_aviso()


def posiciones(nodos):
    """Coordenadas de cada nodo: las notas a mano, el resto en filas."""
    pos = {n: POS_BASE[n] for n in nodos if n in POS_BASE}
    extras = [n for n in nodos if n not in POS_BASE]
    for indice, nombre in enumerate(extras):
        fila, columna = divmod(indice, 6)
        pos[nombre] = (0.6 + columna * 1.5, -1.9 - fila * 1.2)
    return pos, math.ceil(len(extras) / 6)


def dibujar(grafo, ruta, origen, destino):
    """Dibuja la red; la ruta elegida se resalta en dorado."""
    nodos = grafo.nombres()
    pos, filas_extra = posiciones(nodos)
    en_ruta = set()
    if ruta:
        en_ruta = {frozenset(par) for par in zip(ruta, ruta[1:])}

    fig = go.Figure()
    for resaltada in (False, True):
        for a, b, peso in grafo.aristas():
            if (frozenset((a, b)) in en_ruta) != resaltada:
                continue
            x0, y0 = pos[a]
            x1, y1 = pos[b]
            if resaltada:  # halo dorado debajo de la ruta
                fig.add_trace(go.Scatter(
                    x=[x0, x1], y=[y0, y1], mode="lines",
                    line=dict(width=20, color="rgba(227,185,72,0.20)"),
                    hoverinfo="none", showlegend=False))
            fig.add_trace(go.Scatter(
                x=[x0, x1], y=[y0, y1], mode="lines",
                line=dict(width=6 if resaltada else 1.4,
                          color=ORO if resaltada else LINEA),
                hoverinfo="none", showlegend=False))
            fig.add_annotation(
                x=(x0 + x1) / 2, y=(y0 + y1) / 2, text=f"{peso}",
                showarrow=False, bgcolor=NEGRO, borderpad=3,
                font=dict(family=DISPLAY, size=20 if resaltada else 17,
                          color=ORO if resaltada else APAGADO))

    relleno, borde, texto, tamano = [], [], [], []
    for nombre in nodos:
        if nombre in (origen, destino):
            relleno.append(ORO)
            borde.append(MARFIL)
            texto.append(NEGRO)
            tamano.append(72)
        elif ruta and nombre in ruta:
            relleno.append(NEGRO)
            borde.append(ORO)
            texto.append(ORO)
            tamano.append(64)
        else:
            relleno.append(PANEL)
            borde.append(LINEA)
            texto.append(APAGADO)
            tamano.append(64)

    fig.add_trace(go.Scatter(
        x=[pos[n][0] for n in nodos], y=[pos[n][1] for n in nodos],
        mode="markers+text", text=[html.escape(n) for n in nodos],
        textposition="middle center",
        textfont=dict(family=DISPLAY, size=22, color=texto),
        marker=dict(size=tamano, color=relleno,
                    line=dict(width=3, color=borde)),
        hoverinfo="none", showlegend=False))

    xs = [p[0] for p in pos.values()] or [0]
    ys = [p[1] for p in pos.values()] or [0]
    fig.update_layout(
        height=560 + 100 * filas_extra, margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(visible=False, range=[min(xs) - 0.8, max(xs) + 0.8]),
        yaxis=dict(visible=False, range=[min(ys) - 0.9, max(ys) + 0.8]))
    return fig


@st.cache_data
def audio_de_ruta(ruta):
    """Sintetiza la ruta nota por nota con timbre de saxofón tenor."""
    tasa, duracion = 22050, 0.55
    azar = random.Random(7)
    # Armónicos: el saxofón tiene mucho cuerpo en el 2.º, 3.º y 4.º
    armonicos = [1.0, 0.85, 0.70, 0.50, 0.35, 0.25, 0.15, 0.10]
    total = sum(armonicos)
    muestras = []
    for nota in ruta:
        frecuencia = FRECUENCIA[nota] / 2  # una octava abajo (tenor)
        fase = 0.0
        for i in range(int(tasa * duracion)):
            t = i / tasa
            # vibrato lento que entra poco a poco
            vibrato = 1 + 0.007 * math.sin(2 * math.pi * 5.5 * t) * min(
                1.0, t / 0.2)
            fase += 2 * math.pi * frecuencia * vibrato / tasa
            ataque = min(1.0, t / 0.045)
            suelta = min(1.0, (duracion - t) / 0.09)
            envolvente = ataque * suelta * (0.85 + 0.15 * math.exp(-6 * t))
            onda = sum(a * math.sin(k * fase)
                       for k, a in enumerate(armonicos, start=1)) / total
            soplido = azar.gauss(0, 1) * 0.03
            muestras.append((0.8 * onda + soplido) * envolvente)

    # Eco corto, como en un club
    retraso = int(tasa * 0.16)
    salida = muestras + [0.0] * (retraso * 2)
    for i, muestra in enumerate(muestras):
        salida[i + retraso] += 0.28 * muestra
        salida[i + 2 * retraso] += 0.10 * muestra

    pico = max(abs(x) for x in salida) or 1.0
    datos = b"".join(struct.pack("<h", int(x / pico * 0.85 * 32767))
                     for x in salida)
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as archivo:
        archivo.setnchannels(1)
        archivo.setsampwidth(2)
        archivo.setframerate(tasa)
        archivo.writeframes(datos)
    return buffer.getvalue()


def tabla_pasos(nodos, pasos):
    """Tabla HTML con las distancias que Dijkstra va fijando."""
    cabecera = "".join(f"<th>{html.escape(n)}</th>" for n in nodos)
    filas = ""
    for numero, paso in enumerate(pasos, start=1):
        celdas = ""
        for nodo in nodos:
            distancia = paso["dist"][nodo]
            texto = "∞" if distancia == math.inf else str(distancia)
            clase = "fijo" if nodo in paso["fijos"] else ""
            celdas += f'<td class="{clase}">{texto}</td>'
        filas += (f'<tr><td>{numero}</td>'
                  f'<td class="visita">{html.escape(paso["visita"])}</td>'
                  f'{celdas}</tr>')
    return (f'<table class="tabla"><tr><th>Paso</th><th>Visita</th>'
            f'{cabecera}</tr>{filas}</table>'
            '<p class="nota-tabla">Cada fila muestra las distancias al fijar '
            'el nodo visitado. En dorado, las ya definitivas; ∞ significa '
            'que aún no se llega.</p>')


def encabezado():
    """Título grande de la página."""
    st.markdown(
        '<div class="titulo">Ruta<br>musical</div>'
        '<div class="barra"></div>'
        '<p class="bajada">Escribe dos nodos. La ruta más barata '
        'se ilumina.</p>',
        unsafe_allow_html=True)


def calcular_ruta(grafo, texto_origen, texto_destino):
    """Valida los nodos escritos y ejecuta Dijkstra.

    Devuelve (origen, destino, ruta, costo, pasos) o None si hay un error.
    """
    if not texto_origen.strip() or not texto_destino.strip():
        st.info("Escribe un nodo de origen y uno de destino.")
        return None
    try:
        origen = grafo.resolver_nodo(texto_origen)
        destino = grafo.resolver_nodo(texto_destino)
    except KeyError as error:
        st.error(error.args[0])
        return None
    costo, ruta = grafo.dijkstra(origen, destino)
    return origen, destino, ruta or None, costo, grafo.pasos


def sax_con_mensaje(mensaje):
    """Muestra un texto corto junto al saxofón."""
    st.markdown(f'<div class="resultado"><div class="vacio">{mensaje}'
                f'</div>{SAX_IMG}</div>', unsafe_allow_html=True)


def panel_resultado(resultado):
    """Muestra costo, tramos, saxofón y audio de la ruta encontrada."""
    if resultado is None:
        st.markdown(f'<div class="resultado"><div></div>{SAX_IMG}</div>',
                    unsafe_allow_html=True)
        return
    origen, destino, ruta, costo, _ = resultado
    if origen == destino:
        sax_con_mensaje("Elige dos nodos distintos para ver la ruta.")
    elif ruta is None:
        st.warning(f"No existe una ruta posible entre {origen} "
                   f"y {destino}.")
        sax_con_mensaje("Prueba con otra pareja de nodos.")
    else:
        grafo = st.session_state["grafo"]
        tramos = "".join(
            f'<div class="tramo"><span>{html.escape(a)} a '
            f'{html.escape(b)}</span><b>{grafo.peso(a, b)}</b></div>'
            for a, b in zip(ruta, ruta[1:]))
        st.markdown(
            '<div class="resultado"><div>'
            f'<div class="costo">{costo}</div>'
            '<div class="leyenda">costo total</div>'
            f'</div>{SAX_IMG}</div>{tramos}',
            unsafe_allow_html=True)
        notas = tuple(n for n in ruta if n in FRECUENCIA)
        if notas:
            st.markdown('<div class="leyenda" style="margin:20px 0 0 0">'
                        'Escucha la ruta en saxofón</div>',
                        unsafe_allow_html=True)
            st.audio(audio_de_ruta(notas), format="audio/wav")


def pestanas_datos(grafo, resultado):
    """Pestañas con la red actual (pandas) y el paso a paso."""
    tab_red, tab_pasos = st.tabs(["Red actual", "Paso a paso de Dijkstra"])
    with tab_red:
        tabla = pd.DataFrame(grafo.aristas(),
                             columns=["Origen", "Destino", "Peso"])
        st.caption(f"{len(grafo.nombres())} nodos y {len(tabla)} conexiones")
        st.dataframe(tabla, hide_index=True, width="stretch")
    with tab_pasos:
        if resultado is None:
            st.info("Calcula una ruta para ver el detalle del algoritmo.")
        else:
            st.markdown(tabla_pasos(grafo.nombres(), resultado[4]),
                        unsafe_allow_html=True)


def main():
    """Arma la interfaz completa."""
    configurar_pagina()
    grafo = obtener_grafo()
    barra_lateral()

    izquierda, derecha = st.columns([2, 3], gap="large")
    with izquierda:
        encabezado()
        col_origen, col_destino = st.columns(2)
        texto_origen = col_origen.text_input("Desde", value="Do")
        texto_destino = col_destino.text_input("Hasta", value="Do2")
        resultado = calcular_ruta(grafo, texto_origen, texto_destino)
        panel_resultado(resultado)

    with derecha:
        origen = resultado[0] if resultado else None
        destino = resultado[1] if resultado else None
        ruta = resultado[2] if resultado else None
        st.plotly_chart(dibujar(grafo, ruta, origen, destino),
                        width="stretch", theme=None)

    st.write("")
    pestanas_datos(grafo, resultado)


main()
