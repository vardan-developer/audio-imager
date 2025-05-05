from PyQt5.QtWidgets import (QWidget, QComboBox, QSpinBox, QPushButton, 
                            QHBoxLayout, QVBoxLayout, QLabel, QFrame,
                            QDoubleSpinBox, QToolButton, QSizePolicy)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont, QIcon
from font_mapping import get_fonts_mapping

class FontStyleSelector(QWidget):
    """
    A component for selecting font styles that can be integrated into a PyQt5 GUI.
    Provides font family selection, size adjustment, bold toggling, word spacing,
    and text casing options in a two-row toolbar-like interface.
    """
    fontChanged = pyqtSignal(dict)  # Signal emitted when font settings change
    
    def __init__(self, parent=None, min_font_size=8, max_font_size=300, default_size=12, cached_data = None):
        super().__init__(parent)
        
        # Get font mappings
        self.fonts_mapping = get_fonts_mapping()
        self.cached_data = cached_data
        # Process font data
        self.font_families = self._process_font_families()
        
        # Initialize UI
        self._init_ui(min_font_size, max_font_size, default_size)
        
        # Apply cached settings if available
        if self.cached_data:
            self.apply_cached_settings()
        
    def _process_font_families(self):
        """Process font mapping to extract font families and their variants"""
        font_families = {}
        
        for (name, weight), path in self.fonts_mapping.items():
            if name not in font_families:
                font_families[name] = {'variants': set(), 'paths': {}}
            
            font_families[name]['variants'].add(weight)
            font_families[name]['paths'][weight] = path
            
        return font_families
    
    def _init_ui(self, min_font_size, max_font_size, default_size):
        """Initialize the UI components in a two-row toolbar-like style"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(2)
        
        # First row: Font family, size, and bold
        row1_frame = QFrame(self)
        row1_frame.setFrameShape(QFrame.NoFrame)  # Remove frame border
        row1_frame.setStyleSheet("QFrame { background-color: #f0f0f0; border: none; }")
        row1_layout = QHBoxLayout(row1_frame)
        row1_layout.setSpacing(2)
        row1_layout.setContentsMargins(4, 2, 4, 2)
        
        # Font family selection with improved dropdown
        self.family_combo = QComboBox()
        self.family_combo.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.family_combo.setMinimumWidth(150)
        self.family_combo.setMaximumWidth(300)  # Set a reasonable maximum width
        self.family_combo.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        
        # Sort font families alphabetically and add to combo box
        sorted_families = sorted(self.font_families.keys())
        self.family_combo.addItems(sorted_families)
        row1_layout.addWidget(self.family_combo)
        
        # Add vertical separator
        separator1 = QFrame()
        separator1.setFrameShape(QFrame.VLine)
        separator1.setFrameShadow(QFrame.Sunken)
        separator1.setStyleSheet("QFrame { color: #d0d0d0; }")  # Lighter color for separator
        row1_layout.addWidget(separator1)
        
        # Font size selection
        self.size_spin = QSpinBox()
        self.size_spin.setRange(min_font_size, max_font_size)
        self.size_spin.setValue(default_size)
        self.size_spin.setFixedWidth(50)
        row1_layout.addWidget(self.size_spin)
        
        # Add vertical separator
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.VLine)
        separator2.setFrameShadow(QFrame.Sunken)
        separator2.setStyleSheet("QFrame { color: #d0d0d0; }")  # Lighter color for separator
        row1_layout.addWidget(separator2)
        
        # Improved Bold button
        self.bold_button = QToolButton()
        self.bold_button.setText("B")
        self.bold_button.setCheckable(True)
        self.bold_button.setFixedSize(28, 28)
        self.bold_button.setFont(QFont("Arial", 10, QFont.Bold))
        self.bold_button.setToolTip("Bold")
        self.bold_button.setStyleSheet("""
            QToolButton {
                background-color: #f8f8f8;
            }
            QToolButton:checked {
                background-color: #e0e000;
                border: 1px solid #000000;
            }
            QToolButton:hover {
                background-color: #e8e8e8;
            }
        """)
        row1_layout.addWidget(self.bold_button)
        
        # Add stretch to push everything to the left
        row1_layout.addStretch()
        
        # Second row: Word spacing and text casing
        row2_frame = QFrame(self)
        row2_frame.setFrameShape(QFrame.NoFrame)  # Remove frame border
        row2_frame.setStyleSheet("QFrame { background-color: #f0f0f0; border: none; }")
        row2_layout = QHBoxLayout(row2_frame)
        row2_layout.setSpacing(2)
        row2_layout.setContentsMargins(4, 2, 4, 2)
        
        # Word spacing control
        spacing_label = QLabel("Spacing:")
        self.spacing_spin = QDoubleSpinBox()
        self.spacing_spin.setRange(0.8, 3.0)
        self.spacing_spin.setValue(1.0)
        self.spacing_spin.setSingleStep(0.1)
        self.spacing_spin.setFixedWidth(60)
        row2_layout.addWidget(spacing_label)
        row2_layout.addWidget(self.spacing_spin)
        
        # Add vertical separator
        separator3 = QFrame()
        separator3.setFrameShape(QFrame.VLine)
        separator3.setFrameShadow(QFrame.Sunken)
        separator3.setStyleSheet("QFrame { color: #d0d0d0; }")  # Lighter color for separator
        row2_layout.addWidget(separator3)
        
        # Text casing options with improved dropdown
        casing_label = QLabel("Case:")
        row2_layout.addWidget(casing_label)
        
        self.casing_combo = QComboBox()
        self.casing_combo.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.casing_combo.addItems(["Normal", "UPPERCASE", "lowercase", "Capitalize"])
        self.casing_combo.setMinimumWidth(100)
        row2_layout.addWidget(self.casing_combo)
        
        # Add stretch to push everything to the left
        row2_layout.addStretch()
        
        # Add both rows to main layout
        main_layout.addWidget(row1_frame)
        main_layout.addWidget(row2_frame)
        
        # Connect signals
        self.family_combo.currentTextChanged.connect(self._update_bold_availability)
        self.family_combo.currentTextChanged.connect(self._emit_font_changed)
        self.size_spin.valueChanged.connect(self._emit_font_changed)
        self.bold_button.toggled.connect(self._emit_font_changed)
        self.spacing_spin.valueChanged.connect(self._emit_font_changed)
        self.casing_combo.currentTextChanged.connect(self._emit_font_changed)
        
        # Initialize bold button state
        self._update_bold_availability(self.family_combo.currentText())
    
    def _update_bold_availability(self, font_family):
        """Enable or disable bold button based on font variants availability"""
        if not font_family or font_family not in self.font_families:
            self.bold_button.setEnabled(False)
            return
            
        variants = self.font_families[font_family]['variants']
        has_bold = any(v.lower() == 'bold' or v.lower() == 'semibold' or v.lower() == 'medium' for v in variants)
        has_regular = any(v.lower() == 'regular' for v in variants)
        
        # Enable bold button only if the font has both regular and bold variants
        self.bold_button.setEnabled(has_bold and has_regular)
        
        # If bold is not available, ensure it's not selected
        if not (has_bold and has_regular) and self.bold_button.isChecked():
            self.bold_button.setChecked(False)
    
    def _emit_font_changed(self, *args):
        """Emit signal with current font settings"""
        font_info = self.get_current_font()
        self.fontChanged.emit(font_info)
    
    def get_current_font(self):
        """Return the current font settings"""
        font_family = self.family_combo.currentText()
        font_size = self.size_spin.value()
        is_bold = self.bold_button.isChecked()
        word_spacing = self.spacing_spin.value()
        text_case = self.casing_combo.currentText()
        
        # Get the appropriate font path
        font_path = None
        if font_family in self.font_families:
            weight = 'Bold' if is_bold else 'Regular'
            paths = self.font_families[font_family]['paths']
            
            if weight in paths:
                font_path = paths[weight]
            elif len(paths) > 0:
                # Fallback to any available variant
                font_path = next(iter(paths.values()))
        
        return {
            'family': font_family,
            'size': font_size,
            'bold': is_bold,
            'path': font_path,
            'word_spacing': word_spacing,
            'text_case': text_case
        }
    
    def apply_text_case(self, text):
        """Apply the selected text case to the given text"""
        case_type = self.casing_combo.currentText()
        
        if case_type == "UPPERCASE":
            return text.upper()
        elif case_type == "lowercase":
            return text.lower()
        elif case_type == "Capitalize":
            return text.title()
        else:  # Normal
            return text
    
    def apply_cached_settings(self):
        """Apply font settings from cached data"""
        if not self.cached_data:
            return
        
        print(f"Applying cached font settings: {self.cached_data}")
        
        # Set font family if available
        if "font_family" in self.cached_data:
            # Extract font family name from path
            import os
            font_path = self.cached_data["font_family"]
            font_filename = os.path.basename(font_path).lower()
            
            # Try to find a matching font in our families
            for i in range(self.family_combo.count()):
                family_name = self.family_combo.itemText(i)
                if family_name.lower() in font_filename or font_filename in family_name.lower():
                    self.family_combo.setCurrentIndex(i)
                    print(f"Setting font family to {family_name} based on {font_filename}")
                    break
        
        # Set font size if available - even more explicit handling
        if "font_size" in self.cached_data:
            try:
                # Handle different types of input - string, int, float
                size_value = self.cached_data["font_size"]
                if isinstance(size_value, str):
                    size = int(float(size_value))
                else:
                    size = int(size_value)
                    
                print(f"Setting font size to {size} (original value: {size_value}, type: {type(size_value)})")
                
                # Make sure size is within allowed range
                max_size = self.size_spin.maximum()
                min_size = self.size_spin.minimum()
                
                if size > max_size:
                    print(f"Size {size} exceeds maximum {max_size}, capping")
                    size = max_size
                elif size < min_size:
                    print(f"Size {size} below minimum {min_size}, capping")
                    size = min_size
                    
                # Set the value and verify it was set
                self.size_spin.setValue(size)
                print(f"Font size now set to: {self.size_spin.value()}")
            except (ValueError, TypeError) as e:
                print(f"Error setting font size: {e}")
        
        # Set word spacing if available
        if "word_spacing" in self.cached_data:
            try:
                spacing = float(self.cached_data["word_spacing"])
                print(f"Setting word spacing to {spacing}")
                self.spacing_spin.setValue(spacing)
            except (ValueError, TypeError) as e:
                print(f"Error setting word spacing: {e}")
        
        # Set text casing if available
        if "casing" in self.cached_data:
            casing = self.cached_data["casing"]
            index = self.casing_combo.findText(casing)
            if index >= 0:
                print(f"Setting text casing to {casing}")
                self.casing_combo.setCurrentIndex(index) 