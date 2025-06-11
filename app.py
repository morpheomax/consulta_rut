import streamlit as st
import pandas as pd

# Título
st.title("Buscador de Categoría por RUT")

# Carga del archivo txt en un DataFrame
@st.cache_data
def load_data():
    df = pd.read_csv("Chile_ABC_Tramos2023 1.txt", sep=";", header=None, names=["RUT", "Categoria"], dtype=str)
    return df

df = load_data()

# Ingreso de RUT
rut_input = st.text_input("Ingresa el RUT sin guion ni dígito verificador:", max_chars=8)

# Búsqueda
if rut_input:
    resultado = df[df["RUT"] == rut_input]
    if not resultado.empty:
        st.success(f"RUT: {resultado.iloc[0]['RUT']} - Categoría: {resultado.iloc[0]['Categoria']}")
    else:
        st.error("RUT no encontrado.")
