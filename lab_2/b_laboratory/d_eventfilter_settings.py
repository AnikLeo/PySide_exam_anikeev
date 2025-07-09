"""
Реализация программу взаимодействия виджетов друг с другом:
Форма для приложения (ui/d_eventfilter_settings_form.ui)

Программа должна обладать следующим функционалом:

1. Добавить для dial возможность установки значений кнопками клавиатуры(+ и -),
   выводить новые значения в консоль

2. Соединить между собой QDial, QSlider, QLCDNumber
   (изменение значения в одном, изменяет значения в других)

3. Для QLCDNumber сделать отображение в различных системах счисления (oct, hex, bin, dec),
   изменять формат отображаемого значения в зависимости от выбранного в comboBox параметра.

4. Сохранять значение выбранного в comboBox режима отображения
   и значение LCDNumber в QSettings, при перезапуске программы выводить
   в него соответствующие значения
"""

import sys
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtUiTools import QUiLoader


class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()


        self.load_ui("ui/d_eventfilter_settings_form.ui")


        self.init_widgets()


        self.setup_connections()


        self.load_settings()


        self.installEventFilter(self)

    def load_ui(self, ui_file):
        loader = QUiLoader()
        file = QtCore.QFile(ui_file)
        if not file.open(QtCore.QFile.ReadOnly):
            print(f"Cannot open UI file: {file.errorString()}")
            sys.exit(-1)

        self.ui = loader.load(file)
        file.close()

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.ui)

    def init_widgets(self):

        self.dial = self.ui.findChild(QtWidgets.QDial, "dial")
        self.slider = self.ui.findChild(QtWidgets.QSlider, "horizontalSlider")
        self.lcd = self.ui.findChild(QtWidgets.QLCDNumber, "lcdNumber")
        self.combo = self.ui.findChild(QtWidgets.QComboBox, "comboBox")


        self.dial.setRange(0, 100)
        self.slider.setRange(0, 100)
        self.lcd.setDigitCount(5)


        self.combo.addItems(["DEC", "HEX", "OCT", "BIN"])


        self.dial.setValue(50)

    def setup_connections(self):

        self.dial.valueChanged.connect(self.update_all_widgets)
        self.slider.valueChanged.connect(self.update_all_widgets)


        self.combo.currentTextChanged.connect(self.update_lcd_format)


        self.update_all_widgets(self.dial.value())

    def update_all_widgets(self, value):

        self.dial.setValue(value)
        self.slider.setValue(value)
        self.lcd.display(value)


        self.update_lcd_format(self.combo.currentText())


        print(f"Current value: {value}")

    def update_lcd_format(self, format_str):
        value = self.dial.value()

        if format_str == "DEC":
            self.lcd.setDecMode()
            self.lcd.display(value)
        elif format_str == "HEX":
            self.lcd.setHexMode()
            self.lcd.display(value)
        elif format_str == "OCT":
            self.lcd.setOctMode()
            self.lcd.display(value)
        elif format_str == "BIN":

            self.lcd.setDecMode()
            self.lcd.display(bin(value))

    def eventFilter(self, obj, event):

        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Plus:
                self.dial.setValue(self.dial.value() + 1)
                return True
            elif event.key() == QtCore.Qt.Key_Minus:
                self.dial.setValue(self.dial.value() - 1)
                return True
        return super().eventFilter(obj, event)

    def load_settings(self):
        self.settings = QtCore.QSettings("MyCompany", "WidgetInteractionApp")


        value = self.settings.value("lcdValue", 50, int)
        format_str = self.settings.value("displayFormat", "DEC", str)


        self.dial.setValue(value)
        self.combo.setCurrentText(format_str)

        print(f"Loaded settings: value={value}, format={format_str}")

    def save_settings(self):

        self.settings.setValue("lcdValue", self.dial.value())
        self.settings.setValue("displayFormat", self.combo.currentText())

        print("Settings saved")

    def closeEvent(self, event):

        self.save_settings()
        super().closeEvent(event)




if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
