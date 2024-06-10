import sqlite3

def get_connection():
    connection = sqlite3.connect('banco_de_dados_nino_gas.db')
    return connection

def get_cursor():
    conn = get_connection()
    cursor = conn.cursor()
    return cursor