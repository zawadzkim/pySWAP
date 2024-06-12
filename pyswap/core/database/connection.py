"""
This module is responsible for creating a connection to the database.

Classes:
    DatabaseConnection: Creates a connection to the database.
"""

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
import os
from .models import Base

"""
TODO: Implement an option to use different databases like MySQL, PostgreSQL, etc.
TODO: Implement a way to dump a database like postgresql, mysql, etc. to sqlite.
"""


class DatabaseConnection:
    """Creates a connection to the database.

    Upon calling the connect method, a check is made to see if the database file
    exists. If it does not, the file is created. The tables are then checked
    and created if they do not exist.

    Attributes:
        engine: The database engine.
        session: The database session.
        db_path: The path to the database file.

    Methods:
        connect: Connect to the database.
    """

    def __init__(self, db_path: str = 'pyswap.db'):
        self.engine = None
        self.session = None
        self.db_path = db_path
        self.connect()

    def connect(self):
        """Connect to the dabase or create a new one."""
        if os.path.exists(self.db_path):
            if os.path.isfile(self.db_path):
                print("Database exists. Connecting...")

        else:
            print("Database does not exist. Creating...")

        self.engine = create_engine(f'sqlite:///{self.db_path}')
        session = sessionmaker(bind=self.engine)
        self.session = session()

        # Check if tables exist in the database
        inspector = inspect(self.engine)
        table_names = inspector.get_table_names()

        for table in Base.metadata.tables.keys():
            if table not in table_names:
                print(
                    f"Table {table} does not exist in the database. Creating...")
                Base.metadata.tables[table].create(self.engine)
            else:
                print(f"Table {table} exists in the database.")
