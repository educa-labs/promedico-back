import psycopg2 as psql
import json
import datetime
import hashlib, uuid
import json

class DB():

    def __init__(self):
        self.conn = psql.connect("dbname=promedico user=felipe \
            password=123abc456 host=localhost port=5432")
        self.cur = self.conn.cursor()
        

    def poblar(self):
        try:
            self.cur.execute("""DROP TABLE IF EXISTS Usuarios, Actividades, Categorias,\
             Tipo, Tags, HasTag, Clinica, Noticias, Departamentos, AdminDepartamento, Tipos;""")

        except:
            print("Tablas no existian, creando tablas...")

            
        #Crear tabla Usuarios
        self.cur.execute("""
            CREATE TABLE Usuarios(id serial, nombre text, fecha timestamp,
            ocupacion text, pass text, salt text, mail text, clinica int,
            id_departamento int, token text,
            PRIMARY KEY(id));
            """)

        #Crear tabla Actividades
        self.cur.execute("""
            CREATE TABLE Actividades(id serial, id_usuario int references Usuarios(id), 
            titulo text, fecha timestamp, fecha_registro timestamp, tipo int, 
            reflexion text, PRIMARY KEY(id) );
            """)

        #Crear tabla Categorias / Tipo
        self.cur.execute("""
                CREATE TABLE Tipos(id serial primary key, titulo text, value int);
            """)
   

        #Crear tabla Tags
        self.cur.execute("""
            CREATE TABLE Tags(id serial primary key, title text, value int, descripcion text, meta int, color text);
            """)

        #Crear relacion TieneTag
        self.cur.execute("""
            CREATE TABLE HasTag(
            id_actividad int references Actividades(id), 
            id_tag int references Tags(id), 
            PRIMARY KEY (id_actividad, id_tag));
            """)

        #Crear tabla Clinica
        self.cur.execute("""
            CREATE TABLE Clinica(id serial, title text, PRIMARY KEY(id));
            """)

        #Crear tabla Departamentos
        self.cur.execute("""
            CREATE TABLE Departamentos(id serial primary key, title text, id_clinica int references Clinica(id), status int)
            """)

        #Crear relacion AdminDepartamento (si un usuario es admin de un departamento)
        self.cur.execute("""
            CREATE TABLE AdminDepartamento(id_usuario int references Usuarios(id),
             id_departamento int references Departamentos(id),
              PRIMARY KEY (id_usuario, id_departamento))
            """)

        #Crear tabla Noticias
        self.cur.execute("""
            CREATE TABLE Noticias(id serial primary key, titulo text, 
            descripcion text, link text, fecha timestamp);
            """)

        #Commit cambios en las tablas
        self.conn.commit()


    """
    Funciones de registro e inicio de Sesion
    """


    def nuevoUsuario(self, jeison):
        ret = {"status": 0}
        """
        Verifica que el usuario tenga todos los campos y sean validos
        1 si es correcto
        0 si hay datos incorrectos
        2 Usuario repetido
        El resto se maneja desde Front
        REQS:
        id serial,
        nombre text, 
        apellido text, 
        fecha timestamp, (automatico)
        ocupacion text, 
        pass text, 
        salt text, 
        mail text, 
        clinica int,
        id_departamento int, 
        token text
        """
        nombre = jeison["nombre"]
        ocupacion = jeison["ocupacion"] 
        password = jeison["password"].encode('utf-8')
        salt = uuid.uuid4().hex
        hashed_password = hashlib.sha256(password + salt.encode('utf-8')).hexdigest()
        mail = jeison["mail"]
        clinica = jeison["clinica"] #id de la clinica
        id_departamento = jeison["departamento"]

        token = uuid.uuid4().hex
        #Verificar que el usuario no se repita
        self.cur.execute("SELECT mail FROM Usuarios WHERE mail = %s;", (mail,))
        mailBD = self.cur.fetchall()
        if len(mailBD) > 0:
            ret["status"] = 0
            return ret

        #Insertar nuevo usuario
        tupla = (nombre, datetime.datetime.now(), 
            ocupacion, hashed_password, salt, mail, 
            clinica, id_departamento, token)

        self.cur.execute("""INSERT INTO Usuarios(nombre, fecha, ocupacion, pass, salt, mail, 
                            clinica, id_departamento, token) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);""",
                             tupla)
        self.conn.commit()

        ret["status"] = 1

        return ret

    def getSalt(self, mail):
        """
        Retorna SALT para ser encriptada la contrasena
        """
        salt = self.cur.execute("""
            SELECT salt FROM Usuarios WHERE mail = %s;
            """, (mail, ))
        salt = self.cur.fetchone()[0]

        return salt

    def login(self, jeison):
        """
        Password debe venir encriptada con salt
        Retorna 0 si la contrasena es incorrecta
        Retorna 1 si es correcto todo
        Retorna 2 si el departamento no esta inscrito o clinica
        Retorna 3 si el usuario no existe
        """
        mail = jeison["mail"]
        password = jeison["password"]
        result = {"status": 0, "token": None, "nombre": None}

        #Se obtiene password
        self.cur.execute("""
            SELECT pass, id_departamento FROM Usuarios WHERE mail = %s;
            """, (mail,))
        a = self.cur.fetchone()
        if a == None:
            return result
        real_password, id_depto = a

        #Se obiente salt y se hace encriptacion para comparar
        salt = self.getSalt(mail)
        password = hashlib.sha256(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()

        #Obtener status del departamento
        a = self.cur.execute("""
            SELECT status FROM Departamentos WHERE id = %s;
            """, (id_depto,))
        status_departamento = self.cur.fetchone()[0]

        values = (mail, )

        if status_departamento == 0:
            result["status"] = 0

        if status_departamento and password == real_password:
            result["status"] = 1
            self.cur.execute("SELECT token FROM Usuarios WHERE mail = %s;", values)
            result["token"] = self.cur.fetchone()[0]
            self.cur.execute("SELECT token, nombre, ocupacion, mail, id FROM Usuarios WHERE mail = %s;", values)
            datos = self.cur.fetchone()
            result["token"] = datos[0]
            result["nombre"] = datos[1]
            result["ocupacion"] = datos[2]
            result["mail"] = datos[3]
            id_usuario = datos[4]
            result["id"] = id_usuario


        elif password != real_password:
            result["status"] = 0
        
        elif not status_departamento:
            result["status"] = 0

        # Verificacion de administrador
        result["admin"] = False
        self.cur.execute("SELECT id_departamento FROM AdminDepartamento WHERE id_usuario = %s;", (id_usuario,))
        a = self.cur.fetchone()
        if a != None:
            result["admin"] = True



        return result

    def nuevaClinica(self, jeison):
        """
        REQS
        Title
        """
        title = jeison["title"]
        values = (title,)
        try:
            self.cur.execute("INSERT INTO Clinicas VALUES(%s);", values)
            self.conn.commit()
        except:
            return "Error"
        return "Clinica creada"

    def nuevoDepartamento(self,jeison):
        """
        REQS
        id_clinica
        title
        
        Status se genera automatico
        """
        id_clinica = jeison["id_clinica"]
        title = jeison["title"]

        values = (id_clinica, title)

        try:
            self.cur.execute("INSERT INTO Departamentos VALUES (%s, %s);", values)
            self.conn.commit()
        except:
            return "Error"
        return "Departamento creado"


    """
    Funciones de la API 
    """

    def getActividades(self, jeison):
        """
        Retorna las actividades de un usuario
        REQS:
        token
        RET:
        status bool : request es correcto o no segun token
        """
        tagSearch = False # Buscar un solo tipo de tag.
        token = jeison["token"]
        result = {"actividades" : list(), "status": 0}
        if "tag" in jeison:
            tagSearch = True

        # {
        # "nombre": None,
        # "fecha": None, 
        # "tipo": None,
        # "tags": [],
        # "reflexion": None,
        # "id": None
        # }

        self.cur.execute("""
            SELECT id FROM Usuarios WHERE token = %s;
            """,(token,))
        id_usuario = self.cur.fetchone()[0]

        if not tagSearch:
            actividades = self.cur.execute("""
                SELECT titulo, fecha, fecha_registro, tipo, reflexion, id FROM Actividades WHERE id_usuario = %s;
                """, (id_usuario,))
        else:
            actividades = self.cur.execute("""
                SELECT titulo, fecha, fecha_registro, tipo, reflexion, id 
                FROM Actividades 
                INNER JOIN HasTag 
                ON HasTag.id_actividad = Actividades.id 
                WHERE id_usuario = %s
                AND id_tag = %s;
                """, (id_usuario, jeison["tag"]))

        for actividad in self.cur:
            actividad = {
                    "titulo": actividad[0],
                    "fecha": str(actividad[1]),
                    "fecha_registro": str(actividad[2]), 
                    "tipo": actividad[3],
                    "tags": self._getTags(actividad[5]),
                    "reflexion": actividad[4],
                    "id": actividad[5]
                    }
            result["actividades"].append(actividad)

        for actividad in result["actividades"]:
            newCursor = self.conn.cursor()
            newCursor.execute("""
                SELECT Tipos.titulo, Tipos.value FROM Actividades
                INNER JOIN Tipos
                ON Tipos.id = Actividades.tipo
                WHERE Tipos.id = %s;
                """, (actividad["tipo"],))
            actividad["tipo"] = newCursor.fetchone()


        return result

    def addActividad(self, jeison):
        """
        POST
        Agrega una nueva actividad a un usuario
        1 o 0 si la insercion fue correcta o no.
        REQS:
        id_usuario int
        fecha timestamp
        titulo text
        tipo int
        reflexion text

        """
        result = {"status": 0}

        for key in ["token", "fecha", "titulo", "tipo", "reflexion", "tags"]:
            if key not in jeison:
                return json.dumps({"status": 0})

        try:
            token = jeison["token"]
            self.cur.execute("""
                            SELECT id FROM Usuarios WHERE token = %s;
                            """,(token,))
            id_usuario = self.cur.fetchone()[0]

            fecha_registro = datetime.datetime.now()
            self.cur.execute("""
                INSERT INTO Actividades(id_usuario, 
                            titulo, fecha, fecha_registro, tipo, 
                            reflexion) VALUES(%s, %s, %s, %s, %s, %s);
                """,(id_usuario, jeison["titulo"], jeison["fecha"], fecha_registro, jeison["tipo"], jeison["reflexion"]))
            self.conn.commit()
            result["status"] = 1
        except Exception as e:
            print("Error: {}".format(e))
            return result

        #Linkear tags a la actividad
        self.cur.execute("""SELECT id
                        FROM Actividades 
                        WHERE id_usuario = %s
                        AND titulo = %s
                        AND fecha_registro = %s""", 
                        (id_usuario, jeison["titulo"], fecha_registro)
                        )    
        id_actividad = self.cur.fetchone()[0]
        for tag in jeison["tags"]:
            self.cur.execute("INSERT INTO HasTag (id_actividad, id_tag) VALUES (%s,%s);", (id_actividad,tag))
            self.conn.commit()


        return result

    def removeActividad(self, jeison):
        """
        Eliminar una actividad de un usuario
        REQS
        token
        id_actividad
        """
        result = {"status": 0}
        token = jeison["token"]
        id_actividad = jeison["id_actividad"]
        self.cur.execute("""SELECT id
                            FROM Usuarios
                            WHERE token = %s;
                            """,
                            (token,)
                            )
        id_usuario = self.cur.fetchone()[0]
        if id_usuario == None:
            return result
        
        self.cur.execute("DELETE FROM HasTag WHERE id_actividad = %s;", (id_actividad,))
        self.cur.execute("DELETE FROM Actividades WHERE id = %s;", (id_actividad,))
        self.conn.commit()

        result["status"] = 1
        return result

    # TO DO
    def getAllUsers(self, jeison):
        """
        Retorna todos los datos de todos los usuarios
        Excepto id, token, clave y salt
        """
        result = {"status": 1, "users": list()}
        token = jeison["token"]

        self.cur.execute("""SELECT id
                            FROM Usuarios
                            WHERE token = %s;
                            """,
                            (token,)
                            )
        id_usuario = self.cur.fetchone()[0]

        self.cur.execute("""SELECT id_departamento
                            FROM AdminDepartamento
                            WHERE id_usuario = %s""",
                            (id_usuario,)
                            )
        id_departamento = self.cur.fetchone()[0]

        if id_departamento == None:
            return result

        # Continuar
        self.cur.execute("""SELECT nombre, ocupacion, token
                            FROM Usuarios
                            WHERE id_departamento = %s;
                        """, (id_departamento,))
        for user in self.cur:
            new_user = {"nombre": user[0], "ocupacion": user[1]}
            token = user[2]
            new_user["tags"] = self.getTagsInfo({"token": token})["tags"]

            result["users"].append(new_user)


        return result




    # En testeo
    def getTagsInfo(self, jeison):
        """
        Obtiene la informacion de los tags de una persona
        /getTagsInfo
        """
        modo = 0
        if "modo" in jeison:
            modo = jeison["modo"]

        result = {"status": 0, "tags": list()}
        token = jeison["token"]
        print(token)
        self.cur.execute("""SELECT id
                            FROM Usuarios
                            WHERE token = %s;
                            """,
                            (token,)
                            )
        id_usuario = self.cur.fetchone()[0]

        # Reutilizar codigo de getTags #
        self.cur.execute("SELECT * FROM Tags;")
        tags = {"tags": [{"id": x[0], "titulo": x[1], "puntaje_usuario": x[2], "descripcion": x[3], "meta": x[4], "color": x[5]}  for x in self.cur]}
        ################################

        final_tags = {"tags": list()}
        for tag in tags["tags"]:
            if modo == 0:
                self.cur.execute("""SELECT COUNT(*) 
                                    FROM Actividades
                                    INNER JOIN HasTag
                                    ON Actividades.id = HasTag.id_actividad 
                                    WHERE HasTag.id_tag = %s;""", 
                                    (tag["id"],))
            elif modo == 1:
                self.cur.execute("""SELECT COUNT(*) 
                                    FROM Actividades
                                    INNER JOIN HasTag
                                    ON Actividades.id = HasTag.id_actividad 
                                    WHERE HasTag.id_tag = %s
                                    AND reflexion != '';""", 
                                    (tag["id"],))

            else:
                self.cur.execute("""SELECT COUNT(*) 
                                    FROM Actividades
                                    INNER JOIN HasTag
                                    ON Actividades.id = HasTag.id_actividad 
                                    WHERE HasTag.id_tag = %s;""", 
                                    (tag["id"],))


            suma = self.cur.fetchone()[0]
            tag["puntaje_usuario"] *= suma
            if tag["puntaje_usuario"] < tag["meta"] and modo == 2:
                continue
            else:
                final_tags["tags"].append(tag)

        return final_tags


    def getClinicas(self):
        result = {"clinicas": list()}
        clinicas = self.cur.execute("SELECT title,id FROM Clinica;")
        for clinica in self.cur:
            result["clinicas"].append({"title": clinica[0], "id": clinica[1]})

        return result


    def getDeptos(self, id_clinica):
        result = {"deptos": list()}
        deptos = self.cur.execute("SELECT title,id FROM Departamentos WHERE id_clinica = %s;", (id_clinica,))
        for depto in self.cur:
            result["deptos"].append({"title": depto[0], "id": depto[1]})

        return result

    def getTags(self):
        self.cur.execute("SELECT * FROM Tags;")
        ret = {"tags": [{"id": x[0], "titulo": x[1], "puntaje_usuario": x[2], "descripcion": x[3], "meta": x[4], "color": x[5], "pico": True}  for x in self.cur]}
        ret = ret
        return ret

    def getTipos(self):
        self.cur.execute("SELECT * FROM Tipos;")
        ret = {"tipos": [{"id": x[0], "titulo": x[1], "value": x[2]}  for x in self.cur]}
        ret = ret
        return ret


    """
    Funciones de adminstrador

    """






    """
    Funciones privadas
    """
    def _getTags(self, id_actividad):
        self.cur2 = self.conn.cursor()
        tags = self.cur2.execute("""
            SELECT Tags.title, Tags.value, Tags.color FROM Tags
            INNER JOIN HasTag
            ON Tags.id = HasTag.id_tag
            WHERE HasTag.id_actividad = %s
            """, (id_actividad,))

        ret = list()
        for tag in self.cur2:
            ret.append({"title": tag[0], "value": tag[1], "color": tag[2]})

        return ret


if __name__ == "__main__":
    db = DB()

    db.poblar()
    #db.selectSimulaciones()
    db.conn.close()


