import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, 
                             QStackedWidget, QMainWindow, QLabel, QDialog, QLineEdit, QCheckBox, 
                             QScrollArea)
from PyQt5.QtGui import QPainter, QBrush, QColor, QPalette, QFont
from PyQt5.QtCore import Qt, QTimer

class ScrollableItem(QWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setLayout(QHBoxLayout())
        
        # Create and set up the label
        self.label = QLabel(text, self)
        self.label.setStyleSheet( "padding: 5px;")
        self.layout().addWidget(self.label)
        
        # Create and set up the delete button
        self.delete_button = QPushButton("Delete", self)
        self.delete_button.clicked.connect(self.delete_item)
        self.layout().addWidget(self.delete_button)
    
    def delete_item(self):
        # Remove the widget from its parent
        self.setParent(None)  

class Tab1(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        
        # Use QGridLayout for the main layout
        main_layout = QGridLayout(self)
        
        # Create a QWidget with fixed height for the labels
        label_container = QWidget(self)
        label_container.setFixedHeight(50)  # Set the height of the container to 50px
        
        # Set a larger font for the labels
        label_font = QFont()
        label_font.setPointSize(24)
        
        # Create a grid layout for the labels within the container
        label_grid = QGridLayout(label_container)
        labels = ["Name", "Channel", "Cue", "Time"]
        for i, label_text in enumerate(labels):
            label = QLabel(label_text, self)
            label.setFont(label_font)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("background-color: lightgray;")
            label_grid.addWidget(label, 0, i)
        
        # Create a widget for the input fields with a background color
        self.input_container = QWidget(self)
        self.input_container.setStyleSheet("background-color: #222222;")
        
        # Create a grid layout for the input fields
        self.input_grid = QGridLayout(self.input_container)
        self.input_fields = []
        for i in range(len(labels)):
            input_field = QLineEdit(self)
            input_field.setPlaceholderText(f"Enter {labels[i]}")
            input_field.setFixedHeight(40)
            input_field.setStyleSheet("color: black; padding: 5px;")
            self.input_fields.append(input_field)
            self.input_grid.addWidget(input_field, 0, i)
        
        # Add the label container to the first row of the main grid layout
        main_layout.addWidget(label_container, 0, 0, 1, len(labels))
        
        # Add the input container to the second row of the main grid layout
        main_layout.addWidget(self.input_container, 1, 0, 1, len(labels))
        
        # Create a scrollable area below the input fields
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)  # Allow the content to resize within the scroll area
        self.scroll_content = QWidget()
        #self.scroll_content.setStyleSheet("background-color: lightyellow;")
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_content)
        
        # Add the scrollable area to the main layout
        main_layout.addWidget(self.scroll_area, 2, 0, 1, len(labels))  # Span across all columns below input fields
        
        # Create a widget for the right side of the page
        right_side_widget = QWidget(self)
        right_side_widget.setStyleSheet("background-color: lightcoral;")
        
        # Create a grid layout for the right side widget
        right_side_grid = QGridLayout(right_side_widget)
        
        # Add 3 buttons manually to the right side grid layout
        button1 = QPushButton("Button 1", self)
        button2 = QPushButton("Button 2", self)
        button3 = QPushButton("Button 3", self)
        
        # Connect Button 1 to a method that handles input data
        button1.clicked.connect(self.handle_button1_click)
        
        # Add buttons to the grid layout
        right_side_grid.addWidget(button1, 0, 0)
        right_side_grid.addWidget(button2, 1, 0)
        right_side_grid.addWidget(button3, 2, 0)
        
        main_layout.addWidget(right_side_widget, 0, len(labels), 2, 1)  # Spanning all rows on the right
        
        # Add another widget below the red one on the left
        left_side_widget = QWidget(self)
        left_side_widget.setStyleSheet("background-color: lightgreen;")
        main_layout.addWidget(left_side_widget, 2, len(labels), 2, 1)  # Column len(labels), spanning 2 rows
        
        # Adjust the back button placement
        back_button = QPushButton('Back to Main', self)
        back_button.setFixedHeight(50)
        back_button.clicked.connect(self.go_back)
        main_layout.addWidget(back_button, 4, 0, 1, len(labels) + 1)

        self.setLayout(main_layout)

    def handle_button1_click(self):
        # Add text from input fields to the scrollable area
        for input_field in self.input_fields:
            text = input_field.text()
            if text:
                item = ScrollableItem(text, self)
                self.scroll_layout.addWidget(item)
        
        # Ensure that the layout updates and scroll area resizes
        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_content)
        
        # Clear input fields and reset placeholders
        for input_field in self.input_fields:
            input_field.clear()
            input_field.setPlaceholderText(f"Enter {input_field.placeholderText().split(' ')[1]}")

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
        self.label = QLabel(f"Channel #: {self.tab_number}")
        self.label.setFixedSize(200, 100)
        self.label.setStyleSheet("background-color: white; color: black; font-size: 24px;")
        self.label.setAlignment(Qt.AlignCenter)

        # Create a QVBoxLayout for the label
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.label)
        self.setLayout(self.vbox)
    
    def show_confirmation_dialog(self):
        if not self.system_armed:
            self.confirmation_dialog = QDialog(self)
            self.confirmation_dialog.setWindowTitle("Confirmation")
            layout = QVBoxLayout()
            
            message_label = QLabel("Are you sure you want to arm the system?", self)
            layout.addWidget(message_label)
            
            button_box = QHBoxLayout()
            yes_button = QPushButton("Yes", self)
            no_button = QPushButton("No", self)
            button_box.addWidget(yes_button)
            button_box.addWidget(no_button)
            layout.addLayout(button_box)
            
            yes_button.clicked.connect(self.arm_system)
            no_button.clicked.connect(self.confirmation_dialog.accept)
            
            self.confirmation_dialog.setLayout(layout)
            self.confirmation_dialog.exec_()
        else:
            self.arm_button.setText('Arm System')
            self.arm_button.setStyleSheet("background-color: green; color: black;")
            self.reset_arm.setEnabled(True)
            self.system_armed = False

    def arm_system(self):
        self.arm_button.setText('Disarm System')
        self.arm_button.setStyleSheet("background-color: red; color: black;")
        self.reset_arm.setEnabled(True)
        self.system_armed = True
        self.confirmation_dialog.accept()
    
    def reset_system(self):
        self.arm_button.setText('Arm System')
        self.arm_button.setStyleSheet("background-color: green; color: black;")
        self.reset_arm.setEnabled(False)
        self.system_armed = False

    # The rest of your existing code...

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        self.tab1 = Tab1(self)
        self.tab2 = Tab2(self)
        self.stacked_widget.addWidget(self.tab1)
        self.stacked_widget.addWidget(self.tab2)
        
        # Set the window to full screen
        self.showFullScreen()

        self.show()


    def show_main_page(self):
        self.stacked_widget.setCurrentWidget(self.tab1)
    
    def show_second_page(self):
        self.stacked_widget.setCurrentWidget(self.tab2)

app = QApplication(sys.argv)
window = MainWindow()
sys.exit(app.exec_())
