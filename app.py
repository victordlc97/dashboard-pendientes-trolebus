import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Pendientes Trolebús - SITRAMYTEM", layout="wide", page_icon="🚎")

COLOR_PRIMARY = "#1B2644"
COLOR_ACCENT  = "#8DCADB"
COLOR_YELLOW  = "#ECD635"

st.markdown(f"""
<style>
    /* Fondo general */
    .stApp {{ background-color: #f4f6f9; }}

    /* Título principal */
    h1 {{ color: {COLOR_PRIMARY} !important; letter-spacing: -0.5px; }}

    /* Subtítulos */
    h2, h3 {{ color: {COLOR_PRIMARY} !important; }}

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

    /* Divisor */
    hr {{ border-color: {COLOR_ACCENT}; opacity: 0.4; }}

    /* Caption */
    .stCaption {{ color: #555 !important; }}
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
st.subheader("Detalle de temas")


def estado_badge(estado: str) -> str:
    color = ESTADO_COLOR.get(estado, "#ccc")
    text_color = COLOR_PRIMARY if estado == "En curso" else "white"
    return f"background-color: {color}; color: {text_color}; font-weight: 600;"


styled = df_f.drop(columns=["Expediente"]).style.map(
    lambda v: estado_badge(v) if v in ESTADO_COLOR else "", subset=["Estado"]
)
st.dataframe(styled, use_container_width=True, hide_index=True)
