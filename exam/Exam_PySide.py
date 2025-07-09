import sys
import platform
import psutil
import time
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget,
                               QLabel, QTableWidget, QTableWidgetItem,
                               QComboBox, QTabWidget)
from PySide6.QtCore import QTimer, Qt


class SystemMonitor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Системный монитор")
        self.setGeometry(100, 100, 800, 600)


        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)


        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)


        self.general_tab = QWidget()
        self.general_layout = QVBoxLayout(self.general_tab)
        self.general_info_label = QLabel()
        self.general_info_label.setAlignment(Qt.AlignLeft)
        self.general_info_label.setStyleSheet("font-family: monospace;")
        self.general_layout.addWidget(self.general_info_label)
        self.tabs.addTab(self.general_tab, "Общая информация")


        self.processes_tab = QWidget()
        self.processes_layout = QVBoxLayout(self.processes_tab)
        self.processes_table = QTableWidget()
        self.processes_table.setColumnCount(4)
        self.processes_table.setHorizontalHeaderLabels(["PID", "Имя", "CPU %", "Память"])
        self.processes_layout.addWidget(self.processes_table)
        self.tabs.addTab(self.processes_tab, "Процессы")


        self.services_tab = QWidget()
        self.services_layout = QVBoxLayout(self.services_tab)
        self.services_table = QTableWidget()
        self.services_table.setColumnCount(3)
        self.services_table.setHorizontalHeaderLabels(["Имя", "Статус", "PID"])
        self.services_layout.addWidget(self.services_table)
        self.tabs.addTab(self.services_tab, "Службы")


        self.scheduler_tab = QWidget()
        self.scheduler_layout = QVBoxLayout(self.scheduler_tab)
        self.scheduler_table = QTableWidget()
        self.scheduler_table.setColumnCount(3)
        self.scheduler_table.setHorizontalHeaderLabels(["Имя", "Состояние", "Следующий запуск"])
        self.scheduler_layout.addWidget(self.scheduler_table)
        self.tabs.addTab(self.scheduler_tab, "Планировщик")


        self.refresh_combobox = QComboBox()
        self.refresh_combobox.addItems(["1 секунда", "5 секунд", "10 секунд", "30 секунд"])
        self.refresh_combobox.setCurrentIndex(1)
        self.refresh_combobox.currentIndexChanged.connect(self.change_refresh_interval)
        self.layout.addWidget(self.refresh_combobox)


        self.timer = QTimer()
        self.timer.timeout.connect(self.update_all_info)
        self.change_refresh_interval(1)  # Начинаем с 5 секунд


        self.update_all_info()

    def change_refresh_interval(self, index):
        intervals = [1000, 5000, 10000, 30000]
        self.timer.stop()
        self.timer.start(intervals[index])

    def update_all_info(self):
        self.update_general_info()
        self.update_processes()
        self.update_services()
        self.update_scheduler_tasks()

    def update_general_info(self):

        cpu_info = f"Процессор: {platform.processor()}\n"
        cpu_info += f"Ядер: {psutil.cpu_count(logical=False)}, потоков: {psutil.cpu_count()}\n"
        cpu_info += f"Текущая загрузка: {psutil.cpu_percent()}%\n\n"


        mem = psutil.virtual_memory()
        mem_info = f"Оперативная память: {self.format_bytes(mem.total)}\n"
        mem_info += f"Использовано: {self.format_bytes(mem.used)} ({mem.percent}%)\n"
        mem_info += f"Доступно: {self.format_bytes(mem.available)}\n\n"


        disks_info = ""
        partitions = psutil.disk_partitions()
        for partition in partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disks_info += f"Диск {partition.device}: {partition.mountpoint}\n"
                disks_info += f"Файловая система: {partition.fstype}\n"
                disks_info += f"Общий объем: {self.format_bytes(usage.total)}\n"
                disks_info += f"Использовано: {self.format_bytes(usage.used)} ({usage.percent}%)\n"
                disks_info += f"Свободно: {self.format_bytes(usage.free)}\n\n"
            except:
                continue

        full_info = cpu_info + mem_info + disks_info
        self.general_info_label.setText(full_info)

    def update_processes(self):
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
            try:
                processes.append([
                    proc.info['pid'],
                    proc.info['name'],
                    proc.info['cpu_percent'],
                    self.format_bytes(proc.info['memory_info'].rss)
                ])
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue


        processes.sort(key=lambda p: p[2], reverse=True)

        self.processes_table.setRowCount(len(processes))
        for row, proc in enumerate(processes):
            for col, value in enumerate(proc):
                item = QTableWidgetItem(str(value))
                self.processes_table.setItem(row, col, item)

    def update_services(self):
        services = []
        if platform.system() == "Windows":
            try:
                import win32service
                import win32con

                scm = win32service.OpenSCManager(None, None, win32con.SC_MANAGER_ENUMERATE_SERVICE)
                type_filter = win32service.SERVICE_WIN32
                state_filter = win32service.SERVICE_STATE_ALL

                statuses = win32service.EnumServicesStatus(scm, type_filter, state_filter)

                for short_name, display_name, status in statuses:
                    try:
                        status_str = {
                            win32service.SERVICE_STOPPED: "Остановлена",
                            win32service.SERVICE_START_PENDING: "Запускается",
                            win32service.SERVICE_STOP_PENDING: "Останавливается",
                            win32service.SERVICE_RUNNING: "Выполняется",
                            win32service.SERVICE_CONTINUE_PENDING: "Продолжается",
                            win32service.SERVICE_PAUSE_PENDING: "Приостанавливается",
                            win32service.SERVICE_PAUSED: "Приостановлена"
                        }.get(status[1], "Неизвестно")

                        # Получаем PID службы
                        service_handle = win32service.OpenService(scm, short_name, win32con.SERVICE_QUERY_STATUS)
                        status_info = win32service.QueryServiceStatusEx(service_handle)
                        pid = status_info['ProcessId'] if 'ProcessId' in status_info else "N/A"

                        services.append([display_name, status_str, pid])
                    except:
                        continue
            except ImportError:
                services.append(["Не удалось загрузить информацию о службах", "Требуется pywin32", "N/A"])
        else:
            services.append(["Информация о службах доступна только в Windows", "", ""])

        self.services_table.setRowCount(len(services))
        for row, service in enumerate(services):
            for col, value in enumerate(service):
                item = QTableWidgetItem(str(value))
                self.services_table.setItem(row, col, item)

    def update_scheduler_tasks(self):
        tasks = []
        if platform.system() == "Windows":
            try:
                import pythoncom
                from win32com.taskscheduler import taskscheduler

                pythoncom.CoInitialize()
                scheduler = taskscheduler.CTaskScheduler()
                scheduler.Connect()

                tasks_folder = scheduler.GetFolder("\\")
                tasks_list = tasks_folder.GetTasks(0)

                for task in tasks_list:
                    try:
                        name = task.GetName()
                        state = task.GetState()
                        next_run = task.GetNextRunTime()

                        state_str = {
                            0: "Неизвестно",
                            1: "Отключена",
                            2: "Очередь",
                            3: "Готова",
                            4: "Выполняется"
                        }.get(state, "Неизвестно")

                        tasks.append([name, state_str, str(next_run)])
                    except:
                        continue
            except ImportError:
                tasks.append(["Не удалось загрузить задачи планировщика", "Требуется pywin32", ""])
            except:
                tasks.append(["Ошибка при получении задач планировщика", "", ""])
        else:
            tasks.append(["Информация о задачах планировщика доступна только в Windows", "", ""])

        self.scheduler_table.setRowCount(len(tasks))
        for row, task in enumerate(tasks):
            for col, value in enumerate(task):
                item = QTableWidgetItem(str(value))
                self.scheduler_table.setItem(row, col, item)

    @staticmethod
    def format_bytes(size):

        power = 2 ** 10
        n = 0
        units = {0: 'B', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
        while size > power and n < len(units) - 1:
            size /= power
            n += 1
        return f"{size:.2f} {units[n]}"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    monitor = SystemMonitor()
    monitor.show()
    sys.exit(app.exec())