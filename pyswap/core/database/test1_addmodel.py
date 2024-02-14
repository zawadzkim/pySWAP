"""TEST 1: Create a SWAPModel object and save it to the database"""

from sqlalchemy.orm import sessionmaker, declarative_base
from models import SWAPModel
from main import main
from sqlalchemy import create_engine, exc

db_path = "sqlite:///test.sqlite3"

main(db_path)

# Setup a database connection. Using in-memory database here.
engine = create_engine(db_path, echo=True)

Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# Create all tables derived from the EntityBase object
Base.metadata.create_all(engine)

# Declare a new row
first_item = SWAPModel(name="TEST MODEL 4",
                       swp=dict(a=1, b="foo", c=[1, 1, 2, 3, 5, 8, 13]),
                       drainage=dict(a=1, b="foo", c=[1, 1, 2, 3, 5, 8, 13]),
                       crop=dict(a=1, b="foo", c=[1, 1, 2, 3, 5, 8, 13]),
                       met=b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f')

# Insert it into the database
try:
    session.add(first_item)
    session.commit()
except exc.IntegrityError:
    session.rollback()
    print(f"Warning: Record with name '{first_item.name}' already exists and was not added.")
