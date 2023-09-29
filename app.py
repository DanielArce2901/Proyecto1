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
        opcionInicio = st.selectbox('¿Seleccione lo que desea consultar?', ["Buscar Investigador", "Buscar Proyecto","Buscar Publicacion","Buscar area de conocimiento","Busqueda por Colegas"])
        if (opcionInicio=="Buscar Investigador"):
            investigador=recuperar_Investigadores_para_visualizar()
            with investigador:
                try:
                    inv=recuperar_Investigadores_para_visualizar()
                    opciones=[]
                    for a in inv:
                        opciones.append(a)
                    seleccion = st.selectbox("Selecciona una opción:", opciones)

                    #conseguir los datos de la persona
                    perfil=[]


                    # Cuadros de texto para capturar datos
                    st.write("ID:",perfil[3])
                    st.write("Nombre:",perfil[0])
                    st.write("Institución:",perfil[1])
                    st.write("Título:",perfil[2])
                    st.write("Email:",perfil[4])
                    
                    data = {
                        'Titulo':general[0],
                        'Duracion meses':general[1],
                        'Area de Conocimiento':general[2],
                        'Año':general[3],
                        'ID':general[4]
                    }

                    df = pd.DataFrame(data)
                    # Título de la aplicación
                    st.title("Proyectos de Investigador")
                    # Mostrar el DataFrame en Streamlit
                    st.dataframe(df)
                    
                except:
                    st.warning("No hay datos cargados")


        if (opcionInicio=="Buscar Proyecto"):
            proyecto=recuperar_proyectos_para_visualizar()
            with proyecto:
                try:
                    inv=recuperar_proyectos_para_visualizar()
                    opciones=[]
                    for a in inv:
                        opciones.append(a)
                    seleccion = st.selectbox("Selecciona una opción:", opciones)

                    #conseguir los datos de la persona
                    perfil=[]

                    # Cuadros de texto para capturar datos
                    st.write("ID:",perfil[4])
                    st.write("Titulo:",perfil[0])
                    st.write("Meses:",perfil[1])
                    st.write("Area de conocimiento:",perfil[2])
                    st.write("Año:",perfil[3])

                    
                    data = {
                        'ID':general[4],
                        'Nombre':general[0],
                        'Titulo academico':general[1],
                        'Institucion':general[2],
                        'Email':general[3]
                    }

                    

                    df = pd.DataFrame(data)
                    # Título de la aplicación
                    st.title("Investigadores del Proyecto")
                    # Mostrar el DataFrame en Streamlit
                    st.dataframe(df)
                    

                    # Título 2
                    st.title("Publicaciones del Proyecto")
                    # Mostrar el DataFrame en Streamlit
                    st.dataframe(df_2)

                except:
                    st.warning("No hay datos cargados")


        if (opcionInicio=="Buscar Publicacion"):
            publicacion=recuperar_Publicaciones_para_visualizar()
            with publicacion:
                try:
                    inv=recuperar_Publicaciones_para_visualizar()
                    opciones=[]
                    for a in inv:
                        opciones.append(a)
                    seleccion = st.selectbox("Selecciona una opción:", opciones)

                    #conseguir los datos de la persona
                    perfil=[]

                    # Cuadros de texto para capturar datos
                    st.write("ID:",perfil[2])
                    st.write("Titulo:",perfil[0])
                    st.write("Nombre:",perfil[1])
                    st.write("Año:",perfil[3])
                    general=recuperar_Publicaciones_para_visualizar()
                    st.write("Proyecto Asociado:",general[0])

                except:
                    st.warning("No hay datos cargados")

        if (opcionInicio=="Buscar area de conocimiento"):
                try:
                    inv=retornar_areas_conocimiento()
                    opciones=[]
                    for a in inv:
                        opciones.append(a)
                    seleccion = st.selectbox("Selecciona una opción:", opciones)
                    
                    st.write("Area de conocimiento: ",seleccion)
                    #general=cc.retornar_proyectos_conocimiento(seleccion)
                    #general_2=cc.retornar_articulos_conocimiento(seleccion)
                    data = {
                        'Titulos Proyectos':general,
                    }

                    data2 = {
                        #'Titulos Articulos':general_2,
                    }
                    df = pd.DataFrame(data)
                    df_2= pd.DataFrame(data2)
                    
                    # Título de la aplicación
                    st.write("Proyectos del area de conocimiento")
                    # Mostrar el DataFrame en Streamlit
                    st.dataframe(df)

                    # Título 2
                    st.write("Articulos del area de conocimiento")
                    # Mostrar el DataFrame en Streamlit
                    st.dataframe(df_2)

                except:
                    st.warning("No hay datos cargados")

        if (opcionInicio=="Busqueda por Colegas"):
           # with area:
                try:
                    inv=recuperar_Investigadores_para_visualizar()
                    opciones=[]
                    for a in inv:
                        opciones.append(a)
                    seleccion = st.selectbox("Selecciona una opción:", opciones)
                    
                    st.write("ID:",general[3])
                    st.write("Nombre:",general[0])
                    st.write("Institución:",general[1])
                    st.write("Título:",general[2])
                    st.write("Email:",general[4])

                    data = {
                        #'Nombre Colegas':general_2
                    }
                    df = pd.DataFrame(data)                
                    # Título de la aplicación
                    st.title("Colegas")
                    # Mostrar el DataFrame en Streamlit
                    st.dataframe(df)
                            
                except:
                    st.warning("No hay datos cargados")
        
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
                #registrarInvestigador(base)
                st.write("Proyectos:")
            
            elif operacion == "Actualizar":
                #modificarInvestigador(base)
                st.write("Proyectos:")
                
            
            elif operacion == "Visualizar":
                #mostrarInvestigador(base)
                st.write("Proyectos:")
            
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
