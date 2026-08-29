from infrastructure.models.amenity_model import AmenityModel


class AmenityRepository:
    def __init__(self, session):
        self.session = session

    def add(self, data: dict):
        item = AmenityModel(**data)
        self.session.add(item)
        self.session.commit()
        return item

    def get_by_id(self, id: int):
        return self.session.query(AmenityModel).filter(AmenityModel.AmenityID == id).first()

    def list(self):
        return self.session.query(AmenityModel).all()

    def update(self, data: dict):
        item = self.get_by_id(data['id'])
        if not item:
            return None
        for key, value in data.items():
            if key != 'id':
                setattr(item, key, value)
        self.session.commit()
        return item

    def delete(self, id: int):
        item = self.get_by_id(id)
        if item:
            self.session.delete(item)
            self.session.commit()
        return item