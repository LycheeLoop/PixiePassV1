## -------------------------- IMPORTS ------------------------------- ##
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QMessageBox, QDialogButtonBox
from homeicon import HomeIcon
from encryption import cipher
from utils import get_image_path



## -------------------------- SEARCH ACCOUNT SCREEN (Q-WIDGET) ------------------------------- ##

class SearchPassword(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create grid layout
        self.grid = QGridLayout(self)

        # Add the home icon to the layout
        self.home_icon_label = HomeIcon(self, self.go_home)
        self.grid.addWidget(self.home_icon_label, 0, 4, Qt.AlignTop | Qt.AlignRight)

        # Create title of screen
        self.label = QLabel("Search PixiePass", self)
        self.label.setAlignment(Qt.AlignTop)
        self.label.setStyleSheet("font-size: 18px; font-weight: bold; font-family: Arial; ")
        self.grid.addWidget(self.label, 0, 0, 1, 2)

        # Create initial website entry LABELS and FIELD
        self.website_label = QLabel("Website:", self)  # website
        self.website_label.setStyleSheet("font-size: 12px")
        self.grid.addWidget(self.website_label, 3, 0)

        self.website_entry = QLineEdit(self)  # website
        self.website_entry.setPlaceholderText("Enter the website ")
        self.grid.addWidget(self.website_entry, 3, 1, 1, 3)

        # Create label to display the found account credentials ( Initially hidden )
        self.account_label = QLabel()
        self.account_label.setStyleSheet("font-size: 12px")
        self.account_label.setVisible(False)
        self.grid.addWidget(self.account_label, 2, 0)

        # Create find button
        self.find_button = QPushButton("Find Password 🔎", self)
        self.find_button.setCursor(Qt.PointingHandCursor)
        # Add button to grid layout and set stretch factors
        self.grid.addWidget(self.find_button, 4, 0, 1, 3)
        # Connect add button to slot for functionality
        self.find_button.clicked.connect(self.on_search_button_clicked)

        # Create listed accounts button
        self.reference_button = QPushButton("Saved Accounts", self)
        self.reference_button.setCursor(Qt.PointingHandCursor)
        # Add button to grid layout and set stretch factors
        self.grid.addWidget(self.reference_button, 4, 3, 1, 2)
        # Connect add button to slot for functionality
        self.reference_button.clicked.connect(self.reference_button_clicked)

        # Create EDIT password button
        self.edit_button = QPushButton("Edit ✏️", self)
        self.edit_button.setStyleSheet("""QPushButton { background-color:#C0C0C0; 
                }
                QPushButton:hover {
                    background-color: #4e4f4e;
                }
                """)
        self.edit_button.setCursor(Qt.PointingHandCursor)
        self.grid.addWidget(self.edit_button, 2, 3)
        self.edit_button.setVisible(False)
        # Connect edit button to slot for functionality
        self.edit_button.clicked.connect(self.edit_button_clicked)

        # Create edit account fields (initially hidden)
        self.edit_label = QLabel(f"Edit Account", self)
        self.edit_label.setAlignment(Qt.AlignTop)
        self.edit_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.grid.addWidget(self.edit_label, 0, 0, 1, 2)
        self.edit_label.setVisible(False)

        # Create new website entry label and field
        self.new_website_label = QLabel("Website:", self)  # EDITED website label
        self.new_website_label.setStyleSheet("font-size: 12px")
        self.grid.addWidget(self.new_website_label, 1, 0)
        self.new_website_label.setVisible(False)

        self.new_website_entry = QLineEdit(self) #EDITED website entry
        self.new_website_entry.setPlaceholderText("Enter the website ")
        self.grid.addWidget(self.new_website_entry, 1, 2, 1, 3)
        self.new_website_entry.setVisible(False)

        # Create new username entry label and field
        self.new_username_label = QLabel("Username:", self)  # EDITED username label
        self.new_username_label.setStyleSheet("font-size: 12px")
        self.grid.addWidget(self.new_username_label, 2, 0)
        self.new_username_label.setVisible(False)

        self.new_username_entry = QLineEdit(self)
        self.new_username_entry.setPlaceholderText("Enter the username ") #EDITED username entry label
        self.grid.addWidget(self.new_username_entry, 2, 2, 1, 3)
        self.new_username_entry.setVisible(False)

        # Create new password entry label and field
        self.new_password_label = QLabel("Password:", self)  # EDITED password label
        self.new_password_label.setStyleSheet("font-size: 12px")
        self.grid.addWidget(self.new_password_label, 3, 0)
        self.new_password_label.setVisible(False)

        self.new_password_entry = QLineEdit(self)  # EDITED password entry
        self.new_password_entry.setPlaceholderText("Enter the password ")
        self.grid.addWidget(self.new_password_entry, 3, 2, 1, 3)
        self.new_password_entry.setVisible(False)

        # Create UPDATE ACCOUNT button
        self.update_button = QPushButton("Update Account", self)
        self.update_button.setCursor(Qt.PointingHandCursor)
        self.grid.addWidget(self.update_button, 4, 0, 1, 2)
        self.update_button.setVisible(False)
        # Connect update button to slot for functionality
        self.update_button.clicked.connect(self.update_button_clicked)

        # Create CANCEL UPDATE ACCOUNT button
        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.setCursor(Qt.PointingHandCursor)
        self.grid.addWidget(self.cancel_button, 4, 3, 1, 2)
        self.cancel_button.setVisible(False)
        # Connect update button to slot for functionality
        self.cancel_button.clicked.connect(self.cancel_button_clicked)

        # Create DELETE password button
        self.delete_button = QPushButton("Delete", self)
        self.delete_button.setStyleSheet("""QPushButton { background-color:#C0C0C0; 
        }
        QPushButton:hover {
            background-color: #4e4f4e;
        }
        """)
        self.delete_button.setCursor(Qt.PointingHandCursor)
        self.grid.addWidget(self.delete_button, 2, 4)
        self.delete_button.setVisible(False)
        # Connect delete button to slot for functionality
        self.delete_button.clicked.connect(self.delete_button_clicked)

    ## -------------------------- Search accounts methods ------------------------------- ##


    @Slot()
    def go_home(self, event):
        # Navigate to the home screen and clear all inputs
        self.website_entry.clear()
        self.delete_button.setVisible(False)
        self.edit_button.setVisible(False)
        self.account_label.clear()
        parent_widget = self.parent()  # Get the parent (which is the QStackedWidget)
        parent_widget.setCurrentIndex(0)  # Set the current index to home screen (index 0)

        # Search for the specified account
    @Slot()
    def on_search_button_clicked(self):
        self.account_label.clear()
        website = self.website_entry.text()
        # Call the search function
        from main import session, search  # Import session here
        account = search(session, website)


        if not website:
            #Display error message if no website is entered
            msg = QMessageBox(self)
            msg.setWindowTitle("Review")
            msg.setText("Please enter website.")
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
            pixmap = QPixmap(get_image_path("warning.png"))  # Replace with your actual image path
            # Resize the icon by scaling the QPixmap
            scaled_pixmap = pixmap.scaled(60, 60, Qt.KeepAspectRatio,
                                          Qt.SmoothTransformation)  # Set width and height
            # Set the scaled pixmap as the icon for the QMessageBox
            msg.setIconPixmap(scaled_pixmap)
            msg.exec()
        else:
            if account:
                # Store the account details in an instance variable
                self.current_account = account
                # Update UI elements
                decrypted_password = self.decrypt_password(account.password)
                self.account_label.setText(f"<p><b>Website:</b> {account.website}</p>"
                     f"<p><b>Username:</b> {account.username}</p>"
                     f"<p><b>Password:</b> {decrypted_password}</p>"
                )
                # Make the found account label visible
                self.account_label.setVisible(True)
                self.website_entry.clear()

                # Make edit and delete password buttons visible
                self.edit_button.setVisible(True)
                self.delete_button.setVisible(True)

            else:
                # Hide the account label if no account is found
                self.account_label.setVisible(False)
                self.edit_button.setVisible(False)
                self.delete_button.setVisible(False)
                # Show error message if no account is found
                msg = QMessageBox(self)
                msg.setWindowTitle("Review")
                msg.setText("Account not found!")
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
                pixmap = QPixmap(get_image_path("warning.png"))
                # Resize the icon by scaling the QPixmap
                scaled_pixmap = pixmap.scaled(60, 60, Qt.KeepAspectRatio,
                                              Qt.SmoothTransformation)  # Set width and height
                # Set the scaled pixmap as the icon for the QMessageBox
                msg.setIconPixmap(scaled_pixmap)
                msg.exec()



    @Slot()
    def edit_button_clicked(self):
        self.clear_screen()
        self.edit_label.setVisible(True)
        self.new_website_label.setVisible(True)
        self.new_website_entry.setVisible(True)
        self.new_username_label.setVisible(True)
        self.new_username_entry.setVisible(True)
        self.new_password_label.setVisible(True)
        self.new_password_entry.setVisible(True)
        self.home_icon_label.setVisible(True)
        self.update_button.setVisible(True)
        self.cancel_button.setVisible(True)
        if self.current_account:
            website = self.current_account.website
            username = self.current_account.username
            encrypted_password = self.current_account.password
            # Decrypt the password
            decrypted_password = self.decrypt_password(encrypted_password)
            #password = self.current_account.password
            self.edit_label.setText(f"Edit {website} Account")
            self.new_website_entry.setText(f"{website}")
            self.new_username_entry.setText(f"{username}")
            self.new_password_entry.setText(f"{decrypted_password}")


    @Slot()
    def update_button_clicked(self):
        # Update account with new details
        if self.current_account:
            from main import edit_account

            new_website = self.new_website_entry.text().strip()
            new_username = self.new_username_entry.text().strip()
            new_password = self.new_password_entry.text().strip()
            encrypted_new_password = self.encrypt_password(new_password)

            # Call the edit_account function from main.py
            edit_account(
                website=self.current_account.website,
                new_website=new_website if new_website else None,
                new_username=new_username if new_username else None,
                new_password=encrypted_new_password if encrypted_new_password else None
            )
            print(f"Account updated for website: {self.current_account.website}")
            # Display success message box
            msg = QMessageBox(self)
            msg.setWindowTitle("Success")
            msg.setText(f"{new_website} account updated!")
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
            pixmap = QPixmap(get_image_path("broom.png"))
            # Resize the icon by scaling the QPixmap
            scaled_pixmap = pixmap.scaled(55, 55, Qt.KeepAspectRatio,
                                          Qt.SmoothTransformation)  # Set width and height
            # Set the scaled pixmap as the icon for the QMessageBox
            msg.setIconPixmap(scaled_pixmap)
            msg.exec()
            self.new_website_entry.clear()
            self.new_username_entry.clear()
            self.new_password_entry.clear()
            self.clear_screen()
            self.home_icon_label.setVisible(True)
            self.label.setVisible(True)
            self.website_label.setVisible(True)
            self.website_entry.setVisible(True)
            self.website_entry.clear()
            self.find_button.setVisible(True)
            self.reference_button.setVisible(True)


    @Slot()
    def cancel_button_clicked(self):
        self.new_website_entry.clear()
        self.new_username_entry.clear()
        self.new_password_entry.clear()
        self.clear_screen()
        self.label.setVisible(True)
        self.label.setText("Search PixiePass")
        self.home_icon_label.setVisible(True)
        self.website_label.setVisible(True)
        self.website_entry.setVisible(True)
        self.find_button.setVisible(True)
        self.reference_button.setVisible(True)


    @Slot()
    def delete_button_clicked(self):
        if self.current_account:
            msg = QMessageBox(self)
            msg.setWindowTitle("Confirmation")
            msg.setText("Are you sure you want to delete this account?")
            # Add Yes and Cancel buttons
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
            pixmap = QPixmap(get_image_path("warning.png"))
            # Resize the icon by scaling the QPixmap
            scaled_pixmap = pixmap.scaled(55, 55, Qt.KeepAspectRatio,
                                          Qt.SmoothTransformation)  # Set width and height
            # Set the scaled pixmap as the icon for the QMessageBox
            msg.setIconPixmap(scaled_pixmap)

            result = msg.exec()
            # Check which button was clicked
            if result == QMessageBox.Yes:
                from main import delete_account
                website = self.current_account.website
                delete_account(website)
                print("Yes clicked")

                msg = QMessageBox(self)
                msg.setWindowTitle("Delete")
                msg.setText("Account successfully deleted!")
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
                pixmap = QPixmap(get_image_path("broom.png"))
                # Resize the icon by scaling the QPixmap
                scaled_pixmap = pixmap.scaled(55, 55, Qt.KeepAspectRatio,
                                              Qt.SmoothTransformation)  # Set width and height
                # Set the scaled pixmap as the icon for the QMessageBox
                msg.setIconPixmap(scaled_pixmap)
                msg.exec()
                self.clear_screen()
                self.label.setVisible(True)
                self.home_icon_label.setVisible(True)
                self.website_label.setVisible(True)
                self.find_button.setVisible(True)
                self.website_entry.setVisible(True)
                self.reference_button.setVisible(True)

            else:
                print("Cancel clicked")

    @Slot()
    def reference_button_clicked(self, event):
        parent_widget = self.parent()  # Get the parent (which is the QStackedWidget)
        parent_widget.setCurrentIndex(3)  # Set the current index to home screen (index 0)


    @Slot()
    def clear_screen(self):
        for i in range(self.grid.count()):
            widget = self.grid.itemAt(i).widget()
            if widget:
                widget.setVisible(False)

## Encryption and Decryption

    def decrypt_password(self, encrypted_password):
        #Decrypt the password with Fernet
        try:
            # Decrypt the password
            return cipher.decrypt(encrypted_password.encode()).decode()
        except Exception as e:
            print(f"Error decrypting password: {e}")
            return "Decryption Error"

    def encrypt_password(self, password):
        #Encrypt the password using Fernet
        try:
            return cipher.encrypt(password.encode()).decode()
        except Exception as e:
            print(f"Error encrypting password: {e}")
            return None