import streamlit as st
import pandas as pd
import os
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns
import sys

# Añadir el directorio utils al path para importar tus módulos
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

# Intentar importar tus módulos personalizados
try:
    from recomendador import recomendar_peliculas
    from visualizaciones import generar_visualizaciones
except ImportError as e:
    st.warning(f"No se pudieron cargar los módulos personalizados: {e}")

# Configuración de la página
st.set_page_config(
    page_title="Sistema de Recomendación de Películas",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Función para cargar datos con manejo de errores mejorado
@st.cache_data
def load_data():
    data = {}
    data_dir = "data"
    archivos_csv = [
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
    
    for archivo in archivos_csv:
        try:
            filepath = os.path.join(data_dir, archivo)
            # Verificar si el archivo existe antes de intentar cargarlo
            if os.path.exists(filepath):
                data[archivo.split('.')[0]] = pd.read_csv(filepath)
                st.success(f"✅ {archivo} cargado correctamente")
            else:
                st.warning(f"⚠️ Archivo no encontrado: {filepath}")
        except Exception as e:
            st.error(f"❌ Error al cargar {archivo}: {str(e)}")
    
    return data

# Cargar datos al iniciar la aplicación
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
                # Intentar mostrar imagen del actor/director
                try:
                    img_dir = "imagenes/imagenes_directores_actores"
                    actor_img = f"{row['actor_principal'].replace(' ', '_')}.jpg"
                    img_path = os.path.join(img_dir, actor_img)
                    if os.path.exists(img_path):
                        st.image(Image.open(img_path), width=150)
                    st.write(f"**{row['pelicula']}** ({row['vistas']} vistas)")
                except:
                    st.write(f"**{row['pelicula']}** ({row['vistas']} vistas)")

# Página de Visualizaciones
elif seleccion == "📊 Visualizaciones":
    st.header("Visualizaciones de Datos")
    
    # Selector de tipo de visualización
    viz_type = st.selectbox("Selecciona el tipo de visualización", [
        "Top 10 Películas Más Vistas",
        "Recaudación por Película",
        "Distribución de Vistas por País",
        "Premios vs. Calificación"
    ])
    
    if viz_type == "Top 10 Películas Más Vistas" and 'top_10_mas_vistas' in data:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x='vistas', y='pelicula', data=data['top_10_mas_vistas'], palette='viridis', ax=ax)
        ax.set_title('Top 10 Películas Más Vistas')
        ax.set_xlabel('Número de Vistas')
        ax.set_ylabel('Película')
        st.pyplot(fig)
    
    elif viz_type == "Recaudación por Película" and 'recaudacion_peliculas' in data:
        fig, ax = plt.subplots(figsize=(10, 6))
        top10 = data['recaudacion_peliculas'].nlargest(10, 'recaudacion')
        sns.barplot(x='recaudacion', y='pelicula', data=top10, palette='magma', ax=ax)
        ax.set_title('Top 10 Películas por Recaudación')
        ax.set_xlabel('Recaudación (en millones)')
        ax.set_ylabel('Película')
        st.pyplot(fig)

# Página de Recomendador
elif seleccion == "🎯 Recomendador":
    st.header("Sistema de Recomendación")
    
    with st.form("preferencias_form"):
        st.subheader("Configura tus preferencias")
        
        col1, col2 = st.columns(2)
        
        with col1:
            genero = st.selectbox("Género favorito", [
                "Todos", "Acción", "Aventura", "Comedia", "Drama", 
                "Ciencia Ficción", "Terror", "Romance", "Animación"
            ])
            año_min, año_max = st.slider(
                "Rango de años",
                1950, 2023, (2000, 2023)
        
        with col2:
            rating_min = st.slider("Rating mínimo", 1.0, 10.0, 7.0, step=0.5)
            duracion = st.selectbox("Duración preferida", [
                "Cualquiera", "Corta (<90 min)", "Media (90-120 min)", "Larga (>120 min)"
            ])
        
        submitted = st.form_submit_button("Generar Recomendaciones")
    
    if submitted:
        try:
            # Usar tu módulo de recomendación si está disponible
            if 'recomendar_peliculas' in globals():
                recomendaciones = recomendar_peliculas(
                    data, genero, (año_min, año_max), rating_min, duracion)
            else:
                # Implementación de respaldo
                if 'peliculas_completas' in data:
                    filtro = data['peliculas_completas'].copy()
                    if genero != "Todos":
                        filtro = filtro[filtro['genero'].str.contains(genero, case=False)]
                    filtro = filtro[(filtro['año'] >= año_min) & (filtro['año'] <= año_max)]
                    filtro = filtro[filtro['rating'] >= rating_min]
                    
                    if duracion == "Corta (<90 min)":
                        filtro = filtro[filtro['duracion'] < 90]
                    elif duracion == "Media (90-120 min)":
                        filtro = filtro[(filtro['duracion'] >= 90) & (filtro['duracion'] <= 120)]
                    elif duracion == "Larga (>120 min)":
                        filtro = filtro[filtro['duracion'] > 120]
                    
                    recomendaciones = filtro.sort_values('rating', ascending=False).head(5)
                else:
                    recomendaciones = None
            
            if recomendaciones is not None and not recomendaciones.empty:
                st.success("🎉 Recomendaciones generadas con éxito!")
                
                cols = st.columns(3)
                for idx, (_, row) in enumerate(recomendaciones.iterrows()):
                    with cols[idx % 3]:
                        st.subheader(row['titulo'])
                        try:
                            img_dir = "imagenes/imagenes_directores_actores"
                            # Intentar mostrar imagen del director/actor principal
                            director_img = f"{row['director'].replace(' ', '_')}.jpg"
                            img_path = os.path.join(img_dir, director_img)
                            if os.path.exists(img_path):
                                st.image(Image.open(img_path), width=200)
                            else:
                                actor_img = f"{row['actor_principal'].replace(' ', '_')}.jpg"
                                img_path = os.path.join(img_dir, actor_img)
                                if os.path.exists(img_path):
                                    st.image(Image.open(img_path), width=200)
                        except:
                            pass
                        
                        st.write(f"**Director:** {row.get('director', 'N/A')}")
                        st.write(f"**Año:** {row.get('año', 'N/A')}")
                        st.write(f"**Rating:** {row.get('rating', 'N/A')}/10")
                        st.write(f"**Duración:** {row.get('duracion', 'N/A')} min")
            else:
                st.warning("No se encontraron películas que coincidan con tus criterios.")
        
        except Exception as e:
            st.error(f"Error al generar recomendaciones: {str(e)}")

# Página Acerca De
elif seleccion == "ℹ️ Acerca De":
    st.header("Acerca de Este Proyecto")
    st.write("""
    ### Sistema de Recomendación de Películas
    
    Este proyecto fue desarrollado para analizar datos cinematográficos y proporcionar
    recomendaciones personalizadas basadas en las preferencias del usuario.
    
    **Características principales:**
    - Visualización de datos de películas
    - Sistema de recomendación personalizado
    - Análisis de tendencias cinematográficas
    
    **Tecnologías utilizadas:**
    - Python 🐍
    - Streamlit 🎈
    - Pandas 🐼
    - Matplotlib/Seaborn 📊
    
    **Datos incluidos:**
    - Información de más de 500 películas
    - Datos de actores y directores
    - Recaudación y calificaciones
    """)

# Mostrar estructura de archivos en el sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("Estructura del Proyecto")
st.sidebar.code("""
peliculas_proyecto/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   ├── actores_directores.csv
│   ├── actores_directores_peliculas.csv
│   ├── comentarios_peliculas.csv
│   ├── mapa_peliculas.csv
│   ├── peliculas_completas.csv
│   ├── peliculas_premios.csv
│   ├── recaudacion_peliculas.csv
│   ├── top_10_mas_vistas.csv
│   ├── top_10_mejor_puntuadas.csv
│   ├── vistas_por_pais.csv
│   └── vistas_por_pais_con_coords.csv
├── imagenes/
│   └── imagenes_directores_actores/
│       ├── Antonio_Banderas.jpg
│       ├── ... (más imágenes)
└── utils/
    ├── recomendador.py
    └── visualizaciones.py
""")

# Footer
st.markdown("---")
st.markdown("© 2023 Sistema de Recomendación de Películas")
