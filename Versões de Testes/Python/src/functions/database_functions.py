import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import get_cursor, get_connection

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