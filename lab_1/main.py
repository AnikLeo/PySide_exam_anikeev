import sys
from PySide6 import QtWidgets

app = QtWidgets.QApplication()

window = QtWidgets.QWidget()

window.show()

sys.exit(app.exec())



# app = QApplication(sys.argv)
#
# window = QWidget()
# window.setWindowTitle('Простейшее окно')
# window.show()
#
# sys.exit(app.exec())