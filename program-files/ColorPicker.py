from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
                            QLabel, QFrame)
from PyQt5.QtGui import QColor, QPainter, QLinearGradient
from PyQt5.QtCore import Qt, pyqtSignal, QRect

class ColorSquare(QFrame):
    clicked = pyqtSignal(QColor)
    
    def __init__(self, color=QColor(255, 255, 255), size=25):
        super().__init__()
        self.color = color
        self.setFixedSize(size, size)
        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.setCursor(Qt.PointingHandCursor)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), self.color)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.color)

class ColorPreviewBar(QFrame):
    def __init__(self):
        super().__init__()
        self.color = QColor(255, 0, 0)
        self.setMinimumSize(200, 30)
        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), self.color)
        
    def setColor(self, color):
        self.color = color
        self.update()

class ColorSpectrum(QFrame):
    colorChanged = pyqtSignal(QColor)
    
    def __init__(self):
        super().__init__()
        self.setMinimumSize(200, 200)
        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.setCursor(Qt.CrossCursor)
        self.selected_color = QColor(255, 0, 0)
        self.selected_pos = None
        
    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.rect()
        
        # Draw color spectrum
        for x in range(rect.width()):
            for y in range(rect.height()):
                h = x / rect.width()
                s = 1.0 - (y / rect.height())
                v = 1.0
                color = QColor.fromHsvF(h, s, v)
                painter.setPen(color)
                painter.drawPoint(x, y)
        
        # Draw selection marker if a color is selected
        if self.selected_pos:
            painter.setPen(Qt.white)
            painter.drawEllipse(self.selected_pos, 5, 5)
            painter.setPen(Qt.black)
            painter.drawEllipse(self.selected_pos, 4, 4)
    
    def mousePressEvent(self, event):
        self.updateColor(event.pos())
        
    def mouseMoveEvent(self, event):
        self.updateColor(event.pos())
        
    def updateColor(self, pos):
        if self.rect().contains(pos):
            self.selected_pos = pos
            h = pos.x() / self.width()
            s = 1.0 - (pos.y() / self.height())
            self.selected_color = QColor.fromHsvF(h, s, 1.0)
            self.update()
            self.colorChanged.emit(self.selected_color)

class ColorPicker(QWidget):
    colorChanged = pyqtSignal(QColor)
    
    def __init__(self, cached_data=None):
        super().__init__()
        self.cached_data = cached_data
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Basic colors row
        basic_colors_layout = QHBoxLayout()
        self.basic_colors = [
            "#FF0000", "#FF8000", "#FFFF00", "#80FF00", "#00FF00",
            "#00FF80", "#00FFFF", "#0080FF", "#0000FF", "#8000FF",
            "#FF00FF", "#FF0080", "#000000", "#FFFFFF"
        ]
        
        for color in self.basic_colors:
            square = ColorSquare(QColor(color))
            square.clicked.connect(self.onColorSelected)
            basic_colors_layout.addWidget(square)
            
        basic_colors_layout.addStretch()
        layout.addLayout(basic_colors_layout)
        
        # Color spectrum
        self.spectrum = ColorSpectrum()
        self.spectrum.colorChanged.connect(self.onColorSelected)
        layout.addWidget(self.spectrum)
        
        # Hex color input
        hex_layout = QHBoxLayout()
        hex_layout.addWidget(QLabel("Hex:"))
        
        self.hex_input = QLineEdit()
        self.hex_input.setPlaceholderText("#RRGGBB")
        self.hex_input.textChanged.connect(self.onHexChanged)
        hex_layout.addWidget(self.hex_input)
        
        layout.addLayout(hex_layout)
        
        # Color preview bar
        self.preview_bar = ColorPreviewBar()
        layout.addWidget(self.preview_bar)
        
        # Set initial color from cache if available
        if self.cached_data and "color" in self.cached_data and self.cached_data["color"] != "random":
            try:
                print(f"ColorPicker using cached color: {self.cached_data['color']}")
                self.current_color = QColor(self.cached_data["color"])
                if not self.current_color.isValid():
                    print(f"Invalid color in cache: {self.cached_data['color']}, using default")
                    self.current_color = QColor("#FF0000")  # Fallback to red
            except Exception as e:
                print(f"Error setting cached color: {e}")
                self.current_color = QColor("#FF0000")  # Fallback to red
        else:
            self.current_color = QColor("#FF0000")  # Default to red
            
        self.updateHexInput(self.current_color)
        self.preview_bar.setColor(self.current_color)
        
    def onColorSelected(self, color):
        self.current_color = color
        self.updateHexInput(color)
        self.preview_bar.setColor(color)
        self.colorChanged.emit(color)
        
    def onHexChanged(self, hex_value):
        # Remove any spaces and ensure # is present
        hex_value = hex_value.strip()
        if not hex_value.startswith('#'):
            hex_value = '#' + hex_value
            
        # Only update if it's a valid color
        color = QColor(hex_value)
        if color.isValid():
            self.current_color = color
            self.preview_bar.setColor(color)
            self.colorChanged.emit(color)
            
    def updateHexInput(self, color):
        hex_value = color.name().upper()
        self.hex_input.setText(hex_value)
        
    def getColor(self):
        return self.current_color 