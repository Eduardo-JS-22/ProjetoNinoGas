import sys, sqlite3
from PyQt5.QtWidgets import QComboBox, QHeaderView, QTableWidget, QTableWidgetItem, QMessageBox, QLineEdit, QFormLayout, QApplication, QMainWindow, QToolBar, QDockWidget, QLabel, QStackedWidget, QWidget, QVBoxLayout, QListWidget, QPushButton, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon
from datetime import datetime, timedelta

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 1920, 1080)  # Define o tamanho da janela

        # Cria a QTableWidget com 10 linhas e 5 colunas
        self.table = QTableWidget(10, 5, self)
        
        # Ajusta a largura da tabela para 75% da largura da tela
        self.table.setFixedWidth(int(self.width() * 0.75))

        # Configura o header para que as colunas se ajustem uniformemente
        self.header = self.table.horizontalHeader()
        self.header.setSectionResizeMode(QHeaderView.Stretch)

        # Move a tabela para o canto superior esquerdo da janela
        self.table.move(0, 0)

        self.setCentralWidget(self.table)

        # Cria um QDockWidget para ocupar os 25% restantes
        dock_widget = QDockWidget("Informações", self)
        dock_widget.setAllowedAreas(Qt.RightDockWidgetArea)

        # Cria um widget de conteúdo para o QDockWidget
        content_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Conteúdo do DockWidget"))
        content_widget.setLayout(layout)

        dock_widget.setWidget(content_widget)
        self.addDockWidget(Qt.RightDockWidgetArea, dock_widget)

        # Ajusta a largura da QDockWidget para 25% da largura total da janela
        dock_widget.setFixedWidth(int(self.width() * 0.25))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
