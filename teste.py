import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect('banco_de_dados_nino_gas.db')
cursor = conn.cursor()

day = '26'
month = ''

query = '''
    SELECT cobrancas.id, clientes.nome, cobrancas.valor_total, cobrancas.data_venda, cobrancas.data_fechamento
    FROM cobrancas
    JOIN clientes ON cobrancas.cliente_id = clientes.id
    WHERE cobrancas.ativo = 0
'''
params = []

if month and day:
    query += ' AND strftime("%m", cobrancas.data_fechamento) = ? AND strftime("%d", cobrancas.data_fechamento) = ?'
    params.extend([f'{month:02}', f'{day:02}'])
elif month:
    query += ' AND strftime("%m", cobrancas.data_fechamento) = ?'
    params.append(f'{month:02}')
elif day:
    query += ' AND strftime("%d", cobrancas.data_fechamento) = ?'
    params.append(f'{day:02}')

query += 'ORDER BY cobrancas.data_fechamento'
        
cursor.execute(query, params)
cobrancas = []

for row in cursor.fetchall():
    cobrancas.append(f"{row[0]} £ {row[1]} £ {row[2]} £ {row[3]} £ {row[4]}")
        
print(cobrancas)     

# Commit e fechar a conexão
conn.commit()
conn.close()
