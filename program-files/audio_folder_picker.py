import sys
from PyQt5.QtWidgets import (QApplication, QDialog, QFileDialog, QVBoxLayout, 
                            QHBoxLayout, QLineEdit, QPushButton, QLabel)
from PyQt5.QtCore import Qt

class FolderPickerDialog(QDialog):
    def __init__(self, parent=None, cached_data=None):
        super().__init__(parent)
        self.selected_folder = ""
        self.cached_data = cached_data
        self.init_ui()
        
        # Apply cached data if available
        if self.cached_data and "selected_folder" in self.cached_data:
            self.folder_path.setText(self.cached_data["selected_folder"])
            self.selected_folder = self.cached_data["selected_folder"]
        
    def init_ui(self):
        # Set window title and size
        self.setWindowTitle("Select Folder")
        self.resize(500, 100)
        
        # Create main layout
        main_layout = QVBoxLayout()
        
        # Create folder selection layout
        folder_layout = QHBoxLayout()
        
        # Add label
        folder_label = QLabel("Folder Path:")
        folder_layout.addWidget(folder_label)
        
        # Add text field for folder path
        self.folder_path = QLineEdit()
        folder_layout.addWidget(self.folder_path)
        
        # Add browse button
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_folder)
        folder_layout.addWidget(browse_button)
        
        # Add folder selection layout to main layout
        main_layout.addLayout(folder_layout)
        
        # Add OK button
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        main_layout.addWidget(ok_button, alignment=Qt.AlignRight)
        
        # Set dialog layout
        self.setLayout(main_layout)
    
    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folder_path.setText(folder)
            self.selected_folder = folder
    
    def get_selected_folder(self):
        # Return the path from the text field (in case user typed it manually)
        return self.folder_path.text() or self.selected_folder

# Example usage
if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = FolderPickerDialog()
    
    if dialog.exec_() == QDialog.Accepted:
        selected_folder = dialog.get_selected_folder()
        print(f"Selected folder: {selected_folder}")
    else:
        print("No folder selected")

