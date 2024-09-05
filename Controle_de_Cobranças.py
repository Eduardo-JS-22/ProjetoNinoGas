import sys, sqlite3
from PyQt5.QtWidgets import QCompleter, QComboBox, QHeaderView, QTableWidget, QTableWidgetItem, QMessageBox, QLineEdit, QFormLayout, QApplication, QMainWindow, QToolBar, QDockWidget, QLabel, QStackedWidget, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QSizePolicy
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
        self.add_client_nome = QLineEdit()
        self.add_client_nome.setStyleSheet('font-size: 24px')
        self.add_client_endereco = QLineEdit()
        self.add_client_endereco.setStyleSheet('font-size: 24px')
        self.add_client_telefone = QLineEdit()
        self.add_client_telefone.setStyleSheet('font-size: 24px')
        self.add_client_valor = QLineEdit()
        self.add_client_valor.setStyleSheet('font-size: 24px')
        self.add_client_data = QLineEdit()
        self.add_client_data.setStyleSheet('font-size: 24px')
        self.edit_client_name = QLineEdit()
        self.edit_client_name.setStyleSheet('font-size: 24px')
        self.edit_client_endereco = QLineEdit()
        self.edit_client_endereco.setStyleSheet('font-size: 24px')
        self.edit_client_telefone = QLineEdit()
        self.edit_client_telefone.setStyleSheet('font-size: 24px')
        self.old_edit_client_name = QLineEdit()
        self.add_bill_name = QLineEdit()
        self.add_bill_name.setStyleSheet('font-size: 24px')
        self.add_bill_endereco = QLineEdit()
        self.add_bill_endereco.setStyleSheet('font-size: 24px')
        self.add_bill_endereco.setReadOnly(True)
        self.add_bill_valor = QLineEdit()
        self.add_bill_valor.setStyleSheet('font-size: 24px')
        self.add_bill_data = QLineEdit()
        self.add_bill_data.setStyleSheet('font-size: 24px')
        self.pay_bill_name = QLineEdit()
        self.pay_bill_name.setStyleSheet('font-size: 24px')
        self.pay_bill_endereco = QLineEdit()
        self.pay_bill_endereco.setStyleSheet('font-size: 24px')
        self.pay_bill_endereco.setReadOnly(True)
        self.pay_bill_valor = QLineEdit()
        self.pay_bill_valor.setStyleSheet('font-size: 24px')
        self.pay_bill_data = QLineEdit()
        self.pay_bill_data.setStyleSheet('font-size: 24px')
        self.filter_bill_name = QLineEdit()
        self.filter_bill_name.setStyleSheet('font-size: 24px')
        self.report_valor_total = QLineEdit()
        self.report_valor_total.setStyleSheet('font-size: 24px')
        self.report_valor_total.setReadOnly(True)
        self.month_date = QComboBox()
        self.month_date.setStyleSheet('font-size: 24px')
        self.month_date.addItem("")
        self.day_date = QComboBox()
        self.day_date.setStyleSheet('font-size: 24px')
        self.day_date.addItem("")
        self.dock = QDockWidget("Dock", self)

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
        self.setGeometry(100, 100, 600, 400)

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
                font-size: 12px;
            }
            QListWidget QScrollBar {
                background: lightgray;
            }
            QListView::item:selected {
                background: lightgray;
            }
            QTableWidget {
                font-size: 16px;
            }
            QDockWidget {
                width: 200px;
            }
        """)

        # Criando a barra de ferramentas
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)  # Impede que a barra de ferramentas seja movida
        self.addToolBar(Qt.TopToolBarArea, toolbar)

        container_widget = QWidget()
        layout = QHBoxLayout(container_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # Adicionando botões na barra de ferramentas
        btn_clientes = QPushButton("Cobranças Ativas", self)
        btn_clientes.clicked.connect(lambda: self.show_page("Clientes"))
        layout.addWidget(btn_clientes)

        btn_relatorios = QPushButton("Cobranças Pagas", self)
        btn_relatorios.clicked.connect(lambda: self.show_page("Histórico"))
        layout.addWidget(btn_relatorios)

        # Define uma política de tamanho para que os botões preencham a largura disponível
        for btn in [btn_clientes, btn_relatorios]:
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        # Adiciona o widget contêiner à barra de ferramentas
        toolbar.addWidget(container_widget)

        # Stack para trocar entre as páginas
        self.stack = QStackedWidget(self)
        self.setCentralWidget(self.stack)

        # Páginas
        self.pages = {}
        for page_name in ["Clientes", "Histórico"]:
            page = QWidget()
            self.page_layout = QVBoxLayout(page)
            self.button_layout = QHBoxLayout()

            if page_name == "Clientes":
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

                report_client_button = QPushButton("Relatórios", self)
                report_client_button.clicked.connect(self.dock_report_client)
                self.button_layout.addWidget(report_client_button)
                new_client_button = QPushButton("Novo Cliente", self)
                new_client_button.clicked.connect(self.dock_new_client)
                self.button_layout.addWidget(new_client_button)
                edit_client_button = QPushButton("Editar Cliente", self)
                edit_client_button.clicked.connect(self.dock_edit_client)
                self.button_layout.addWidget(edit_client_button)
                new_bill_client = QPushButton("Nova Venda", self)
                new_bill_client.clicked.connect(self.dock_new_bill)
                self.button_layout.addWidget(new_bill_client)
                pay_bill_client = QPushButton("Pagar Venda", self)
                pay_bill_client.clicked.connect(self.dock_pay_bill)
                self.button_layout.addWidget(pay_bill_client)
                self.page_layout.addLayout(self.button_layout)
            else:
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

    def load_data_clients(self):
        self.table_clients.setColumnCount(6)
        self.table_clients.setRowCount(30 if self.billing_system.filtrar_quantidade_clientes_ativos() < 30 else self.billing_system.filtrar_quantidade_clientes_ativos())
        self.table_clients.setHorizontalHeaderLabels(["Nome", "Endereço", "Telefone", "Valor Devido", "Data da Venda", "Data de Vencimento"])

        clientes = self.billing_system.list_clients()
        for i in range(len(clientes)):
            data_venda = datetime.strptime(str(clientes[i].split('£')[4].strip()), "%Y-%m-%d") if (clientes[i].split('£')[4].strip() != "None") else ""
            data_pagamento = datetime.strptime(str(clientes[i].split('£')[5].strip()), "%Y-%m-%d") if (clientes[i].split('£')[5].strip() != "None") else ""
            self.table_clients.setItem(i, 0, QTableWidgetItem(str(clientes[i].split('£')[0].strip())))
            self.table_clients.setItem(i, 1, QTableWidgetItem(str(clientes[i].split('£')[1].strip()))) if (clientes[i].split('£')[1].strip() != "None") else self.table_clients.setItem(i, 1, QTableWidgetItem(""))
            self.table_clients.setItem(i, 2, QTableWidgetItem(str(clientes[i].split('£')[2].strip()))) if (clientes[i].split('£')[2].strip() != "None") else self.table_clients.setItem(i, 2, QTableWidgetItem(""))
            self.table_clients.setItem(i, 3, QTableWidgetItem(str(clientes[i].split('£')[3].strip()))) if (clientes[i].split('£')[3].strip() != "None") else self.table_clients.setItem(i, 3, QTableWidgetItem(""))
            self.table_clients.setItem(i, 4, QTableWidgetItem(data_venda.strftime("%d/%m/%Y"))) if (data_venda != "") else self.table_clients.setItem(i, 4, QTableWidgetItem(""))
            self.table_clients.setItem(i, 5, QTableWidgetItem(data_pagamento.strftime("%d/%m/%Y"))) if (data_pagamento != "") else self.table_clients.setItem(i, 4, QTableWidgetItem(""))
    
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
        cobrancas = self.billing_system.filtrar_cobrancas_por_data(self.month_to_number.get(mes) if mes != "" else "", int(dia) if dia != "" else "")
        if (len(cobrancas) > 0):
            self.table_closed_bills.clear()
            self.table_closed_bills.setColumnCount(5)
            self.table_closed_bills.setRowCount(30 if self.billing_system.filtrar_quantidade_cobrancas_fechadas() < 30 else self.billing_system.filtrar_quantidade_cobrancas_fechadas())
            self.table_closed_bills.setHorizontalHeaderLabels(["Venda", "Cliente", "Valor Total", "Data de Venda", "Data de Pagamento"])

            for i in range(len(cobrancas)):
                data_venda = datetime.strptime(str(cobrancas[i].split('£')[3].strip()), "%Y-%m-%d")
                data_pagamento = datetime.strptime(str(cobrancas[i].split('£')[4].strip()), "%Y-%m-%d")
                self.table_closed_bills.setItem(i, 0, QTableWidgetItem(str(cobrancas[i].split('£')[0].strip())))
                self.table_closed_bills.setItem(i, 1, QTableWidgetItem(str(cobrancas[i].split('£')[1].strip())))
                self.table_closed_bills.setItem(i, 2, QTableWidgetItem(str(cobrancas[i].split('£')[2].strip())))
                self.table_closed_bills.setItem(i, 3, QTableWidgetItem(data_venda.strftime("%d/%m/%Y")))
                self.table_closed_bills.setItem(i, 4, QTableWidgetItem(data_pagamento.strftime("%d/%m/%Y")))
        else:
            QMessageBox.warning(self, "Erro", "Nenhuma cobrança encontrada para a data selecionada.")
    
    def load_data_client_pay_bills_filter_date(self, dia, mes):
        clientes = self.billing_system.get_to_load_clients_pay_by_date(self.month_to_number.get(mes) if mes != "" else "", int(dia) if dia != "" else "")
        if (len(clientes) > 0):
            self.table_clients.clear()
            self.table_clients.setColumnCount(6)
            self.table_clients.setRowCount(30 if self.billing_system.filtrar_quantidade_clientes_ativos() < 30 else self.billing_system.filtrar_quantidade_clientes_ativos())
            self.table_clients.setHorizontalHeaderLabels(["Nome", "Endereço", "Telefone", "Valor Devido", "Data da Venda", "Data de Vencimento"])

            for i in range(len(clientes)):
                data_venda = datetime.strptime(str(clientes[i].split('£')[4].strip()), "%Y-%m-%d") if (clientes[i].split('£')[4].strip() != "None") else ""
                data_pagamento = datetime.strptime(str(clientes[i].split('£')[5].strip()), "%Y-%m-%d") if (clientes[i].split('£')[5].strip() != "None") else ""
                self.table_clients.setItem(i, 0, QTableWidgetItem(str(clientes[i].split('£')[0].strip())))
                self.table_clients.setItem(i, 1, QTableWidgetItem(str(clientes[i].split('£')[1].strip()))) if (clientes[i].split('£')[1].strip() != "None") else self.table_clients.setItem(i, 1, QTableWidgetItem(""))
                self.table_clients.setItem(i, 2, QTableWidgetItem(str(clientes[i].split('£')[2].strip()))) if (clientes[i].split('£')[2].strip() != "None") else self.table_clients.setItem(i, 2, QTableWidgetItem(""))
                self.table_clients.setItem(i, 3, QTableWidgetItem(str(clientes[i].split('£')[3].strip()))) if (clientes[i].split('£')[3].strip() != "None") else self.table_clients.setItem(i, 3, QTableWidgetItem(""))
                self.table_clients.setItem(i, 4, QTableWidgetItem(data_venda.strftime("%d/%m/%Y"))) if (data_venda != "") else self.table_clients.setItem(i, 4, QTableWidgetItem(""))
                self.table_clients.setItem(i, 5, QTableWidgetItem(data_pagamento.strftime("%d/%m/%Y"))) if (data_pagamento != "") else self.table_clients.setItem(i, 4, QTableWidgetItem(""))
        else:
            QMessageBox.warning(self, "Erro", "Nenhum cliente com dívida para a data selecionada.")
    
    def client_cell_was_clicked(self, row):
        self.clients = f"{self.table_clients.item(row, 0).text()}"
    
    def dock_new_client(self):
        self.dock.close()
        self.dock = QDockWidget("Novo Cliente", self)
        self.dock.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)

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
        valor = QLabel("Valor:")
        valor.setStyleSheet('font-size: 24px')
        data = QLabel("Data:")
        data.setStyleSheet('font-size: 24px')

        dock_layout.addRow(nome, self.add_client_nome)
        dock_layout.addRow(endereco, self.add_client_endereco)
        dock_layout.addRow(telefone, self.add_client_telefone)
        dock_layout.addRow(valor, self.add_client_valor)
        dock_layout.addRow(data, self.add_client_data)
        dock_layout.addRow(salvar_button)

        data_hoje = datetime.now().date()
        data_hoje_str = data_hoje.isoformat()
        data_atual = datetime.strptime(data_hoje_str, "%Y-%m-%d")
        self.add_client_data.setText(data_atual.strftime("%d/%m/%Y"))

        dock_widget.setLayout(dock_layout)
        self.dock.setWidget(dock_widget)

        self.dock.visibilityChanged.connect(self.on_dock_visibility_changed)

        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock)

        salvar_button.clicked.connect(self.add_client)

    def dock_edit_client(self):
        self.dock.close()
        self.dock = QDockWidget("Editar Cliente", self)
        self.dock.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)

        dock_widget = QWidget()
        dock_layout = QFormLayout()
        salvar_button = QPushButton("Salvar")
        excluir_button = QPushButton("Excluir")

        nome = QLabel("Nome:")
        nome.setStyleSheet('font-size: 24px')
        endereco = QLabel("Endereço:")
        endereco.setStyleSheet('font-size: 24px')
        telefone = QLabel("Telefone:")
        telefone.setStyleSheet('font-size: 24px')

        dock_layout.addRow(nome, self.edit_client_name)
        dock_layout.addRow(endereco, self.edit_client_endereco)
        dock_layout.addRow(telefone, self.edit_client_telefone)
        dock_layout.addRow(salvar_button)
        dock_layout.addRow(excluir_button)

        lista_clientes = self.billing_system.list_clients_names()
        lista_nomes = [cliente.split(" £ ")[1] for cliente in lista_clientes]

        self.completer = QCompleter(lista_nomes, self)
        self.completer.setCaseSensitivity(False)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.edit_client_name.setCompleter(self.completer)
        self.completer.popup().setStyleSheet("font-size: 18px;")

        self.edit_client_name.textChanged.connect(self.on_edit_bill_name_changed)

        dock_widget.setLayout(dock_layout)
        self.dock.setWidget(dock_widget)

        self.dock.visibilityChanged.connect(self.on_dock_visibility_changed)

        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock)

        salvar_button.clicked.connect(self.edit_client)
        excluir_button.clicked.connect(self.delete_client)
    
    def dock_new_bill(self):
        self.dock.close()
        self.dock = QDockWidget("Nova Venda", self)
        self.dock.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
        dock_widget = QWidget()
        dock_layout = QFormLayout()
        salvar_button = QPushButton("Salvar")

        cliente = QLabel("Cliente:")
        cliente.setStyleSheet('font-size: 20px')
        endereco = QLabel("Endereço:")
        endereco.setStyleSheet('font-size: 20px')
        valor_total = QLabel("Valor Total:")
        valor_total.setStyleSheet('font-size: 20px')
        data_venda = QLabel("Data da Venda:")
        data_venda.setStyleSheet('font-size: 20px')

        dock_layout.addRow(cliente, self.add_bill_name)
        dock_layout.addRow(endereco, self.add_bill_endereco)
        dock_layout.addRow(valor_total, self.add_bill_valor)
        dock_layout.addRow(data_venda, self.add_bill_data)
        dock_layout.addRow(salvar_button)

        dock_widget.setLayout(dock_layout)
        self.dock.setWidget(dock_widget)

        self.dock.visibilityChanged.connect(self.on_dock_visibility_changed)

        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock)

        salvar_button.clicked.connect(self.add_bill)

        lista_clientes = self.billing_system.list_clients_names()
        lista_nomes = [cliente.split(" £ ")[1] for cliente in lista_clientes]

        self.completer = QCompleter(lista_nomes, self)
        self.completer.setCaseSensitivity(False)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.add_bill_name.setCompleter(self.completer)
        self.completer.popup().setStyleSheet("font-size: 18px;")

        self.add_bill_name.textChanged.connect(self.on_add_bill_name_changed)

        data_hoje = datetime.now().date()
        data_hoje_str = data_hoje.isoformat()
        data_atual = datetime.strptime(data_hoje_str, "%Y-%m-%d")
        self.add_bill_data.setText(data_atual.strftime("%d/%m/%Y"))
    
    def dock_pay_bill(self):
        self.dock.close()
        self.dock = QDockWidget("Pagar Dívida", self)
        self.dock.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
        dock_widget = QWidget()
        dock_layout = QFormLayout()
        pagar_button = QPushButton("Pagar")

        cliente = QLabel("Cliente:")
        cliente.setStyleSheet('font-size: 20px')
        endereco = QLabel("Endereço:")
        endereco.setStyleSheet('font-size: 20px')
        valor_pago = QLabel("Valor Pago:")
        valor_pago.setStyleSheet('font-size: 20px')
        data_pagamento = QLabel("Data de Pagamento:")
        data_pagamento.setStyleSheet('font-size: 20px')

        dock_layout.addRow(cliente, self.pay_bill_name)
        dock_layout.addRow(endereco, self.pay_bill_endereco)
        dock_layout.addRow(valor_pago, self.pay_bill_valor)
        dock_layout.addRow(data_pagamento, self.pay_bill_data)
        dock_layout.addRow(pagar_button)

        dock_widget.setLayout(dock_layout)
        self.dock.setWidget(dock_widget)

        self.dock.visibilityChanged.connect(self.on_dock_visibility_changed)

        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock)

        pagar_button.clicked.connect(self.close_bill)

        lista_clientes = self.billing_system.list_clients_names()
        lista_nomes = [cliente.split(" £ ")[1] for cliente in lista_clientes]

        self.completer = QCompleter(lista_nomes, self)
        self.completer.setCaseSensitivity(False)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.pay_bill_name.setCompleter(self.completer)
        self.completer.popup().setStyleSheet("font-size: 18px;")

        self.pay_bill_name.textChanged.connect(self.on_pay_bill_name_changed)

        data_hoje = datetime.now().date()
        data_hoje_str = data_hoje.isoformat()
        data_atual = datetime.strptime(data_hoje_str, "%Y-%m-%d")
        self.pay_bill_data.setText(data_atual.strftime("%d/%m/%Y"))
    
    def dock_report_client(self):
        self.dock.close()
        self.dock = QDockWidget("Filtrar Por Data", self)
        self.dock.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)

        dock_widget = QWidget()
        dock_layout = QFormLayout()
        filtrar_button = QPushButton("Filtrar Relatório")
        copiar_button = QPushButton("Copiar Relatório Por Data")
        copiar2_button = QPushButton("Copiar Relatório Por Nome")
        atualizar_button = QPushButton("Atualizar Página")

        dia = QLabel("Dia:")
        dia.setStyleSheet('font-size: 24px')
        mes = QLabel("Mês:")
        mes.setStyleSheet('font-size: 24px')
        valor = QLabel("Valor Total:")
        valor.setStyleSheet('font-size: 24px')

        dock_layout.addRow(dia, self.day_date)
        dock_layout.addRow(mes, self.month_date)
        dock_layout.addRow(valor, self.report_valor_total)
        dock_layout.addRow(filtrar_button)
        dock_layout.addRow(copiar_button)
        dock_layout.addRow(copiar2_button)
        dock_layout.addRow(atualizar_button)

        self.report_valor_total.setText(self.billing_system.return_valor_total())

        dock_widget.setLayout(dock_layout)
        self.dock.setWidget(dock_widget)

        self.dock.visibilityChanged.connect(self.on_dock_visibility_changed)

        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock)

        filtrar_button.clicked.connect(self.filter_client_pay_bills)
        copiar_button.clicked.connect(self.copy_client_pay_bills)
        copiar2_button.clicked.connect(self.copy_client_pay_bills_2)
        atualizar_button.clicked.connect(self.update_data)

    def dock_filter_closed_bill_name(self):
        self.dock.close()
        self.dock = QDockWidget("Filtrar Por Nome", self)
        self.dock.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)

        lista_clientes = self.billing_system.list_clients_names()
        lista_nomes = [cliente.split(" £ ")[1] for cliente in lista_clientes]

        dock_widget = QWidget()
        dock_layout = QFormLayout()
        filtrar_button = QPushButton("Filtrar Cobranças")
        copiar_button = QPushButton("Copiar Cobranças")
        atualizar_button = QPushButton("Atualizar Página")

        cliente = QLabel("Cliente:")
        cliente.setStyleSheet('font-size: 24px')

        dock_layout.addRow(cliente, self.filter_bill_name)
        dock_layout.addRow(filtrar_button)
        dock_layout.addRow(copiar_button)
        dock_layout.addRow(atualizar_button)

        self.completer = QCompleter(lista_nomes, self)
        self.completer.setCaseSensitivity(False)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.filter_bill_name.setCompleter(self.completer)

        self.completer.popup().setStyleSheet("font-size: 18px;")

        dock_widget.setLayout(dock_layout)
        self.dock.setWidget(dock_widget)

        self.dock.visibilityChanged.connect(self.on_dock_visibility_changed)

        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock)

        filtrar_button.clicked.connect(self.filter_closed_bill_name)
        copiar_button.clicked.connect(self.copy_bill_filter_name)
        atualizar_button.clicked.connect(self.update_data)

    def dock_filter_closed_bill_date(self):
        self.dock.close()
        self.dock = QDockWidget("Filtrar Por Data", self)
        self.dock.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)

        dock_widget = QWidget()
        dock_layout = QFormLayout()
        filtrar_button = QPushButton("Filtrar Cobranças")
        copiar_button = QPushButton("Copiar Cobranças")
        atualizar_button = QPushButton("Atualizar Página")

        dia = QLabel("Dia:")
        dia.setStyleSheet('font-size: 24px')
        mes = QLabel("Mês:")
        mes.setStyleSheet('font-size: 24px')

        dock_layout.addRow(dia, self.day_date)
        dock_layout.addRow(mes, self.month_date)
        dock_layout.addRow(filtrar_button)
        dock_layout.addRow(copiar_button)
        dock_layout.addRow(atualizar_button)

        dock_widget.setLayout(dock_layout)
        self.dock.setWidget(dock_widget)

        self.dock.visibilityChanged.connect(self.on_dock_visibility_changed)

        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock)

        filtrar_button.clicked.connect(self.filter_closed_bill_date)
        copiar_button.clicked.connect(self.copy_bill_filter_date)
        atualizar_button.clicked.connect(self.update_data)
    
    def on_dock_visibility_changed(self, visible):
        if not visible:
            self.update_data()

    def on_add_bill_name_changed(self, text):
        cliente = str(text)
    
        if cliente and '-' in cliente:
            try:
                cliente_id = cliente.split('-')[1].strip()
                cliente_dados = self.billing_system.return_client(cliente_id)
                if cliente_dados:
                    self.add_bill_endereco.setText(cliente_dados[1])
                else:
                    self.add_bill_endereco.clear()
            except IndexError:
                self.add_bill_endereco.clear()
        else:
            self.add_bill_endereco.clear()
    
    def on_pay_bill_name_changed(self, text):
        cliente = str(text)
    
        if cliente and '-' in cliente:
            try:
                cliente_id = cliente.split('-')[1].strip()
                cliente_dados = self.billing_system.return_client(cliente_id)
                if cliente_dados:
                    self.pay_bill_endereco.setText(cliente_dados[1])
                    self.pay_bill_valor.setText(str(cliente_dados[3])) if (cliente_dados[3] != None) else self.pay_bill_valor.setText("0")
                else:
                    self.pay_bill_endereco.clear()
            except IndexError:
                self.pay_bill_endereco.clear()
        else:
            self.add_bill_endereco.clear()

    def on_edit_bill_name_changed(self, text):
        cliente = str(text)
    
        if cliente and '-' in cliente:
            try:
                cliente_id = cliente.split('-')[1].strip()
                cliente_dados = self.billing_system.return_client(cliente_id)
                if cliente_dados:
                    self.old_edit_client_name.setText(str(cliente_dados[0]))
                    self.edit_client_name.setText(str(cliente_dados[0]).split('-')[0].strip())
                    self.edit_client_endereco.setText(cliente_dados[1])
                    self.edit_client_telefone.setText(cliente_dados[2])
                else:
                    self.pay_bill_endereco.clear()
            except IndexError:
                self.pay_bill_endereco.clear()
        else:
            self.add_bill_endereco.clear()

    def add_client(self):
        nome = self.add_client_nome.text()
        endereco = self.add_client_endereco.text()
        telefone = self.add_client_telefone.text()
        valor = self.add_client_valor.text()
        data = self.add_client_data.text()

        if (nome != ""):
            cliente_id = self.billing_system.add_client(nome, endereco, telefone)
            if (valor != ""):
                data_venda_converted = datetime.strptime(data.strip(), "%d/%m/%Y").strftime("%Y-%m-%d")
                self.billing_system.add_bill(int(cliente_id), float(valor), data_venda_converted)
                self.billing_system.update_client_bill(cliente_id)
            self.update_data()
        else:
            QMessageBox.information(self, "Atenção", "Preencha ao menos o nome do cliente.")
    
    def edit_client(self):
        nome = self.edit_client_name.text()
        endereco = self.edit_client_endereco.text()
        telefone = self.edit_client_telefone.text()
        antigo_nome = self.old_edit_client_name.text()

        if (antigo_nome != ""):
            cliente_id = antigo_nome.split('-')[1].strip()
        else:
            QMessageBox.information(self, "Erro", "Dados do cliente não localizado.")
        
        if nome != "" and "-" not in nome:
            nome = f"{nome} - {cliente_id}"

        if (cliente_id != "" and nome != ""):
            self.billing_system.update_client(cliente_id, nome, endereco, telefone)
            self.update_data()
            self.clients = None
        else:
            QMessageBox.information(self, "Atenção", "Preencha pelo menos o nome do cliente.")

    def delete_client(self):
        antigo_nome = self.old_edit_client_name.text()

        if (antigo_nome != ""):
            cliente_id = antigo_nome.split('-')[1].strip()

            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Excluir cliente")
            msg_box.setText(f"Deseja excluir o cliente {antigo_nome}?")
            btn_excluir = QPushButton("Excluir")
            msg_box.addButton(btn_excluir, QMessageBox.YesRole)
            btn_cancelar = QPushButton("Cancelar")
            msg_box.addButton(btn_cancelar, QMessageBox.NoRole)
            resposta = msg_box.exec_()
            
            if resposta == 0:
                valor_total = self.billing_system.return_debit_value(cliente_id)
                if (valor_total == None):
                    self.billing_system.delete_client(cliente_id)
                    QMessageBox.information(self, "Info", f"Cliente {antigo_nome} excluído.")
                else:
                    QMessageBox.warning(self, "Atenção", "Impossível excluir o cliente sem dar baixa nos seus débitos!")
            else:
                self.dock.close()
            
            self.update_data()
            self.clients = None
        else:
            QMessageBox.information(self, "Erro", "Dados do cliente não localizado.")
    
    def add_bill(self):
        nome = self.add_bill_name.text()
        valor = self.add_bill_valor.text()
        data = self.add_bill_data.text()

        if (nome != ""):
            cliente_id = str(nome).split('-')[1].strip()

            if (cliente_id != "" and valor != "" and data != ""):
                data_venda_converted = datetime.strptime(data.strip(), "%d/%m/%Y").strftime("%Y-%m-%d")
                self.billing_system.add_bill(int(cliente_id), float(valor), data_venda_converted)
                self.billing_system.update_client_bill(cliente_id)
                self.update_data()
                self.clients = None
            else:
                QMessageBox.warning(self, "Atenção", "Preencha todos os dados da cobrança.")
        else:
            QMessageBox.warning(self, "Atenção", "Preencha o nome do usuário.")
    
    def close_bill(self):
        nome = self.pay_bill_name.text()
        valor = float(self.pay_bill_valor.text())
        data = datetime.strptime(self.pay_bill_data.text().strip(), "%d/%m/%Y").strftime("%Y-%m-%d")

        if (nome != ""):
            cliente_id = str(nome).split('-')[1].strip()
            valor_total = self.billing_system.return_debit_value(cliente_id)
            
            if (valor != 0):
                if (valor <= valor_total):
                    if (cliente_id != "" and valor != "" and data != ""):
                        self.billing_system.fechar_cobrancas(cliente_id, valor, data)
                        self.billing_system.update_client_bill(cliente_id)
                        self.update_data()
                        self.clients = None
                    else:
                        QMessageBox.warning(self, "Atenção", "Preencha todos os dados da cobrança.")
                else:
                    QMessageBox.warning(self, "Atenção", "O valor pago não pode ser maior que o valor devido!")
            else:
                QMessageBox.warning(self, "Atenção", f"Impossível processar pagamento do cliente {nome}, porque o valor pago está igual a 0.")
                self.update_data()
                self.clients = None
        else:
            QMessageBox.warning(self, "Atenção", "Preencha o nome do usuário.")
    
    def filter_closed_bill_name(self):
        nome_selecionado = self.filter_bill_name.text()
        lista_clientes = self.billing_system.list_clients_names()
        cliente_id = ""
        for cliente in lista_clientes:
            if nome_selecionado in cliente:
                cliente_id = cliente
                break

        if (cliente_id != ""):
            self.table_closed_bills.clear()
            self.load_data_closed_bills_filter_name(int(cliente_id.split('£')[0].strip()))
        else:
            QMessageBox.warning(self, "Erro", f"Nenhum cobrança localizada do cliente: {nome_selecionado}.")
    
    def copy_bill_filter_name(self):
        nome_selecionado = self.filter_bill_name.text()
        lista_clientes = self.billing_system.list_clients_names()
        cliente_id = ""
        for cliente in lista_clientes:
            if nome_selecionado in cliente:
                cliente_id = cliente
                break

        if (cliente_id != ""):
            cobrancas = self.billing_system.filtrar_cobrancas_por_cliente(int(cliente_id.split('£')[0].strip()))
            list_cobrancas = []
            list_cobrancas.append("Cobranças Pagas:")
            list_cobrancas.append("Cliente | Valor | Data da Venda | Data do Pagamento")

            for item in cobrancas:
                cobranca = item.split('£')
                nome = str(cobranca[1])
                data_venda = datetime.strptime(str(cobranca[3].strip()), "%Y-%m-%d")
                data_pagamento = datetime.strptime(str(cobranca[4].strip()), "%Y-%m-%d")
                list_cobrancas.append(f"- {nome.split('-')[0].strip()} | {cobranca[2]} | {data_venda.strftime('%d/%m/%Y')} | {data_pagamento.strftime('%d/%m/%Y')}")
            clipboard = QApplication.clipboard()
            clipboard.setText("\n".join(list_cobrancas))
            QMessageBox.information(self, "Info", "Cobranças copiadas para área de transferência.")
        else:
            QMessageBox.warning(self, "Erro", f"Cliente não localizado com o nome: {nome_selecionado}")

    def filter_closed_bill_date(self):
        mes = self.month_date.currentText()
        dia = self.day_date.currentText()

        if (mes != "" or dia != ""):
            self.load_data_closed_bills_filter_date(dia, mes)
        else:
            QMessageBox.warning(self, "Erro", "Selecione um dia e/ou um mês para filtrar as cobranças.")
    
    def copy_bill_filter_date(self):
        mes = self.month_date.currentText()
        dia = self.day_date.currentText()

        if (mes != "" or dia != ""):
            cobrancas = self.billing_system.filtrar_cobrancas_por_data(self.month_to_number.get(mes) if mes != "" else "", int(dia) if dia != "" else "")
            if (len(cobrancas) > 0):
                list_cobrancas = []
                list_cobrancas.append("Cobranças Pagas:")
                list_cobrancas.append("Cliente | Valor | Data da Venda | Data do Pagamento")

                for item in cobrancas:
                    cobranca = item.split('£')
                    nome = str(cobranca[1])
                    data_venda = datetime.strptime(str(cobranca[3].strip()), "%Y-%m-%d")
                    data_pagamento = datetime.strptime(str(cobranca[4].strip()), "%Y-%m-%d")
                    list_cobrancas.append(f"- {nome.split('-')[0].strip()} | {cobranca[2]} | {data_venda.strftime('%d/%m/%Y')} | {data_pagamento.strftime('%d/%m/%Y')}")
                clipboard = QApplication.clipboard()
                clipboard.setText("\n".join(list_cobrancas))
                QMessageBox.information(self, "Info", "Cobranças copiadas para área de transferência.")
            else:
                QMessageBox.warning(self, "Erro", "Nenhuma cobrança localizada com base na data inserida.")
        else:
            QMessageBox.warning(self, "Erro", "Selecione um dia e/ou um mês para filtrar as cobranças.")
    
    def filter_client_pay_bills(self):
        mes = self.month_date.currentText()
        dia = self.day_date.currentText()

        if (mes != "" or dia != ""):
            self.load_data_client_pay_bills_filter_date(dia, mes)
        else:
            QMessageBox.warning(self, "Erro", "Selecione um dia e/ou um mês para filtrar os clientes.")

    def copy_client_pay_bills(self):
        mes = self.month_date.currentText()
        dia = self.day_date.currentText()

        if (mes != "" or dia != ""):
            clientes = self.billing_system.get_clients_pay_by_date(self.month_to_number.get(mes) if mes != "" else "", int(dia) if dia != "" else "")
            if (len(clientes) > 0):
                list_clientes = []
                list_clientes.append("Cobranças a Pagar:")
                list_clientes.append("Cliente | Valor | Data de Venda | Data de Vencimento")

                for item in clientes:
                    cobranca = item.split('£')
                    nome = str(cobranca[0])
                    data_venda = datetime.strptime(str(cobranca[2].strip()), "%Y-%m-%d")
                    data_vencimento = datetime.strptime(str(cobranca[3].strip()), "%Y-%m-%d")
                    list_clientes.append(f"- {nome.split('-')[0].strip()} | {cobranca[1]} | {data_venda.strftime('%d/%m/%Y')} | {data_vencimento.strftime('%d/%m/%Y')}")
                clipboard = QApplication.clipboard()
                clipboard.setText("\n".join(list_clientes))
                QMessageBox.information(self, "Info", "Relatório copiado para área de transferência.")
            else:
                QMessageBox.warning(self, "Atenção", "Nenhuma cobrança para o dia e ou mês selecionado.")
        else:
            clientes = self.billing_system.get_clients_pay_by_date(self.month_to_number.get(mes) if mes != "" else "", int(dia) if dia != "" else "")
            if (len(clientes) > 0):
                list_clientes = []
                list_clientes.append("Cobranças a Pagar:")
                list_clientes.append("Cliente | Valor | Data de Venda | Data de Vencimento")

                comprimento = 0

                for item in clientes:
                    cobranca = item.split('£')
                    if (comprimento < len(cobranca[0])):
                        comprimento = len(cobranca[0])
                
                for item in clientes:
                    cobranca = item.split('£')
                    nome = str(cobranca[0])
                    data_venda = datetime.strptime(str(cobranca[2].strip()), "%Y-%m-%d")
                    data_vencimento = datetime.strptime(str(cobranca[3].strip()), "%Y-%m-%d")
                    list_clientes.append(f"- {nome.split('-')[0].strip()} | {cobranca[1]} | {data_venda.strftime('%d/%m/%Y')} | {data_vencimento.strftime('%d/%m/%Y')}")
                clipboard = QApplication.clipboard()
                clipboard.setText("\n".join(list_clientes))
                QMessageBox.information(self, "Info", "Relatório copiado para área de transferência.")
            else:
                QMessageBox.warning(self, "Atenção", "Nenhuma cobrança em aberto.")
    
    def copy_client_pay_bills_2(self):
        mes = self.month_date.currentText()
        dia = self.day_date.currentText()

        if (mes != "" or dia != ""):
            clientes = self.billing_system.get_clients_pay_by_date_name(self.month_to_number.get(mes) if mes != "" else "", int(dia) if dia != "" else "")
            if (len(clientes) > 0):
                list_clientes = []
                list_clientes.append("Cobranças a Pagar:")
                list_clientes.append("Cliente | Valor | Data de Venda | Data de Vencimento")

                for item in clientes:
                    cobranca = item.split('£')
                    nome = str(cobranca[0])
                    data_venda = datetime.strptime(str(cobranca[2].strip()), "%Y-%m-%d")
                    data_vencimento = datetime.strptime(str(cobranca[3].strip()), "%Y-%m-%d")
                    list_clientes.append(f"- {nome.split('-')[0].strip()} | {cobranca[1]} | {data_venda.strftime('%d/%m/%Y')} | {data_vencimento.strftime('%d/%m/%Y')}")
                clipboard = QApplication.clipboard()
                clipboard.setText("\n".join(list_clientes))
                QMessageBox.information(self, "Info", "Relatório copiado para área de transferência.")
            else:
                QMessageBox.warning(self, "Atenção", "Nenhuma cobrança para o dia e ou mês selecionado.")
        else:
            clientes = self.billing_system.get_clients_pay_by_date_name(self.month_to_number.get(mes) if mes != "" else "", int(dia) if dia != "" else "")
            if (len(clientes) > 0):
                list_clientes = []
                list_clientes.append("Cobranças a Pagar:")
                list_clientes.append("Cliente | Valor | Data de Venda | Data de Vencimento")

                comprimento = 0

                for item in clientes:
                    cobranca = item.split('£')
                    if (comprimento < len(cobranca[0])):
                        comprimento = len(cobranca[0])
                
                for item in clientes:
                    cobranca = item.split('£')
                    nome = str(cobranca[0])
                    data_venda = datetime.strptime(str(cobranca[2].strip()), "%Y-%m-%d")
                    data_vencimento = datetime.strptime(str(cobranca[3].strip()), "%Y-%m-%d")
                    list_clientes.append(f"- {nome.split('-')[0].strip()} | {cobranca[1]} | {data_venda.strftime('%d/%m/%Y')} | {data_vencimento.strftime('%d/%m/%Y')}")
                clipboard = QApplication.clipboard()
                clipboard.setText("\n".join(list_clientes))
                QMessageBox.information(self, "Info", "Relatório copiado para área de transferência.")
            else:
                QMessageBox.warning(self, "Atenção", "Nenhuma cobrança em aberto.")
    
    def update_data(self):
        self.table_clients.clear()
        self.load_data_clients()
        self.table_closed_bills.clear()
        self.load_data_closed_bills()
        self.add_client_nome.clear()
        self.add_client_endereco.clear()
        self.add_client_telefone.clear()
        self.add_client_valor.clear()
        self.add_client_data.clear()
        self.edit_client_name.clear()
        self.edit_client_endereco.clear()
        self.edit_client_telefone.clear()
        self.add_bill_name.clear()
        self.add_bill_endereco.clear()
        self.add_bill_valor.clear()
        self.add_bill_data.clear()
        self.pay_bill_name.clear()
        self.pay_bill_endereco.clear()
        self.pay_bill_valor.clear()
        self.pay_bill_data.clear()
        self.filter_bill_name.clear()
        self.report_valor_total.clear()
        self.report_valor_total.setText(self.billing_system.return_valor_total())
        data_hoje = datetime.now().date()
        data_hoje_str = data_hoje.isoformat()
        data_atual = datetime.strptime(data_hoje_str, "%Y-%m-%d")
        self.add_client_data.setText(data_atual.strftime("%d/%m/%Y"))
        self.add_bill_data.setText(data_atual.strftime("%d/%m/%Y"))
        self.pay_bill_data.setText(data_atual.strftime("%d/%m/%Y"))

class BillingSystem:
    def __init__(self, db_name='banco_de_dados_nino_gas.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def add_client(self, nome, endereco, telefone):
        self.cursor.execute('''
            INSERT INTO clientes (nome, endereco, telefone)
            VALUES (?, ?, ?)
        ''', (nome, endereco, telefone))
        cliente_id = self.cursor.lastrowid
        nome_atualizado = f"{nome} - {cliente_id}"
        self.cursor.execute('''
            UPDATE clientes
            SET nome = ?
            WHERE id = ?
        ''', (nome_atualizado, cliente_id))
        self.conn.commit()
        return cliente_id

    def add_bill(self, cliente_id, valor_total, data_venda):
        datetime_venda = datetime.strptime(data_venda, "%Y-%m-%d").date()
        data_vencimento = datetime_venda + timedelta(days=30)
        self.cursor.execute('''
            INSERT INTO cobrancas (cliente_id, valor_total, data_venda, data_vencimento, data_fechamento, ativo)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (cliente_id, valor_total, datetime_venda, data_vencimento, None, True))
        self.conn.commit()
    
    def update_client_bill(self, cliente_id):
        self.cursor.execute('''
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
        ''', (cliente_id,))
        result = self.cursor.fetchone()
        if (result != None):
            self.cursor.execute('''
                UPDATE clientes
                SET valor_total = ?, data_venda = ?, data_vencimento = ?
                WHERE id = ?
            ''', (result[1], result[2], result[3], cliente_id))
        else:
            self.cursor.execute('''
                UPDATE clientes
                SET valor_total = NULL, data_venda = NULL, data_vencimento = NULL
                WHERE id = ?
            ''', (cliente_id,))
        self.conn.commit()
    
    def return_debit_value(self, client_id):
        self.cursor.execute("""
            SELECT 
                cliente_id,
                SUM(valor_total)
            FROM cobrancas
            WHERE cliente_id = ?
        """, (client_id,))
        row = self.cursor.fetchone()
        return row[1]

    def list_clients(self):
        clientes = []
        self.cursor.execute('SELECT clientes.nome, clientes.endereco, clientes.telefone, clientes.valor_total, clientes.data_venda, clientes.data_vencimento FROM clientes ORDER BY LOWER(clientes.nome) ASC')
        for row in self.cursor.fetchall():
            clientes.append(f"{row[0]} £ {row[1]} £ {row[2]} £ {row[3]} £ {row[4]} £ {row[5]}")
        return clientes
    
    def return_client(self, id):
        self.cursor.execute("""
            SELECT clientes.nome, clientes.endereco, clientes.telefone, clientes.valor_total
            FROM clientes
            WHERE clientes.id = ?
        """, (id,))
        row = self.cursor.fetchone()
        return row
    
    def list_clients_names(self):
        clientes = []
        self.cursor.execute('SELECT clientes.id, nome FROM clientes')
        for row in self.cursor.fetchall():
            clientes.append(str(row[0]) + " £ " + row[1])
        return clientes
    
    def list_closed_bills(self):
        cobrancas = []
        self.cursor.execute('''
            SELECT cobrancas.id, clientes.nome, cobrancas.valor_total, cobrancas.data_venda, cobrancas.data_fechamento
            FROM cobrancas
            JOIN clientes ON cobrancas.cliente_id = clientes.id
            WHERE cobrancas.ativo = 0
            ORDER BY cobrancas.data_fechamento DESC
        ''')
        for row in self.cursor.fetchall():
            cobrancas.append(f"{row[0]} £ {row[1]} £ {row[2]} £ {row[3]} £ {row[4]}")
        return cobrancas
    
    def update_client(self, cliente_id, nome, endereco, telefone):
        self.cursor.execute('''
            UPDATE clientes
            SET nome = ?, endereco = ?, telefone = ?
            WHERE id = ?
        ''', (nome, endereco, telefone, cliente_id))
        self.conn.commit()
    
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
    
    def filtrar_cobrancas_por_cliente(self, cliente_id):
        cobrancas = []
        self.cursor.execute('''
            SELECT cobrancas.id, clientes.nome, cobrancas.valor_total, cobrancas.data_venda, cobrancas.data_fechamento
            FROM cobrancas
            JOIN clientes ON cobrancas.cliente_id = clientes.id
            WHERE cobrancas.ativo = 0 AND clientes.id = ?
            ORDER BY cobrancas.data_fechamento
        ''', (cliente_id,))
        for row in self.cursor.fetchall():
            cobrancas.append(f"{row[0]} £ {row[1]} £ {row[2]} £ {row[3]} £ {row[4]}")
        return cobrancas
    
    def filtrar_cobrancas_por_data(self, month=None, day=None):
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
        self.conn.commit()

    def fechar_cobrancas(self, cliente_id, valor_pago, data_atual):
        # Seleciona as cobranças ativas do cliente, ordenadas pela data de venda
        self.cursor.execute('''
            SELECT id, valor_total, data_venda, data_vencimento 
            FROM cobrancas
            WHERE cliente_id = ? AND ativo = 1
            ORDER BY id
        ''', (cliente_id,))
        cobrancas = self.cursor.fetchall()

        for cobranca in cobrancas:
            cobranca_id, valor_total, data_venda, data_vencimento = cobranca
            
            # Se o pagamento cobrir o valor total da cobrança
            if valor_pago >= valor_total:
                # Encerra a cobrança
                self.cursor.execute('''
                    UPDATE cobrancas
                    SET ativo = 0, data_fechamento = ?
                    WHERE id = ?
                ''', (data_atual, cobranca_id))
                
                # Subtrai o valor pago do total
                valor_pago -= valor_total
            elif valor_pago == 0:
                break
            else:
                # Se o pagamento não cobrir o valor total, ajusta o valor da cobrança
                new_valor_total = valor_total - valor_pago

                # Atualiza a cobrança atual com o valor pago
                self.cursor.execute('''
                    UPDATE cobrancas
                    SET valor_total = ?, ativo = 0, data_fechamento = ?
                    WHERE id = ?
                ''', (valor_pago, data_atual, cobranca_id))

                # Cria uma nova cobrança com o valor restante
                self.cursor.execute('''
                    INSERT INTO cobrancas (cliente_id, valor_total, data_venda, data_vencimento, ativo)
                    VALUES (?, ?, ?, ?, 1)
                ''', (cliente_id, new_valor_total, data_venda, data_vencimento))

                # O pagamento foi totalmente processado
                valor_pago = 0
                break
    
    def get_clients_pay_by_date(self, month=None, day=None):
        query = '''
            SELECT clientes.nome, clientes.valor_total, clientes.data_venda, clientes.data_vencimento
            FROM clientes
            WHERE clientes.valor_total IS NOT NULL
        '''
        params = []

        if month and day:
            query += ' AND strftime("%m", clientes.data_vencimento) = ? AND strftime("%d", clientes.data_vencimento) = ?'
            params.extend([f'{month:02}', f'{day:02}'])
        elif month:
            query += ' AND strftime("%m", clientes.data_vencimento) = ?'
            params.append(f'{month:02}')
        elif day:
            query += ' AND strftime("%d", clientes.data_vencimento) = ?'
            params.append(f'{day:02}')
        
        query += 'ORDER BY clientes.data_vencimento'
        
        self.cursor.execute(query, params)
        clientes = []

        for row in self.cursor.fetchall():
            clientes.append(f"{row[0]} £ {row[1]} £ {row[2]} £ {row[3]}")
        
        return clientes
    
    def get_clients_pay_by_date_name(self, month=None, day=None):
        query = '''
            SELECT clientes.nome, clientes.valor_total, clientes.data_venda, clientes.data_vencimento
            FROM clientes
            WHERE clientes.valor_total IS NOT NULL
        '''
        params = []

        if month and day:
            query += ' AND strftime("%m", clientes.data_vencimento) = ? AND strftime("%d", clientes.data_vencimento) = ?'
            params.extend([f'{month:02}', f'{day:02}'])
        elif month:
            query += ' AND strftime("%m", clientes.data_vencimento) = ?'
            params.append(f'{month:02}')
        elif day:
            query += ' AND strftime("%d", clientes.data_vencimento) = ?'
            params.append(f'{day:02}')
        
        query += 'ORDER BY LOWER(clientes.nome) ASC'
        
        self.cursor.execute(query, params)
        clientes = []

        for row in self.cursor.fetchall():
            clientes.append(f"{row[0]} £ {row[1]} £ {row[2]}£ {row[2]}")
        
        return clientes
    
    def get_to_load_clients_pay_by_date(self, month=None, day=None):
        query = '''
            SELECT clientes.nome, clientes.endereco, clientes.telefone, clientes.valor_total, clientes.data_venda, clientes.data_vencimento
            FROM clientes
            WHERE clientes.valor_total IS NOT NULL
        '''
        params = []

        if month and day:
            query += ' AND strftime("%m", clientes.data_vencimento) = ? AND strftime("%d", clientes.data_vencimento) = ?'
            params.extend([f'{month:02}', f'{day:02}'])
        elif month:
            query += ' AND strftime("%m", clientes.data_vencimento) = ?'
            params.append(f'{month:02}')
        elif day:
            query += ' AND strftime("%d", clientes.data_vencimento) = ?'
            params.append(f'{day:02}')
        
        self.cursor.execute(query, params)
        clientes = []

        for row in self.cursor.fetchall():
            clientes.append(f"{row[0]} £ {row[1]} £ {row[2]} £ {row[3]} £ {row[4]} £ {row[5]}")
        
        return clientes
    
    def return_valor_total(self):
        self.cursor.execute('''
            SELECT SUM(valor_total) AS total_valor_total
            FROM clientes;
        ''')
        row = self.cursor.fetchall()
        valor = str(row[0]).strip("(),")
        return valor
    
    def delete_client(self, cliente_id):
        self.cursor.execute('''
            DELETE FROM clientes WHERE id = ?
        ''', (cliente_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
