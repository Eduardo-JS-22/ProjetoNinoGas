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
        #data_vencimento = data_venda + timedelta(days=30)
        data_vencimento = "2024-05-24"
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
            WHERe cobrancas.ativo = 1
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

    def filter_past_due_bills(self):
        data_hoje = datetime.now().date()
        data_hoje_str = data_hoje.isoformat()
        print(f"Data atual (ISO): {data_hoje_str}")

        self.cursor.execute('''
            SELECT cobrancas.id, clientes.nome, cobrancas.valor_total, cobrancas.data_venda, cobrancas.data_vencimento
            FROM cobrancas
            JOIN clientes ON cobrancas.cliente_id = clientes.id
            WHERE cobrancas.data_vencimento < ? AND cobrancas.ativo = 1
        ''', (data_hoje_str,))

        for row in self.cursor.fetchall():
            print(row)

    def close(self):
        self.conn.close()

billing_system = BillingSystem()

#billing_system.add_client("Marcos Oliveira", "Rua C, 123", "47938136819")
#billing_system.list_clients()
#billing_system.add_bill(4, 105, "2024-04-24")
#billing_system.filter_past_due_bills()
billing_system.close_bill(16)
#billing_system.list_bills()
billing_system.close()