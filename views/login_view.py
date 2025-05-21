from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from viewmodels.login_viewmodel import LoginViewModel
from views.inventory_view import InventoryView

class LoginView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TrendFlex Login")
        self.resize(300, 200)

        # UI elements
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()

        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.handle_login)

        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

        self.viewmodel = LoginViewModel()

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        role = self.viewmodel.login(username, password)

        if role == "admin":
            QMessageBox.information(self, "Login", "Admin login successful!")
            # TODO: Load Admin Dashboard
        elif role == "staff":
            QMessageBox.information(self, "Login", "Staff login successful!")
            # TODO: Load Staff Dashboard
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid credentials.")
        
        if role == "admin" or role == "staff":
            self.inventory_window = InventoryView(role)
            self.inventory_window.show()
            self.close()
