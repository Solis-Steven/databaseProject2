import psycopg2
from psycopg2 import DatabaseError

def makeConnection(pHost, pPort, pUser, pPassword, pDatabase):
    try:
        connection = psycopg2.connect(
            host= pHost,
            port = pPort,
            user= pUser,
            password= pPassword,
            database= pDatabase
        )

        print("Conexión exitosa.")
        cursor = connection.cursor()
        cursor.execute("SELECT version()")  #seleccionar version solo para comprobar que no tira error la conexion
        row = cursor.fetchone()
        print("Versión del servidor de PostgreSQL: {}".format(row))
    except DatabaseError as ex:
        print("Error durante la conexión: {}".format(ex))
    return connection
