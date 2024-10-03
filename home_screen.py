## -------------------------- IMPORTS ------------------------------- ##
from PySide6.QtWidgets import QApplication, QPushButton, QLabel, QWidget, QGridLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from utils import get_image_path



## -------------------------- INITIAL HOME SCREEN (Q-WIDGET) ------------------------------- ##
class HomeScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("PixiePass")
        self.resize(500, 500)

        # Create grid layout
        grid = QGridLayout(self)
        grid.setVerticalSpacing(10)
        grid.setHorizontalSpacing(10)
        # Create a QLabel to display the home screen image
        image_label = QLabel(self)
        pixmap = QPixmap(get_image_path("pixiehome.png"))  # Use the function to get the image path
        image_label.setPixmap(pixmap)
        # Add image QLabel image to the grid layout
        grid.addWidget(image_label, 0, 0, 1, 2, Qt.AlignCenter)  # Adjust position and span as needed
        # Create home screen buttons
        search_button = QPushButton("  Search 🔎", self)
        search_button.setCursor(Qt.PointingHandCursor)
        add_button = QPushButton("Add Password", self)
        add_button.setCursor(Qt.PointingHandCursor)
        # Add buttons to grid layout and set stretch factors
        grid.addWidget(search_button, 1, 0)
        grid.addWidget(add_button, 1, 1)
        # Use layout stretch to ensure all buttons expand to equal width
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        # Connect buttons to its functions
        add_button.clicked.connect(lambda: parent.setCurrentIndex(1))  # Switch to form
        search_button.clicked.connect(lambda: parent.setCurrentIndex(2))

        # Set layout for the window
        self.setLayout(grid)
