import streamlit as st
import couchdb
import hashlib
import pandas as pd
from datetime import datetime
import calendar



# Función para establecer conexión con la base de datos CouchDB
def establecerConexion():
    couchdb_server_url = 'http://admin:admin@localhost:5984'
    try:
        server = couchdb.Server(couchdb_server_url)
        db = server['proyecto_bases']
        return db
    except couchdb.http.ResourceNotFound:
        st.error("No se pudo encontrar la base de datos 'proyecto_bases'.")
        return None
    except couchdb.http.ServerError as e:
        st.error(f"Error al conectar con CouchDB: {e}")
        return None

# Función para hashear contraseñas
def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def cerrar_sesion():
    # Eliminar el estado de la sesión
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.experimental_rerun()  # Re-ejecutar el script para actualizar la página


def registro_colaborador():
    st.header("Registro de Colaborador")

    # Inicializar las variables de estado si aún no existen
    if 'registro_email' not in st.session_state:
        st.session_state['registro_email'] = ''
    if 'registro_password' not in st.session_state:
        st.session_state['registro_password'] = ''
    # ... inicializar el resto de las variables de estado

    email = st.text_input("Correo Electrónico", key='registro_email')
    password = st.text_input("Contraseña", type="password", key='registro_password')
    nombre = st.text_input("Nombre Completo", key='registro_nombre')
    puesto = st.text_input("Puesto", key='registro_puesto')
    departamento = st.text_input("Departamento", key='registro_departamento')

    if st.button('Registrarse'):
        if not email or not password or not nombre or not puesto or not departamento:
            st.error("Todos los campos son obligatorios para el registro.")
        else:
            db = establecerConexion()
            if db:
                if db.get(email):
                    st.error("El correo electrónico ya está registrado.")
                else:
                    
                    nuevo_usuario = {
                        "_id": email,
                        "contraseña": password,
                        "nombre": nombre,
                        "puesto": puesto,
                        "departamento": departamento
                    }
                    try:
                        db.save(nuevo_usuario)
                        st.success("Registro exitoso.")
                        # Limpiar el estado del formulario después del registro exitoso
                        for key in ['registro_email', 'registro_password', 'registro_nombre', 'registro_puesto', 'registro_departamento']:
                            st.session_state[key] = ''
                    except Exception as e:
                        st.error(f"Ocurrió un error al guardar el usuario: {e}")



def main():
    # Cargar un CSS externo
    with open("style.css") as f:
       st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Título de la página
    st.title("Plataforma de Viajes Corporativos")

    # Menú lateral para selección de rol
    st.sidebar.title("Menú")
    opcion = st.sidebar.radio("Selecciona tu rol:", ["Colaborador", "Personal Administrativo"])

    # Inicio de sesión o registro de Colaborador
    
    if opcion == "Colaborador":
        if 'usuario' not in st.session_state:
            # Si no ha iniciado sesión, mostrar el formulario de inicio de sesión
            colaborador_login()
            
            
        else:
            mostrar_opciones_colaborador()
            
    # Inicio de sesión de Personal Administrativo
    elif opcion == "Personal Administrativo":
        if 'admin' not in st.session_state:
            # Si no ha iniciado sesión, mostrar el formulario de inicio de sesión
            personal_administrativo_login()
        else:
            # Si ya inició sesión, mostrar el menú de opciones administrativas
            mostrar_opciones_administrativas()
    
    if st.sidebar.button('Cerrar Sesión'):
                cerrar_sesion()   
                
    if st.sidebar.button('¿No tienes cuenta? Regístrate aquí'):
                registro_colaborador()                   


# Función para el inicio de sesión o registro de Colaborador
def colaborador_login():
    st.header("Inicio de sesión de Colaborador")
    with st.form(key='colaborador_login_form'):
        email = st.text_input("Correo Electrónico")
        password = st.text_input("Contraseña", type="password")
        login_button = st.form_submit_button(label='Iniciar Sesión')
        
        if login_button:
            db = establecerConexion()
            if db:
                if not email or not password:
                    st.error("Todos los campos son obligatorios para el registro.")
                    return 
                usuario = db.get(email)
                departamento=usuario.get('departamento')
                
                if usuario and usuario['contraseña'] == password:
                    st.session_state['usuario'] = usuario  # Guardar el usuario en el estado de sesión
                    st.session_state['emailActual'] = email  # Guardar el correo electrónico en el estado de sesión
                    st.session_state['departamento'] = departamento
                    st.success("Inicio de sesión exitoso.")
                    st.experimental_rerun()  # Re-ejecutar el script para actualizar la página
                else:
                    st.error("Usuario o contraseña incorrectos.")







            
            


def obtener_siguiente_numero(db):
    # Suponiendo que 'db' es tu conexión a la base de datos y que tienes un documento que almacena el último número utilizado.
    # Este documento podría tener un ID como 'ultimo_id_viaje'.
    try:
        doc = db['ultimo_id_viaje']
        ultimo_numero = doc['ultimo_numero']
        nuevo_numero = ultimo_numero + 1
        # Actualizar el documento en la base de datos de forma atómica
        db.save({'_id': 'ultimo_id_viaje', '_rev': doc['_rev'], 'ultimo_numero': nuevo_numero})
        return nuevo_numero
    except couchdb.http.ResourceNotFound:
        # Si el documento no existe, crear uno nuevo con el número inicial
        db.save({'_id': 'ultimo_id_viaje', 'ultimo_numero': 1})
        return 1

def generar_id_viaje_con_numero(db):
    numero_unico = obtener_siguiente_numero(db)
    id_viaje = f"viaje_{numero_unico}"
    return id_viaje
   


# Función para mostrar opciones adicionales para colaboradores
def mostrar_opciones_colaborador():
    # Opciones como modificar/eliminar solicitud, ver historial, etc.
    # ...
   
    menu_option = st.selectbox(
        "Selecciona una opción:",
        ("", "Registrar una solicitud de viaje", "Editar solicitud", "Eliminar solicitud", "Ver historial"),
        index=0  # Esto hace que la opción por defecto sea vacía
    )
     # Formulario de registro de colaborador
    if  menu_option == "Registrar una solicitud de viaje":
        with st.form(key='colaborador_form'):
            viaje_internacional = st.checkbox("Viaje Internacional")
            destino = st.text_input("Destino") 
            motivo_viaje = st.selectbox("Motivo del Viaje", ["Seguimiento", "Cierre Venta", "Capacitación"])
            fecha_inicio = st.date_input("Fecha de Inicio")
            fecha_fin = st.date_input("Fecha de Finalización")
            aerolinea = st.text_input("Nombre de la Aerolínea")
            precio_boletos = st.number_input("Precio de los Boletos")
            alojamiento = st.text_input("Nombre del Alojamiento")
            transporte = st.checkbox("Requiere Transporte")
            submit_button = st.form_submit_button(label='Registrar Solicitud')
            if submit_button:
                # Validación de los datos (puedes expandir según sea necesario)
                if fecha_inicio > fecha_fin:
                    st.error("La fecha de inicio no puede ser posterior a la fecha de finalización.")
                else:
                    # Establecer conexión con la base de datos
                    db = establecerConexion()
                    # Crear la solicitud
                    idCreado=generar_id_viaje_con_numero(db)
                    
                    email = st.session_state['emailActual']
                    departamento=st.session_state['departamento']
                    documento_colaborador=db[email]
                    if documento_colaborador:
                        # Asegurarse de que el documento tiene una clave 'viajes' que es una lista
                        if 'viajes' not in documento_colaborador:
                            documento_colaborador['viajes'] = []
                        
                        # Añadir el nuevo idCreado a la lista de 'viajes'
                        documento_colaborador['viajes'].append(idCreado)
                        
                        # Guardar el documento actualizado en la base de datos
                        db.save(documento_colaborador)
                        
                    else:
                        st.error("No se encontró el documento del colaborador.")

                # Crear la solicitud de viaje como un documento separado
                solicitud_viaje = {
                    '_id': idCreado,
                    'tipo': 'viaje',
                    'viaje_internacional': viaje_internacional,
                    'usuario_id': email,
                    'departamento':departamento,
                    'destino': destino,
                    'motivo_viaje': motivo_viaje,
                    'fecha_inicio': fecha_inicio.isoformat(),
                    'fecha_fin': fecha_fin.isoformat(),
                    'aerolinea': aerolinea,
                    'precio_boletos': precio_boletos,
                    'alojamiento': alojamiento,
                    'transporte': transporte,
                    'estado': 'Pendiente'
                }

                # Guardar la solicitud de viaje en la base de datos
                try:
                    db.save(solicitud_viaje)
                    st.success("Solicitud de viaje registrada con éxito.")
                except Exception as e:
                    st.error(f"Ocurrió un error al guardar la solicitud de viaje: {e}")
    if menu_option == "Editar solicitud":  
        db = establecerConexion()
        usuario_id = st.session_state['emailActual']
        solicitudes = [doc['doc'] for doc in db.view('_all_docs', include_docs=True) if doc['doc'].get('usuario_id') == usuario_id]
        ids_solicitudes = [solicitud['_id'] for solicitud in solicitudes]
        id_solicitud_seleccionada = st.selectbox("Selecciona la solicitud a editar", ids_solicitudes)

        # Obtener el documento de la solicitud seleccionada
        solicitud = db.get(id_solicitud_seleccionada) 
        if db:
            with st.form(key='editar_solicitud_form'):
                
                if solicitud:
                    # Convertir las fechas de cadena a objetos datetime
                    fecha_inicio_value = datetime.strptime(solicitud.get('fecha_inicio'), '%Y-%m-%d').date() if solicitud.get('fecha_inicio') else datetime.now().date()
                    fecha_fin_value = datetime.strptime(solicitud.get('fecha_fin'), '%Y-%m-%d').date() if solicitud.get('fecha_fin') else datetime.now().date()

                    # Suponiendo que la solicitud tiene los mismos campos que al registrar
                    viaje_internacional = st.checkbox("Viaje Internacional", value=solicitud.get('viaje_internacional', False))
                    pais_destino = st.text_input("Destino", value=solicitud.get('destino', '')) 
                    motivo_viaje = st.selectbox("Motivo del Viaje", ["Seguimiento", "Cierre Venta", "Capacitación"], index=["Seguimiento", "Cierre Venta", "Capacitación"].index(solicitud.get('motivo_viaje', 'Seguimiento')))
                    fecha_inicio = st.date_input("Fecha de Inicio", value=fecha_inicio_value)
                    fecha_fin = st.date_input("Fecha de Finalización", value=fecha_fin_value)
                    aerolinea = st.text_input("Nombre de la Aerolínea", value=solicitud.get('aerolinea', ''))
                    precio_boletos_value = float(solicitud.get('precio_boletos', 0.0))
                    alojamiento = st.text_input("Nombre del Alojamiento", value=solicitud.get('alojamiento', ''))
                    transporte = st.checkbox("Requiere Transporte", value=solicitud.get('transporte', False))
                    submit_button = st.form_submit_button(label='Actualizar Solicitud')
                    if submit_button:
                        # Actualizar la solicitud
                        solicitud.update({
                            'viaje_internacional': viaje_internacional,
                            'destino': pais_destino,
                            'motivo_viaje': motivo_viaje,
                            'fecha_inicio': fecha_inicio.isoformat(),
                            'fecha_fin': fecha_fin.isoformat(),
                            'aerolinea': aerolinea,
                            'precio_boletos': precio_boletos_value,
                            'alojamiento': alojamiento,
                            'transporte': transporte,
                        })
                        db.save(solicitud)
                        st.success("Solicitud actualizada con éxito.")
                else:
                    st.error("No se encontró la solicitud seleccionada.")
        else:
            st.error("No se pudo establecer conexión con la base de datos.")

        
    if  menu_option == "Eliminar solicitud":  
            db = establecerConexion()
            usuario_id = st.session_state['emailActual']
            solicitudes = [doc['doc'] for doc in db.view('_all_docs', include_docs=True) if doc['doc'].get('usuario_id') == usuario_id]
            ids_solicitudes = [solicitud['_id'] for solicitud in solicitudes]
            id_solicitud = st.selectbox("Selecciona la solicitud a eliminar", ids_solicitudes)
            if st.button("Eliminar Solicitud"):
                try:
                    db.delete(db[id_solicitud])
                    st.success("Solicitud eliminada con éxito.")
                except Exception as e:
                    st.error(f"Ocurrió un error al eliminar la solicitud: {e}")
                    
    if menu_option == "Ver historial":  
        db = establecerConexion()
        usuario_id = st.session_state['emailActual']
        solicitudes = [doc['doc'] for doc in db.view('_all_docs', include_docs=True) if doc['doc'].get('usuario_id') == usuario_id]

        if solicitudes:
            # Convertir la lista de diccionarios en un DataFrame de pandas
            df_solicitudes = pd.DataFrame(solicitudes)

            # Opcional: Seleccionar o reordenar las columnas si es necesario
            df_solicitudes = df_solicitudes[['fecha_inicio', 'fecha_fin', 'destino', 'motivo_viaje', 'estado', 'aerolinea', 'precio_boletos', 'alojamiento', 'transporte']]

            # Mostrar el DataFrame como una tabla en Streamlit
            st.table(df_solicitudes)
        else:
            st.write("No hay solicitudes en el historial.")
                          


    
# Función para el inicio de sesión de Personal Administrativo
def personal_administrativo_login():
    st.header("Inicio de sesión - Personal Administrativo")
    with st.form(key='admin_form'):
        admin_user = st.text_input("Usuario")
        admin_password = st.text_input("Contraseña", type="password")
        login_button = st.form_submit_button(label='Iniciar Sesión')
        if login_button:
            db = establecerConexion()
            if db:
                try:
                    admin = db.get("admin_username")
                    if admin and admin['password'] == admin_password:
                        st.session_state['admin'] = admin_user
                        st.success("Inicio de sesión exitoso.")
                        st.experimental_rerun()  # Re-ejecutar el script para actualizar la página
                    else:
                        st.error("Usuario o contraseña incorrectos.")
                except couchdb.http.ResourceNotFound:
                    st.error("El usuario administrador no existe en la base de datos.")

# Función para mostrar opciones adicionales para el personal administrativo
def mostrar_opciones_administrativas():
    st.header("Panel Administrativo")
    menu_option = st.selectbox(
        "Selecciona una opción:",
        ("", "Valorar Solicitudes", "Consultar Viajes Programados", "Consultar Viajes Internacionales", "Consultar por Destino Específico"),
        index=0  # Esto hace que la opción por defecto sea vacía
    )

       
    # Página para valorar solicitudes
    if menu_option == "Valorar Solicitudes":
        db = establecerConexion()
        if db:
            # Obtener todas las solicitudes con estado 'Pendiente'
            solicitudes_pendientes = [doc['doc'] for doc in db.view('_all_docs', include_docs=True) if doc['doc'].get('estado') == 'Pendiente']
            
            if solicitudes_pendientes:
                # Mostrar solo los ID de las solicitudes pendientes en el selectbox
                id_solicitud_seleccionada = st.selectbox("Seleccionar Solicitud Pendiente", [s['_id'] for s in solicitudes_pendientes])
                
                # Obtener la solicitud seleccionada
                solicitud = db.get(id_solicitud_seleccionada)
                
                # Iniciar un formulario de Streamlit
                with st.form(key='valorar_solicitudes_form'):
                    # Display the values as text
                    st.text(f"Viaje Internacional: {solicitud.get('viaje_internacional', False)}")
                    if solicitud.get('viaje_internacional', False):
                        st.text(f"Destino: {solicitud.get('destino', '')}")
                    st.text(f"Motivo del Viaje: {solicitud.get('motivo_viaje', 'Seguimiento')}")
                    st.text(f"Fecha de Inicio: {solicitud.get('fecha_inicio')}")
                    st.text(f"Fecha de Finalización: {solicitud.get('fecha_fin')}")
                    st.text(f"Nombre de la Aerolínea: {solicitud.get('aerolinea', '')}")
                    st.text(f"Precio de los Boletos: {solicitud.get('precio_boletos', 0.0)}")
                    st.text(f"Nombre del Alojamiento: {solicitud.get('alojamiento', '')}")
                    st.text(f"Requiere Transporte: {solicitud.get('transporte', False)}")
                    
                    # Permitir al usuario valorar la solicitud seleccionada
                    valoracion = st.radio("Valoración", ["Aprobado", "Rechazado"])
                    # Usar un botón de envío de formulario para guardar la valoración
                    submit_button = st.form_submit_button("Guardar Valoración")
                
                if submit_button:
                    solicitud['estado'] = valoracion
                    db.save(solicitud)
                    st.success("Valoración guardada.")
            else:
                st.info("No hay solicitudes pendientes por valorar.")
        else:
            st.error("No se pudo establecer conexión con la base de datos.")



            


    # Página para consultar viajes programados
    if menu_option == "Consultar Viajes Programados":
        db = establecerConexion()
        if db:
            # Permitir al usuario seleccionar un mes y un año
            mes_seleccionado = st.selectbox("Seleccionar Mes", range(1, 13))
            año_seleccionado = st.selectbox("Seleccionar Año", range(2020, 2024))

            try:
                # Convertir mes y año seleccionado a formato de fecha para comparación
                fecha_inicio_mes = f"{año_seleccionado}-{mes_seleccionado:02d}-01"
                fecha_fin_mes = f"{año_seleccionado}-{mes_seleccionado:02d}-{calendar.monthrange(año_seleccionado, mes_seleccionado)[1]}"

                # Obtener todas las solicitudes aprobadas que coincidan con el mes y año seleccionado
                solicitudes_aprobadas_mes = [
                    doc['doc'] for doc in db.view('_all_docs', include_docs=True)
                    if doc['doc'].get('estado') == 'Aprobado' and
                    fecha_inicio_mes <= doc['doc'].get('fecha_inicio') <= fecha_fin_mes
                ]

                if solicitudes_aprobadas_mes:
                    # Mostrar la información requerida para cada solicitud aprobada
                    for solicitud in solicitudes_aprobadas_mes:
                        nombre_colaborador = solicitud.get('usuario_id', 'Nombre no disponible')
                        departamento = solicitud.get('departamento', 'Departamento no disponible')
                        st.write(f"Correo de Colaborador(a): {nombre_colaborador}, Departamento: {departamento}")
                else:
                    st.info("No hay viajes programados para el mes y año seleccionado.")
            except Exception as e:
                st.error(f"Se produjo un error al obtener las solicitudes: {e}")
        else:
            st.error("No se pudo establecer conexión con la base de datos.")


    # Página para consultar viajes internacionales
    if menu_option == "Consultar Viajes Internacionales":
        db = establecerConexion()
        if db:
            # Permitir al usuario seleccionar un trimestre y un año
            trimestre_seleccionado = st.selectbox("Seleccionar Trimestre", ["Q1", "Q2", "Q3", "Q4"])
            año_seleccionado = st.selectbox("Seleccionar Año", range(2020, 2024))

            # Definir los meses de inicio y fin basados en el trimestre seleccionado
            meses_trimestre = {
                "Q1": (1, 3),
                "Q2": (4, 6),
                "Q3": (7, 9),
                "Q4": (10, 12),
            }
            mes_inicio, mes_fin = meses_trimestre[trimestre_seleccionado]
            fecha_inicio_trimestre = f"{año_seleccionado}-{mes_inicio:02d}-01"
            ultimo_dia_mes_fin = calendar.monthrange(año_seleccionado, mes_fin)[1]
            fecha_fin_trimestre = f"{año_seleccionado}-{mes_fin:02d}-{ultimo_dia_mes_fin}"

            try:
                # Obtener todas las solicitudes de viajes internacionales en el trimestre seleccionado
                solicitudes_internacionales_trimestre = [
                    doc['doc'] for doc in db.view('_all_docs', include_docs=True)
                    if doc['doc'].get('viaje_internacional') and
                    doc['doc'].get('estado') == 'Aprobado' and
                    fecha_inicio_trimestre <= doc['doc'].get('fecha_inicio') <= fecha_fin_trimestre
                ]

                if solicitudes_internacionales_trimestre:
                    # Mostrar la información requerida para cada solicitud de viaje internacional
                    for solicitud in solicitudes_internacionales_trimestre:
                        nombre_colaborador = solicitud.get('usuario_id', 'Nombre no disponible')  # Asumiendo que usuario_id es el correo del colaborador
                        pais_destino = solicitud.get('destino', 'Destino no disponible')
                        st.write(f"Correo de Colaborador(a): {nombre_colaborador}, País de Destino: {pais_destino}")
                else:
                    st.info("No hay viajes internacionales programados para el trimestre y año seleccionado.")
            except Exception as e:
                st.error(f"Se produjo un error al obtener las solicitudes: {e}")
        else:
            st.error("No se pudo establecer conexión con la base de datos.")


    
    if menu_option == "Consultar por Destino Específico":
        db = establecerConexion()
        if db:
            # Permitir al usuario ingresar o seleccionar un destino
            destino_seleccionado = st.text_input("Ingrese o seleccione un destino")

            if destino_seleccionado:
                try:
                    # Obtener todas las solicitudes que coincidan con el destino seleccionado
                    solicitudes_destino_especifico = [
                        doc['doc'] for doc in db.view('_all_docs', include_docs=True)
                        if doc['doc'].get('destino') == destino_seleccionado
                    ]

                    if solicitudes_destino_especifico:
                        # Mostrar la información requerida para cada solicitud hacia el destino seleccionado
                        for solicitud in solicitudes_destino_especifico:
                            nombre_colaborador = solicitud.get('usuario_id', 'Nombre no disponible')  # Asumiendo que usuario_id es el correo del colaborador
                            fecha_inicio = solicitud.get('fecha_inicio', 'Fecha no disponible')
                            motivo_viaje = solicitud.get('motivo_viaje', 'Motivo no disponible')
                            st.write(f"Correo de Colaborador(a): {nombre_colaborador}, Fecha de Inicio: {fecha_inicio}, Motivo del Viaje: {motivo_viaje}")
                    else:
                        st.info(f"No hay viajes programados hacia el destino: {destino_seleccionado}.")
                except Exception as e:
                    st.error(f"Se produjo un error al obtener las solicitudes: {e}")
            else:
                st.info("Por favor, ingrese o seleccione un destino para consultar.")
        else:
            st.error("No se pudo establecer conexión con la base de datos.")

    

# Ejecutar la función principal
if __name__ == "__main__":
    main()

    






    