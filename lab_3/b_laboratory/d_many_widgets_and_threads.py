"""
Реализовать окно, которое будет объединять в себе сразу два предыдущих виджета
"""
import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QTabWidget,
                               QWidget, QVBoxLayout)
from c_weatherapi_widget import WeatherWidget
from b_systeminfo_widget import SystemMonitorWidget


class CombinedMonitorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Комбинированный мониторинг")
        self.resize(800, 600)

        self.setup_ui()

    def setup_ui(self):

        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)


        tab_widget = QTabWidget()


        tab_widget.addTab(SystemMonitorWidget(), "Мониторинг системы")
        tab_widget.addTab(WeatherWidget(), "Погодный монитор")


        main_layout.addWidget(tab_widget)


        self.setCentralWidget(central_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CombinedMonitorWindow()
    window.show()
    sys.exit(app.exec_())
