from PyQt5.QtWidgets import (QDialog, QWidget, QVBoxLayout, QHBoxLayout,
                            QPushButton, QLabel, QFrame, QCheckBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor
from ColorPicker import ColorPicker
from font_style_selector import FontStyleSelector
import random

class BottomBarFormatter(QDialog):
    # Signal to emit the data when OK is clicked
    dataReady = pyqtSignal(dict)
    
    def __init__(self, parent=None, cached_data=None):
        super().__init__(parent)
        self.setWindowTitle("Bottom Bar Formatter")
        self.setMinimumSize(900, 700)  # Set a reasonable minimum size
        self.cached_data = cached_data
        self.initUI()
        
    def initUI(self):
        # Create main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Create container for components
        components_frame = QFrame()
        components_frame.setFrameStyle(QFrame.StyledPanel)
        components_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f8f8;
                border: 1px solid #ddd;
                border-radius: 8px;
            }
        """)
        components_layout = QVBoxLayout(components_frame)
        components_layout.setSpacing(20)
        
        # Add Font Style Selector
        font_label = QLabel("Font Style")
        font_label.setFont(QFont("Arial", 12, QFont.Bold))
        components_layout.addWidget(font_label)
        
        self.font_selector = FontStyleSelector(cached_data=self.cached_data)
        components_layout.addWidget(self.font_selector)
        
        # Add separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("QFrame { border: 1px solid #ddd; }")
        components_layout.addWidget(separator)
        
        # Add Color Picker
        color_label = QLabel("Color Selection")
        color_label.setFont(QFont("Arial", 12, QFont.Bold))
        components_layout.addWidget(color_label)
        
        # Add random color checkbox
        self.random_color_checkbox = QCheckBox("Use Random Color")
        self.random_color_checkbox.setStyleSheet("""
            QCheckBox {
                font-size: 14px;
                padding: 8px 0px;
            }
        """)
        components_layout.addWidget(self.random_color_checkbox)
        
        self.color_picker = ColorPicker(cached_data=self.cached_data)
        components_layout.addWidget(self.color_picker)
        
        # Add the components frame to main layout
        main_layout.addWidget(components_frame)
        
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
        """)
        
        button_layout.addWidget(self.reset_button)
        button_layout.addStretch()
        button_layout.addWidget(self.ok_button)
        
        # Add button layout to main layout
        main_layout.addLayout(button_layout)
        
        # Connect signals
        self.reset_button.clicked.connect(self.reset_all)
        self.ok_button.clicked.connect(self.on_ok_clicked)
        
        # Store initial values for reset
        self.initial_color = QColor("#FF0000")  # Default red color
        self.initial_font = self.font_selector.get_current_font()
        
        # Apply cached settings
        if self.cached_data:
            self.apply_cached_settings()
    
    def apply_cached_settings(self):
        """Apply cached settings to UI elements"""
        if not self.cached_data:
            return
        
        print(f"Applying cached settings to BottomBarFormatter: {self.cached_data}")    
        # Set random color checkbox if available
        if "random_color" in self.cached_data:
            self.random_color_checkbox.setChecked(self.cached_data["random_color"])
            
        # Set color if available and not using random color
        if "color" in self.cached_data and not self.random_color_checkbox.isChecked():
            try:
                color = QColor(self.cached_data["color"])
                if color.isValid():
                    self.color_picker.onColorSelected(color)
                    print(f"Set color to {color.name()}")
            except Exception as e:
                print(f"Error setting color: {e}")
            
        # Set font settings if available
        if "font_family" in self.cached_data:
            # Find the family in the combobox and select it
            index = self.font_selector.family_combo.findText(self.cached_data["font_family"])
            if index >= 0:
                self.font_selector.family_combo.setCurrentIndex(index)
                print(f"Set font family to index {index}: {self.cached_data['font_family']}")
        
        if "font_size" in self.cached_data:
            size = self.cached_data["font_size"]
            print(f"Setting font size to {size}")
            self.font_selector.size_spin.setValue(size)
            
        if "word_spacing" in self.cached_data:
            spacing = self.cached_data["word_spacing"]
            print(f"Setting word spacing to {spacing}")
            self.font_selector.spacing_spin.setValue(spacing)
            
        if "casing" in self.cached_data:
            casing = self.cached_data["casing"]
            print(f"Setting casing to {casing}")
            index = self.font_selector.casing_combo.findText(casing)
            if index >= 0:
                self.font_selector.casing_combo.setCurrentIndex(index)
    
    def reset_all(self):
        """Reset all components to their initial values"""
        # Reset color picker
        self.color_picker.onColorSelected(self.initial_color)
        
        # Reset random color checkbox
        self.random_color_checkbox.setChecked(False)
        
        # Reset font selector
        self.font_selector.family_combo.setCurrentIndex(0)
        self.font_selector.size_spin.setValue(12)
        self.font_selector.bold_button.setChecked(False)
        self.font_selector.spacing_spin.setValue(1.0)
        self.font_selector.casing_combo.setCurrentText("Normal")
    
    def get_all_data(self):
        """Collect and return all the current settings"""
        data = {
            'random_color': self.random_color_checkbox.isChecked(),
            'color': "random" if self.random_color_checkbox.isChecked() else self.color_picker.getColor().name(),
            'font_family': self.font_selector.get_current_font()['path'],
            'font_size': self.font_selector.get_current_font()['size'],
            'word_spacing': self.font_selector.spacing_spin.value(),
            'casing': self.font_selector.casing_combo.currentText()
        }
        return data
    
    def on_ok_clicked(self):
        """Handle OK button click"""
        # Get the data
        data = self.get_all_data()
        # Emit the data
        self.dataReady.emit(data)
        # Accept the dialog
        self.accept()

# Example usage
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    window = BottomBarFormatter()
    
    # Example of how to handle the data
    def handle_data(data):
        print("Color:", data['color'])
        print("Font family:", data['font_family'])
        print("Font size:", data['font_size'])
        print("Word spacing:", data['word_spacing'])
        print("Text case:", data['casing'])
    
    # Connect the dataReady signal to our handler
    # window.dataReady.connect(handle_data)
    
    window.show()
    print(window.get_all_data())
    sys.exit(app.exec_()) 