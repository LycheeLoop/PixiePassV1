## -------------------------- IMPORTS ------------------------------- ##
from PySide6.QtCore import Qt, Slot, QSize
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QGridLayout, QMessageBox, QDialogButtonBox
from PySide6 import QtSvg
from homeicon import HomeIcon
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from PySide6.QtGui import QPixmap,QImage, QPainter
from PySide6.QtSvg import QSvgRenderer
import secrets
import string
from cryptography.fernet import Fernet
from encryption import cipher
from utils import get_image_path






## -------------------------- ADD PASSWORD SCREEN (Q-WIDGET) ------------------------------- ##

class AddPassword(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("PixiePass - Add Password")

        # Create grid layout
        self.grid = QGridLayout(self)

        # Add the home icon to the layout
        self.home_icon_label = HomeIcon(self, self.go_home)
        self.grid.addWidget(self.home_icon_label, 0, 3, Qt.AlignTop | Qt.AlignRight)

        # Create title label of screen
        self.label = QLabel("Add a New Password", self)
        self.label.setAlignment(Qt.AlignTop)
        self.label.setStyleSheet("font-size: 18px; font-weight: bold; font-family: Arial; ")
        self.grid.addWidget(self.label, 0, 0, 1, 2)

        # Create entry LABELS and FIELDS
        self.website_label = QLabel("Website:", self) #website label
        self.website_label.setStyleSheet("font-size: 12px")
        self.grid.addWidget(self.website_label, 1, 0, 1, 1)

        self.website_entry = QLineEdit(self)  # website entry
        self.website_entry.setPlaceholderText("Enter website... ")
        self.grid.addWidget(self.website_entry, 1, 1, 1, 3)

        self.username_label = QLabel("Username:", self) #username label
        self.username_label.setStyleSheet("font-size: 12px")
        self.grid.addWidget(self.username_label, 2, 0, 1, 1)

        self.username_entry = QLineEdit(self)  # username entry
        self.username_entry.setPlaceholderText("Enter username... ")
        self.grid.addWidget(self.username_entry, 2, 1, 1, 3)


        self.password_label = QLabel("Password:", self) #password label
        self.password_label.setStyleSheet("font-size: 12px")
        self.grid.addWidget(self.password_label, 3, 0, 1, 1)


        self.password_entry = QLineEdit(self) #password entry
        self.password_entry.setPlaceholderText("Enter password... ")
        self.grid.addWidget(self.password_entry, 3, 1, 1, 3)

        # Create generate password button
        self.generate_button = QPushButton("Generate Password", self)
        self.generate_button.setCursor(Qt.PointingHandCursor)
        # Add button to grid layout and set stretch factors
        self.grid.addWidget(self.generate_button, 4, 0, 1, 2)
        # Connect generate button to slot for functionality
        self.generate_button.clicked.connect(self.generate_password)

        # Create add password button
        self.add_button = QPushButton("Add Password +", self)
        self.add_button.setStyleSheet("""QPushButton { background-color:#B4CE78; 
                }
                QPushButton:hover {
                    background-color: #C0C0C0;
                }
                """)
        self.add_button.setCursor(Qt.PointingHandCursor)
        # Add button to grid layout and set stretch factors
        self.grid.addWidget(self.add_button, 4, 2, 1, 2)
        # Connect add button to slot for functionality
        self.add_button.clicked.connect(self.on_submit_button_clicked)

        # Use layout stretch to ensure all buttons expand to equal width
        self.grid.setColumnStretch(0, 1)
        self.grid.setColumnStretch(1, 1)

    ## -------------------------- Add password methods ------------------------------- ##

    @Slot()
    def go_home(self, event):
        # Navigate to the home screen
        parent_widget = self.parent()  # Get the parent (which is the QStackedWidget)
        parent_widget.setCurrentIndex(0)  # Set the current index to home screen (index 0)
        self.password_entry.clear()

    ### Generate a random password and automatically fill password entry
    @Slot()
    def generate_password(self):
        alphabet = string.ascii_letters + string.digits
        while True:
            generated_password = ''.join(secrets.choice(alphabet) for i in range(13))
            if (any(c.islower() for c in generated_password)
                    and any(c.isupper() for c in generated_password)
                    and sum(c.isdigit() for c in generated_password) >= 3):
                print(generated_password) #for debugging
                self.password_entry.setText(generated_password)
                break





    ### Submit all changes to account and update database
    @Slot()
    def on_submit_button_clicked(self):
        from main import Account, add_account, find_duplicate

        website = self.website_entry.text().capitalize()
        username = self.username_entry.text()
        password = self.password_entry.text()


        #Verify details were entered correctly
        if not website or not username or not password:
            msg = QMessageBox(self)
            msg.setWindowTitle("Review")
            msg.setText("Please fill in all fields.")
            # Add a button
            msg.setStandardButtons(QMessageBox.Ok)
            # Access the layout and center the button
            msg_layout = msg.layout()
            button_box = msg.findChild(QDialogButtonBox)
            msg_layout.setAlignment(button_box, Qt.AlignCenter)
            # Change cursor for the "Ok" button
            ok_button = button_box.button(QDialogButtonBox.Ok)  # Use QDialogButtonBox.Ok instead of QMessageBox.Ok
            ok_button.setCursor(Qt.PointingHandCursor)
            # Load the custom icon using the relative path
            pixmap = QPixmap(get_image_path("warning.png"))  # Correctly use the function to get the image path
            # Resize the icon by scaling the QPixmap
            scaled_pixmap = pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Set width and height
            # Set the scaled pixmap as the icon for the QMessageBox
            msg.setIconPixmap(scaled_pixmap)
            msg.exec()

        ## Check if account is already in database. If not, add new account to database.
        if website and username and password:
            if find_duplicate(website) == True:
                msg = QMessageBox(self)
                msg.setWindowTitle("Review")
                msg.setText("Website already exists in PixiePass.")
                # Add a button
                msg.setStandardButtons(QMessageBox.Ok)
                # Access the layout and center the button
                msg_layout = msg.layout()
                button_box = msg.findChild(QDialogButtonBox)
                msg_layout.setAlignment(button_box, Qt.AlignCenter)
                # Change cursor for the "Ok" button
                ok_button = button_box.button(QDialogButtonBox.Ok)  # Use QDialogButtonBox.Ok instead of QMessageBox.Ok
                ok_button.setCursor(Qt.PointingHandCursor)
                # Load the custom icon using the relative path
                pixmap = QPixmap(get_image_path("warning.png"))  # Correctly use the function to get the image path
                # Resize the icon by scaling the QPixmap
                scaled_pixmap = pixmap.scaled(60, 60, Qt.KeepAspectRatio,
                                              Qt.SmoothTransformation)  # Set width and height
                # Set the scaled pixmap as the icon for the QMessageBox
                msg.setIconPixmap(scaled_pixmap)
                msg.exec()

            if find_duplicate(website) == False:
                encrypted_password = self.encrypt_password(password)
                add_account(website, username, encrypted_password)
                msg = QMessageBox(self)
                msg.setWindowTitle("Success")
                msg.setText("Password added successfully!")
                # Add a button
                msg.setStandardButtons(QMessageBox.Ok)
                # Access the layout and center the button
                msg_layout = msg.layout()
                button_box = msg.findChild(QDialogButtonBox)
                msg_layout.setAlignment(button_box, Qt.AlignCenter)
                # Change cursor for the "Ok" button
                ok_button = button_box.button(QDialogButtonBox.Ok)  # Use QDialogButtonBox.Ok instead of QMessageBox.Ok
                ok_button.setCursor(Qt.PointingHandCursor)
                # Load the custom icon
                pixmap = QPixmap(get_image_path("magicwand.png"))  # Replace with your actual image path
                # Resize the icon by scaling the QPixmap
                scaled_pixmap = pixmap.scaled(55, 55, Qt.KeepAspectRatio,
                                              Qt.SmoothTransformation)  # Set desired width and height
                # Set the scaled pixmap as the icon for the QMessageBox
                msg.setIconPixmap(scaled_pixmap)
                msg.exec()
                # Clear the QLineEdit fields after the message box is closed
                self.website_entry.clear()
                self.username_entry.clear()
                self.password_entry.clear()

    # Encrypt the password using Fernet
    def encrypt_password(self, password):
        return cipher.encrypt(password.encode()).decode()
