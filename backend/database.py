from neo4j import GraphDatabase
from py2neo import Graph, Node

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
    # Guarda el nodo en la base de datos
    graph.create(nodo)