import sys, sqlite3
from PyQt5.QtWidgets import QComboBox, QHeaderView, QTableWidget, QTableWidgetItem, QMessageBox, QLineEdit, QFormLayout, QApplication, QMainWindow, QToolBar, QDockWidget, QLabel, QStackedWidget, QWidget, QVBoxLayout, QListWidget, QPushButton, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from datetime import datetime, timedelta

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.billing_system = BillingSystem()
        self.billing_system.delete_cobrancas()
        self.bills = []
        self.clients = None
        self.nome_input = QLineEdit()
        self.nome_input.setStyleSheet('font-size: 24px')
        self.endereco_input = QLineEdit()
        self.endereco_input.setStyleSheet('font-size: 24px')
        self.telefone_input = QLineEdit()
        self.telefone_input.setStyleSheet('font-size: 24px')
        self.cliente_id_input = QLineEdit()
        self.cliente_id_input.setStyleSheet('font-size: 24px')
        self.valor_input = QLineEdit()
        self.valor_input.setStyleSheet('font-size: 24px')
        self.data_venda_input = QLineEdit()
        self.data_venda_input.setStyleSheet('font-size: 24px')
        self.month_date = QComboBox()
        self.month_date.setStyleSheet('font-size: 24px')
        self.day_date = QComboBox()
        self.day_date.setStyleSheet('font-size: 24px')
        self.day_date.addItem("")
        self.month_date.addItem("")

        days = list(range(1, 32))
        months = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        self.month_to_number = {month: index + 1 for index, month in enumerate(months)}

        for day in days:
            self.day_date.addItem(str(day))
        
        for month in months:
            self.month_date.addItem(month)

        # Configurações da janela principal
        self.setWindowTitle("Controle de Cobranças")
        self.setWindowIcon(QIcon('logo.png'))
        self.setGeometry(100, 100, 1280, 720)

        # Paleta de cores para o menu superior
        self.setStyleSheet("""
            QMainWindow {
                background-color: white;
            }
            QToolBar {
                background-color: orange;         
                color: white;
                height: 10%;
                font-size: 24px;
            }
            QToolButton {
                background-color: white;
                color: orange;
                border: none;
                font-size: 30px;
                margin: 5px;
                padding: 10px;
                width: 150px;
                height: 40px;
            }
            QToolButton:hover {
                background-color: lightgray;
            }
            QLabel {
                font-size: 48px;
                color: black;
            }
            QPushButton {
                background-color: orange;
                color: white;
                border: none;
                font-size: 24px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: darkorange;
            }
            QListWidget {
                border: 2px solid black;
                background: white;
                font-size: 16px;
            }
            QListWidget QScrollBar {
                background: lightgray;
            }
            QListView::item:selected {
                background: lightgray;
            }
            QTableWidget {
                font-size: 24px;
            }
        """)

        # Criando a barra de ferramentas
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)  # Impede que a barra de ferramentas seja movida
        self.addToolBar(Qt.TopToolBarArea, toolbar)

        # Cria um widget contêiner e define um layout horizontal
        container_widget = QWidget()
        layout = QHBoxLayout(container_widget)
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margens do layout

        # Adicionando título "Nino Gás"
        btn_inicial = QPushButton("Menu", self)
        btn_inicial.clicked.connect(lambda: self.show_page("Página Inicial"))
        layout.addWidget(btn_inicial)

        # Adicionando botões na barra de ferramentas
        btn_clientes = QPushButton("Clientes", self)
        btn_clientes.clicked.connect(lambda: self.show_page("Clientes"))
        layout.addWidget(btn_clientes)

        btn_cobrancas = QPushButton("Cobranças", self)
        btn_cobrancas.clicked.connect(lambda: self.show_page("Cobranças"))
        layout.addWidget(btn_cobrancas)

        btn_relatorios = QPushButton("Histórico", self)
        btn_relatorios.clicked.connect(lambda: self.show_page("Histórico"))
        layout.addWidget(btn_relatorios)

        # Define uma política de tamanho para que os botões preencham a largura disponível
        for btn in [btn_inicial, btn_clientes, btn_cobrancas, btn_relatorios]:
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        # Adiciona o widget contêiner à barra de ferramentas
        toolbar.addWidget(container_widget)

        # Stack para trocar entre as páginas
        self.stack = QStackedWidget(self)
        self.setCentralWidget(self.stack)

        # Páginas
        self.pages = {}
        for page_name in ["Página Inicial", "Clientes", "Cobranças", "Histórico"]:
            page = QWidget()
            self.page_layout = QVBoxLayout(page)
            self.button_layout = QHBoxLayout()

            if page_name == "Página Inicial":
                self.table_past_bills = QTableWidget()
                self.table_past_bills.setFont(QFont("Arial", 12))
                titulo = QLabel("Cobranças Vencidas", self)
                titulo.setAlignment(Qt.AlignCenter)
                self.page_layout.addWidget(titulo)
                self.page_layout.addWidget(self.table_past_bills)
                self.load_data_past_bills()
                        
                header = self.table_past_bills.horizontalHeader()
                header.setSectionResizeMode(QHeaderView.Stretch)

                copy_bills = QPushButton("Copiar Todas as Cobranças", self)
                copy_bills.clicked.connect(self.copy_cobrancas)
                self.button_layout.addWidget(copy_bills)
                copy_won_bills = QPushButton("Copiar Cobranças Vencidas", self)
                copy_won_bills.clicked.connect(self.copy_cobrancas_vencidas)
                self.button_layout.addWidget(copy_won_bills)

                self.page_layout.addLayout(self.button_layout)

            elif page_name == "Clientes":
                titulo = QLabel("Clientes", self)
                titulo.setAlignment(Qt.AlignCenter)
                self.page_layout.addWidget(titulo)
                client_container_widget = QWidget()
                client_layout = QHBoxLayout(client_container_widget)
                client_layout.setContentsMargins(0, 0, 0, 0)

                self.table_clients = QTableWidget()
                self.table_clients.setFont(QFont("Arial", 12))
                self.page_layout.addWidget(self.table_clients)
                self.load_data_clients()
                self.table_clients.cellClicked.connect(self.client_cell_was_clicked)

                header = self.table_clients.horizontalHeader()
                header.setSectionResizeMode(QHeaderView.Stretch)

                new_client_button = QPushButton("Adicionar Novo Cliente", self)
                new_client_button.clicked.connect(self.dock_new_client)
                self.button_layout.addWidget(new_client_button)
                edit_client_button = QPushButton("Editar Cliente Selecionado", self)
                edit_client_button.clicked.connect(self.dock_edit_client)
                self.button_layout.addWidget(edit_client_button)
                self.page_layout.addLayout(self.button_layout)
            elif page_name == "Cobranças":
                titulo = QLabel("Cobranças", self)
                titulo.setAlignment(Qt.AlignCenter)
                self.page_layout.addWidget(titulo)
                self.table_bills = QTableWidget()
                self.table_bills.setFont(QFont("Arial", 12))
                self.page_layout.addWidget(self.table_bills)
                self.load_data_bills()
                self.table_bills.cellClicked.connect(self.bill_cell_was_clicked)

                header = self.table_bills.horizontalHeader()
                header.setSectionResizeMode(QHeaderView.Stretch)

                copy_bills = QPushButton("Copiar Cobranças", self)
                copy_bills.clicked.connect(self.copy_cobrancas)
                self.button_layout.addWidget(copy_bills)
                copy_won_bills = QPushButton("Copiar Cobranças Vencidas", self)
                copy_won_bills.clicked.connect(self.copy_cobrancas_vencidas)
                self.button_layout.addWidget(copy_won_bills)
                create_bill_button = QPushButton("Criar Nova Cobrança", self)
                create_bill_button.clicked.connect(self.dock_new_bill)
                self.button_layout.addWidget(create_bill_button)
                close_bill_button = QPushButton("Fechar Cobranças Selecionadas", self)
                close_bill_button.clicked.connect(self.close_cobrancas_selecionadas)
                self.button_layout.addWidget(close_bill_button)

                self.page_layout.addLayout(self.button_layout)
            else:
                titulo = QLabel("Histórico", self)
                titulo.setAlignment(Qt.AlignCenter)
                self.page_layout.addWidget(titulo)
                self.table_closed_bills = QTableWidget()
                self.table_closed_bills.setFont(QFont("Arial", 12))
                self.page_layout.addWidget(self.table_closed_bills)
                self.load_data_closed_bills()

                header = self.table_closed_bills.horizontalHeader()
                header.setSectionResizeMode(QHeaderView.Stretch)

                filter_closed_bill_name = QPushButton("Filtrar Por Cliente", self)
                filter_closed_bill_name.clicked.connect(self.dock_filter_closed_bill_name)
                self.button_layout.addWidget(filter_closed_bill_name)
                filter_closed_bill_date = QPushButton("Filtrar Por Data", self)
                filter_closed_bill_date.clicked.connect(self.dock_filter_closed_bill_date)
                self.button_layout.addWidget(filter_closed_bill_date)

                self.page_layout.addLayout(self.button_layout)

            self.stack.addWidget(page)
            self.pages[page_name] = page

    def show_page(self, page_name):
        self.stack.setCurrentWidget(self.pages[page_name])

    def update_data(self):
        self.table_past_bills.clear()
        self.load_data_past_bills()
        self.table_clients.clear()
        self.load_data_clients()
        self.table_bills.clear()
        self.load_data_bills()
        self.table_closed_bills.clear()
        self.load_data_closed_bills()
        self.nome_input.clear()
        self.endereco_input.clear()
        self.telefone_input.clear()
        self.cliente_id_input.clear()
        self.valor_input.clear()
        self.data_venda_input.clear()
        data_hoje = datetime.now().date()
        data_hoje_str = data_hoje.isoformat()
        data_atual = datetime.strptime(data_hoje_str, "%Y-%m-%d")
        self.data_venda_input.setText(data_atual.strftime("%d/%m/%Y"))

    def load_data_clients(self):
        self.table_clients.setColumnCount(4)
        self.table_clients.setRowCount(30 if self.billing_system.filtrar_quantidade_clientes_ativos() < 30 else self.billing_system.filtrar_quantidade_clientes_ativos())
        self.table_clients.setHorizontalHeaderLabels(["Cliente", "Nome", "Endereço", "Telefone"])

        clientes = self.billing_system.list_clients()
        for i in range(len(clientes)):
            self.table_clients.setItem(i, 0, QTableWidgetItem(str(clientes[i].split('£')[0].strip())))
            self.table_clients.setItem(i, 1, QTableWidgetItem(str(clientes[i].split('£')[1].strip())))
            self.table_clients.setItem(i, 2, QTableWidgetItem(str(clientes[i].split('£')[2].strip())))
            self.table_clients.setItem(i, 3, QTableWidgetItem(str(clientes[i].split('£')[3].strip())))

    def load_data_bills(self):
        self.table_bills.setColumnCount(5)
        self.table_bills.setRowCount(30 if self.billing_system.filtrar_quantidade_cobrancas_ativas() < 30 else self.billing_system.filtrar_quantidade_cobrancas_ativas())
        self.table_bills.setHorizontalHeaderLabels(["Venda", "Cliente", "Valor Total", "Data de Venda", "Data de Vencimento"])

        cobrancas = self.billing_system.list_bills()
        for i in range(len(cobrancas)):
            data_venda = datetime.strptime(str(cobrancas[i].split('£')[3].strip()), "%Y-%m-%d")
            data_vencimento = datetime.strptime(str(cobrancas[i].split('£')[4].strip()), "%Y-%m-%d")
            self.table_bills.setItem(i, 0, QTableWidgetItem(str(cobrancas[i].split('£')[0].strip())))
            self.table_bills.setItem(i, 1, QTableWidgetItem(str(cobrancas[i].split('£')[1].strip())))
            self.table_bills.setItem(i, 2, QTableWidgetItem(str(cobrancas[i].split('£')[2].strip())))
            self.table_bills.setItem(i, 3, QTableWidgetItem(data_venda.strftime("%d/%m/%Y")))
            self.table_bills.setItem(i, 4, QTableWidgetItem(data_vencimento.strftime("%d/%m/%Y")))
    
    def load_data_closed_bills(self):
        self.table_closed_bills.setColumnCount(5)
        self.table_closed_bills.setRowCount(30 if self.billing_system.filtrar_quantidade_cobrancas_fechadas() < 30 else self.billing_system.filtrar_quantidade_cobrancas_fechadas())
        self.table_closed_bills.setHorizontalHeaderLabels(["Venda", "Cliente", "Valor Total", "Data de Venda", "Data de Pagamento"])

        cobrancas = self.billing_system.list_closed_bills()
        for i in range(len(cobrancas)):
            data_venda = datetime.strptime(str(cobrancas[i].split('£')[3].strip()), "%Y-%m-%d")
            data_pagamento = datetime.strptime(str(cobrancas[i].split('£')[4].strip()), "%Y-%m-%d")
            self.table_closed_bills.setItem(i, 0, QTableWidgetItem(str(cobrancas[i].split('£')[0].strip())))
            self.table_closed_bills.setItem(i, 1, QTableWidgetItem(str(cobrancas[i].split('£')[1].strip())))
            self.table_closed_bills.setItem(i, 2, QTableWidgetItem(str(cobrancas[i].split('£')[2].strip())))
            self.table_closed_bills.setItem(i, 3, QTableWidgetItem(data_venda.strftime("%d/%m/%Y")))
            self.table_closed_bills.setItem(i, 4, QTableWidgetItem(data_pagamento.strftime("%d/%m/%Y")))
        
    def load_data_past_bills(self):
        self.table_past_bills.setColumnCount(5)
        self.table_past_bills.setRowCount(len(self.billing_system.filter_past_due_bills()) if len(self.billing_system.filter_past_due_bills()) > 30 else 30)
        self.table_past_bills.setHorizontalHeaderLabels(["Venda", "Cliente", "Valor Total", "Data de Venda", "Data de Vencimento"])

        cobrancas = self.billing_system.filter_past_due_bills()
        for i in range(len(cobrancas)):
            data_venda = datetime.strptime(str(cobrancas[i].split('£')[3].strip()), "%Y-%m-%d")
            data_vencimento = datetime.strptime(str(cobrancas[i].split('£')[4].strip()), "%Y-%m-%d")
            self.table_past_bills.setItem(i, 0, QTableWidgetItem(str(cobrancas[i].split('£')[0].strip())))
            self.table_past_bills.setItem(i, 1, QTableWidgetItem(str(cobrancas[i].split('£')[1].strip())))
            self.table_past_bills.setItem(i, 2, QTableWidgetItem(str(cobrancas[i].split('£')[2].strip())))
            self.table_past_bills.setItem(i, 3, QTableWidgetItem(data_venda.strftime("%d/%m/%Y")))
            self.table_past_bills.setItem(i, 4, QTableWidgetItem(data_vencimento.strftime("%d/%m/%Y")))

    def load_data_closed_bills_filter_name(self, cliente_id):
        self.table_closed_bills.setColumnCount(5)
        self.table_closed_bills.setRowCount(30 if self.billing_system.filtrar_quantidade_cobrancas_fechadas() < 30 else self.billing_system.filtrar_quantidade_cobrancas_fechadas())
        self.table_closed_bills.setHorizontalHeaderLabels(["Venda", "Cliente", "Valor Total", "Data de Venda", "Data de Pagamento"])

        cobrancas = self.billing_system.filtrar_cobrancas_por_cliente(cliente_id)
        for i in range(len(cobrancas)):
            data_venda = datetime.strptime(str(cobrancas[i].split('£')[3].strip()), "%Y-%m-%d")
            data_pagamento = datetime.strptime(str(cobrancas[i].split('£')[4].strip()), "%Y-%m-%d")
            self.table_closed_bills.setItem(i, 0, QTableWidgetItem(str(cobrancas[i].split('£')[0].strip())))
            self.table_closed_bills.setItem(i, 1, QTableWidgetItem(str(cobrancas[i].split('£')[1].strip())))
            self.table_closed_bills.setItem(i, 2, QTableWidgetItem(str(cobrancas[i].split('£')[2].strip())))
            self.table_closed_bills.setItem(i, 3, QTableWidgetItem(data_venda.strftime("%d/%m/%Y")))
            self.table_closed_bills.setItem(i, 4, QTableWidgetItem(data_pagamento.strftime("%d/%m/%Y")))
    
    def load_data_closed_bills_filter_date(self, dia, mes):
        self.table_closed_bills.setColumnCount(5)
        self.table_closed_bills.setRowCount(30 if self.billing_system.filtrar_quantidade_cobrancas_fechadas() < 30 else self.billing_system.filtrar_quantidade_cobrancas_fechadas())
        self.table_closed_bills.setHorizontalHeaderLabels(["Venda", "Cliente", "Valor Total", "Data de Venda", "Data de Pagamento"])

        cobrancas = self.billing_system.get_cobrancas_by_date(self.month_to_number.get(mes) if mes != "" else "", int(dia) if dia != "" else "")
        for i in range(len(cobrancas)):
            data_venda = datetime.strptime(str(cobrancas[i].split('£')[3].strip()), "%Y-%m-%d")
            data_pagamento = datetime.strptime(str(cobrancas[i].split('£')[4].strip()), "%Y-%m-%d")
            self.table_closed_bills.setItem(i, 0, QTableWidgetItem(str(cobrancas[i].split('£')[0].strip())))
            self.table_closed_bills.setItem(i, 1, QTableWidgetItem(str(cobrancas[i].split('£')[1].strip())))
            self.table_closed_bills.setItem(i, 2, QTableWidgetItem(str(cobrancas[i].split('£')[2].strip())))
            self.table_closed_bills.setItem(i, 3, QTableWidgetItem(data_venda.strftime("%d/%m/%Y")))
            self.table_closed_bills.setItem(i, 4, QTableWidgetItem(data_pagamento.strftime("%d/%m/%Y")))

    def copy_cobrancas_vencidas(self):
        cobrancas_vencidas = self.billing_system.filter_past_due_bills()
        if (len(cobrancas_vencidas) > 0):
            list_cobrancas = []
            list_cobrancas.append("- Venda | Cliente | Valor | Data da Venda")

            comprimento = 0

            for item in cobrancas_vencidas:
                cobranca = item.split('£')
                if (comprimento < len(cobranca[1])):
                    comprimento = len(cobranca[1])
            
            for item in cobrancas_vencidas:
                cobranca = item.split('£')
                data_venda = datetime.strptime(str(cobranca[3].strip()), "%Y-%m-%d")
                list_cobrancas.append(f"- {{:>2}} | {{:<{comprimento}}} | {{:>4}} | {{:<10}}".format(cobranca[0], cobranca[1], cobranca[2], data_venda.strftime("%d/%m/%Y")))

            clipboard = QApplication.clipboard()
            clipboard.setText("\n".join(list_cobrancas))
            QMessageBox.information(self, "Info", "Cobranças vencidas copiadas para área de transferência.")
        else:
            QMessageBox.warning(self, "Erro", "Não há cobranças vencidas para copiar.")

    def copy_cobrancas(self):
        cobrancas = self.billing_system.buscar_cobrancas()
        if (len(cobrancas) > 0):
            list_cobrancas = []
            list_cobrancas.append("- Venda | Cliente | Valor | Data da Venda")

            comprimento = 0

            for item in cobrancas:
                cobranca = item.split('£')
                if (comprimento < len(cobranca[1])):
                    comprimento = len(cobranca[1])
            
            for item in cobrancas:
                cobranca = item.split('£')
                data_venda = datetime.strptime(str(cobranca[3].strip()), "%Y-%m-%d")
                list_cobrancas.append(f"- {{:>2}} | {{:<{comprimento}}} | {{:>4}} | {{:<10}}".format(cobranca[0], cobranca[1], cobranca[2], data_venda.strftime("%d/%m/%Y")))

            clipboard = QApplication.clipboard()
            clipboard.setText("\n".join(list_cobrancas))
            QMessageBox.information(self, "Info", "Cobranças copiadas para área de transferência.")
        else:
            QMessageBox.warning(self, "Erro", "Não há cobranças para copiar.")
    
    def client_cell_was_clicked(self, row):
        self.clients = self.table_clients.item(row, 0).text()
    
    def copy_clientes_selecionadas(self):
        if (self.clients != None):
            clipboard = QApplication.clipboard()
            clipboard.setText(self.clients)
            self.clients = None
        else:
            QMessageBox.warning(self, "Erro", "Nenhum cliente selecionado para edição.")
    
    def bill_cell_was_clicked(self, row):
        items = self.table_bills.selectedItems()
        for i in range(len(items)):
            self.bills.append(str(self.table_bills.item(row, 0).text()))
    
    def close_cobrancas_selecionadas(self):
        cobrancas = []
        if (len(self.bills) > 0):
            for i in range(len(self.bills)):
                cobrancas.append(self.bills[i].split('-')[0].strip())
                lista_unica = list(set(cobrancas))
            
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Fechar Cobranças")
            msg_box.setText(f"Deseja fechar as cobranças: {', '.join(lista_unica)}?")
            
            fechar_button = msg_box.addButton("Fechar", QMessageBox.ActionRole)
            cancelar_button = msg_box.addButton("Cancelar", QMessageBox.RejectRole)

            msg_box.setDefaultButton(cancelar_button)

            msg_box.exec_()

            if msg_box.clickedButton() == fechar_button:
                for i in range(len(self.bills)):
                    self.billing_system.close_bill(self.bills[i].split('-')[0].strip())
                self.update_data()
                self.bills = []
            else:
                self.bills = []
        else:
            QMessageBox.warning(self, "Erro", "Nenhuma cobrança selecionada para encerrar.")
    
    def dock_new_client(self):
        dock = QDockWidget("Novo Cliente", self)
        dock.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)

        # Criar o conteúdo do dock
        dock_widget = QWidget()
        dock_layout = QFormLayout()
        salvar_button = QPushButton("Salvar")

        nome = QLabel("Nome:")
        nome.setStyleSheet('font-size: 24px')
        endereco = QLabel("Endereço:")
        endereco.setStyleSheet('font-size: 24px')
        telefone = QLabel("Telefone:")
        telefone.setStyleSheet('font-size: 24px')

        dock_layout.addRow(nome, self.nome_input)
        dock_layout.addRow(endereco, self.endereco_input)
        dock_layout.addRow(telefone, self.telefone_input)
        dock_layout.addRow(salvar_button)

        dock_widget.setLayout(dock_layout)
        dock.setWidget(dock_widget)

        # Adicionar o widget dock à janela principal
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)

        # Conectar o botão "Salvar" à função save_data
        salvar_button.clicked.connect(self.add_client)

    def dock_edit_client(self):
        if (self.clients != None):
            self.dock = QDockWidget("Editar Cliente", self)
            self.dock.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
            dados_cliente = self.billing_system.return_client(self.clients.split('-')[0].strip())

            if (dados_cliente != None):
                # Criar o conteúdo do dock
                dock_widget = QWidget()
                dock_layout = QFormLayout()

                self.nome_input = QLineEdit()
                self.endereco_input = QLineEdit()
                self.telefone_input = QLineEdit()
                salvar_button = QPushButton("Salvar")

                self.nome_input.setText(dados_cliente[0])
                self.endereco_input.setText(dados_cliente[1])
                self.telefone_input.setText(dados_cliente[2])

                self.nome_input.setStyleSheet('font-size: 24px')
                self.endereco_input.setStyleSheet('font-size: 24px')
                self.telefone_input.setStyleSheet('font-size: 24px')

                nome = QLabel("Nome:")
                nome.setStyleSheet('font-size: 24px')
                endereco = QLabel("Endereço:")
                endereco.setStyleSheet('font-size: 24px')
                telefone = QLabel("Telefone:")
                telefone.setStyleSheet('font-size: 24px')

                dock_layout.addRow(nome, self.nome_input)
                dock_layout.addRow(endereco, self.endereco_input)
                dock_layout.addRow(telefone, self.telefone_input)
                dock_layout.addRow(salvar_button)

                dock_widget.setLayout(dock_layout)
                self.dock.setWidget(dock_widget)

                # Adicionar o widget dock à janela principal
                self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock)

                # Conectar o botão "Salvar" à função save_data
                salvar_button.clicked.connect(self.edit_client)
            else:
                QMessageBox.warning(self, "Erro", "Erro ao buscar dados do cliente.")
        else:
            QMessageBox.warning(self, "Erro", "Nenhum cliente selecionado para edição.")
    
    def dock_new_bill(self):
        dock = QDockWidget("Nova Cobrança", self)
        dock.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)

        # Criar o conteúdo do dock
        dock_widget = QWidget()
        dock_layout = QFormLayout()
        self.cliente_id_input.textChanged.connect(self.on_text_changed)
        salvar_button = QPushButton("Salvar")

        cliente = QLabel("Cliente:")
        cliente.setStyleSheet('font-size: 24px')
        valor_total = QLabel("Valor Total:")
        valor_total.setStyleSheet('font-size: 24px')
        data_venda = QLabel("Data da Venda:")
        data_venda.setStyleSheet('font-size: 24px')


        dock_layout.addRow(cliente, self.cliente_id_input)
        dock_layout.addRow(valor_total, self.valor_input)
        dock_layout.addRow(data_venda, self.data_venda_input)
        dock_layout.addRow(salvar_button)

        self.suggestions_list = QListWidget(self)
        self.suggestions_list.setStyleSheet('font-size: 24px')
        self.suggestions_list.itemClicked.connect(self.on_item_clicked)
        dock_layout.addWidget(self.suggestions_list)
        self.suggestions_list.hide()
        self.data = self.billing_system.list_clients_names()

        data_hoje = datetime.now().date()
        data_hoje_str = data_hoje.isoformat()
        data_atual = datetime.strptime(data_hoje_str, "%Y-%m-%d")
        self.data_venda_input.setText(data_atual.strftime("%d/%m/%Y"))

        dock_widget.setLayout(dock_layout)
        dock.setWidget(dock_widget)

        # Adicionar o widget dock à janela principal
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)

        # Conectar o botão "Salvar" à função save_data
        salvar_button.clicked.connect(self.add_bill)

    def dock_filter_closed_bill_name(self):
        dock = QDockWidget("Filtrar Por Nome", self)
        dock.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)

        dock_widget = QWidget()
        dock_layout = QFormLayout()
        self.cliente_id_input.textChanged.connect(self.on_text_changed)
        filtrar_button = QPushButton("Filtrar Cobranças")
        copiar_button = QPushButton("Copiar Cobranças")

        cliente = QLabel("Cliente:")
        cliente.setStyleSheet('font-size: 24px')

        dock_layout.addRow(cliente, self.cliente_id_input)
        dock_layout.addRow(filtrar_button)
        dock_layout.addRow(copiar_button)

        self.suggestions_list = QListWidget(self)
        self.suggestions_list.setStyleSheet('font-size: 24px')
        self.suggestions_list.itemClicked.connect(self.on_item_clicked)
        dock_layout.addWidget(self.suggestions_list)
        self.suggestions_list.hide()
        self.data = self.billing_system.list_clients_names()

        dock_widget.setLayout(dock_layout)
        dock.setWidget(dock_widget)

        dock.visibilityChanged.connect(self.on_dock_visibility_changed)

        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)

        filtrar_button.clicked.connect(self.filter_closed_bill_name)
        copiar_button.clicked.connect(self.copy_bill_filter_name)

    def dock_filter_closed_bill_date(self):
        dock = QDockWidget("Filtrar Por Data", self)
        dock.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)

        dock_widget = QWidget()
        dock_layout = QFormLayout()
        filtrar_button = QPushButton("Filtrar Cobranças")
        copiar_button = QPushButton("Copiar Cobranças")

        dia = QLabel("Dia:")
        dia.setStyleSheet('font-size: 24px')
        mes = QLabel("Mês:")
        mes.setStyleSheet('font-size: 24px')

        dock_layout.addRow(dia, self.day_date)
        dock_layout.addRow(mes, self.month_date)
        dock_layout.addRow(filtrar_button)
        dock_layout.addRow(copiar_button)

        dock_widget.setLayout(dock_layout)
        dock.setWidget(dock_widget)

        dock.visibilityChanged.connect(self.on_dock_visibility_changed)

        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)

        filtrar_button.clicked.connect(self.filter_closed_bill_date)
        copiar_button.clicked.connect(self.copy_bill_filter_date)
    
    def on_dock_visibility_changed(self, visible):
        if not visible:
            self.update_data()
    
    def on_text_changed(self, text):
        if text:
            self.suggestions_list.clear()
            filtered_data = [item for item in self.data if text.lower() in item.lower()]
            self.suggestions_list.addItems(filtered_data)
            self.suggestions_list.show()
        else:
            self.suggestions_list.hide()
    
    def on_item_clicked(self, item):
        self.cliente_id_input.setText(item.text())
        self.suggestions_list.hide()

    def add_client(self):
        nome = self.nome_input.text()
        endereco = self.endereco_input.text()
        telefone = self.telefone_input.text()

        if (nome != None and endereco != None and telefone != None):
            self.billing_system.add_client(nome, endereco, telefone)
            self.update_data()
        else:
            QMessageBox.information(self, "Dados incompletos para cadastrar novo cliente.")
    
    def edit_client(self):
        nome = self.nome_input.text()
        endereco = self.endereco_input.text()
        telefone = self.telefone_input.text()
        cliente_id = self.clients.split('-')[0].strip()

        if (nome != None and endereco != None and telefone != None):
            self.billing_system.update_client(cliente_id, nome, endereco, telefone)
            self.update_data()
            self.clients = None
            self.dock.close()
        else:
            QMessageBox.information(self, "Erro ao atualizar cliente.")
    
    def add_bill(self):
        cliente_id = self.cliente_id_input.text()
        valor_total = self.valor_input.text()
        data_venda = self.data_venda_input.text()

        if (cliente_id != None and valor_total != None and data_venda != None):
            data_venda_converted = datetime.strptime(data_venda.strip(), "%d/%m/%Y").strftime("%Y-%m-%d")
            self.billing_system.add_bill(int(cliente_id.split('-')[0].strip()), float(valor_total), data_venda_converted)
            self.update_data()
        else:
            QMessageBox.warning(self, "Erro", "Erro ao cadastrar cobrança.")
    
    def filter_closed_bill_name(self):
        cliente_id = self.cliente_id_input.text()

        if (cliente_id != ""):
            self.table_closed_bills.clear()
            self.load_data_closed_bills_filter_name(int(cliente_id.split('-')[0].strip()))
        else:
            QMessageBox.warning(self, "Erro", "Selecione um cliente para filtrar as cobranças.")
    
    def copy_bill_filter_name(self):
        cliente_id = self.cliente_id_input.text()

        if (cliente_id != ""):
            cobrancas = self.billing_system.filtrar_cobrancas_por_cliente(int(cliente_id.split('-')[0].strip()))
            list_cobrancas = []
            list_cobrancas.append("- Venda | Cliente | Valor | Data da Venda | Data do Pagamento")

            comprimento = 0

            for item in cobrancas:
                cobranca = item.split('£')
                if (comprimento < len(cobranca[1])):
                    comprimento = len(cobranca[1])
            
            for item in cobrancas:
                cobranca = item.split('£')
                data_venda = datetime.strptime(str(cobranca[3].strip()), "%Y-%m-%d")
                data_pagamento = datetime.strptime(str(cobranca[4].strip()), "%Y-%m-%d")
                list_cobrancas.append(f"- {{:>2}} | {{:<{comprimento}}} | {{:>4}} | {{:<10}} | {{:<10}}".format(cobranca[0], cobranca[1], cobranca[2], data_venda.strftime("%d/%m/%Y"), data_pagamento.strftime("%d/%m/%Y")))
            clipboard = QApplication.clipboard()
            clipboard.setText("\n".join(list_cobrancas))
            QMessageBox.information(self, "Info", "Cobranças copiadas para área de transferência.")
        else:
            QMessageBox.warning(self, "Erro", "Erro ao copiar cobrança por cliente.")

    def filter_closed_bill_date(self):
        mes = self.month_date.currentText()
        dia = self.day_date.currentText()

        if (mes != "" or dia != ""):
            self.table_closed_bills.clear()
            self.load_data_closed_bills_filter_date(dia, mes)
        else:
            QMessageBox.warning(self, "Erro", "Selecione um dia e/ou um mês para filtrar as cobranças.")
    
    def copy_bill_filter_date(self):
        mes = self.month_date.currentText()
        dia = self.day_date.currentText()

        if (mes != "" or dia != ""):
            cobrancas = self.billing_system.get_cobrancas_by_date(self.month_to_number.get(mes) if mes != "" else "", int(dia) if dia != "" else "")
            list_cobrancas = []
            list_cobrancas.append("- Venda | Cliente | Valor | Data da Venda | Data do Pagamento")

            comprimento = 0

            for item in cobrancas:
                cobranca = item.split('£')
                if (comprimento < len(cobranca[1])):
                    comprimento = len(cobranca[1])
            
            for item in cobrancas:
                cobranca = item.split('£')
                data_venda = datetime.strptime(str(cobranca[3].strip()), "%Y-%m-%d")
                data_pagamento = datetime.strptime(str(cobranca[4].strip()), "%Y-%m-%d")
                list_cobrancas.append(f"- {{:>2}} | {{:<{comprimento}}} | {{:>4}} | {{:<10}} | {{:<10}} ".format(cobranca[0], cobranca[1], cobranca[2], data_venda.strftime("%d/%m/%Y"), data_pagamento.strftime("%d/%m/%Y")))
            clipboard = QApplication.clipboard()
            clipboard.setText("\n".join(list_cobrancas))
            QMessageBox.information(self, "Info", "Cobranças copiadas para área de transferência.")
        else:
            QMessageBox.warning(self, "Erro", "Selecione um dia e/ou um mês para filtrar as cobranças.")

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

    def close(self):
        self.conn.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
