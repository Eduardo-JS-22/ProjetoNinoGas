import sqlite3

def clear_table_and_reset_autoincrement(table_name):
    conn = sqlite3.connect('banco_de_dados_nino_gas.db')
    cursor = conn.cursor()

    # Excluir todos os dados da tabela
    cursor.execute(f"DELETE FROM {table_name}")

    # Zerar a sequência de autoincremento
    cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table_name}'")

    # Salvar as mudanças e fechar a conexão
    conn.commit()
    conn.close()

# Exemplo de uso da função
clear_table_and_reset_autoincrement('clientes')
clear_table_and_reset_autoincrement('cobrancas')
