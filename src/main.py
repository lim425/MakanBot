import sys
import os
from PySide6.QtWidgets import QApplication
from mainwindow import MainWindow

app = QApplication(sys.argv)
script_dir = os.path.dirname(os.path.abspath(__file__))
style_path = os.path.join(script_dir, "gui", "style.qss")

with open(style_path, "r") as f:
    app.setStyleSheet(f.read())
    
w = MainWindow(app)

w.showMaximized()
app.exec()
