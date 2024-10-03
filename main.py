## -------------------------- IMPORTS ------------------------------- ##
import os
import sys

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                               QStackedWidget, QLabel)
from sqlalchemy import Integer, String, create_engine, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from account_list import AccountList
from add_password import AddPassword
from home_screen import HomeScreen
from search_password import SearchPassword
from utils import get_base_path
from PySide6.QtCore import QThread, Signal
import time
## -------------------------- Asynchronous loading test ------------------------------- ##







#-----------------------------------TESTING ABOVE ---------------------------------------#

## -------------------------- DATABASE CREATION using relative paths for packaging ------------------------------- ##

def get_base_path():
    if getattr(sys, 'frozen', False):  # If running as a PyInstaller bundle
        return sys._MEIPASS
    else:
        return os.path.abspath(".")

# Base class for declarative model
class Base(DeclarativeBase):
    pass

# Table creation
class Account(Base):
    __tablename__ = 'accounts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    website: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    password: Mapped[str] = mapped_column(String(50), nullable=False)

# Path to the database file (updated to use relative path)
db_path = os.path.join(get_base_path(), 'instance', 'accounts.db')

# Check if the database file exists
if not os.path.exists(db_path):
    # If the file doesn't exist, create the engine and the tables
    engine = create_engine(f'sqlite:///{db_path}', echo=True)
    Base.metadata.create_all(engine)  # Create tables
else:
    # If the file exists, just create the engine
    engine = create_engine(f'sqlite:///{db_path}', echo=True)

# Bind session to the database
Session = sessionmaker(bind=engine)
session = Session()  # Create an active session






## -------------------------- MAIN WINDOW (Q-WIDGET) THAT PARENTS ALL SCREENS IN PROGRAM ------------------------------- ##

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PixiePass")
        self.setFixedSize(500, 500)

        # Create QStackedWidget to manage different screens
        self.stack_widget = QStackedWidget()

        # Initialize the home screen, add password, search password, and account list screens
        self.home_screen = HomeScreen(self.stack_widget)
        self.add_password = AddPassword(self.stack_widget)
        self.search_password = SearchPassword(self.stack_widget)
        self.account_list = AccountList(self.stack_widget)

        # Add all screens to the widget stack
        self.stack_widget.addWidget(self.home_screen)  # index 0
        self.stack_widget.addWidget(self.add_password)  # index 1
        self.stack_widget.addWidget(self.search_password) # index 2
        self.stack_widget.addWidget(self.account_list) # index 3

        # Set the initial screen to the home screen
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.stack_widget)
        self.stack_widget.setCurrentIndex(0)  # Show the home screen by default


#### -------------------Applying CSS with relative path for packing with Pyinstaller ------------##

        def get_base_path():
            if getattr(sys, 'frozen', False):  # If running as a PyInstaller bundle
                return sys._MEIPASS
            else:
                return os.path.abspath(".")

        def get_styles_path():
            return os.path.join(get_base_path(), 'styles.css')

        # Load external stylesheet
        with open(get_styles_path(), "r") as f:
            stylesheet = f.read()

        app.setStyleSheet(stylesheet)  # Apply stylesheet to entire application
 ## -------------- Relative path for images found in assets folder for PyInstaller bundle ----------##

def get_image_path(image_name):
    return os.path.join(get_base_path(), 'assets', image_name)



## -------------------------- DATABASE FUNCTIONS ------------------------------- ##

### Add a new account to the database ###
def add_account(website, username, password):
    new_account = Account(website=website, username=username, password=password)
    session.add(new_account)
    session.commit()


### Check if account is already stored in the database/ ** use func to make website case INSENSITIVE for efficient searching
def find_duplicate(website):
    account = session.query(Account).filter(func.lower(Account.website) == func.lower(website)).first()
    if account:
        print(f"Account with website '{website}' exists.")
        return True
    else:
        print(f"No account found with website '{website}'.")
        return False

### Search for existing account details/ **use ilike to make website case INSENSITIVE ###
def search(session, website):
    return session.query(Account).filter(Account.website.ilike(website)).first()


### Edit an existing account ###
def edit_account(website, new_website=None, new_username=None, new_password=None):
    # Find the account by website (or you can use other criteria, like username)
    account = session.query(Account).filter_by(website=website).first()

    if account:
        # Update the fields if new values are provided
        if new_website:
            account.website = new_website
        if new_username:
            account.username = new_username
        if new_password:
            account.password = new_password

        # Commit the changes to the database
        session.commit()
        return True #if update is successful
    else:
        return False #if not successful


### Delete an existing account ###
def delete_account(website):
    # Query for account based on website
    account_to_delete = session.query(Account).filter_by(website=website).first()
    if account_to_delete:
        # If the account is found, delete it
        session.delete(account_to_delete)
        session.commit()
    else:
        print("No account found.")









if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.setWindowTitle("PixiePass")
    window.show()

    sys.exit(app.exec())