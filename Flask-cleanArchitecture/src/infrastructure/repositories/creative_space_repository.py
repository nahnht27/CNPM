from datetime import datetime
from typing import List, Optional

from infrastructure.databases.factory_database import FactoryDatabase as db_factory
from infrastructure.models.creative_space_model import CreativeSpaceModel
from infrastructure.models.category_model import CategoryModel
from infrastructure.models.space_image_model import SpaceImageModel


class CreativeSpaceRepository:

    def __init__(self, session=None):
        self.session = session or db_factory.get_database('POSTGREE').session

    # =========================================================
    # CREATE
    # =========================================================

    def add(self, data) -> CreativeSpaceModel:

        m = CreativeSpaceModel(
            provider_id=data.get('provider_id'),
            name=data.get('name'),
            category_id=data.get('category_id'),
            description=data.get('description'),
            size_sqm=data.get('size_sqm'),
            max_capacity=data.get('max_capacity'),
            operating_hours=data.get('operating_hours'),
            pricing_model=data.get('pricing_model'),
            base_price=data.get('base_price'),
            status=data.get('status', 'active'),
            address=data.get('address'),

            # DB yêu cầu CreatedAt NOT NULL
            # Nếu frontend không gửi thì tự tạo thời gian hiện tại
            created_at=data.get('created_at') or datetime.now()
        )

        try:
            self.session.add(m)
            self.session.commit()
            self.session.refresh(m)

            return m

        except Exception:
            self.session.rollback()
            raise

    # =========================================================
    # GET BY ID
    # =========================================================

    def get_by_id(self, id: int) -> Optional[CreativeSpaceModel]:

        return (
            self.session
            .query(CreativeSpaceModel)
            .filter_by(id=id)
            .first()
        )

    # =========================================================
    # GET DETAIL
    # =========================================================

    def get_detail(self, id: int):

        space = (
            self.session
            .query(CreativeSpaceModel)
            .filter_by(id=id)
            .first()
        )

        if not space:
            return None

        category = (
            self.session
            .query(CategoryModel)
            .filter_by(id=space.category_id)
            .first()
        )

        images = (
            self.session
            .query(SpaceImageModel)
            .filter_by(space_id=space.id)
            .all()
        )

        return {
            'id': space.id,
            'provider_id': space.provider_id,
            'name': space.name,
            'category_id': space.category_id,
            'category_name': category.name if category else None,
            'description': space.description,
            'size_sqm': space.size_sqm,
            'max_capacity': space.max_capacity,
            'operating_hours': space.operating_hours,
            'pricing_model': space.pricing_model,
            'base_price': space.base_price,
            'status': space.status,
            'address': space.address,
            'created_at': space.created_at,

            'images': [
                image.image_url
                for image in images
            ]
        }

    # =========================================================
    # LIST
    # =========================================================

    def list(self, provider_id=None) -> List:

        query = (
            self.session
            .query(CreativeSpaceModel)
        )

        # Nếu có provider_id thì chỉ lấy space
        # thuộc provider đó
        if provider_id is not None:
            query = query.filter(
                CreativeSpaceModel.provider_id == provider_id
            )

        spaces = query.all()

        result = []

        for space in spaces:

            image = (
                self.session
                .query(SpaceImageModel)
                .filter_by(space_id=space.id)
                .first()
            )

            result.append({
                'id': space.id,
                'provider_id': space.provider_id,
                'name': space.name,
                'category_id': space.category_id,
                'description': space.description,
                'size_sqm': space.size_sqm,
                'max_capacity': space.max_capacity,
                'operating_hours': space.operating_hours,
                'pricing_model': space.pricing_model,
                'base_price': space.base_price,
                'status': space.status,
                'address': space.address,
                'image_url': image.image_url if image else None,
                'created_at': space.created_at
            })

        return result

    # =========================================================
    # UPDATE
    # =========================================================

    def update(self, data) -> CreativeSpaceModel:

        m = (
            self.session
            .query(CreativeSpaceModel)
            .filter_by(id=data.get('id'))
            .first()
        )

        if not m:
            raise ValueError('Not found')

        for key, value in data.items():

            if key == 'id':
                continue

            if hasattr(m, key):
                setattr(m, key, value)

        try:
            self.session.commit()
            self.session.refresh(m)

            return m

        except Exception:
            self.session.rollback()
            raise

    # =========================================================
    # DELETE
    # =========================================================

    def delete(self, id: int) -> None:

        m = (
            self.session
            .query(CreativeSpaceModel)
            .filter_by(id=id)
            .first()
        )

        if not m:
            return

        try:
            self.session.delete(m)
            self.session.commit()

        except Exception:
            self.session.rollback()
            raise