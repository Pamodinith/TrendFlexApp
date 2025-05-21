import sqlite3

conn = sqlite3.connect("trendflex.db")
cursor = conn.cursor()

# Recreate the inventory table
cursor.execute('''
CREATE TABLE IF NOT EXISTS inventory (
    item_code TEXT PRIMARY KEY,
    name TEXT,
    description TEXT,
    price REAL,
    qty_s INTEGER,
    qty_m INTEGER,
    qty_l INTEGER,
    qty_xl INTEGER
)
''')

# Insert sample item
cursor.execute('''
INSERT OR IGNORE INTO inventory (item_code, name, description, price, qty_s, qty_m, qty_l, qty_xl)
VALUES ('TS01', 'T-Shirt', 'Plain white tee', 950.0, 10, 15, 12, 8)
''')

conn.commit()
conn.close()
