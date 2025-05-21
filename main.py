'''
import sys
from PySide6.QtWidgets import QApplication
from views.login_view import LoginView
from database.connection import initialize_db

if __name__ == "__main__":
    initialize_db()  # <- This will create the DB and tables if not exist


    app = QApplication(sys.argv)
    window = LoginView()
    window.show()
    sys.exit(app.exec())
    '''
'''
from PyQt6.QtWidgets import QApplication
import sys
from views.billing_view import BillingView

app = QApplication(sys.argv)
window = BillingView()
window.show()
sys.exit(app.exec())
'''
import sys
from PySide6.QtWidgets import QApplication
from PyQt6.QtWidgets import QApplication
from views.login_view import LoginView
from database.connection import initialize_db
from views.billing_view import BillingView

if __name__ == "__main__":
    initialize_db()  # <- This will create the DB and tables if not exist


    app = QApplication(sys.argv)
    window = BillingView()
    #window = LoginView()
    window.show()
    sys.exit(app.exec())