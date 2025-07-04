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

# Función mejorada para cargar datos
@st.cache_data
def load_data():
    data = {}
    # Lista completa de tus archivos basada en lo que compartiste
    archivos = [
        'actores_directores',
        'actores_directores_peliculas',
        'comentarios_peliculas.csv',
        'mapa_peliculas_coup',
        'pop_pais',
        'mapa_peliculas_comple',
        'peliculas_premios',
        'recaudacion_peliculas',
        'top_10_mas_vistas',
        'top_10_mejor_puntuadas',
        'vistas_por_pais',
        'vistas_por_pais_coup_on_coords'
    ]
    
    for archivo in archivos:
        try:
            # Primero intentamos cargar como CSV
            try:
                data[archivo] = pd.read_csv(f'{archivo}')
                st.success(f"Archivo {archivo} cargado correctamente")
                continue
            except:
                pass
            
            # Si falla, intentamos sin extensión
            try:
                nombre_sin_ext = archivo.split('.')[0]
                data[nombre_sin_ext] = pd.read_csv(nombre_sin_ext)
                st.success(f"Archivo {nombre_sin_ext} cargado correctamente")
                continue
            except:
                pass
            
            # Si sigue fallando, mostramos advertencia
            st.warning(f"No se pudo cargar el archivo: {archivo}")
            data[archivo] = None
            
        except Exception as e:
            st.error(f"Error al cargar {archivo}: {str(e)}")
            data[archivo] = None
    
    return data

# Título de la aplicación
st.title("Sistema de Recomendación de Películas 🎥")

# Cargar datos mostrando progreso
with st.spinner('Cargando datos...'):
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
    
    # Mostrar archivos cargados exitosamente
    st.subheader("Archivos cargados")
    archivos_cargados = [k for k, v in data.items() if v is not None]
    if archivos_cargados:
        st.write("Se cargaron correctamente los siguientes archivos:")
        for archivo in archivos_cargados:
            st.write(f"- {archivo}")
    else:
        st.error("No se pudo cargar ningún archivo. Verifica la ubicación de los archivos.")

elif seleccion == "Visualizaciones":
    st.header("Visualizaciones de datos")
    
    # Verificar qué datos están disponibles para visualización
    disponibles = [k for k, v in data.items() if v is not None]
    st.write("Datos disponibles para visualización:", ", ".join(disponibles) if disponibles else "Ninguno")
    
    # Visualización condicional basada en archivos disponibles
    if 'top_10_mas_vistas' in disponibles:
        st.subheader("Top 10 películas más vistas")
        try:
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x='vistas', y='pelicula', data=data['top_10_mas_vistas'], ax=ax)
            st.pyplot(fig)
        except Exception as e:
            st.error(f"No se pudo generar la visualización: {str(e)}")

elif seleccion == "Recomendador":
    st.header("Sistema de recomendación de películas")
    
    # Interfaz básica de recomendación
    st.write("Configura tus preferencias:")
    
    col1, col2 = st.columns(2)
    with col1:
        genero = st.selectbox("Género", ["Acción", "Comedia", "Drama", "Terror", "Ciencia Ficción"])
        año = st.slider("Año de lanzamiento", 1950, 2023, (2000, 2020))
    
    with col2:
        rating = st.slider("Rating mínimo", 1.0, 10.0, 7.0)
        duracion = st.selectbox("Duración", ["Cualquiera", "Corta (<90 min)", "Media (90-120 min)", "Larga (>120 min)"])
    
    if st.button("Generar recomendaciones"):
        st.success("""
        Recomendaciones basadas en tus preferencias:
        1. Película Ejemplo 1 (8.5/10)
        2. Película Ejemplo 2 (8.2/10)
        3. Película Ejemplo 3 (8.0/10)
        """)

elif seleccion == "Acerca de":
    st.header("Acerca de este proyecto")
    st.write("""
    **Recomendador Visualizaciones** es una aplicación para analizar y recomendar películas.
    
    Desarrollado con:
    - Python
    - Streamlit
    - Pandas
    - Matplotlib/Seaborn
    """)

# Instrucciones importantes al final
st.sidebar.markdown("---")
st.sidebar.info("""
**Nota importante:** 
Si los archivos no se cargan, verifica que:
1. Estén en el mismo directorio que app.py
2. Los nombres coincidan exactamente
3. Tengan formato CSV válido
""")
