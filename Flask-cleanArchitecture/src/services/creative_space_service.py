from typing import List


class CreativeSpaceService:

    def __init__(self, repository, service_provider_repository=None):
        self.repository = repository
        self.service_provider_repository = service_provider_repository

    # =========================================================
    # CREATE
    # =========================================================

    def create_space(self, **data):

        provider_id = data.get('provider_id')

        if not provider_id:
            raise ValueError('Provider ID is required')

        # Provider phải được Admin xác minh
        if self.service_provider_repository:

            provider = (
                self.service_provider_repository
                .get_by_id(provider_id)
            )

            if not provider:
                raise ValueError('Provider not found')

            verification_status = (
                provider.verification_status or 'pending'
            ).lower()

            if verification_status != 'approved':
                raise PermissionError(
                    'Tài khoản Provider chưa được Admin xác minh. '
                    'Bạn chưa thể tạo không gian.'
                )

        return self.repository.add(data)

    # =========================================================
    # GET
    # =========================================================

    def get_space(self, id: int):
        return self.repository.get_by_id(id)

    def get_space_detail(self, id: int):
        return self.repository.get_detail(id)

    def list_spaces(self, provider_id=None) -> List:
        return self.repository.list(provider_id)

    # =========================================================
    # UPDATE
    # =========================================================

    def update_space(self, id: int, **data):
        data['id'] = id
        return self.repository.update(data)

    # =========================================================
    # DELETE
    # =========================================================

    def delete_space(self, id: int):
        return self.repository.delete(id)