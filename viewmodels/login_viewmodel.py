from services.auth_service import AuthService

class LoginViewModel:
    def __init__(self):
        self.auth_service = AuthService()

    def login(self, username: str, password: str) -> str:
        return self.auth_service.authenticate(username, password)
