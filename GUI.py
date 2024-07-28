import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QTabWidget, QMainWindow, QSpacerItem, QSizePolicy, QLabel

class Tab1(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout(self)
        label = QLabel("This is Tab 1", self)
        layout.addWidget(label)
        back_button = QPushButton('Back to Main', self)
        back_button.clicked.connect(self.go_back)
        layout.addWidget(back_button)
        self.setLayout(layout)

    def go_back(self):
        self.main_window.go_back()

class Tab2(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout(self)
        label = QLabel("This is Tab 2", self)
        layout.addWidget(label)
        back_button = QPushButton('Back to Main', self)
        back_button.clicked.connect(self.go_back)
        layout.addWidget(back_button)
        self.setLayout(layout)

    def go_back(self):
        self.main_window.go_back()

class Tab3(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout(self)
        label = QLabel("This is Tab 3", self)
        layout.addWidget(label)
        back_button = QPushButton('Back to Main', self)
        back_button.clicked.connect(self.go_back)
        layout.addWidget(back_button)
        self.setLayout(layout)

    def go_back(self):
        self.main_window.go_back()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle('Main Window')
        self.setGeometry(100, 100, 1920, 1080)

        # Create central widget and set layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.vbox_layout = QVBoxLayout(self.central_widget)

        # Create buttons
        self.button1 = QPushButton('1', self)
        self.button2 = QPushButton('2', self)
        self.button3 = QPushButton('3', self)

        # Set button sizes
        self.button1.setFixedSize(200, 50)
        self.button2.setFixedSize(200, 50)
        self.button3.setFixedSize(200, 50)

        # Create layout for buttons and add them
        self.button_layout = QHBoxLayout()
        self.button_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.button_layout.addWidget(self.button1)
        self.button_layout.addWidget(self.button2)
        self.button_layout.addWidget(self.button3)
        self.button_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Create tab widget
        self.tabs = QTabWidget()

        # Add the layouts to the main layout
        self.vbox_layout.addLayout(self.button_layout)
        self.vbox_layout.addWidget(self.tabs)

        # Connect buttons to methods
        self.button1.clicked.connect(lambda: self.show_tab(0))
        self.button2.clicked.connect(lambda: self.show_tab(1))
        self.button3.clicked.connect(lambda: self.show_tab(2))

        # Add the tabs but hide them initially
        self.tab1 = Tab1(self)
        self.tab2 = Tab2(self)
        self.tab3 = Tab3(self)
        self.tabs.addTab(self.tab1, "Tab 1")
        self.tabs.addTab(self.tab2, "Tab 2")
        self.tabs.addTab(self.tab3, "Tab 3")
        self.tabs.setTabVisible(0, False)
        self.tabs.setTabVisible(1, False)
        self.tabs.setTabVisible(2, False)

    def show_tab(self, index):
        self.tabs.setTabVisible(index, True)
        self.tabs.setCurrentIndex(index)

    def go_back(self):
        self.tabs.setTabVisible(self.tabs.currentIndex(), False)

# Entry point of the application
if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainWin = MainWindow()
    mainWin.show()

    sys.exit(app.exec_())



