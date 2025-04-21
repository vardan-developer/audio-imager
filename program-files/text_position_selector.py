from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QRadioButton, QButtonGroup, QSpinBox, QFrame,
                            QGridLayout)
from PyQt5.QtCore import pyqtSignal, Qt

class TextPositionSelector(QWidget):
    """
    A component for selecting text position that can be integrated into a PyQt5 GUI.
    Provides preset position selection via a grid of radio buttons and custom position
    input via spinboxes.
    """
    positionChanged = pyqtSignal(dict)  # Signal emitted when position settings change
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Initialize UI
        self._init_ui()
        
    def _init_ui(self):
        """Initialize the UI components"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create frame
        frame = QFrame(self)
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setStyleSheet("""
            QFrame {
                background-color: #f0f0f0;
            }
        """)
        
        frame_layout = QVBoxLayout(frame)
        frame_layout.setSpacing(10)
        
        # # Position selection section
        # position_label = QLabel("Position")
        # frame_layout.addWidget(position_label)
        
        # Radio button options
        position_options_layout = QHBoxLayout()
        
        # Preset position option
        self.preset_radio = QRadioButton("Preset Position")
        self.preset_radio.setChecked(True)
        
        # Custom position option
        self.custom_radio = QRadioButton("Custom Position")
        
        # Add to button group
        self.position_type_group = QButtonGroup(self)
        self.position_type_group.addButton(self.preset_radio, 1)
        self.position_type_group.addButton(self.custom_radio, 2)
        
        position_options_layout.addWidget(self.preset_radio)
        position_options_layout.addWidget(self.custom_radio)
        position_options_layout.addStretch()
        
        frame_layout.addLayout(position_options_layout)
        
        # Create container for both position selection methods
        position_container = QHBoxLayout()
        
        # Preset position grid (3x3 grid of radio buttons)
        preset_container = QFrame()
        preset_layout = QGridLayout(preset_container)
        preset_layout.setSpacing(10)  # Increased spacing for better visibility
        
        self.preset_positions = QButtonGroup(self)
        
        # Create 3x3 grid of radio buttons with Windows-style appearance
        for row in range(3):
            for col in range(3):
                position_id = row * 3 + col + 1
                radio = QRadioButton()
                
                # Set the top-left position as default
                if row == 0 and col == 0:
                    radio.setChecked(True)
                
                self.preset_positions.addButton(radio, position_id)
                preset_layout.addWidget(radio, row, col, Qt.AlignCenter)
        
        # Custom position inputs
        custom_container = QFrame()
        custom_layout = QGridLayout(custom_container)
        
        # Left position
        left_label = QLabel("Left")
        self.left_spin = QSpinBox()
        self.left_spin.setRange(0, 1000)
        self.left_spin.setValue(0)
        self.left_spin.setFixedWidth(60)
        
        # Top position
        top_label = QLabel("Top")
        self.top_spin = QSpinBox()
        self.top_spin.setRange(0, 1000)
        self.top_spin.setValue(0)
        self.top_spin.setFixedWidth(60)
        
        custom_layout.addWidget(left_label, 0, 0)
        custom_layout.addWidget(self.left_spin, 0, 1)
        custom_layout.addWidget(top_label, 1, 0)
        custom_layout.addWidget(self.top_spin, 1, 1)
        
        # Initially disable custom position inputs
        custom_container.setEnabled(False)
        
        # Add both containers to position container
        position_container.addWidget(preset_container)
        position_container.addWidget(custom_container)
        position_container.addStretch()
        
        frame_layout.addLayout(position_container)
        
        # Add frame to main layout
        main_layout.addWidget(frame)
        
        # Connect signals
        self.preset_radio.toggled.connect(lambda checked: preset_container.setEnabled(checked))
        self.custom_radio.toggled.connect(lambda checked: custom_container.setEnabled(checked))
        
        self.preset_positions.buttonClicked.connect(self._emit_position_changed)
        self.position_type_group.buttonClicked.connect(self._emit_position_changed)
        self.left_spin.valueChanged.connect(self._emit_position_changed)
        self.top_spin.valueChanged.connect(self._emit_position_changed)
    
    def _emit_position_changed(self, *args):
        """Emit signal with current position settings"""
        position_info = self.get_current_position()
        self.positionChanged.emit(position_info)
    
    def get_current_position(self):
        """Return the current position settings"""
        use_preset = self.preset_radio.isChecked()
        
        if use_preset:
            # Get the selected preset position (1-9)
            preset_id = self.preset_positions.checkedId()
            
            # Convert preset ID to row and column (0-based)
            row = (preset_id - 1) // 3
            col = (preset_id - 1) % 3
            
            # Map to position names
            position_names = {
                (0, 0): "top-left",
                (0, 1): "top-center",
                (0, 2): "top-right",
                (1, 0): "middle-left",
                (1, 1): "middle-center",
                (1, 2): "middle-right",
                (2, 0): "bottom-left",
                (2, 1): "bottom-center",
                (2, 2): "bottom-right"
            }
            
            position_name = position_names.get((row, col), "top-left")
            
            return {
                'type': 'preset',
                'preset_id': preset_id,
                'position_name': position_name,
                'row': row,
                'col': col
            }
        else:
            # Get custom position values
            left = self.left_spin.value()
            top = self.top_spin.value()
            
            return {
                'type': 'custom',
                'left': left,
                'top': top
            } 