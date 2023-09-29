import streamlit as st
from Investigador import Investigador
import pandas as pd


def registrarInvestigador(base):
    try:
        idInv = st.number_input("ID para el investigador",0)
        nombre = st.text_input("Nombre completo del investigador")
        titulo = st.text_input("Título academico del investigador")
        institucion = st.text_input("Institucion del investigador")
        iEmail = st.text_input("Email del investigador")
        
        if st.button("Registrarse", key="boton_registro"):
            #crear investigador con los datos ingresados
            investigador = Investigador(pId= idInv, nombre_completo=nombre, titulo_academico= titulo,
                institucion= institucion, pEmail=iEmail)
            
            #Agregar investigador en la base de datos
            investigador.agregarInvestigador(base)
            st.success("Registro exitoso")

    except:
        print("Error al ingresar un dato numerico")

def modificarInvestigador(base):
    try:
        idInv = st.number_input("ID para el investigador",0)
        nombre = st.text_input("Nombre completo del investigador")
        titulo = st.text_input("Título academico del investigador")
        institucion = st.text_input("Institucion del investigador")
        iEmail = st.text_input("Email del investigador")
        
        if st.button("Modificar", key="boton_registro"):
            #crear investigador con los datos ingresados
            investigador = Investigador(pId= idInv, nombre_completo=nombre, titulo_academico= titulo,
                institucion= institucion, pEmail=iEmail)
            
            #Modificar investigador en la base de datos
            investigador.modificarInvestigador(base)
            st.success("Modificacion exitos")

    except:
        print("Error al ingresar un dato numerico")

def mostrarInvestigador(base):
    try:
        idInv = st.number_input("ID para el investigador",0)
        consulta = "MATCH(p:Investigador{id:$id}) \
            RETURN p.id AS ID, p.nombre_completo AS Nombre, p.titulo_academico AS Titulo_Academico,\
                p.institucion AS Institucion, p.email AS Email"
        parametro = {"id": idInv}
        if st.button("Buscar", key="boton_registro"):
            nodo = base.query(consulta, parametro)
            
            #Tomar los datos del nodo y guardarlos en una matriz
            propiedades = nodo[0].values("ID", "Nombre","Titulo_Academico", "Institucion", "Email")
            investigador = []
            investigador.append(propiedades)

            #Para convertir la matriz con los datos en un dataframe
            tablaInv = pd.DataFrame(investigador, columns = ["ID", "Nombre","Titulo_Academico", "Institucion", "Email"])

            #mostrar el dataframe en la pagina
            st.table(tablaInv)
    except:
        print("Error al ingresar un dato numerico")


    