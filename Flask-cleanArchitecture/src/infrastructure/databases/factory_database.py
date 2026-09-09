

from infrastructure.databases.abstract_database import AbstractDatabase


class FactoryDatabase:
    @staticmethod
    def get_database(database_type) -> AbstractDatabase:
        if database_type == 'MSSQL':
            from infrastructure.databases.database_mssql import DatabaseMSSQL
            return DatabaseMSSQL()
        if database_type == 'POSTGREE':
            # Return PostgreSQL database instance
            from infrastructure.databases.database_postgres import DatabasePostgres
            return DatabasePostgres()
        raise ValueError(f"Unsupported database type: {database_type}")