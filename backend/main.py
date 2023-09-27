import pandas as pd
from io import StringIO
from backend.database import crear_nodos_en_neo4j
#Hola

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