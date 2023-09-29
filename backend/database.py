from neo4j import GraphDatabase
from py2neo import Graph, Node,Relationship
URI = "neo4j+s://1e46531c.databases.neo4j.io"
AUTH = ("neo4j", "proyectoBases12")

def crear_nodos_en_neo4j(nodos):
    graph = Graph(URI, auth=AUTH)
    for nodo in nodos:
        tipo = nodo.pop("tipo")
        node = Node(tipo, **nodo)
        graph.create(node)

def crear_nodo(nodo):
    # Crea una conexión a la base de datos Neo4j
    graph = Graph(URI, auth=AUTH)
    
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




def recuperar_proyectos_para_visualizar():
    graph = Graph(URI, auth=AUTH)
    query = "MATCH (p:Proyectos) RETURN p"
    try:
        resultados = graph.run(query).data()
        proyectos = []
        for resultado in resultados:
            proyecto = resultado.get('p', {})
            proyectos.append(proyecto)
        return proyectos
    except Exception as e:
        print(f"Error al recuperar proyectos: {e}")
        return []  # Retorna una lista vacía en caso de error

def recuperar_Investigadores_para_visualizar():
    graph = Graph(URI, auth=AUTH)
    query = "MATCH (p:Investigadores) RETURN p"
    try:
        resultados = graph.run(query).data()
        proyectos = []
        for resultado in resultados:
            proyecto = resultado.get('p', {})
            proyectos.append(proyecto)
        return proyectos
    except Exception as e:
        print(f"Error al recuperar proyectos: {e}")
        return []  # Retorna una lista vacía en caso de error

def recuperar_Publicaciones_para_visualizar():
    graph = Graph(URI, auth=AUTH)
    query = "MATCH (p:Publicaciones) RETURN p"
    try:
        resultados = graph.run(query).data()
        proyectos = []
        for resultado in resultados:
            proyecto = resultado.get('p', {})
            proyectos.append(proyecto)
        return proyectos
    except Exception as e:
        print(f"Error al recuperar proyectos: {e}")
        return []  # Retorna una lista vacía en caso de error


def verificar_publicaciones_existente(idPub):
    graph = Graph(URI, auth=AUTH)
    publicacion = graph.nodes.match("Publicaciones", idPub=idPub).first()
    if publicacion==None:
        return False 
    else:
        return True

def actualizar_publicacion(idPub, datos_publicacion):
    graph = Graph(URI, auth=AUTH)
    publicacion = graph.nodes.match("Publicaciones", idPub=idPub).first()
    if publicacion:
        publicacion.update(**publicacion)
        graph.push(publicacion)

def obtener_nodos():
    graph = Graph(URI, auth=AUTH)

    consulta_cypher = """
    MATCH (n:Publicaciones)
    RETURN n
    LIMIT 100
    """

    # Ejecutar la consulta y obtener los resultados
    resultados = graph.run(consulta_cypher)

    return resultados

def crear_publicacion(datos_publicacion):
    graph = Graph(URI, auth=AUTH)
    publicacion = Node("Publicaciones", **datos_publicacion)
    graph.create(publicacion)

    

def recuperar_relaciones_proyectos_investigadores():
    graph = Graph(URI, auth=AUTH)
    query = """
    MATCH (i:Investigadores)-[r:PARTICIPA_EN]->(p:Proyectos)
    RETURN i as investigador, r as relacion, p as proyecto
    """
    try:
        resultados = graph.run(query).data()
        relaciones = []
        for resultado in resultados:
            investigador = resultado.get('investigador', {})
            relacion = resultado.get('relacion', {})
            proyecto = resultado.get('proyecto', {})
            relaciones.append({
                'investigador': investigador,
                'relacion': relacion,
                'proyecto': proyecto
            })
        return relaciones
    except Exception as e:
        print(f"Error al recuperar relaciones: {e}")
        return []  # Retorna una lista vacía en caso de error
    
    
    
def recuperar_relaciones_proyectos_publicaciones():
    graph = Graph(URI, auth=AUTH)
    query = """
    MATCH (i:Publicaciones)-[r:PERTENECE_A]->(p:Proyectos)
    RETURN i as publicacion, r as relacion, p as proyecto
    """
    try:
        resultados = graph.run(query).data()
        relaciones = []
        for resultado in resultados:
            publicacion = resultado.get('publicacion', {})
            relacion = resultado.get('relacion', {})
            proyecto = resultado.get('proyecto', {})
            relaciones.append({
                'publicacion': publicacion,
                'relacion': relacion,
                'proyecto': proyecto
            })
        return relaciones
    except Exception as e:
        print(f"Error al recuperar relaciones: {e}")
        return []  # Retorna una lista vacía en caso de error
    
    
def asociar_investigador_proyectos(selected_investigador, selected_proyectos):
    graph = Graph(URI, auth=AUTH)  # Asegúrate de que URI y AUTH estén definidos correctamente
    try:
        # Convertir el ID del investigador a int
        idInv = int(selected_investigador)
    except ValueError:
        print(f"ID inválido: Investigador {selected_investigador}")
        return
    
    # Verificar si el nodo del investigador existe antes de crear las relaciones
    investigador = graph.nodes.match("Investigadores", id=idInv).first()
    if not investigador:
        print(f"No se pudo crear las relaciones porque el Investigador {idInv} no existe.")
        return
    
    for idProy_str in selected_proyectos:
        try:
            # Convertir el ID del proyecto a int
            idProy = int(idProy_str)
            
            # Verificar si el nodo del proyecto existe antes de crear la relación
            proyecto = graph.nodes.match("Proyectos", idPry=idProy).first()
            if not proyecto:
                print(f"No se pudo crear la relación con el Proyecto {idProy} porque no existe.")
                continue
            
            # Crear la relación entre el investigador y el proyecto
            graph.create(Relationship(investigador, "PARTICIPA_EN", proyecto))
            print(f"Relación creada con éxito entre Investigador {idInv} y Proyecto {idProy}")
        
        except ValueError:
            print(f"ID inválido: Proyecto {idProy_str}")
        except Exception as e:
            print(f"Error al crear la relación entre Investigador {idInv} y Proyecto {idProy_str}: {e}")


def asociar_publicacion_proyectos(selected_publicacion, selected_proyectos):
    graph = Graph(URI, auth=AUTH)  # Asegúrate de que URI y AUTH estén definidos correctamente
    try:
        # Convertir el ID del investigador a int
        idInv = int(selected_publicacion)
    except ValueError:
        print(f"ID inválido: Investigador {selected_publicacion}")
        return
    
    # Verificar si el nodo del investigador existe antes de crear las relaciones
    investigador = graph.nodes.match("Publicaciones", idPub=idInv).first()
    if not investigador:
        print(f"No se pudo crear las relaciones porque el artículo {idInv} no existe.")
        return
    
    for idProy_str in selected_proyectos:
        try:
            # Convertir el ID del proyecto a int
            idProy = int(idProy_str)
            
            # Verificar si el nodo del proyecto existe antes de crear la relación
            proyecto = graph.nodes.match("Proyectos", idPry=idProy).first()
            if not proyecto:
                print(f"No se pudo crear la relación con el Proyecto {idProy} porque no existe.")
                continue
            
            # Crear la relación entre el investigador y el proyecto
            graph.create(Relationship(investigador, "PERTENECE_A", proyecto))
            print(f"Relación creada con éxito entre artículo {idInv} y Proyecto {idProy}")
        
        except ValueError:
            print(f"ID inválido: Proyecto {idProy_str}")
        except Exception as e:
            print(f"Error al crear la relación entre artículo {idInv} y Proyecto {idProy_str}: {e}")