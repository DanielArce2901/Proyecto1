from neo4j import GraphDatabase
from py2neo import Graph, Node,Relationship
from Investigador import Investigador
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


#erc

class DataBase:
    #Método constructor
    def __init__(self, pUri, pCredenciales):
        #Especificación de atributos
        self.__uri = pUri
        self.__credenciales = pCredenciales
        self.driver = None
        self.conectado = None

        try:
            self.driver = GraphDatabase.driver(pUri, auth= pCredenciales)
            self.driver.verify_connectivity()
            self.conectado = True
        except:
            print("Error con la conexion a la base de datos")
            self.conectado=False

    def estaConectado(self):
        return self.conectado

    def query(self, consulta, parametros=None):
        session = None
        respuesta = None
        if(self.estaConectado()):
            try:
                session = self.driver.session()
                respuesta = list(session.run(consulta, parametros))
            except:
                print("Error de consulta")
            finally:
                if (session is not None):
                    session.close()
            
        return respuesta
    

def top_areas_conocimiento():
    consulta= "MATCH (p:Proyecto) WITH p.area_conocimiento as area, COUNT(p) AS cantidad_proyectos ORDER BY cantidad_proyectos DESC LIMIT 5 RETURN area , cantidad_proyectos"
    top5=[]
    aux=[]
    data_base_connection= GraphDatabase.driver(uri=URI,auth=(AUTH))
    session = data_base_connection.session()
    result=session.run(consulta)
    for a in result:
        area=(f"{a['area']}")
        cantidad_proyectos=(f"{a['cantidad_proyectos']}")
        aux.append(area)
        aux.append(cantidad_proyectos)
        top5.append(aux)
        aux=[]
    print ("datos regresados")
    return top5

def top_areas_instituciones():
    consulta= "MATCH (I:Investigador) WITH I.institucion as INS, COUNT(I) AS cantidad_ins ORDER BY cantidad_ins DESC LIMIT 5 RETURN INS , cantidad_ins"
    top5=[]
    aux=[]
    data_base_connection= GraphDatabase.driver(uri=URI,auth=(AUTH))
    session = data_base_connection.session()
    result=session.run(consulta)
    for a in result:
        area=(f"{a['INS']}")
        cantidad_proyectos=(f"{a['cantidad_ins']}")
        aux.append(area)
        aux.append(cantidad_proyectos)
        top5.append(aux)
        aux=[]
    print ("datos regresados")
    return top5


def top_investigadores():
    consulta= "MATCH (I:Investigador)-[:trabaja_en_el_proyecto ]->(p:Proyecto) WITH I, COUNT(p) AS cantidad_proyectos ORDER BY cantidad_proyectos DESC LIMIT 5 RETURN I.nombre_completo AS nombre,I.institucion as ins, cantidad_proyectos as cant"
    top5=[]
    aux=[]
    data_base_connection= GraphDatabase.driver(uri=URI,auth=(AUTH))
    session = data_base_connection.session()
    result=session.run(consulta)
    for a in result:
        nombre=(f"{a['nombre']}")
        area=(f"{a['ins']}")
        cantidad_proyectos=(f"{a['cant']}")
        aux.append(nombre)
        aux.append(area)
        aux.append(cantidad_proyectos)
        top5.append(aux)
        aux=[]
    print ("datos regresados")
    return top5


#consulta de busqueda de un investigador

#para desplegar el nombre de los investigadores usar la funcion retornar_Investigadores()
#ademas para desplegar toda la info del Investigador usar datos_Investigador(nombre)

#usar esta funcion para tener los datos de los proyectos en los que trabaja un investigador
def info_proyectos_Investigador(nombre):
    lista_Proyectos=[]
    graph = Graph(uri=URI,auth=(AUTH))
    result=graph.run("MATCH (I:Investigador {nombre_completo: '"+nombre+"'})-[:trabaja_en_el_proyecto]->(p:Proyecto)RETURN p")
    for record in result:
        nodo=record["p"]
        aux=[]
        for key,value in nodo.items():
            aux.append(f"{key}:{value}")
        lista_Proyectos.append(aux)
    print ("datos regresados")
    return (lista_Proyectos)
    

#consulta de busqueda de un proyecto

#para deplegar el nombre de los proyectos usar retornar_Proyectos()
#para desplegar los datos del proyecto seleccionado usar 

#usar esta funcion para tener los datos de los investigadores que trabajan en un proyecto

def info_Investigadores_Proyecto(nombre):
    lista_Investigadores=[]
    graph = Graph(uri=URI,auth=(AUTH))
    result=graph.run("MATCH (p:Proyecto {titulo_proyecto: '"+nombre+"'})<-[:trabaja_en_el_proyecto]-(i:Investigador)RETURN i")
    for record in result:
        nodo=record["i"]
        aux=[]
        for key,value in nodo.items():
            aux.append(f"{key}:{value}")
        lista_Investigadores.append(aux)
    print ("datos regresados")
    return (lista_Investigadores)  

#usar esta funcion para tener la info de las publicaciones asociadas al proyecto

def info_Publicaciones_Proyecto(nombre):
    lista_Publicaciones=[]
    graph = Graph(uri=URI,auth=(AUTH))
    result=graph.run("MATCH (p:Proyecto {titulo_proyecto: '"+nombre+"'})<-[:publicacion_del_proyecto]-(pu:Publicacion)RETURN pu")
    for record in result:
        nodo=record["pu"]
        aux=[]
        for key,value in nodo.items():
            aux.append(f"{key}:{value}")
        lista_Publicaciones.append(aux)
    print ("datos regresados")
    return (lista_Publicaciones)


#consulta busqueda de publicaciones

#para desplegar el nombre de las publicaciones usar retornar_Articulos()
#para desplegar los datos de un articulo usar datos_Publicacion(titulo_publicacion)

#usar esta funcion para tener los titulos de los proyectos asociados a una publicacion
def info_Proyecto_Publicacion(nombre):
    lista_Proyectos=[]
    data_base_connection= GraphDatabase.driver(uri=URI,auth=(AUTH))
    session = data_base_connection.session()
    result = session.run("MATCH (pu:Publicacion {titulo_publicacion: '"+nombre+"'})-[:publicacion_del_proyecto]->(p:Proyecto)RETURN p.titulo_proyecto as titulo")
    for a in result:
        titulo=(f"{a['titulo']}")
        lista_Proyectos.append(titulo)
    print ("datos regresados")
    return (lista_Proyectos)


#consulta busqueda por area de conocimiento

#retorna las areas de conocimiento sin repetirse
def retornar_areas_conocimiento():
    lista_area=[]
    data_base_connection= GraphDatabase.driver(uri=URI,auth=(AUTH))
    session = data_base_connection.session()
    result = session.run("MATCH (P:Proyecto) RETURN distinct P.area_conocimiento AS area")
    for a in result:
        area=(f"{a['area']}")
        lista_area.append(area)
    print("Datos retornados")
    return print(lista_area)

#retorna los nombres de los proyectos de esa area de conocimiento

def retornar_proyectos_conocimiento(nombre):
    lista_titulo=[]
    data_base_connection= GraphDatabase.driver(uri=URI,auth=(AUTH))
    session = data_base_connection.session()
    result = session.run("MATCH (P:Proyecto) where P.area_conocimiento='"+nombre+"'RETURN P.titulo_proyecto AS titulo")
    for a in result:
        titulo=(f"{a['titulo']}")
        lista_titulo.append(titulo)
    print("Datos retornados")
    return print(lista_titulo)


#retorna los titulos de los articulos relacionados a esa area de conocimiento

def retornar_articulos_conocimiento(nombre):
    lista_Articulos=[]
    data_base_connection= GraphDatabase.driver(uri=URI,auth=(AUTH))
    session = data_base_connection.session()
    result = session.run("MATCH (p:Proyecto {area_conocimiento:'"+nombre+"'})<-[:publicacion_del_proyecto]-(pu:Publicacion) RETURN pu.titulo_publicacion as titulo")
    for a in result:
        titulo=(f"{a['titulo']}")
        lista_Articulos.append(titulo)
    print ("datos regresados")
    return print(lista_Articulos)

#consulta busqueda de colegas

#para desplegar los nombres de los investigadores usar retornar_Investigadores()
#para desplegar la informacion de un investigador en especifico usar datos_Investigador(nombre)

def retornar_colegas(nombre):
    lista_colegas=[]
    data_base_connection= GraphDatabase.driver(uri=URI,auth=(AUTH))
    session = data_base_connection.session()
    result = session.run("MATCH (I:Investigadores {nombre_completo:'"+nombre+"'})-[:trabaja_en_el_proyecto]->(P:Proyectos)<-[:trabaja_en_el_proyecto]-(oi:Investigadores) WHERE I <> oi RETURN  distinct oi.nombre_completo as colegas")
    for a in result:
        titulo=(f"{a['colegas']}")
        lista_colegas.append(titulo)
    print ("datos regresados")
    return print(lista_colegas)