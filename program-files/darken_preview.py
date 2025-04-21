from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QRadioButton, QButtonGroup, QPushButton)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QPainter, QColor

class DarkenPreview(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.current_darkness = 0.75  # 75% by default
        self.preview_size = QSize(200, 200)
        self.original_pixmap = None
        
    def initUI(self):
        layout = QVBoxLayout()
        
        # Preview Area (similar to ImagePreview)
        self.preview_label = QLabel()
        self.preview_label.setFixedSize(200, 200)
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setText("Darkened preview\n800x800")
        self.preview_label.setStyleSheet("""
            QLabel {
                color: gray;
                border: 1px solid #ccc;
                background-color: white;
            }
        """)
        
        # Options Area
        options_layout = QVBoxLayout()
        
        title_label = QLabel("Darken background image")
        options_layout.addWidget(title_label)
        
        # Radio Buttons for darkness levels
        self.button_group = QButtonGroup()
        
        # Create radio buttons with different darkness levels
        darkness_levels = [
            ("75% (selected by default)", 0.75),
            ("65%", 0.65),
            ("50%", 0.50),
            ("25%", 0.25)
        ]
        
        for label, value in darkness_levels:
            radio = QRadioButton(label)
            if value == 0.75:  # Default option
                radio.setChecked(True)
            self.button_group.addButton(radio)
            options_layout.addWidget(radio)
            radio.toggled.connect(lambda checked, v=value: checked and self.darkness_changed(v))
        
        # Next button
       
        
        # Add all widgets to main layout
        layout.addWidget(self.preview_label)
        layout.addLayout(options_layout)
        # layout.addWidget(next_button, alignment=Qt.AlignRight)
        layout.addStretch()
        
        self.setLayout(layout)
        
    def darkness_changed(self, value):
        self.current_darkness = value
        self.update_preview()
        
    def update_preview(self):
        if not self.original_pixmap:
            return
            
        # Create a new pixmap for the preview
        preview_pixmap = QPixmap(self.preview_size)
        preview_pixmap.fill(Qt.white)
        
        # Scale the original image to fit the preview
        scaled_pixmap = self.original_pixmap.scaled(
            self.preview_size,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        
        # Create painter and draw the darkened image
        painter = QPainter(preview_pixmap)
        
        # Draw the scaled image
        x = (self.preview_size.width() - scaled_pixmap.width()) // 2
        y = (self.preview_size.height() - scaled_pixmap.height()) // 2
        painter.drawPixmap(x, y, scaled_pixmap)
        
        # Apply darkening effect
        darkness = int(255 * (1 - self.current_darkness))  # Convert percentage to alpha
        painter.fillRect(
            0, 0, 
            self.preview_size.width(), 
            self.preview_size.height(),
            QColor(0, 0, 0, 255 - darkness)  # Black with alpha
        )
        
        painter.end()
        self.preview_label.setPixmap(preview_pixmap)
        
    def set_image(self, pixmap):
        if pixmap is None:
            return
            
        self.original_pixmap = pixmap
        self.update_preview() 