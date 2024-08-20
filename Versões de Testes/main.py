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
        datetime_venda = datetime.strptime(data_venda, "%Y-%m-%d").date()
        data_vencimento = datetime_venda + timedelta(days=30)
        self.cursor.execute('''
            INSERT INTO cobrancas (cliente_id, valor_total, data_venda, data_vencimento, data_fechamento, ativo)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (cliente_id, valor_total, datetime_venda, data_vencimento, None, True))
        self.conn.commit()

    def list_clients(self):
        clientes = []
        self.cursor.execute('SELECT clientes.id, clientes.nome, clientes.endereco, clientes.telefone FROM clientes')
        for row in self.cursor.fetchall():
            clientes.append(f"{row[0]} £ {row[1]} £ {row[2]} £ {row[3]}")
        return clientes
    
    def return_client(self, cliente_id):
        self.cursor.execute("""
            SELECT clientes.nome, clientes.endereco, clientes.telefone
            FROM clientes
            WHERE id = ?
        """, (cliente_id,))
        row = self.cursor.fetchone()
        return row
    
    def list_clients_names(self):
        clientes = []
        self.cursor.execute('SELECT clientes.id, nome FROM clientes')
        for row in self.cursor.fetchall():
            clientes.append(str(row[0]) + " - " + row[1])
        return clientes

    def list_bills(self):
        cobrancas = []
        self.cursor.execute('''
            SELECT cobrancas.id, clientes.nome, cobrancas.valor_total, cobrancas.data_venda, cobrancas.data_vencimento
            FROM cobrancas
            JOIN clientes ON cobrancas.cliente_id = clientes.id
            WHERE cobrancas.ativo = 1
        ''')
        for row in self.cursor.fetchall():
            cobrancas.append(f"{row[0]} £ {row[1]} £ {row[2]} £ {row[3]} £ {row[4]}")
        return cobrancas
    
    def list_closed_bills(self):
        cobrancas = []
        self.cursor.execute('''
            SELECT cobrancas.id, clientes.nome, cobrancas.valor_total, cobrancas.data_venda, cobrancas.data_fechamento
            FROM cobrancas
            JOIN clientes ON cobrancas.cliente_id = clientes.id
            WHERE cobrancas.ativo = 0
        ''')
        for row in self.cursor.fetchall():
            cobrancas.append(f"{row[0]} £ {row[1]} £ {row[2]} £ {row[3]} £ {row[4]}")
        return cobrancas

    def close_bill(self, bill_id):
        self.cursor.execute('''
            UPDATE cobrancas
            SET data_fechamento = ?, ativo = ?
            WHERE id = ?
        ''', (datetime.now().date(), False, bill_id))
        self.conn.commit()
        #self.number_close_days(bill_id)
    
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
    
    def update_client(self, cliente_id, nome, endereco, telefone):
        self.cursor.execute('''
            UPDATE clientes
            SET nome = ?, endereco = ?, telefone = ?
            WHERE id = ?
        ''', (nome, endereco, telefone, cliente_id))
        self.conn.commit()
    
    def add_custom_bill(self):
        self.cursor.execute('''
            INSERT INTO cobrancas (cliente_id, valor_total, data_venda, data_vencimento, data_fechamento, ativo)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (2, 125, "2024-02-15", "2024-03-16", None, True))
        self.conn.commit()

    def filter_past_due_bills(self):
        cobrancas = []
        data_hoje = datetime.now().date()
        data_hoje_str = data_hoje.isoformat()

        self.cursor.execute('''
            SELECT cobrancas.id, clientes.nome, cobrancas.valor_total, cobrancas.data_venda, cobrancas.data_vencimento
            FROM cobrancas
            JOIN clientes ON cobrancas.cliente_id = clientes.id
            WHERE cobrancas.data_vencimento < ? AND cobrancas.ativo = 1
        ''', (data_hoje_str,))
        for row in self.cursor.fetchall():
            cobrancas.append(f"{row[0]} £ {row[1]} £ {row[2]} £ {row[3]} £ {row[4]}")
        return cobrancas
    
    def menu(self):
        quantidade_cobrancas_ativas = self.filtrar_quantidade_cobrancas_ativas()
        quantidade_cobrancas_vencidas = self.filtrar_quantidade_cobrancas_vencidas()
        quantidade_clientes_ativos = self.filtrar_quantidade_clientes_ativos()
        return("Total Clientes: "+str(quantidade_clientes_ativos)+"\nCobranças Ativas: "+str(quantidade_cobrancas_ativas)+"\nCobranças Vencidas: "+str(quantidade_cobrancas_vencidas))
    
    def filtrar_quantidade_cobrancas_ativas(self):
        self.cursor.execute('''
            SELECT cobrancas.id
            FROM cobrancas
            WHERE cobrancas.ativo = 1
        ''')
        rows = self.cursor.fetchall()
        return len(rows)
    
    def filtrar_quantidade_cobrancas_vencidas(self):
        data_hoje = datetime.now().date()
        data_hoje_str = data_hoje.isoformat()
        self.cursor.execute('''
            SELECT cobrancas.id, clientes.nome, cobrancas.valor_total, cobrancas.data_venda, cobrancas.data_vencimento
            FROM cobrancas
            JOIN clientes ON cobrancas.cliente_id = clientes.id
            WHERE cobrancas.data_vencimento < ? AND cobrancas.ativo = 1
        ''', (data_hoje_str,))
        rows = self.cursor.fetchall()
        return len(rows)
    
    def filtrar_quantidade_clientes_ativos(self):
        self.cursor.execute('''
            SELECT clientes.id
            FROM clientes
        ''')
        rows = self.cursor.fetchall()
        return len(rows)
    
    def filtrar_quantidade_cobrancas_fechadas(self):
        self.cursor.execute('''
            SELECT cobrancas.id, clientes.nome, cobrancas.valor_total, cobrancas.data_venda, cobrancas.data_vencimento
            FROM cobrancas
            JOIN clientes ON cobrancas.cliente_id = clientes.id
            WHERE cobrancas.ativo = 0
        ''')
        rows = self.cursor.fetchall()
        return len(rows)
    
    def buscar_cobrancas(self):
        cobrancas = []
        self.cursor.execute('''
            SELECT cobrancas.id, clientes.nome, cobrancas.valor_total, cobrancas.data_venda, cobrancas.data_vencimento
            FROM cobrancas
            JOIN clientes ON cobrancas.cliente_id = clientes.id
            WHERE cobrancas.ativo = 1
        ''')
        for row in self.cursor.fetchall():
            cobrancas.append(f"{row[0]} £ {row[1]} £ {row[2]} £ {row[3]} £ {row[4]}")
        return cobrancas
    
    def filtrar_cobrancas_por_cliente(self, cliente_id):
        cobrancas = []
        self.cursor.execute('''
            SELECT cobrancas.id, clientes.nome, cobrancas.valor_total, cobrancas.data_venda, cobrancas.data_fechamento
            FROM cobrancas
            JOIN clientes ON cobrancas.cliente_id = clientes.id
            WHERE cobrancas.ativo = 0 AND clientes.id = ?
        ''', (cliente_id,))
        for row in self.cursor.fetchall():
            cobrancas.append(f"{row[0]} £ {row[1]} £ {row[2]} £ {row[3]} £ {row[4]}")
        return cobrancas
    
    def get_cobrancas_by_date(self, month=None, day=None):
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
        
        self.cursor.execute(query, params)
        cobrancas = []

        for row in self.cursor.fetchall():
            cobrancas.append(f"{row[0]} £ {row[1]} £ {row[2]} £ {row[3]} £ {row[4]}")
        
        return cobrancas
    
    def delete_cobrancas(self):
        data = (datetime.now() - timedelta(days=730)).strftime('%Y-%m-%d')
        self.cursor.execute('''
            DELETE FROM cobrancas WHERE cobrancas.ativo = 0 AND cobrancas.data_fechamento <= ?
        ''', (data,))

    def update_custom_bill(self):
        self.cursor.execute('''
            UPDATE cobrancas
            SET cliente_id = 18, valor_total = 125, data_venda = ?, data_vencimento = ?
            WHERE id = 66
        ''', ('2024-08-19', '2024-09-18'))
        self.conn.commit()


    def close(self):
        self.conn.close()

billing_system = BillingSystem()
#billing_system.add_client("Marcos Oliveira", "Rua C, 123", "47938136819")
#billing_system.list_clients()
#billing_system.add_bill(4, 105, "2024-04-24")
#billing_system.filter_past_due_bills()
#billing_system.close_bill(16)
#print(billing_system.list_bills())
#billing_system.list_clients_names()
#billing_system.update_client(7, "Alberto da Nóbrega", "Rua Alfredo Spindler, 156, Cruzeiro", "47995128436")
#print(billing_system.list_closed_bills())
#print(billing_system.filtrar_quantidade_cobrancas_fechadas())
#billing_system.delete_cobrancas()
#print(billing_system.filtrar_cobrancas_por_cliente(2))
#print(billing_system.get_cobrancas_by_date("", 3))
#print(len(billing_system.filter_past_due_bills()))
billing_system.update_custom_bill()
billing_system.close()