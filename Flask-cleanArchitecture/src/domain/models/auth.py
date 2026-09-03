class Auth:
    def __init__(
        self,
        username: str,
        password: str,
        passwordcomfirm: str,
        email: str,
        role_id: int = None
    ):
        self.username = username
        self.password = password
        self.passwordcomfirm = passwordcomfirm
        self.email = email
        self.role_id = role_id
        self.id = None