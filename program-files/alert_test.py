import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from alert_window import  show_alert


if __name__ == "__main__":
    show_alert("This is a test alert message!") 