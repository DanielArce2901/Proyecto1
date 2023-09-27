import streamlit as st
from backend.main import procesar_archivos
from backend.main import procesar_relaciones,procesar_relaciones_entre_publ_Proy

from backend.database import verificar_proyecto_existente,crear_proyecto,actualizar_proyecto,visualizar_proyectos

from backend.main import crear_nodo_publicaciones


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
                st.success("Los datos se han cargado correctamente en Neo4j.")
            else:
                st.warning("Por favor, suba los archivos CSV primero.")
                
    elif choice == "Gestión de Datos":
        st.subheader("Sección de Gestión de Datos")
        
        # Crear el submenú para Gestión de Datos
        gestion_menu = ["CRUD 1", "CRUD 2", "Gestión de proyectos", "Asociar Investigador", "Asociar Artículo"]
        gestion_choice = st.sidebar.selectbox("Gestión de Datos", gestion_menu)
        
        if gestion_choice == "CRUD 1":

            st.subheader("CRUD 1")
            # Aquí puedes agregar el código para manejar el CRUD 1.

            st.subheader("Crear publicacion")
            titulo = st.text_input("Ingrese Titulo")
            nombre = st.text_input("Ingrese el Nombre")
            anoPublicacion  = st.text_input("Ingrese el ano")
            if st.button("Crear publicacion"):
                 if(titulo and nombre and anoPublicacion):
                     crear_nodo_publicaciones(titulo, nombre, anoPublicacion)
                     st.success("Se agrego la publicacion")
                 else:
                     st.warning("Faltan datos")

            
        elif gestion_choice == "CRUD 2":
            st.subheader("CRUD 2")
            # Aquí puedes agregar el código para manejar el CRUD 2.
            
        elif gestion_choice == "Gestión de proyectos":
            st.subheader("Proyectos")
            
            # Opción de selección para Crear, Actualizar o Visualizar proyectos
            operacion = st.selectbox("Seleccione una operación:", ["Crear", "Actualizar", "Visualizar"])
            
            if operacion == "Crear":
                proyecto_data = {
                    "idPry": st.number_input("ID del Proyecto:", format="%d", value=0, step=1),
                    "titulo_proyecto": st.text_input("Título del Proyecto:"),
                    "anno_inicio": st.number_input("Año de Inicio:", format="%d", value=0, step=1),
                    "duracion_meses": st.number_input("Duración en Meses:", format="%d", value=0, step=1),
                    "area_conocimiento": st.text_input("Área de Conocimiento:")
                }
                idPry = int(proyecto_data["idPry"])
                if idPry:  # Verificar si el usuario ha ingresado un ID del proyecto
                    verificador=verificar_proyecto_existente(idPry)
                    if  verificador==True:
                        st.warning("El proyecto con este ID ya existe en la base de datos.")
                    else:
                        if st.button("Crear Proyecto"):
                            crear_proyecto(proyecto_data)
                            st.success("Proyecto creado exitosamente.")
            
            elif operacion == "Actualizar":
                idPry = st.number_input("ID del Proyecto a Actualizar:",format="%d", value=0, step=1)
                idPry=int(idPry)
                if idPry:
                    verificador=verificar_proyecto_existente(idPry)
                    if verificador==True:
                        proyecto_data = {
                            "titulo_proyecto": st.text_input("Nuevo Título del Proyecto:"),
                            "anno_inicio": st.number_input("Nuevo Año de Inicio:", format="%d", value=0, step=1),
                            "duracion_meses": st.number_input("Nueva Duración en Meses:", format="%d", value=0, step=1),
                            "area_conocimiento": st.text_input("Nueva Área de Conocimiento:")
                        }
                        if st.button("Actualizar Proyecto"):
                            actualizar_proyecto(idPry, proyecto_data)
                            st.success("Proyecto actualizado exitosamente.")
                    else:
                        st.error("El proyecto con este ID no existe en la base de datos.")
            
            elif operacion == "Visualizar":
                # Aquí puedes añadir el código para visualizar los proyectos
                st.write("Visualizar Proyectos")

                        
            
        elif gestion_choice == "Asociar Investigador":
            st.subheader("Asociar Investigador a un proyecto")
            uploaded_files = st.file_uploader("Subir archivos CSV", type=["csv"], accept_multiple_files=True)
            if st.button("Cargar Datos"):
                if uploaded_files:
                    procesar_relaciones(uploaded_files)  # Cargar nodos primero
                    st.success("Los datos se han cargado correctamente en Neo4j.")
                else:
                    st.warning("Por favor, suba los archivos CSV primero.")
            
        elif gestion_choice == "Asociar Artículo":
            st.subheader("Asociar Artículo")
            uploaded_files = st.file_uploader("Subir archivos CSV", type=["csv"], accept_multiple_files=True)
            if st.button("Cargar Datos"):
                if uploaded_files:
                    procesar_relaciones_entre_publ_Proy(uploaded_files)  # Cargar nodos primero
                    st.success("Los datos se han cargado correctamente en Neo4j.")
                else:
                    st.warning("Por favor, suba los archivos CSV primero.")
            
if __name__ == "__main__":
    main()
