from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QTableWidget, QTableWidgetItem, QComboBox, QMessageBox,
    QDateEdit, QDialog, QHBoxLayout
)
from PySide6.QtCore import Qt, QDate
from logic import (
    authenticate_user, get_all_events, get_registered_events,
    register_event, create_event, delete_event, get_all_registrations
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Event Registration System")
        self.setGeometry(100, 100, 600, 500)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.student_data = None
        self.init_login_ui()

    def set_new_layout(self, layout):
        old_layout = self.central_widget.layout()
        if old_layout:
            QWidget().setLayout(old_layout)
        self.central_widget.setLayout(layout)

    # -------------------- LOGIN UI --------------------
    def init_login_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("🔐 Event Registration System")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold;")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setFixedWidth(250)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedWidth(250)

        login_btn = QPushButton("Login")
        login_btn.setFixedWidth(120)
        login_btn.clicked.connect(self.login)

        layout.addWidget(title)
        layout.addSpacing(10)
        layout.addWidget(self.username_input, alignment=Qt.AlignCenter)
        layout.addWidget(self.password_input, alignment=Qt.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(login_btn, alignment=Qt.AlignCenter)

        self.set_new_layout(layout)

    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Please enter both username and password.")
            return

        role, user_data = authenticate_user(username, password)

        if role == "admin":
            self.init_admin_ui()
        elif role == "student":
            self.student_data = user_data
            self.init_student_ui()
        else:
            QMessageBox.critical(self, "Login Failed", "❌ Invalid credentials.")

    # -------------------- STUDENT UI --------------------
    def init_student_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        welcome = QLabel(f"👋 Welcome, {self.student_data['student_name']}")
        welcome.setAlignment(Qt.AlignCenter)
        welcome.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(welcome)

        self.event_list = QComboBox()
        self.update_event_list()
        layout.addWidget(self.event_list)

        register_btn = QPushButton("✅ Register for Selected Event")
        register_btn.clicked.connect(self.register_for_selected_event)
        layout.addWidget(register_btn)

        view_registered_btn = QPushButton("📋 View Registered Events")
        view_registered_btn.clicked.connect(self.show_registered_events)
        layout.addWidget(view_registered_btn)

        logout_btn = QPushButton("🔓 Logout")
        logout_btn.clicked.connect(self.init_login_ui)
        layout.addWidget(logout_btn)

        self.set_new_layout(layout)

    def update_event_list(self):
        self.event_list.clear()
        events = get_all_events()
        for event in events:
            self.event_list.addItem(
                f"{event['event_name']} on {event['event_date']} at {event['venue']}",
                event['event_id']
            )

    def register_for_selected_event(self):
        selected_index = self.event_list.currentIndex()
        if selected_index == -1:
            return
        event_id = self.event_list.itemData(selected_index)
        msg = register_event(self.student_data['student_id'], event_id)
        QMessageBox.information(self, "Registration", msg)

    def show_registered_events(self):
        events = get_registered_events(self.student_data['student_id'])
        if not events:
            QMessageBox.information(self, "Registered Events", "No events registered.")
            return

        table = QTableWidget(len(events), 3)
        table.setHorizontalHeaderLabels(["Event Name", "Date", "Venue"])

        for row, event in enumerate(events):
            table.setItem(row, 0, QTableWidgetItem(event['event_name']))
            table.setItem(row, 1, QTableWidgetItem(str(event['event_date'])))
            table.setItem(row, 2, QTableWidgetItem(event['venue']))

        self.show_table_dialog("📋 Registered Events", table)

    # -------------------- ADMIN UI --------------------
    def init_admin_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        title = QLabel("🛠️ Admin Panel")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        self.event_name = QLineEdit()
        self.event_name.setPlaceholderText("Event Name")

        self.event_date = QDateEdit()
        self.event_date.setCalendarPopup(True)
        self.event_date.setDate(QDate.currentDate())

        self.event_venue = QLineEdit()
        self.event_venue.setPlaceholderText("Venue")

        add_btn = QPushButton("➕ Create Event")
        add_btn.clicked.connect(self.add_event)

        layout.addWidget(self.event_name)
        layout.addWidget(self.event_date)
        layout.addWidget(self.event_venue)
        layout.addWidget(add_btn)

        self.event_list_widget = QTableWidget()
        self.event_list_widget.setColumnCount(3)
        self.event_list_widget.setHorizontalHeaderLabels(["Event ID", "Event", "Date & Venue"])
        self.refresh_event_list()
        layout.addWidget(self.event_list_widget)

        del_btn = QPushButton("🗑️ Delete Selected Event")
        del_btn.clicked.connect(self.delete_selected_event)
        layout.addWidget(del_btn)

        view_regs_btn = QPushButton("📋 View All Registrations")
        view_regs_btn.clicked.connect(self.show_all_registrations)
        layout.addWidget(view_regs_btn)

        logout_btn = QPushButton("🔓 Logout")
        logout_btn.clicked.connect(self.init_login_ui)
        layout.addWidget(logout_btn)

        self.set_new_layout(layout)

    def refresh_event_list(self):
        events = get_all_events()
        self.event_list_widget.setRowCount(len(events))

        for row, e in enumerate(events):
            self.event_list_widget.setItem(row, 0, QTableWidgetItem(str(e['event_id'])))
            self.event_list_widget.setItem(row, 1, QTableWidgetItem(e['event_name']))
            self.event_list_widget.setItem(row, 2, QTableWidgetItem(f"{e['event_date']} at {e['venue']}"))

    def add_event(self):
        name = self.event_name.text().strip()
        date = self.event_date.date().toString("yyyy-MM-dd")
        venue = self.event_venue.text().strip()

        if name and venue:
            create_event(name, date, venue)
            self.refresh_event_list()
            QMessageBox.information(self, "Success", "✅ Event created.")
        else:
            QMessageBox.warning(self, "Missing Info", "Please enter all fields.")

    def delete_selected_event(self):
        selected = self.event_list_widget.currentRow()
        if selected >= 0:
            event_id_item = self.event_list_widget.item(selected, 0)
            if event_id_item:
                delete_event(int(event_id_item.text()))
                self.refresh_event_list()
                QMessageBox.information(self, "Deleted", "🗑️ Event deleted.")

    def show_all_registrations(self):
        regs = get_all_registrations()
        if not regs:
            QMessageBox.information(self, "No Data", "No registrations found.")
            return
        
        table = QTableWidget(len(regs), 3)
        table.setHorizontalHeaderLabels(["Student", "Event", "Date"])

        for row, r in enumerate(regs):
            table.setItem(row, 0, QTableWidgetItem(str(r['student_name'])))
            table.setItem(row, 1, QTableWidgetItem(str(r['event_name'])))
            table.setItem(row, 2, QTableWidgetItem(str(r['registration_date'])))

        self.show_table_dialog("📋 All Registrations", table)


    # -------------------- Reusable Table Dialog --------------------
    def show_table_dialog(self, title, table_widget):
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        layout = QVBoxLayout()
        layout.addWidget(table_widget)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn, alignment=Qt.AlignRight)
        dialog.setLayout(layout)
        dialog.resize(500, 300)
        dialog.exec()
