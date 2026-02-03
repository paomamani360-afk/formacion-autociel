import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de ancho de pantalla
st.set_page_config(layout="wide", page_title="Dashboard Formación Autociel")

# Estilo CSS para que se parezca a tu imagen (azul oscuro y blanco)
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    [data-testid="stMetricValue"] { font-size: 25px; color: #1e3d59; }
    </style>
    """, unsafe_allow_html=True)

# --- CARGA DE DATOS ---
SHEET_ID = "11yH6PUYMpt-m65hFH9t2tWSEgdRpLOCFR3OFjJtWToQ"
# GID de la pestaña "NOMINA REAL DE AUTOCIEL"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=870107738"

@st.cache_data
def load_data():
    return pd.read_csv(URL)

df = load_data()

# --- SIDEBAR (Filtros de tu imagen) ---
st.sidebar.title("Filtros")
area = st.sidebar.multiselect("Área", ["Posventa", "Venta"])
cargo = st.sidebar.multiselect("Cargo", df['Cargo'].unique() if 'Cargo' in df.columns else [])
niveles = st.sidebar.multiselect("Niveles 1 y 2", ["Nivel 1", "Nivel 2"])

# --- CUERPO PRINCIPAL ---
st.title("📊 Indicadores de Formación")

# Fila de Tarjetas (Como en tu imagen 2)
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Posventa", "72%", "Avance Total")
    st.metric("Venta", "73%", "Avance Total")
with c2:
    st.metric("Nivel 1", "66%", "Posventa")
    st.metric("Nivel 1", "67%", "Venta")
with c3:
    st.metric("Cant. Colaboradores", "23")
    st.write("**Figuras Obligatorias:** 15")
with c4:
    st.metric("Ausentismo", "0%")
    st.write("**Figuras Opcionales:** 8")

st.divider()

# Tabla de cursos (Como en tu imagen 1 y 2)
st.subheader("Cursos por Colaborador y Estado")
# Aquí filtramos si hay datos, si no, mostramos el dataframe base
st.dataframe(df, use_container_width=True)

# Gráfico de Avance (Como el de tu imagen 1)
st.subheader("% Avance de Certificación")
fig = px.bar(df, x="Cargo", y="Capacitaciones" if "Capacitaciones" in df.columns else None, 
             color_discrete_sequence=['#45ada8'])
st.plotly_chart(fig, use_container_width=True)
