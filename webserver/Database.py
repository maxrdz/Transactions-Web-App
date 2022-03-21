import os
from pymysql import connections
from sqlalchemy import engine, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from google.cloud.sql.connector import connector
from sqlalchemy import Column, String, SMALLINT, TIMESTAMP, Integer

DeclarativeBase = declarative_base()


class User(DeclarativeBase):
    __tablename__ = "users"
    user_name = Column(String(10), primary_key=True)
    password = Column(String(20))
    first_name = Column(String(30))
    last_name = Column(String(30))
    status = Column(SMALLINT)
    created_at = Column(TIMESTAMP)


class Transaction(DeclarativeBase):
    __tablename__ = "transactions"
    entry_id = Column(Integer, primary_key=True)
    timestamp = Column(TIMESTAMP)
    topic = Column(String(20))
    type = Column(SMALLINT)  # 0 = Spent, 1 = Deposit
    amount = Column(Integer)


class DatabaseManager:
    """
    Handles the client connection to the MySQL
    server through the Google Cloud Platform
    for user authentication and accessing transactions.
    """
    def __init__(self):
        self.configuration = {
            "creds": "gcp-service-key.json",
            "instance": "wide-plating-343222:us-west4:transaction-db",
            "sql-driver": "pymysql",
            "sql-user": "server",
            "sql-pass": "mysqldbpass",
            "sql-db": "TransactionDB"
        }
        # GCP API account credentials
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.configuration['creds']

        self.notify("Connecting to GCP Cloud MySQL server ..")
        self.engine = self.init_connection_engine()
        session = sessionmaker(bind=self.engine)
        self.session = session()
        self.notify("MySQL session created successfully.")

    def notify(self, string):
        print(f"[{self.__class__.__name__}]: {string}")

    def init_connection_engine(self) -> engine.Engine:
        def get_connect() -> connections.Connection:
            connect: connections.Connection = connector.connect(
                self.configuration["instance"],
                self.configuration["sql-driver"],
                user=self.configuration["sql-user"],
                password=self.configuration["sql-pass"],
                db=self.configuration["sql-db"],
            )
            return connect

        new_engine = create_engine(
            f"mysql+{self.configuration['sql-driver']}://",
            creator=get_connect,
        )
        return new_engine

    def authenticate_user(self, username: str, password: str):
        """
        Query and authenticate user credentials given.
        Returns query status, [user_found: ``Bool``, pass_matched: ``Bool``]
        """
        user_query = self.session.query(User)
        query_status = [False, False]

        for user in user_query:
            if user.user_name == username:
                query_status[0] = True
        # If username not found, exit method.
        if not query_status[0]:
            return query_status

        for user in user_query:
            if user.user_name == username and user.password == password:
                query_status[1] = True
                return query_status
        return query_status

    def create_transaction(self, topic: str, t_type: int, amount: int):
        """
        Add a new transaction entry to the database. For
        transaction type, 0 = Spent and 1 = Deposit.
        """
        transaction = Transaction()
        transaction.entry_id = None  # TODO: Generate ID
        transaction.timestamp = None  # TODO: Get Timestamp
        transaction.topic = topic
        transaction.type = t_type
        transaction.amount = amount
        self.session.add(transaction)
        self.session.commit()  # Insert new User to db table.
