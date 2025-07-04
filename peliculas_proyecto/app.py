import streamlit as st
import pandas as pd
import os
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración básica de la página
st.set_page_config(
    page_title="Recomendador de Películas",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cargar datos - ajustado a tus archivos
@st.cache_data
def load_data():
    data = {}
    try:
        # Lista de tus archivos de datos (ajusta según lo que realmente uses)
        files = {
            'actores_directores': 'actores_directores',
            'peliculas_premios': 'peliculas_premios',
            'recaudacion': 'recaudacion_peliculas',
            'top_vistas': 'top_10_mas_vistas',
            'top_puntuadas': 'top_10_mejor_puntuadas',
            'comentarios': 'comentarios_peliculas.csv',
            'vistas_pais': 'vistas_por_pais'
        }
        
        # Intentar cargar cada archivo con y sin extensión .csv
        for name, filename in files.items():
            try:
                # Primero intenta con .csv
                data[name] = pd.read_csv(f'{filename}.csv')
            except:
                # Si falla, intenta sin extensión
                try:
                    data[name] = pd.read_csv(filename)
                except Exception as e:
                    st.warning(f"No se pudo cargar {filename}: {str(e)}")
                    data[name] = None
        
        return data
    except Exception as e:
        st.error(f"Error cargando datos: {e}")
        return {}

# Título de la aplicación
st.title("Sistema de Recomendación de Películas 🎥")

# Cargar datos
data = load_data()

# Sidebar para navegación
st.sidebar.title("Navegación")
opciones = ["Inicio", "Visualizaciones", "Recomendador", "Acerca de"]
seleccion = st.sidebar.radio("Ir a", opciones)

if seleccion == "Inicio":
    st.header("Bienvenido al recomendador de películas")
    st.write("""
    Esta aplicación te permite explorar datos de películas y obtener recomendaciones 
    personalizadas basadas en tus preferencias.
    """)
    
    # Mostrar estadísticas si los datos están cargados
    if data.get('top_vistas') is not None:
        st.subheader("Algunas estadísticas")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Películas en top vistas", len(data['top_vistas']))
        with col2:
            st.metric("Películas mejor puntuadas", len(data['top_puntuadas']) if data.get('top_puntuadas') is not None else "N/A")

elif seleccion == "Visualizaciones":
    st.header("Visualizaciones de datos")
    
    # Visualización 1: Top películas más vistas
    if data.get('top_vistas') is not None:
        st.subheader("Top 10 películas más vistas")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x='vistas', y='pelicula', data=data['top_vistas'], ax=ax)
        ax.set_xlabel('Número de vistas')
        ax.set_ylabel('Película')
        st.pyplot(fig)
    else:
        st.warning("Datos de top vistas no disponibles")
    
    # Visualización 2: Recaudación (si existe)
    if data.get('recaudacion') is not None:
        st.subheader("Recaudación de películas")
        # Ajusta según las columnas que tenga tu archivo
        if 'recaudacion' in data['recaudacion'].columns:
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x='recaudacion', y='pelicula', data=data['recaudacion'].nlargest(10, 'recaudacion'), ax=ax)
            ax.set_xlabel('Recaudación')
            ax.set_ylabel('Película')
            st.pyplot(fig)

elif seleccion == "Recomendador":
    st.header("Sistema de recomendación de películas")
    
    # Ejemplo de interfaz de recomendación - ajusta según tu lógica
    col1, col2 = st.columns(2)
    
    with col1:
        genero = st.selectbox("Género favorito", 
                             ["Acción", "Comedia", "Drama", "Ciencia Ficción", "Terror"])
        año_min = st.slider("Año mínimo", 1950, 2023, 2000)
    
    with col2:
        rating_min = st.slider("Rating mínimo", 1.0, 10.0, 7.0, step=0.5)
        duracion = st.selectbox("Duración preferida", 
                              ["Cualquiera", "<90 min", "90-120 min", ">120 min"])
    
    if st.button("Generar recomendaciones"):
        # Aquí iría tu lógica real de recomendación
        # Esto es solo un ejemplo placeholder
        st.success("""
        Recomendaciones basadas en tus preferencias:
        1. Película de ejemplo 1 (8.5/10)
        2. Película de ejemplo 2 (8.2/10)
        3. Película de ejemplo 3 (8.0/10)
        """)
        
        # Espacio para mostrar imágenes/pósters de películas recomendadas
        st.subheader("Pósters de películas recomendadas")
        try:
            # Ejemplo de cómo mostrar imágenes - ajusta paths según tu estructura
            img_dir = "imagenes_directores_actores"  # Cambia esto por tu directorio real
            if os.path.exists(img_dir):
                sample_images = [f for f in os.listdir(img_dir) if f.endswith(('.jpg', '.png'))][:3]
                cols = st.columns(3)
                for i, img in enumerate(sample_images):
                    with cols[i]:
                        st.image(Image.open(os.path.join(img_dir, img)), width=150)
        except Exception as e:
            st.warning(f"No se pudieron cargar imágenes: {e}")

elif seleccion == "Acerca de":
    st.header("Acerca de este proyecto")
    st.write("""
    **Recomendador de películas** es un sistema que analiza datos cinematográficos
    para proporcionar recomendaciones personalizadas a los usuarios.
    
    **Datos incluidos:**
    - Top películas más vistas
    - Películas mejor puntuadas
    - Datos de recaudación
    - Información de actores y directores
    - Comentarios sobre películas
    """)
    
    st.write("Desarrollado con Python y Streamlit")

# Notas importantes:
# 1. Asegúrate de que todos tus archivos de datos estén en el mismo directorio que app.py
# 2. Si los archivos están en una subcarpeta 'data', ajusta los paths añadiendo 'data/' antes del nombre
# 3. Verifica los nombres exactos de las columnas en tus CSVs para ajustar las visualizaciones
