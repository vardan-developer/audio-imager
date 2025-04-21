from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QRadioButton, QButtonGroup, QFrame)
from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5.QtGui import QPixmap, QPainter

class ImagePreview(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.current_option = "do_nothing"
        self.preview_size = QSize(200, 200)  # Small preview size
        self.final_size = QSize(800, 800)    # Final target size
        self.original_pixmap = None  # Store the original pixmap
        
    def initUI(self):
        layout = QHBoxLayout()
        
        # Preview Area
        self.preview_frame = QFrame()
        self.preview_frame.setFrameStyle(QFrame.Box | QFrame.Plain)
        self.preview_frame.setFixedSize(200, 200)  # Small preview size
        self.preview_frame.setStyleSheet("QFrame { background-color: white; }")
        
        self.preview_label = QLabel(self.preview_frame)
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setText("Image preview area\n800x800")
        self.preview_label.setStyleSheet("QLabel { color: gray; }")
        self.preview_label.setFixedSize(200, 200)
        
        # Options Area
        options_layout = QVBoxLayout()
        options_widget = QWidget()
        options_widget.setLayout(options_layout)
        
        options_label = QLabel("Image options for selected file")
        options_layout.addWidget(options_label)
        
        # Radio Buttons
        self.button_group = QButtonGroup()
        
        crop_radio = QRadioButton("Crop to AR")
        stretch_radio = QRadioButton("Stretch to AR")
        nothing_radio = QRadioButton("Do Nothing (selected by default)")
        nothing_radio.setChecked(True)
        
        self.button_group.addButton(crop_radio)
        self.button_group.addButton(stretch_radio)
        self.button_group.addButton(nothing_radio)
        
        options_layout.addWidget(crop_radio)
        options_layout.addWidget(stretch_radio)
        options_layout.addWidget(nothing_radio)
        options_layout.addStretch()
        
        # Connect radio buttons
        crop_radio.toggled.connect(lambda checked: checked and self.option_changed("crop"))
        stretch_radio.toggled.connect(lambda checked: checked and self.option_changed("stretch"))
        nothing_radio.toggled.connect(lambda checked: checked and self.option_changed("do_nothing"))
        
        # Add widgets to main layout
        layout.addWidget(self.preview_frame)
        layout.addWidget(options_widget)
        layout.addStretch()
        
        self.setLayout(layout)
        
    def option_changed(self, option):
        self.current_option = option
        if self.original_pixmap:
            self.update_preview()
        
    def update_preview(self):
        if not self.original_pixmap:
            return
            
        preview_pixmap = QPixmap(self.preview_size)
        preview_pixmap.fill(Qt.white)
        
        painter = QPainter(preview_pixmap)
        
        if self.current_option == "crop":
            # Calculate the crop dimensions to maintain aspect ratio
            src_ratio = self.original_pixmap.width() / self.original_pixmap.height()
            target_ratio = self.preview_size.width() / self.preview_size.height()
            
            if src_ratio > target_ratio:
                # Image is wider than target, crop width
                new_width = int(self.original_pixmap.height() * target_ratio)
                x_offset = (self.original_pixmap.width() - new_width) // 2
                crop_rect = QRect(x_offset, 0, new_width, self.original_pixmap.height())
            else:
                # Image is taller than target, crop height
                new_height = int(self.original_pixmap.width() / target_ratio)
                y_offset = (self.original_pixmap.height() - new_height) // 2
                crop_rect = QRect(0, y_offset, self.original_pixmap.width(), new_height)
            
            cropped = self.original_pixmap.copy(crop_rect)
            scaled_pixmap = cropped.scaled(self.preview_size, 
                                         Qt.KeepAspectRatio,
                                         Qt.SmoothTransformation)
        elif self.current_option == "stretch":
            # Stretch to fill the preview area
            scaled_pixmap = self.original_pixmap.scaled(self.preview_size,
                                                      Qt.IgnoreAspectRatio,
                                                      Qt.SmoothTransformation)
        else:  # do_nothing
            # Keep original aspect ratio
            scaled_pixmap = self.original_pixmap.scaled(self.preview_size,
                                                      Qt.KeepAspectRatio,
                                                      Qt.SmoothTransformation)
            
        # Center the image in preview area
        x = (self.preview_size.width() - scaled_pixmap.width()) // 2
        y = (self.preview_size.height() - scaled_pixmap.height()) // 2
        painter.drawPixmap(x, y, scaled_pixmap)
        painter.end()
        
        self.preview_label.setPixmap(preview_pixmap)
        
    def set_image(self, pixmap):
        if pixmap is None:
            return
            
        self.original_pixmap = pixmap
        self.update_preview() 