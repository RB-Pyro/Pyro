import sys
import os
import csv
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, 
                             QStackedWidget, QMainWindow, QLabel, QDialog, QLineEdit, QCheckBox, 
                             QScrollArea, QSizePolicy,QSpacerItem,QMessageBox,QFileDialog,QProgressBar)
from PyQt5.QtGui import QPainter, QBrush, QColor, QPalette, QFont,QDrag
from PyQt5.QtCore import Qt, QTimer,QMimeData,pyqtSignal,QStandardPaths

class ScrollableItem(QWidget):
    def __init__(self, values_dict, parent=None):
        super().__init__(parent)
        self.values = values_dict
        self.setFixedHeight(50)  # Set the height to 50px

        # Set the background color to light blue, text color to black, and add a black border
        self.setStyleSheet("""
            background-color: lightblue;
            color: black;
            border: 3px solid black;
        """)

        # Create a horizontal box layout for the item
        hbox_layout = QHBoxLayout(self)
        hbox_layout.setContentsMargins(10, 0, 10, 0)  # Add horizontal margins
        hbox_layout.setSpacing(10)  # Add spacing between widgets

        # Create QLabel widgets for each value in the dictionary and add them to the layout
        self.labels = []
        for key, value in self.values.items():
            label = QLabel(value, self)
            label.setStyleSheet("color: black; padding: 5px;")
            label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            hbox_layout.addWidget(label)
            self.labels.append(label)

        # Create and set up the edit button
        self.edit_button = QPushButton("Edit", self)
        self.edit_button.setFixedSize(80, 40)  # Set height to 40px and width to 80px
        self.edit_button.clicked.connect(self.toggle_edit_save)
        hbox_layout.addWidget(self.edit_button)  # Add edit button to the layout

        # Create and set up the delete button
        self.delete_button = QPushButton("Delete", self)
        self.delete_button.setFixedSize(80, 40)  # Set height to 40px and width to 80px
        self.delete_button.setStyleSheet("background-color: lightcoral;")  # Light red color
        self.delete_button.clicked.connect(self.delete_item)
        hbox_layout.addWidget(self.delete_button)  # Add delete button to the layout

    def delete_item(self):
        # Remove the widget from its parent
        self.setParent(None)

    def toggle_edit_save(self):
        if self.edit_button.text() == "Edit":
            self.switch_to_edit_mode()
        else:
            self.save_edits()

    def switch_to_edit_mode(self):
        # Replace labels with line edits
        self.line_edits = []
        for label in self.labels:
            line_edit = QLineEdit(label.text(), self)
            line_edit.setStyleSheet("color: black; padding: 5px;")
            line_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout().replaceWidget(label, line_edit)
            label.hide()
            self.line_edits.append(line_edit)

        self.edit_button.setText("Save")

    def save_edits(self):
        # Save the values from the line edits back into the dictionary
        for key, line_edit in zip(self.values.keys(), self.line_edits):
            self.values[key] = line_edit.text()

        # Replace line edits with updated labels
        for label, line_edit in zip(self.labels, self.line_edits):
            label.setText(line_edit.text())
            self.layout().replaceWidget(line_edit, label)
            line_edit.hide()
            label.show()

        self.edit_button.setText("Edit")






class Tab1(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        # Define labels at the class level
        self.labels = ["Name", "Channel", "Cue", "Time"]

        # Initialize the dictionary to store input data
        self.input_data = {}
        self.scrollable_data = []  # To store the scrollable area data

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
        for i, label_text in enumerate(self.labels):
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
        for i in range(len(self.labels)):
            input_field = QLineEdit(self)
            input_field.setPlaceholderText(f"Enter {self.labels[i]}")
            input_field.setFixedHeight(40)
            input_field.setStyleSheet("color: black; padding: 5px;")
            self.input_fields.append(input_field)
            self.input_grid.addWidget(input_field, 0, i)
        
        # Add the label container to the first row of the main grid layout
        main_layout.addWidget(label_container, 0, 0, 1, len(self.labels))

        # Add the input container to the second row of the main grid layout
        main_layout.addWidget(self.input_container, 1, 0, 1, len(self.labels))

        # Create a scrollable area below the input fields
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)  # Allow the content to resize within the scroll area
        self.scroll_content = QWidget()
        self.scroll_content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.scroll_layout = QGridLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        self.scroll_layout.setSpacing(0)  # Remove spacing
        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_content)

        # Add the scrollable area to the main layout
        main_layout.addWidget(self.scroll_area, 2, 0, 1, len(self.labels))  # Span across all columns below input fields

        # Create a widget for the right side of the page
        right_side_widget = QWidget(self)
        right_side_widget.setStyleSheet("background-color: lightcoral;")
        
        # Create a grid layout for the right side widget
        right_side_grid = QGridLayout(right_side_widget)
        
        # Add 3 buttons manually to the right side grid layout
        button1 = QPushButton("Add To Script", self)
        button2 = QPushButton("Export Script", self)
        button3 = QPushButton("Import Script", self)
        
        # Connect Button 1 to a method that handles input data
        button1.clicked.connect(self.handle_button1_click)
        button2.clicked.connect(self.export_to_csv)
        button3.clicked.connect(self.import_from_csv)  # Connect button3 to import method
        
        # Add buttons to the grid layout
        right_side_grid.addWidget(button1, 0, 0)
        right_side_grid.addWidget(button2, 1, 0)
        right_side_grid.addWidget(button3, 2, 0)
        
        main_layout.addWidget(right_side_widget, 0, len(self.labels), 2, 1)  # Spanning all rows on the right
        
        # Add another widget below the red one on the left
        left_side_widget = QWidget(self)
        left_side_widget.setStyleSheet("background-color: lightgreen;")
        main_layout.addWidget(left_side_widget, 2, len(self.labels), 2, 1)  # Column len(labels), spanning 2 rows
        
        # Adjust the back button placement
        back_button = QPushButton('Back to Main', self)
        back_button.setFixedHeight(50)
        back_button.clicked.connect(self.go_back)
        main_layout.addWidget(back_button, 4, 0, 1, len(self.labels) + 1)

        self.setLayout(main_layout)

    def handle_button1_click(self):
        # Retrieve text from input fields and store it in the dictionary
        self.input_data = {label: input_field.text() for label, input_field in zip(self.labels, self.input_fields)}

        # Add the data to scrollable_data
        if any(self.input_data.values()):  # Check if any data is entered
            self.scrollable_data.append(self.input_data.copy())  # Store a copy of the input data

            # Create a new ScrollableItem with the input data dictionary
            item = ScrollableItem(self.input_data.copy(), self)
            self.scroll_layout.addWidget(item)

        # Clear input fields and reset placeholders
        for input_field in self.input_fields:
            input_field.clear()
            input_field.setPlaceholderText(f"Enter {input_field.placeholderText().split(' ')[1]}")

        # Set focus back to the first input field
        if self.input_fields:
            self.input_fields[0].setFocus()

    def export_to_csv(self):
        if not self.scrollable_data:
            QMessageBox.warning(self, "No Data", "There is no data to export.")
            return

        # Create a pop-up dialog for file name input
        file_name_dialog = QDialog(self)
        file_name_dialog.setWindowTitle("Save CSV")

        layout = QVBoxLayout(file_name_dialog)
        
        label = QLabel("Enter file name:", file_name_dialog)
        layout.addWidget(label)

        file_name_input = QLineEdit(file_name_dialog)
        file_name_input.setPlaceholderText("File name")
        layout.addWidget(file_name_input)

        save_button = QPushButton("Save", file_name_dialog)
        layout.addWidget(save_button)

        # Define the behavior when the save button is clicked
        def save_file():
            file_name = file_name_input.text().strip()
            if not file_name:
                QMessageBox.warning(file_name_dialog, "Invalid Name", "Please enter a valid file name.")
                return
            
            # Get the desktop path based on the platform
            if os.name == 'nt':  # For Windows
                desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
            else:  # For macOS and Linux
                desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')

            full_path = os.path.join(desktop_path, file_name + ".csv")
            
            # Save the CSV file
            with open(full_path, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=self.labels)
                writer.writeheader()
                writer.writerows(self.scrollable_data)
            
            QMessageBox.information(self, "Success", f"File saved to {full_path}")
            file_name_dialog.accept()  # Close the dialog

        save_button.clicked.connect(save_file)
        
        file_name_dialog.exec_()

    def import_from_csv(self):
        # Open file dialog to select the CSV file
        file_name, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
        if not file_name:
            return  # User canceled the dialog

        # Clear the current scrollable area
        self.scrollable_data = []
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Read data from the CSV file
        with open(file_name, 'r') as file:
            reader = csv.DictReader(file)
            self.scrollable_data = list(reader)  # Store data into scrollable_data

            # Add data to the scrollable area
            for data in self.scrollable_data:
                item = ScrollableItem(data, self)
                self.scroll_layout.addWidget(item)

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

        # Main layout
        layout = QVBoxLayout(self)

        # Progress bar at the top
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedHeight(30)  # Increase the height for better visibility
        layout.addWidget(self.progress_bar)

        # Start button
        start_button = QPushButton('Start Progress', self)
        start_button.clicked.connect(self.start_progress)
        layout.addWidget(start_button)

        # Add the back button
        back_button_layout = QHBoxLayout()
        back_button_layout.addStretch()
        back_button = QPushButton('Back to Main', self)
        back_button.setFixedHeight(50)
        back_button.clicked.connect(self.go_back)
        back_button_layout.addWidget(back_button)
        layout.addLayout(back_button_layout)

        self.setLayout(layout)

        # Timer for progress bar
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)

    def start_progress(self):
        self.progress_bar.setValue(0)  # Reset progress
        self.timer.start(1000)  # Update every second

    def update_progress(self):
        current_value = self.progress_bar.value()
        if current_value < 100:
            self.progress_bar.setValue(current_value + 10)  # Increase progress by 10%
        else:
            self.timer.stop()  # Stop the timer once progress reaches 100%

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
