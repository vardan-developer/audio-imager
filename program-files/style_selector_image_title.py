from PyQt5.QtWidgets import (QDialog, QWidget, QVBoxLayout, QHBoxLayout,
                            QPushButton, QLabel, QFrame)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor
from ColorPicker import ColorPicker
from font_style_selector import FontStyleSelector
from text_position_selector import TextPositionSelector

class ImageTitleFormatter(QDialog):
    # Signal to emit the data when OK is clicked
    dataReady = pyqtSignal(dict)
    
    def __init__(self, parent=None, cached_data=None):
        super().__init__(parent)
        self.setWindowTitle("Podcast Title Formatter")
        self.setMinimumSize(900, 700)  # Set a reasonable minimum size
        self.cached_data = cached_data
        self.initUI()
        
    def initUI(self):
        # Create main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Title label
        title_label = QLabel("Podcast Title Formatter")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Create two-column layout
        columns_layout = QHBoxLayout()
        
        # Left column (Color Picker)
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
        
        # Add Color Picker
        color_label = QLabel("Color Selection")
        color_label.setFont(QFont("Arial", 12, QFont.Bold))
        left_layout.addWidget(color_label)
        
        self.color_picker = ColorPicker(cached_data=self.cached_data)
        left_layout.addWidget(self.color_picker)
        left_layout.addStretch()
        
        # Right column (Font Style and Text Position)
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
        
        # Add Font Style Selector
        font_label = QLabel("Font Style")
        font_label.setFont(QFont("Arial", 12, QFont.Bold))
        right_layout.addWidget(font_label)
        
        self.font_selector = FontStyleSelector(cached_data=self.cached_data)
        right_layout.addWidget(self.font_selector)
        
        # Add some spacing between components
        spacer = QFrame()
        spacer.setFrameShape(QFrame.HLine)
        spacer.setStyleSheet("QFrame { border: 1px solid #ddd; }")
        right_layout.addWidget(spacer)
        
        # Add Text Position Selector
        position_label = QLabel("Text Position")
        position_label.setFont(QFont("Arial", 12, QFont.Bold))
        right_layout.addWidget(position_label)
        
        self.position_selector = TextPositionSelector(cached_data=self.cached_data)
        right_layout.addWidget(self.position_selector)
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
        self.initial_position = self.position_selector.get_current_position()
        
        # Apply cached settings if available
        if self.cached_data:
            self.apply_cached_settings()
            
    def apply_cached_settings(self):
        """Apply cached settings to UI components"""
        if not self.cached_data:
            return
            
        print(f"Applying cached settings to ImageTitleFormatter: {self.cached_data}")
            
        # Apply color if available
        if "color" in self.cached_data:
            color = QColor(self.cached_data["color"])
            self.color_picker.onColorSelected(color)
        
        # Note: Font settings are now handled directly by FontStyleSelector's apply_cached_settings method
        # since we pass the cached_data to it during initialization
            
        # Apply position settings if available
        if "position" in self.cached_data and isinstance(self.cached_data["position"], dict):
            pos_data = self.cached_data["position"]
            
            # Handle preset positions
            if "type" in pos_data and pos_data["type"] == "preset":
                self.position_selector.preset_radio.setChecked(True)
                
                # Find and select the button for the preset position
                if "preset_id" in pos_data:
                    btn = self.position_selector.preset_positions.button(pos_data["preset_id"])
                    if btn:
                        btn.setChecked(True)
                        print(f"Set preset position id: {pos_data['preset_id']}")
                # Alternative using row/col if preset_id is not available
                elif "row" in pos_data and "col" in pos_data:
                    preset_id = pos_data["row"] * 3 + pos_data["col"] + 1
                    btn = self.position_selector.preset_positions.button(preset_id)
                    if btn:
                        btn.setChecked(True)
                        print(f"Set preset position from row/col: {preset_id}")
            
            # Handle custom positions
            elif "type" in pos_data and pos_data["type"] == "custom":
                self.position_selector.custom_radio.setChecked(True)
                
                if "left" in pos_data:
                    self.position_selector.left_spin.setValue(pos_data["left"])
                if "top" in pos_data:
                    self.position_selector.top_spin.setValue(pos_data["top"])
    
    def reset_all(self):
        """Reset all components to their initial values"""
        # Reset color picker
        self.color_picker.onColorSelected(self.initial_color)
        
        # Reset font selector
        # Reset font family to first item
        self.font_selector.family_combo.setCurrentIndex(0)
        # Reset font size to default
        self.font_selector.size_spin.setValue(12)
        # Reset bold to unchecked
        self.font_selector.bold_button.setChecked(False)
        # Reset word spacing to 1.0
        self.font_selector.spacing_spin.setValue(1.0)
        # Reset text case to Normal
        self.font_selector.casing_combo.setCurrentText("Normal")
        
        # Reset position selector
        # Select preset position option
        self.position_selector.preset_radio.setChecked(True)
        # Reset to top-left position (first button)
        first_button = self.position_selector.preset_positions.button(1)
        if first_button:
            first_button.setChecked(True)
        # Reset custom position values
        self.position_selector.left_spin.setValue(0)
        self.position_selector.top_spin.setValue(0)
    
    def on_ok_clicked(self):
        """Handle OK button click"""
        # Get the data
        data = self.get_all_data()
        # Emit the data
        self.dataReady.emit(data)
        # Accept the dialog
        self.accept()
    
    def get_all_data(self):
        """Collect and return all the current settings"""
        data = {
            'color': self.color_picker.getColor().name(),
            'font_family': self.font_selector.get_current_font()['path'],
            'font_size': self.font_selector.get_current_font()['size'],
            'word_spacing': self.font_selector.spacing_spin.value(),
            'casing': self.font_selector.casing_combo.currentText(),
            'position': self.position_selector.get_current_position()
        }
        return data
    
# Example usage
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    window = ImageTitleFormatter()
    
    # Example of how to handle the data
    def handle_data(data):
        print("Color:", data['color'].name())
        print("Font:", data['font'])
        print("Position:", data['position'])
    
    # Connect the dataReady signal to our handler
    window.dataReady.connect(handle_data)
    
    window.show()
    print(window.get_all_data())
    sys.exit(app.exec_())
