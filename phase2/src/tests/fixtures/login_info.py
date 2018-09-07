class AuthInfo:
    def __init__(self, login, password, status=None):
        self.login = login
        self.password = password
        self.exp_status = status

    def get_json(self):
        return {"username": self.login, "password": self.password}