from PyQt5.QtWidgets import (QDialog, QWidget, QVBoxLayout, QHBoxLayout,
                            QPushButton, QLabel, QFrame)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QPixmap
from darken_preview import DarkenPreview
from image_preview import ImagePreview
import os

class ImageSelector(QDialog):
    # Signal to emit the data when OK is clicked
    dataReady = pyqtSignal(dict)
    
    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Image Selector")
        self.setMinimumSize(900, 600)  # Set a reasonable minimum size
        self.current_image_path = image_path
        self.initUI()
        
        # Set the initial image after UI is initialized
        if self.current_image_path:
            if self.set_image(self.current_image_path):
                # self.image_path_label.setText(f"Current image: {self.current_image_path.split('/')[-1]}")
                self.ok_button.setEnabled(True)
            else:
                # self.image_path_label.setText("Failed to load image")
                self.ok_button.setEnabled(False)
        
    def initUI(self):
        # Create main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Create two-column layout
        columns_layout = QHBoxLayout()
        
        # Left column (Image Preview)
        left_column = QFrame()
        left_column.setFrameStyle(QFrame.StyledPanel)
        left_column.setStyleSheet("""
            QFrame {
                background-color: #f8f8f8;
                border: 1px solid #ddd;
                border-radius: 8px;
            }
        """)
        left_layout = QVBoxLayout(left_column)
        
        # Add Image Preview
        preview_label = QLabel("Image Preview")
        preview_label.setFont(QFont("Arial", 12, QFont.Bold))
        left_layout.addWidget(preview_label)
        
        self.image_preview = ImagePreview()
        left_layout.addWidget(self.image_preview)
        left_layout.addStretch()
        
        # Right column (Darken Preview)
        right_column = QFrame()
        right_column.setFrameStyle(QFrame.StyledPanel)
        right_column.setStyleSheet("""
            QFrame {
                background-color: #f8f8f8;
                border: 1px solid #ddd;
                border-radius: 8px;
            }
        """)
        right_layout = QVBoxLayout(right_column)
        
        # Add Darken Preview
        darken_label = QLabel("Darken Preview")
        darken_label.setFont(QFont("Arial", 12, QFont.Bold))
        right_layout.addWidget(darken_label)
        
        self.darken_preview = DarkenPreview()
        right_layout.addWidget(self.darken_preview)
        right_layout.addStretch()
        
        # Add columns to layout
        columns_layout.addWidget(left_column)
        columns_layout.addWidget(right_column)
        
        # Add columns layout to main layout
        main_layout.addLayout(columns_layout)
        
        # Create button layout
        button_layout = QHBoxLayout()
        
        # Reset button
        self.reset_button = QPushButton("Reset")
        self.reset_button.setFixedSize(100, 35)
        self.reset_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
            QPushButton:pressed {
                background-color: #b71c1c;
            }
        """)
        
        # OK button
        self.ok_button = QPushButton("OK")
        self.ok_button.setFixedSize(100, 35)
        self.ok_button.setEnabled(False)  # Disabled until image loads successfully
        self.ok_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        
        button_layout.addWidget(self.reset_button)
        button_layout.addStretch()
        button_layout.addWidget(self.ok_button)
        
        # Add button layout to main layout
        main_layout.addLayout(button_layout)
        
        # Connect signals
        self.reset_button.clicked.connect(self.reset_all)
        self.ok_button.clicked.connect(self.on_ok_clicked)
    
    def set_image(self, image_path):
        """Set the image for both previews"""
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            self.image_preview.set_image(pixmap)
            self.darken_preview.set_image(pixmap)
            return True
        return False
    
    def reset_all(self):
        """Reset all components to their initial values"""
        # Reset image preview to "Do Nothing" option
        nothing_radio = [btn for btn in self.image_preview.button_group.buttons() 
                        if btn.text() == "Do Nothing (selected by default)"][0]
        nothing_radio.setChecked(True)
        
        # Reset darken preview to 75%
        seventy_five_radio = [btn for btn in self.darken_preview.button_group.buttons() 
                            if "75%" in btn.text()][0]
        seventy_five_radio.setChecked(True)
    
    def get_all_data(self):
        """Collect and return all the current settings"""
        data = {
            'image_path': self.current_image_path,
            'aspect_ratio_option': self.image_preview.current_option,
            'darkness_level': self.darken_preview.current_darkness
        }
        return data
    
    def on_ok_clicked(self):
        """Handle OK button click"""
        # Get the data
        data = self.get_all_data()
        # Emit the data
        self.dataReady.emit(data)
        # Accept the dialog (equivalent to returning QDialog.Accepted)
        self.accept()
    
    def get_result(self):
        """Return the data when dialog is accepted"""
        return self.get_all_data()

# Example usage
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    
    # Get the absolute path to the image
    current_dir = os.path.dirname(os.path.abspath(__file__))
    test_image_path = os.path.join(current_dir, "test_image.jpg")  # Replace with your actual image name
    
    app = QApplication(sys.argv)
    
    # Make sure the image exists before creating the window
    if os.path.exists(test_image_path):
        window = ImageSelector(test_image_path)
        
        def handle_data(data):
            print("Image Path:", data['image_path'])
            print("Aspect Ratio Option:", data['aspect_ratio_option'])
            print("Darkness Level:", data['darkness_level'])
        
        window.dataReady.connect(handle_data)
        window.show()
        sys.exit(app.exec_())
    else:
        print(f"Error: Image not found at {test_image_path}")
        sys.exit(1) 