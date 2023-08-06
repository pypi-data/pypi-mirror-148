import pathlib
import sqlite3
import os
from sqlite3                                    import Error


class DatabaseOperation:
    """
        - Takes 1 required argument - database file name
        - Creates a DB file in the provided location or path
    """

    def __init__(self, db_file):
        self.db_file = db_file
        self.db_dir  = pathlib.Path(__file__).parents[0]

    def create_connection(self):
        """ create a database connection to a SQLite database """

        db_dir_input = input('\tDB FULLPATH:    ')
        if db_dir_input:
            self.db_dir = db_dir_input

        db_path = f'{self.db_dir}/{self.db_file}'

        if os.path.isfile(db_path):
            print('DB already exists!')
            return None

        conn = None
        try:
            conn = sqlite3.connect(db_path)
            print(f'Success ==> v{sqlite3.version}')
        except Error as e:
            print(f'Error ==> {e}')
        finally:
            if conn:
                conn.close()
