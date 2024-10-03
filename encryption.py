import os
import sys
from cryptography.fernet import Fernet

# Function to get the base path, depending on whether the app is bundled or not
def get_base_path():
    if getattr(sys, 'frozen', False):  # If running as a PyInstaller bundle
        return sys._MEIPASS
    else:
        return os.path.abspath(".")

# Path to store the Fernet key (now using relative path)
key_file = os.path.join(get_base_path(), 'instance', 'fernet_key.key')

def load_or_generate_key():
    # Check if the key file exists
    if not os.path.exists(key_file):
        # If it does not exist, generate a new key
        key = Fernet.generate_key()
        # Ensure the directory exists
        os.makedirs(os.path.dirname(key_file), exist_ok=True)
        # Save key to a file
        with open(key_file, 'wb') as file:
            file.write(key)
        print("New Fernet key created and saved.")
    else:
        # If the file exists, load the key from the file
        with open(key_file, 'rb') as file:
            key = file.read()
        print("Fernet key found and loaded from file")
    return key





# Load or generate the key
fernet_key = load_or_generate_key()

# Create the Fernet cipher with the key
cipher = Fernet(fernet_key)
