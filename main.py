import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(layout="wide", page_title="Dashboard Formación Autociel")

# --- CONEXIÓN A LOS DATOS ---
SHEET_ID = "11yH6PUYMpt-m65hFH9t2tWSEgdRpLOCFR3OFjJtWToQ"
# GID de la hoja "NOMINA REAL DE AUTOCIEL"
URL_NOMINA = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=870107738"

@st.cache_data
def load_data():
    # Cargamos la nómina real
    df = pd.read_csv(URL_NOMINA)
    return df

try:
    df_raw = load_data()

    # --- BARRA LATERAL (FILTROS) ---
    st.sidebar.header("Filtros de Búsqueda")
    
    # Filtro de Áreas (basado en la columna 'Area' de tu sheet)
    list_areas = df_raw['Area'].unique().tolist() if 'Area' in df_raw.columns else []
    selected_areas = st.sidebar.multiselect("Filtrar por Áreas:", list_areas)

    # Filtro de Cargos
    list_cargos = df_raw['Cargo'].unique().tolist() if 'Cargo' in df_raw.columns else []
    selected_cargos = st.sidebar.multiselect("Filtrar por Figura/Cargo:", list_cargos)

    # Buscador por nombre
    search_user = st.sidebar.text_input("Buscar Colaborador por nombre:")

    # Aplicar Filtros
    df_filt = df_raw.copy()
    if selected_areas:
        df_filt = df_filt[df_filt['Area'].isin(selected_areas)]
    if selected_cargos:
        df_filt = df_filt[df_filt['Cargo'].isin(selected_cargos)]
    if search_user:
        df_filt = df_filt[df_filt['Nombre'].str.contains(search_user, case=False, na=False)]

    # --- DISEÑO DEL DASHBOARD ---
    st.title("📊 Indicadores de Formación - Autociel")

    # Fila 1: Métricas Principales
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Avance Posventa", "72%", help="Porcentaje de cumplimiento área Posventa")
    with col2:
        st.metric("Avance Ventas", "73%", help="Porcentaje de cumplimiento área Ventas")
    with col3:
        st.metric("Colaboradores", len(df_filt))
    with col4:
        st.metric("Pendientes", "23")

    st.divider()

    # Fila 2: Tabla de Datos
    st.subheader("📋 Detalle de Cursos y Seguimiento")
    st.dataframe(df_filt, use_container_width=True)

except Exception as e:
    st.error(f"Error al cargar los datos: {e}")
    st.info("Asegúrate de que el Google Sheet esté compartido como 'Cualquier persona con el enlace puede leer'.")
