import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle('Main Window')
        self.setGeometry(100, 100, 1920, 1080)

        # Create buttons
        self.button1 = QPushButton('1', self)
        self.button2 = QPushButton('2', self)
        self.button3 = QPushButton('3', self)

        # Set button sizes
        self.button1.setFixedSize(200, 50)
        self.button2.setFixedSize(200, 50)
        self.button3.setFixedSize(200, 50)

        # Create layout and add buttons
        layout = QHBoxLayout()
        layout.addWidget(self.button1, alignment=Qt.AlignCenter)
        layout.addWidget(self.button2, alignment=Qt.AlignCenter)
        layout.addWidget(self.button3, alignment=Qt.AlignCenter)

        # Set the layout for the main window
        self.setLayout(layout)

# Entry point of the application
if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainWin = MainWindow()
    mainWin.show()

    sys.exit(app.exec_())

