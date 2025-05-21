from database.connection import get_connection

class AuthService:
    def __init__(self):
        pass

    def authenticate(self, username: str, password: str) -> str:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT role FROM users WHERE username = ? AND password = ?",
            (username, password)
        )
        result = cursor.fetchone()

        conn.close()

        if result:
            return result[0]  # 'admin' or 'staff'
        return ""
