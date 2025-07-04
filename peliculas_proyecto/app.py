import streamlit as st
import pandas as pd
import os
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de la página
st.set_page_config(
    page_title="Recomendador de Películas",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Función para cargar datos
@st.cache_data
def load_data():
    data = {}
    data_dir = "data"
    
    # Lista de archivos esperados
    archivos = [
        "actores_directores.csv",
        "actores_directores_peliculas.csv",
        "comentarios_peliculas.csv",
        "mapa_peliculas.csv",
        "peliculas_completas.csv",
        "peliculas_premios.csv",
        "recaudacion_peliculas.csv",
        "top_10_mas_vistas.csv",
        "top_10_mejor_puntuadas.csv",
        "vistas_por_pais.csv",
        "vistas_por_pais_con_coords.csv"
    ]
    
    for archivo in archivos:
        filepath = os.path.join(data_dir, archivo)
        try:
            if os.path.exists(filepath):
                data[archivo.split('.')[0]] = pd.read_csv(filepath)
                st.success(f"✅ {archivo} cargado correctamente")
            else:
                st.warning(f"⚠️ Archivo no encontrado: {filepath}")
        except Exception as e:
            st.error(f"❌ Error al cargar {archivo}: {str(e)}")
    
    return data

# Cargar datos
with st.spinner('Cargando datos...'):
    data = load_data()

# Título principal
st.title("🎥 Sistema de Recomendación de Películas")

# Sidebar con navegación
st.sidebar.title("Navegación")
menu_opciones = ["🏠 Inicio", "📊 Visualizaciones", "🎯 Recomendador", "ℹ️ Acerca de"]
seleccion = st.sidebar.radio("Ir a", menu_opciones)

# Página de Inicio
if seleccion == "🏠 Inicio":
    st.header("Bienvenido al Sistema de Recomendación de Películas")
    st.write("""
    Explora nuestro catálogo de películas, descubre visualizaciones interesantes 
    y obtén recomendaciones personalizadas basadas en tus preferencias.
    """)
    
    # Mostrar estadísticas básicas
    if 'top_10_mas_vistas' in data:
        st.subheader("Top 3 Películas Más Vistas")
        top3 = data['top_10_mas_vistas'].head(3)
        cols = st.columns(3)
        for idx, (_, row) in enumerate(top3.iterrows()):
            with cols[idx]:
                st.write(f"**{row['pelicula']}** ({row['vistas']} vistas)")

# Página de Visualizaciones
elif seleccion == "📊 Visualizaciones":
    st.header("Visualizaciones de Datos")
    
    if 'top_10_mas_vistas' in data:
        st.subheader("Top 10 películas más vistas")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x='vistas', y='pelicula', data=data['top_10_mas_vistas'], ax=ax)
        ax.set_xlabel('Número de vistas')
        ax.set_ylabel('Película')
        st.pyplot(fig)

# Página de Recomendador
elif seleccion == "🎯 Recomendador":
    st.header("Sistema de recomendación de películas")
    
    with st.form("preferencias_form"):
        st.subheader("Configura tus preferencias")
        
        col1, col2 = st.columns(2)
        
        with col1:
            genero = st.selectbox("Género", ["Todos", "Acción", "Comedia", "Drama", "Ciencia Ficción"])
            # CORRECCIÓN: Cambiado de año_min/max a min_year/max_year
            min_year, max_year = st.slider(
                "Rango de años",
                1950, 2023, (2000, 2023))
        
        with col2:
            rating_min = st.slider("Rating mínimo", 1.0, 10.0, 7.0, step=0.5)
            duracion = st.selectbox("Duración", ["Cualquiera", "<90 min", "90-120 min", ">120 min"])
        
        submitted = st.form_submit_button("Generar Recomendaciones")
    
    if submitted:
        st.success("""
        Recomendaciones basadas en tus preferencias:
        1. Película Ejemplo 1 (8.5/10)
        2. Película Ejemplo 2 (8.2/10)
        3. Película Ejemplo 3 (8.0/10)
        """)

# Página Acerca De
elif seleccion == "ℹ️ Acerca De":
    st.header("Acerca de este proyecto")
    st.write("""
    **Recomendador Visualizaciones** es una aplicación para analizar y recomendar películas.
    
    Desarrollado con:
    - Python
    - Streamlit
    - Pandas
    - Matplotlib/Seaborn
    """)

# Instrucciones importantes
st.sidebar.markdown("---")
st.sidebar.info("""
**Nota importante:** 
Si los archivos no se cargan, verifica que:
1. Estén en la carpeta 'data'
2. Los nombres coincidan exactamente
3. Tengan formato CSV válido
""")
