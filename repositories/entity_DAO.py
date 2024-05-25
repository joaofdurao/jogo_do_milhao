"""
This module contains the EntityDAO class, which is an abstract class
for Data Access Objects (DAOs) with basic CRUD operations.
"""

import mariadb
from config.cursor_mariadb import CursorMariaDB



class EntityDAO():
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
        self.conn, self.cursor = self._connect()
        if operation == "CREATE":
            self.transaction_result = self._create(*args)
        elif operation == "FIND":
            self.transaction_result = self._find_by_id(*args)
        elif operation == "UPDATE":
            self.transaction_result = self._update(*args)
        elif operation == "DELETE":
            self.transaction_result = self._delete(*args)
        else:
            print ("Invalid operation")
        self.conn.close()

    def _connect(self):
        """
        Connects to the database.

        Returns:
            The database connection and cursor objects.
        """
        return CursorMariaDB().create_connection()

    def _create(self, data_dict):
        """
        Creates a new record in the database.

        Args:
            data_dict: A dictionary containing the attributes and values of the record.

        Returns:
            True if the record was created successfully, False otherwise.
        """
        table_name = str(self.__class__.__name__).lower() + "_tb"
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

    def _find_by_id(self, entity_id):
        """
        Finds a record in the database based on the given entity ID.

        Args:
            entity_id: The ID of the entity to search for.

        Returns:
            The matching record, or None if not found.
        """
        table_name = str(self.__class__.__name__).lower() + "_tb"
        query = f"SELECT * FROM {table_name} WHERE id = {entity_id}"
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            if result:
                return result
            else:
                print("Record not found")
                return None
        except mariadb.Error as e:
            print(f"Error finding record: {e}")
            return None

    def _update(self, data_dict, entity_id):
        """
        Updates a record in the database based on the given ID.

        Args:
            data_dict: A dictionary containing the updated data.
            entity_id: The ID of the record to update.

        Returns:
            True if the update was successful, False otherwise.
        """
        table_name = str(self.__class__.__name__).lower() + "_tb"
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

    def _delete(self, entity_id):
        """
        Deletes a record from the database based on the given entity ID.

        Args:
            entity_id: The ID of the record to delete.

        Returns:
            True if the deletion was successful, False otherwise.
        """
        table_name = str(self.__class__.__name__).lower() + "_tb"
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
