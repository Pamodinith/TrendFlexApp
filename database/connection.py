import sqlite3
import os

DB_NAME = "trendflex.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    return conn

def initialize_db():
    if not os.path.exists(DB_NAME):
        conn = get_connection()
        cursor = conn.cursor()

        # Create tables
        cursor.executescript("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT CHECK(role IN ('admin', 'staff')) NOT NULL
        );

        CREATE TABLE items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_code TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL
        );

        CREATE TABLE item_sizes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER NOT NULL,
            size TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE
        );

        CREATE TABLE bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bill_no TEXT UNIQUE NOT NULL,
            timestamp TEXT NOT NULL,
            payment_method TEXT NOT NULL,
            paid REAL,
            balance REAL
        );

        CREATE TABLE bill_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bill_id INTEGER NOT NULL,
            item_code TEXT NOT NULL,
            size TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (bill_id) REFERENCES bills(id) ON DELETE CASCADE
        );
        """)

        # Add one admin and one staff user
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ("admin", "admin123", "admin"))
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ("staff", "staff123", "staff"))

        conn.commit()
        conn.close()
    def create_bills_table():
        conn = sqlite3.connect("trendflex.db")
        cursor = conn.cursor()

        # Table for storing bills
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bills (
                bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
                bill_no TEXT,
                date TEXT,
                total REAL,
                payment_mode TEXT,
                cash_given REAL,
                balance REAL
            )
        ''')

        # Table for storing each item in the bill
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bill_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bill_id INTEGER,
                item_code TEXT,
                item_name TEXT,
                size TEXT,
                qty INTEGER,
                price REAL,
                FOREIGN KEY (bill_id) REFERENCES bills (bill_id)
            )
        ''')

        conn.commit()
        conn.close()

