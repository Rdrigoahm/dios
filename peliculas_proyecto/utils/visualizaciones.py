# utils/visualizaciones.py
import streamlit as st
import pandas as pd
from PIL import Image
import os

def mostrar_top_peliculas(df):
    st.header("📊 Películas más vistas y mejor puntuadas")

    top_vistas = df.sort_values("votos", ascending=False).head(10)
    top_puntuadas = df[df["votos"] >= 100].sort_values("puntuacion", ascending=False).head(10)

    st.subheader("🎥 Top 10 más vistas")
    st.dataframe(top_vistas[["titulo", "año", "votos"]])

    st.subheader("🏆 Top 10 mejor puntuadas")
    st.dataframe(top_puntuadas[["titulo", "año", "puntuacion", "votos"]])

def mostrar_actores_directores(df):
    st.header("👤 Actores y Directores de las Mejores Películas")

    top_puntuadas = df[df["votos"] >= 100].sort_values("puntuacion", ascending=False).head(10)

    for _, row in top_puntuadas.iterrows():
        st.subheader(f"{row['titulo']} ({row['año']})")
        cols = st.columns(2)

        actores = row["actores"].split(", ")
        directores = row["directores"].split(", ")

        with cols[0]:
            st.markdown("🎭 **Actores**")
            for actor in actores:
                ruta = f"imagenes/directores_actores/{actor.replace(' ', '_')}.jpg"
                if os.path.exists(ruta):
                    st.image(ruta, width=120, caption=actor)
                else:
                    st.markdown(f"- {actor}")

        with cols[1]:
            st.markdown("🎬 **Directores**")
            for director in directores:
                ruta = f"imagenes/directores_actores/{director.replace(' ', '_')}.jpg"
                if os.path.exists(ruta):
                    st.image(ruta, width=120, caption=director)
                else:
                    st.markdown(f"- {director}")
