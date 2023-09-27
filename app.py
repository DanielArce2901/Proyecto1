import streamlit as st
from backend.main import procesar_archivos

def main():
    st.title("Proyecto 1 Bases de datos Avanzadas")
    
    # Crear el menú principal
    menu = ["Consultas", "Subir Datos", "Gestión de Datos"]
    choice = st.sidebar.selectbox("Menú", menu)
    
    if choice == "Consultas":
        st.subheader("Sección de Consultas")
        # Aquí puedes agregar el código para manejar las consultas.
        
    elif choice == "Subir Datos":
        st.subheader("Sección para Subir Datos")
        uploaded_files = st.file_uploader("Subir archivos CSV", type=["csv"], accept_multiple_files=True)
        
        if st.button("Cargar Datos"):
            if uploaded_files:
                procesar_archivos(uploaded_files)  # Cargar nodos primero
                #crear_relaciones(uploaded_files)  # Luego crear relaciones
                st.success("Los datos se han cargado correctamente en Neo4j.")
            else:
                st.warning("Por favor, suba los archivos CSV primero.")
                
    elif choice == "Gestión de Datos":
        st.subheader("Sección de Gestión de Datos")
        
        # Crear el submenú para Gestión de Datos
        gestion_menu = ["CRUD 1", "CRUD 2", "CRUD 3", "Asociar Investigador", "Asociar Artículo"]
        gestion_choice = st.sidebar.selectbox("Gestión de Datos", gestion_menu)
        
        if gestion_choice == "CRUD 1":
            st.subheader("Crear publicacion")
            titulo = st.text_input("Ingrese Titulo")
            nombre = st.text_input("Ingrese el Nombre")
            anoPublicacion  = st.text_input("Ingrese el ano")
            if(titulo and nombre and anoPublicacion):
                st.write("Titulo:",titulo,"\n", "Nombre:", nombre,"\n", "Ano publicacion:",anoPublicacion)

        elif gestion_choice == "CRUD 2":
            st.subheader("CRUD 2")
            # Aquí puedes agregar el código para manejar el CRUD 2.
            
        elif gestion_choice == "CRUD 3":
            st.subheader("CRUD 3")
            # Aquí puedes agregar el código para manejar el CRUD 3.
            
        elif gestion_choice == "Asociar Investigador":
            st.subheader("Asociar Investigador")
            # Aquí puedes agregar el código para manejar la asociación de investigadores.
            
        elif gestion_choice == "Asociar Artículo":
            st.subheader("Asociar Artículo")
            # Aquí puedes agregar el código para manejar la asociación de artículos.
            
if __name__ == "__main__":
    main()
