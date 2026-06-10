import os
import mysql.connector


class DbConnect:
    """Database connector. """
    def __init__(self, host=None, user=None, password=None, database=None):
        self.host = host or os.getenv('DB_HOST', 'localhost')
        self.user = user or os.getenv('DB_USER', 'root')
        self.password = password or os.getenv('DB_PASSWORD','')
        self.database = database or os.getenv('DB_DATABASE', 'world')
        self.connection = None
        self.cursor = None

    def connect(self):
        """Connects to DB and returns a cursor (or None on failure)."""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
            )

            print("** Connection to the database was successful. **")
            if self.connection.is_connected():
                # Use buffered cursor to allow rowcount and fetchall reliably
                self.cursor = self.connection.cursor()
                print("** cursor to the database created successful. **\n")
                return self.cursor

        except mysql.connector.Error as err:
            print(f"Error connecting to DB: {err}")
            self.connection = None
            self.cursor = None
            return None


    def db_commit(self):
        if self.connection.is_connected():
            self.connection.commit()


    def disconnect(self):
        """Disconnects from the database."""
        if self.cursor:
            try:
                self.cursor.close()
            except Exception:
                pass
        if self.connection:
            try:
                self.connection.close()
            except Exception:
                pass
            print("\n** Connection to the database has been closed. **")