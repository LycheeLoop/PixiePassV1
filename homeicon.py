from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, Slot
from utils import get_image_path


## -------------------------- HOME ICON (Q-LABEL) ------------------------------- ##
class HomeIcon(QLabel):
    def __init__(self, parent=None, callback=None):
        super().__init__(parent)

        # Set the icon as clickable
        self.setCursor(Qt.PointingHandCursor)

        # Load your .png file
        pixmap = QPixmap(get_image_path("mushroomhome.png"))

        # Resize the image
        scaled_pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # Set the scaled pixmap on the QLabel
        self.setPixmap(scaled_pixmap)

        # Connect the icon click to the callback
        self.mousePressEvent = callback if callback else self.go_home

    @Slot()
    def go_home(self, event):
        # Default behavior: navigate to home if no custom callback is provided
        parent_widget = self.parent()  # Get the parent (QStackedWidget)
        parent_widget.setCurrentIndex(0)  # Set to the home screen index
