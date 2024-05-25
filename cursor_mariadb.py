"""This script connects to MariaDB Platform and creates a cursor object."""
import mariadb
import sys


class CursorMariaDB:

    def __init__(self, user, password, host, port, database):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        


    def connect(self):
        # Connect to MariaDB Platform
        try:
            conn = mariadb.connect(
                self.user="db_user",
                password="db_user_passwd",
                host="192.0.2.1",
                port=3306,
                database="employees"

            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

        # Get Cursor
        cur = conn.cursor()