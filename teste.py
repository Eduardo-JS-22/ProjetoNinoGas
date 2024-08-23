import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect('banco_de_dados_nino_gas.db')
cursor = conn.cursor()

clientes = []
cursor.execute('SELECT clientes.id FROM clientes')
for row in cursor.fetchall():
    cursor.execute('''
        SELECT 
            cliente_id,
            SUM(valor_total) AS soma_valor_total, 
            MIN(data_venda) AS data_venda_mais_antiga, 
            MIN(data_vencimento) AS data_vencimento_mais_antiga
        FROM 
            cobrancas
        WHERE
            cliente_id = ? AND ativo = 1
        GROUP BY 
            cliente_id;
    ''', (row[0],))
    result = cursor.fetchone()
    if (result != None):
        cursor.execute('''
            UPDATE clientes
            SET valor_total = ?, data_venda = ?, data_vencimento = ?
            WHERE id = ?
        ''', (result[1], result[2], result[3], row[0]))
    else:
        cursor.execute('''
            UPDATE clientes
            SET valor_total = NULL, data_venda = NULL, data_vencimento = NULL
            WHERE id = ?
        ''', (row[0],))

# Commit e fechar a conexão
conn.commit()
conn.close()
