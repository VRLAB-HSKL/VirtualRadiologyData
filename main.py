from PyQt6.QtWidgets import QApplication
import sys
import menu
from postprocessing import config

app = QApplication(sys.argv)
window = menu.Menu()
window.show()

try:
    sys.exit(app.exec())
except SystemExit:
    if config.httpd is not None:
        config.httpd.shutdown()
    print("closing window")
