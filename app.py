import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Pendientes Trolebús - SITRAMYTEM", layout="wide", page_icon="🚎")

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

ESTADO_ORDER = ["Urgente", "En curso", "Pendiente"]
ESTADO_COLOR = {"Urgente": "#e63946", "En curso": "#f4a300", "Pendiente": "#adb5bd"}

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

total = len(df_f)
urgentes = int((df_f["Estado"] == "Urgente").sum())
en_curso = int((df_f["Estado"] == "En curso").sum())

col1, col2, col3 = st.columns(3)
col1.metric("📋 Pendientes totales", total)
col2.metric("🔴 Urgentes", urgentes)
col3.metric("🟡 En curso", en_curso)

st.divider()

left, right = st.columns([1, 1.4])

with left:
    st.subheader("Semáforo de urgencia")
    pct_urgente = (urgentes / total * 100) if total else 0
    fig_gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=pct_urgente,
            number={"suffix": "%"},
            title={"text": "% de pendientes urgentes"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#1d3557"},
                "steps": [
                    {"range": [0, 20], "color": "#2a9d8f"},
                    {"range": [20, 50], "color": "#f4a300"},
                    {"range": [50, 100], "color": "#e63946"},
                ],
                "threshold": {
                    "line": {"color": "black", "width": 4},
                    "thickness": 0.8,
                    "value": pct_urgente,
                },
            },
        )
    )
    fig_gauge.update_layout(height=320, margin=dict(l=20, r=20, t=60, b=10))
    st.plotly_chart(fig_gauge, use_container_width=True)

with right:
    st.subheader("Pendientes por categoría y estado")
    conteo = (
        df_f.groupby(["Categoría", "Estado"]).size().reset_index(name="Cantidad")
    )
    fig_bar = go.Figure()
    for estado in ESTADO_ORDER:
        sub = conteo[conteo["Estado"] == estado]
        fig_bar.add_bar(
            x=sub["Categoría"], y=sub["Cantidad"], name=estado, marker_color=ESTADO_COLOR[estado]
        )
    fig_bar.update_layout(
        barmode="stack", height=320, margin=dict(l=20, r=20, t=20, b=10), legend_title="Estado"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

st.divider()
st.subheader("Comparativo por contrato")

comp = df_f.groupby(["Contrato", "Estado"]).size().reset_index(name="Cantidad")
fig_comp = go.Figure()
for estado in ESTADO_ORDER:
    sub = comp[comp["Estado"] == estado]
    fig_comp.add_bar(
        x=sub["Contrato"], y=sub["Cantidad"], name=estado, marker_color=ESTADO_COLOR[estado]
    )
fig_comp.update_layout(barmode="stack", height=280, margin=dict(l=20, r=20, t=20, b=10))
st.plotly_chart(fig_comp, use_container_width=True)

st.divider()
st.subheader("Detalle de pendientes")


def estado_badge(estado: str) -> str:
    color = ESTADO_COLOR[estado]
    return f"background-color: {color}; color: white; font-weight: 600;"


styled = df_f.drop(columns=["Expediente"]).style.map(
    lambda v: estado_badge(v) if v in ESTADO_COLOR else "", subset=["Estado"]
)
st.dataframe(styled, use_container_width=True, hide_index=True)
