from PySide6.QtWidgets import QApplication
from gui_app import MainWindow

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
