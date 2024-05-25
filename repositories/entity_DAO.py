"""
This module contains the AbstractDAO class, which is an abstract class
for Data Access Objects (DAOs) with basic CRUD operations.
"""

from abc import ABC, abstractmethod
import mariadb
from config.cursor_mariadb import CursorMariaDB



class AbstractDAO(ABC):
    """
    Abstract class for Data Access Objects (DAOs) with basic CRUD operations.
    """

    def __init__(self, operation, *args):
        """
        Initializes the DAO with the database connection details.

        Args:
            operation: The operation to perform (CREATE, FIND, UPDATE, DELETE).
            *args: Additional arguments based on the operation.
        """
        self.conn, self.cursor = self.connect()
        if operation == "CREATE":
            self.create_result = self.create(*args)
        elif operation == "FIND":
            self.find_result = self.find_by_id(*args)
        elif operation == "UPDATE":
            self.update_result = self.update(*args)
        elif operation == "DELETE":
            self.delete_result = self.delete(*args)
        else:
            print ("Invalid operation")
        self.conn.close()

    @abstractmethod
    def connect(self):
        """
        Connects to the database.

        Returns:
            The database connection and cursor objects.
        """
        return CursorMariaDB()

    @abstractmethod
    def create(self, data_dict):
        """
        Creates a new record in the database.

        Args:
            data_dict: A dictionary containing the attributes and values of the record.

        Returns:
            True if the record was created successfully, False otherwise.
        """
        table_name = str(str(self.__class__.__name__), "_tb")
        columns = ", ".join([f"{column}" for column in data_dict.keys()])
        values_space = ", ".join("?" * len(data_dict.keys()))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values_space})"
        values = tuple(data_dict.values())

        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            print("Record created successfully")
            return True
        except mariadb.Error as e:
            print(f"Error creating record: {e}")
            self.conn.rollback()
            return False

    @abstractmethod
    def find_by_id(self, entity_id):
        """
        Finds a record in the database based on the given entity ID.

        Args:
            entity_id: The ID of the entity to search for.

        Returns:
            The matching record, or None if not found.
        """
        table_name = str(str(self.__class__.__name__), "_tb")
        query = f"SELECT * FROM {table_name} WHERE id = {entity_id}"
        try:
            self.cursor.execute(query)
            result = self.cursor
            if result:
                return result
            else:
                print("Record not found")
                return None
        except mariadb.Error as e:
            print(f"Error finding record: {e}")
            return None

    @abstractmethod
    def update(self, data_dict, entity_id):
        """
        Updates a record in the database based on the given ID.

        Args:
            data_dict: A dictionary containing the updated data.
            entity_id: The ID of the record to update.

        Returns:
            True if the update was successful, False otherwise.
        """
        table_name = str(str(self.__class__.__name__), "_tb")
        columns = ", ".join([f"{column} = ?" for column in data_dict.keys()])
        query = f"UPDATE {table_name} SET {columns} WHERE id = {entity_id}"
        values = tuple(data_dict.values())

        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            print("Record updated successfully")
            return True
        except mariadb.Error as e:
            print(f"Error updating record: {e}")
            self.conn.rollback()
            return False

    @abstractmethod
    def delete(self, entity_id):
        """
        Deletes a record from the database based on the given entity ID.

        Args:
            entity_id: The ID of the record to delete.

        Returns:
            True if the deletion was successful, False otherwise.
        """
        table_name = str(str(self.__class__.__name__), "_tb")
        query = f"DELETE FROM {table_name} WHERE id = {entity_id}"

        try:
            self.cursor.execute(query)
            self.conn.commit()
            print("Record deleted successfully")
            return True
        except mariadb.Error as e:
            print(f"Error deleting record: {e}")
            self.conn.rollback()
            return False
