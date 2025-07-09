import sys
import psycopg2
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
                               QComboBox, QDateEdit, QMessageBox, QTabWidget, QDialog, QDialogButtonBox)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QIntValidator


class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Подключение к БД")
        self.setModal(True)

        layout = QVBoxLayout()

        self.host_input = QLineEdit("vpngw.avalon.ru")
        self.dbname_input = QLineEdit("dbSQL\DevDB2024_leoanik")
        self.user_input = QLineEdit("pguser")
        self.password_input = QLineEdit('Pa$$w0rd')
        self.password_input.setEchoMode(QLineEdit.Password)

        layout.addWidget(QLabel("Хост:"))
        layout.addWidget(self.host_input)
        layout.addWidget(QLabel("Имя базы данных:"))
        layout.addWidget(self.dbname_input)
        layout.addWidget(QLabel("Пользователь:"))
        layout.addWidget(self.user_input)
        layout.addWidget(QLabel("Пароль:"))
        layout.addWidget(self.password_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)
        self.setLayout(layout)

    def get_connection_params(self):
        return {
            'host': self.host_input.text(),
            'dbname': self.dbname_input.text(),
            'user': self.user_input.text(),
            'password': self.password_input.text()
        }


class MainWindow(QMainWindow):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.setWindowTitle("Управление кадрами")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QTabWidget()
        self.setCentralWidget(self.central_widget)

        # Создаем вкладки для разных таблиц
        self.create_employees_tab()
        self.create_departments_tab()
        self.create_positions_tab()
        self.create_staff_assignments_tab()
        self.create_orders_tab()

        # Обновляем данные при запуске
        self.refresh_all_tabs()

    def create_employees_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Таблица для отображения данных
        self.employees_table = QTableWidget()
        self.employees_table.setColumnCount(9)
        self.employees_table.setHorizontalHeaderLabels([
            "ID", "ФИО", "Дата рождения", "Адрес", "Телефон", "Email",
            "Дата найма", "Дата увольнения", "Приказ о найме"
        ])

        # Форма для добавления/редактирования
        form_layout = QVBoxLayout()

        self.emp_id_input = QLineEdit()
        self.emp_id_input.setPlaceholderText("Автозаполнение")
        self.emp_id_input.setReadOnly(True)
        self.emp_full_name_input = QLineEdit()
        self.emp_birth_date_input = QDateEdit()
        self.emp_birth_date_input.setCalendarPopup(True)
        self.emp_address_input = QLineEdit()
        self.emp_phone_input = QLineEdit()
        self.emp_email_input = QLineEdit()
        self.emp_hire_date_input = QDateEdit()
        self.emp_hire_date_input.setCalendarPopup(True)
        self.emp_terminate_date_input = QDateEdit()
        self.emp_terminate_date_input.setCalendarPopup(True)
        self.emp_terminate_date_input.setDate(QDate.fromString("", ""))  # Пустая дата
        self.emp_creation_order_combo = QComboBox()

        form_layout.addWidget(QLabel("ID:"))
        form_layout.addWidget(self.emp_id_input)
        form_layout.addWidget(QLabel("ФИО:"))
        form_layout.addWidget(self.emp_full_name_input)
        form_layout.addWidget(QLabel("Дата рождения:"))
        form_layout.addWidget(self.emp_birth_date_input)
        form_layout.addWidget(QLabel("Адрес:"))
        form_layout.addWidget(self.emp_address_input)
        form_layout.addWidget(QLabel("Телефон:"))
        form_layout.addWidget(self.emp_phone_input)
        form_layout.addWidget(QLabel("Email:"))
        form_layout.addWidget(self.emp_email_input)
        form_layout.addWidget(QLabel("Дата найма:"))
        form_layout.addWidget(self.emp_hire_date_input)
        form_layout.addWidget(QLabel("Дата увольнения:"))
        form_layout.addWidget(self.emp_terminate_date_input)
        form_layout.addWidget(QLabel("Приказ о найме:"))
        form_layout.addWidget(self.emp_creation_order_combo)

        # Кнопки управления
        button_layout = QHBoxLayout()
        self.add_emp_btn = QPushButton("Добавить")
        self.add_emp_btn.clicked.connect(self.add_employee)
        self.update_emp_btn = QPushButton("Обновить")
        self.update_emp_btn.clicked.connect(self.update_employee)
        self.delete_emp_btn = QPushButton("Удалить")
        self.delete_emp_btn.clicked.connect(self.delete_employee)
        self.clear_emp_btn = QPushButton("Очистить")
        self.clear_emp_btn.clicked.connect(self.clear_employee_form)

        button_layout.addWidget(self.add_emp_btn)
        button_layout.addWidget(self.update_emp_btn)
        button_layout.addWidget(self.delete_emp_btn)
        button_layout.addWidget(self.clear_emp_btn)

        layout.addWidget(self.employees_table)
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)

        tab.setLayout(layout)
        self.central_widget.addTab(tab, "Сотрудники")

        # Подключаем выбор строки в таблице
        self.employees_table.cellClicked.connect(self.load_employee_data)

    def create_departments_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.departments_table = QTableWidget()
        self.departments_table.setColumnCount(8)
        self.departments_table.setHorizontalHeaderLabels([
            "ID", "Название", "Родительский отдел", "Менеджер",
            "Дата открытия", "Дата закрытия", "Приказ создания", "Приказ закрытия"
        ])

        form_layout = QVBoxLayout()

        self.dept_id_input = QLineEdit()
        self.dept_id_input.setReadOnly(True)
        self.dept_name_input = QLineEdit()
        self.dept_parent_combo = QComboBox()
        self.dept_manager_combo = QComboBox()
        self.dept_opening_date_input = QDateEdit()
        self.dept_opening_date_input.setCalendarPopup(True)
        self.dept_close_date_input = QDateEdit()
        self.dept_close_date_input.setCalendarPopup(True)
        self.dept_close_date_input.setDate(QDate.fromString("", ""))
        self.dept_creation_order_combo = QComboBox()
        self.dept_close_order_combo = QComboBox()

        form_layout.addWidget(QLabel("ID:"))
        form_layout.addWidget(self.dept_id_input)
        form_layout.addWidget(QLabel("Название:"))
        form_layout.addWidget(self.dept_name_input)
        form_layout.addWidget(QLabel("Родительский отдел:"))
        form_layout.addWidget(self.dept_parent_combo)
        form_layout.addWidget(QLabel("Менеджер:"))
        form_layout.addWidget(self.dept_manager_combo)
        form_layout.addWidget(QLabel("Дата открытия:"))
        form_layout.addWidget(self.dept_opening_date_input)
        form_layout.addWidget(QLabel("Дата закрытия:"))
        form_layout.addWidget(self.dept_close_date_input)
        form_layout.addWidget(QLabel("Приказ создания:"))
        form_layout.addWidget(self.dept_creation_order_combo)
        form_layout.addWidget(QLabel("Приказ закрытия:"))
        form_layout.addWidget(self.dept_close_order_combo)

        button_layout = QHBoxLayout()
        self.add_dept_btn = QPushButton("Добавить")
        self.add_dept_btn.clicked.connect(self.add_department)
        self.update_dept_btn = QPushButton("Обновить")
        self.update_dept_btn.clicked.connect(self.update_department)
        self.delete_dept_btn = QPushButton("Удалить")
        self.delete_dept_btn.clicked.connect(self.delete_department)
        self.clear_dept_btn = QPushButton("Очистить")
        self.clear_dept_btn.clicked.connect(self.clear_department_form)

        button_layout.addWidget(self.add_dept_btn)
        button_layout.addWidget(self.update_dept_btn)
        button_layout.addWidget(self.delete_dept_btn)
        button_layout.addWidget(self.clear_dept_btn)

        layout.addWidget(self.departments_table)
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)

        tab.setLayout(layout)
        self.central_widget.addTab(tab, "Отделы")

        self.departments_table.cellClicked.connect(self.load_department_data)

    def create_positions_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.positions_table = QTableWidget()
        self.positions_table.setColumnCount(4)
        self.positions_table.setHorizontalHeaderLabels([
            "ID", "Название", "Мин. зарплата", "Макс. зарплата"
        ])

        form_layout = QVBoxLayout()

        self.pos_id_input = QLineEdit()
        self.pos_id_input.setReadOnly(True)
        self.pos_title_input = QLineEdit()
        self.pos_min_salary_input = QLineEdit()
        self.pos_min_salary_input.setValidator(QIntValidator(0, 999999))
        self.pos_max_salary_input = QLineEdit()
        self.pos_max_salary_input.setValidator(QIntValidator(0, 999999))

        form_layout.addWidget(QLabel("ID:"))
        form_layout.addWidget(self.pos_id_input)
        form_layout.addWidget(QLabel("Название:"))
        form_layout.addWidget(self.pos_title_input)
        form_layout.addWidget(QLabel("Мин. зарплата:"))
        form_layout.addWidget(self.pos_min_salary_input)
        form_layout.addWidget(QLabel("Макс. зарплата:"))
        form_layout.addWidget(self.pos_max_salary_input)

        button_layout = QHBoxLayout()
        self.add_pos_btn = QPushButton("Добавить")
        self.add_pos_btn.clicked.connect(self.add_position)
        self.update_pos_btn = QPushButton("Обновить")
        self.update_pos_btn.clicked.connect(self.update_position)
        self.delete_pos_btn = QPushButton("Удалить")
        self.delete_pos_btn.clicked.connect(self.delete_position)
        self.clear_pos_btn = QPushButton("Очистить")
        self.clear_pos_btn.clicked.connect(self.clear_position_form)

        button_layout.addWidget(self.add_pos_btn)
        button_layout.addWidget(self.update_pos_btn)
        button_layout.addWidget(self.delete_pos_btn)
        button_layout.addWidget(self.clear_pos_btn)

        layout.addWidget(self.positions_table)
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)

        tab.setLayout(layout)
        self.central_widget.addTab(tab, "Должности")

        self.positions_table.cellClicked.connect(self.load_position_data)

    def create_staff_assignments_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.assignments_table = QTableWidget()
        self.assignments_table.setColumnCount(9)
        self.assignments_table.setHorizontalHeaderLabels([
            "ID", "Сотрудник", "Отдел", "Должность", "Ставка",
            "Зарплата", "Дата назначения", "Дата снятия", "Приказ назначения"
        ])

        form_layout = QVBoxLayout()

        self.assign_id_input = QLineEdit()
        self.assign_id_input.setReadOnly(True)
        self.assign_employee_combo = QComboBox()
        self.assign_department_combo = QComboBox()
        self.assign_position_combo = QComboBox()
        self.assign_rate_input = QLineEdit()
        self.assign_rate_input.setValidator(QIntValidator(0, 100))
        self.assign_salary_input = QLineEdit()
        self.assign_salary_input.setValidator(QIntValidator(0, 999999))
        self.assign_date_input = QDateEdit()
        self.assign_date_input.setCalendarPopup(True)
        self.assign_removal_date_input = QDateEdit()
        self.assign_removal_date_input.setCalendarPopup(True)
        self.assign_removal_date_input.setDate(QDate.fromString("", ""))
        self.assign_order_combo = QComboBox()

        form_layout.addWidget(QLabel("ID:"))
        form_layout.addWidget(self.assign_id_input)
        form_layout.addWidget(QLabel("Сотрудник:"))
        form_layout.addWidget(self.assign_employee_combo)
        form_layout.addWidget(QLabel("Отдел:"))
        form_layout.addWidget(self.assign_department_combo)
        form_layout.addWidget(QLabel("Должность:"))
        form_layout.addWidget(self.assign_position_combo)
        form_layout.addWidget(QLabel("Ставка (%):"))
        form_layout.addWidget(self.assign_rate_input)
        form_layout.addWidget(QLabel("Зарплата:"))
        form_layout.addWidget(self.assign_salary_input)
        form_layout.addWidget(QLabel("Дата назначения:"))
        form_layout.addWidget(self.assign_date_input)
        form_layout.addWidget(QLabel("Дата снятия:"))
        form_layout.addWidget(self.assign_removal_date_input)
        form_layout.addWidget(QLabel("Приказ назначения:"))
        form_layout.addWidget(self.assign_order_combo)

        button_layout = QHBoxLayout()
        self.add_assign_btn = QPushButton("Добавить")
        self.add_assign_btn.clicked.connect(self.add_assignment)
        self.update_assign_btn = QPushButton("Обновить")
        self.update_assign_btn.clicked.connect(self.update_assignment)
        self.delete_assign_btn = QPushButton("Удалить")
        self.delete_assign_btn.clicked.connect(self.delete_assignment)
        self.clear_assign_btn = QPushButton("Очистить")
        self.clear_assign_btn.clicked.connect(self.clear_assignment_form)

        button_layout.addWidget(self.add_assign_btn)
        button_layout.addWidget(self.update_assign_btn)
        button_layout.addWidget(self.delete_assign_btn)
        button_layout.addWidget(self.clear_assign_btn)

        layout.addWidget(self.assignments_table)
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)

        tab.setLayout(layout)
        self.central_widget.addTab(tab, "Назначения")

        self.assignments_table.cellClicked.connect(self.load_assignment_data)

    def create_orders_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(5)
        self.orders_table.setHorizontalHeaderLabels([
            "ID", "Название", "Дата", "Номер", "Подписант"
        ])

        form_layout = QVBoxLayout()

        self.order_id_input = QLineEdit()
        self.order_id_input.setReadOnly(True)
        self.order_title_input = QLineEdit()
        self.order_date_input = QDateEdit()
        self.order_date_input.setCalendarPopup(True)
        self.order_number_input = QLineEdit()
        self.order_number_input.setValidator(QIntValidator(0, 999999))
        self.order_signer_combo = QComboBox()

        form_layout.addWidget(QLabel("ID:"))
        form_layout.addWidget(self.order_id_input)
        form_layout.addWidget(QLabel("Название:"))
        form_layout.addWidget(self.order_title_input)
        form_layout.addWidget(QLabel("Дата:"))
        form_layout.addWidget(self.order_date_input)
        form_layout.addWidget(QLabel("Номер:"))
        form_layout.addWidget(self.order_number_input)
        form_layout.addWidget(QLabel("Подписант:"))
        form_layout.addWidget(self.order_signer_combo)

        button_layout = QHBoxLayout()
        self.add_order_btn = QPushButton("Добавить")
        self.add_order_btn.clicked.connect(self.add_order)
        self.update_order_btn = QPushButton("Обновить")
        self.update_order_btn.clicked.connect(self.update_order)
        self.delete_order_btn = QPushButton("Удалить")
        self.delete_order_btn.clicked.connect(self.delete_order)
        self.clear_order_btn = QPushButton("Очистить")
        self.clear_order_btn.clicked.connect(self.clear_order_form)

        button_layout.addWidget(self.add_order_btn)
        button_layout.addWidget(self.update_order_btn)
        button_layout.addWidget(self.delete_order_btn)
        button_layout.addWidget(self.clear_order_btn)

        layout.addWidget(self.orders_table)
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)

        tab.setLayout(layout)
        self.central_widget.addTab(tab, "Приказы")

        self.orders_table.cellClicked.connect(self.load_order_data)

    def refresh_all_tabs(self):
        self.refresh_employees()
        self.refresh_departments()
        self.refresh_positions()
        self.refresh_assignments()
        self.refresh_orders()

        # Обновляем комбобоксы
        self.update_combo_boxes()

    def update_combo_boxes(self):
        # Обновляем комбобоксы для сотрудников
        self.emp_creation_order_combo.clear()
        self.dept_manager_combo.clear()
        self.assign_employee_combo.clear()
        self.order_signer_combo.clear()

        self.cursor.execute("SELECT order_id, title FROM orders")
        orders = self.cursor.fetchall()
        for order_id, title in orders:
            self.emp_creation_order_combo.addItem(f"{title} (ID: {order_id})", order_id)
            self.dept_creation_order_combo.addItem(f"{title} (ID: {order_id})", order_id)
            self.dept_close_order_combo.addItem(f"{title} (ID: {order_id})", order_id)
            self.assign_order_combo.addItem(f"{title} (ID: {order_id})", order_id)

        self.cursor.execute("SELECT employee_id, full_name FROM employees")
        employees = self.cursor.fetchall()
        for emp_id, name in employees:
            self.dept_manager_combo.addItem(f"{name} (ID: {emp_id})", emp_id)
            self.assign_employee_combo.addItem(f"{name} (ID: {emp_id})", emp_id)
            self.order_signer_combo.addItem(f"{name} (ID: {emp_id})", emp_id)

        self.cursor.execute("SELECT department_id, name FROM departments")
        departments = self.cursor.fetchall()
        self.dept_parent_combo.clear()
        self.dept_parent_combo.addItem("Нет", None)
        self.assign_department_combo.clear()
        for dept_id, name in departments:
            self.dept_parent_combo.addItem(f"{name} (ID: {dept_id})", dept_id)
            self.assign_department_combo.addItem(f"{name} (ID: {dept_id})", dept_id)

        self.cursor.execute("SELECT position_id, title FROM positions")
        positions = self.cursor.fetchall()
        self.assign_position_combo.clear()
        for pos_id, title in positions:
            self.assign_position_combo.addItem(f"{title} (ID: {pos_id})", pos_id)

    # Методы для работы с сотрудниками
    def refresh_employees(self):
        self.cursor.execute("""
                            SELECT employee_id,
                                   full_name,
                                   birth_date,
                                   registration_address,
                                   phone,
                                   email,
                                   hire_date,
                                   terminate_date,
                                   creation_order_id
                            FROM employees
                            """)
        employees = self.cursor.fetchall()

        self.employees_table.setRowCount(len(employees))
        for row, emp in enumerate(employees):
            for col, value in enumerate(emp):
                item = QTableWidgetItem(str(value) if value is not None else "")
                self.employees_table.setItem(row, col, item)

    def load_employee_data(self, row):
        emp_id = self.employees_table.item(row, 0).text()
        self.cursor.execute("""
                            SELECT employee_id,
                                   full_name,
                                   birth_date,
                                   registration_address,
                                   phone,
                                   email,
                                   hire_date,
                                   terminate_date,
                                   creation_order_id
                            FROM employees
                            WHERE employee_id = %s
                            """, (emp_id,))
        emp = self.cursor.fetchone()

        self.emp_id_input.setText(str(emp[0]))
        self.emp_full_name_input.setText(emp[1])
        self.emp_birth_date_input.setDate(QDate.fromString(emp[2].isoformat(), "yyyy-MM-dd"))
        self.emp_address_input.setText(emp[3])
        self.emp_phone_input.setText(emp[4] if emp[4] else "")
        self.emp_email_input.setText(emp[5] if emp[5] else "")
        self.emp_hire_date_input.setDate(QDate.fromString(emp[6].isoformat(), "yyyy-MM-dd"))

        if emp[7]:
            self.emp_terminate_date_input.setDate(QDate.fromString(emp[7].isoformat(), "yyyy-MM-dd"))
        else:
            self.emp_terminate_date_input.setDate(QDate.fromString("", ""))

        # Устанавливаем правильный приказ в комбобоксе
        for i in range(self.emp_creation_order_combo.count()):
            if self.emp_creation_order_combo.itemData(i) == emp[8]:
                self.emp_creation_order_combo.setCurrentIndex(i)
                break

    def add_employee(self):
        full_name = self.emp_full_name_input.text()
        birth_date = self.emp_birth_date_input.date().toString("yyyy-MM-dd")
        address = self.emp_address_input.text()
        phone = self.emp_phone_input.text() or None
        email = self.emp_email_input.text() or None
        hire_date = self.emp_hire_date_input.date().toString("yyyy-MM-dd")
        terminate_date = self.emp_terminate_date_input.date().toString(
            "yyyy-MM-dd") if self.emp_terminate_date_input.date().isValid() else None
        creation_order_id = self.emp_creation_order_combo.currentData()

        try:
            self.cursor.execute("""
                                INSERT INTO employees (full_name, birth_date, registration_address,
                                                       phone, email, hire_date, terminate_date, creation_order_id)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING employee_id
                                """, (full_name, birth_date, address, phone, email, hire_date, terminate_date,
                                      creation_order_id))

            emp_id = self.cursor.fetchone()[0]
            self.connection.commit()
            QMessageBox.information(self, "Успех", f"Сотрудник добавлен с ID: {emp_id}")
            self.refresh_employees()
            self.update_combo_boxes()
            self.clear_employee_form()
        except Exception as e:
            self.connection.rollback()
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить сотрудника: {str(e)}")

    def update_employee(self):
        emp_id = self.emp_id_input.text()
        if not emp_id:
            QMessageBox.warning(self, "Ошибка", "Выберите сотрудника для обновления")
            return

        full_name = self.emp_full_name_input.text()
        birth_date = self.emp_birth_date_input.date().toString("yyyy-MM-dd")
        address = self.emp_address_input.text()
        phone = self.emp_phone_input.text() or None
        email = self.emp_email_input.text() or None
        hire_date = self.emp_hire_date_input.date().toString("yyyy-MM-dd")
        terminate_date = self.emp_terminate_date_input.date().toString(
            "yyyy-MM-dd") if self.emp_terminate_date_input.date().isValid() else None
        creation_order_id = self.emp_creation_order_combo.currentData()

        try:
            self.cursor.execute("""
                                UPDATE employees
                                SET full_name            = %s,
                                    birth_date           = %s,
                                    registration_address = %s,
                                    phone                = %s,
                                    email                = %s,
                                    hire_date            = %s,
                                    terminate_date       = %s,
                                    creation_order_id    = %s
                                WHERE employee_id = %s
                                """, (full_name, birth_date, address, phone, email,
                                      hire_date, terminate_date, creation_order_id, emp_id))

            self.connection.commit()
            QMessageBox.information(self, "Успех", "Данные сотрудника обновлены")
            self.refresh_employees()
            self.update_combo_boxes()
        except Exception as e:
            self.connection.rollback()
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить сотрудника: {str(e)}")

    def delete_employee(self):
        emp_id = self.emp_id_input.text()
        if not emp_id:
            QMessageBox.warning(self, "Ошибка", "Выберите сотрудника для удаления")
            return

        reply = QMessageBox.question(
            self, 'Подтверждение',
            'Вы уверены, что хотите удалить этого сотрудника? Это может привести к удалению связанных записей.',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                self.cursor.execute("DELETE FROM employees WHERE employee_id = %s", (emp_id,))
                self.connection.commit()
                QMessageBox.information(self, "Успех", "Сотрудник удален")
                self.refresh_employees()
                self.update_combo_boxes()
                self.clear_employee_form()
            except Exception as e:
                self.connection.rollback()
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить сотрудника: {str(e)}")

    def clear_employee_form(self):
        self.emp_id_input.clear()
        self.emp_full_name_input.clear()
        self.emp_birth_date_input.setDate(QDate.currentDate())
        self.emp_address_input.clear()
        self.emp_phone_input.clear()
        self.emp_email_input.clear()
        self.emp_hire_date_input.setDate(QDate.currentDate())
        self.emp_terminate_date_input.setDate(QDate.fromString("", ""))
        self.emp_creation_order_combo.setCurrentIndex(0)

    # Методы для работы с отделами
    def refresh_departments(self):
        self.cursor.execute("""
                            SELECT d.department_id,
                                   d.name,
                                   parent.name as parent_name,
                                   e.full_name as manager_name,
                                   d.opening_date,
                                   d.close_date,
                                   d.creation_order_id,
                                   d.close_order_id
                            FROM departments d
                                     LEFT JOIN departments parent ON d.parent_department_id = parent.department_id
                                     LEFT JOIN employees e ON d.manager_id = e.employee_id
                            """)
        departments = self.cursor.fetchall()

        self.departments_table.setRowCount(len(departments))
        for row, dept in enumerate(departments):
            for col, value in enumerate(dept):
                item = QTableWidgetItem(str(value) if value is not None else "")
                self.departments_table.setItem(row, col, item)

    def load_department_data(self, row):
        dept_id = self.departments_table.item(row, 0).text()
        self.cursor.execute("""
                            SELECT department_id,
                                   name,
                                   parent_department_id,
                                   manager_id,
                                   opening_date,
                                   close_date,
                                   creation_order_id,
                                   close_order_id
                            FROM departments
                            WHERE department_id = %s
                            """, (dept_id,))
        dept = self.cursor.fetchone()

        self.dept_id_input.setText(str(dept[0]))
        self.dept_name_input.setText(dept[1])

        # Устанавливаем родительский отдел
        for i in range(self.dept_parent_combo.count()):
            if self.dept_parent_combo.itemData(i) == dept[2]:
                self.dept_parent_combo.setCurrentIndex(i)
                break

        # Устанавливаем менеджера
        for i in range(self.dept_manager_combo.count()):
            if self.dept_manager_combo.itemData(i) == dept[3]:
                self.dept_manager_combo.setCurrentIndex(i)
                break

        self.dept_opening_date_input.setDate(QDate.fromString(dept[4].isoformat(), "yyyy-MM-dd"))

        if dept[5]:
            self.dept_close_date_input.setDate(QDate.fromString(dept[5].isoformat(), "yyyy-MM-dd"))
        else:
            self.dept_close_date_input.setDate(QDate.fromString("", ""))

        # Устанавливаем приказы
        for i in range(self.dept_creation_order_combo.count()):
            if self.dept_creation_order_combo.itemData(i) == dept[6]:
                self.dept_creation_order_combo.setCurrentIndex(i)
                break

        for i in range(self.dept_close_order_combo.count()):
            if self.dept_close_order_combo.itemData(i) == dept[7]:
                self.dept_close_order_combo.setCurrentIndex(i)
                break

    def add_department(self):
        name = self.dept_name_input.text()
        parent_id = self.dept_parent_combo.currentData()
        manager_id = self.dept_manager_combo.currentData()
        opening_date = self.dept_opening_date_input.date().toString("yyyy-MM-dd")
        close_date = self.dept_close_date_input.date().toString(
            "yyyy-MM-dd") if self.dept_close_date_input.date().isValid() else None
        creation_order_id = self.dept_creation_order_combo.currentData()
        close_order_id = self.dept_close_order_combo.currentData() if self.dept_close_order_combo.currentIndex() > 0 else None

        try:
            self.cursor.execute("""
                                INSERT INTO departments (name, parent_department_id, manager_id,
                                                         opening_date, close_date, creation_order_id, close_order_id)
                                VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING department_id
                                """, (name, parent_id, manager_id, opening_date, close_date, creation_order_id,
                                      close_order_id))

            dept_id = self.cursor.fetchone()[0]
            self.connection.commit()
            QMessageBox.information(self, "Успех", f"Отдел добавлен с ID: {dept_id}")
            self.refresh_departments()
            self.update_combo_boxes()
            self.clear_department_form()
        except Exception as e:
            self.connection.rollback()
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить отдел: {str(e)}")

    def update_department(self):
        dept_id = self.dept_id_input.text()
        if not dept_id:
            QMessageBox.warning(self, "Ошибка", "Выберите отдел для обновления")
            return

        name = self.dept_name_input.text()
        parent_id = self.dept_parent_combo.currentData()
        manager_id = self.dept_manager_combo.currentData()
        opening_date = self.dept_opening_date_input.date().toString("yyyy-MM-dd")
        close_date = self.dept_close_date_input.date().toString(
            "yyyy-MM-dd") if self.dept_close_date_input.date().isValid() else None
        creation_order_id = self.dept_creation_order_combo.currentData()
        close_order_id = self.dept_close_order_combo.currentData() if self.dept_close_order_combo.currentIndex() > 0 else None

        try:
            self.cursor.execute("""
                                UPDATE departments
                                SET name                 = %s,
                                    parent_department_id = %s,
                                    manager_id           = %s,
                                    opening_date         = %s,
                                    close_date           = %s,
                                    creation_order_id    = %s,
                                    close_order_id       = %s
                                WHERE department_id = %s
                                """, (name, parent_id, manager_id, opening_date, close_date,
                                      creation_order_id, close_order_id, dept_id))

            self.connection.commit()
            QMessageBox.information(self, "Успех", "Данные отдела обновлены")
            self.refresh_departments()
            self.update_combo_boxes()
        except Exception as e:
            self.connection.rollback()
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить отдел: {str(e)}")

    def delete_department(self):
        dept_id = self.dept_id_input.text()
        if not dept_id:
            QMessageBox.warning(self, "Ошибка", "Выберите отдел для удаления")
            return

        reply = QMessageBox.question(
            self, 'Подтверждение',
            'Вы уверены, что хотите удалить этот отдел? Это может привести к удалению связанных записей.',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                self.cursor.execute("DELETE FROM departments WHERE department_id = %s", (dept_id,))
                self.connection.commit()
                QMessageBox.information(self, "Успех", "Отдел удален")
                self.refresh_departments()
                self.update_combo_boxes()
                self.clear_department_form()
            except Exception as e:
                self.connection.rollback()
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить отдел: {str(e)}")

    def clear_department_form(self):
        self.dept_id_input.clear()
        self.dept_name_input.clear()
        self.dept_parent_combo.setCurrentIndex(0)
        self.dept_manager_combo.setCurrentIndex(0)
        self.dept_opening_date_input.setDate(QDate.currentDate())
        self.dept_close_date_input.setDate(QDate.fromString("", ""))
        self.dept_creation_order_combo.setCurrentIndex(0)
        self.dept_close_order_combo.setCurrentIndex(0)

    # Методы для работы с должностями
    def refresh_positions(self):
        self.cursor.execute("SELECT position_id, title, min_salary, max_salary FROM positions")
        positions = self.cursor.fetchall()

        self.positions_table.setRowCount(len(positions))
        for row, pos in enumerate(positions):
            for col, value in enumerate(pos):
                item = QTableWidgetItem(str(value) if value is not None else "")
                self.positions_table.setItem(row, col, item)

    def load_position_data(self, row):
        pos_id = self.positions_table.item(row, 0).text()
        self.cursor.execute("""
                            SELECT position_id, title, min_salary, max_salary
                            FROM positions
                            WHERE position_id = %s
                            """, (pos_id,))
        pos = self.cursor.fetchone()

        self.pos_id_input.setText(str(pos[0]))
        self.pos_title_input.setText(pos[1])
        self.pos_min_salary_input.setText(str(pos[2]))
        self.pos_max_salary_input.setText(str(pos[3]))

    def add_position(self):
        title = self.pos_title_input.text()
        min_salary = self.pos_min_salary_input.text()
        max_salary = self.pos_max_salary_input.text()

        try:
            self.cursor.execute("""
                                INSERT INTO positions (title, min_salary, max_salary)
                                VALUES (%s, %s, %s) RETURNING position_id
                                """, (title, min_salary, max_salary))

            pos_id = self.cursor.fetchone()[0]
            self.connection.commit()
            QMessageBox.information(self, "Успех", f"Должность добавлена с ID: {pos_id}")
            self.refresh_positions()
            self.update_combo_boxes()
            self.clear_position_form()
        except Exception as e:
            self.connection.rollback()
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить должность: {str(e)}")

    def update_position(self):
        pos_id = self.pos_id_input.text()
        if not pos_id:
            QMessageBox.warning(self, "Ошибка", "Выберите должность для обновления")
            return

        title = self.pos_title_input.text()
        min_salary = self.pos_min_salary_input.text()
        max_salary = self.pos_max_salary_input.text()

        try:
            self.cursor.execute("""
                                UPDATE positions
                                SET title      = %s,
                                    min_salary = %s,
                                    max_salary = %s
                                WHERE position_id = %s
                                """, (title, min_salary, max_salary, pos_id))

            self.connection.commit()
            QMessageBox.information(self, "Успех", "Данные должности обновлены")
            self.refresh_positions()
            self.update_combo_boxes()
        except Exception as e:
            self.connection.rollback()
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить должность: {str(e)}")

    def delete_position(self):
        pos_id = self.pos_id_input.text()
        if not pos_id:
            QMessageBox.warning(self, "Ошибка", "Выберите должность для удаления")
            return

        reply = QMessageBox.question(
            self, 'Подтверждение',
            'Вы уверены, что хотите удалить эту должность? Это может привести к удалению связанных записей.',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                self.cursor.execute("DELETE FROM positions WHERE position_id = %s", (pos_id,))
                self.connection.commit()
                QMessageBox.information(self, "Успех", "Должность удалена")
                self.refresh_positions()
                self.update_combo_boxes()
                self.clear_position_form()
            except Exception as e:
                self.connection.rollback()
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить должность: {str(e)}")

    def clear_position_form(self):
        self.pos_id_input.clear()
        self.pos_title_input.clear()
        self.pos_min_salary_input.clear()
        self.pos_max_salary_input.clear()

    # Методы для работы с назначениями
    def refresh_assignments(self):
        self.cursor.execute("""
                            SELECT sa.assignment_id,
                                   e.full_name as employee_name,
                                   d.name      as department_name,
                                   p.title     as position_title,
                                   sa.employment_rate,
                                   sa.salary,
                                   sa.assignment_date,
                                   sa.removal_date,
                                   sa.assignment_order_id
                            FROM staff_assignments sa
                                     JOIN employees e ON sa.employee_id = e.employee_id
                                     JOIN departments d ON sa.department_id = d.department_id
                                     JOIN positions p ON sa.position_id = p.position_id
                            """)
        assignments = self.cursor.fetchall()

        self.assignments_table.setRowCount(len(assignments))
        for row, assign in enumerate(assignments):
            for col, value in enumerate(assign):
                item = QTableWidgetItem(str(value) if value is not None else "")
                self.assignments_table.setItem(row, col, item)

    def load_assignment_data(self, row):
        assign_id = self.assignments_table.item(row, 0).text()
        self.cursor.execute("""
                            SELECT assignment_id,
                                   employee_id,
                                   department_id,
                                   position_id,
                                   employment_rate,
                                   salary,
                                   assignment_date,
                                   removal_date,
                                   assignment_order_id
                            FROM staff_assignments
                            WHERE assignment_id = %s
                            """, (assign_id,))
        assign = self.cursor.fetchone()

        self.assign_id_input.setText(str(assign[0]))

        # Устанавливаем сотрудника
        for i in range(self.assign_employee_combo.count()):
            if self.assign_employee_combo.itemData(i) == assign[1]:
                self.assign_employee_combo.setCurrentIndex(i)
                break

        # Устанавливаем отдел
        for i in range(self.assign_department_combo.count()):
            if self.assign_department_combo.itemData(i) == assign[2]:
                self.assign_department_combo.setCurrentIndex(i)
                break

        # Устанавливаем должность
        for i in range(self.assign_position_combo.count()):
            if self.assign_position_combo.itemData(i) == assign[3]:
                self.assign_position_combo.setCurrentIndex(i)
                break

        self.assign_rate_input.setText(str(assign[4]))
        self.assign_salary_input.setText(str(assign[5]))
        self.assign_date_input.setDate(QDate.fromString(assign[6].isoformat(), "yyyy-MM-dd"))

        if assign[7]:
            self.assign_removal_date_input.setDate(QDate.fromString(assign[7].isoformat(), "yyyy-MM-dd"))
        else:
            self.assign_removal_date_input.setDate(QDate.fromString("", ""))

        # Устанавливаем приказ
        for i in range(self.assign_order_combo.count()):
            if self.assign_order_combo.itemData(i) == assign[8]:
                self.assign_order_combo.setCurrentIndex(i)
                break

    def add_assignment(self):
        employee_id = self.assign_employee_combo.currentData()
        department_id = self.assign_department_combo.currentData()
        position_id = self.assign_position_combo.currentData()
        rate = self.assign_rate_input.text()
        salary = self.assign_salary_input.text()
        assign_date = self.assign_date_input.date().toString("yyyy-MM-dd")
        removal_date = self.assign_removal_date_input.date().toString(
            "yyyy-MM-dd") if self.assign_removal_date_input.date().isValid() else None
        order_id = self.assign_order_combo.currentData()

        try:
            self.cursor.execute("""
                                INSERT INTO staff_assignments (employee_id, department_id, position_id,
                                                               employment_rate, salary, assignment_date,
                                                               removal_date, assignment_order_id)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING assignment_id
                                """, (employee_id, department_id, position_id, rate, salary,
                                      assign_date, removal_date, order_id))

            assign_id = self.cursor.fetchone()[0]
            self.connection.commit()
            QMessageBox.information(self, "Успех", f"Назначение добавлено с ID: {assign_id}")
            self.refresh_assignments()
            self.clear_assignment_form()
        except Exception as e:
            self.connection.rollback()
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить назначение: {str(e)}")

    def update_assignment(self):
        assign_id = self.assign_id_input.text()
        if not assign_id:
            QMessageBox.warning(self, "Ошибка", "Выберите назначение для обновления")
            return

        employee_id = self.assign_employee_combo.currentData()
        department_id = self.assign_department_combo.currentData()
        position_id = self.assign_position_combo.currentData()
        rate = self.assign_rate_input.text()
        salary = self.assign_salary_input.text()
        assign_date = self.assign_date_input.date().toString("yyyy-MM-dd")
        removal_date = self.assign_removal_date_input.date().toString(
            "yyyy-MM-dd") if self.assign_removal_date_input.date().isValid() else None
        order_id = self.assign_order_combo.currentData()

        try:
            self.cursor.execute("""
                                UPDATE staff_assignments
                                SET employee_id         = %s,
                                    department_id       = %s,
                                    position_id         = %s,
                                    employment_rate     = %s,
                                    salary              = %s,
                                    assignment_date     = %s,
                                    removal_date        = %s,
                                    assignment_order_id = %s
                                WHERE assignment_id = %s
                                """, (employee_id, department_id, position_id, rate, salary,
                                      assign_date, removal_date, order_id, assign_id))

            self.connection.commit()
            QMessageBox.information(self, "Успех", "Данные назначения обновлены")
            self.refresh_assignments()
        except Exception as e:
            self.connection.rollback()
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить назначение: {str(e)}")

    def delete_assignment(self):
        assign_id = self.assign_id_input.text()
        if not assign_id:
            QMessageBox.warning(self, "Ошибка", "Выберите назначение для удаления")
            return

        reply = QMessageBox.question(
            self, 'Подтверждение',
            'Вы уверены, что хотите удалить это назначение?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                self.cursor.execute("DELETE FROM staff_assignments WHERE assignment_id = %s", (assign_id,))
                self.connection.commit()
                QMessageBox.information(self, "Успех", "Назначение удалено")
                self.refresh_assignments()
                self.clear_assignment_form()
            except Exception as e:
                self.connection.rollback()
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить назначение: {str(e)}")

    def clear_assignment_form(self):
        self.assign_id_input.clear()
        self.assign_employee_combo.setCurrentIndex(0)
        self.assign_department_combo.setCurrentIndex(0)
        self.assign_position_combo.setCurrentIndex(0)
        self.assign_rate_input.clear()
        self.assign_salary_input.clear()
        self.assign_date_input.setDate(QDate.currentDate())
        self.assign_removal_date_input.setDate(QDate.fromString("", ""))
        self.assign_order_combo.setCurrentIndex(0)

    # Методы для работы с приказами
    def refresh_orders(self):
        self.cursor.execute("""
                            SELECT o.order_id,
                                   o.title,
                                   o.order_date,
                                   o.order_number,
                                   e.full_name as signer_name
                            FROM orders o
                                     LEFT JOIN employees e ON o.signer_id = e.employee_id
                            """)
        orders = self.cursor.fetchall()

        self.orders_table.setRowCount(len(orders))
        for row, order in enumerate(orders):
            for col, value in enumerate(order):
                item = QTableWidgetItem(str(value) if value is not None else "")
                self.orders_table.setItem(row, col, item)

    def load_order_data(self, row):
        order_id = self.orders_table.item(row, 0).text()
        self.cursor.execute("""
                            SELECT order_id, title, order_date, order_number, signer_id
                            FROM orders
                            WHERE order_id = %s
                            """, (order_id,))
        order = self.cursor.fetchone()

        self.order_id_input.setText(str(order[0]))
        self.order_title_input.setText(order[1])
        self.order_date_input.setDate(QDate.fromString(order[2].isoformat(), "yyyy-MM-dd"))
        self.order_number_input.setText(str(order[3]))

        # Устанавливаем подписанта
        for i in range(self.order_signer_combo.count()):
            if self.order_signer_combo.itemData(i) == order[4]:
                self.order_signer_combo.setCurrentIndex(i)
                break

    def add_order(self):
        title = self.order_title_input.text()
        order_date = self.order_date_input.date().toString("yyyy-MM-dd")
        order_number = self.order_number_input.text()
        signer_id = self.order_signer_combo.currentData()

        try:
            self.cursor.execute("""
                                INSERT INTO orders (title, order_date, order_number, signer_id)
                                VALUES (%s, %s, %s, %s) RETURNING order_id
                                """, (title, order_date, order_number, signer_id))

            order_id = self.cursor.fetchone()[0]
            self.connection.commit()
            QMessageBox.information(self, "Успех", f"Приказ добавлен с ID: {order_id}")
            self.refresh_orders()
            self.update_combo_boxes()
            self.clear_order_form()
        except Exception as e:
            self.connection.rollback()
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить приказ: {str(e)}")

    def update_order(self):
        order_id = self.order_id_input.text()
        if not order_id:
            QMessageBox.warning(self, "Ошибка", "Выберите приказ для обновления")
            return

        title = self.order_title_input.text()
        order_date = self.order_date_input.date().toString("yyyy-MM-dd")
        order_number = self.order_number_input.text()
        signer_id = self.order_signer_combo.currentData()

        try:
            self.cursor.execute("""
                                UPDATE orders
                                SET title        = %s,
                                    order_date   = %s,
                                    order_number = %s,
                                    signer_id    = %s
                                WHERE order_id = %s
                                """, (title, order_date, order_number, signer_id, order_id))

            self.connection.commit()
            QMessageBox.information(self, "Успех", "Данные приказа обновлены")
            self.refresh_orders()
            self.update_combo_boxes()
        except Exception as e:
            self.connection.rollback()
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить приказ: {str(e)}")

    def delete_order(self):
        order_id = self.order_id_input.text()
        if not order_id:
            QMessageBox.warning(self, "Ошибка", "Выберите приказ для удаления")
            return

        reply = QMessageBox.question(
            self, 'Подтверждение',
            'Вы уверены, что хотите удалить этот приказ? Это может привести к удалению связанных записей.',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                self.cursor.execute("DELETE FROM orders WHERE order_id = %s", (order_id,))
                self.connection.commit()
                QMessageBox.information(self, "Успех", "Приказ удален")
                self.refresh_orders()
                self.update_combo_boxes()
                self.clear_order_form()
            except Exception as e:
                self.connection.rollback()
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить приказ: {str(e)}")

    def clear_order_form(self):
        self.order_id_input.clear()
        self.order_title_input.clear()
        self.order_date_input.setDate(QDate.currentDate())
        self.order_number_input.clear()
        self.order_signer_combo.setCurrentIndex(0)


def main():
    app = QApplication(sys.argv)

    # Показываем диалог авторизации
    login_dialog = LoginDialog()
    if login_dialog.exec() == QDialog.Accepted:
        connection_params = login_dialog.get_connection_params()

        try:
            # Подключаемся к БД
            connection = psycopg2.connect(
                host=connection_params['host'],
                dbname=connection_params['dbname'],
                user=connection_params['user'],
                password=connection_params['password']
            )

            # Если подключение успешно, показываем главное окно
            window = MainWindow(connection)
            window.show()
            sys.exit(app.exec())
        except psycopg2.Error as e:
            QMessageBox.critical(None, "Ошибка подключения", f"Не удалось подключиться к базе данных: {str(e)}")
            sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()