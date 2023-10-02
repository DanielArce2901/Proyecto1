import streamlit as st
import pandas as pd
from backend.database import *
import streamlit as st

#______________________________Personalizar interfaz_________________________




def main():
    st.title("Proyecto 1 Bases de datos Avanzadas")
    
    # Crear el menú principal
    menu = ["Subir Datos","Consultas", "Gestión de Datos"]
    choice = st.sidebar.selectbox("Menú", menu)
    if choice == "Subir Datos":
        st.subheader("Sección para Subir Datos")
        tipo_nodo = st.selectbox("Seleccione el tipo de nodo:", ["Proyectos", "Publicaciones", "Investigadores"])
        
        estructuras_validas = {
            "Proyectos": {"idPry", "titulo_proyecto", "anno_inicio", "duracion_meses", "area_conocimiento"},
            "Publicaciones": {"idPub", "titulo_publicacion", "anno_publicacion", "nombre_revista"},
            "Investigadores": {"id","nombre_completo","titulo_academico","institucion","email"}
        }
        
        uploaded_files = st.file_uploader(f"Subir archivos CSV para {tipo_nodo}", type=["csv"], accept_multiple_files=True)
        
        if st.button("Cargar Nodos"):
            if uploaded_files:
                for uploaded_file in uploaded_files:
                    # Leer el archivo CSV y convertirlo en un DataFrame
                    df = pd.read_csv(uploaded_file)
                    
                    # Verificar si el DataFrame tiene las columnas correctas
                    if set(df.columns) != estructuras_validas[tipo_nodo]:
                        st.error(f"El archivo {uploaded_file.name} no tiene las columnas correctas para {tipo_nodo}.")
                        continue 
                    procesar_archivos(df, tipo_nodo)
                    st.success(f"Los nodos de {tipo_nodo} del archivo {uploaded_file.name} se han cargado correctamente en Neo4j.")
            else:
                st.warning("Por favor, suba los archivos CSV primero.")
    if existe_nodo('Proyectos') and existe_nodo('Publicaciones') and existe_nodo('Investigadores'):
        if choice == "Consultas":
            st.subheader("Sección de Consultas")
            opcionInicio = st.selectbox('¿Seleccione lo que desea consultar?', ["Top 5 de áreas de conocimiento","Top 5 de instituciones","Top 5 investigadores(as)", "Buscar Investigador", "Buscar Proyecto","Buscar Publicacion","Buscar area de conocimiento","Busqueda por Colegas"])
            investigador=recuperar_investigadores_para_visualizar()
            df_investigador = pd.DataFrame(investigador)
            proyecto=recuperar_proyectos_para_visualizar()
            df_proyecto = pd.DataFrame(proyecto)
            publicacion=recuperar_Publicaciones_para_visualizar()
            df_publicacion = pd.DataFrame(publicacion)

            # Consulta 1
            if (opcionInicio=="Top 5 de áreas de conocimiento"):
                    st.title('Top 5 de áreas de conocimiento con la mayor cantidad de investigaciones')
                    data = obtener_top_areas_conocimiento()
                    df = pd.DataFrame(data, columns=["Área de Conocimiento", "Cantidad de Proyectos"])
                    st.dataframe(df)

            # Consulta 2
            if (opcionInicio=="Top 5 de instituciones"):
                    st.title("Top 5 de Instituciones con la Mayor Cantidad de Investigaciones")
                    data = obtener_top_instituciones()
                    df = pd.DataFrame(data, columns=["Institución", "Cantidad de Investigaciones"])
                    st.dataframe(df)

            # Consulta 3
            if (opcionInicio=="Top 5 investigadores(as)"):
                    st.title('Top 5 de Investigadores con la Mayor Cantidad de Investigaciones')
                    # Obtener los datos de los investigadores
                    data = obtener_top_investigadores()
                    df = pd.DataFrame(data, columns=["Nombre del Investigador", "Institución", "Cantidad de Proyectos"])
                    st.dataframe(df)

            # Consulta 4
            if (opcionInicio=="Buscar Investigador"):
                    st.title('Búsqueda de un Investigador')
                    relacion_inv_pry=recuperar_relaciones_proyectos_investigadores()
                    df_relacion_inv_pry= pd.DataFrame(relacion_inv_pry)
                    data = []
                    for item in relacion_inv_pry:
                        investigador = item['investigador']
                        proyecto = item['proyecto']
                        data.append({
                            'id': investigador['id'],
                            'idPry': proyecto['idPry'],
                            'nombre_completo': investigador['nombre_completo'],
                            'email': investigador['email'],
                            'institucion': investigador['institucion'],
                            'titulo_academico': investigador['titulo_academico'],
                            'titulo_proyecto': proyecto['titulo_proyecto'],
                            'anno_inicio': proyecto['anno_inicio'],
                            'area_conocimiento': proyecto['area_conocimiento'],
                            'duracion_meses': proyecto['duracion_meses'],
                        })

                    df_relacion_inv_pry = pd.DataFrame(data)
                    # Crear un widget de selección con los nombres de los investigadores
                    selected_investigator = st.selectbox('Selecciona un investigador:', df_investigador['nombre_completo'].tolist())
                    
                    # Filtrar el DataFrame de investigadores basado en la selección del usuario
                    selected_investigator_data = df_investigador[df_investigador['nombre_completo'] == selected_investigator]
                    
                    # Mostrar los datos del investigador seleccionado
                    st.subheader('Datos del Investigador Seleccionado')
                    st.write(selected_investigator_data)
                    
                    # Verificar si df_relacion_inv_pry está vacío
                    if not df_relacion_inv_pry.empty:
                        # Obtener y mostrar los proyectos asociados al investigador seleccionado
                        st.subheader('Proyectos Asociados')
                        proyectos_ids = df_relacion_inv_pry[df_relacion_inv_pry['id'] == selected_investigator_data.iloc[0]['id']]['idPry'].tolist()
                        proyectos_asociados = df_proyecto[df_proyecto['idPry'].isin(proyectos_ids)]
                        st.write(proyectos_asociados)
                    else:
                        st.warning('Este investigador no está asociado a ningún proyecto.')

            # Consulta 5

            if (opcionInicio=="Buscar Proyecto"):
                    st.title('Búsqueda de un Proyecto')
                    relacion_inv_pry=recuperar_relaciones_proyectos_investigadores()
                    df_relacion_inv_pry= pd.DataFrame(relacion_inv_pry)
                    data = []
                    for item in relacion_inv_pry:
                        investigador = item['investigador']
                        proyecto = item['proyecto']
                        data.append({
                            'id': investigador['id'],
                            'idPry': proyecto['idPry'],
                            'nombre_completo': investigador['nombre_completo'],
                            'email': investigador['email'],
                            'institucion': investigador['institucion'],
                            'titulo_academico': investigador['titulo_academico'],
                            'titulo_proyecto': proyecto['titulo_proyecto'],
                            'anno_inicio': proyecto['anno_inicio'],
                            'area_conocimiento': proyecto['area_conocimiento'],
                            'duracion_meses': proyecto['duracion_meses'],
                        })

                    df_relacion_inv_pry = pd.DataFrame(data)



                    # Crear un widget de selección con los nombres de los proyectos
                    selected_project = st.selectbox('Selecciona un proyecto:', df_proyecto['titulo_proyecto'].tolist())

                    # Filtrar el DataFrame de proyectos basado en la selección del usuario
                    selected_project_data = df_proyecto[df_proyecto['titulo_proyecto'] == selected_project]

                    # Mostrar los datos del proyecto seleccionado
                    st.subheader('Datos del Proyecto Seleccionado')
                    st.write(selected_project_data)
                    if not df_relacion_inv_pry.empty:
                        # Obtener y mostrar los investigadores asociados al proyecto seleccionado
                        st.subheader('Investigadores Asociados')
                        investigadores_ids = df_relacion_inv_pry[df_relacion_inv_pry['idPry'] == selected_project_data.iloc[0]['idPry']]['id'].tolist()
                        investigadores_asociados = df_investigador[df_investigador['id'].isin(investigadores_ids)]
                        st.write(investigadores_asociados)
                    else:
                        st.warning('No hay investigadores asociados a este proyecto.')

            # Consulta 6

            if (opcionInicio=="Buscar Publicacion"):
                    st.title('Búsqueda de una Publicación')
                    relacion_plu_pry=recuperar_relaciones_proyectos_publicaciones()
                    df_relacion_plu_pry= pd.DataFrame(relacion_plu_pry)
                    # Crear un DataFrame para las relaciones entre proyectos y publicaciones
                    data = []
                    for item in relacion_plu_pry:
                        publicacion = item['publicacion']
                        proyecto = item['proyecto']
                        data.append({
                            'idPub': publicacion['idPub'],
                            'idPry': proyecto['idPry'],
                            'titulo_publicacion': publicacion['titulo_publicacion'],
                            'fecha_publicacion': publicacion['fecha_publicacion'],
                            'resumen': publicacion['resumen'],
                            'palabras_clave': publicacion['palabras_clave'],
                            'titulo_proyecto': proyecto['titulo_proyecto'],
                            'anno_inicio': proyecto['anno_inicio'],
                            'area_conocimiento': proyecto['area_conocimiento'],
                            'duracion_meses': proyecto['duracion_meses'],
                        })

                    df_relacion_plu_pry = pd.DataFrame(data)

                    # Crear un widget de selección con los títulos de las publicaciones
                    selected_publications = st.multiselect('Selecciona una o más publicaciones:', df_publicacion['titulo_publicacion'].tolist())

                    for selected_publication in selected_publications:
                        # Filtrar el DataFrame de publicaciones basado en la selección del usuario
                        selected_publication_data = df_publicacion[df_publicacion['titulo_publicacion'] == selected_publication]

                        # Mostrar los datos de la publicación seleccionada
                        st.subheader('Datos de la Publicación Seleccionada')
                        st.write(selected_publication_data)

                        if not df_relacion_plu_pry.empty:
                            # Obtener y mostrar los proyectos asociados a la publicación seleccionada
                            st.subheader('Proyecto Asociado')
                            proyectos_ids = df_relacion_plu_pry[df_relacion_plu_pry['idPub'] == selected_publication_data.iloc[0]['idPub']]['idPry'].tolist()
                            proyectos_asociados = df_proyecto[df_proyecto['idPry'].isin(proyectos_ids)]
                            st.write(proyectos_asociados)
                        else:
                            st.warning('No hay proyectos asociados a esta publicación.')

            # Consulta 7

            if opcionInicio == "Buscar area de conocimiento":
                    selected_area = st.selectbox("Selecciona un área de conocimiento", obtener_areas())
                    if st.button("Mostrar información"):
                        area_nombre, proyectos, publicaciones = obtener_informacion_area_conocimiento(selected_area)
                        # Mostrar la información en Streamlit
                        st.subheader("Información del área de conocimiento")
                        st.write("Nombre del área:", area_nombre)
                        st.subheader("Proyectos en esta área")
                        for resultado in proyectos:
                            st.write(resultado)
                        st.subheader("Publicaciones asociadas a proyectos en esta área")
                        for resultado in publicaciones:
                            st.write(resultado)

            # Consulta 8 

            if opcionInicio == "Busqueda por Colegas":
                    selected_investigador = st.selectbox("Selecciona el investigador", obtener_investigadores())
                    informacion, colegas = obtener_datos(selected_investigador)
                    if st.button("Mostrar información"):
                        st.subheader("Información del Investigador")
                        st.markdown( f'<p style="color:white;">ID: {informacion["id"]}</p>',unsafe_allow_html=True)
                        st.write("Nombre completo:", informacion["nombre"])
                        st.write("Título académico:", informacion["titulo"])
                        st.write("Institución:", informacion["institucion"])
                        st.markdown( f'<p style="color:white;">Correo: {informacion["correo"]}</p>',unsafe_allow_html=True)

                        st.subheader("Colegas con los que ha trabajado en proyectos de investigación")
                        for colega in colegas:
                            st.write(colega)

        elif choice == "Gestión de Datos":
            st.subheader("Sección de Gestión de Datos")
            
            # Crear el submenú para Gestión de Datos
            gestion_menu = ["Gestion de Publicaciones", "Gestion de Investigadores", "Gestión de proyectos", "Asociar Investigador", "Asociar Artículo"]
            gestion_choice = st.sidebar.selectbox("Gestión de Datos", gestion_menu)
            
            if gestion_choice == "Gestion de Publicaciones":

                st.subheader("Publicaciones")
                # Aquí puedes agregar el código para manejar el CRUD 1.
                opcion= st.selectbox("Seleccione la opcion:", ["Crear","Actualizar", "Visualizar"])

                if opcion == "Crear":
                    publicaciones_data = {
                        "idPub": st.number_input("ID de la publicacion:", format= "%d", value=0, step = 1),
                        "titulo_publicacion": st.text_input("Titulo de la publicacion"),
                        "nombre_revista": st.text_input("Nombre de la revista"),
                        "anno_publicacion": st.number_input("Año de publicacion:", format= "%d", value=0, step = 1)
                    }
                    idPub = int(publicaciones_data["idPub"])
                    if idPub:  # Verificar si el usuario ha ingresado un ID del proyecto
                        verificador=verificar_publicaciones_existente(idPub)
                        if  verificador==True:
                            st.warning("Ya existe una publicacion con ese ID.")
                        else:
                            if publicaciones_data["titulo_publicacion"] and publicaciones_data["nombre_revista"]:
                                if st.button("Crear Publicacion"):
                                    crear_publicacion(publicaciones_data)
                                    st.success("Publicacion creada")

                elif opcion == "Actualizar":

                    idPub = st.number_input("ID de la publicacion:", format= "%d", value=0, step = 1)
                    idPub = int(idPub)
                    if idPub:
                        verificador = verificar_publicaciones_existente(idPub)
                        if verificador == True:
                            publicaciones_data = {
                            "titulo_publicacion": st.text_input("Titulo de la publicacion"),
                            "nombre_revista": st.text_input("Nombre de la revista"),
                            "anno_publicacion": st.number_input("Año publicacion", format= "%d", value=0, step = 1)
                            }
                            if publicaciones_data["titulo_publicacion"] and publicaciones_data["nombre_revista"]:
                                if st.button("Actualizar publicacion"):
                                    actualizar_publicacion(idPub, publicaciones_data)
                                    st.success("Actualizacion realizada")
                        else:
                            st.warning("No se encontro el ID")
                
                elif opcion == "Visualizar":
                    publicaciones = recuperar_publicaciones_para_visualizar()
                    df_publicaciones = pd.DataFrame(publicaciones)
                    df_publicaciones.rename(columns={
                        'anno_publicacion': 'Año de publicacion',
                        'nombre_revista': 'Nombre de revista',
                        'titulo_publicacion': 'Titulo de publicacion',
                        'idPub': 'ID de la publicacion'
                    }, inplace=True)
                    st.title('Lista de Proyectos')
                    st.table(df_publicaciones)

                
            elif gestion_choice == "Gestion de Investigadores":
                st.subheader("Investigadores")
                operacion = st.selectbox("Seleccione una operación:", ["Crear", "Actualizar", "Visualizar"])
                
                if operacion == "Crear":
                    investigador_data = {
                        "id": st.number_input("ID del Investigador:", format="%d", value=0, step=1),
                        "nombre_completo": st.text_input("Nombre completo del investigador:"),
                        "titulo_academico": st.text_input("Título académico del investigador:"),
                        "email": st.text_input("Email del investigador:")
                    }
                    idInv = int(investigador_data["id"])
                    if idInv:  # Verificar si el usuario ha ingresado un ID del investigador
                        verificador=verificar_investigador_existente(idInv)
                        if  verificador==True:
                            st.warning("El investigador con este ID ya existe en la base de datos.")
                        else:
                            if investigador_data["nombre_completo"] and investigador_data["titulo_academico"] and investigador_data["email"]:
                                if st.button("Crear Investigador"):
                                    crear_investigador(investigador_data)
                                    st.success("Investigador creado exitosamente.")
                
                elif operacion == "Actualizar":
                    idInv = st.number_input("ID del Investigador a actualizar:",format="%d", value=0, step=1)
                    idInv=int(idInv)
                    if idInv:
                        verificador=verificar_investigador_existente(idInv)
                        if verificador==True:
                            investigador_data = {
                                "nombre_completo": st.text_input("Nuevo nombre completo del investigador:"),
                                "titulo_academico": st.text_input("Nuevo título académico:"),
                                "email": st.text_input("Nuevo email del investigador:")
                            }
                            if investigador_data["nombre_completo"] and investigador_data["titulo_academico"] and investigador_data["email"]:
                                if st.button("Actualizar Investigador"):
                                    actualizar_investigador(idInv, investigador_data)
                                    st.success("Investigador actualizado exitosamente.")
                        else:
                            st.error("El Investigador con este ID no existe en la base de datos.")
                
                elif operacion == "Visualizar":
                    st.write("Investigadores:")
                    investigadores = recuperar_investigadores_para_visualizar()
                    print (investigadores)
                    df_investigadores = pd.DataFrame(investigadores)
                    df_investigadores.rename(columns={
                        'id': 'ID del Investigador',
                        'nombre_completo': 'Nombre completo del investigador',
                        'titulo_academico': 'Titulo académico del investigador',
                        'email': 'Email del Investigador'
                    }, inplace=True)
                    st.title('Lista de Investigadores')
                    st.table(df_investigadores)

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
                            if proyecto_data["titulo_proyecto"] and proyecto_data["area_conocimiento"]:
                                if st.button("Actualizar Proyecto"):
                                    actualizar_proyecto(idPry, proyecto_data)
                                    st.success("Proyecto actualizado exitosamente.")
                        else:
                            st.error("El proyecto con este ID no existe en la base de datos.")
                
                elif operacion == "Visualizar":
                    st.write("Proyectos:")
                    proyectos = recuperar_proyectos_para_visualizar()
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
                operacion = st.selectbox("Seleccione una operación:", ["Subir archivos CSV", "Relacionar manualmente"])
                
                if operacion == "Subir archivos CSV":
                    uploaded_files = st.file_uploader("Subir archivos CSV", type=["csv"], accept_multiple_files=True)
                    if st.button("Cargar relaciones"):
                            if uploaded_files:
                                for uploaded_file in uploaded_files:
                                    df = pd.read_csv(uploaded_file)
                                    
                                    # Verificar si el DataFrame tiene las columnas correctas
                                    if set(df.columns) == {'idInv', 'idProy'}:
                                        # Verificar si los valores en las columnas son numéricos
                                        if not (df['idInv'].apply(lambda x: str(x).isnumeric()).all() and df['idProy'].apply(lambda x: str(x).isnumeric()).all()):
                                            st.error(f"El archivo {uploaded_file.name} contiene valores no numéricos en las columnas de ID.")
                                            continue
                                        # Procesar las relaciones si todo está bien
                                        procesar_relaciones(df)
                                    else:
                                        st.error(f"El archivo {uploaded_file.name} contiene valores no numéricos en las columnas de ID o es un archivo de nodos.")
                                    st.success(f"Los datos del archivo {uploaded_file.name} se han cargado correctamente en Neo4j.")
                            else:
                                st.warning("Por favor, suba los archivos CSV primero.")
                if operacion=="Relacionar manualmente":
                    st.subheader("Asociar Investigador a un proyecto")
                    
                    # Obtener la lista de investigadores y proyectos de la base de datos
                    investigadores = recuperar_investigadores_para_visualizar()  
                    df_investigadores = pd.DataFrame(investigadores)
                    proyectos = recuperar_proyectos_para_visualizar() 
                    df_proyectos = pd.DataFrame(proyectos)
                    
                    # Crear un widget de selección con los nombres de los investigadores
                    selected_investigador = st.selectbox(
                        'Selecciona un investigador:',
                        df_investigadores.apply(lambda row: (row['id'], row['nombre_completo']), axis=1)
                    )[0]  # [0] para obtener el id del tuple (id, nombre_completo)
                    
                    # Crear un widget de selección múltiple con los nombres de los proyectos, pero retornando los ids
                    selected_proyectos = st.multiselect(
                        'Selecciona los proyectos:',
                        df_proyectos.apply(lambda row: (row['idPry'], row['titulo_proyecto']), axis=1)
                    )
                    selected_proyectos_ids = [proyecto[0] for proyecto in selected_proyectos]  # Obtener solo los ids de los proyectos seleccionados
        
                    print (selected_proyectos)
                    print (selected_investigador)
                    if st.button("Asociar"):
                        if not selected_proyectos:
                            st.warning("Por favor, selecciona al menos un proyecto.")
                        else:
                            # Asociar el investigador seleccionado con los proyectos seleccionados
                            asociar_investigador_proyectos(selected_investigador, selected_proyectos_ids)  # Deberías implementar esta función
                            st.success(f"El investigador {selected_investigador} ha sido asociado correctamente a los proyectos seleccionados.")
                
            elif gestion_choice == "Asociar Artículo":
                st.subheader("Asociar Artículo a un proyecto")
                operacion = st.selectbox("Seleccione una operación:", ["Subir archivos CSV", "Relacionar manualmente"])
                
                if operacion == "Subir archivos CSV":
                
                    uploaded_files = st.file_uploader("Subir archivos CSV", type=["csv"], accept_multiple_files=True)
                    if st.button("Cargar relaciones"):
                        if uploaded_files:
                            for uploaded_file in uploaded_files:
                                df = pd.read_csv(uploaded_file)
                                
                                # Verificar si el DataFrame tiene las columnas correctas
                                if set(df.columns) != {'idProyecto', 'idArt'}:
                                    st.error(f"El archivo {uploaded_file.name} no tiene las columnas correctas.")
                                    continue
                                
                                # Verificar si los valores en las columnas son numéricos
                                if not (df['idProyecto'].apply(lambda x: str(x).isnumeric()).all() and df['idArt'].apply(lambda x: str(x).isnumeric()).all()):
                                    st.error(f"El archivo {uploaded_file.name} contiene valores no numéricos en las columnas de ID.")
                                    continue
                                
                                # Procesar las relaciones si todo está bien
                                procesar_relaciones_PUB_PRO(df)
                                st.success(f"Las relaciones del archivo {uploaded_file.name} se han cargado correctamente en Neo4j.")
                        else:
                            st.warning("Por favor, suba los archivos CSV primero.")
                if operacion=="Relacionar manualmente":
                    st.subheader("Asociar artículo a un proyecto")
                    
                    # Obtener la lista de investigadores y proyectos de la base de datos
                    publicacion = recuperar_Publicaciones_para_visualizar()  
                    df_publicacion = pd.DataFrame(publicacion)
                    proyectos = recuperar_proyectos_para_visualizar() 
                    df_proyectos = pd.DataFrame(proyectos)
                    
                    # Crear un widget de selección con los nombres de los investigadores
                    selected_publicacion = st.selectbox(
                        'Selecciona un artículo:',
                        df_publicacion.apply(lambda row: (row['idPub'], row['nombre_revista']), axis=1)
                    )[0]  
                    
                    # Crear un widget de selección múltiple con los nombres de los proyectos, pero retornando los ids
                    selected_proyectos = st.selectbox(
                        'Selecciona los proyectos:',
                        df_proyectos.apply(lambda row: (row['idPry'], row['titulo_proyecto']), axis=1)
                    )
                    if st.button("Asociar"):
                        if not selected_proyectos:
                            st.warning("Por favor, selecciona al menos un proyecto.")
                        else:
                            # Asociar el investigador seleccionado con los proyectos seleccionados
                            asociar_publicacion_proyectos(selected_publicacion, selected_proyectos)  # Deberías implementar esta función
                            st.success(f"El artículo {selected_publicacion} ha sido asociado correctamente a los proyectos seleccionados.")
    else:
        st.error('No todos los tipos de nodos requeridos existen en la base de datos.')                

            
if __name__ == "__main__":
    main()
