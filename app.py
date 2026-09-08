import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Pendientes Trolebús - SITRAMYTEM", layout="wide", page_icon="🚎")

COLOR_PRIMARY = "#1B2644"
COLOR_ACCENT  = "#8DCADB"
COLOR_YELLOW  = "#ECD635"

st.markdown(f"""
<style>
    /* Fondo general y color de fuente base */
    .stApp {{
        background-color: #f4f6f9;
        color: {COLOR_PRIMARY} !important;
    }}

    /* Todo el texto del cuerpo principal */
    .stApp p, .stApp span, .stApp div, .stApp label,
    .stApp li, .stApp td, .stApp th {{
        color: {COLOR_PRIMARY} !important;
    }}

    /* Títulos */
    h1, h2, h3, h4, h5, h6 {{
        color: {COLOR_PRIMARY} !important;
        letter-spacing: -0.3px;
    }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        background-color: {COLOR_PRIMARY};
    }}
    [data-testid="stSidebar"] * {{
        color: white !important;
    }}
    [data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {{
        background-color: {COLOR_ACCENT} !important;
    }}

    /* Métricas */
    [data-testid="metric-container"] {{
        background: white;
        border-left: 5px solid {COLOR_PRIMARY};
        border-radius: 6px;
        padding: 16px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.07);
    }}
    [data-testid="stMetricLabel"] {{ color: {COLOR_PRIMARY} !important; font-weight: 600; }}
    [data-testid="stMetricValue"] {{ color: {COLOR_PRIMARY} !important; }}

    /* Caption */
    [data-testid="stCaptionContainer"] p {{
        color: #444 !important;
    }}

    /* Divisor */
    hr {{ border-color: {COLOR_ACCENT}; opacity: 0.4; }}
</style>
""", unsafe_allow_html=True)

CORTE = "8 de septiembre de 2026"
CONTRAPARTE = "SITRAMYTEM"

DATA = [
    ("Contrato 1", "LP-SITRAMYTEM-DPPC-PAD-02-2023", "José Antonio (CUPISA)/ INDIMA", "Planos as-built", "Documentación", "En curso",
     "Actualizar los planos con las correcciones emitidas por INDIMA; falta la firma de Supervisión y definir la fecha de entrega."),
    ("Contrato 1", "LP-SITRAMYTEM-DPPC-PAD-02-2023", "José Antonio (CUPISA)", "Dossier de Calidad", "Documentación", "En curso",
     "Cupisa esta actualizando información, Supervisión tiene la gran mayoría. Entrega programada para el día 21 de septiembre."),
    ("Contrato 1", "LP-SITRAMYTEM-DPPC-PAD-02-2023", "CUPISA", "Bitácora de obra", "Documentación", "Pendiente",
     "Continuar el registro, detenido desde 2024. IMPORTANTE: pendiente la firma del Ing. Mauricio y de Supervisión."),
    ("Contrato 1", "LP-SITRAMYTEM-DPPC-PAD-02-2023", "SITRAMYTEM/MGMG", "Documentos de Terminación Anticipada", "Administrativo", "En curso",
     "Elaborar la documentación para dar paso al cierre correspondiente."),
    ("Contrato 1", "LP-SITRAMYTEM-DPPC-PAD-02-2023", "SITRAMYTEM/MGMG", "Revisión del Expediente Único de Obra", "Administrativo", "En curso",
     "Revisar qué cuestiones administrativas siguen abiertas."),
    ("Contrato 1", "LP-SITRAMYTEM-DPPC-PAD-02-2023", "SITRAMYTEM", "Retroalimentación de GNR", "Coordinación", "Pendiente",
     "Está en espera de respuesta por parte de SITRAMYTEM; se presentó hace menos de un mes."),
    ("Contrato 1", "LP-SITRAMYTEM-DPPC-PAD-02-2023", "CUPISA", "Displays", "Coordinación", "Pendiente",
     "Coordinar con el proveedor, por parte de CUPISA, la instalación en las subestaciones."),
    ("Contrato 1", "LP-SITRAMYTEM-DPPC-PAD-02-2023", "CUPISA", "Estimación Finiquito", "Documentación", "Pendiente", ""),
    ("Contrato 2", "LP-SITRAMYTEM-DPPC-PAD-06-2024", "José Antonio (CUPISA)", "Planos as-built", "Documentación", "En curso",
     "Actualizar los planos con el estado real de la obra; falta la firma de Supervisión y definir la fecha de entrega."),
    ("Contrato 2", "LP-SITRAMYTEM-DPPC-PAD-06-2024", "José Antonio (CUPISA)", "Dossier de Calidad", "Documentación", "Pendiente", ""),
    ("Contrato 2", "LP-SITRAMYTEM-DPPC-PAD-06-2024", "MGMG/CUPISA", "Bitácora de obra", "Documentación", "Pendiente",
     "Iniciar el registro desde cero debido al extravío por parte de SITRAMYTEM. IMPORTANTE: pendiente la firma del Ing. Mauricio y de Supervisión."),
    ("Contrato 2", "LP-SITRAMYTEM-DPPC-PAD-06-2024", "SITRAMYTEM/MGMG", "Actas administrativas de cierre", "Administrativo", "Pendiente",
     "Integrar la documentación para el cierre del contrato."),
    ("Contrato 2", "LP-SITRAMYTEM-DPPC-PAD-06-2024", "SITRAMYTEM/MGMG", "Revisión del Expediente Único de Obra", "Administrativo", "Pendiente",
     "Revisar qué cuestiones administrativas siguen abiertas."),
    ("Contrato 2", "LP-SITRAMYTEM-DPPC-PAD-06-2024", "SITRAMYTEM", "Retroalimentación de GNR", "Coordinación", "Pendiente",
     "Está en espera de respuesta por parte de SITRAMYTEM; se presentó hace menos de un mes."),
    ("Contrato 2", "LP-SITRAMYTEM-DPPC-PAD-06-2024", "INDIMA/CUPISA", "Precios extraordinarios", "Financiero", "En curso",
     "Cotizaciones pendientes por parte de CUPISA; dictámenes en curso. Preparar y presentar para el reconocimiento de costos."),
    ("Contrato 2", "LP-SITRAMYTEM-DPPC-PAD-06-2024", "CUPISA", "Estimación Finiquito", "Documentación", "Pendiente", ""),
]

df = pd.DataFrame(
    DATA,
    columns=["Contrato", "Expediente", "Responsable", "Tema", "Categoría", "Estado", "Descripción"],
)

ESTADO_ORDER = ["En curso", "Pendiente"]
ESTADO_COLOR = {"En curso": COLOR_YELLOW, "Pendiente": COLOR_ACCENT}

st.sidebar.header("Filtros")
contratos_sel = st.sidebar.multiselect(
    "Contrato", sorted(df["Contrato"].unique()), default=sorted(df["Contrato"].unique())
)
estados_sel = st.sidebar.multiselect("Estado", ESTADO_ORDER, default=ESTADO_ORDER)
categorias_sel = st.sidebar.multiselect(
    "Categoría", sorted(df["Categoría"].unique()), default=sorted(df["Categoría"].unique())
)

df_f = df[
    df["Contrato"].isin(contratos_sel)
    & df["Estado"].isin(estados_sel)
    & df["Categoría"].isin(categorias_sel)
]

st.title("🚎 Pendientes Contratos Trolebús")
st.caption(f"Corte: {CORTE}  ·  Contraparte: {CONTRAPARTE}")

st.markdown(f"""
<div style="display:flex; gap:16px; margin: 8px 0 4px 0;">
    <div style="background:white; border-left:5px solid {COLOR_PRIMARY}; border-radius:6px;
                padding:10px 18px; box-shadow:0 2px 6px rgba(0,0,0,0.07); flex:1;">
        <span style="color:{COLOR_ACCENT}; font-weight:700; font-size:0.85rem;">CONTRATO 1</span><br>
        <span style="color:{COLOR_PRIMARY}; font-weight:600; font-size:0.9rem;">LP-SITRAMYTEM-DPPC-PAD-02-2023</span>
    </div>
    <div style="background:white; border-left:5px solid {COLOR_ACCENT}; border-radius:6px;
                padding:10px 18px; box-shadow:0 2px 6px rgba(0,0,0,0.07); flex:1;">
        <span style="color:{COLOR_PRIMARY}; font-weight:700; font-size:0.85rem;">CONTRATO 2</span><br>
        <span style="color:{COLOR_PRIMARY}; font-weight:600; font-size:0.9rem;">LP-SITRAMYTEM-DPPC-PAD-06-2024</span>
    </div>
</div>
""", unsafe_allow_html=True)
st.divider()

total     = len(df_f)
en_curso  = int((df_f["Estado"] == "En curso").sum())
pendientes = int((df_f["Estado"] == "Pendiente").sum())

col1, col2, col3 = st.columns(3)
col1.metric("📋 Total de temas", total)
col2.metric("🟡 En curso", en_curso)
col3.metric("🔵 Pendientes", pendientes)

st.divider()

left, right = st.columns([1, 1.4])

with left:
    st.subheader("Avance general")
    pct_en_curso = (en_curso / total * 100) if total else 0
    fig_gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=pct_en_curso,
            number={"suffix": "%", "font": {"color": COLOR_PRIMARY}},
            title={"text": "% de temas en curso", "font": {"color": COLOR_PRIMARY}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": COLOR_PRIMARY},
                "bar": {"color": COLOR_PRIMARY},
                "bgcolor": "white",
                "steps": [
                    {"range": [0, 33],  "color": "#e8edf5"},
                    {"range": [33, 66], "color": COLOR_ACCENT},
                    {"range": [66, 100],"color": COLOR_YELLOW},
                ],
                "threshold": {
                    "line": {"color": COLOR_PRIMARY, "width": 4},
                    "thickness": 0.8,
                    "value": pct_en_curso,
                },
            },
        )
    )
    fig_gauge.update_layout(
        height=320,
        margin=dict(l=20, r=20, t=60, b=10),
        paper_bgcolor="white",
        plot_bgcolor="white",
    )
    st.plotly_chart(fig_gauge, use_container_width=True)

with right:
    st.subheader("Temas por categoría y estado")
    conteo = df_f.groupby(["Categoría", "Estado"]).size().reset_index(name="Cantidad")
    fig_bar = go.Figure()
    for estado in ESTADO_ORDER:
        sub = conteo[conteo["Estado"] == estado]
        fig_bar.add_bar(
            x=sub["Categoría"],
            y=sub["Cantidad"],
            name=estado,
            marker_color=ESTADO_COLOR[estado],
            marker_line_color=COLOR_PRIMARY,
            marker_line_width=0.8,
        )
    fig_bar.update_layout(
        barmode="stack",
        height=320,
        margin=dict(l=20, r=20, t=20, b=10),
        legend_title="Estado",
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color=COLOR_PRIMARY),
        xaxis=dict(gridcolor="#e8edf5"),
        yaxis=dict(gridcolor="#e8edf5"),
    )
    st.plotly_chart(fig_bar, use_container_width=True)

st.divider()
st.subheader("Comparativo por contrato")

comp = df_f.groupby(["Contrato", "Estado"]).size().reset_index(name="Cantidad")
fig_comp = go.Figure()
for estado in ESTADO_ORDER:
    sub = comp[comp["Estado"] == estado]
    fig_comp.add_bar(
        x=sub["Contrato"],
        y=sub["Cantidad"],
        name=estado,
        marker_color=ESTADO_COLOR[estado],
        marker_line_color=COLOR_PRIMARY,
        marker_line_width=0.8,
    )
fig_comp.update_layout(
    barmode="stack",
    height=280,
    margin=dict(l=20, r=20, t=20, b=10),
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(color=COLOR_PRIMARY),
    xaxis=dict(gridcolor="#e8edf5"),
    yaxis=dict(gridcolor="#e8edf5"),
)
st.plotly_chart(fig_comp, use_container_width=True)

st.divider()
st.subheader("Avance por responsable")

resp = df_f.groupby(["Responsable", "Estado"]).size().reset_index(name="Cantidad")
fig_resp = go.Figure()
for estado in ESTADO_ORDER:
    sub = resp[resp["Estado"] == estado]
    fig_resp.add_bar(
        y=sub["Responsable"],
        x=sub["Cantidad"],
        name=estado,
        orientation="h",
        marker_color=ESTADO_COLOR[estado],
        marker_line_color=COLOR_PRIMARY,
        marker_line_width=0.8,
    )
fig_resp.update_layout(
    barmode="stack",
    height=max(280, len(df_f["Responsable"].unique()) * 50),
    margin=dict(l=20, r=20, t=20, b=10),
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(color=COLOR_PRIMARY),
    xaxis=dict(gridcolor="#e8edf5", title="Cantidad de temas"),
    yaxis=dict(gridcolor="#e8edf5", automargin=True),
    legend_title="Estado",
)
st.plotly_chart(fig_resp, use_container_width=True)

st.divider()
st.subheader("Seguimiento por Gantt")
st.markdown(f"""
<div style="background:white; border:2px dashed {COLOR_ACCENT}; border-radius:10px;
            padding:32px; text-align:center; box-shadow:0 2px 8px rgba(0,0,0,0.06);">
    <div style="font-size:2.2rem; margin-bottom:12px;">📅</div>
    <p style="color:{COLOR_PRIMARY}; font-size:1.1rem; font-weight:700; margin:0 0 8px 0;">
        Diagrama de Gantt no disponible
    </p>
    <p style="color:#555; font-size:0.95rem; margin:0 0 20px 0; max-width:500px; margin-left:auto; margin-right:auto;">
        Para activar el seguimiento por Gantt se requiere definir, por cada tema,
        una <strong>fecha de inicio</strong> y una <strong>fecha límite de resolución</strong>.
        Estas fechas aún no están registradas — se recomienda definirlas a la brevedad
        como parte del control de avance.
    </p>
    <div style="display:inline-block; background:{COLOR_PRIMARY}; color:white;
                padding:8px 24px; border-radius:6px; font-weight:600; font-size:0.9rem;">
        ⚠️ Acción requerida: solicitar fechas a los responsables
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()
st.subheader("Detalle de temas")

COLS = ["Contrato", "Expediente", "Responsable", "Tema", "Categoría", "Estado", "Descripción"]

header_cells = "".join(
    f'<th style="padding:10px 14px; text-align:left; font-weight:600; white-space:nowrap;">{c}</th>'
    for c in COLS
)

rows_html = ""
for i, (_, row) in enumerate(df_f[COLS].iterrows()):
    bg = "white" if i % 2 == 0 else "#f4f6f9"
    cells = ""
    for col in COLS:
        val = str(row[col]) if row[col] else ""
        if col == "Estado":
            color = ESTADO_COLOR.get(val, "#ccc")
            text_color = COLOR_PRIMARY if val == "En curso" else "white"
            cells += (
                f'<td style="padding:10px 14px; white-space:nowrap;">'
                f'<span style="background:{color}; color:{text_color}; padding:3px 10px; '
                f'border-radius:4px; font-weight:600;">{val}</span></td>'
            )
        elif col == "Descripción":
            cells += (
                f'<td style="padding:10px 14px; min-width:280px; '
                f'word-wrap:break-word; white-space:normal;">{val}</td>'
            )
        else:
            cells += f'<td style="padding:10px 14px; white-space:nowrap;">{val}</td>'
    rows_html += f'<tr style="background:{bg}; border-bottom:1px solid #e8edf5;">{cells}</tr>'

st.markdown(f"""
<div style="overflow-x:auto; border-radius:8px; box-shadow:0 2px 8px rgba(0,0,0,0.08);">
<table style="width:100%; border-collapse:collapse; font-size:0.88rem; color:{COLOR_PRIMARY};">
    <thead>
        <tr style="background:{COLOR_PRIMARY}; color:white;">
            {header_cells}
        </tr>
    </thead>
    <tbody>
        {rows_html}
    </tbody>
</table>
</div>
""", unsafe_allow_html=True)
