import sqlite3
from datetime import datetime, timedelta

class BillingSystem:
    def __init__(self, db_name='banco_de_dados_nino_gas.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def add_client(self, nome, endereco, telefone):
        self.cursor.execute('''
            INSERT INTO clientes (nome, nota, endereco, telefone)
            VALUES (?, ?, ?, ?)
        ''', (nome, 0, endereco, telefone))
        self.conn.commit()

    def add_bill(self, cliente_id, valor_total, data_venda):
        data_vencimento = data_venda + timedelta(days=30)
        self.cursor.execute('''
            INSERT INTO cobrancas (cliente_id, valor_total, data_venda, data_vencimento, data_fechamento, ativo)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (cliente_id, valor_total, data_venda, data_vencimento, None, True))
        self.conn.commit()

    def list_clients(self):
        self.cursor.execute('SELECT * FROM clientes')
        for row in self.cursor.fetchall():
            print(row)

    def list_bills(self):
        self.cursor.execute('''
            SELECT cobrancas.id, clientes.nome, cobrancas.valor_total, cobrancas.data_venda, cobrancas.data_vencimento, cobrancas.data_fechamento, cobrancas.ativo
            FROM cobrancas
            JOIN clientes ON cobrancas.cliente_id = clientes.id
        ''')
        for row in self.cursor.fetchall():
            print(row)

    def close_bill(self, bill_id):
        self.cursor.execute('''
            UPDATE cobrancas
            SET data_fechamento = ?, ativo = ?
            WHERE id = ?
        ''', (datetime.now().date(), False, bill_id))
        self.conn.commit()
        self.number_close_days(bill_id)
    
    def number_close_days(self, bill_id):
        self.cursor.execute('''
            SELECT data_vencimento, data_fechamento, cliente_id
            FROM cobrancas
            WHERE id = ?
        ''', (bill_id,))

        row = self.cursor.fetchone()
        if row:
            date1 = datetime.strptime(row[0], "%Y-%m-%d")
            date2 = datetime.strptime(row[1], "%Y-%m-%d")
            difference = date2 - date1
            days_between = difference.days
            if days_between > 0 and days_between > 15 and days_between <= 30:
                self.update_user_score(row[2], 1)
            elif days_between > 0 and days_between > 30:
                self.update_user_score(row[2], 2)
    
    def update_user_score(self, user_id, score):
        self.cursor.execute('''
            UPDATE clientes
            SET nota = ?
            WHERE id = ?
        ''', (score, user_id))
        self.conn.commit()
    
    def add_custom_bill(self):
        self.cursor.execute('''
            INSERT INTO cobrancas (cliente_id, valor_total, data_venda, data_vencimento, data_fechamento, ativo)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (2, 125, "2024-02-15", "2024-03-16", None, True))
        self.conn.commit()

    def close(self):
        self.conn.close()

# Exemplo de uso
billing_system = BillingSystem()

# Adicionar clientes
#billing_system.add_client("João Silva", 8, "Rua A, 123", "41987654321")
#billing_system.add_client("Maria Oliveira", 9, "Rua B, 456", "41987654322")

# Listar clientes
#billing_system.list_clients()

# Adicionar cobranças
#billing_system.add_bill(1, 100.0, "2023-06-30", "2023-07-30", None, True)
#billing_system.add_bill(2, 150.0, "2023-06-29", "2023-07-29", None, True)

billing_system.close_bill(8)

# Listar cobranças com nomes de clientes
#billing_system.list_bills()

# Fechar a conexão
billing_system.close()


#Filtrar as cobranças que vencenram (data_fechamento maior que a data de hoje)