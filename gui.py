import sys
from PyQt5.QtWidgets import QMessageBox, QLineEdit, QFormLayout, QApplication, QMainWindow, QToolBar, QDockWidget, QLabel, QStackedWidget, QWidget, QVBoxLayout, QListWidget, QPushButton, QAbstractItemView, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt
from main import BillingSystem
from datetime import datetime

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.billing_system = BillingSystem()
        self.bills = []
        self.clients = None
        self.nome_input = QLineEdit()
        self.endereco_input = QLineEdit()
        self.telefone_input = QLineEdit()
        self.cliente_id_input = QLineEdit()
        self.valor_input = QLineEdit()
        self.data_venda_input = QLineEdit()

        # Configurações da janela principal
        self.setWindowTitle("Nino Gás")
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
                font-size: 24px;
                color: black;
            }
            QPushButton {
                background-color: orange;
                color: white;
                border: none;
                font-size: 18px;
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

        # Define uma política de tamanho para que os botões preencham a largura disponível
        for btn in [btn_inicial, btn_clientes, btn_cobrancas]:
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        # Adiciona o widget contêiner à barra de ferramentas
        toolbar.addWidget(container_widget)

        # Stack para trocar entre as páginas
        self.stack = QStackedWidget(self)
        self.setCentralWidget(self.stack)

        # Páginas
        self.pages = {}
        for page_name in ["Página Inicial", "Clientes", "Cobranças", "Relatórios"]:
            page = QWidget()
            self.page_layout = QVBoxLayout(page)
            self.button_layout = QHBoxLayout()

            if page_name == "Página Inicial":
                # Adiciona o menu
                menu = self.billing_system.menu()
                self.list_widget = QLabel(menu, self)
                self.list_widget.setAlignment(Qt.AlignCenter)
                self.page_layout.addWidget(self.list_widget)
            elif page_name == "Clientes":
                self.list_widget_client = QListWidget(self)
                self.list_widget_client.setSelectionMode(
                    QAbstractItemView.ExtendedSelection
                )
                clientes = self.billing_system.list_clients()
                self.list_widget_client.itemClicked.connect(self.print_itens_client)
                self.list_widget_client.addItems(clientes)
                self.page_layout.addWidget(self.list_widget_client)

                new_client_button = QPushButton("Adicionar Novo Cliente", self)
                new_client_button.clicked.connect(self.dock_new_client)
                self.button_layout.addWidget(new_client_button)
                edit_client_button = QPushButton("Editar Cliente Selecionado", self)
                edit_client_button.clicked.connect(self.dock_edit_client)
                self.button_layout.addWidget(edit_client_button)
                self.page_layout.addLayout(self.button_layout)
            elif page_name == "Cobranças":
                # Adiciona a lista de cobranças
                self.list_widget_bill = QListWidget(self)
                self.list_widget_bill.setSelectionMode(
                    QAbstractItemView.ExtendedSelection
                )
                cobrancas = self.billing_system.list_bills()
                self.list_widget_bill.itemClicked.connect(self.print_itens_bill)
                self.list_widget_bill.addItems(cobrancas)
                self.page_layout.addWidget(self.list_widget_bill)

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
                label = QLabel(page_name, self)
                label.setAlignment(Qt.AlignCenter)
                self.page_layout.addWidget(label)

            self.stack.addWidget(page)
            self.pages[page_name] = page

    def show_page(self, page_name):
        self.stack.setCurrentWidget(self.pages[page_name])

    def update_data(self):
        menu = self.billing_system.menu()
        self.list_widget.clear()
        self.list_widget.setText(menu)
        clientes = self.billing_system.list_clients()
        self.list_widget_client.clear()
        self.list_widget_client.addItems(clientes)
        cobrancas = self.billing_system.list_bills()
        self.list_widget_bill.clear()
        self.list_widget_bill.addItems(cobrancas)
        self.nome_input.clear()
        self.endereco_input.clear()
        self.telefone_input.clear()
        self.cliente_id_input.clear()
        self.valor_input.clear()
        self.data_venda_input.clear()

    def copy_cobrancas_vencidas(self):
        cobrancas_vencidas = self.billing_system.filter_past_due_bills()
        clipboard = QApplication.clipboard()
        clipboard.setText("\n".join(cobrancas_vencidas))

    def copy_cobrancas(self):
        cobrancas = self.billing_system.list_bills()
        clipboard = QApplication.clipboard()
        clipboard.setText("\n".join(cobrancas))
    
    def print_itens_client(self):
        self.clients = str(self.list_widget_client.selectedItems()[0].text())
        print (self.clients)
    
    def copy_clientes_selecionadas(self):
        if (self.clients != None):
            clipboard = QApplication.clipboard()
            clipboard.setText(self.clients)
            self.clients = None
            print(self.clients)
        else:
            QMessageBox.warning(self, "Erro", "Nenhum cliente selecionado para edição.")
    
    def print_itens_bill(self):
        items = self.list_widget_bill.selectedItems()
        for i in range(len(items)):
            self.bills.append(str(self.list_widget_bill.selectedItems()[i].text()))
        print (list(set(self.bills)))
    
    def close_cobrancas_selecionadas(self):
        if (len(self.bills) > 0):
            for i in range(len(self.bills)):
                self.billing_system.close_bill(self.bills[i].split('-')[0].strip())
            self.update_data()
        else:
            QMessageBox.warning(self, "Erro", "Nenhuma cobrança selecionada para encerrar.")
    
    def dock_new_client(self):
        dock = QDockWidget("Novo Cliente", self)
        dock.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)

        # Criar o conteúdo do dock
        dock_widget = QWidget()
        dock_layout = QFormLayout()
        salvar_button = QPushButton("Salvar")

        dock_layout.addRow("Nome:", self.nome_input)
        dock_layout.addRow("Endereço:", self.endereco_input)
        dock_layout.addRow("Telefone:", self.telefone_input)
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

                dock_layout.addRow("Nome:", self.nome_input)
                dock_layout.addRow("Endereço:", self.endereco_input)
                dock_layout.addRow("Telefone:", self.telefone_input)
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

        dock_layout.addRow("Cliente:", self.cliente_id_input)
        dock_layout.addRow("Valor Total:", self.valor_input)
        dock_layout.addRow("Data da Venda:", self.data_venda_input)
        dock_layout.addRow(salvar_button)

        self.suggestions_list = QListWidget(self)
        self.suggestions_list.itemClicked.connect(self.on_item_clicked)
        dock_layout.addWidget(self.suggestions_list)
        self.suggestions_list.hide()
        self.data = self.billing_system.list_clients_names()

        data_hoje = datetime.now().date()
        data_hoje_str = data_hoje.isoformat()
        self.data_venda_input.setText(data_hoje_str)

        dock_widget.setLayout(dock_layout)
        dock.setWidget(dock_widget)

        # Adicionar o widget dock à janela principal
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)

        # Conectar o botão "Salvar" à função save_data
        salvar_button.clicked.connect(self.add_bill)
    
    def on_text_changed(self, text):
        if text:
            self.suggestions_list.clear()
            filtered_data = [item for item in self.data if text.lower() in item.lower()]
            self.suggestions_list.addItems(filtered_data)
            self.suggestions_list.show()
            if (len(filtered_data) == 1):
                print(int(filtered_data[0].split('-')[0].strip()))
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
            print(self.billing_system.list_clients())
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
            print(self.billing_system.list_clients())
            self.clients = None
            self.dock.close()
        else:
            QMessageBox.information(self, "Erro ao atualizar cliente.")
    
    def add_bill(self):
        cliente_id = self.cliente_id_input.text()
        valor_total = self.valor_input.text()
        data_venda = self.data_venda_input.text()

        if (cliente_id != None and valor_total != None and data_venda != None):
            self.billing_system.add_bill(int(cliente_id.split('-')[0].strip()), float(valor_total), data_venda)
            self.update_data()
            print (self.billing_system.list_bills())
        else:
            QMessageBox.warning(self, "Erro", "Erro ao cadastrar cobrança.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
