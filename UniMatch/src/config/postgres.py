import psycopg2

def get_connection():
    return psycopg2.connect(
        host='localhost',
        database='unimatch',
        user='postgres',
        password='postgres'
    )