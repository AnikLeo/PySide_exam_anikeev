from PySide6 import QtWidgets


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__initUi() # TODO Вызовите метод для инициализации интерфейса

    def __initUi(self) -> None:
        """
        Инициализация интерфейса

        :return: None
        """

        self.labelLogin = QtWidgets.QLabel("Логин")  # TODO Создайте виджет QLabel с текстом "Логин"
        self.labelRegistration = QtWidgets.QLabel("Регистрация")  # TODO Создайте виджет QLabel с текстом "Регистрация"

        self.lineEditLogin = QtWidgets.QLineEdit()  # TODO создайте виджет QLineEdit
        self.lineEditLogin.setPlaceholderText("Введите логин") # TODO добавьте placeholderText "Введите логин" с помощью метода .setPlaceholderText()
        self.lineEditPassword = QtWidgets.QLineEdit()  # TODO создайте виджет QLineEdit
        self.lineEditPassword.setPlaceholderText("Введите пароль")  # TODO добавьте placeholderText "Введите пароль"
        self.lineEditPassword.setEchoMode(QtWidgets.QLineEdit.PasswordEchoOnEdit)  # TODO установите ограничение видимости вводимых знаков с помощью метода .setEchoMode()

        self.pushButtonLogin = QtWidgets.QPushButton()  # TODO создайте виджет QPushButton
        self.pushButtonLogin.setText("Войти")  # TODO установите текст "Войти" с помощью метода setText()

        self.pushButtonRegistration = QtWidgets.QPushButton()  # TODO создайте виджет QPushButton
        self.pushButtonRegistration.setText("Регистрация")  # TODO установите текст "Регистрация" с помощью метода setText()

        self.layoutLogin = QtWidgets.QHBoxLayout()  # TODO Создайте QHBoxLayout
        self.layoutLogin.addWidget(self.labelLogin)  # TODO с помощью метода .addWidget() добавьте labelLogin
        self.layoutLogin.addWidget(self.lineEditLogin)  # TODO с помощью метода .addWidget() добавьте self.lineEditLogin

        self.layoutPassword = QtWidgets.QHBoxLayout()  # TODO Создайте QHBoxLayout
        self.layoutPassword.addWidget(self.labelRegistration)  # TODO с помощью метода .addWidget() добавьте labelRegistration
        self.layoutPassword.addWidget(self.lineEditPassword)  # TODO с помощью метода .addWidget() добавьте self.lineEditPassword

        self.layoutButtons = QtWidgets.QHBoxLayout()  # TODO Создайте QHBoxLayout
        self.layoutButtons.addWidget(self.pushButtonLogin)  # TODO с помощью метода .addWidget() добавьте self.pushButtonLogin
        self.layoutButtons.addWidget(self.pushButtonRegistration)  # TODO с помощью метода .addWidget() добавьте self.pushButtonRegistration

        self.layoutMain = QtWidgets.QVBoxLayout()   # TODO Создайте QVBoxLayout
        self.layoutMain.addLayout(self.layoutLogin)  # TODO с помощью метода .addLayout() добавьте layoutLogin
        self.layoutMain.addLayout(self.layoutPassword)  # TODO с помощью метода .addLayout() добавьте layoutPassword
        self.layoutMain.addLayout(self.layoutButtons)  # TODO с помощью метода .addLayout() добавьте layoutButtons

        self.setLayout(self.layoutMain)  # TODO с помощью метода setLayout установите layoutMain на основной виджет


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
