import sys
from PyQt5.QtWidgets import (QApplication, QDialog, QFileDialog, QVBoxLayout, 
                            QHBoxLayout, QLineEdit, QPushButton, QLabel)
from PyQt5.QtCore import Qt

class ImagePickerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_image = ""
        self.init_ui()
        
    def init_ui(self):
        # Set window title and size
        self.setWindowTitle("Select Image")
        self.resize(500, 100)
        
        # Create main layout
        main_layout = QVBoxLayout()
        
        # Create image selection layout
        image_layout = QHBoxLayout()
        
        # Add label
        image_label = QLabel("Image Path:")
        image_layout.addWidget(image_label)
        
        # Add text field for image path
        self.image_path = QLineEdit()
        image_layout.addWidget(self.image_path)
        
        # Add browse button
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_image)
        image_layout.addWidget(browse_button)
        
        # Add image selection layout to main layout
        main_layout.addLayout(image_layout)
        
        # Add OK button
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        main_layout.addWidget(ok_button, alignment=Qt.AlignRight)
        
        # Set dialog layout
        self.setLayout(main_layout)
    
    def browse_image(self):
        # Define image file types for the filter
        image_filter = "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.tiff);;All Files (*)"
        
        # Open file dialog to select an image
        image_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Select Image", 
            "", 
            image_filter
        )
        
        if image_path:
            self.image_path.setText(image_path)
            self.selected_image = image_path
    
    def get_selected_image(self):
        # Return the path from the text field (in case user typed it manually)
        return self.image_path.text() or self.selected_image

# Example usage
if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = ImagePickerDialog()
    
    if dialog.exec_() == QDialog.Accepted:
        selected_image = dialog.get_selected_image()
        print(f"Selected image: {selected_image}")
    else:
        print("No image selected")
