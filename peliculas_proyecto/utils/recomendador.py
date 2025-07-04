# utils/recomendador.py
import streamlit as st

def mostrar_quiz_recomendacion(df):
    st.header("🎯 Recomendación personalizada")

    genero = st.selectbox("¿Qué género prefieres?", df["genero"].explode().unique())
    duracion_max = st.slider("Duración máxima (min)", 60, 240, 120)
    plataforma = st.selectbox("¿Dónde quieres verla?", df["donde_ver"].unique())

    filtradas = df[
        (df["genero"].apply(lambda g: genero in g)) &
        (df["duracion"] <= duracion_max) &
        (df["donde_ver"] == plataforma)
    ]

    if not filtradas.empty:
        st.success(f"Se encontraron {len(filtradas)} películas que coinciden:")
        for _, row in filtradas.iterrows():
            st.markdown(f"**🎬 {row['titulo']} ({row['año']})** - {row['duracion']} min")
    else:
        st.warning("No se encontraron coincidencias con tus preferencias.")
