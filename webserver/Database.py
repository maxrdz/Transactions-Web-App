import os
import uuid
from datetime import datetime, timedelta
from pymysql import connections
from sqlalchemy import engine, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from google.cloud.sql.connector import connector
from sqlalchemy import Column, String, SMALLINT, TIMESTAMP, Integer
from apscheduler.schedulers.background import BackgroundScheduler

DeclarativeBase = declarative_base()


class User(DeclarativeBase):
    __tablename__ = "users"
    user_name = Column(String(10), primary_key=True)
    password = Column(String(20))
    first_name = Column(String(30))
    last_name = Column(String(30))
    status = Column(SMALLINT)
    created_at = Column(TIMESTAMP)
    session_id = Column(String(40))  # (NULL if logged out)
    sid_expires = Column(TIMESTAMP)  # Defaults to last time updated

    def __repr__(self):  # How print() prints this object.
        return f"{self.user_name} | {self.password} | \
{self.first_name} | {self.last_name} | {self.status} | \
{self.created_at} | {self.session_id} | {self.sid_expires}"


class Transaction(DeclarativeBase):
    __tablename__ = "transactions"
    entry_id = Column(Integer, primary_key=True)
    timestamp = Column(TIMESTAMP)
    topic = Column(String(20))
    type = Column(SMALLINT)  # 0 = Spent, 1 = Deposit
    amount = Column(Integer)

    def __repr__(self):  # How print() prints this object.
        return f"{self.entry_id} | {self.timestamp} |\
{self.topic} | {self.type} | {self.amount}"


class DatabaseManager:
    """
    Handles the client connection to the MySQL
    server through the Google Cloud Platform
    for user authentication and accessing transactions.
    """
    def __init__(self):
        self.gcp_config = {
            "creds": "gcp-service-key.json",
            "instance": "wide-plating-343222:us-west4:transaction-db",
            "sql-driver": "pymysql",
            "sql-user": "server",
            "sql-pass": "mysqldbpass",
            "sql-db": "TransactionDB"
        }
        self.sessions_config = {
            "valid_time": 20,  # (minutes)
            "check_interval": 10  # (minutes)
        }
        # Set GCP API service account keys
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.gcp_config['creds']

        # Initialize connection to the MySQL server
        self.notify("Connecting to GCP Cloud MySQL server ..")
        self.engine = self.init_connection_engine()
        session = sessionmaker(bind=self.engine)
        self.session = session()
        self.notify("MySQL session created successfully.")

        # Initialize scheduler (user session expiration)
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(
            self.check_session_expirations, "interval",
            minutes=self.sessions_config['check_interval'])
        self.scheduler.start()

    def notify(self, string):
        print(f"[{self.__class__.__name__}]: {string}")

    def init_connection_engine(self) -> engine.Engine:
        def get_connect() -> connections.Connection:
            connect: connections.Connection = connector.connect(
                self.gcp_config["instance"],
                self.gcp_config["sql-driver"],
                user=self.gcp_config["sql-user"],
                password=self.gcp_config["sql-pass"],
                db=self.gcp_config["sql-db"]
            )
            return connect

        new_engine = create_engine(
            f"mysql+{self.gcp_config['sql-driver']}://",
            creator=get_connect,
        )
        return new_engine

    def authenticate_user(self, username: str, password: str):
        """
        Query and authenticate user credentials given.
        Returns query status, [user_found: ``Bool``, pass_matched: ``Bool``]
        """
        user = self.session.query(User).get(username)
        credentials_status = [False, False]

        if user is None:
            self.notify(f"Failed to authenticate. [User not found]")
            return credentials_status
        credentials_status[0] = True  # Username found

        if user.status != 1:
            return False  # Check if user account is disabled

        if user.password == password:
            credentials_status[1] = True
            self.notify(f"{username} authenticated!")
            return credentials_status

        self.notify(f"{username} failed to authenticate. [Wrong Password]")
        return credentials_status

    def create_session(self, username: str):
        """
        Create and assign new Session ID to User specified.
        """
        user = self.session.query(User).get(username)

        if user.session_id is not None:
            self.notify(f"{username} already has an active session!")
            return user.session_id  # The User already has a session.

        new_sid = uuid.uuid4()
        user.session_id = new_sid
        user.sid_expires = \
            datetime.now() + timedelta(minutes=self.sessions_config['valid_time'])

        self.session.commit()  # Insert data to database.
        self.notify(f"{username} started a new session.")
        return new_sid

    def end_session(self, username: str):
        """
        End an existing session for a User and delete SID in database.
        """
        user = self.session.query(User).get(username)
        user.session_id = None
        self.session.commit()
        self.notify(f"{username}'s session was ended.")

    def validate_session(self, username: str, session_id: str):
        """
        Validate the Session ID for an existing user in the database.
        """
        user = self.session.query(User).get(username)
        if user.session_id == session_id:
            return True
        return False

    def check_session_expirations(self):
        """
        Scheduled event that checks the database for expired sessions.
        """
        user_table = self.session.query(User)

        for user in user_table:
            if user.session_id is not None:
                # Check expiration if SID exists
                expiration = user.sid_expires
                if datetime.now() > expiration:
                    self.end_session(user.user_name)

    def create_transaction(self, topic: str, t_type: int, amount: int):
        """
        Add a new transaction entry to the database. For
        transaction type, 0 = Spent and 1 = Deposit.
        """
        transaction = Transaction()
        transaction.entry_id = uuid.uuid4()
        transaction.timestamp = None  # TODO: Get Timestamp
        transaction.topic = topic
        transaction.type = t_type
        transaction.amount = amount
        self.session.add(transaction)
        self.session.commit()  # Insert new Transaction to database.

    def print_db_table(self, table_class: DeclarativeBase):
        """Prints entire table from database. (Debugging Purposes)"""
        if User.__class__ is not type(DeclarativeBase):
            self.notify("print_db_table(): Table not of type 'DeclarativeBase'")
            return
        table_query = self.session.query(table_class)
        table = self.session.execute(table_query)
        for row_object in table:
            print(row_object)
