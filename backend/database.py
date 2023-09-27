from neo4j import GraphDatabase
from py2neo import Graph, Node, Relationship
import numpy as np


URI = "neo4j+s://1e46531c.databases.neo4j.io"
AUTH = ("neo4j", "proyectoBases12")

def crear_nodos_en_neo4j(nodos):
    graph = Graph(URI, auth=AUTH)
    for nodo in nodos:
        tipo = nodo.pop("tipo")
        node = Node(tipo, **nodo)
        graph.create(node)


def crear_relaciones_para_Inv_Proy(relaciones):
    graph = Graph(URI, auth=AUTH)
    for relacion in relaciones:
        try:
            # Obtener y convertir los IDs a int
            idInv = int(relacion.get("idInv", 0))
            idProy = int(relacion.get("idProy", 0))
            
            # Verificar si los IDs son válidos antes de buscar los nodos
            if idInv and idProy:
                # Verificar si ambos nodos existen antes de crear la relación
                if verificar_nodos_Inv_Proy(graph, idInv, idProy):
                    investigador = graph.nodes.match("Investigadores", id=idInv).first()
                    proyecto = graph.nodes.match("Proyectos", idPry=idProy).first()
                    graph.create(Relationship(investigador, "PARTICIPA_EN", proyecto))
                else:
                    print(f"No se pudo crear la relación entre Investigador {idInv} y Proyecto {idProy} porque uno o ambos nodos no existen.")
            else:
                print(f"IDs inválidos: Investigador {idInv}, Proyecto {idProy}")
        except Exception as e:
            print(f"Error al crear la relación entre Investigador {relacion.get('idInv')} y Proyecto {relacion.get('idProy')}: {e}")



def verificar_nodos_Inv_Proy(graph, idInv, idProy):
    investigador = graph.nodes.match("Investigadores", id=idInv).first()
    proyecto = graph.nodes.match("Proyectos", idPry=idProy).first()
    
    if investigador is None:
        print(f"No se encontró el nodo Investigador con id={idInv}")
    if proyecto is None:
        print(f"No se encontró el nodo Proyecto con id={idProy}")
    
    return investigador is not None and proyecto is not None


def crear_relaciones_para_publ_Proy(relaciones):
    graph = Graph(URI, auth=AUTH)
    for relacion in relaciones:
        try:
            # Obtener y convertir los IDs a int
            idPubl = int(relacion.get("idArt", 0))
            idProy = int(relacion.get("idProyecto", 0))
            
            # Verificar si los IDs son válidos antes de buscar los nodos
            if idPubl and idProy:
                # Verificar si ambos nodos existen antes de crear la relación
                if verificar_nodos_Inv_Proy(graph, idPubl, idProy):
                    publicacion = graph.nodes.match("Publicaciones", idPub=idPubl).first()
                    proyecto = graph.nodes.match("Proyectos", idPry=idProy).first()
                    graph.create(Relationship(publicacion, "PERTENECE_A", proyecto))
                else:
                    print(f"No se pudo crear la relación entre Publicación {idPubl} y Proyecto {idProy} porque uno o ambos nodos no existen.")
            else:
                print(f"IDs inválidos: Publicación {idPubl}, Proyecto {idProy}")
        except Exception as e:
            print(f"Error al crear la relación entre Publicación {relacion.get('idPubl')} y Proyecto {relacion.get('idProy')}: {e}")
            
def verificar_nodos_Plu_Proy(graph, idPubl, idProy):
    publicacion = graph.nodes.match("Publicaciones", idPub=idPubl).first()
    proyecto = graph.nodes.match("Proyectos", idPry=idProy).first()
    
    if publicacion is None:
        print(f"No se encontró el nodo Publicación con id={idPubl}")
    if proyecto is None:
        print(f"No se encontró el nodo Proyecto con id={idProy}")
    
    return publicacion is not None and proyecto is not None


def verificar_proyecto_existente(idPry):
    graph = Graph(URI, auth=AUTH)
    proyecto = graph.nodes.match("Proyectos", idPry=idPry).first()
    if proyecto==None:
        return False 
    else:
        return True

def crear_proyecto(proyecto_data):
    graph = Graph(URI, auth=AUTH)
    proyecto = Node("Proyectos", **proyecto_data)
    graph.create(proyecto)
    
def actualizar_proyecto(idPry, proyecto_data):
    graph = Graph(URI, auth=AUTH)
    proyecto = graph.nodes.match("Proyectos", idPry=idPry).first()
    if proyecto:
        proyecto.update(**proyecto_data)
        graph.push(proyecto)




def visualizar_proyectos():
    return 0


verificar_proyecto_existente(21)