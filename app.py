import streamlit as st
from py2neo import Graph, Node, Relationship
import pandas as pd
from io import StringIO
from neo4j import GraphDatabase
from backend.main import procesar_archivos


def main():
    st.title("Proyecto 1 Bases de datos Avanzadas")
    uploaded_files = st.file_uploader("Subir archivos CSV", type=["csv"], accept_multiple_files=True)
    
    if st.button("Cargar Datos"):
        if uploaded_files:
            procesar_archivos(uploaded_files)  # Cargar nodos primero
            #crear_relaciones(uploaded_files)  # Luego crear relaciones
            st.success("Los datos se han cargado correctamente en Neo4j.")
        else:
            st.warning("Por favor, suba los archivos CSV primero.")

    # Agrega aquí las opciones para analizar las relaciones entre investigadores, proyectos y publicaciones.

if __name__ == "__main__":
    main()