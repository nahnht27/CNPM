from typing import List, Optional
from infrastructure.databases.factory_database import FactoryDatabase as db_factory
from infrastructure.models.post_model import PostModel

class PostRepository:
    def __init__(self, session=None):
        self.session = session or db_factory.get_database('POSTGREE').session

    def add(self, data) -> PostModel:
        m = PostModel(
            author_id=data.get('author_id'),
            title=data.get('title'),
            content=data.get('content'),
            category=data.get('category'),
            status=data.get('status'),
            created_at=data.get('created_at')
        )
        self.session.add(m)
        self.session.commit()
        self.session.refresh(m)
        return m

    def get_by_id(self, id: int) -> Optional[PostModel]:
        return self.session.query(PostModel).filter_by(id=id).first()

    def list(self) -> List[PostModel]:
        return self.session.query(PostModel).all()

    def update(self, data) -> PostModel:
        m = self.session.query(PostModel).filter_by(id=data.get('id')).first()
        if not m:
            raise ValueError('Not found')
        for k, v in data.items():
            if hasattr(m, k) and k != 'id':
                setattr(m, k, v)
        self.session.commit()
        return m

    def delete(self, id: int) -> None:
        m = self.session.query(PostModel).filter_by(id=id).first()
        if m:
            self.session.delete(m)
            self.session.commit()
