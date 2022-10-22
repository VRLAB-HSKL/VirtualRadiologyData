from PyQt6.QtWidgets import QApplication
import sys
import menu
from postprocessing import templconf

app = QApplication(sys.argv)
window = menu.Menu()
window.show()

try:
    sys.exit(app.exec())
except SystemExit:
    if templconf.httpd is not None:
        templconf.httpd.shutdown()
    print("closing window")
