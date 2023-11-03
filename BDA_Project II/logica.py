import streamlit as st

#load an external CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Página de inicio
st.title("Plataforma de Viajes Corporativos")

# Opciones de inicio de sesión o registro
opcion = st.radio("Selecciona una opción:", ["Registro de Colaborador", "Inicio de Sesión (Personal Administrativo)"])

if opcion == "Registro de Colaborador":
    st.header("Registro de Colaborador")
    
    # Formulario de registro de colaborador
    email = st.text_input("Correo Electrónico")
    password = st.text_input("Contraseña", type="password")
    nombre = st.text_input("Nombre Completo")
    puesto = st.text_input("Puesto")
    departamento = st.text_input("Departamento")
    viaje_internacional = st.checkbox("Viaje Internacional")
    pais_destino = st.text_input("País de Destino")
    motivo_viaje = st.selectbox("Motivo del Viaje", ["Seguimiento", "Cierre Venta", "Capacitación"])
    fecha_inicio = st.date_input("Fecha de Inicio")
    fecha_fin = st.date_input("Fecha de Finalización")
    aerolinea = st.text_input("Nombre de la Aerolínea")
    precio_boletos = st.number_input("Precio de los Boletos")
    alojamiento = st.text_input("Nombre del Alojamiento")
    transporte = st.checkbox("Requiere Transporte")
    if st.button("Registrar Solicitud"):
        print ("Aún no hay nada, es solo para cerrar el if")
        # Aquí implementarás la lógica para guardar la solicitud en la base de datos (puedes hacerlo más tarde).
elif opcion == "Inicio de Sesión (Personal Administrativo)":
    st.header("Inicio de Sesión - Personal Administrativo")
    
    # Formulario de inicio de sesión para personal administrativo
    admin_user = st.text_input("Usuario")
    admin_password = st.text_input("Contraseña", type="password")
    
    if st.button("Iniciar Sesión"):
        print ("Aún no hay nada, es solo para cerrar el if")
        # Aquí implementarás la lógica de autenticación del personal administrativo (puedes hacerlo más tarde).
# Página para colaboradores ver historial de solicitudes (simulado)
if opcion == "Registro de Colaborador":
    st.header("Historial de Solicitudes de Colaborador")
    # Aquí mostrarás el historial de solicitudes del colaborador (simulado).

# Página para personal administrativo para ver solicitudes pendientes (simulado)
if opcion == "Inicio de Sesión (Personal Administrativo)":
    st.header("Solicitudes Pendientes (Personal Administrativo)")
    # Aquí mostrarás la lista de solicitudes pendientes (simulado).

# Página para personal administrativo para valorar solicitudes (simulado)
if opcion == "Inicio de Sesión (Personal Administrativo)":
    st.header("Valorar Solicitud (Personal Administrativo)")
    # Aquí permitirás al personal administrativo valorar las solicitudes (simulado).

# Página para personal administrativo para consultar viajes programados (simulado)
if opcion == "Inicio de Sesión (Personal Administrativo)":
    st.header("Consultar Viajes Programados (Personal Administrativo)")
    # Aquí permitirás al personal administrativo consultar viajes programados (simulado).

# Página para personal administrativo para consultar viajes internacionales (simulado)
if opcion == "Inicio de Sesión (Personal Administrativo)":
    st.header("Consultar Viajes Internacionales (Personal Administrativo)")
    # Aquí permitirás al personal administrativo consultar viajes internacionales (simulado).

# Página para personal administrativo para consultar por destino específico (simulado)
if opcion == "Inicio de Sesión (Personal Administrativo)":
    st.header("Consultar por Destino Específico (Personal Administrativo)")
    # Aquí permitirás al personal administrativo consultar por destino específico (simulado).
