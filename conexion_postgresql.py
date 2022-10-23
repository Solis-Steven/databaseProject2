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
        return connection
    except DatabaseError as ex:
        print("Error durante la conexión: {}".format(ex))