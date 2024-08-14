import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from functions.database_functions import *

def add_client(nome, nota, endereco, telefone):
    function_string = '''
        INSERT INTO clientes (nome, nota, endereco, telefone)
        VALUES (?, ?, ?, ?)
    ''', (nome, nota, endereco, telefone)
    add_data(function_string)
    
def list_clients():
    function_string = 'SELECT * FROM clientes'
    list_data(function_string)