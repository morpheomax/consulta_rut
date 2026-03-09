# file: app.py
from pathlib import Path
import html
import re
import unicodedata

import pandas as pd
import streamlit as st


# =========================
# Configuración principal
# =========================
st.set_page_config(
    page_title="Buscador de Clasificación por RUT",
    page_icon="🧾",
    layout="centered",
    initial_sidebar_state="collapsed",
)

EXCEL_FILE = Path("ABC_clientes.xlsx")  # Reemplazar por el nombre real del archivo
EXCEL_SHEET = "sheet1"  # Reemplazar por el nombre real de la hoja

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


# =========================
# Utilidades
# =========================
def normalize_text(text: str) -> str:
    """
    Normaliza texto para comparar nombres de columnas:
    - minúsculas
    - sin tildes
    - espacios y símbolos -> _
    """
    text = unicodedata.normalize("NFKD", str(text)).encode("ascii", "ignore").decode("utf-8")
    text = re.sub(r"[^a-zA-Z0-9]+", "_", text.lower()).strip("_")
    return text


def clean_rut(value: str | None) -> str:
    """
    Deja solo dígitos del RUT, sin puntos, guion ni DV.
    También elimina ceros a la izquierda para homologar la búsqueda.
    """
    if value is None:
        return ""

    digits_only = re.sub(r"\D", "", str(value))
    if not digits_only:
        return ""

    cleaned = digits_only.lstrip("0")
    return cleaned if cleaned else "0"


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Renombra columnas del Excel a los nombres esperados por la app.
    """
    rename_map = {}
    for col in df.columns:
        normalized = normalize_text(col)
        if normalized in COLUMN_ALIASES:
            rename_map[col] = COLUMN_ALIASES[normalized]

    df = df.rename(columns=rename_map)

    missing = [col for col in DISPLAY_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(
            "Faltan columnas obligatorias en el Excel: " + ", ".join(missing)
        )

    return df[DISPLAY_COLUMNS].copy()


@st.cache_data(show_spinner="Cargando base de clientes...")
def _load_data_cached(excel_path: str, file_mtime: float) -> pd.DataFrame:
    """
    Carga cacheada del Excel. file_mtime se usa para invalidar cache
    cuando el archivo cambia.
    """
    _ = file_mtime  # se usa solo para invalidar cache si cambia el archivo

    df = pd.read_excel(excel_path, dtype=str)
    df = standardize_columns(df)

    for col in DISPLAY_COLUMNS:
        df[col] = df[col].fillna("").astype(str).str.strip()

    df["Rut_empresa_busqueda"] = df["Rut_empresa"].apply(clean_rut)
    df = df[df["Rut_empresa_busqueda"] != ""].copy()
    df = df.drop_duplicates(subset="Rut_empresa_busqueda", keep="first")

    return df


def load_data(excel_path: Path) -> pd.DataFrame:
    if not excel_path.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo Excel: {excel_path.resolve()}"
        )
    return _load_data_cached(str(excel_path), excel_path.stat().st_mtime)


def get_default_result(rut_input: str) -> dict:
    """
    Resultado por defecto cuando el RUT no existe en la base.
    """
    return {
        "Rut_empresa": rut_input,
        "Dv_empresa": "No disponible",
        "Razon_social": "No disponible",
        "Actividad_economica": "No disponible",
        "Direccion": "No disponible",
        "Clasificacion": "C3",
    }


def search_company(df: pd.DataFrame, rut_input: str) -> tuple[dict, bool]:
    """
    Busca por Rut_empresa.
    Retorna:
    - dict con los datos
    - bool indicando si fue encontrado
    """
    search_key = clean_rut(rut_input)
    match = df.loc[df["Rut_empresa_busqueda"] == search_key]

    if not match.empty:
        result = match.iloc[0][DISPLAY_COLUMNS].to_dict()
        return result, True

    return get_default_result(search_key), False


def format_full_rut(rut: str, dv: str) -> str:
    rut_clean = clean_rut(rut)
    if not rut_clean:
        return "No disponible"

    if dv and dv != "No disponible":
        return f"{rut_clean}-{dv}"
    return rut_clean


def inject_styles() -> None:
    st.markdown(
        """
        <style>
            .block-container {
                max-width: 980px;
                padding-top: 2rem;
                padding-bottom: 2rem;
            }

            .hero {
                background: linear-gradient(135deg, #0f172a 0%, #1d4ed8 100%);
                border-radius: 18px;
                padding: 1.4rem 1.6rem;
                color: white;
                margin-bottom: 1rem;
            }

            .hero h1 {
                margin: 0;
                font-size: 1.9rem;
                font-weight: 700;
            }

            .hero p {
                margin: 0.45rem 0 0 0;
                color: #e2e8f0;
                font-size: 0.98rem;
            }

            .class-card {
                border-radius: 18px;
                padding: 1.3rem;
                color: white;
                text-align: center;
                margin-bottom: 1rem;
                box-shadow: 0 10px 25px rgba(15, 23, 42, 0.10);
            }

            .class-title {
                font-size: 0.95rem;
                opacity: 0.95;
                margin-bottom: 0.35rem;
            }

            .class-value {
                font-size: 3rem;
                font-weight: 800;
                line-height: 1.05;
                margin-bottom: 0.35rem;
            }

            .class-subtitle {
                font-size: 0.92rem;
                opacity: 0.95;
            }

            .detail-label {
                color: #64748b;
                font-size: 0.9rem;
                font-weight: 600;
            }

            .detail-value {
                color: #0f172a;
                font-size: 1rem;
                font-weight: 500;
                word-break: break-word;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header() -> None:
    st.markdown(
        """
        <div class="hero">
            <h1>Buscador de Clasificación por RUT</h1>
            <p>
                Consulta clientes por <strong>RUT empresa</strong> ingresando solo números,
                sin puntos, sin guion y sin dígito verificador.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def get_classification_color(classification: str) -> str:
    value = str(classification).strip().upper()
    colors = {
        "C1": "#16a34a",
        "C2": "#f59e0b",
        "C3": "#dc2626",
    }
    return colors.get(value, "#334155")


def render_classification_card(classification: str, found: bool) -> None:
    title = "Clasificación encontrada" if found else "Clasificación por defecto"
    subtitle = "Dato principal de la consulta"
    color = get_classification_color(classification)

    st.markdown(
        f"""
        <div class="class-card" style="background: {color};">
            <div class="class-title">{html.escape(title)}</div>
            <div class="class-value">{html.escape(str(classification))}</div>
            <div class="class-subtitle">{html.escape(subtitle)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_detail_section(result: dict) -> None:
    """
    Renderiza el detalle del cliente usando componentes nativos de Streamlit
    para evitar que se vean etiquetas HTML.
    """
    st.subheader("Detalle del cliente")

    with st.container(border=True):
        for idx, col in enumerate(DISPLAY_COLUMNS):
            label = FRIENDLY_LABELS.get(col, col)
            value = result.get(col, "") or "No disponible"

            left, right = st.columns([1, 2.2])
            with left:
                st.markdown(f"**{label}**")
            with right:
                st.write(value)

            if idx < len(DISPLAY_COLUMNS) - 1:
                st.divider()


def init_session_state() -> None:
    defaults = {
        "search_result": None,
        "search_found": False,
        "search_error": "",
        "last_rut": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# =========================
# App
# =========================
inject_styles()
render_header()
init_session_state()

with st.expander("Instrucciones de uso", expanded=False):
    st.markdown(
        """
        - Ingresa el **RUT de la empresa** usando solo números.
        - No escribas puntos, guion ni dígito verificador.
        - Si el RUT no existe en la base, la app devolverá **Clasificación C3** por defecto.
        """
    )

try:
    df = load_data(EXCEL_FILE)
except FileNotFoundError as e:
    st.error(str(e))
    st.info("Guarda el archivo Excel en la misma carpeta de la app o ajusta la variable EXCEL_FILE.")
    st.stop()
except ValueError as e:
    st.error(f"Problema con la estructura del Excel: {e}")
    st.stop()
except Exception as e:
    st.error(f"Ocurrió un error al cargar el archivo: {e}")
    st.stop()

with st.form("busqueda_rut", clear_on_submit=False):
    rut_input = st.text_input(
        "Ingresa el RUT del cliente",
        placeholder="Ejemplo: 76123456",
        help="Solo números, sin puntos, sin guion y sin dígito verificador.",
        max_chars=12,
    )

    submitted = st.form_submit_button(
        "Buscar cliente",
        type="primary",
        use_container_width=True,
    )

if submitted:
    rut_clean = clean_rut(rut_input)

    if not rut_clean or len(rut_clean) < 7:
        st.session_state["search_result"] = None
        st.session_state["search_found"] = False
        st.session_state["search_error"] = (
            "Ingresa un RUT válido usando solo números, sin puntos, sin guion y sin dígito verificador."
        )
        st.session_state["last_rut"] = ""
    else:
        result, found = search_company(df, rut_clean)
        st.session_state["search_result"] = result
        st.session_state["search_found"] = found
        st.session_state["search_error"] = ""
        st.session_state["last_rut"] = rut_clean

if st.session_state["search_error"]:
    st.warning(st.session_state["search_error"])

if st.session_state["search_result"] is not None:
    result = st.session_state["search_result"]
    found = st.session_state["search_found"]

    if found:
        st.success("Cliente encontrado en la base.")
    else:
        st.warning("No se encontró el RUT en la base. Se muestra clasificación por defecto C3.")

    col1, col2 = st.columns([1, 1.8], gap="large")

    with col1:
        render_classification_card(result["Clasificacion"], found)
        full_rut = format_full_rut(result["Rut_empresa"], result["Dv_empresa"])
        st.markdown(f"**RUT consultado:** {full_rut}")

    with col2:
        render_detail_section(result)

    if not found:
        st.info(
            "Es posible que el cliente haya formalizado la empresa fuera del periodo que informa SII o que su facturación corresponda a C3."
        )

st.caption(f"Base cargada: {EXCEL_FILE.name} · Registros disponibles: {len(df):,}".replace(",", "."))