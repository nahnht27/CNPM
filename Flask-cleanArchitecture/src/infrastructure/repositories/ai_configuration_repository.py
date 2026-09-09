from infrastructure.models.ai_configuration_model import AIConfigurationModel


class AIConfigurationRepository:
    def __init__(self, session):
        self.session = session

    def add(self, data: dict):
        item = AIConfigurationModel(**data)
        self.session.add(item)
        self.session.commit()
        return item

    def get_by_id(self, id: int):
        return self.session.query(AIConfigurationModel).filter(AIConfigurationModel.id == id).first()

    def list(self):
        return self.session.query(AIConfigurationModel).all()

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