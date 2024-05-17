from collections import namedtuple
import psycopg2
from psycopg2 import Error
from psycopg2.extras import RealDictCursor
from django.db import connection


def connect_to_db():
    try:
        connection = psycopg2.connect(user="basdat",
                                      password="basdat",
                                      host="localhost",
                                      port="5432",
                                      database="marmut")
        connection.autocommit = True
        return connection
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
        return None


def execute_query(query):
    cursor = connection.cursor()
    cursor.execute("set search_path to marmut")
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result
