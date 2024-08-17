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
        self.label.setStyleSheet("padding: 5px;")
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
        # Create a grid layout for the scroll_content
        self.scroll_layout = QGridLayout(self.scroll_content)
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
        self.back_button = QPushButton('Back to Main', self)
        self.back_button.setFixedHeight(50)
        self.back_button.clicked.connect(self.go_back)
        main_layout.addWidget(self.back_button, 4, 0, 1, len(labels) + 1)

        self.setLayout(main_layout)

    def handle_button1_click(self):
        # Create a new horizontal container widget
        container = QWidget(self)
        horizontal_layout = QHBoxLayout(container)

        # Add text from input fields to the horizontal layout
        for input_field in self.input_fields:
            text = input_field.text()
            if text:
                label = QLabel(text, self)
                label.setStyleSheet("border: 1px solid black; padding: 5px;")  # Optional: Add border and padding for visibility
                horizontal_layout.addWidget(label)
                # Debug statement to confirm labels are added
                print(f"Added label with text: {text}")

        # Add the new container to the scroll layout (as a new row in the grid)
        row_position = self.scroll_layout.rowCount()
        self.scroll_layout.addWidget(container, row_position, 0)

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
        top_layout.addWidget(self.show_timer,0,0,1,2)
        top_layout.addWidget(self.arm_button, 1, 0)
        top_layout.addWidget(self.reset_arm, 1, 1)

        # Add top layout to the main layout
        main_layout.addLayout(top_layout)
        self.setLayout(main_layout)

    def show_confirmation_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Confirmation")
        dialog.setStyleSheet("background-color: lightgray; color: black;")  # Set a background color for the dialog and text color

        layout = QVBoxLayout(dialog)

        label = QLabel("Are you sure you want to arm the system?", dialog)
        layout.addWidget(label)

        button_layout = QHBoxLayout()
        confirm_button = QPushButton("Yes", dialog)
        cancel_button = QPushButton("No", dialog)
        button_layout.addWidget(confirm_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

        confirm_button.clicked.connect(self.arm_system)
        cancel_button.clicked.connect(dialog.reject)

        dialog.exec_()

    def arm_system(self):
        self.system_armed = True
        self.arm_button.setText("System Armed")
        self.arm_button.setStyleSheet("background-color: red; color: white;")
        self.show_timer.setText("Show Timer: \n00.00")
        # Return to main page after arm is pressed
        self.main_window.show_main_page()

    def reset_system(self):
        self.system_armed = False
        self.arm_button.setText("Arm System")
        self.arm_button.setStyleSheet("background-color: green; color: black;")
        self.show_timer.setText("Show Timer: \n00.00")
        # Return to main page after unarm is pressed
        self.main_window.show_main_page()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 Main Window")
        self.setGeometry(100, 100, 800, 600)

        # Create a stacked widget for the main and tab widgets
        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        # Create instances of tabs
        self.tab1 = Tab1(self)
        self.tab2 = Tab2(self)

        # Add tabs to the stacked widget
        self.stacked_widget.addWidget(self.tab1)
        self.stacked_widget.addWidget(self.tab2)

        # Show the main page initially
        self.show_main_page()

    def show_main_page(self):
        self.stacked_widget.setCurrentWidget(self.tab1)

    def show_tab2(self):
        self.stacked_widget.setCurrentWidget(self.tab2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
