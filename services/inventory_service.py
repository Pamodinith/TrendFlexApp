from database.connection import get_connection

class InventoryService:
    def fetch_all_items(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT i.item_code, i.name, i.price, s.size, s.quantity
            FROM items i
            JOIN item_sizes s ON i.id = s.item_id
            ORDER BY i.item_code, s.size
        """)
        items = cursor.fetchall()
        conn.close()
        return items
    def add_item_to_db(self, code, name, desc, price, sizes_dict):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            # Check for duplicate
            cursor.execute("SELECT id FROM items WHERE item_code = ?", (code,))
            if cursor.fetchone():
                return False

            cursor.execute(
                "INSERT INTO items (item_code, name, description, price) VALUES (?, ?, ?, ?)",
                (code, name, desc, price)
            )
            item_id = cursor.lastrowid

            for size, qty in sizes_dict.items():
                cursor.execute(
                    "INSERT INTO item_sizes (item_id, size, quantity) VALUES (?, ?, ?)",
                    (item_id, size, qty)
                )

            conn.commit()
            return True
        except Exception as e:
            print(f"[DB ERROR] {e}")
            return False
        finally:
            conn.close()
    
    def fetch_item_details(self, item_code):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT i.item_code, i.name, i.description, i.price, s.size, s.quantity
            FROM items i
            JOIN item_sizes s ON i.id = s.item_id
            WHERE i.item_code = ?
        """, (item_code,))
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return None

        # Extract info and sizes
        first = rows[0]
        sizes = [(row[4], row[5]) for row in rows]

        return {
            "item_code": first[0],
            "name": first[1],
            "description": first[2],
            "price": first[3],
            "sizes": sizes
        }

    def update_item_in_db(self, code, name, desc, price, sizes_dict):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                UPDATE items SET name = ?, description = ?, price = ? WHERE item_code = ?
            """, (name, desc, price, code))

            cursor.execute("SELECT id FROM items WHERE item_code = ?", (code,))
            item_id = cursor.fetchone()[0]

            for size, qty in sizes_dict.items():
                cursor.execute("""
                    UPDATE item_sizes SET quantity = ? WHERE item_id = ? AND size = ?
                """, (qty, item_id, size))

            conn.commit()
            return True
        except Exception as e:
            print(f"[DB ERROR] {e}")
            return False
        finally:
            conn.close()

    def delete_item_from_db(self, item_code):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id FROM items WHERE item_code = ?", (item_code,))
            row = cursor.fetchone()
            if not row:
                return False
            item_id = row[0]

            cursor.execute("DELETE FROM item_sizes WHERE item_id = ?", (item_id,))
            cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"[DB ERROR] {e}")
            return False
        finally:
            conn.close()


