import streamlit as st
import pandas as pd
from backend.main import procesar_archivos
from backend.main import procesar_relaciones,procesar_relaciones_entre_publ_Proy
from Investigador import Investigador
from backend.database import *
from CRUDInvestigador import *
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

            st.subheader("Publicaciones")
            # Aquí puedes agregar el código para manejar el CRUD 1.
            opcion= st.selectbox("Seleccione la opcion:", ["Crear","Actualizar", "Visualizar"])

            if opcion == "Crear":
                datos = {
                    "idPub": st.number_input("ID de la publicacion:", format= "%d", value=0, step = 1),
                    "titulo_publicacion": st.text_input("Titulo de la publicacion"),
                    "nombre_revista": st.text_input("Nombre de la revista"),
                    "anno_publicacion": st.number_input("Año de publicacion:", format= "%d", value=0, step = 1)
                }
                idPub = int(datos["idPub"])
                if idPub:  # Verificar si el usuario ha ingresado un ID del proyecto
                    verificador=verificar_publicaciones_existente(idPub)
                    if  verificador==True:
                        st.warning("Ya existe una publicacion con ese ID.")
                    else:
                        if st.button("Crear Publicacion"):
                            crear_publicacion(datos)
                            st.success("Publicacion creada")

            elif opcion == "Actualizar":

                idPub = st.number_input("ID de la publicacion:", format= "%d", value=0, step = 1)
                idPub = int(idPub)
                if idPub:
                    verificador = verificar_publicaciones_existente(idPub)
                    if verificador == True:
                        datos = {
                        "titulo_publicacion": st.text_input("Titulo de la publicacion"),
                        "nombre_revista": st.text_input("Nombre de la revista"),
                        "anno_publicacion": st.number_input("Año publicacion", format= "%d", value=0, step = 1)
                        }
                        if st.button("actualizar publicacion"):
                            actualizar_publicacion(idPub, datos)
                            st.success("Actualizacion realizada")
                    else:
                        st.warning("No se encontro el ID")
            
            elif opcion == "Visualizar":
                st.subheader("Publicaciones almacenadas")
                if st.button("Mostrar publicaciones"):
                    resultados = obtener_nodos()
                    for resultado in resultados:
                        nodo = resultado["n"]
                        st.write("ID:", nodo.identity, "Propiedades:",dict(nodo))

            
        elif gestion_choice == "CRUD 2":
            st.subheader("CRUD 2")
            operacion = st.selectbox("Seleccione una operación:", ["Crear", "Actualizar", "Visualizar"])
            
            if operacion == "Crear":
                registrarInvestigador(base)
            
            elif operacion == "Actualizar":
                modificarInvestigador(base)
            
            elif operacion == "Visualizar":
                mostrarInvestigador(base)
            
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
                            if proyecto_data["titulo_proyecto"] and proyecto_data["area_conocimiento"]:
                                crear_proyecto(proyecto_data)
                                st.success("Proyecto creado exitosamente.")
                            else:
                                st.warning("Faltan datos.")
            
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
                st.write("Proyectos:")
                proyectos = recuperar_proyectos_para_visualizar()
                print (proyectos)
                df_proyectos = pd.DataFrame(proyectos)
                df_proyectos.rename(columns={
                    'anno_inicio': 'Año de Inicio',
                    'area_conocimiento': 'Área de Conocimiento',
                    'duracion_meses': 'Duración (meses)',
                    'idPry': 'ID del Proyecto',
                    'titulo_proyecto': 'Título del Proyecto'
                }, inplace=True)
                st.title('Lista de Proyectos')
                st.table(df_proyectos)

                        
            
        elif gestion_choice == "Asociar Investigador":
            st.subheader("Asociar Investigador a un proyecto")
            uploaded_files = st.file_uploader("Subir archivos CSV", type=["csv"], accept_multiple_files=True)
            if st.button("Cargar relaciones"):
                if uploaded_files:
                    procesar_relaciones(uploaded_files)  # Cargar nodos primero
                    st.success("Los datos se han cargado correctamente en Neo4j.")
                else:
                    st.warning("Por favor, suba los archivos CSV primero.")
            
        elif gestion_choice == "Asociar Artículo":
            st.subheader("Asociar Artículo")
            uploaded_files = st.file_uploader("Subir archivos CSV", type=["csv"], accept_multiple_files=True)
            if st.button("Cargar relaciones"):
                if uploaded_files:
                    procesar_relaciones_entre_publ_Proy(uploaded_files)  # Cargar nodos primero
                    st.success("Los datos se han cargado correctamente en Neo4j.")
                else:
                    st.warning("Por favor, suba los archivos CSV primero.")
            
if __name__ == "__main__":
    main()
