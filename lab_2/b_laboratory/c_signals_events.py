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
import sys
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtUiTools import QUiLoader


class WindowStateMonitor(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()


        self.ui = self.load_ui("ui/c_signals_events_form.ui")


        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.ui)


        self.plainTextEdit = QtWidgets.QPlainTextEdit()
        self.plainTextEdit.setReadOnly(True)


        vertical_layout = self.ui.findChild(QtWidgets.QVBoxLayout, "verticalLayout_2")
        if vertical_layout:
            vertical_layout.addWidget(self.plainTextEdit)


        self.dial = self.ui.findChild(QtWidgets.QDial, "dial")
        self.horizontal_slider = self.ui.findChild(QtWidgets.QSlider, "horizontalSlider")

        if self.dial:
            self.dial.setRange(0, 100)
        if self.horizontal_slider:
            self.horizontal_slider.setRange(0, 100)


        self.setup_connections()


        self.update_screen_info()

    def load_ui(self, ui_file):
        loader = QUiLoader()
        file = QtCore.QFile(ui_file)
        if not file.open(QtCore.QFile.ReadOnly):
            print(f"Cannot open UI file: {file.errorString()}")
            sys.exit(-1)

        ui = loader.load(file)
        file.close()
        return ui

    def setup_connections(self):
        if self.dial:
            self.dial.valueChanged.connect(self.move_window_by_dial)
        if self.horizontal_slider:
            self.horizontal_slider.valueChanged.connect(self.resize_window_by_slider)


        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.WindowStateChange:
            self.on_window_state_changed(self.windowState())
        return super().eventFilter(obj, event)

    def move_window_by_dial(self, value):
        old_pos = self.pos()
        new_pos = QtCore.QPoint(value * 3, value * 2)
        self.move(new_pos)
        self.log_position_change(old_pos, new_pos)

    def resize_window_by_slider(self, value):
        new_width = 300 + value * 2
        new_height = 200 + value
        self.resize(new_width, new_height)
        self.log_console(f"Window resized to: {new_width}x{new_height}")

    def update_screen_info(self):
        screen = self.screen() if self.screen() else QtWidgets.QApplication.primaryScreen()
        screens = QtWidgets.QApplication.screens()

        info = f"""
=== Screen Information ({QtCore.QDateTime.currentDateTime().toString('hh:mm:ss')}) ===
Number of screens: {len(screens)}
Current primary screen: {QtWidgets.QApplication.primaryScreen().name()}
Screen resolution: {screen.size().width()}x{screen.size().height()}
Current screen: {screen.name()}
Window size: {self.width()}x{self.height()}
Minimum size: {self.minimumWidth()}x{self.minimumHeight()}
Window position: {self.x()}, {self.y()}
Window center: {self.geometry().center().x()}, {self.geometry().center().y()}
Window state: {self.get_window_state()}
"""
        self.plainTextEdit.appendPlainText(info)
        self.plainTextEdit.moveCursor(QtGui.QTextCursor.End)

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
        return "Hidden"

    def log_position_change(self, old_pos, new_pos):
        message = f"[{QtCore.QDateTime.currentDateTime().toString('hh:mm:ss')}] Window moved from ({old_pos.x()}, {old_pos.y()}) to ({new_pos.x()}, {new_pos.y()})"
        self.log_console(message)
        self.update_screen_info()

    def log_console(self, message):
        print(message)

    def on_window_state_changed(self, state):
        state_str = "Normal"
        if state & QtCore.Qt.WindowMinimized:
            state_str = "Minimized"
        elif state & QtCore.Qt.WindowMaximized:
            state_str = "Maximized"
        elif state & QtCore.Qt.WindowFullScreen:
            state_str = "FullScreen"

        message = f"[{QtCore.QDateTime.currentDateTime().toString('hh:mm:ss')}] Window state changed: {state_str}"
        self.log_console(message)
        self.update_screen_info()

    def on_screen_changed(self, screen):
        message = f"[{QtCore.QDateTime.currentDateTime().toString('hh:mm:ss')}] Window moved to screen: {screen.name()}"
        self.log_console(message)
        self.update_screen_info()

    def moveEvent(self, event):
        super().moveEvent(event)
        self.update_screen_info()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.log_console(
            f"[{QtCore.QDateTime.currentDateTime().toString('hh:mm:ss')}] Window resized to: {self.width()}x{self.height()}")
        self.update_screen_info()

    def changeEvent(self, event):
        super().changeEvent(event)
        if event.type() == QtCore.QEvent.WindowStateChange:
            self.on_window_state_changed(self.windowState())
            self.update_screen_info()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = WindowStateMonitor()
    window.show()

    sys.exit(app.exec())
