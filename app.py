
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="AAVV el Pla - Biblioteca", layout="wide")

# Cargar datos
@st.cache_data
def load_data():
    try:
        libros = pd.read_csv("libros.csv")
    except:
        libros = pd.DataFrame(columns=["ID", "Título", "Autor", "Categoría"])
    try:
        usuarios = pd.read_csv("usuarios.csv")
    except:
        usuarios = pd.DataFrame(columns=["ID", "Nombre", "Apellido", "Teléfono", "Email"])
    try:
        prestamos = pd.read_csv("prestamos.csv")
    except:
        prestamos = pd.DataFrame(columns=["ID", "Libro_ID", "Usuario_ID", "Fecha_Prestamo", "Fecha_Devolucion"])
    return libros, usuarios, prestamos

def save_data(libros, usuarios, prestamos):
    libros.to_csv("libros.csv", index=False)
    usuarios.to_csv("usuarios.csv", index=False)
    prestamos.to_csv("prestamos.csv", index=False)

libros, usuarios, prestamos = load_data()

st.title("📚 AAVV el Pla - Biblioteca")

menu = st.sidebar.radio("Menú", ["Libros", "Usuarios", "Préstamos", "Consultas"])

if menu == "Libros":
    st.header("Gestión de Libros")
    with st.form("add_libro"):
        st.subheader("Añadir Libro")
        id_libro = st.text_input("ID")
        titulo = st.text_input("Título")
        autor = st.text_input("Autor")
        categoria = st.text_input("Categoría")
        submitted = st.form_submit_button("Guardar")
        if submitted:
            libros.loc[len(libros)] = [id_libro, titulo, autor, categoria]
            save_data(libros, usuarios, prestamos)
            st.success("Libro añadido correctamente.")

    st.subheader("Lista de Libros")
    st.dataframe(libros)

elif menu == "Usuarios":
    st.header("Gestión de Usuarios")
    with st.form("add_usuario"):
        st.subheader("Añadir Usuario")
        id_usuario = st.text_input("ID Usuario")
        nombre = st.text_input("Nombre")
        apellido = st.text_input("Apellido")
        telefono = st.text_input("Teléfono")
        email = st.text_input("Email")
        submitted = st.form_submit_button("Guardar")
        if submitted:
            usuarios.loc[len(usuarios)] = [id_usuario, nombre, apellido, telefono, email]
            save_data(libros, usuarios, prestamos)
            st.success("Usuario añadido correctamente.")
    st.subheader("Lista de Usuarios")
    st.dataframe(usuarios)

elif menu == "Préstamos":
    st.header("Gestión de Préstamos")
    with st.form("add_prestamo"):
        st.subheader("Registrar Préstamo")
        id_prestamo = st.text_input("ID Préstamo")
        libro_id = st.selectbox("Libro", libros["ID"] if not libros.empty else [])
        usuario_id = st.selectbox("Usuario", usuarios["ID"] if not usuarios.empty else [])
        fecha_prestamo = st.date_input("Fecha de Préstamo", value=datetime.today())
        fecha_devolucion = st.date_input("Fecha de Devolución")
        submitted = st.form_submit_button("Guardar")
        if submitted:
            prestamos.loc[len(prestamos)] = [id_prestamo, libro_id, usuario_id, fecha_prestamo, fecha_devolucion]
            save_data(libros, usuarios, prestamos)
            st.success("Préstamo registrado correctamente.")
    st.subheader("Lista de Préstamos")
    overdue = pd.to_datetime(prestamos["Fecha_Devolucion"]) < datetime.today()
    st.dataframe(prestamos.style.apply(lambda x: ['background-color: salmon' if o else '' for o in overdue], axis=1))

elif menu == "Consultas":
    st.header("Consultas")
    consulta_tipo = st.selectbox("Tipo de consulta", ["Libro por Autor", "Libro por Título", "Libro por Categoría", "Usuario por Nombre", "Usuario por Teléfono", "Usuario por Email", "Préstamos por Fecha"])
    if consulta_tipo.startswith("Libro"):
        if consulta_tipo.endswith("Autor"):
            autor = st.text_input("Autor")
            resultado = libros[libros["Autor"].str.contains(autor, case=False, na=False)]
        elif consulta_tipo.endswith("Título"):
            titulo = st.text_input("Título")
            resultado = libros[libros["Título"].str.contains(titulo, case=False, na=False)]
        elif consulta_tipo.endswith("Categoría"):
            cat = st.text_input("Categoría")
            resultado = libros[libros["Categoría"].str.contains(cat, case=False, na=False)]
        st.dataframe(resultado)
    elif consulta_tipo.startswith("Usuario"):
        if consulta_tipo.endswith("Nombre"):
            nombre = st.text_input("Nombre")
            resultado = usuarios[usuarios["Nombre"].str.contains(nombre, case=False, na=False)]
        elif consulta_tipo.endswith("Teléfono"):
            telefono = st.text_input("Teléfono")
            resultado = usuarios[usuarios["Teléfono"].str.contains(telefono, case=False, na=False)]
        elif consulta_tipo.endswith("Email"):
            email = st.text_input("Email")
            resultado = usuarios[usuarios["Email"].str.contains(email, case=False, na=False)]
        st.dataframe(resultado)
    elif consulta_tipo.startswith("Préstamos"):
        fecha = st.date_input("Fecha")
        condicion = st.selectbox("Condición", ["Mayor", "Igual", "Menor"])
        prestamos["Fecha_Devolucion"] = pd.to_datetime(prestamos["Fecha_Devolucion"])
        if condicion == "Mayor":
            resultado = prestamos[prestamos["Fecha_Devolucion"] > fecha]
        elif condicion == "Igual":
            resultado = prestamos[prestamos["Fecha_Devolucion"] == fecha]
        else:
            resultado = prestamos[prestamos["Fecha_Devolucion"] < fecha]
        st.dataframe(resultado)
