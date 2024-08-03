import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QStackedWidget, QMainWindow, QSizePolicy, QLabel

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
        self.main_window.show_main_page()

class Tab2(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout(self)
        label = QLabel("This is Tab 2", self)
        layout.addWidget(label)
        
        # Create the grid layout
        grid_layout = QGridLayout()
        
        # Add 20 buttons to the first 4x5 cells of the grid
        self.buttons = []
        for i in range(4):
            for j in range(5):
                button = QPushButton(f'Button {i*5 + j + 1}', self)
                button.setFixedSize(180, 180)
                button.clicked.connect(self.create_button_callback(i, j))
                self.buttons.append(button)
                grid_layout.addWidget(button, i, j)
        
        layout.addLayout(grid_layout)
        
        # Add the back button
        back_button = QPushButton('Back to Main', self)
        back_button.clicked.connect(self.go_back)
        layout.addWidget(back_button)
        
        self.setLayout(layout)

    def create_button_callback(self, row, col):
        def callback():
            print(f'Button at {row}, {col} clicked')
            # Add individual functionality here
        return callback

    def go_back(self):
        self.main_window.show_main_page()

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
        self.main_window.show_main_page()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle('Main Window')
        self.setGeometry(100, 100, 1920, 1080)

        # Create central widget and set layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.stack = QStackedWidget(self.central_widget)
        self.vbox_layout = QVBoxLayout(self.central_widget)
        self.vbox_layout.addWidget(self.stack)

        # Create the main page widget
        self.main_page = QWidget()
        self.stack.addWidget(self.main_page)
        self.grid_layout = QGridLayout(self.main_page)

        # Create buttons
        self.button1 = QPushButton('Button 1', self.main_page)
        self.button2 = QPushButton('Button 2', self.main_page)
        self.button3 = QPushButton('Button 3', self.main_page)

        # Set button sizes
        self.button1.setFixedSize(300, 300)
        self.button2.setFixedSize(300, 300)
        self.button3.setFixedSize(300, 300)

        # Add buttons to the grid layout
        self.grid_layout.addWidget(self.button1, 0, 0)
        self.grid_layout.addWidget(self.button2, 0, 1)
        self.grid_layout.addWidget(self.button3, 0, 2)

        # Connect buttons to methods
        self.button1.clicked.connect(lambda: self.show_tab(1))
        self.button2.clicked.connect(lambda: self.show_tab(2))
        self.button3.clicked.connect(lambda: self.show_tab(3))

        # Create tab pages
        self.tab1 = Tab1(self)
        self.tab2 = Tab2(self)
        self.tab3 = Tab3(self)
        self.stack.addWidget(self.tab1)
        self.stack.addWidget(self.tab2)
        self.stack.addWidget(self.tab3)

        # Initially show the main page
        self.show_main_page()

    def show_tab(self, tab_index):
        self.stack.setCurrentIndex(tab_index)

    def show_main_page(self):
        self.stack.setCurrentIndex(0)

# Entry point of the application
if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainWin = MainWindow()
    mainWin.show()

    sys.exit(app.exec_())






