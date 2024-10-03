## -------------------------- IMPORTS ------------------------------- ##
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QLineEdit, QPushButton, QGridLayout, QMessageBox, QDialogButtonBox
from sqlalchemy.orm import sessionmaker
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, Slot, QSize
from homeicon import HomeIcon
from utils import get_image_path



## -------------------------- ACCOUNT LIST SCREEN (Q-WIDGET) ------------------------------- ##
class AccountList(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)


        # Create grid layout
        self.grid = QGridLayout(self)

        # Add the home icon to the layout
        self.home_icon_label = HomeIcon(self, self.go_home)
        self.grid.addWidget(self.home_icon_label, 0, 4, Qt.AlignTop | Qt.AlignRight)


        # Create TITLE LABEL of screen (add password)
        self.label = QLabel("Saved Passwords", self)
        self.label.setAlignment(Qt.AlignTop)
        self.label.setStyleSheet("font-size: 18px; font-weight: bold; font-family: Arial; ")
        self.grid.addWidget(self.label, 0, 0, 1, 2)

        # Create 'back' password button
        self.back_button = QPushButton("Back to Search 🔎", self)
        self.back_button.setCursor(Qt.PointingHandCursor)
        # Add button to grid layout and set stretch factors
        self.grid.addWidget(self.back_button, 3, 1, 1, 3)
        # Connect add button to slot for functionality
        self.back_button.clicked.connect(self.back_button_clicked)

        #Create refresh button
        self.refresh_icon_label = ClickableLabel(self)
        self.refresh_icon_label.setCursor(Qt.PointingHandCursor)
       #Load the PNG image for refresh icon
        pixmap = QPixmap(get_image_path("refreshgo.png"))  # Path to your .png file
        scaled_pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # Set the pixmap to the label and resize the QLabel to match the pixmap size
        self.refresh_icon_label.setPixmap(scaled_pixmap)
        self.refresh_icon_label.setFixedSize(scaled_pixmap.size())  # Make QLabel size equal to image size
        # Set the pixmap to the label
        self.refresh_icon_label.setPixmap(scaled_pixmap)
        # Add the refresh icon to the grid layout
        self.grid.addWidget(self.refresh_icon_label, 2, 2, 1, 1)

        # Create QListWidget for displaying accounts
        self.list_widget = QListWidget()
        # Add QListWidget to the layout
        self.grid.addWidget(self.list_widget, 1, 0, 1, 5)
        # Initially populate the list widget with data
        self.populate_list_widget()

    ## -------------------------- Account list methods TEST!!!! ------------------------------- ##



    ## -------------------------- Account list methods ------------------------------- ##

    def populate_list_widget(self):
        from main import Account, engine  # Fetch all accounts from the database and add to list
        Session = sessionmaker(bind=engine)
        session = Session()

        websites = self.get_all_websites(session)
        self.list_widget.clear() #Clear existing items before refreshing
        for website in websites:
            self.list_widget.addItem(website)


    #Method for fetching all saved accounts in database
    def get_all_websites(self, session):
        from main import Account
        accounts = session.query(Account).all()
        websites = [account.website for account in accounts]
        return websites

    @Slot()
    def back_button_clicked(self):
        # Navigate back to search screen
        parent_widget = self.parent()  # Get the parent (which is the QStackedWidget)
        parent_widget.setCurrentIndex(2)  # Set the current index to home screen (index 0)

    @Slot()
    def go_home(self, event):
        # Navigate to the home screen
        parent_widget = self.parent()  # Get the parent (which is the QStackedWidget)
        parent_widget.setCurrentIndex(0)  # Set the current index to home screen (index 0)


    @Slot()
    def refresh_list(self):
        self.populate_list_widget() # Repopulate the cleared list


# Create a subclass of QLabel to handle mouse press events
class ClickableLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)

    # Override the mousePressEvent method
    def mousePressEvent(self, event):
        self.parent().refresh_list()  # Call the refresh method from the parent widget
