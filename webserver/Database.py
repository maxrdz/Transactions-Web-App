import pymysql
from sqlalchemy import engine, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from google.cloud.sql.connector import connector


class DatabaseManager:
    """
    Handles the client connection to the MySQL
    server through the Google Cloud Platform
    for user authentication and accessing transactions.
    """
    def __init__(self):
        self.Base = declarative_base()
        self.configuration = {
            "instance": "wide-plating-343222:us-west4:transaction-db",
            "mysql-driver": "pymysql",
            "user": "server",
            "password": "mysqldb554982",
            "database": "TransactionDB"
        }
        self.engine = self.init_connection_engine()
        self.session = sessionmaker(bind=self.engine)

    def init_connection_engine(self) -> engine.Engine:
        def get_session() -> pymysql.connections.Connection:
            session: pymysql.connections.Connection = connector.connect(
                self.configuration["instance"],
                self.configuration["mysql-driver"],
                user=self.configuration["user"],
                password=self.configuration["password"],
                db=self.configuration["database"],
            )
            return session

        new_engine = create_engine(
            f"mysql+{self.configuration['mysql-driver']}://",
            creator=get_session,
        )
        return new_engine

    def authenticate_user(self, user, password):
        """Authenticate the username and password given."""
        pass
