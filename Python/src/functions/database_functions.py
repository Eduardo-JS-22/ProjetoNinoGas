from database.connection import *

def add_data(function):
    cursor = get_cursor()
    connection = get_connection()
    cursor.execute(function)
    connection.commit()

def list_data(function):
    cursor = get_cursor()
    cursor.execute(function)
    for row in cursor.fetchall():
        print(row)