import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Panel de Precios de Renta — Guadalajara", layout="wide")
st.header("📊 Precios de Renta de Viviendas en Guadalajara")

# ---- Diccionario de traducciones ----
COLUMN_TRANSLATIONS = {
    "no": "índice",
    "location": "ubicación",
    "price": "precio",
    "bedrooms": "recámaras",
    "bathrooms": "baños",
    "garage": "cocheras",
    "area": "superficie (m²)",
}

# Inverso para mapear de español -> inglés
INV_TRANSLATIONS = {v: k for k, v in COLUMN_TRANSLATIONS.items()}

# ---- Carga de datos ----


@st.cache_data
def load_data_from_csv(path: str, encoding: str = "utf-8") -> pd.DataFrame:
    return pd.read_csv(path, encoding=encoding)


st.sidebar.header("Datos")
uploaded = st.sidebar.file_uploader("Subir archivo CSV", type=[
    "csv"], help="Opcional: sube un CSV propio.")

df = None
error_msg = None
try:
    if uploaded is not None:
        df = pd.read_csv(uploaded, encoding="utf-8")
        st.sidebar.success("CSV cargado desde el uploader.")
    else:
        st.sidebar.info(
            "Usando gdl_rental_prices.csv en la carpeta raíz del proyecto.")
        df = load_data_from_csv("gdl_rental_prices.csv")
except Exception as e:
    error_msg = f"Error al cargar el CSV: {e}"

if error_msg:
    st.error(error_msg)
    st.stop()

if df is None or df.empty:
    st.warning("No se pudo cargar el DataFrame o está vacío.")
    st.stop()

st.write("### Vista previa de los datos")
# Mostrar con columnas traducidas
df_display = df.rename(columns=COLUMN_TRANSLATIONS)
st.dataframe(df_display.head(), use_container_width=True)

# ---- Columnas ----
numeric_cols = df.select_dtypes(include="number").columns.tolist()
cat_cols = df.select_dtypes(exclude="number").columns.tolist()

numeric_cols_es = [COLUMN_TRANSLATIONS.get(c, c) for c in numeric_cols]
cat_cols_es = [COLUMN_TRANSLATIONS.get(c, c) for c in cat_cols]

with st.expander("Ver columnas detectadas"):
    st.write("**Numéricas:**", numeric_cols_es)
    st.write("**Categóricas:**", cat_cols_es)

# ---- Controles ----
st.sidebar.header("Controles de gráficos")

default_hist = "price" if "price" in numeric_cols else (
    numeric_cols[0] if numeric_cols else None)
default_x = "area" if "area" in numeric_cols else (
    numeric_cols[0] if numeric_cols else None)
default_y = "price" if "price" in numeric_cols else (
    numeric_cols[1] if len(numeric_cols) > 1 else None)

hist_col_es = st.sidebar.selectbox("Columna para histograma", options=numeric_cols_es, index=numeric_cols.index(
    default_hist) if default_hist in numeric_cols else 0)
x_col_es = st.sidebar.selectbox("Eje X (dispersión)", options=numeric_cols_es,
                                index=numeric_cols.index(default_x) if default_x in numeric_cols else 0)
y_col_es = st.sidebar.selectbox("Eje Y (dispersión)", options=numeric_cols_es, index=numeric_cols.index(
    default_y) if default_y in numeric_cols else (1 if len(numeric_cols) > 1 else 0))

# Mapear de español a inglés
hist_col = INV_TRANSLATIONS[hist_col_es]
x_col = INV_TRANSLATIONS[x_col_es]
y_col = INV_TRANSLATIONS[y_col_es]

mostrar_desc = st.sidebar.checkbox(
    "Mostrar estadísticas descriptivas", value=False)
if mostrar_desc:
    st.write("### Estadísticas descriptivas")
    st.dataframe(df.describe(), use_container_width=True)

# ---- Gráficos ----
st.subheader("Gráficos con **botones**")
col1, col2 = st.columns(2)

with col1:
    if st.button("Generar histograma"):
        fig_hist = px.histogram(df, x=hist_col, nbins=30,
                                title=f"Histograma de {hist_col_es}")
        st.plotly_chart(fig_hist, use_container_width=True)

with col2:
    if st.button("Generar gráfico de dispersión"):
        if x_col == y_col:
            st.warning("Elige columnas diferentes para X e Y.")
        else:
            fig_scatter = px.scatter(
                df, x=x_col, y=y_col, title=f"Dispersión: {x_col_es} vs {y_col_es}")
            st.plotly_chart(fig_scatter, use_container_width=True)

# ---- Extra con checkboxes ----
st.subheader("Extra: Gráficos con **casillas de verificación**")
chk_hist = st.checkbox("Mostrar histograma (casilla)")
chk_scatter = st.checkbox("Mostrar dispersión (casilla)")

if chk_hist:
    fig_hist2 = px.histogram(df, x=hist_col, nbins=30,
                             title=f"[Checkbox] Histograma de {hist_col_es}")
    st.plotly_chart(fig_hist2, use_container_width=True)

if chk_scatter:
    if x_col == y_col:
        st.info("Elige columnas distintas para X e Y.")
    else:
        fig_scatter2 = px.scatter(
            df, x=x_col, y=y_col, title=f"[Checkbox] Dispersión: {x_col_es} vs {y_col_es}")
        st.plotly_chart(fig_scatter2, use_container_width=True)

st.sidebar.markdown("---")
if st.sidebar.button("Refrescar aplicación"):
    st.experimental_rerun()
