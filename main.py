from PyQt6.QtWidgets import QApplication
import sys
import treeView

app = QApplication(sys.argv)
window = treeView.TreeView()
window.show()

try:
    sys.exit(app.exec())
except SystemExit:
    print("closing window")
