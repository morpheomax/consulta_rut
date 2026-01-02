import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import st_folium
import time

# Cambiar título, ícono, y layout de la página
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

# Carga del archivo Excel en un DataFrame
def load_data():
    try:
        df = pd.read_excel("ABC.xlsx", dtype=str)
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
        location = geolocator.geocode(address, timeout=10)
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
        resultado = df[df["Rut_empresa"] == rut_input]
        if not resultado.empty:
            row = resultado.iloc[0]
            st.success("✅ RUT encontrado")

            # Destacar Categoría primero
            st.markdown(f'<div class="category-highlight">🏷️ Categoría: {row["CAT"]}</div>', unsafe_allow_html=True)

            # Usar columnas para organizar la info
            col1, col2 = st.columns([1, 1])

            with col1:
                st.markdown('<div class="info-box">', unsafe_allow_html=True)
                st.write(f"**RUT Empresa:** {row['Rut_empresa']}-{row['Dv_empresa']}")
                st.write(f"**Razón Social:** {row['Razon_social']}")
                st.write(f"**Tramo Ventas:** {row['Tramo_ventas']}")
                st.write(f"**Año Comercial:** {row['Annio_comercial']}")
                st.write(f"**Rubro Económico:** {row['Rubro_economico']}")
                st.write(f"**Subrubro Económico:** {row['Subrubro_economico']}")
                st.write(f"**Actividad Económica:** {row['Actividad_economica']}")
                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                st.markdown('<div class="info-box">', unsafe_allow_html=True)
                st.write(f"**Región:** {row['Region']}")
                st.write(f"**Provincia:** {row['Provincia']}")
                st.write(f"**Comuna:** {row['Comuna']}")
                st.markdown('</div>', unsafe_allow_html=True)

                # Mapa
                lat, lon = get_coordinates(row['Provincia'], row['Comuna'])
                if lat and lon:
                    st.subheader("📍 Ubicación en Mapa")
                    m = folium.Map(location=[lat, lon], zoom_start=12)
                    folium.Marker([lat, lon], popup=f"{row['Razon_social']} - {row['Comuna']}, {row['Provincia']}").add_to(m)
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
            resultados = df[df["Rut_empresa"].isin(ruts_list)]
            if not resultados.empty:
                st.success(f"✅ Encontrados {len(resultados)} RUTs de {len(ruts_list)} buscados")
                # Mostrar tabla con scrollbar si es necesario
                st.dataframe(resultados, width='stretch')
                # Resumen
                st.markdown("### 📈 Resumen")
                st.write(f"**Total RUTs encontrados:** {len(resultados)}")
                st.write(f"**Categorías encontradas:** {', '.join(resultados['CAT'].unique())}")
            else:
                st.error("❌ Ningún RUT encontrado. Verifica los números ingresados.")
        else:
            st.warning("⚠️ Por favor, ingresa al menos un RUT.")
