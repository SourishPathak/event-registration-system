from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QMessageBox, QComboBox, QTableWidget, QTableWidgetItem, QHBoxLayout
)
from PySide6.QtCore import Qt
from db import get_connection
from datetime import datetime


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Event Registration System")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.student_id_input = QLineEdit()
        self.student_id_input.setPlaceholderText("Enter Student ID")

        self.admin_pwd_input = QLineEdit()
        self.admin_pwd_input.setPlaceholderText("Enter Admin Password")
        self.admin_pwd_input.setEchoMode(QLineEdit.Password)

        self.student_btn = QPushButton("Login as Student")
        self.admin_btn = QPushButton("Login as Admin")

        self.layout.addWidget(QLabel("Welcome to Event Registration System"))
        self.layout.addWidget(self.student_id_input)
        self.layout.addWidget(self.student_btn)
        self.layout.addWidget(QLabel("OR"))
        self.layout.addWidget(self.admin_pwd_input)
        self.layout.addWidget(self.admin_btn)

        self.student_btn.clicked.connect(self.login_student)
        self.admin_btn.clicked.connect(self.login_admin)

    def login_student(self):
        student_id = self.student_id_input.text()
        if not student_id.isdigit():
            QMessageBox.warning(self, "Error", "Enter a valid numeric Student ID.")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
        student = cursor.fetchone()
        conn.close()

        if student:
            self.load_student_dashboard(int(student_id), student["student_name"])
        else:
            QMessageBox.warning(self, "Login Failed", "Student not found.")

    def login_admin(self):
        pwd = self.admin_pwd_input.text()
        if pwd == "admin123":
            self.load_admin_dashboard()
        else:
            QMessageBox.critical(self, "Access Denied", "Incorrect admin password.")

    # -------------------- STUDENT DASHBOARD --------------------

    def load_student_dashboard(self, student_id, student_name):
        self.clear_layout()

        self.layout.addWidget(QLabel(f"👋 Welcome, {student_name}"))

        self.event_table = QTableWidget()
        self.event_table.setColumnCount(4)
        self.event_table.setHorizontalHeaderLabels(["ID", "Name", "Date", "Venue"])

        self.load_events()

        self.layout.addWidget(self.event_table)

        register_btn = QPushButton("Register for Selected Event")
        register_btn.clicked.connect(lambda: self.register_for_event(student_id))
        self.layout.addWidget(register_btn)

    def load_events(self):
        self.event_table.setRowCount(0)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM events")
        events = cursor.fetchall()
        conn.close()

        for row, event in enumerate(events):
            self.event_table.insertRow(row)
            self.event_table.setItem(row, 0, QTableWidgetItem(str(event["event_id"])))
            self.event_table.setItem(row, 1, QTableWidgetItem(event["event_name"]))
            self.event_table.setItem(row, 2, QTableWidgetItem(str(event["event_date"])))
            self.event_table.setItem(row, 3, QTableWidgetItem(event["venue"]))

    def register_for_event(self, student_id):
        selected_row = self.event_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "No Selection", "Select an event to register.")
            return

        event_id = int(self.event_table.item(selected_row, 0).text())

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM registrations WHERE student_id = %s AND event_id = %s", (student_id, event_id))
        if cursor.fetchone():
            QMessageBox.information(self, "Info", "Already registered for this event.")
        else:
            cursor.execute(
                "INSERT INTO registrations (student_id, event_id, registration_date) VALUES (%s, %s, %s)",
                (student_id, event_id, datetime.today().strftime('%Y-%m-%d'))
            )
            conn.commit()
            QMessageBox.information(self, "Success", "Registration successful.")
        conn.close()

    # -------------------- ADMIN DASHBOARD --------------------

    def load_admin_dashboard(self):
        self.clear_layout()

        self.layout.addWidget(QLabel("🛠 Admin Dashboard"))

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Event Name")
        self.date_input = QLineEdit()
        self.date_input.setPlaceholderText("YYYY-MM-DD")
        self.venue_input = QLineEdit()
        self.venue_input.setPlaceholderText("Venue")

        add_btn = QPushButton("Create Event")
        add_btn.clicked.connect(self.add_event)

        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.date_input)
        self.layout.addWidget(self.venue_input)
        self.layout.addWidget(add_btn)

        self.refresh_btn = QPushButton("View All Events")
        self.refresh_btn.clicked.connect(self.load_events_admin)
        self.layout.addWidget(self.refresh_btn)

        self.admin_event_table = QTableWidget()
        self.admin_event_table.setColumnCount(4)
        self.admin_event_table.setHorizontalHeaderLabels(["ID", "Name", "Date", "Venue"])
        self.layout.addWidget(self.admin_event_table)
        delete_btn = QPushButton("Delete Selected Event")
        delete_btn.clicked.connect(self.delete_event)
        self.stack_layout.addWidget(delete_btn)

        self.refresh_events()
        logout_btn = QPushButton("Logout")
        logout_btn.clicked.connect(self.login_screen)
        self.stack_layout.addWidget(logout_btn)

    def add_event(self):
        name = self.name_input.text()
        date = self.date_input.text()
        venue = self.venue_input.text()

        if not name or not date or not venue:
            QMessageBox.warning(self, "Input Error", "All fields are required.")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO events (event_name, event_date, venue) VALUES (%s, %s, %s)", (name, date, venue))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Success", "Event created.")
        self.load_events_admin()

    def load_events_admin(self):
        self.admin_event_table.setRowCount(0)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM events")
        events = cursor.fetchall()
        conn.close()

        for row, event in enumerate(events):
            self.admin_event_table.insertRow(row)
            self.admin_event_table.setItem(row, 0, QTableWidgetItem(str(event["event_id"])))
            self.admin_event_table.setItem(row, 1, QTableWidgetItem(event["event_name"]))
            self.admin_event_table.setItem(row, 2, QTableWidgetItem(str(event["event_date"])))
            self.admin_event_table.setItem(row, 3, QTableWidgetItem(event["venue"]))

    # -------------------- UTILITY --------------------

    def clear_layout(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
