"""
Реализовать виджет, который будет работать с потоком WeatherHandler из модуля a_threads

Создавать форму можно как в ручную, так и с помощью программы Designer

Форма должна содержать:
1. поле для ввода широты и долготы (после запуска потока они должны блокироваться)
2. поле для ввода времени задержки (после запуска потока оно должно блокироваться)
3. поле для вывода информации о погоде в указанных координатах
4. поток необходимо запускать и останавливать при нажатии на кнопку
"""
import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                               QLabel, QLineEdit, QPushButton, QTextEdit)
from PySide6.QtCore import Qt
from a_threads import WeatherHandler


class WeatherWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Погодный монитор')
        self.setup_ui()
        self.weather_thread = None

    def setup_ui(self):

        main_layout = QVBoxLayout()


        coords_layout = QHBoxLayout()
        coords_layout.addWidget(QLabel('Широта:'))
        self.lat_edit = QLineEdit()
        self.lat_edit.setPlaceholderText('Например: 55.75')
        coords_layout.addWidget(self.lat_edit)

        coords_layout.addWidget(QLabel('Долгота:'))
        self.lon_edit = QLineEdit()
        self.lon_edit.setPlaceholderText('Например: 37.61')
        coords_layout.addWidget(self.lon_edit)

        main_layout.addLayout(coords_layout)


        delay_layout = QHBoxLayout()
        delay_layout.addWidget(QLabel('Интервал обновления (сек):'))
        self.delay_edit = QLineEdit()
        self.delay_edit.setPlaceholderText('Например: 10')
        delay_layout.addWidget(self.delay_edit)

        main_layout.addLayout(delay_layout)


        self.control_btn = QPushButton('Старт')
        self.control_btn.clicked.connect(self.toggle_thread)
        main_layout.addWidget(self.control_btn)


        self.weather_output = QTextEdit()
        self.weather_output.setReadOnly(True)
        self.weather_output.setPlaceholderText('Здесь будет отображаться информация о погоде...')
        main_layout.addWidget(self.weather_output)

        self.setLayout(main_layout)

    def toggle_thread(self):
        if self.weather_thread and self.weather_thread.isRunning():
            self.stop_thread()
        else:
            self.start_thread()

    def start_thread(self):

        try:
            lat = float(self.lat_edit.text())
            lon = float(self.lon_edit.text())
            delay = float(self.delay_edit.text())
        except ValueError:
            self.weather_output.setPlainText('Ошибка: введите корректные числовые значения')
            return

        self.weather_thread = WeatherHandler(lat, lon)
        self.weather_thread.setDelay(delay)


        self.weather_thread.weatherDataReceived.connect(self.update_weather_info)
        self.weather_thread.errorOccurred.connect(self.show_error)
        self.weather_thread.finished.connect(self.thread_finished)


        self.weather_thread._WeatherHandler__status = True
        self.weather_thread.start()


        self.control_btn.setText('Стоп')
        self.set_inputs_enabled(False)


        if self.weather_thread:
            self.weather_thread._WeatherHandler__status = False
            self.weather_thread.quit()
            self.weather_thread.wait()
            self.weather_thread = None


        self.control_btn.setText('Старт')
        self.set_inputs_enabled(True)

    def set_inputs_enabled(self, enabled):

        self.lat_edit.setEnabled(enabled)
        self.lon_edit.setEnabled(enabled)
        self.delay_edit.setEnabled(enabled)

    def update_weather_info(self, data):

        current = data.get('current_weather', {})

        weather_info = (
            f"Температура: {current.get('temperature', 'N/A')}°C\n"
            f"Скорость ветра: {current.get('windspeed', 'N/A')} км/ч\n"
            f"Направление ветра: {current.get('winddirection', 'N/A')}°\n"
            f"Код погоды: {current.get('weathercode', 'N/A')}\n"
            f"Время обновления: {current.get('time', 'N/A')}\n"
        )

        self.weather_output.setPlainText(weather_info)

    def show_error(self, error_msg):

        self.weather_output.setPlainText(f"Ошибка: {error_msg}")

    def thread_finished(self):

        self.control_btn.setText('Старт')
        self.set_inputs_enabled(True)

    def closeEvent(self, event):

        self.stop_thread()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = WeatherWidget()
    widget.resize(400, 300)
    widget.show()
    sys.exit(app.exec_())