import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, 
                             QStackedWidget, QMainWindow, QLabel, QDialog, QLineEdit, QCheckBox, 
                             QScrollArea, QSizePolicy)
from PyQt5.QtGui import QPainter, QBrush, QColor, QPalette, QFont
from PyQt5.QtCore import Qt, QTimer

class ScrollableItem(QWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setFixedHeight(50)  # Set the height to 50px

        # Create a horizontal box layout for the item
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)  # Add horizontal margins
        layout.setSpacing(10)  # Add spacing between widgets

        # Create and set up the label
        self.label = QLabel(text, self)
        self.label.setStyleSheet("padding: 5px;")
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.label)  # Add label with expanding size policy

        # Create and set up the edit button
        self.edit_button = QPushButton("Edit", self)
        self.edit_button.setFixedSize(80, 40)  # Set height to 40px and width to 80px
        layout.addWidget(self.edit_button)

        # Create and set up the delete button
        self.delete_button = QPushButton("Delete", self)
        self.delete_button.setFixedSize(80, 40)  # Set height to 40px and width to 80px
        self.delete_button.clicked.connect(self.delete_item)
        layout.addWidget(self.delete_button)

        layout.addStretch()  # Ensure the layout expands
        self.setLayout(layout)

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
            input_field.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
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
        self.scroll_content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        self.scroll_layout.setSpacing(0)  # Remove spacing
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
        # Retrieve text from input fields
        texts = [input_field.text() for input_field in self.input_fields]

        # Create a new ScrollableItem with the text from the input fields
        if any(texts):
            combined_text = " | ".join(texts)
            item = ScrollableItem(combined_text, self)
            self.scroll_layout.addWidget(item)

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

        # Add settings layout and widgets here
        # For example, you can add checkboxes, sliders, etc.

        self.setLayout(layout)

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
