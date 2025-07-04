import streamlit as st
import pandas as pd
import os
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns
import sys

# Configuración inicial
st.set_page_config(
    page_title="Recomendador de Películas",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Función mejorada para verificar y cargar archivos
def load_data_with_verification():
    data = {}
    data_dir = "data"
    
    # Verificar si la carpeta data existe
    if not os.path.exists(data_dir):
        st.error(f"❌ La carpeta '{data_dir}' no existe en el directorio actual")
        st.error(f"Directorio actual: {os.getcwd()}")
        return data
    
    st.info(f"📁 Contenido de la carpeta '{data_dir}':")
    files_in_data = os.listdir(data_dir)
    st.write(files_in_data)
    
    # Mapeo de nombres de archivos (sin extensión) a posibles nombres reales
    expected_files = {
        'actores_directores': ['actores_directores.csv', 'actores_directores'],
        'actores_directores_peliculas': ['actores_directores_peliculas.csv', 'actores_directores_peliculas'],
        'comentarios_peliculas': ['comentarios_peliculas.csv', 'comentarios_peliculas.csv.csv'],
        'mapa_peliculas': ['mapa_peliculas.csv', 'mapa_peliculas_coup'],
        'peliculas_completas': ['peliculas_completas.csv', 'mapa_peliculas_comple'],
        'peliculas_premios': ['peliculas_premios.csv'],
        'recaudacion_peliculas': ['recaudacion_peliculas.csv'],
        'top_10_mas_vistas': ['top_10_mas_vistas.csv'],
        'top_10_mejor_puntuadas': ['top_10_mejor_puntuadas.csv'],
        'vistas_por_pais': ['vistas_por_pais.csv', 'vistas_por_pais'],
        'vistas_por_pais_con_coords': ['vistas_por_pais_con_coords.csv', 'vistas_por_pais_coup_on_coords']
    }
    
    for file_key, possible_names in expected_files.items():
        loaded = False
        for filename in possible_names:
            filepath = os.path.join(data_dir, filename)
            if os.path.exists(filepath):
                try:
                    # Intentar leer como CSV
                    data[file_key] = pd.read_csv(filepath)
                    st.success(f"✅ {filename} cargado como '{file_key}'")
                    loaded = True
                    break
                except pd.errors.EmptyDataError:
                    st.warning(f"⚠️ {filename} está vacío")
                    break
                except Exception as e:
                    st.warning(f"⚠️ Error al leer {filename}: {str(e)}")
                    break
        
        if not loaded:
            st.error(f"❌ No se encontró ningún archivo válido para: {file_key}")
            st.error(f"Archivos probados: {', '.join(possible_names)}")
    
    return data

# Cargar datos con verificación
with st.spinner('Verificando y cargando archivos...'):
    data = load_data_with_verification()

# Mostrar estructura del proyecto en sidebar
st.sidebar.title("Estructura del Proyecto")
st.sidebar.code("""
peliculas_proyecto/
├── app.py
├── requirements.txt
├── README.md
├── data/ (debe contener los archivos CSV)
├── imagenes/
│   └── imagenes_directores_actores/
└── utils/
    ├── recomendador.py
    └── visualizaciones.py
""")

# Páginas de la aplicación
pages = {
    "🏠 Inicio": lambda: show_home_page(data),
    "📊 Visualizaciones": lambda: show_visualizations(data),
    "🎯 Recomendador": lambda: show_recommender(data),
    "ℹ️ Acerca De": lambda: show_about()
}

page = st.sidebar.radio("Navegación", list(pages.keys()))
pages[page]()

def show_home_page(data):
    st.title("🎥 Sistema de Recomendación de Películas")
    st.write("""
    Bienvenido al sistema de recomendación de películas. 
    Explora nuestras visualizaciones y obtén recomendaciones personalizadas.
    """)
    
    # Mostrar estado de carga de datos
    st.subheader("Estado de los Datos")
    if data:
        st.success("Algunos archivos se cargaron correctamente")
        st.write("Claves disponibles en los datos:", list(data.keys()))
    else:
        st.error("No se pudo cargar ningún archivo de datos")

def show_visualizations(data):
    st.title("📊 Visualizaciones de Datos")
    
    if not data:
        st.warning("No hay datos disponibles para visualizar")
        return
    
    # Selector de visualización
    viz_option = st.selectbox(
        "Selecciona una visualización",
        options=["Top Películas", "Recaudación", "Distribución por País"]
    )
    
    if viz_option == "Top Películas" and 'top_10_mas_vistas' in data:
        st.subheader("Top 10 Películas Más Vistas")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(
            x='vistas', 
            y='pelicula', 
            data=data['top_10_mas_vistas'],
            palette='coolwarm',
            ax=ax
        )
        ax.set_xlabel("Número de Vistas")
        ax.set_ylabel("Película")
        st.pyplot(fig)

def show_recommender(data):
    st.title("🎯 Sistema de Recomendación")
    
    with st.form("preferences_form"):
        st.subheader("Configura tus preferencias")
        
        col1, col2 = st.columns(2)
        
        with col1:
            genre = st.selectbox(
                "Género favorito",
                options=["Todos", "Acción", "Comedia", "Drama", "Ciencia Ficción"]
            )
            year_range = st.slider(
                "Rango de años",
                1950, 2023, (2000, 2023)
            
        with col2:
            min_rating = st.slider(
                "Rating mínimo",
                1.0, 10.0, 7.0, 0.5)
            duration = st.selectbox(
                "Duración preferida",
                options=["Cualquiera", "Corta (<90 min)", "Media (90-120 min)", "Larga (>120 min)"]
            )
        
        submitted = st.form_submit_button("Generar Recomendaciones")
    
    if submitted:
        if not data:
            st.error("No hay datos disponibles para generar recomendaciones")
            return
        
        # Lógica de recomendación simple (puedes reemplazar con tu módulo)
        st.success("Recomendaciones generadas (ejemplo):")
        st.write("1. Película Ejemplo 1 (8.5/10)")
        st.write("2. Película Ejemplo 2 (8.2/10)")
        st.write("3. Película Ejemplo 3 (8.0/10)")

def show_about():
    st.title("ℹ️ Acerca del Proyecto")
    st.write("""
    Sistema de recomendación de películas desarrollado con Streamlit.
    
    **Características:**
    - Análisis de datos cinematográficos
    - Visualizaciones interactivas
    - Sistema de recomendación personalizado
    
    **Tecnologías:**
    - Python
    - Streamlit
    - Pandas
    - Matplotlib/Seaborn
    """)

if __name__ == "__main__":
    # Instrucciones adicionales
    st.sidebar.markdown("---")
    st.sidebar.info("""
    **Si los archivos no se cargan:**
    1. Verifica que estén en la carpeta 'data'
    2. Comprueba los nombres exactos
    3. Asegúrate que sean archivos CSV válidos
    """)
