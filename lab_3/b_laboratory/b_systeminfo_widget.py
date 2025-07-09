"""
Реализовать виджет, который будет работать с потоком SystemInfo из модуля a_threads

Создавать форму можно как в ручную, так и с помощью программы Designer

Форма должна содержать:
1. поле для ввода времени задержки
2. поле для вывода информации о загрузке CPU
3. поле для вывода информации о загрузке RAM
4. поток необходимо запускать сразу при старте приложения
5. установку времени задержки сделать "горячей", т.е. поток должен сразу
реагировать на изменение времени задержки
"""
import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QFormLayout
)
from PySide6.QtCore import QThread, Signal, QObject, Slot
from PySide6.QtGui import QDoubleValidator
import psutil
import time


class SystemInfoWorker(QObject):

    cpu_updated = Signal(float)
    ram_updated = Signal(float, float, float)  # used, total, percent

    def __init__(self, interval=1.0):
        super().__init__()
        self.interval = interval
        self.is_running = True

    def set_interval(self, interval):

        self.interval = interval

    def stop(self):

        self.is_running = False

    def run(self):

        while self.is_running:
            # Получаем данные CPU
            cpu_percent = psutil.cpu_percent(interval=0.1)


            ram = psutil.virtual_memory()
            ram_used = ram.used / (1024 ** 3)  # в GB
            ram_total = ram.total / (1024 ** 3)  # в GB
            ram_percent = ram.percent


            self.cpu_updated.emit(cpu_percent)
            self.ram_updated.emit(ram_used, ram_total, ram_percent)


            delay = self.interval
            while delay > 0 and self.is_running:
                time.sleep(0.1)
                delay -= 0.1


class SystemMonitorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_thread()

    def setup_ui(self):

        self.setWindowTitle("System Monitor")
        self.resize(300, 150)

        layout = QVBoxLayout()
        form_layout = QFormLayout()


        self.interval_input = QLineEdit("1.0")
        self.interval_input.setValidator(QDoubleValidator(0.1, 10.0, 1))
        self.interval_input.textChanged.connect(self.update_interval)
        form_layout.addRow("Update Interval (sec):", self.interval_input)


        self.cpu_label = QLabel("0%")
        form_layout.addRow("CPU Usage:", self.cpu_label)


        self.ram_label = QLabel("0.0 GB / 0.0 GB (0%)")
        form_layout.addRow("RAM Usage:", self.ram_label)

        layout.addLayout(form_layout)
        self.setLayout(layout)

    def setup_thread(self):

        self.thread = QThread()
        self.worker = SystemInfoWorker(float(self.interval_input.text()))

        self.worker.moveToThread(self.thread)

        # Подключаем сигналы
        self.worker.cpu_updated.connect(self.update_cpu_display)
        self.worker.ram_updated.connect(self.update_ram_display)
        self.thread.started.connect(self.worker.run)

        # Запускаем поток
        self.thread.start()

    @Slot(str)
    def update_interval(self, text):

        try:
            interval = float(text)
            if interval > 0:
                self.worker.set_interval(interval)
        except ValueError:
            pass

    @Slot(float)
    def update_cpu_display(self, percent):

        self.cpu_label.setText(f"{percent:.1f}%")

    @Slot(float, float, float)
    def update_ram_display(self, used, total, percent):

        self.ram_label.setText(f"{used:.2f} GB / {total:.2f} GB ({percent:.1f}%)")

    def closeEvent(self, event):

        self.worker.stop()
        self.thread.quit()
        self.thread.wait()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = SystemMonitorWidget()
    widget.show()
    sys.exit(app.exec())