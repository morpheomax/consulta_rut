import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import st_folium
import time
import pickle
import os
st.set_page_config(
    page_title="Buscador de Categoría por RUT",
    page_icon="🧾",
    layout="wide"
)

# Estilos CSS para UI moderna
st.markdown("""
<style>
    .main-header {
        font-size: 2.5em;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 20px;
    }
    .sub-header {
        font-size: 1.5em;
        color: #A23B72;
        margin-top: 20px;
    }
    .info-box {
        background-color: #F0F8FF;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #2E86AB;
        margin-bottom: 10px;
    }
    .category-highlight {
        background-color: #FFFACD;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #FFD700;
        text-align: center;
        font-size: 1.2em;
        font-weight: bold;
        color: #8B4513;
        margin-bottom: 20px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 12px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 12px;
        transition: background-color 0.3s;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 2px solid #ddd;
        padding: 10px;
    }
    .stTextArea>div>textarea {
        border-radius: 8px;
        border: 2px solid #ddd;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Título visible dentro de la app
st.markdown('<h1 class="main-header">Buscador de Categoría por RUT</h1>', unsafe_allow_html=True)

# Carga del archivo Excel en un DataFrame con optimización de cache usando Parquet
@st.cache_data
def load_data():
    parquet_file = "ABC.parquet"
    if os.path.exists(parquet_file):
        try:
            df = pd.read_parquet(parquet_file)
            return df
        except:
            pass  # Si falla, cargar desde Excel

    try:
        # Leer las columnas disponibles en el Excel
        df_sample = pd.read_excel("ABC.xlsx", nrows=0)
        available_cols = df_sample.columns.tolist()
        
        # Columnas deseadas
        desired_cols = ["Rut_empresa", "Dv_empresa", "Razon_social", "Tramo_ventas", "Annio_comercial",
                        "Rubro_economico", "Subrubro_economico", "Actividad_economica", "Region", "Provincia", "Comuna", "CAT"]
        
        # Filtrar columnas disponibles
        usecols = [col for col in desired_cols if col in available_cols]
        
        if not usecols:
            st.error("❌ No se encontraron las columnas necesarias en ABC.xlsx.")
            return pd.DataFrame()
        
        # Mostrar warning si faltan columnas
        missing_cols = [col for col in desired_cols if col not in available_cols]
        if missing_cols:
            st.warning(f"⚠️ Columnas faltantes en ABC.xlsx: {', '.join(missing_cols)}. La app funcionará con las disponibles.")
        
        df = pd.read_excel("ABC.xlsx", usecols=usecols, dtype=str)
        
        # Verificar que Rut_empresa esté presente para el índice
        if "Rut_empresa" not in df.columns:
            st.error("❌ La columna 'Rut_empresa' es obligatoria y no se encontró en ABC.xlsx.")
            return pd.DataFrame()
        
        # Crear índice para búsquedas más rápidas
        df.set_index("Rut_empresa", inplace=True)
        # Guardar como Parquet para futuras cargas rápidas y eficientes
        df.to_parquet(parquet_file, index=True)
        return df
    except Exception as e:
        st.error(f"❌ Error al cargar el archivo ABC.xlsx: {e}. Asegúrate de que el archivo no esté abierto en otra aplicación.")
        return pd.DataFrame()  # Retornar DataFrame vacío para evitar crashes

df = load_data()

if df.empty:
    st.error("❌ No se pudo cargar el archivo de datos ABC.xlsx. Asegúrate de que el archivo exista y no esté abierto en otra aplicación.")
    st.stop()

# Función para geocodificar
@st.cache_data
def get_coordinates(provincia, comuna):
    geolocator = Nominatim(user_agent="consulta_rut_app")
    address = f"{comuna}, {provincia}, Chile"
    try:
        location = geolocator.geocode(address, timeout=5)  # Reducir timeout a 5 segundos
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except:
        return None, None

# Crear tabs
tab1, tab2 = st.tabs(["🔍 Búsqueda Individual", "📊 Búsqueda Masiva"])

with tab1:
    st.markdown('<h2 class="sub-header">Búsqueda por RUT Individual</h2>', unsafe_allow_html=True)
    # Ingreso de RUT
    rut_input = st.text_input("Ingresa el RUT sin guion ni dígito verificador:", max_chars=8, help="Ejemplo: 12345678")

    # Búsqueda
    if rut_input:
        if rut_input in df.index:
            row = df.loc[rut_input]
            st.success("✅ RUT encontrado")

            # Destacar Categoría primero (si existe)
            if 'CAT' in row.index:
                st.markdown(f'<div class="category-highlight">🏷️ Categoría: {row["CAT"]}</div>', unsafe_allow_html=True)
            else:
                st.warning("⚠️ Categoría no disponible")

            # Usar columnas para organizar la info
            col1, col2 = st.columns([1, 1])

            with col1:
                st.markdown('<div class="info-box">', unsafe_allow_html=True)
                if 'Dv_empresa' in row.index:
                    st.write(f"**RUT Empresa:** {row.name}-{row['Dv_empresa']}")
                if 'Razon_social' in row.index:
                    st.write(f"**Razón Social:** {row['Razon_social']}")
                if 'Tramo_ventas' in row.index:
                    st.write(f"**Tramo Ventas:** {row['Tramo_ventas']}")
                if 'Annio_comercial' in row.index:
                    st.write(f"**Año Comercial:** {row['Annio_comercial']}")
                if 'Rubro_economico' in row.index:
                    st.write(f"**Rubro Económico:** {row['Rubro_economico']}")
                if 'Subrubro_economico' in row.index:
                    st.write(f"**Subrubro Económico:** {row['Subrubro_economico']}")
                if 'Actividad_economica' in row.index:
                    st.write(f"**Actividad Económica:** {row['Actividad_economica']}")
                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                st.markdown('<div class="info-box">', unsafe_allow_html=True)
                if 'Region' in row.index:
                    st.write(f"**Región:** {row['Region']}")
                if 'Provincia' in row.index:
                    st.write(f"**Provincia:** {row['Provincia']}")
                if 'Comuna' in row.index:
                    st.write(f"**Comuna:** {row['Comuna']}")
                st.markdown('</div>', unsafe_allow_html=True)

                # Mapa (solo si hay Provincia y Comuna)
                if 'Provincia' in row.index and 'Comuna' in row.index:
                    with st.spinner("📍 Obteniendo ubicación en el mapa..."):
                        lat, lon = get_coordinates(row['Provincia'], row['Comuna'])
                    if lat and lon:
                        st.subheader("📍 Ubicación en Mapa")
                        m = folium.Map(location=[lat, lon], zoom_start=12)
                        popup_text = f"{row['Razon_social'] if 'Razon_social' in row.index else 'Empresa'} - {row['Comuna']}, {row['Provincia']}"
                        folium.Marker([lat, lon], popup=popup_text).add_to(m)
                        st_folium(m, width=700, height=400)
                    else:
                        st.warning("⚠️ No se pudo geocodificar la ubicación para mostrar el mapa. Verifica la dirección.")
        else:
            st.error("❌ RUT no encontrado. Verifica el número ingresado.")

with tab2:
    st.markdown('<h2 class="sub-header">Búsqueda Masiva de RUTs</h2>', unsafe_allow_html=True)
    ruts_input = st.text_area("Ingresa una lista de RUTs separados por comas o saltos de línea (sin guion ni dígito verificador):", height=150, help="Ejemplo:\n12345678\n87654321\n11223344")

    if st.button("🔍 Buscar RUTs"):
        if ruts_input:
            # Procesar la lista de RUTs
            ruts_list = [rut.strip() for rut in ruts_input.replace(',', '\n').split('\n') if rut.strip()]
            # Filtrar RUTs válidos
            valid_ruts = [rut for rut in ruts_list if rut in df.index]
            if valid_ruts:
                resultados = df.loc[valid_ruts].reset_index()
                st.success(f"✅ Encontrados {len(resultados)} RUTs de {len(ruts_list)} buscados")
                # Mostrar tabla con scrollbar si es necesario
                st.dataframe(resultados, width='stretch')
                # Resumen
                st.markdown("### 📈 Resumen")
                st.write(f"**Total RUTs encontrados:** {len(resultados)}")
                if 'CAT' in resultados.columns:
                    st.write(f"**Categorías encontradas:** {', '.join(resultados['CAT'].unique())}")
                else:
                    st.write("**Categorías:** No disponible")
            else:
                st.error("❌ Ningún RUT encontrado. Verifica los números ingresados.")
        else:
            st.warning("⚠️ Por favor, ingresa al menos un RUT.")



