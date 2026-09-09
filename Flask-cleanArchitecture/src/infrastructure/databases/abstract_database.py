from abc import ABC, abstractmethod
# from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from config import DevelopmentConfig,Config, FactoryConfig

try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    _HAS_SQLALCHEMY = True
except Exception:
    # Allow static imports when SQLAlchemy is not installed in the environment
    _HAS_SQLALCHEMY = False


class AbstractDatabase(ABC):
    def __init__(self):
        self.database_uri = FactoryConfig.get_config("development").DATABASE_URI
        if _HAS_SQLALCHEMY:
            self.engine = create_engine(self.database_uri)
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            self.session = self.SessionLocal()
        else:
            self.engine = None
            self.SessionLocal = None
            self.session = None
    @abstractmethod
    def init_database(app):
        pass