from classes import *
from windows import *
from PySide6.QtWidgets import QApplication, QMainWindow 
app = QApplication()
window = QMainWindow()
ui = MainWindow()
ui.setupUi(window)
window.show()
app.exec()