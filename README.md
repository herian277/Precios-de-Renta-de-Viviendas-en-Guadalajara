# 📊 Panel de Precios de Renta en Guadalajara

Aplicación web desarrollada con **Streamlit**, **pandas** y **plotly** para explorar precios de renta de viviendas en la Zona Metropolitana de Guadalajara (dataset `gdl_rental_prices.csv`).
link a RENDER: https://precios-de-renta-de-viviendas-en.onrender.com

## Funcionalidades principales

- Encabezado y vista previa interactiva de los datos.
- Carga de datos:
  - Automática desde `gdl_rental_prices.csv`.
  - Opción de subir un archivo CSV propio desde la barra lateral.
- Controles para elegir columnas numéricas y graficar:
  - **Histograma** de frecuencias.
  - **Gráfico de dispersión** (relación entre dos variables).
- Visualización de **estadísticas descriptivas** opcionales.
- Interacción mediante **botones** o **casillas de verificación** (checkboxes).
- **Traducción completa de la interfaz y las columnas**:  
  - Ejemplo: `price` → `precio`, `bedrooms` → `recámaras`, `bathrooms` → `baños`, etc.  
  - Esto mejora la usabilidad para usuarios hispanohablantes.

## Estructura del proyecto

.
├── README.md
├── app.py
├── gdl_rental_prices.csv
├── requirements.txt
└── notebooks
└── EDA.ipynb

shell
Copiar código

## Requisitos

- Python 3.12+
- Entorno virtual recomendado

## Instalación

```bash
# Crear y activar entorno virtual (Windows PowerShell)
py -m venv .venv
.\.venv\Scripts\Activate.ps1

# Actualizar pip
python -m pip install --upgrade pip

# Instalar dependencias
pip install -r requirements.txt
