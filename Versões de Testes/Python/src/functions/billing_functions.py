import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from functions.database_functions import *

def add_bill(cliente_id, valor_total, data_venda, data_vencimento, data_fechamento, ativo):
    function_string = '''
        INSERT INTO cobrancas (cliente_id, valor_total, data_venda, data_vencimento, data_fechamento, ativo)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (cliente_id, valor_total, data_venda, data_vencimento, data_fechamento, ativo)
    add_data(function_string)

def list_bills():
    function_string = '''
        SELECT cobrancas.id, clientes.nome, cobrancas.valor_total, cobrancas.data_venda, cobrancas.data_vencimento, cobrancas.data_fechamento, cobrancas.ativo
        FROM cobrancas
        JOIN clientes ON cobrancas.cliente_id = clientes.id
    '''
    list_data(function_string)