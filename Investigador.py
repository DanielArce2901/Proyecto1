

class Investigador:
    def __init__(self, pId, nombre_completo, titulo_academico, institucion, pEmail):
        self.id = pId
        self.nombre_completo = nombre_completo
        self.titulo_academico = titulo_academico
        self.institucion = institucion
        self.email = pEmail

    def agregarInvestigador(self, pBase):
        consulta = "MERGE (i:Investigador {id: $id, nombre_completo: $nombre_completo,\
            titulo_academico: $titulo_academico, institucion: $institucion, email: $email})"
        
        parametros= {"id": self.id,"nombre_completo": self.nombre_completo, 
            "titulo_academico": self.titulo_academico, "institucion":self.institucion, "email": self.email}

        pBase.query(consulta, parametros)
    
    def modificarInvestigador(self, pBase):
        consulta = "MATCH(p:Investigador{id: $id})\
                SET p.nombre_completo=$nombre_completo, p.titulo_academico = $titulo_academico, \
                p.institucion = $institucion, p.email = $email"
        
        parametros= {"id": self.id,"nombre_completo": self.nombre_completo, 
            "titulo_academico": self.titulo_academico, "institucion":self.institucion, "email": self.email}
        
        pBase.query(consulta, parametros)



        
    


        

    