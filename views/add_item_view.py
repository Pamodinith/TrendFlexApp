from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QFormLayout, QMessageBox
)
from PySide6.QtCore import Signal
from viewmodels.add_item_viewmodel import AddItemViewModel

class AddItemView(QWidget):

    item_added = Signal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add New Inventory Item")
        self.resize(400, 400)

        self.viewmodel = AddItemViewModel()

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.code_input = QLineEdit()
        self.name_input = QLineEdit()
        self.desc_input = QLineEdit()
        self.price_input = QLineEdit()

        self.size_s_input = QLineEdit()
        self.size_m_input = QLineEdit()
        self.size_l_input = QLineEdit()

        form_layout.addRow("Item Code:", self.code_input)
        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("Description:", self.desc_input)
        form_layout.addRow("Price:", self.price_input)
        form_layout.addRow("Size S Quantity:", self.size_s_input)
        form_layout.addRow("Size M Quantity:", self.size_m_input)
        form_layout.addRow("Size L Quantity:", self.size_l_input)

        layout.addLayout(form_layout)

        self.save_btn = QPushButton("Add Item")
        self.save_btn.clicked.connect(self.save_item)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

    def save_item(self):
        item = {
            "code": self.code_input.text().strip(),
            "name": self.name_input.text().strip(),
            "desc": self.desc_input.text().strip(),
            "price": self.price_input.text().strip(),
            "sizes": {
                "S": self.size_s_input.text().strip(),
                "M": self.size_m_input.text().strip(),
                "L": self.size_l_input.text().strip()
            }
        }

        success, message = self.viewmodel.add_item(item)

        msg = QMessageBox()
        if success:
            self.item_added.emit()
            msg.setIcon(QMessageBox.Information)
        else:
            msg.setIcon(QMessageBox.Warning)

        msg.setText(message)
        msg.exec()
