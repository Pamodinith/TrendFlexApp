from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QComboBox,
    QSpinBox, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDoubleValidator
import sqlite3
from datetime import datetime


class BillingView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Billing")

        # Item code input
        self.item_code_label = QLabel("Item Code:")
        self.item_code_input = QLineEdit()

        # Size selection (will populate after item code entered)
        self.size_label = QLabel("Select Size:")
        self.size_combo = QComboBox()
        self.size_combo.setEnabled(False)  # Disable until item code checked

        # Quantity input
        self.quantity_label = QLabel("Quantity:")
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setMinimum(1)
        self.quantity_spin.setMaximum(100)
        self.quantity_spin.setEnabled(False)

        # Add item button
        self.add_item_button = QPushButton("Add Item")
        self.add_item_button.setEnabled(False)

        # Table to show added items
        self.items_table = QTableWidget()
        self.items_table.setColumnCount(7)
        self.items_table.setHorizontalHeaderLabels(
            ["Item Code", "Name", "Size", "Qty", "Price/unit", "Total","Remove"]
        )
        self.items_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # Total amount label
        self.total_label = QLabel("Total: 0.00")

        # Payment buttons and inputs
        self.cash_button = QPushButton("Pay by Cash")
        self.card_button = QPushButton("Pay by Card")

        # Layout setup
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.item_code_label)
        input_layout.addWidget(self.item_code_input)
        input_layout.addWidget(self.size_label)
        input_layout.addWidget(self.size_combo)
        input_layout.addWidget(self.quantity_label)
        input_layout.addWidget(self.quantity_spin)
        input_layout.addWidget(self.add_item_button)


        main_layout = QVBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.items_table)
        main_layout.addWidget(self.total_label)

        self.setLayout(main_layout)

        # Connect signals
        self.item_code_input.editingFinished.connect(self.on_item_code_entered)
        self.add_item_button.clicked.connect(self.add_item_to_bill)
        
        self.current_items = []  # List of dicts representing bill items

        self.update_total()

        # Payment Option
        payment_layout = QHBoxLayout()

        self.payment_mode_combo = QComboBox()
        self.payment_mode_combo.addItems(["Cash", "Card"])
        self.payment_mode_combo.currentTextChanged.connect(self.toggle_cash_input)

        self.cash_input = QLineEdit()
        self.cash_input.setPlaceholderText("Cash received")
        self.cash_input.setValidator(QDoubleValidator(0.0, 1000000.0, 2))
        self.cash_input.textChanged.connect(self.calculate_balance)

        self.balance_label = QLabel("Balance: Rs. 0.00")

        payment_layout.addWidget(QLabel("Payment Method:"))
        payment_layout.addWidget(self.payment_mode_combo)
        payment_layout.addWidget(self.cash_input)
        payment_layout.addWidget(self.balance_label)

        main_layout.addLayout(payment_layout)
        self.proceed_button = QPushButton("Proceed & Print Bill")
        self.proceed_button.clicked.connect(self.finalize_bill)
        main_layout.addWidget(self.proceed_button)

        self.toggle_cash_input("Cash")


    def fetch_item_from_db(self, item_code):
        conn = sqlite3.connect("trendflex.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM inventory WHERE item_code = ?", (item_code,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        # Assume columns: item_code, name, description, price, qty_s, qty_m, qty_l, qty_xl...
        item = {
        "code": row[0],
        "name": row[1],
        "description": row[2],
        "price": row[3],
        "sizes": {
            "S": row[4],
            "M": row[5],
            "L": row[6],
        }
        }
        return item
    
    def toggle_cash_input(self, mode):
        if mode == "Cash":
            self.cash_input.setVisible(True)
            self.balance_label.setVisible(True)
        else:
            self.cash_input.setVisible(False)
            self.balance_label.setVisible(False)


    def on_item_code_entered(self):

        code = self.item_code_input.text().strip().upper()
        item = self.fetch_item_from_db(code)

        if not item:
            QMessageBox.warning(self, "Not Found", f"Item '{code}' not found in inventory.")
            return

        self.selected_item = item
        self.size_combo.clear()

        for size, qty in item["sizes"].items():
            if qty > 0:
                self.size_combo.addItem(f"{size} (Available: {qty})", size)

        self.qty_input.setText("")
        self.qty_input.setFocus()

    def add_item_to_bill(self):
        code = self.item_code_input.text().strip().upper()
        size = self.size_combo.currentData()  # Use .currentData() to get size value
        qty = self.quantity_spin.value()

        item = self.fetch_item_from_db(code)
        if not item:
            QMessageBox.warning(self, "Error", "Item code not found in database.")
            return

        available_qty = item["sizes"].get(size, 0)
        if qty > available_qty:
            QMessageBox.warning(self, "Error", f"Only {available_qty} items available in size {size}.")
            return

        # Check duplicates in current bill
        for existing_item in self.current_items:
            if existing_item["code"] == code and existing_item["size"] == size:
                QMessageBox.warning(self, "Duplicate", "This item and size already added to the bill.")
                return

        # Add to current bill list
        name = item["name"]
        price = item["price"]
        total = price * qty

        self.current_items.append({
            "code": code,
            "name": name,
            "size": size,
            "qty": qty,
            "price": price,
            "total": total
        })

        self.refresh_table()
        self.update_total()


    def refresh_table(self):
        self.items_table.setRowCount(len(self.current_items))
        for row, item in enumerate(self.current_items):
            self.items_table.setItem(row, 0, QTableWidgetItem(item["code"]))
            self.items_table.setItem(row, 1, QTableWidgetItem(item["name"]))
            self.items_table.setItem(row, 2, QTableWidgetItem(item["size"]))
            self.items_table.setItem(row, 3, QTableWidgetItem(str(item["qty"])))
            self.items_table.setItem(row, 4, QTableWidgetItem(str(item["price"])))
            self.items_table.setItem(row, 5, QTableWidgetItem(str(item["total"])))
            # Create Remove button for each row
            btn = QPushButton("Remove")
            btn.clicked.connect(lambda checked, r=row: self.remove_item(r))
            self.items_table.setCellWidget(row, 6, btn)

    def update_total(self):
        total = sum(item["total"] for item in self.current_items)
        self.total_label.setText(f"Total: {total:.2f}")

    def remove_item(self, row):
        del self.current_items[row]
        self.refresh_table()
        self.update_total()

    def calculate_balance(self):
        try:
            given = float(self.cash_input.text())
            total = self.total_amount
            balance = given - total
            self.balance_label.setText(f"Balance: Rs. {balance:.2f}")
        except ValueError:
            self.balance_label.setText("Balance: Rs. 0.00")

    def finalize_bill(self):
        if not self.current_items:
            QMessageBox.warning(self, "No Items", "Please add at least one item to bill.")
            return

        payment_mode = self.payment_mode_combo.currentText()
        cash_given = 0.0
        balance = 0.0
        if payment_mode == "Cash":
            try:
                cash_given = float(self.cash_input.text())
                if cash_given < self.total_amount:
                    QMessageBox.warning(self, "Insufficient", "Cash given is less than total.")
                    return
            except ValueError:
                QMessageBox.warning(self, "Invalid Input", "Enter a valid cash amount.")
                return
            balance = cash_given - self.total_amount
        else:
            balance = 0.0  # Card case

        # --- Save bill to DB ---
        conn = sqlite3.connect("trendflex.db")
        cursor = conn.cursor()

        bill_no = f"INV{int(datetime.now().timestamp())}"
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute('''
            INSERT INTO bills (bill_no, date, total, payment_mode, cash_given, balance)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (bill_no, date, self.total_amount, payment_mode, cash_given, balance))
        bill_id = cursor.lastrowid

        for item in self.current_items:
            cursor.execute('''
                INSERT INTO bill_items (bill_id, item_code, item_name, size, qty, price)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                bill_id,
                item["code"],
                item["name"],
                item["size"],
                item["qty"],
                item["price"]
            ))

        # --- Update inventory ---
        cursor.execute('''
            UPDATE inventory
            SET qty_{} = qty_{} - ?
            WHERE item_code = ?
        '''.format(item["size"].lower(), item["size"].lower()), (item["qty"], item["code"]))

        QMessageBox.information(
            self,
            "Bill Complete",
            f"Payment successful via {payment_mode}.\nBalance: Rs. {balance:.2f}",
        )

        self.reset_billing_form()

    def reset_billing_form(self):
        self.current_items.clear()
        self.refresh_table()
        self.update_total()
        self.cash_input.clear()
        self.balance_label.setText("Balance: Rs. 0.00")


    
