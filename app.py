# file: app.py
from pathlib import Path
import re
import unicodedata

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Buscador de Clasificación por RUT",
    page_icon="🧾",
    layout="centered",
)

# Archivo y hoja
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "ABC_clientes.xlsx"
SHEET_NAME = 0  # Usa la primera hoja del Excel. Cambia si necesitas una hoja específica.

DISPLAY_COLUMNS = [
    "Rut_empresa",
    "Dv_empresa",
    "Razon_social",
    "Actividad_economica",
    "Direccion",
    "Clasificacion",
]

COLUMN_ALIASES = {
    "rut_empresa": "Rut_empresa",
    "dv_empresa": "Dv_empresa",
    "razon_social": "Razon_social",
    "actividad_economica": "Actividad_economica",
    "direccion": "Direccion",
    "clasificacion": "Clasificacion",
}

FRIENDLY_LABELS = {
    "Rut_empresa": "RUT empresa",
    "Dv_empresa": "DV empresa",
    "Razon_social": "Razón social",
    "Actividad_economica": "Actividad económica",
    "Direccion": "Dirección",
    "Clasificacion": "Clasificación",
}


def normalize_name(value):
    text = unicodedata.normalize("NFKD", str(value)).encode("ascii", "ignore").decode("utf-8")
    return re.sub(r"[^a-zA-Z0-9]+", "_", text.lower()).strip("_")


def clean_rut(value):
    if value is None:
        return ""

    digits = re.sub(r"\D", "", str(value))
    if not digits:
        return ""

    cleaned = digits.lstrip("0")
    return cleaned if cleaned else "0"


def safe_value(value):
    text = str(value).strip() if value is not None else ""
    return text if text else "No disponible"


def format_full_rut(rut, dv):
    rut_clean = clean_rut(rut)
    dv_text = safe_value(dv)

    if not rut_clean:
        return "No disponible"

    if dv_text != "No disponible":
        return f"{rut_clean}-{dv_text}"

    return rut_clean


@st.cache_data(show_spinner="Cargando base de clientes...")
def load_data(file_path, sheet_name, file_mtime):
    _ = file_mtime  # Se usa para invalidar caché si cambia el archivo

    df = pd.read_excel(file_path, sheet_name=sheet_name, dtype=str)

    rename_map = {}
    for col in df.columns:
        normalized = normalize_name(col)
        if normalized in COLUMN_ALIASES:
            rename_map[col] = COLUMN_ALIASES[normalized]

    df = df.rename(columns=rename_map)

    missing = [col for col in DISPLAY_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError("Faltan columnas obligatorias en el Excel: " + ", ".join(missing))

    df = df[DISPLAY_COLUMNS].copy()

    for col in DISPLAY_COLUMNS:
        df[col] = df[col].fillna("").astype(str).str.strip()

    df["rut_busqueda"] = df["Rut_empresa"].apply(clean_rut)
    df = df[df["rut_busqueda"] != ""].drop_duplicates(subset="rut_busqueda", keep="first")

    return df


def get_data():
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {DATA_FILE.resolve()}")

    return load_data(str(DATA_FILE), SHEET_NAME, DATA_FILE.stat().st_mtime)


def default_result(rut):
    return {
        "Rut_empresa": rut,
        "Dv_empresa": "No disponible",
        "Razon_social": "No disponible",
        "Actividad_economica": "No disponible",
        "Direccion": "No disponible",
        "Clasificacion": "C3",
    }


def search_company(df, rut_input):
    rut_clean = clean_rut(rut_input)
    if not rut_clean:
        return None, False

    match = df.loc[df["rut_busqueda"] == rut_clean]

    if match.empty:
        return default_result(rut_clean), False

    row = match.iloc[0]
    result = {col: safe_value(row[col]) for col in DISPLAY_COLUMNS}
    return result, True


def render_classification(classification, found):
    st.subheader("Clasificación")
    st.metric("Resultado", classification)

    classification = str(classification).upper().strip()

    if found:
        if classification == "C1":
            st.success("Cliente encontrado en la base.")
        elif classification == "C2":
            st.warning("Cliente encontrado en la base.")
        else:
            st.error("Cliente encontrado en la base.")
    else:
        st.warning("No se encontró el RUT en la base. Se asigna clasificación C3 por defecto.")


def render_details(result):
    st.subheader("Detalle del cliente")

    with st.container(border=True):
        for col in DISPLAY_COLUMNS:
            left, right = st.columns([1, 2])
            left.markdown(f"**{FRIENDLY_LABELS[col]}**")
            right.write(safe_value(result.get(col, "")))


st.title("Buscador de Clasificación por RUT")
st.caption("Consulta clientes ingresando solo el RUT, sin puntos, sin guion y sin dígito verificador.")

with st.expander("Instrucciones de uso", expanded=False):
    st.markdown(
        """
        - Ingresa el **RUT de la empresa** usando solo números.
        - No escribas puntos, guion ni dígito verificador.
        - Si el RUT no existe en la base, se devolverá **Clasificación C3** por defecto.
        """
    )

try:
    df = get_data()
except FileNotFoundError as e:
    st.error(str(e))
    st.stop()
except ValueError as e:
    st.error(f"Problema con la estructura del archivo: {e}")
    st.stop()
except Exception as e:
    st.error(f"Error al cargar la base: {e}")
    st.stop()

with st.form("search_form"):
    rut_input = st.text_input(
        "Ingresa el RUT del cliente",
        placeholder="Ejemplo: 76123456",
        max_chars=12,
    )
    submitted = st.form_submit_button("Buscar cliente", type="primary", use_container_width=True)

if submitted:
    rut_clean = clean_rut(rut_input)

    if not rut_clean or len(rut_clean) < 7:
        st.warning("Ingresa un RUT válido usando solo números, sin puntos, sin guion y sin dígito verificador.")
    else:
        result, found = search_company(df, rut_clean)

        col1, col2 = st.columns([1, 2], gap="large")

        with col1:
            render_classification(result["Clasificacion"], found)
            st.caption(f"RUT consultado: {format_full_rut(result['Rut_empresa'], result['Dv_empresa'])}")

        with col2:
            render_details(result)

        if not found:
            st.info(
                "Es posible que el cliente haya formalizado la empresa fuera del periodo que informa SII "
                "o que su facturación corresponda a C3."
            )

st.caption(f"Base cargada: {DATA_FILE.name} · Registros disponibles: {len(df):,}".replace(",", "."))