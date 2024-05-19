from collections import namedtuple
import psycopg2
from psycopg2 import Error
import psycopg2
from psycopg2.extras import RealDictCursor
from django.db import connection


def connect_to_db():
    try:
        connection = psycopg2.connect(
            user="postgres.guabdrzkgntpcrpwjpff",
            password="ilovemarmut20204",
            host="aws-0-ap-southeast-1.pooler.supabase.com",
            port="5432",
            database="postgres",
        )
        connection.autocommit = True
        return connection
    except Exception as error:
        print("Error while connecting to PostgreSQL", error)
        return None


def execute_query(query):
    first_word = query.split(' ')[0]
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("set search_path to marmut")
    cursor.execute(query)
    desc = cursor.description

    if first_word.lower() == 'select':
        return [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]
    cursor.close()
