from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QMessageBox
)
from PySide6.QtCore import Signal
from viewmodels.edit_item_viewmodel import EditItemViewModel

class EditItemView(QWidget):
    item_edited = Signal()

    def __init__(self, item_code):
        super().__init__()
        self.setWindowTitle(f"Edit Item: {item_code}")
        self.resize(400, 400)

        self.viewmodel = EditItemViewModel()
        self.item_code = item_code

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.code_label = QLabel(item_code)  # Item code uneditable
        self.name_input = QLineEdit()
        self.desc_input = QLineEdit()
        self.price_input = QLineEdit()

        self.size_s_input = QLineEdit()
        self.size_m_input = QLineEdit()
        self.size_l_input = QLineEdit()

        form_layout.addRow("Item Code:", self.code_label)
        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("Description:", self.desc_input)
        form_layout.addRow("Price:", self.price_input)
        form_layout.addRow("Size S Quantity:", self.size_s_input)
        form_layout.addRow("Size M Quantity:", self.size_m_input)
        form_layout.addRow("Size L Quantity:", self.size_l_input)

        layout.addLayout(form_layout)

        self.save_btn = QPushButton("Save Changes")
        self.save_btn.clicked.connect(self.save_changes)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

        self.load_item_data()

    def load_item_data(self):
        item = self.viewmodel.get_item_by_code(self.item_code)
        if not item:
            QMessageBox.warning(self, "Error", "Item not found.")
            self.close()
            return

        # item is tuple: (item_code, name, description, price, size, quantity)
        # We need to group sizes, so VM should send grouped data

        self.name_input.setText(item["name"])
        self.desc_input.setText(item["description"])
        self.price_input.setText(str(item["price"]))
        self.size_s_input.setText(str(item["sizes"].get("S", 0)))
        self.size_m_input.setText(str(item["sizes"].get("M", 0)))
        self.size_l_input.setText(str(item["sizes"].get("L", 0)))

    def save_changes(self):
        item_data = {
            "code": self.item_code,
            "name": self.name_input.text().strip(),
            "desc": self.desc_input.text().strip(),
            "price": self.price_input.text().strip(),
            "sizes": {
                "S": self.size_s_input.text().strip(),
                "M": self.size_m_input.text().strip(),
                "L": self.size_l_input.text().strip(),
            }
        }
        success, message = self.viewmodel.update_item(item_data)

        msg = QMessageBox()
        if success:
            msg.setIcon(QMessageBox.Information)
            self.item_edited.emit()
            self.close()
        else:
            msg.setIcon(QMessageBox.Warning)
        msg.setText(message)
        msg.exec()
