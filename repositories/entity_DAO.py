from abc import ABC, abstractmethod
import mariadb
from config.cursor_mariadb import CursorMariaDB

class AbstractDAO(ABC):
    """
    Abstract class for Data Access Objects (DAOs) with basic CRUD operations.
    """

    def __init__(self):
        """
        Initializes the DAO with the database connection details.
        """
        self.cursor = self.connect()
        

    @abstractmethod
    def connect(self):
        """
        Connects to the database.
        """
        return CursorMariaDB()

    @abstractmethod
    def disconnect(self, cursor):
        """
        Disconnects from the database.
        """
        cursor.close()
        print("Connection closed.")

    @abstractmethod
    def create(self, data):
        """
        Creates a new record in the database.

        Args:
            data: The data to be inserted.

        Returns:
            The ID of the newly created record.
        """
        pass

    @abstractmethod
    def read(self, id):
        """
        Retrieves a record from the database based on the given ID.

        Args:
            id: The ID of the record to retrieve.

        Returns:
            The retrieved record.
        """
        pass

    @abstractmethod
    def update(self, id, data):
        """
        Updates a record in the database based on the given ID.

        Args:
            id: The ID of the record to update.
            data: The updated data.

        Returns:
            True if the update was successful, False otherwise.
        """
        pass

    @abstractmethod
    def delete(self, id):
        """
        Deletes a record from the database based on the given ID.

        Args:
            id: The ID of the record to delete.

        Returns:
            True if the deletion was successful, False otherwise.
        """
        pass