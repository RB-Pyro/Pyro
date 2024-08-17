import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QStackedWidget, QMainWindow, QLabel, QDialog, QLineEdit, QCheckBox, QFrame
from PyQt5.QtGui import QPainter, QBrush, QColor, QPalette, QFont
from PyQt5.QtCore import Qt, QTimer



class Tab1(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        
        layout = QVBoxLayout(self)
        
        # Create a QWidget to represent the row with input fields
        input_row_widget = QWidget(self)
        
        # Set background color for the row
        palette = input_row_widget.palette()
        palette.setColor(QPalette.Background, QColor(220, 220, 220))  # Light gray color
        input_row_widget.setAutoFillBackground(True)
        input_row_widget.setPalette(palette)
        
        # Create a horizontal layout for the label-input pairs
        input_layout = QHBoxLayout(input_row_widget)
        
        # Set a larger font for the labels
        label_font = QFont()
        label_font.setPointSize(12)  # Set font size (e.g., 12 points)
        
        # Add labels and input fields in a vertical layout within the horizontal layout
        labels = ["Name", "Channel", "Cue", "Time"]
        for label_text in labels:
            vbox = QVBoxLayout()
            
            # Create a frame to act as a box for the label
            label_box = QFrame(self)
            label_box.setFrameShape(QFrame.Box)
            label_box.setLineWidth(1)
            label_box.setFixedWidth(50) 
            
            label = QLabel(label_text, self)
            label.setFont(label_font)  # Apply the larger font to the label
            label.setAlignment(Qt.AlignCenter)  # Center the label horizontally
            
            # Add the label to the label box
            label_box_layout = QVBoxLayout(label_box)
            label_box_layout.addWidget(label)
            label_box_layout.setContentsMargins(5, 5, 5, 5)  # Add padding inside the box
            
            # Add the label box and input field to the vbox
            vbox.addWidget(label_box)
            input_field = QLineEdit(self)
            input_field.setPlaceholderText(f"Enter {label_text}")
            vbox.addWidget(input_field)
            
            # Add the vbox to the horizontal layout
            input_layout.addLayout(vbox)
        
        # Set the layout of the input_row_widget
        input_row_widget.setLayout(input_layout)
        
        # Add the row widget to the main layout
        layout.addWidget(input_row_widget)
        
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
        main_layout.setContentsMargins(10, 10, 10, 10)  # Add some margins to the main layout
        self.setStyleSheet("background-color: lightblue; color: black;")  # Set a background color for the main widget and text color
        self.system_armed = False
        # Create a grid layout for the arm and reset buttons
        top_layout = QGridLayout()
        show_time = 0.00 #placeholder

        self.show_timer = QLabel(f'Show Timer: \n{show_time}',self)
        self.show_timer.setStyleSheet("background-color: white; color: #222222; font-size: 24px;")
        self.show_timer.setFixedSize(200, 100)
        self.show_timer.setAlignment(Qt.AlignCenter)


        # Add Arm System button
        self.arm_button = QPushButton('Arm System', self)
        self.arm_button.setFixedSize(250, 100)
        self.arm_button.setStyleSheet("background-color: green; color: black;")
        self.arm_button.clicked.connect(self.show_confirmation_dialog)

        # Add Unarm System button
        self.reset_arm = QPushButton('Unarm System', self)
        self.reset_arm.setFixedSize(250, 100)
        self.reset_arm.setStyleSheet("background-color: yellow; color: black;")
        self.reset_arm.clicked.connect(self.reset_system)

        # Add buttons to the grid layout
        top_layout.addWidget(self.show_timer,0,0)
        top_layout.addWidget(self.arm_button, 0, 1)  # Place in row 0, column 0
        top_layout.addWidget(self.reset_arm, 0, 2)  # Place in row 0, column 1
        

        # Set background color for top layout
        top_widget = QWidget()
        top_widget.setLayout(top_layout)
        top_widget.setStyleSheet("background-color: lightgray;")  # No padding to ensure buttons aren't blocked
        main_layout.addWidget(top_widget)

        # The rest of your existing code...
        # Define an integer variable
        self.tab_number = 1  # You can change this to any integer

        # Create a QLabel to display the integer in a box
        self.label = QLabel(f"Channel #:  {self.tab_number}", self)
        self.label.setFixedSize(300, 50)  # Set a fixed size for the box
        self.label.setAlignment(Qt.AlignCenter)  # Center the text
        self.label.setStyleSheet("border: 2px solid black; padding: 10px; color: black;")  # Add a border and padding

        # Create buttons and set their fixed size to match the label's height
        left_button = QPushButton('<', self)
        left_button.setFixedSize(50, 50)  # Set size to match label's height
        left_button.clicked.connect(self.decrease_mod_num)

        right_button = QPushButton('>', self)
        right_button.setFixedSize(50, 50)  # Set size to match label's height
        right_button.clicked.connect(self.increase_mod_num)

        # Create a horizontal layout to center the label and add buttons
        label_layout = QHBoxLayout()
        label_layout.addStretch()  # Pushes the content to the center
        label_layout.addWidget(left_button)  # Add left button
        label_layout.addWidget(self.label)  # Add the label
        label_layout.addWidget(right_button)  # Add right button
        label_layout.addStretch()  # Pushes the content to the center

        # Set background color for label layout
        label_widget = QWidget()
        label_widget.setLayout(label_layout)
        label_widget.setStyleSheet("background-color: lightyellow;")  # No padding to ensure buttons aren't blocked
        main_layout.addWidget(label_widget)

        # Create the grid layout
        grid_layout = QGridLayout()

        # Add 20 buttons to the first 4x5 cells of the grid with circles
        self.buttons = []
        self.circles = []
        for i in range(4):
            for j in range(5):
                button_layout = QHBoxLayout()
                button = QPushButton(f'CUE {i * 5 + j + 1}', self)
                button.setFixedSize(150, 150)
                button.clicked.connect(self.create_button_callback(i, j))
                self.buttons.append(button)
                button_layout.addWidget(button)

                circle = CircleLabel()
                self.circles.append(circle)
                button_layout.addWidget(circle)
                grid_layout.addLayout(button_layout, i, j)

        # Set background color for the grid layout
        grid_widget = QWidget()
        grid_widget.setLayout(grid_layout)
        grid_widget.setStyleSheet("background-color: lightcoral;")  # No padding to ensure buttons aren't blocked
        main_layout.addWidget(grid_widget)

        # Add the back button
        back_button_layout = QHBoxLayout()
        back_button_layout.addStretch()
        back_button = QPushButton('Back to Main', self)
        back_button.setFixedHeight(50)
        back_button.clicked.connect(self.go_back)
        back_button_layout.addWidget(back_button)

        # Set background color for back button layout
        back_button_widget = QWidget()
        back_button_widget.setLayout(back_button_layout)
        back_button_widget.setStyleSheet("background-color: lightgreen;")  # No padding to ensure buttons aren't blocked
        main_layout.addWidget(back_button_widget)

        self.setLayout(main_layout)



    def show_confirmation_dialog(self):
       if self.system:
        dialog = QDialog(self)
        dialog.setWindowTitle("Confirmation")
        layout = QVBoxLayout(dialog)

        label = QLabel("Confirm you want to arm system", dialog)
        layout.addWidget(label)

        yes_button = QPushButton("YES", dialog)
        yes_button.clicked.connect(lambda: self.confirm_arm(dialog))
        layout.addWidget(yes_button)

        no_button = QPushButton("NO", dialog)
        no_button.clicked.connect(lambda: self.cancel_arm(dialog))
        layout.addWidget(no_button)

        dialog.setLayout(layout)
        dialog.exec_()  # Show the dialog modally

    def confirm_arm(self, dialog):
        self.arm_system()
        dialog.accept()  # Close the dialog

    def cancel_arm(self, dialog):
        self.reset_system()
        dialog.accept()  # Close the dialog

    def arm_system(self):
        self.arm_button.setText('!SYSTEM ARMED!')
        self.system_armed = True
        self.arm_button.setStyleSheet("background-color: #FF0000;")



    def reset_system(self):
        self.system_armed = False
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

    def decrease_mod_num(self):
        if self.tab_number > 1:
            self.tab_number -= 1
        self.label.setText(f"Channel #:  {self.tab_number}")

    def increase_mod_num(self):
        self.tab_number += 1
        self.label.setText(f"Channel #:  {self.tab_number}")

class Armed_Alert(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle('Armed Alert Warning')
        self.setGeometry(400, 400, 400, 300)
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