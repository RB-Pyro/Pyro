import sys
import csv
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, 
                             QStackedWidget, QMainWindow, QLabel, QDialog, QLineEdit, QCheckBox, 
                             QScrollArea, QSizePolicy,QSpacerItem)
from PyQt5.QtGui import QPainter, QBrush, QColor, QPalette, QFont
from PyQt5.QtCore import Qt, QTimer



class ScrollableItem(QWidget):
    def __init__(self, values, parent=None):
        super().__init__(parent)
        self.values = values
        self.setFixedHeight(50)  # Set the height to 50px

        # Set the background color to light blue, text color to black, and add a black border
        self.setStyleSheet("""
            background-color: lightblue;
            color: black;
            border: 3px solid black;
        """)

        # Create a horizontal box layout for the item
        self.hbox_layout = QHBoxLayout(self)
        self.hbox_layout.setContentsMargins(10, 0, 10, 0)  # Add horizontal margins
        self.hbox_layout.setSpacing(10)  # Add spacing between widgets

        # Create and set up the label with black text color
        self.label = QLabel(self.values, self)
        self.label.setStyleSheet("color: black; padding: 5px;")
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Add a spacer to push the label to fill available space
        self.hbox_layout.addWidget(self.label)  # Add label to the layout with expansion

        # Create and add a stretchable spacer item before the buttons
        hspacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hbox_layout.addItem(hspacer)

        # Create and set up the edit button
        self.edit_button = QPushButton("Edit", self)
        self.edit_button.setFixedSize(80, 40)  # Set height to 40px and width to 80px
        self.edit_button.clicked.connect(self.toggle_edit_save)
        self.hbox_layout.addWidget(self.edit_button)  # Add edit button to the layout

        # Create and set up the delete button
        self.delete_button = QPushButton("Delete", self)
        self.delete_button.setFixedSize(80, 40)  # Set height to 40px and width to 80px
        self.delete_button.setStyleSheet("background-color: lightcoral;")  # Light red color
        self.delete_button.clicked.connect(self.delete_item)
        self.hbox_layout.addWidget(self.delete_button)  # Add delete button to the layout

        # Create a dictionary to hold the text fields when in edit mode
        self.edit_fields = {}

    def toggle_edit_save(self):
        if self.edit_button.text() == "Edit":
            self.switch_to_edit_mode()
        else:
            self.switch_to_save_mode()

    def switch_to_edit_mode(self):
        self.edit_button.setText("Save")
        self.label.hide()  # Hide the label

        # Replace the label with text fields
        for idx, (key, value) in enumerate(zip(self.values.keys(), self.values.values())):
            edit_field = QLineEdit(value, self)
            edit_field.setFixedHeight(40)
            edit_field.setStyleSheet("color: black; padding: 5px;")
            self.hbox_layout.insertWidget(idx, edit_field)
            self.edit_fields[key] = edit_field

    def switch_to_save_mode(self):
        self.edit_button.setText("Edit")
        
        # Update the values in the dictionary
        for key, edit_field in self.edit_fields.items():
            self.values[key] = edit_field.text()

        # Update the label with the new combined text
        combined_values = " | ".join(self.values.values())
        self.label.setText(combined_values)
        self.label.show()  # Show the label again

        # Remove the text fields
        for edit_field in self.edit_fields.values():
            self.hbox_layout.removeWidget(edit_field)
            edit_field.deleteLater()

        # Clear the edit fields dictionary
        self.edit_fields.clear()

    def delete_item(self):
        # Remove the widget from its parent
        self.setParent(None)








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
        self.arm_button.clicked.connect(self.show_confirmation_dialog)

        self.reset_arm = QPushButton('Unarm System', self)
        self.reset_arm.setFixedSize(250, 100)
        self.reset_arm.setStyleSheet("background-color: yellow; color: black;")
        self.reset_arm.clicked.connect(self.reset_system)

        top_layout = QHBoxLayout()
        top_layout.addStretch()  # This pushes the button to the right
        top_layout.addWidget(self.arm_button)
        
        main_layout.addLayout(top_layout)

        # Define an integer variable
        self.tab_number = 1 # You can change this to any integer

        # Create a QLabel to display the integer in a box
        self.label = QLabel(f"Channel #:  {self.tab_number}", self)
        self.label.setFixedSize(300, 50)  # Set a fixed size for the box
        self.label.setAlignment(Qt.AlignCenter)  # Center the text
        self.label.setStyleSheet("border: 2px solid black; padding: 10px;")  # Add a border and padding

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

        main_layout.addLayout(label_layout)  # Add the centered layout to the main layout

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

    def show_confirmation_dialog(self):
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
        self.arm_button.setStyleSheet("background-color: red; color: white;")

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

    def decrease_mod_num(self):
        if self.tab_number > 1:
            self.tab_number -= 1
        self.label.setText(f"Channel #:  {self.tab_number}")

    def increase_mod_num(self):
        self.tab_number += 1
        self.label.setText(f"Channel #:  {self.tab_number}")


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
