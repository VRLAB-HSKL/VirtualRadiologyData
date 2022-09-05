from PyQt6.QtWidgets import QApplication
import sys
import menu

app = QApplication(sys.argv)
window = menu.Menu()
window.show()

try:
    sys.exit(app.exec())
except SystemExit:
    print("closing window")
