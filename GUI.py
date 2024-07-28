import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QTabWidget, QMainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle('Main Window')
        self.setGeometry(100, 100, 1920, 1080)

        # Create central widget and set layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        vbox_layout = QVBoxLayout(central_widget)

        # Create buttons
        self.button1 = QPushButton('1', self)
        self.button2 = QPushButton('2', self)
        self.button3 = QPushButton('3', self)

        # Set button sizes
        self.button1.setFixedSize(200, 50)
        self.button2.setFixedSize(200, 50)
        self.button3.setFixedSize(200, 50)

        # Create layout for buttons and add them
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.button1, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.button2, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.button3, alignment=Qt.AlignCenter)

        # Create tab widget
        self.tabs = QTabWidget()

        # Add layouts to the main layout
        vbox_layout.addLayout(button_layout)
        vbox_layout.addWidget(self.tabs)

        # Connect buttons to methods
        self.button1.clicked.connect(lambda: self.open_tab("Tab 1"))
        self.button2.clicked.connect(lambda: self.open_tab("Tab 2"))
        self.button3.clicked.connect(lambda: self.open_tab("Tab 3"))

    def open_tab(self, tab_name):
        new_tab = QWidget()
        self.tabs.addTab(new_tab, tab_name)

# Entry point of the application
if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainWin = MainWindow()
    mainWin.show()

    sys.exit(app.exec_())


