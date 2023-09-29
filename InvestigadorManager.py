from neo4j import GraphDatabase
from Investigador import Investigador
class InvestigadorManager:
    def __init__(self, uri, username, password):
        self._driver = GraphDatabase.driver(uri, auth=(username, password))

    def close(self):
        self._driver.close()

    def crear_investigador(self, investigador):
        with self._driver.session() as session:
            session.write_transaction(self._crear_investigador, investigador)

    def _crear_investigador(self, tx, investigador):
        query = """
        CREATE (i:Investigador {id: $id, nombre_completo: $nombre_completo, 
                                titulo_academico: $titulo_academico, 
                                institucion: $institucion, email: $email})
        """
        tx.run(query, id=investigador.id, nombre_completo=investigador.nombre_completo,
            titulo_academico=investigador.titulo_academico,
            institucion=investigador.institucion, email=investigador.email)

    def obtener_investigador(self, id):
        with self._driver.session() as session:
            return session.read_transaction(self._obtener_investigador, id)

    def _obtener_investigador(self, tx, id):
        query = "MATCH (i:Investigador {id: $id}) RETURN i"
        result = tx.run(query, id=id)
        record = result.single()
        if record:
            return Investigador(record['id'], record['nombre_completo'],
                                record['titulo_academico'], record['institucion'], record['email'])
        return None

    def actualizar_investigador(self, investigador):
        with self._driver.session() as session:
            session.write_transaction(self._actualizar_investigador, investigador)

    def _actualizar_investigador(self, tx, investigador):
        query = """
        MATCH (i:Investigador {id: $id})
        SET i.nombre_completo = $nombre_completo,
            i.titulo_academico = $titulo_academico,
            i.institucion = $institucion,
            i.email = $email
        """
        tx.run(query, id=investigador.id, nombre_completo=investigador.nombre_completo,
            titulo_academico=investigador.titulo_academico,
            institucion=investigador.institucion, email=investigador.email)