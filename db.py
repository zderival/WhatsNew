import os
import psycopg2

_conn = None
#This is a singleton: an instance of something that gets shared everywhere
def get_connection():
    global _conn
    if _conn is None:
        _conn = psycopg2.connect(
        host=os.getenv("host"),
        database=os.getenv("Database_Name"),
        user=os.getenv("Database_Username"),
        password=os.getenv("Database_Password")
)
    return _conn