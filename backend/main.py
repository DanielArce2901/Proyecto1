import pandas as pd
from io import StringIO
from backend.database import crear_nodos_en_neo4j
from backend.database import crear_nodo
from py2neo import Graph, Node
#Hola
#cuanto cuestas mamacita?

def procesar_archivos(uploaded_files):
    nodos = []
    for uploaded_file in uploaded_files:
        if uploaded_file is not None:
            # Leer el contenido del archivo CSV
            csv_content = uploaded_file.read().decode("utf-8")
            
            # Crear un archivo temporal en memoria a partir del contenido
            csv_file = StringIO(csv_content)
            
            # Determinar el tipo de nodo
            filename = uploaded_file.name
            node_type = filename.split(".")[0]
            
            # Preparar los datos
            df = pd.read_csv(csv_file, skipinitialspace=True)
            for _, row in df.iterrows():
                nodo = {"tipo": node_type}
                for col in df.columns:
                    nodo[col] = row[col]
                nodos.append(nodo)
    crear_nodos_en_neo4j(nodos)
    return nodos

def crear_nodo_publicaciones(titulo_publicacion, nombre_revista, anno_publicacion):
    # Crea un nodo de tipo "Publicaciones" con las propiedades especificadas
    nodo = Node("Publicaciones",
                titulo_publicacion= titulo_publicacion,
                nombre_revista= nombre_revista,
                anno_publicacion= anno_publicacion)
    crear_nodo(nodo)
    return nodo

    
