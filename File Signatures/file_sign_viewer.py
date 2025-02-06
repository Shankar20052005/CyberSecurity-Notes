import sys
import binascii
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QFileDialog, QDesktopWidget

class FileSignatureApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("File Signature Viewer")
        self.setGeometry(100, 100, 400, 200)
        self.center_window()  # Center the window on the screen

        self.label = QLabel("Select a file to view its signature", self)
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

    def get_file_signature(self):
        """Opens a file dialog centered on the screen and displays the file signature"""
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog  # Ensures it works well on WSL
        file_dialog = QFileDialog(self)
        file_dialog.setOptions(options)
        file_dialog.setWindowTitle("Select File")
        file_dialog.setGeometry(self.geometry())  # Opens near the main window

        file_path, _ = file_dialog.getOpenFileName(self, "Select File")
        if file_path:
            with open(file_path, "rb") as f:
                signature = binascii.hexlify(f.read(8)).decode().upper()
            self.label.setText(f"File Signature: {signature}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileSignatureApp()
    window.show()
    sys.exit(app.exec_())

