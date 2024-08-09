import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        # Configurações iniciais
        self.setWindowTitle("Alterar Cor das Linhas Selecionadas")
        self.setGeometry(100, 100, 400, 300)

        # Layout principal
        layout = QVBoxLayout()

        # Criação do QTableWidget com 10 linhas e 3 colunas
        self.table_widget = QTableWidget(10, 3)
        self.table_widget.setSelectionBehavior(QTableWidget.SelectRows)  # Selecionar linhas inteiras
        self.table_widget.setSelectionMode(QTableWidget.MultiSelection)  # Permitir seleção múltipla

        # Adicionando itens à tabela
        for i in range(10):
            for j in range(3):
                item = QTableWidgetItem(f"Item {i+1}-{j+1}")
                self.table_widget.setItem(i, j, item)

        # Conectando a seleção ao método que altera a cor das linhas
        self.table_widget.itemSelectionChanged.connect(self.change_color_of_selected_rows)

        # Adicionando QTableWidget ao layout
        layout.addWidget(self.table_widget)
        self.setLayout(layout)

    def change_color_of_selected_rows(self):
        # Primeiro, reseta as cores para o padrão
        for i in range(self.table_widget.rowCount()):
            for j in range(self.table_widget.columnCount()):
                item = self.table_widget.item(i, j)
                if item is not None:
                    item.setBackground(Qt.white)

        # Agora, altera a cor das linhas selecionadas
        selected_rows = self.table_widget.selectionModel().selectedRows()
        for row in selected_rows:
            for col in range(self.table_widget.columnCount()):
                item = self.table_widget.item(row.row(), col)
                if item is not None:
                    item.setBackground(QColor(255, 255, 0))  # Cor amarela

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
