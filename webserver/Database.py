from pymongo import MongoClient
import datetime


class DatabaseManager:
    """
    Handles the client connection to the local
    MongoDB server for user authentication
    and the transaction database.
    """
    def __init__(self):
        self.HOST = "127.0.0.1"
        self.PORT = 27017
        self.URI = f"mongodb://{self.HOST}:{self.PORT}/"
        self.Client = MongoClient(self.URI)
        self.UsersDB = self._get_db("Users")
        self.TransactionDB = self._get_db("Transactions")

    def authenticate(self, user, password):
        """Authenticate the username and password given."""
        pass

    def _get_db(self, db):
        """[PRIVATE] Gets database instance from MongoDB."""
        return self.Client[db]
