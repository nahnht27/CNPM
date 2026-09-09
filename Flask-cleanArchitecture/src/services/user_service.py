class UserService:

    def __init__(self, repository):
        self.repository = repository

    def get_by_id(self, user_id):
        return self.repository.get_by_id(user_id)

    def update(self, user_id, data):
        return self.repository.update(user_id, data)