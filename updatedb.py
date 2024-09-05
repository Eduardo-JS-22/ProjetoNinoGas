import sqlite3

def update_client_names():
    # Conecte-se ao banco de dados
    conn = sqlite3.connect('banco_de_dados_nino_gas.db')
    cursor = conn.cursor()

    # Selecione todos os clientes com id e nome
    cursor.execute('SELECT id, nome FROM clientes')
    clientes = cursor.fetchall()

    # Itere sobre os clientes e atualize o nome
    for cliente in clientes:
        id, nome = cliente
        novo_nome = f"{nome} - {id}"
        cursor.execute('''
            UPDATE clientes
            SET nome = ?
            WHERE id = ?
        ''', (novo_nome, id))

    # Confirme as alterações
    conn.commit()
    conn.close()

# Chame a função para atualizar os nomes dos clientes
update_client_names()
