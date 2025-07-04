import streamlit as st
import pandas as pd
import os
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración básica de la página
st.set_page_config(
    page_title="Análisis de Películas",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cargar datos (ajusta estos paths según tu estructura real)
@st.cache_data
def load_data():
    # Carga tus archivos CSV aquí
    try:
        actores_directores = pd.read_csv('data/actores_directores.csv')
        peliculas_premios = pd.read_csv('data/peliculas_premios.csv')
        recaudacion = pd.read_csv('data/recaudacion_peliculas.csv')
        top_vistas = pd.read_csv('data/top_10_mas_vistas.csv')
        top_puntuadas = pd.read_csv('data/top_10_mejor_puntuadas.csv')
        return actores_directores, peliculas_premios, recaudacion, top_vistas, top_puntuadas
    except Exception as e:
        st.error(f"Error cargando datos: {e}")
        return None, None, None, None, None

# Título de la aplicación
st.title("Análisis de Películas 🎥")

# Sidebar para navegación
st.sidebar.title("Navegación")
opciones = ["Inicio", "Visualizaciones", "Recomendador", "Acerca de"]
seleccion = st.sidebar.radio("Ir a", opciones)

if seleccion == "Inicio":
    st.header("Bienvenido al análisis de películas")
    st.write("""
    Esta aplicación te permite explorar datos interesantes sobre películas, 
    actores, directores y más. Usa el menú de la izquierda para navegar.
    """)
    
    # Mostrar alguna estadística resumida
    st.subheader("Algunas estadísticas")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Películas en top vistas", "10")
    with col2:
        st.metric("Películas mejor puntuadas", "10")
    with col3:
        st.metric("Países con datos", "50+")

elif seleccion == "Visualizaciones":
    st.header("Visualizaciones de datos")
    
    # Ejemplo de visualización - puedes agregar más
    st.subheader("Top 10 películas más vistas")
    try:
        top_vistas = pd.read_csv('data/top_10_mas_vistas.csv')
        fig, ax = plt.subplots()
        sns.barplot(x='vistas', y='pelicula', data=top_vistas, ax=ax)
        st.pyplot(fig)
    except Exception as e:
        st.error(f"No se pudo cargar la visualización: {e}")
    
    # Puedes agregar más visualizaciones aquí

elif seleccion == "Recomendador":
    st.header("Sistema de recomendación de películas")
    st.write("""
    Esta sección te ayudará a encontrar películas que podrían gustarte 
    basado en tus preferencias.
    """)
    
    # Ejemplo de interfaz de recomendación
    genero = st.selectbox("Selecciona tu género favorito", 
                         ["Acción", "Comedia", "Drama", "Ciencia Ficción"])
    rating = st.slider("Rating mínimo que prefieres", 1, 10, 7)
    
    if st.button("Recomendar películas"):
        # Aquí iría tu lógica de recomendación
        st.success(f"Recomendando películas de {genero} con rating mayor a {rating}")

elif seleccion == "Acerca de":
    st.header("Acerca de este proyecto")
    st.write("""
    Este proyecto fue creado para analizar datos de películas y proporcionar 
    recomendaciones basadas en preferencias de usuarios.
    
    **Tecnologías utilizadas:**
    - Python
    - Streamlit
    - Pandas
    - Matplotlib/Seaborn
    """)

# Nota: Necesitarás ajustar los nombres de archivos y paths según tu estructura exacta