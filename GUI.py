import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QStackedWidget, QMainWindow, QLabel, QSlider, QRadioButton, QCheckBox
from PyQt5.QtGui import QPainter, QBrush, QColor
from PyQt5.QtCore import Qt

class Tab1(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout(self)
        label = QLabel("This is Tab 1", self)
        layout.addWidget(label)

        # Add the back button
        back_button_layout = QHBoxLayout()
        back_button_layout.addStretch()
        back_button = QPushButton('Back to Main', self)
        back_button.setFixedHeight(50)
        back_button.clicked.connect(self.go_back)
        back_button_layout.addWidget(back_button)
        layout.addLayout(back_button_layout)

        self.setLayout(layout)

    def go_back(self):
        self.main_window.show_main_page()

class CircleLabel(QLabel):
    def __init__(self, color=Qt.red):
        super().__init__()
        self.color = color
        self.setFixedSize(50, 50)

    def set_color(self, color):
        self.color = color
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QBrush(self.color, Qt.SolidPattern))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, self.width(), self.height())

class Tab2(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        main_layout = QVBoxLayout(self)

        # Add Arm System button at the top right
        self.arm_button = QPushButton('Arm System', self)
        self.arm_button.setFixedSize(250, 100)
        self.arm_button.setStyleSheet("background-color: green; color: white;")
        self.arm_button.clicked.connect(self.arm_system)

        self.reset_arm = QPushButton('Unarm System', self)
        self.reset_arm.setFixedSize(250, 100)
        self.reset_arm.setStyleSheet("background-color: yellow; color: black;")
        self.reset_arm.clicked.connect(self.reset_system)

        top_layout = QHBoxLayout()
        top_layout.addStretch()  # This pushes the button to the right
        top_layout.addWidget(self.arm_button)
        
        main_layout.addLayout(top_layout)

        label = QLabel("This is Tab 2", self)
        main_layout.addWidget(label)

        # Create the grid layout
        grid_layout = QGridLayout()

        # Add 20 buttons to the first 4x5 cells of the grid with circles
        self.buttons = []
        self.circles = []
        for i in range(4):
            for j in range(5):
                button_layout = QHBoxLayout()
                button = QPushButton(f'CUE {i*5 + j + 1}', self)
                button.setFixedSize(150, 150)
                button.clicked.connect(self.create_button_callback(i, j))
                self.buttons.append(button)
                button_layout.addWidget(button)

                circle = CircleLabel()
                self.circles.append(circle)
                button_layout.addWidget(circle)
                grid_layout.addLayout(button_layout, i, j)

        main_layout.addLayout(grid_layout)

        # Add the back button
        back_button_layout = QHBoxLayout()
        back_button_layout.addStretch()
        back_button = QPushButton('Back to Main', self)
        back_button.setFixedHeight(50)
        back_button.clicked.connect(self.go_back)
        back_button_layout.addWidget(back_button)
        main_layout.addLayout(back_button_layout)

        self.setLayout(main_layout)

    def arm_system(self):
        self.arm_button.setText('!SYSTEM ARMED!')
        self.arm_button.setStyleSheet("background-color: red; color: white;")
        
        # Show the armed alert
        alert = Armed_Alert(self.main_window)
        alert.show()

    def reset_system(self):
        self.arm_button.setText("Arm System")
        self.arm_button.setStyleSheet("background-color: green; color: white;")

    def create_button_callback(self, row, col):
        def callback():
            print(f'Button at {row}, {col} clicked')
            # Add individual functionality here
        return callback

    def set_circle_color(self, index, color):
        self.circles[index].set_color(color)

    def go_back(self):
        self.main_window.show_main_page()

class Armed_Alert(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle('Armed Alert Warning')
        self.setGeometry(200, 200, 400, 300)
        layout = QVBoxLayout(self)
        label = QLabel("Armed Alert", self)
        layout.addWidget(label)
        self.setLayout(layout)


class Tab3(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout(self)
        label = QLabel("This is Tab 3", self)
        layout.addWidget(label)

        # Add the back button
        back_button_layout = QHBoxLayout()
        back_button_layout.addStretch()
        back_button = QPushButton('Back to Main', self)
        back_button.setFixedHeight(50)
        back_button.clicked.connect(self.go_back)
        back_button_layout.addWidget(back_button)
        layout.addLayout(back_button_layout)

        self.setLayout(layout)

    def go_back(self):
        self.main_window.show_main_page()


class SettingsWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle('Settings')
        self.setGeometry(200, 200, 400, 300)
        layout = QVBoxLayout(self)
        label = QLabel("Settings", self)
        layout.addWidget(label)

        # Add checkboxes
        self.checkboxes = []
        for i in range(5):
            checkbox = QCheckBox(f'Checkbox {i+1}', self)
            checkbox.stateChanged.connect(lambda state, i=i: self.checkbox_changed(state, i))
            layout.addWidget(checkbox)
            self.checkboxes.append(checkbox)

        self.setLayout(layout)

    def checkbox_changed(self, state, index):
        is_checked = state == Qt.Checked
        print(f"Checkbox {index+1} is {'checked' if is_checked else 'unchecked'}")
        # Placeholder for actual functionality


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
        self.button1 = QPushButton('Build A Script', self.main_page)
        self.button2 = QPushButton('Manual Fire', self.main_page)
        self.button3 = QPushButton('Scripted Show', self.main_page)
        self.settings_button = QPushButton('Settings', self.main_page)

        # Set button sizes
        self.button1.setFixedSize(300, 300)
        self.button2.setFixedSize(300, 300)
        self.button3.setFixedSize(300, 300)
        self.settings_button.setFixedSize(300, 300)

        # Add buttons to the grid layout
        self.grid_layout.addWidget(self.button1, 0, 0)
        self.grid_layout.addWidget(self.button2, 0, 1)
        self.grid_layout.addWidget(self.button3, 0, 2)
        self.grid_layout.addWidget(self.settings_button, 1, 1)

        # Connect buttons to methods
        self.button1.clicked.connect(lambda: self.show_tab(1))
        self.button2.clicked.connect(lambda: self.show_tab(2))
        self.button3.clicked.connect(lambda: self.show_tab(3))
        self.settings_button.clicked.connect(self.show_settings)

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

    def show_settings(self):
        self.settings_window = SettingsWindow(self)
        self.settings_window.show()

# Entry point of the application
if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainWin = MainWindow()
    mainWin.show()

    sys.exit(app.exec_())


