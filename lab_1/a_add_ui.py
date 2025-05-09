"""
Подключение формы созданной в дизайнере

Команда для конвертации формы:
PySide6-uic path_to_form.ui -o path_to_form.py
"""

from PySide6 import QtWidgets

from ui.b_login_practic import Ui_Form  # Импортируем класс формы


class Window(QtWidgets.QWidget):  # наследуемся от того же класса, что и форма в QtDesigner
    def __init__(self, parent=None):
        super().__init__(parent)

        # Создание "прокси" переменной для работы с формой
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.setWindowTitle("Вход")

        self.ui.pushButtonForgotPass.setText("Забыли пароль?")




if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
