from sqlalchemy.orm import sessionmaker, declarative_base
from models import SWAPModel, Iteration
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
first_item = SWAPModel(name="Test model 5",
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

# Assuming you have an existing SWAPModel with the name 'Test model'
model_name = 'Test model 3'

# Query the SWAPModel table to find the model with the given name
swap_model = session.query(SWAPModel).filter_by(name=model_name).first()

if swap_model:
    # Create a new Iteration instance with the desired data
    new_iteration = Iteration(
        model_id=swap_model.id,
    )

    # Add the new iteration to the session and commit the transaction
    session.add(new_iteration)
    session.commit()

    print(f"New Iteration added: {new_iteration}")
else:
    print(f"No SWAPModel found with the name '{model_name}'")
