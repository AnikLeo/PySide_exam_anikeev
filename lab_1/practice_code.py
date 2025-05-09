from PySide6 import QtWidgets


class Window(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Простое окно")
        self.resize(300, 200)

        print(self.layout())



if __name__ == '__main__':

    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()


# test