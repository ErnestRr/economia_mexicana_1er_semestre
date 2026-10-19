"""
Gráficas del análisis de la economía mexicana: ¿Llegaremos a las metas de crecimiento este año?

Todas las cifras fueron transcritas de los boletines oficiales del INEGI
(carpeta ./data) y de las encuestas de expectativas citadas abajo.

Fuentes:
- IGAE julio 2026 (boletín 603/26, 24-sep-2026):
  https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2026/igae/igae2026_09.pdf
- IOAE agosto 2026 (boletín 597/26, 22-sep-2026):
  https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2026/ioae/ioae2026_09.pdf
- PIB trimestral a precios corrientes 2T-2026 (boletín 501/26, 24-ago-2026):
  https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2026/pibt/pib_Pcorr2026_08.pdf
- Productividad laboral y costo unitario de la mano de obra 2T-2026 (boletín 589/26, 10-sep-2026):
  https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2026/iplcumo/iplcumo2026_09.pdf
- Paquete Económico 2027 (SHCP, 8-sep-2026) y Encuesta Citi (6-oct-2026).
"""

import pandas as pd
import plotly.graph_objects as go


# Mes y año en que se recopilaron los datos.
FECHA_FUENTE = "octubre 2026"

# Firma que aparece en la esquina inferior derecha. Cámbiala por tu nombre o usuario.
FIRMA = "Elaboración propia"

# Paletas de colores (validadas para contraste y daltonismo en ambos fondos).
# Los colores de los datos son iguales en los dos temas; cambian fondos, textos y líneas.
TEMAS = {
    "oscuro": {
        "PLOT_COLOR": "#1C1F1A",
        "PAPER_COLOR": "#1C1F1A",
        "TEXTO": "#F2F4EF",
        "TEXTO_SECUNDARIO": "#A9B0A4",
        "LINEA": "#4A5146",
        "GRID": "#3A4037",
        "CAJA": "#111311",
        "CERO": "#6B7367",
        "CONECTOR": "#4A5146",
        "POSITIVO": "#11A3B5",
        "NEGATIVO": "#E5574A",
        "COLORES_GRUPO": {"Terciarias": "#11A3B5", "Secundarias": "#C47D14", "Primarias": "#A95BC0"},
        "PRODUCTIVIDAD": "#11A3B5",
        "REMUNERACION": "#C47D14",
        # Etiquetas de valor en el color de su barra.
        "ETIQ_POS": "#11A3B5",
        "ETIQ_NEG": "#E5574A",
        "ETIQ_GRUPO": {"Terciarias": "#11A3B5", "Secundarias": "#C47D14", "Primarias": "#A95BC0"},
        # Estilo de reporte: rejilla punteada, sin marco, barras redondeadas y franja detrás del título.
        "ESTILO_REPORTE": True,
        "BANDA_TITULO": "#2B2819",
        "CARPETA_IMGS": "./imgs",
    },
    # Estilo "hecho con Python" para los PNG oscuros: ejes enmarcados, rejilla sólida,
    # barras rectas y etiquetas blancas (el estilo original, para copiar y pegar).
    "oscuro_python": {
        "PLOT_COLOR": "#1C1F1A",
        "PAPER_COLOR": "#262B23",
        "TEXTO": "#FFFFFF",
        "TEXTO_SECUNDARIO": "#B8BDB5",
        "LINEA": "#5A6156",
        "GRID": "#343A31",
        "CAJA": "#111311",
        "CERO": "#8A9186",
        "CONECTOR": "#6B7367",
        "POSITIVO": "#11A3B5",
        "NEGATIVO": "#E5574A",
        "COLORES_GRUPO": {"Terciarias": "#11A3B5", "Secundarias": "#C47D14", "Primarias": "#A95BC0"},
        "PRODUCTIVIDAD": "#11A3B5",
        "REMUNERACION": "#C47D14",
        "ETIQ_POS": None,
        "ETIQ_NEG": None,
        "ETIQ_GRUPO": None,
        "ESTILO_REPORTE": False,
        "BANDA_TITULO": None,
        "CARPETA_IMGS": "./imgs",
    },
    # Estilo de reporte de BI: fondo blanco, barras pastel, etiquetas de color y título en franja amarilla.
    "claro": {
        "PLOT_COLOR": "#FFFFFF",
        "PAPER_COLOR": "#FFFFFF",
        "TEXTO": "#252423",
        "TEXTO_SECUNDARIO": "#605E5C",
        "LINEA": "#C8C6C4",
        "GRID": "#D2CFCB",
        "CAJA": "#FAFAFA",
        "CERO": "#C8C6C4",
        "CONECTOR": "#D2D0CE",
        "POSITIVO": "#A8DDB0",
        "NEGATIVO": "#F4B6AE",
        "COLORES_GRUPO": {"Terciarias": "#A9D2F7", "Secundarias": "#F7CF8D", "Primarias": "#D3B5EA"},
        "PRODUCTIVIDAD": "#1F86E0",
        "REMUNERACION": "#E8912D",
        "ETIQ_POS": "#1E9E3A",
        "ETIQ_NEG": "#D93A2B",
        "ETIQ_GRUPO": {"Terciarias": "#1F86E0", "Secundarias": "#B26F0A", "Primarias": "#8E5BB5"},
        "ESTILO_REPORTE": True,
        "BANDA_TITULO": "#FDF3D8",
        "CARPETA_IMGS": "./imgs/claro",
    },
}

TEMA = "oscuro"


def usar_tema(nombre):
    """Cambia la paleta activa ('oscuro' o 'claro') para todas las gráficas."""

    global TEMA
    TEMA = nombre
    globals().update(TEMAS[nombre])


usar_tema("oscuro")

FUENTE_TIPOGRAFICA = "Segoe UI, Inter, Lato, Arial"


def estilo_base(fig, titulo, subtitulo, fuente, eje_x):
    """
    Aplica el estilo común: fondo oscuro, título con subtítulo,
    y el pie con fuente, título del eje y firma.
    """

    fig.update_layout(
        width=1920,
        height=1080,
        font_family=FUENTE_TIPOGRAFICA,
        font_color=TEXTO,
        font_size=24,
        title_text=f"{titulo}<br><span style='font-size:24px;color:{TEXTO_SECUNDARIO}'>{subtitulo}</span>",
        title_x=0.5,
        title_y=0.96,
        title_xanchor="center",
        title_font_size=38,
        margin_t=150,
        margin_r=50,
        margin_b=130,
        plot_bgcolor=PLOT_COLOR,
        paper_bgcolor=PAPER_COLOR,
        legend_itemsizing="constant",
        legend_bgcolor="rgba(0,0,0,0)",
    )

    pie = [
        dict(x=0.0, xanchor="left", text=f"Fuente: {fuente} ({FECHA_FUENTE})"),
        dict(x=0.5, xanchor="center", text=eje_x),
        dict(x=1.0, xanchor="right", text=FIRMA),
    ]

    for p in pie:
        fig.add_annotation(
            y=-0.1,
            xref="paper",
            yref="paper",
            yanchor="top",
            showarrow=False,
            font_color=TEXTO_SECUNDARIO,
            font_size=20,
            **p,
        )

    return fig


def ejes(fig, **kwargs_y):
    """Ejes recesivos con el mismo estilo en todas las gráficas."""

    comunes = dict(
        linecolor=LINEA,
        tickcolor=LINEA,
        linewidth=1.5,
        showline=True,
        mirror=True,
        ticks="outside",
        ticklen=8,
        gridcolor=GRID,
        gridwidth=1,
        zeroline=False,
    )

    if ESTILO_REPORTE:
        comunes.update(mirror=False, griddash="dot", linewidth=1.5, tickcolor=GRID)
        fig.update_traces(textfont_weight="bold", selector=dict(type="bar"))
        fig.update_layout(barcornerradius=4)

    fig.update_xaxes(**comunes)
    fig.update_yaxes(**comunes, **kwargs_y)


def color_etiqueta(valor):
    """Color de la etiqueta de valor según el signo (en estilo reporte va del color de la barra)."""

    if ETIQ_POS is None:
        return TEXTO
    return ETIQ_POS if valor >= 0 else ETIQ_NEG


def finalizar(fig):
    """En estilo reporte, dibuja la franja amarilla detrás del título (solo para los PNG)."""

    if not BANDA_TITULO:
        return

    margen_t = fig.layout.margin.t
    alto_grafica = fig.layout.height - margen_t - fig.layout.margin.b

    fig.add_shape(
        type="rect",
        xref="paper",
        yref="paper",
        x0=-1,
        x1=2,
        y0=1 + (margen_t - 118) / alto_grafica,
        y1=1 + (margen_t + 10) / alto_grafica,
        fillcolor=BANDA_TITULO,
        line_color=LINEA,
        line_width=1.5,
        layer="below",
    )


def caja_datos(fig, texto, x, y, xanchor="left", yanchor="top"):
    """Recuadro con la lectura rápida de las cifras clave."""

    fig.add_annotation(
        x=x,
        y=y,
        xref="paper",
        yref="paper",
        xanchor=xanchor,
        yanchor=yanchor,
        showarrow=False,
        align="left",
        bordercolor=LINEA,
        borderwidth=1.5,
        borderpad=12,
        bgcolor=CAJA,
        font_size=22,
        text=texto,
    )


def plot_pulso_mensual(guardar=True):
    """
    Gráfica 1: variación mensual del IGAE desestacionalizado
    de julio 2024 a julio 2026, más la estimación oportuna (IOAE) de agosto.
    """

    df = pd.read_csv("./data/igae_variacion_mensual.csv", parse_dates=["PERIODO"])

    obs = df[df["TIPO"] == "observado"]
    est = df[df["TIPO"] == "estimado"]

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=obs["PERIODO"],
            y=obs["VARIACION_MENSUAL"],
            marker_color=[POSITIVO if v >= 0 else NEGATIVO for v in obs["VARIACION_MENSUAL"]],
            marker_line_width=0,
            name="IGAE observado",
            showlegend=False,
        )
    )

    # La estimación oportuna se distingue con textura y su intervalo de confianza al 95%.
    fig.add_trace(
        go.Bar(
            x=est["PERIODO"],
            y=est["VARIACION_MENSUAL"],
            marker_color=PLOT_COLOR,
            marker_line_color=POSITIVO,
            marker_line_width=3,
            marker_pattern_shape="/",
            marker_pattern_fgcolor=POSITIVO,
            error_y=dict(
                type="data",
                symmetric=False,
                array=est["LIM_SUP"] - est["VARIACION_MENSUAL"],
                arrayminus=est["VARIACION_MENSUAL"] - est["LIM_INF"],
                color=TEXTO_SECUNDARIO,
                thickness=2.5,
                width=14,
            ),
            showlegend=False,
        )
    )

    fig.add_hline(y=0, line_color=CERO, line_width=2)

    # Etiquetas selectivas: solo los meses que cuentan la historia.
    destacados = {
        "2026-01-01": ("Ene-26: -1.0%", "bottom"),
        "2026-04-01": ("Abr-26: +1.5%", "top"),
        "2026-07-01": ("Jul-26: +0.8%", "top"),
    }

    for fecha, (texto, pos) in destacados.items():
        valor = df.loc[df["PERIODO"] == fecha, "VARIACION_MENSUAL"].iloc[0]
        fig.add_annotation(
            x=fecha,
            y=valor,
            text=f"<b>{texto}</b>",
            showarrow=False,
            yshift=26 if pos == "top" else -26,
            font_size=22,
        )

    fig.add_annotation(
        x=est["PERIODO"].iloc[0],
        y=est["LIM_SUP"].iloc[0],
        text="Ago-26 estimado<br>(IOAE): +0.1%",
        showarrow=False,
        yshift=40,
        font_size=20,
        font_color=TEXTO_SECUNDARIO,
    )

    caja_datos(
        fig,
        "<b>¿Llegaremos a la meta?</b>"
        "<br>Acumulado ene–jul 2026: <b>+1.5%</b> anual"
        "<br>Julio 2026: <b>+3.3%</b> anual"
        "<br>Agosto (estimación IOAE): <b>+2.5%</b> anual"
        "<br>"
        "<br>Meta Hacienda 2026: <b>1.0% – 2.0%</b>"
        "<br>Consenso analistas (Citi): <b>1.4%</b>",
        x=0.015,
        y=0.97,
    )

    # Etiquetas del eje en español, cada dos meses.
    meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
    ticks = df["PERIODO"].iloc[::2]

    fig.update_xaxes(
        tickvals=ticks,
        ticktext=[f"{meses[f.month - 1]}<br>{f.year}" for f in ticks],
        range=["2024-06-10", "2026-08-25"],
        showgrid=False,
    )

    ejes(fig, title="Variación % respecto al mes anterior", range=[-1.6, 2.4], dtick=0.4, tickformat=".1f", title_standoff=15)

    fig.update_layout(bargap=0.25)

    estilo_base(
        fig,
        "Variación mensual del Indicador Global de la Actividad Económica (IGAE)",
        "Cifras desestacionalizadas, julio 2024–julio 2026. Agosto: estimación oportuna (IOAE) con intervalo de confianza al 95%",
        "INEGI, IGAE e IOAE; SHCP; Encuesta Citi",
        "Mes de referencia",
    )

    if guardar:
        finalizar(fig)
        fig.write_image(f"{CARPETA_IMGS}/1_igae_pulso_mensual.png")
    return fig


def plot_peso_sectores(guardar=True):
    """
    Gráfica 2: participación de cada sector SCIAN en el valor agregado bruto
    nominal del segundo trimestre de 2026.
    """

    df = pd.read_csv("./data/pib_nominal_sectores_2t2026.csv")
    df = df.sort_values("PARTICIPACION")

    fig = go.Figure()

    # Una traza por grupo para que la leyenda identifique el color.
    for grupo in ["Terciarias", "Secundarias", "Primarias"]:
        sub = df[df["GRUPO"] == grupo]
        fig.add_trace(
            go.Bar(
                y=sub["SECTOR"],
                x=sub["PARTICIPACION"],
                orientation="h",
                marker_color=COLORES_GRUPO[grupo],
                marker_line_width=0,
                text=sub["PARTICIPACION"].map(lambda v: f"{v:.1f}%"),
                textposition="outside",
                textfont_color=ETIQ_GRUPO[grupo] if ETIQ_GRUPO else TEXTO,
                cliponaxis=False,
                name=f"Actividades {grupo.lower()}",
            )
        )

    # Totales oficiales del boletín (la suma de los parciales difiere por redondeo).
    totales = {"Terciarias": 63.4, "Secundarias": 32.6, "Primarias": 4.0}
    manuf_constr = df.loc[df["SECTOR"].isin(["Manufactura", "Construcción"]), "PARTICIPACION"].sum()

    caja_datos(
        fig,
        "<b>Peso en la economía</b>"
        f"<br>Comercio y servicios: <b>{totales['Terciarias']:.1f}%</b>"
        f"<br>Industria: <b>{totales['Secundarias']:.1f}%</b>"
        f"<br>   Manufactura + construcción: <b>{manuf_constr:.1f}%</b>"
        f"<br>Agropecuario: <b>{totales['Primarias']:.1f}%</b>"
        "<br><br>Comercio (mayor + menor): <b>20.3%</b>",
        x=0.98,
        y=0.04,
        xanchor="right",
        yanchor="bottom",
    )

    ejes(fig, categoryorder="array", categoryarray=df["SECTOR"].tolist(), ticksuffix="  ", showgrid=False)
    fig.update_xaxes(range=[0, 23.5], ticksuffix="%", dtick=2.5)

    fig.update_layout(
        barmode="overlay",
        bargap=0.22,
        margin_l=40,
        legend_x=0.98,
        legend_xanchor="right",
        legend_y=0.42,
        legend_yanchor="bottom",
        legend_orientation="v",
    )

    estilo_base(
        fig,
        "Participación de cada sector en el PIB",
        "Participación % de cada sector (SCIAN) en el valor agregado bruto a precios corrientes, segundo trimestre de 2026",
        "INEGI, PIB trimestral a precios corrientes",
        "% del valor agregado bruto",
    )

    if guardar:
        finalizar(fig)
        fig.write_image(f"{CARPETA_IMGS}/2_peso_sectores_pib.png")
    return fig


def plot_crecimiento_sectores(guardar=True):
    """
    Gráfica 3: crecimiento anual de cada sector en julio de 2026 contra el IGAE total.
    Sirve como referencia (benchmark) para comparar el P&L de cada empresa.
    """

    df = pd.read_csv("./data/igae_sectores_julio2026.csv")
    pesos = pd.read_csv("./data/pib_nominal_sectores_2t2026.csv")[["SCIAN", "PARTICIPACION"]]

    df = df.merge(pesos, on="SCIAN", how="left").sort_values("VAR_ANUAL_JUL2026")

    # La etiqueta del eje incluye el peso del sector en el PIB.
    df["ETIQUETA"] = df.apply(
        lambda r: f"{r['SECTOR']} <span style='color:{TEXTO_SECUNDARIO}'>({r['PARTICIPACION']:.1f}% PIB)</span>",
        axis=1,
    )

    total_igae = 3.4

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            y=df["ETIQUETA"],
            x=df["VAR_ANUAL_JUL2026"],
            orientation="h",
            marker_color=[POSITIVO if v >= 0 else NEGATIVO for v in df["VAR_ANUAL_JUL2026"]],
            marker_line_width=0,
            text=df["VAR_ANUAL_JUL2026"].map(lambda v: f"{v:+.1f}%"),
            textposition="outside",
            textfont_color=[color_etiqueta(v) for v in df["VAR_ANUAL_JUL2026"]] if ETIQ_POS else TEXTO,
            cliponaxis=False,
            showlegend=False,
        )
    )

    fig.add_vline(x=0, line_color=CERO, line_width=2)
    fig.add_vline(x=total_igae, line_color=TEXTO, line_width=2.5, line_dash="dash")

    fig.add_annotation(
        x=total_igae,
        y=1.0,
        yref="paper",
        text=f"<b>IGAE total: +{total_igae}%</b>  ← tu benchmark",
        showarrow=False,
        xanchor="left",
        yanchor="bottom",
        xshift=8,
        font_size=22,
    )

    caja_datos(
        fig,
        "<b>Cómo leerla</b>"
        "<br>Si tu sector está a la derecha de la línea"
        "<br>y tu empresa no creció: estás cediendo"
        "<br>cuota de mercado.",
        x=0.98,
        y=0.04,
        xanchor="right",
        yanchor="bottom",
    )

    ejes(fig, ticksuffix="  ", showgrid=False)
    fig.update_xaxes(range=[-6, 15.5], ticksuffix="%", dtick=2)

    fig.update_layout(bargap=0.22, margin_l=40)

    estilo_base(
        fig,
        "Crecimiento anual por sector frente al IGAE total",
        "Variación % anual real del IGAE por sector SCIAN, julio de 2026 vs. julio de 2025 (cifras originales)",
        "INEGI, IGAE y PIB trimestral",
        "Variación % anual",
    )

    if guardar:
        finalizar(fig)
        fig.write_image(f"{CARPETA_IMGS}/3_crecimiento_sectores_julio.png")
    return fig


def plot_productividad_costos(guardar=True):
    """
    Gráfica 4: volumen vendido, productividad laboral y remuneración real por sector.
    Cuando la remuneración crece más que la productividad, sube el costo unitario
    de la mano de obra (ICUMO) y el margen se comprime.
    """

    df = pd.read_csv("./data/productividad_costo_2t2026.csv")
    df = df.sort_values("COSTO_UNITARIO")

    fig = go.Figure()

    # Conector entre productividad y remuneración: su distancia es la presión sobre el margen.
    for _, r in df.iterrows():
        fig.add_trace(
            go.Scatter(
                x=[r["PRODUCTIVIDAD"], r["REMUNERACION_REAL"]],
                y=[r["SECTOR"]] * 2,
                mode="lines",
                line_color=CONECTOR,
                line_width=6,
                showlegend=False,
                hoverinfo="skip",
            )
        )

    marcadores = [
        ("VOLUMEN", "Ventas / producción reales", "diamond-open", TEXTO, 24),
        ("PRODUCTIVIDAD", "Productividad laboral", "circle", PRODUCTIVIDAD, 30),
        ("REMUNERACION_REAL", "Remuneración media real", "circle", REMUNERACION, 30),
    ]

    for col, nombre, simbolo, color, tam in marcadores:
        fig.add_trace(
            go.Scatter(
                x=df[col],
                y=df["SECTOR"],
                mode="markers",
                marker_symbol=simbolo,
                marker_color=color,
                marker_size=tam,
                marker_line_width=3 if "open" in simbolo else 2,
                marker_line_color=TEXTO if "open" in simbolo else PLOT_COLOR,
                name=nombre,
            )
        )

    # Columna de resultado: costo unitario de la mano de obra.
    for _, r in df.iterrows():
        flecha = "▲" if r["COSTO_UNITARIO"] > 0 else "▼"
        lectura = "margen bajo presión" if r["COSTO_UNITARIO"] > 0 else "gana eficiencia"
        fig.add_annotation(
            x=1.01,
            xref="paper",
            y=r["SECTOR"],
            text=f"<b>{flecha} {r['COSTO_UNITARIO']:+.1f}%</b>  {lectura}",
            showarrow=False,
            xanchor="left",
            font_size=22,
        )

    fig.add_annotation(
        x=1.01,
        xref="paper",
        y=1.0,
        yref="paper",
        text="<b>Costo unitario de<br>la mano de obra</b>",
        showarrow=False,
        xanchor="left",
        yanchor="bottom",
        align="left",
        font_size=22,
        font_color=TEXTO_SECUNDARIO,
    )

    caja_datos(
        fig,
        "<b>Toda la economía (2T-2026)</b>"
        "<br>Producción (IGAE jul): <b>107.8</b> pts (2018 = 100)"
        "<br>Productividad por hora: <b>97.4</b> pts (2018 = 100)"
        "<br>Producimos 7.8% más que en 2018,"
        "<br>pero cada hora rinde 2.6% menos.",
        x=0.99,
        y=0.97,
        xanchor="right",
        yanchor="top",
    )

    fig.add_vline(x=0, line_color=CERO, line_width=2)

    ejes(fig, ticksuffix="  ", showgrid=False)
    fig.update_xaxes(range=[-4, 15], ticksuffix="%", dtick=2)

    fig.update_layout(
        margin_l=40,
        margin_r=420,
        legend_orientation="h",
        legend_x=0.0,
        legend_xanchor="left",
        legend_y=1.015,
        legend_yanchor="bottom",
    )

    estilo_base(
        fig,
        "Ventas, productividad laboral y remuneración por sector",
        "Variación % anual real, segundo trimestre de 2026 vs. 2025 (cifras originales). Productividad por persona ocupada; en manufactura, por hora trabajada",
        "INEGI, IPL-CUMO e IGAE",
        "Variación % anual",
    )

    # Espacio extra: arriba para la leyenda y a la derecha para la columna de costo unitario.
    fig.update_layout(margin_t=200, margin_r=440)

    if guardar:
        finalizar(fig)
        fig.write_image(f"{CARPETA_IMGS}/4_productividad_vs_costos.png")
    return fig


if __name__ == "__main__":
    import os
    import sys

    # Uso: python graficas_igae.py [oscuro|claro]
    # El tema oscuro es el predeterminado; también puede generarse el tema claro.
    tema = sys.argv[1] if len(sys.argv) > 1 else "oscuro"
    usar_tema("oscuro_python" if tema == "oscuro" else tema)
    os.makedirs(CARPETA_IMGS, exist_ok=True)

    plot_pulso_mensual()
    plot_peso_sectores()
    plot_crecimiento_sectores()
    plot_productividad_costos()
