import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QListWidget, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Autocomplete Example")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.input_line = QLineEdit(self)
        self.input_line.setPlaceholderText("Type to search...")
        self.input_line.textChanged.connect(self.on_text_changed)
        self.layout.addWidget(self.input_line)

        self.suggestions_list = QListWidget(self)
        self.suggestions_list.itemClicked.connect(self.on_item_clicked)
        self.layout.addWidget(self.suggestions_list)
        self.suggestions_list.hide()

        self.data = ["apple", "banana", "grape", "orange", "strawberry", "watermelon", "blueberry", "raspberry"]

    def on_text_changed(self, text):
        if text:
            self.suggestions_list.clear()
            filtered_data = [item for item in self.data if text.lower() in item.lower()]
            self.suggestions_list.addItems(filtered_data)
            self.suggestions_list.show()
        else:
            self.suggestions_list.hide()

    def on_item_clicked(self, item):
        self.input_line.setText(item.text())
        self.suggestions_list.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())