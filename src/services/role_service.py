from typing import List, Optional

class RoleService:
    def __init__(self, repository):
        self.repository = repository

    def create_role(self, name: str, created_at=None, created_by=None):
        return self.repository.add({'name': name, 'created_at': created_at, 'created_by': created_by})

    def get_role(self, role_id: int):
        return self.repository.get_by_id(role_id)

    def list_roles(self) -> List:
        return self.repository.list()

    def update_role(self, role_id: int, name: str = None, updated_at=None, updated_by=None):
        return self.repository.update({'id': role_id, 'name': name, 'updated_at': updated_at, 'updated_by': updated_by})

    def delete_role(self, role_id: int) -> None:
        self.repository.delete(role_id)
