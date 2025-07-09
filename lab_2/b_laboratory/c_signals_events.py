"""
Реализация программу проверки состояния окна:
Форма для приложения (ui/c_signals_events_form.ui)

Программа должна обладать следующим функционалом:

1. Возможность перемещения окна по заданным координатам.
2. Возможность получения параметров экрана (вывод производить в plainTextEdit + добавлять время).
    * Кол-во экранов
    * Текущее основное окно
    * Разрешение экрана
    * На каком экране окно находится
    * Размеры окна
    * Минимальные размеры окна
    * Текущее положение (координаты) окна
    * Координаты центра приложения
    * Отслеживание состояния окна (свернуто/развёрнуто/активно/отображено)
3. Возможность отслеживания состояния окна (вывод производить в консоль + добавлять время).
    * При перемещении окна выводить его старую и новую позицию
    * При изменении размера окна выводить его новый размер
"""


from PySide6.QtWidgets import QApplication, QWidget, QPlainTextEdit, QVBoxLayout, QtWidgets
from PySide6.QtUiTools import loadUi
from PySide6.QtCore import Qt, QDateTime
from PySide6.QtGui import QTextCursor



class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)


        loadUi('ui/c_signals_events_form.ui', self)


        self.plainTextEdit = QPlainTextEdit(self)
        self.plainTextEdit.setReadOnly(True)
        self.verticalLayout_2.addWidget(self.plainTextEdit)


        self.setup_connections()


        self.update_screen_info()

    def setup_connections(self):

        self.dial.valueChanged.connect(self.move_window_by_dial)
        self.horizontalSlider.valueChanged.connect(self.resize_window_by_slider)

        # Отслеживание событий окна
        self.windowStateChanged.connect(self.on_window_state_changed)
        if self.windowHandle():
            self.windowHandle().screenChanged.connect(self.on_screen_changed)

    def move_window_by_dial(self, value):
        old_pos = self.pos()
        new_x = value * 2
        new_y = value * 2
        self.move(new_x, new_y)
        self.log_position_change(old_pos, self.pos())

    def resize_window_by_slider(self, value):
        new_width = 200 + value * 2
        new_height = 150 + value
        self.resize(new_width, new_height)
        self.log_console(f"Window resized to: {new_width}x{new_height}")

    def update_screen_info(self):
        screen = self.windowHandle().screen() if self.windowHandle() else QApplication.primaryScreen()
        screens = QApplication.screens()

        info = f"""
    === Screen Information ({QDateTime.currentDateTime().toString('hh:mm:ss')}) ===
    Number of screens: {len(screens)}
    Current primary screen: {QApplication.primaryScreen().name()}
    Screen resolution: {screen.size().width()}x{screen.size().height()}
    Current screen: {screen.name() if self.windowHandle() else 'primary'}
    Window size: {self.width()}x{self.height()}
    Minimum size: {self.minimumWidth()}x{self.minimumHeight()}
    Window position: {self.x()}, {self.y()}
    Window center: {self.geometry().center().x()}, {self.geometry().center().y()}
    Window state: {self.get_window_state()}
    """
        self.plainTextEdit.appendPlainText(info)
        self.plainTextEdit.moveCursor(QTextCursor.End)

    def get_window_state(self):
        if self.isMinimized():
            return "Minimized"
        elif self.isMaximized():
            return "Maximized"
        elif self.isFullScreen():
            return "FullScreen"
        elif self.isActiveWindow():
            return "Active"
        elif self.isVisible():
            return "Visible"
        else:
            return "Hidden"

    def log_position_change(self, old_pos, new_pos):
        message = f"[{QDateTime.currentDateTime().toString('hh:mm:ss')}] Window moved from ({old_pos.x()}, {old_pos.y()}) to ({new_pos.x()}, {new_pos.y()})"
        self.log_console(message)
        self.update_screen_info()

    def log_console(self, message):
        print(message)

    def on_window_state_changed(self, state):
        state_str = "!"
        if state & Qt.WindowMinimized:
            state_str = "Minimized"
        elif state & Qt.WindowMaximized:
            state_str = "Maximized"
        elif state & Qt.WindowFullScreen:
            state_str = "FullScreen"
        else:
            state_str = "Normal"

        message = f"[{QDateTime.currentDateTime().toString('hh:mm:ss')}] Window state changed: {state_str}"
        self.log_console(message)
        self.update_screen_info()

    def on_screen_changed(self, screen):
        message = f"[{QDateTime.currentDateTime().toString('hh:mm:ss')}] Window moved to screen: {screen.name()}"
        self.log_console(message)
        self.update_screen_info()

    def moveEvent(self, event):
        super().moveEvent(event)
        self.update_screen_info()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.log_console(
            f"[{QDateTime.currentDateTime().toString('hh:mm:ss')}] Window resized to: {self.width()}x{self.height()}")
        self.update_screen_info()

    def changeEvent(self, event):
        super().changeEvent(event)
        if event.type() == event.WindowStateChange:
            self.update_screen_info()


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
