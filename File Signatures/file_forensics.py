import sys
import binascii
import string
import os
import time
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QFileDialog, QDesktopWidget
)
from PyQt5.QtGui import QPalette, QColor

# Dictionary of common file signatures
FILE_SIGNATURES = {
    "FFD8FF": "JPEG Image",
    "89504E47": "PNG Image",
    "47494638": "GIF Image",
    "25504446": "PDF Document",
    "504B0304": "ZIP Archive / DOCX / XLSX",
    "4D5A": "Windows Executable (EXE)",
    "7F454C46": "Linux Executable (ELF)",
    "52617221": "RAR Archive",
    "1F8B08": "GZIP Archive",
    "0000001C66747970": "MP4 Video",
    "494433": "MP3 Audio",
    "000001BA": "MPEG Video",
    "000001B3": "MPEG Video",
    "3C3F786D6C": "XML File",
    "7B226E616D6522": "JSON File",
    "EFBBBF": "UTF-8 TXT File",
    "FFFE": "UTF-16 TXT File (Little Endian)",
    "FEFF": "UTF-16 TXT File (Big Endian)",
    "504B030414000600": "DOCX / XLSX (Office Open XML)",
    "2321": "Script File (#! Interpreter)",
    "7573746172003030": "TAR Archive",
    "4344303031": "ISO Disk Image",
}

class FileSignatureApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("File Signature Viewer")
        self.setGeometry(100, 100, 500, 350)
        self.center_window()
        self.apply_dark_mode()  # Enable dark theme

        self.label = QLabel("Select a file to view its signature and metadata", self)
        self.button = QPushButton("Choose File", self)
        self.button.clicked.connect(self.get_file_signature)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def center_window(self):
        """Centers the main window on the screen"""
        screen_geometry = QDesktopWidget().screenGeometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())

    def apply_dark_mode(self):
        """Applies a dark theme to the GUI"""
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(45, 45, 45))
        dark_palette.setColor(QPalette.WindowText, QColor(220, 220, 220))
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(45, 45, 45))
        dark_palette.setColor(QPalette.ToolTipBase, QColor(220, 220, 220))
        dark_palette.setColor(QPalette.ToolTipText, QColor(220, 220, 220))
        dark_palette.setColor(QPalette.Text, QColor(220, 220, 220))
        dark_palette.setColor(QPalette.Button, QColor(70, 70, 70))
        dark_palette.setColor(QPalette.ButtonText, QColor(220, 220, 220))
        dark_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        dark_palette.setColor(QPalette.Highlight, QColor(38, 79, 120))
        dark_palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        QApplication.instance().setPalette(dark_palette)

    def format_hex(self, byte_string):
        """Formats hex string into spaced 2-byte groups (like a hex editor)"""
        return " ".join(byte_string[i:i+2] for i in range(0, len(byte_string), 2))

    def detect_file_type(self, signature, file_path):
        """Detects the file type based on known signatures or checks if it's a text file."""
        for sig, file_type in FILE_SIGNATURES.items():
            if signature.startswith(sig):
                return file_type

        # Check if the file is likely a plain text file
        try:
            with open(file_path, "rb") as f:
                content = f.read(256)  # Read the first 256 bytes
                if all(chr(b) in string.printable for b in content):
                    return "Plain Text File (TXT)"
        except:
            pass

        return "Unknown File Type"

    def get_file_metadata(self, file_path):
        """Retrieves file metadata with better error handling"""
        try:
            file_size = os.path.getsize(file_path)  # File size in bytes
            last_modified = time.ctime(os.path.getmtime(file_path))  # Last modified time
            created_time = None

            if os.name == "nt":  # Windows: get created time
                created_time = time.ctime(os.path.getctime(file_path))
            else:  # Linux/macOS: use modified time as an approximation
                created_time = last_modified

            return file_size, last_modified, created_time
        except Exception as e:
            return "N/A", "N/A", "N/A"

    def get_file_signature(self):
        """Opens a file dialog, reads the first 16 bytes, and detects the file type"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File")
        if file_path:
            file_size, last_modified, created_time = self.get_file_metadata(file_path)

            try:
                with open(file_path, "rb") as f:
                    raw_bytes = binascii.hexlify(f.read(16)).decode().upper()
                    formatted_signature = self.format_hex(raw_bytes)
                    file_type = self.detect_file_type(raw_bytes, file_path)
            except Exception as e:
                self.label.setText(f"Error reading file: {str(e)}")
                return

            file_name = os.path.basename(file_path)

            self.label.setText(
                f"File: {file_name}\n"
                f"Size: {file_size} bytes\n"
                f"Created: {created_time}\n"
                f"Last Modified: {last_modified}\n"
                f"File Signature: {formatted_signature}\n"
                f"Detected Type: {file_type}"
            )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileSignatureApp()
    window.show()
    sys.exit(app.exec_())

