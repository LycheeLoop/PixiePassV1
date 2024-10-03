import os
import sys


## ----------------------------- Relative paths for account database and images -------------------##

def get_base_path():
    if getattr(sys, 'frozen', False):  # If running as a PyInstaller bundle
        return sys._MEIPASS
    else:
        return os.path.abspath(".")



def get_image_path(image_name):
    return os.path.join(get_base_path(), 'assets', image_name)
