from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

def show_alert(message, parent=None):
    """
    Shows an alert window with the given message.
    Usage:
        from alert_window import show_alert
        show_alert("Your message here")
    """
    # Create application instance if it doesn't exist
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    
    dialog = QDialog(parent)
    dialog.setWindowTitle("Alert")
    dialog.setModal(True)
    dialog.setFixedSize(400, 200)
    dialog.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
    
    # Create layout
    layout = QVBoxLayout()
    layout.setContentsMargins(20, 20, 20, 20)
    layout.setSpacing(20)
    
    # Message label
    message_label = QLabel(message)
    message_label.setWordWrap(True)
    message_label.setAlignment(Qt.AlignCenter)
    message_label.setFont(QFont("Arial", 12))
    message_label.setStyleSheet("""
        QLabel {
            color: #333333;
            background-color: transparent;
            padding: 10px;
        }
    """)
    
    # OK button
    ok_button = QPushButton("OK")
    ok_button.setFixedWidth(100)
    ok_button.setFixedHeight(30)
    ok_button.setFont(QFont("Arial", 10))
    ok_button.setStyleSheet("""
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 5px 15px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        QPushButton:pressed {
            background-color: #3d8b40;
        }
    """)
    ok_button.clicked.connect(dialog.accept)
    
    # Add widgets to layout
    layout.addWidget(message_label)
    layout.addWidget(ok_button, alignment=Qt.AlignCenter)
    
    dialog.setLayout(layout)
    
    # Set window style
    dialog.setStyleSheet("""
        QDialog {
            background-color: white;
            border: 1px solid #cccccc;
            border-radius: 8px;
        }
    """)
    
    dialog.exec_() 