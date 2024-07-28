import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QTabWidget, QMainWindow, QSpacerItem, QSizePolicy, QLabel

class Tab1(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("This is Tab 1", self)
        layout.addWidget(label)
        self.setLayout(layout)

class Tab2(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("This is Tab 2", self)
        layout.addWidget(label)
        self.setLayout(layout)

class Tab3(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("This is Tab 3", self)
        layout.addWidget(label)
        self.setLayout(layout)

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
        button_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        button_layout.addWidget(self.button1)
        button_layout.addWidget(self.button2)
        button_layout.addWidget(self.button3)
        button_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Create tab widget
        self.tabs = QTabWidget()

        # Add the tabs
        self.tab1 = Tab1()
        self.tab2 = Tab2()
        self.tab3 = Tab3()

        self.tabs.addTab(self.tab1, "Tab 1")
        self.tabs.addTab(self.tab2, "Tab 2")
        self.tabs.addTab(self.tab3, "Tab 3")

        # Add layouts to the main layout
        vbox_layout.addLayout(button_layout)
        vbox_layout.addWidget(self.tabs)

        # Connect buttons to methods
        self.button1.clicked.connect(lambda: self.tabs.setCurrentWidget(self.tab1))
        self.button2.clicked.connect(lambda: self.tabs.setCurrentWidget(self.tab2))
        self.button3.clicked.connect(lambda: self.tabs.setCurrentWidget(self.tab3))

# Entry point of the application
if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainWin = MainWindow()
    mainWin.show()

    sys.exit(app.exec_())


