from collections import namedtuple
import psycopg2
from psycopg2 import Error
from psycopg2.extras import RealDictCursor

def connect_to_db():
    try:
        connection = psycopg2.connect(user="",
                                      password="",
                                      host="",
                                      port="",
                                      database="")
        connection.autocommit = True
        return connection
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
        return None

connection = connect_to_db()
