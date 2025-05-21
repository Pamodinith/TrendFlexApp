from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel
from viewmodels.inventory_viewmodel import InventoryViewModel
from PySide6.QtWidgets import QPushButton, QMessageBox
from views.add_item_view import AddItemView
from views.edit_item_view import EditItemView



class InventoryView(QWidget):
    def __init__(self, user_role):
        super().__init__()
        self.setWindowTitle("Inventory")
        self.resize(700, 400)

        self.viewmodel = InventoryViewModel()
        self.user_role = user_role

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label = QLabel(f"Inventory View - Logged in as: {self.user_role.capitalize()}")
        layout.addWidget(self.label)

        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.load_inventory()
        if self.user_role == "admin":
            from views.add_item_view import AddItemView
            self.add_btn = QPushButton("Add New Item")
            self.add_btn.clicked.connect(self.open_add_item_window)
            layout.addWidget(self.add_btn)

            self.edit_btn = QPushButton("Edit Selected Item")
            self.edit_btn.clicked.connect(self.open_edit_item_window)
            self.edit_btn.setEnabled(False)  # Disabled until an item is selected
            layout.addWidget(self.edit_btn)

            self.delete_btn = QPushButton("Delete Selected Item")
            self.delete_btn.clicked.connect(self.delete_selected_item)
            self.delete_btn.setEnabled(False)
            layout.addWidget(self.delete_btn)
        
        self.table.itemSelectionChanged.connect(self.on_selection_changed)


    def open_add_item_window(self):
        self.add_item_window = AddItemView()
        self.add_item_window.item_added.connect(self.load_inventory)
        self.add_item_window.show()


    def load_inventory(self):
        items = self.viewmodel.get_all_items()

        self.table.setRowCount(len(items))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Item Code", "Name", "Price", "Size", "Quantity"])

        for row, item in enumerate(items):
            for col, value in enumerate(item):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

    def on_selection_changed(self):
        has_selection = len(self.table.selectedItems()) > 0
        self.edit_btn.setEnabled(has_selection)
        self.delete_btn.setEnabled(has_selection)

    def get_selected_item_code(self):
        selected_items = self.table.selectedItems()
        if selected_items:
            # Assuming item code is in column 0
            return selected_items[0].text()
        return None

    def open_edit_item_window(self):
        code = self.get_selected_item_code()
        if not code:
            return
        self.edit_window = EditItemView(code)
        self.edit_window.item_edited.connect(self.load_inventory)
        self.edit_window.show()

    def delete_selected_item(self):
        code = self.get_selected_item_code()
        if not code:
            return

        confirm = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete item {code}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            success = self.viewmodel.delete_item(code)
            if success:
                QMessageBox.information(self, "Deleted", "Item deleted successfully.")
                self.load_inventory()
            else:
                QMessageBox.warning(self, "Error", "Failed to delete item.")
