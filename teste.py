import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QCompleter

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Exemplo de lista de nomes no formato "número - nome"
        self.clientes = [
            "1 - Ana",
            "2 - João",
            "3 - Pedro",
            "4 - Maria",
            "5 - Lucas",
            "6 - Aline",
            "7 - Paula",
            "8 - Rafael",
            "9 - Beatriz",
            "10 - André"
        ]

        # Apenas os nomes, sem os números
        self.nomes = [cliente.split(" - ")[1] for cliente in self.clientes]

        self.layout = QVBoxLayout()

        # Input de cliente
        self.cliente_id_input = QLineEdit(self)
        self.cliente_id_input.setPlaceholderText("Digite o nome do cliente")

        # Configurando o QCompleter
        self.completer = QCompleter(self.nomes, self)
        self.completer.setCaseSensitivity(False)  # Ignora maiúsculas/minúsculas
        self.completer.setCompletionMode(QCompleter.PopupCompletion)  # Mostra uma lista suspensa
        self.cliente_id_input.setCompleter(self.completer)

        self.layout.addWidget(self.cliente_id_input)

        # Botão de imprimir
        self.imprimir_button = QPushButton("Imprimir", self)
        self.imprimir_button.clicked.connect(self.imprimir_cliente)

        self.layout.addWidget(self.imprimir_button)

        # Label para exibir o resultado
        self.result_label = QLabel(self)
        self.layout.addWidget(self.result_label)

        self.setLayout(self.layout)
        self.setWindowTitle("Seleção de Clientes")

    def imprimir_cliente(self):
        nome_selecionado = self.cliente_id_input.text()
        
        # Encontrando o nome completo (número - nome) na lista original
        for cliente in self.clientes:
            if nome_selecionado in cliente:
                self.result_label.setText(cliente)
                break

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
