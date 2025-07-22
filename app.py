
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Gestión de Biblioteca", layout="wide")

st.title("📚 Aplicación de Gestión de Biblioteca")

menu = st.sidebar.selectbox("Selecciona una sección", ["Libros", "Usuarios", "Categorías", "Préstamos"])

if menu == "Libros":
    st.header("📖 Consulta de Libros")
    df = pd.read_csv("libros.csv")
    filtro = st.text_input("Buscar por título, autor o categoría")
    if filtro:
        df = df[df.apply(lambda row: filtro.lower() in str(row["Título"]).lower()
                         or filtro.lower() in str(row["Autor"]).lower()
                         or filtro.lower() in str(row["Categoría"]).lower(), axis=1)]
    st.dataframe(df)
    st.download_button("Descargar resultados", df.to_csv(index=False), "libros_filtrados.csv")

elif menu == "Usuarios":
    st.header("👥 Consulta de Usuarios")
    df = pd.read_csv("usuarios.csv")
    filtro = st.text_input("Buscar por nombre, apellido, email o teléfono")
    if filtro:
        df = df[df.apply(lambda row: filtro.lower() in str(row["Nombre"]).lower()
                         or filtro.lower() in str(row["Apellido"]).lower()
                         or filtro.lower() in str(row["Email"]).lower()
                         or filtro.lower() in str(row["Teléfono"]).lower(), axis=1)]
    st.dataframe(df)
    st.download_button("Descargar resultados", df.to_csv(index=False), "usuarios_filtrados.csv")

elif menu == "Categorías":
    st.header("🗂 Categorías y Áreas Temáticas")
    df = pd.read_csv("categorias.csv")
    st.dataframe(df)

elif menu == "Préstamos":
    st.header("📋 Gestión de Préstamos")
    df = pd.read_csv("prestamos.csv")
    df["Fecha Devolución Prevista"] = pd.to_datetime(df["Fecha Devolución Prevista"])
    df["Estado Visual"] = df.apply(lambda row: "🔴 Vencido" if row["Estado"] == "Pendiente" and row["Fecha Devolución Prevista"] < datetime.now() else row["Estado"], axis=1)
    st.dataframe(df.style.applymap(lambda val: 'background-color: pink' if val == "🔴 Vencido" else '', subset=["Estado Visual"]))
    st.download_button("Descargar préstamos", df.to_csv(index=False), "prestamos.csv")
